#!/usr/bin/env python3
"""
MBI Keyword Extraction Pipeline
================================
Decision-Support-System | Data2Dollar | University of St.Gallen

What this script does:
  1. Loads 0_mbi_curriculum_database_withSections.csv
  2. For each course: combines learning_objectives_raw + course_content_raw
  3. Calls OpenAI API → extracts English keywords (hard skills, tools, methods, domains)
  4. Saves the result in a new column 'extracted_keywords' using | as separator
  5. Writes enriched CSV (all original columns preserved)

Safety features built in:
  - Checkpointing : progress saved to JSON after every single row
                    → safe to Ctrl+C and resume at any time
  - Keyword separator: '|' (pipe), NOT comma
                    → no conflict with the semicolon-based CSV format
  - Test mode:   --test flag processes only N rows (default 3) before full run
  - Atomic writes: checkpoint file is written via tmp → rename (no corruption)

Usage:
  # Validate with 3 rows first:
  python extract_keywords_pipeline.py --test

  # Use more test rows:
  python extract_keywords_pipeline.py --test --test-rows 5

  # Full production run:
  python extract_keywords_pipeline.py

  # Use a better model for production:
  python extract_keywords_pipeline.py --model gpt-4o
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
from openai import APIConnectionError, APIError, OpenAI, RateLimitError

# ============================================================================
# SECTION 1 — CONFIGURATION
# Edit these values before running. CLI flags can override MODEL at runtime.
# ============================================================================

INPUT_FILE      = "0_mbi_curriculum_database_withSections.csv"
OUTPUT_FILE     = "mbi_curriculum_enriched_keywords.csv"
CHECKPOINT_FILE = ".keyword_extraction_checkpoint.json"   # hidden dot-file

CSV_DELIMITER   = ";"
CSV_ENCODING    = "utf-8-sig"          # handles BOM-encoded files from Excel

KEYWORD_SEPARATOR = "|"               # pipe — safe inside semicolon-CSV cells

OPENAI_MODEL    = "gpt-4o-mini"        # override via --model flag
TEMPERATURE     = 0.2                  # low = more deterministic output
MAX_RETRIES     = 3
RETRY_DELAY_SEC = 5                    # base delay between retries (doubles each attempt)


# ============================================================================
# SECTION 2 — PROMPT ENGINEERING
#
# SYSTEM_PROMPT defines the LLM's role and strict output rules.
# build_user_prompt() formats the actual course data into the message.
#
# To customise extraction behaviour (e.g. focus on Founder vs. Corporate keywords),
# edit SYSTEM_PROMPT or swap it out per-run using a persona config.
# ============================================================================

SYSTEM_PROMPT = """\
You are an expert curriculum analyst and labour-market keyword extractor.
Your task: read a university course description and extract structured, \
market-relevant keywords that can be matched against startup trends, \
VC investment themes, and corporate job postings.

Extraction categories (cover all that apply):
  - Hard skills  (e.g. machine learning, financial modelling, A/B testing)
  - Tools & software  (e.g. Python, MongoDB, Tableau, Figma)
  - Methods & frameworks  (e.g. Design Thinking, Lean Startup, CRISP-DM)
  - Domain knowledge  (e.g. platform economy, supply chain, ESG)

Output rules — follow EXACTLY:
  1. English only. Translate German terms precisely.
  2. Keywords only — no sentences, no explanations, no numbering.
  3. Minimum 6, maximum 15 keywords.
  4. Separate keywords with a pipe character  |  with NO spaces around it.
  5. Output a SINGLE LINE. Example:
     machine learning|Python|NoSQL|data pipeline|business model design|platform economy
  6. Do NOT output commas, bullet points, or any text outside the keyword list.\
"""


def build_user_prompt(course_title: str, objectives: str, content: str) -> str:
    """Assemble the user turn from the three course fields."""
    obj_text = objectives if objectives and objectives.lower() != "nan" else "(not provided)"
    con_text = content    if content    and content.lower()    != "nan" else "(not provided)"
    return (
        f"Course title: {course_title}\n\n"
        f"Learning objectives:\n{obj_text}\n\n"
        f"Course content:\n{con_text}\n\n"
        "Extract keywords following the system instructions."
    )


# ============================================================================
# SECTION 3 — CHECKPOINTING
# Checkpoints are stored as  {course_id: "kw1|kw2|kw3"}  in a JSON file.
# On restart the pipeline skips rows whose course_id already appears there.
# ============================================================================

def load_checkpoint(path: str) -> dict:
    """Return the checkpoint dict from disk, or an empty dict if none exists."""
    p = Path(path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkpoint(path: str, data: dict) -> None:
    """
    Atomically persist the checkpoint dictionary.
    Writes to a .tmp file first, then renames — prevents corruption on crash.
    """
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    Path(tmp_path).replace(path)


# ============================================================================
# SECTION 4 — OPENAI CLIENT & EXTRACTION LOGIC
# ============================================================================

def initialize_client(model_override: str | None = None) -> tuple[OpenAI, str]:
    """
    Create and return an OpenAI client plus the model name to use.
    Raises SystemExit with a clear message if the API key is missing.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "[ERROR] OPENAI_API_KEY environment variable is not set.\n"
            "Fix:  $env:OPENAI_API_KEY='sk-...your-key...'  (PowerShell)\n"
            "      export OPENAI_API_KEY='sk-...'            (bash/zsh)"
        )
    model = model_override or OPENAI_MODEL
    return OpenAI(api_key=api_key), model


def sanitize_keywords(raw: str) -> str:
    """
    Clean the raw LLM response string:
      - Model may return commas despite instructions → convert to pipes.
      - Strip whitespace around each keyword.
      - Deduplicate (case-insensitive), preserving order.
      - Return pipe-separated string.
    """
    # Detect format: if no pipe but commas present, the model disobeyed format rules
    if "|" not in raw and "," in raw:
        parts = [kw.strip() for kw in raw.split(",")]
    else:
        parts = [kw.strip() for kw in raw.split("|")]

    seen: set[str] = set()
    clean: list[str] = []
    for kw in parts:
        kw_lower = kw.lower().strip()
        if kw_lower and kw_lower not in seen:
            seen.add(kw_lower)
            clean.append(kw.strip())

    return KEYWORD_SEPARATOR.join(clean)


def extract_keywords_for_row(
    client: OpenAI,
    model: str,
    course_title: str,
    objectives: str,
    content: str,
) -> str:
    """
    Send a single course to the OpenAI API and return a pipe-separated keyword string.

    Retry logic:
      - RateLimitError  → wait 60 s (API quota exhausted)
      - APIError / ConnectionError → exponential back-off (5 s, 10 s, 15 s)
      - Any other exception → log and give up immediately

    Returns an empty string if all retries fail (row is still checkpointed so the
    pipeline never re-tries a broken row unnecessarily).
    """
    user_prompt = build_user_prompt(course_title, objectives, content)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_prompt},
                ],
            )
            raw = response.choices[0].message.content.strip()
            return sanitize_keywords(raw)

        except RateLimitError:
            wait = 60
            print(f"    [Rate limit] Waiting {wait}s… (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait)

        except (APIError, APIConnectionError) as exc:
            wait = RETRY_DELAY_SEC * attempt
            print(f"    [API Error] {exc} — retry {attempt}/{MAX_RETRIES} in {wait}s")
            time.sleep(wait)

        except Exception as exc:  # noqa: BLE001
            print(f"    [Unexpected error] {exc} — skipping row")
            break

    print(f"    [FAILED] No keywords extracted after {MAX_RETRIES} attempts.")
    return ""


# ============================================================================
# SECTION 5 — MAIN PIPELINE ORCHESTRATION
# ============================================================================

def run_pipeline(
    test_mode: bool = False,
    test_rows: int = 3,
    model_override: str | None = None,
) -> None:
    print("=" * 65)
    print("  MBI Keyword Extraction Pipeline — Data2Dollar / HSG")
    mode_label = f"TEST ({test_rows} rows)" if test_mode else "FULL RUN"
    print(f"  Mode  : {mode_label}")
    print(f"  Model : {model_override or OPENAI_MODEL}")
    print("=" * 65)

    # ── Step 1: Load CSV ──────────────────────────────────────────────────────
    df = pd.read_csv(INPUT_FILE, sep=CSV_DELIMITER, encoding=CSV_ENCODING, dtype=str)
    print(f"\n[1/5] Loaded {len(df)} rows  from  {INPUT_FILE}")

    if test_mode:
        df = df.head(test_rows).copy()
        print(f"      [TEST MODE] Trimmed to {test_rows} rows.")

    # ── Step 2: Load checkpoint ───────────────────────────────────────────────
    checkpoint = load_checkpoint(CHECKPOINT_FILE)
    print(f"[2/5] Checkpoint: {len(checkpoint)} rows already done → will be skipped")

    # ── Step 3: Initialize API client ─────────────────────────────────────────
    client, model = initialize_client(model_override)
    print(f"[3/5] OpenAI client ready  (model: {model})\n")

    # ── Step 4: Extract keywords row by row ───────────────────────────────────
    keywords_col: list[str] = []
    new_count = 0

    for idx, row in df.iterrows():
        # Use course_id as the stable checkpoint key; fall back to row index
        course_id    = str(row.get("course_id", idx))
        course_title = str(row.get("course_title", ""))
        objectives   = str(row.get("learning_objectives_raw", ""))
        content      = str(row.get("course_content_raw", ""))

        # ── Skip if already in checkpoint ──
        if course_id in checkpoint:
            keywords_col.append(checkpoint[course_id])
            continue

        # ── Extract ──
        short_title = course_title[:55] + "…" if len(course_title) > 55 else course_title
        print(f"  → [{course_id}] {short_title}")
        kws = extract_keywords_for_row(client, model, course_title, objectives, content)

        kw_count = kws.count(KEYWORD_SEPARATOR) + 1 if kws else 0
        preview  = kws[:75] + "…" if len(kws) > 75 else kws
        print(f"    [OK] {kw_count} keywords: {preview}\n")

        # ── Save to checkpoint immediately ──
        checkpoint[course_id] = kws
        save_checkpoint(CHECKPOINT_FILE, checkpoint)

        keywords_col.append(kws)
        new_count += 1

    # ── Step 5: Write enriched CSV ────────────────────────────────────────────
    df["extracted_keywords"] = keywords_col
    df.to_csv(OUTPUT_FILE, sep=CSV_DELIMITER, index=False, encoding=CSV_ENCODING)

    print(f"[4/5] Extracted {new_count} new rows  (skipped {len(checkpoint) - new_count} from checkpoint)")
    print(f"[5/5] Output saved to  {OUTPUT_FILE}")

    # ── Test mode: print a readable preview ───────────────────────────────────
    if test_mode:
        print("\n" + "─" * 65)
        print("  TEST RESULTS PREVIEW")
        print("─" * 65)
        for _, row in df[["course_title", "extracted_keywords"]].iterrows():
            title = str(row["course_title"])[:38]
            kws   = str(row["extracted_keywords"])
            print(f"  {title:<38} │ {kws[:60]}")
        print("─" * 65)
        print("\nIf the results look correct, run without --test for the full dataset.")


# ============================================================================
# SECTION 6 — ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract English keywords from MBI course descriptions via OpenAI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: process only the first N rows (see --test-rows).",
    )
    parser.add_argument(
        "--test-rows",
        type=int,
        default=3,
        metavar="N",
        help="Number of rows to process in test mode (default: 3).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL",
        help=f"OpenAI model to use (default: {OPENAI_MODEL}).",
    )
    args = parser.parse_args()

    run_pipeline(
        test_mode=args.test,
        test_rows=args.test_rows,
        model_override=args.model,
    )
