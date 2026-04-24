#!/usr/bin/env python3
"""
build_assessment_data.py  (v2 — weighted matching)

Reads the two authoritative categorized CSVs and emits three JSON files used
by the Self-Assessment page.  Compared to v1 this adds:

  • IDF weight per skill (rare skills count more)
  • Group weights (FD/FK dominate over SK/PK)
  • Duplicate merge (same title+company kept once with a count)
  • Seniority detection from job title (junior / mid / senior / lead)
  • Experience requirement (FD_Berufserfahrung_Jahre) carried through
  • Numerical intensity scores (Fachkompetenz_Score, Fachdetail_Score, …)
  • Extracted free-text keywords per course (from the _enriched CSV)
  • ECTS → course weight (6 ECTS ≈ 2×, 4 ECTS ≈ 1.3×, 3 ECTS ≈ 1×)
  • Sparseness flag on jobs with <4 skills

Outputs  (interactive_explorer_v2/data/):
  courses.json, jobs.json, skills.json
"""
from __future__ import annotations
import csv, json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
COURSES_CSV   = BASE / "Visualisierung MBI Curriculum" / "mbi_curriculum_kategorisiert.csv"
COURSES_KW_CSV= BASE / "Visualisierung MBI Curriculum" / "mbi_curriculum_enriched_keywords.csv"
JOBS_CSV      = BASE / "Job Datensatz" / "Kategorisierung" / "jobs_kategorisiert_ms_detail.csv"
OUT_DIR       = ROOT / "data"
OUT_DIR.mkdir(exist_ok=True)

# ─── Config ────────────────────────────────────────────────────────────
COURSE_PROFILE_COLS = {
    "Business Development":      "bd",
    "Digital Channel & CRM":     "dc",
    "Startup & Scale-up":        "su",
    "Supply Chain & Operations": "sc",
    "Technology Architecture":   "ts",
    "Digital Transformation":    "tm",
}
JOB_PROFILE_MAP = {
    "Business Developer":                       "bd",
    "Digital Channel & Relationship Manager":   "dc",
    "Startup & Technology Entrepreneur":        "su",
    "Supply Chain & Operations Manager":        "sc",
    "IT Manager":                               "ts",
}
# Group weighting — FD/FK matter more than generic soft-skills
GROUP_WEIGHT = {"FD": 1.6, "FK": 1.0, "MK": 0.9, "SK": 0.7, "PK": 0.6}
GROUP_LABELS = {
    "FK": "Fachkompetenz", "FD": "TechSkill", "SK": "Sozialkompetenz",
    "MK": "Methodenkompetenz", "PK": "Personalkompetenz",
}
# ECTS → how strongly a course contributes
ECTS_WEIGHT = {"3": 1.0, "4": 1.3, "6": 2.0}
# Seniority detection (first match wins, order matters)
SENIORITY_RE = [
    ("lead",   re.compile(r"\b(lead|head of|chief|cto|cio|director|vp)\b", re.I)),
    ("senior", re.compile(r"\b(senior|sr\.?|principal|expert|staff)\b",    re.I)),
    ("junior", re.compile(r"\b(junior|jr\.?|trainee|praktik|intern|werkstudent|einsteiger)\b", re.I)),
]

def prettify(col: str) -> str:
    return re.sub(r"^(FK|FD|SK|MK|PK)_", "", col).replace("_", " ").strip()

def read_csv(path: Path, delim: str | None = None) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        first = fh.readline()
        fh.seek(0)
        d = delim or (";" if first.count(";") > first.count(",") else ",")
        return list(csv.DictReader(fh, delimiter=d))

def skill_columns(header: list[str]) -> list[str]:
    return [c for c in header
            if re.match(r"^(FK|FD|SK|MK|PK)_", c) and c != "FD_Berufserfahrung_Jahre"]

def detect_seniority(title: str) -> str:
    for lvl, rx in SENIORITY_RE:
        if rx.search(title): return lvl
    return "mid"

def to_int(v, default=0):
    try: return int(str(v).strip() or default)
    except (ValueError, TypeError): return default

# ─── Load courses (base + keywords) ────────────────────────────────────
print("Loading courses…")
course_rows = read_csv(COURSES_CSV)
kw_rows     = read_csv(COURSES_KW_CSV) if COURSES_KW_CSV.exists() else []
kw_map: dict[str, list[str]] = {}
for r in kw_rows:
    key = (r.get("course_id") or r.get("course_title") or "").strip()
    raw = (r.get("extracted_keywords") or "").strip()
    if key and raw:
        # pipe-separated, normalize to lowercase, dedupe, keep up to 20
        tokens = [t.strip().lower() for t in raw.split("|") if t.strip()]
        seen, kws = set(), []
        for t in tokens:
            if t not in seen and len(t) >= 3:
                seen.add(t); kws.append(t)
            if len(kws) >= 20: break
        kw_map[key] = kws

course_header = list(course_rows[0].keys()) if course_rows else []
course_skill_cols = skill_columns(course_header)

courses = []
for r in course_rows:
    title = (r.get("course_title") or "").strip()
    if not title: continue
    cid = (r.get("course_id") or "").strip() or title
    profiles = [k for col, k in COURSE_PROFILE_COLS.items()
                if str(r.get(col, "0")).strip() == "1"]
    skills = [c for c in course_skill_cols if str(r.get(c, "0")).strip() == "1"]
    ects = (r.get("ects") or "").strip()
    courses.append({
        "id":       cid,
        "title":    title,
        "ects":     ects,
        "weight":   ECTS_WEIGHT.get(ects, 1.0),
        "lang":     (r.get("language") or "").strip(),
        "profiles": profiles,
        "skills":   skills,
        "keywords": kw_map.get(cid) or kw_map.get(title) or [],
    })

# ─── Load jobs ─────────────────────────────────────────────────────────
print("Loading jobs…")
job_rows = read_csv(JOBS_CSV)
job_header = list(job_rows[0].keys()) if job_rows else []
job_skill_cols = skill_columns(job_header)

raw_jobs = []
for i, r in enumerate(job_rows):
    title = (r.get("job_title") or "").strip()
    if not title: continue
    raw_profile = (r.get("job_profil") or "").strip()
    profile_key = JOB_PROFILE_MAP.get(raw_profile, "other")
    skills = [c for c in job_skill_cols if str(r.get(c, "0")).strip() == "1"]
    if not skills:
        continue  # no signal at all → useless

    raw_jobs.append({
        "id":         i,
        "title":      title,
        "company":    (r.get("company") or "").strip(),
        "location":   (r.get("location") or "").strip(),
        "url":        (r.get("url") or "").strip(),
        "source":     (r.get("quelle") or "").strip(),
        "profile":    profile_key,
        "skills":     skills,
        "seniority":  detect_seniority(title),
        "years_exp":  to_int(r.get("FD_Berufserfahrung_Jahre"), 0),
        "sparse":     len(skills) < 4,
        "scores": {
            "fk":    to_int(r.get("Fachkompetenz_Score")),
            "fd":    to_int(r.get("Fachdetail_Score")),
            "sk":    to_int(r.get("Sozialkompetenz_Score")),
            "mk":    to_int(r.get("Methodenkompetenz_Score")),
            "pk":    to_int(r.get("Personalkompetenz_Score")),
            "ms":    to_int(r.get("MS_Tools_Score")),
        },
    })

# ─── Deduplicate jobs (same title+company) ────────────────────────────
print("Deduplicating jobs…")
buckets: dict[tuple, list[dict]] = defaultdict(list)
for j in raw_jobs:
    key = (j["title"].strip().lower(), j["company"].strip().lower())
    buckets[key].append(j)

jobs = []
for key, group in buckets.items():
    if len(group) == 1:
        j = group[0]; j["count"] = 1
        jobs.append(j); continue
    # Merge: union of skills, max years_exp, keep the first canonical record
    canon = dict(group[0])
    union = set()
    for g in group: union.update(g["skills"])
    canon["skills"]    = sorted(union)
    canon["years_exp"] = max(g["years_exp"] for g in group)
    canon["count"]     = len(group)
    canon["sparse"]    = len(canon["skills"]) < 4
    # average the numeric scores
    sc = {k: 0 for k in group[0]["scores"]}
    for g in group:
        for k, v in g["scores"].items(): sc[k] += v
    canon["scores"] = {k: round(v / len(group), 2) for k, v in sc.items()}
    jobs.append(canon)

print(f"  raw jobs       : {len(raw_jobs)}")
print(f"  after dedup    : {len(jobs)}  (merged {len(raw_jobs)-len(jobs)} duplicates)")
print(f"  sparse (<4 sk) : {sum(1 for j in jobs if j['sparse'])}")

# ─── Compute IDF weights across the job corpus ────────────────────────
N = len(jobs)
doc_freq = Counter()
for j in jobs:
    for s in set(j["skills"]): doc_freq[s] += 1

def idf(s: str) -> float:
    # smoothed IDF; clamp to sensible range
    df = doc_freq.get(s, 0)
    return math.log((N + 1) / (df + 1)) + 1.0  # ≥ 1.0

# ─── Build skills taxonomy with weights ────────────────────────────────
all_cols = set(course_skill_cols) | set(job_skill_cols)
skills = {}
for col in sorted(all_cols):
    group = col.split("_", 1)[0]
    idf_w = round(idf(col), 3)
    grp_w = GROUP_WEIGHT.get(group, 1.0)
    skills[col] = {
        "label":       prettify(col),
        "group":       group,
        "group_label": GROUP_LABELS.get(group, group),
        "group_weight": grp_w,
        "idf":          idf_w,
        "weight":       round(idf_w * grp_w, 3),  # final pre-computed weight
        "job_freq":     doc_freq.get(col, 0),
        "job_pct":      round(doc_freq.get(col, 0) / max(N, 1) * 100, 1),
    }

# ─── Write ─────────────────────────────────────────────────────────────
def dump(path: Path, obj, pretty=False):
    kw = {"indent": 2} if pretty else {"separators": (",", ":")}
    path.write_text(json.dumps(obj, ensure_ascii=False, **kw), encoding="utf-8")

dump(OUT_DIR / "courses.json", courses)
dump(OUT_DIR / "jobs.json",    jobs)
dump(OUT_DIR / "skills.json",  skills, pretty=True)

# ─── Report ────────────────────────────────────────────────────────────
print(f"\n✓ courses.json  {len(courses):>5} courses "
      f"({sum(1 for c in courses if c['keywords'])} with keywords)")
print(f"✓ jobs.json     {len(jobs):>5} jobs  "
      f"(seniority: {Counter(j['seniority'] for j in jobs)})")
print(f"✓ skills.json   {len(skills):>5} skills")
top_w = sorted(skills.items(), key=lambda kv: -kv[1]["weight"])[:5]
bot_w = sorted(skills.items(), key=lambda kv: kv[1]["weight"])[:5]
print("\n  Top-5 gewichtete Skills (diskriminativ):")
for k, v in top_w:
    print(f"    w={v['weight']:5.2f}  [{v['group']}]  {v['label']:30s}  ({v['job_pct']:4.1f}% d. Jobs)")
print("\n  Bottom-5 gewichtete Skills (generisch):")
for k, v in bot_w:
    print(f"    w={v['weight']:5.2f}  [{v['group']}]  {v['label']:30s}  ({v['job_pct']:4.1f}% d. Jobs)")
