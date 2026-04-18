"""Preview the new multi-profile CSV"""

import pandas as pd

df = pd.read_csv("mbi_curriculum_database_v5_multiprofile.csv", encoding='utf-8-sig', sep=';')

print("\n" + "="*80)
print("NEW MULTI-PROFILE CSV STRUCTURE")
print("="*80 + "\n")

print("Columns:", list(df.columns))
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns\n")

# Show a few examples
print("EXAMPLES:")
print("="*80 + "\n")

for idx, row in df.head(3).iterrows():
    print(f"Course: {row['course_id']} - {row['course_title'][:50]}")
    profiles = [col for col in df.columns[7:] if row[col] == 1]
    if profiles:
        print(f"  Profiles: {', '.join(profiles)}")
    else:
        print(f"  Profiles: NONE")
    print()

# Show multi-profile examples
print("="*80)
print("MULTI-PROFILE EXAMPLE:")
print("="*80 + "\n")

df['profile_count'] = df[df.columns[7:]].sum(axis=1)
multi = df[df['profile_count'] > 1].head(1)

for idx, row in multi.iterrows():
    print(f"Course: {row['course_id']} - {row['course_title']}")
    profiles = [col for col in df.columns[7:] if row[col] == 1]
    print(f"  Profiles ({len(profiles)}):")
    for p in profiles:
        print(f"    ✓ {p}: {row[p]}")
    print()

print("="*80)
print(f"✓ File ready: mbi_curriculum_database_v5_multiprofile.csv")
print("="*80 + "\n")
