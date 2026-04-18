"""Extract all text from brochure to find course assignments"""

import fitz
from pathlib import Path

pdf_path = Path("MBI-Profilbroschuere_Januar_2025.pdf")
doc = fitz.open(pdf_path)

print("\n" + "="*80)
print("FULL TEXT EXTRACTION - Looking for course listings")
print("="*80 + "\n")

# Extract all text
all_text = ""
for page_num in range(doc.page_count):
    page = doc[page_num]
    all_text += page.get_text() + "\n[PAGE BREAK]\n"

# Save to file for easier analysis
with open("_broschure_full_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"✓ Full text saved to _broschure_full_text.txt ({len(all_text)} chars)\n")

# Look for course numbers (pattern: digit,digit format or 8,000 format)
import re

print("Looking for course patterns...\n")

# Pattern for course IDs
pattern = r'\d{1,2},\d{3,4}'
matches = re.findall(pattern, all_text)

if matches:
    unique_courses = sorted(set(matches))
    print(f"Found {len(unique_courses)} unique courses:\n")
    print(", ".join(unique_courses[:20]))
    if len(unique_courses) > 20:
        print(f"... and {len(unique_courses) - 20} more")
else:
    print("No course numbers found with that pattern")

# Look for profile keywords and their context
print("\n" + "="*80)
print("SEARCHING FOR PROFILE SECTIONS")
print("="*80 + "\n")

profiles = [
    "Business Development",
    "Digital Channel",
    "Start-up",
    "Supply Chain",
    "Technology",
    "Transforming"
]

for profile in profiles:
    idx = all_text.lower().find(profile.lower())
    if idx != -1:
        # Extract context around profile
        start = max(0, idx - 100)
        end = min(len(all_text), idx + 500)
        context = all_text[start:end]
        print(f"\n{profile}:")
        print(f"  {context[:200]}...\n")
