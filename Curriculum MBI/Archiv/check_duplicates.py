"""Check for duplicate titles in v5 database"""

import pandas as pd
from pathlib import Path

csv_file = Path("mbi_curriculum_database_v5_final.csv")
df = pd.read_csv(csv_file, encoding='utf-8-sig', sep=';')

print("\n" + "="*80)
print("DUPLICATE TITLE CHECK")
print("="*80 + "\n")

# Find duplicates
title_counts = df['course_title'].value_counts()
duplicates = title_counts[title_counts > 1]

if len(duplicates) > 0:
    print(f"Found {len(duplicates)} DUPLICATE TITLES:\n")
    
    for title, count in duplicates.items():
        print(f"  [{count}x] {title}")
        # Show course IDs for each duplicate
        courses = df[df['course_title'] == title][['course_id', 'course_title']].values
        for course_id, _ in courses:
            print(f"       └─ {course_id}")
        print()
else:
    print("✓ No duplicate titles found. All titles are unique.\n")

print("="*80)
print(f"Total unique titles: {df['course_title'].nunique()}/{len(df)}")
print("="*80 + "\n")
