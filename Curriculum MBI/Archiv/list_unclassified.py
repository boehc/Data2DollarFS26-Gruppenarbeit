"""List unclassified courses"""

import pandas as pd

df = pd.read_csv("mbi_curriculum_database_v5_multiprofile.csv", encoding='utf-8-sig', sep=';')

# Get profile columns
profile_cols = df.columns[7:]

# Find courses with no profile assigned
df['profile_count'] = df[profile_cols].sum(axis=1)
unclassified = df[df['profile_count'] == 0]

print("\n" + "="*80)
print(f"UNCLASSIFIED COURSES ({len(unclassified)})")
print("="*80 + "\n")

for idx, row in unclassified.iterrows():
    print(f"{row['course_id']:10s} - {row['course_title']}")

print("\n" + "="*80 + "\n")
