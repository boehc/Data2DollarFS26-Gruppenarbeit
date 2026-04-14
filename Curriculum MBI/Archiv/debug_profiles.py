"""
Extract profiles using better section markers
"""

import re
from pathlib import Path

with open("_broschure_full_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Find all occurrences of "[PAGE BREAK]"
page_breaks = [m.start() for m in re.finditer(r'\[PAGE BREAK\]', text)]

print(f"Found {len(page_breaks)} page breaks\n")

# Extract around the profile markers (looking at extracted content)
profile_patterns = [
    ("Business Development", r"Business Development.*?Pflichtwahlkurse(.*?)(?=Methodenkurse|[A-Z]{2,}.*?[A-Z]{2,}|\[PAGE BREAK\])"),
    ("Digital Channel", r"Digital Channel.*?Pflichtwahlkurse(.*?)(?=Methodenkurse|Forschungs|[A-Z]{2,}|\[PAGE BREAK\])"),
    ("Startup & Scale", r"Start-up & Scale.*?Pflichtwahlkurse(.*?)(?=Methodenkurse|\[PAGE BREAK\])"),
    ("Supply Chain", r"Supply Chain.*?Pflichtwahlkurse(.*?)(?=Methodenkurse|\[PAGE BREAK\])"),
    ("Technology", r"Technology.*?Pflichtwahlkurse(.*?)(?=Methodenkurse|\[PAGE BREAK\])"),
    ("Digital Transformation", r"Transforming and Managing.*?Pflichtwahlkurse(.*?)(?=Methodenkurse|\[PAGE BREAK\]|$)"),
]

course_pattern = r'(\d{1,2},\d{3,4})'

for profile_name, pattern in profile_patterns:
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    if matches:
        # Extract courses from matched sections
        all_courses = []
        for match in matches:
            courses = re.findall(course_pattern, match)
            all_courses.extend(courses)
        unique = sorted(set(all_courses))
        print(f"{profile_name:30s}: {len(unique):2d} courses -> {', '.join(unique[:5])}...")
    else:
        print(f"{profile_name:30s}: NOT FOUND")

print("\n" + "="*80)
print("TESTING SIMPLE SECTION FINDING")
print("="*80 + "\n")

# Try simple approach: find "Business Development" and next "Pflichtwahlkurse"
bd_start = text.lower().find("business development")
if bd_start != -1:
    # Find next "Pflichtwahlkurse"
    pw_start = text.lower().find("pflichtwahlkurse", bd_start)
    if pw_start != -1:
        # Find next major section start
        next_profile_indicators = ["«»", "«", "«Start", "«Supply", "«Technology"]
        next_start = len(text)
        for indicator in next_profile_indicators:
            idx = text.find(indicator, pw_start + 10)
            if idx > pw_start and idx < next_start:
                next_start = idx
        
        section = text[pw_start:next_start]
        courses = re.findall(r'\d{1,2},\d{3,4}', section)
        unique = sorted(set(courses))
        print(f"Business Development (simple): {len(unique)} courses\n{', '.join(unique)}")
