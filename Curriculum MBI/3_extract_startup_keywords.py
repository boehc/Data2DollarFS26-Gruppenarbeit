#!/usr/bin/env python3
"""
Extract Keywords for Startup & Scale-up Persona
Erstellt CSV mit gefilterten Keywords und Häufigkeitsanalyse
"""

import pandas as pd
from collections import Counter

INPUT_FILE = "0.1_mbi_curriculum_enriched_keywords.csv"
OUTPUT_CSV = "Startup_Scaleup_keywords.csv"
OUTPUT_ANALYSIS = "Startup_Scaleup_keywords_analysis.txt"

DELIMITER = ";"
KEYWORD_SEPARATOR = "|"

def main():
    print("=" * 70)
    print("  Startup & Scale-up Persona -- Keyword Extraction")
    print("=" * 70)

    # Step 1: Load
    try:
        df = pd.read_csv(INPUT_FILE, sep=DELIMITER, encoding="utf-8-sig", dtype=str)
        print(f"\n[1/4] Loaded {len(df)} courses")
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    # Step 2: Filter
    startup_col = "Startup & Scale-up"
    if startup_col not in df.columns:
        print(f"[ERROR] Column '{startup_col}' not found!")
        print(f"Available columns: {list(df.columns)}")
        return False

    df_startup = df[df[startup_col].astype(str) == "1"].copy()
    print(f"[2/4] Found {len(df_startup)} 'Startup & Scale-up' courses")

    if len(df_startup) == 0:
        print("[WARNING] No courses found!")
        return False

    # Step 3: Extract keywords
    rows_output = []
    all_keywords_flat = []

    for idx, row in df_startup.iterrows():
        course_id = str(row.get("course_id", "")).strip()
        course_title = str(row.get("course_title", "")).strip()
        keywords_raw = str(row.get("extracted_keywords", "")).strip()

        if keywords_raw and keywords_raw.lower() not in ["nan", "none", ""]:
            keywords = [kw.strip() for kw in keywords_raw.split(KEYWORD_SEPARATOR) if kw.strip()]
        else:
            keywords = []

        rows_output.append({
            "course_id": course_id,
            "course_title": course_title,
            "keywords_count": len(keywords),
            "extracted_keywords": keywords_raw,
        })
        all_keywords_flat.extend(keywords)

    df_output = pd.DataFrame(rows_output)
    df_output.to_csv(OUTPUT_CSV, sep=DELIMITER, index=False, encoding="utf-8-sig")
    print(f"[3/4] Saved to {OUTPUT_CSV}")

    # Step 4: Analyze
    print(f"[4/4] Analyzing...")
    keyword_counts = Counter(all_keywords_flat)
    total_unique = len(keyword_counts)
    total_mentions = sum(keyword_counts.values())
    duplicates = {kw: count for kw, count in keyword_counts.items() if count > 1}
    duplicates_sorted = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)

    # Write analysis
    with open(OUTPUT_ANALYSIS, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("STARTUP & SCALE-UP KEYWORD ANALYSIS\n")
        f.write("=" * 70 + "\n\n")

        f.write("SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"Courses in category:                        {len(df_startup)}\n")
        f.write(f"Total unique keywords:                      {total_unique}\n")
        f.write(f"Total keyword mentions:                     {total_mentions}\n")
        f.write(f"Average keywords per course:                {total_mentions / len(df_startup):.1f}\n")
        f.write(f"Keywords appearing multiple times:          {len(duplicates)}\n")
        f.write(f"Overlap percentage:                         {(len(duplicates) / total_unique * 100):.1f}%\n\n")

        f.write("TOP 20 MOST COMMON KEYWORDS\n")
        f.write("-" * 70 + "\n")
        for rank, (kw, count) in enumerate(keyword_counts.most_common(20), 1):
            f.write(f"{rank:2d}. {kw:<40s}  {count:3d}x\n")
        f.write("\n")

        if duplicates_sorted:
            f.write("KEYWORDS APPEARING MULTIPLE TIMES\n")
            f.write("-" * 70 + "\n")
            for kw, count in duplicates_sorted:
                f.write(f"  {kw:<45s}  {count:2d}x\n")

        f.write("\n")
        f.write("ALL KEYWORDS (alphabetically sorted)\n")
        f.write("-" * 70 + "\n")
        for kw in sorted(keyword_counts.keys()):
            count = keyword_counts[kw]
            f.write(f"{kw:<50s}  {count}x\n")

    print(f"\n[OK] Analysis saved to {OUTPUT_ANALYSIS}")

    print("\n" + "=" * 70)
    print(f"Courses:                    {len(df_startup)}")
    print(f"Unique keywords:            {total_unique}")
    print(f"Total mentions:             {total_mentions}")
    print(f"Keywords 2+ times:          {len(duplicates)}")
    print(f"Overlap rate:               {(len(duplicates) / total_unique * 100):.1f}%")

    if duplicates_sorted:
        print(f"\nTOP 5 OVERLAPS:")
        for kw, count in duplicates_sorted[:5]:
            print(f"  + {kw:.<40s} {count}x")

    print("\n" + "=" * 70)
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
