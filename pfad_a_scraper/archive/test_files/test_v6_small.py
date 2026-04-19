"""
Quick test of V6 scraper with small sample (50 articles)
"""
import sys
import re

# Read the original file
with open('5_startupticker_scraper_v6_MULTI_KEYWORD.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace MAX_ARTICLES = 4500 with 50
content_modified = re.sub(r'MAX_ARTICLES = 4500', 'MAX_ARTICLES = 50', content)

# Replace output filename
content_modified = content_modified.replace(
    "output_path = './data/startupticker_startups_v6.csv'",
    "output_path = './data/startupticker_startups_v6_TEST.csv'"
)

# Write to temp file
with open('temp_test_v6.py', 'w', encoding='utf-8') as f:
    f.write(content_modified)

print("✓ Created temp_test_v6.py with MAX_ARTICLES=50")
print("✓ Output will be saved to: data/startupticker_startups_v6_TEST.csv")
print("\nRun with: python3 temp_test_v6.py")
