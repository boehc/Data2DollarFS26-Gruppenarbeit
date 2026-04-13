#!/usr/bin/env python3
"""
Merge 4 tech articles CSV files into one clean dataset
"""
import csv
from collections import defaultdict

# File paths
base_path = "/Users/nataliekmecova/Documents/tech_trends_project/tech_trends"
input_files = {
    'tc_hist': f"{base_path}/data/techcrunch_historical_clean.csv",
    'hn_hist': f"{base_path}/data/hackernews_historical_clean.csv",
    'tc_2026': f"{base_path}/data/techcrunch_2026_q1.csv",
    'hn_2026': f"{base_path}/data/hackernews_2026_q1.csv",
}

output_file = f"{base_path}/data/articles_raw_merged.csv"

# Target columns
TARGET_COLUMNS = [
    'source', 'category', 'source_type', 'title', 'url',
    'publication_date', 'year', 'year_month', 'author',
    'article_excerpt', 'article_text', 'trend_type'
]

print("=" * 80)
print("MERGING 4 ARTICLE DATASETS")
print("=" * 80)

# Step 1: Read all files
print("\n[1/8] Reading files...")

def read_csv_file(filepath):
    """Read CSV file and return list of dicts"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data
    except FileNotFoundError:
        print(f"  ✗ File not found: {filepath}")
        return []

tc_hist = read_csv_file(input_files['tc_hist'])
print(f"  ✓ TechCrunch historical: {len(tc_hist)} rows")

hn_hist = read_csv_file(input_files['hn_hist'])
print(f"  ✓ HackerNews historical: {len(hn_hist)} rows")

tc_2026 = read_csv_file(input_files['tc_2026'])
print(f"  ✓ TechCrunch 2026: {len(tc_2026)} rows")

hn_2026 = read_csv_file(input_files['hn_2026'])
print(f"  ✓ HackerNews 2026: {len(hn_2026)} rows")

# Step 2: Filter techcrunch_historical.csv to remove 2026 data
print("\n[2/8] Filtering TechCrunch historical (remove 2026)...")
initial_count = len(tc_hist)
tc_hist = [row for row in tc_hist if str(row.get('year', '')).strip() not in ['2026', '2026.0']]
print(f"  Removed {initial_count - len(tc_hist)} rows with year=2026")
print(f"  Kept {len(tc_hist)} rows (2023-2025)")

# Step 3: Standardize columns
print("\n[3/8] Standardizing columns...")

def standardize_row(row, set_category=None):
    """Ensure row has all target columns, fill missing with empty string"""
    standardized = {}
    
    for col in TARGET_COLUMNS:
        if col in row:
            standardized[col] = row[col]
        else:
            standardized[col] = ''
    
    # Set category if specified
    if set_category and (not standardized.get('category') or standardized['category'].strip() == ''):
        standardized['category'] = set_category
    
    # Build year_month from publication_date if missing
    if not standardized.get('year_month') or standardized['year_month'].strip() == '':
        pub_date = standardized.get('publication_date', '')
        if pub_date and len(pub_date) >= 7:
            standardized['year_month'] = pub_date[:7]
    
    return standardized

print("  Processing TechCrunch historical...")
tc_hist = [standardize_row(row) for row in tc_hist]

print("  Processing HackerNews historical...")
hn_hist = [standardize_row(row, set_category='community') for row in hn_hist]

print("  Processing TechCrunch 2026...")
tc_2026 = [standardize_row(row, set_category='mixed') for row in tc_2026]

print("  Processing HackerNews 2026...")
hn_2026 = [standardize_row(row, set_category='community') for row in hn_2026]

# Step 4: Fix year column
print("\n[4/8] Fixing year column...")

def fix_year_value(year_str):
    """Convert year to standard format"""
    if not year_str or year_str.strip() == '':
        return ''
    try:
        return str(int(float(year_str)))
    except:
        return str(year_str)

def fix_years(articles):
    for article in articles:
        article['year'] = fix_year_value(article.get('year', ''))
    return articles

tc_hist = fix_years(tc_hist)
hn_hist = fix_years(hn_hist)
tc_2026 = fix_years(tc_2026)
hn_2026 = fix_years(hn_2026)
print("  ✓ Year column standardized across all files")

# Step 5: Combine all
print("\n[5/8] Combining dataframes...")
all_articles = tc_hist + hn_hist + tc_2026 + hn_2026
print(f"  Total before deduplication: {len(all_articles)} articles")

# Step 5b: Remove duplicate URLs (keep first)
print("\n[5b/8] Removing duplicate URLs...")
initial_count = len(all_articles)
seen_urls = set()
deduped = []

for article in all_articles:
    url = article.get('url', '')
    if url not in seen_urls:
        seen_urls.add(url)
        deduped.append(article)

all_articles = deduped
duplicates_removed = initial_count - len(all_articles)
print(f"  ✓ Removed {duplicates_removed} duplicate URLs")
print(f"  Total after deduplication: {len(all_articles)} articles")

# Step 6: Remove rows with empty or short article_text
print("\n[6/8] Filtering by article text length...")
initial_count = len(all_articles)

filtered = []
for article in all_articles:
    text = article.get('article_text', '').strip()
    if len(text) >= 200:
        filtered.append(article)

all_articles = filtered
text_filtered = initial_count - len(all_articles)
print(f"  ✓ Removed {text_filtered} rows with article_text < 200 chars")
print(f"  Total after text filter: {len(all_articles)} articles")

# Step 7: Write output
print("\n[7/8] Writing output file...")
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=TARGET_COLUMNS)
    writer.writeheader()
    writer.writerows(all_articles)

print(f"  ✓ Saved {len(all_articles)} articles to {output_file}")

# Step 8: Print summary statistics
print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)

print(f"\nTotal articles: {len(all_articles)}")

# By source
print("\nBy source:")
source_counts = defaultdict(int)
for article in all_articles:
    source = article.get('source', 'unknown')
    source_counts[source] += 1

for source in sorted(source_counts.keys()):
    count = source_counts[source]
    pct = 100 * count / len(all_articles)
    print(f"  {source}: {count} ({pct:.1f}%)")

# By year
print("\nBy year:")
year_counts = defaultdict(int)
for article in all_articles:
    year = article.get('year', 'unknown')
    year_counts[year] += 1

for year in sorted(year_counts.keys()):
    count = year_counts[year]
    pct = 100 * count / len(all_articles)
    print(f"  {year}: {count} ({pct:.1f}%)")

# By year_month
print("\nBy year_month:")
ym_counts = defaultdict(int)
for article in all_articles:
    ym = article.get('year_month', 'unknown')
    ym_counts[ym] += 1

months_per_year = defaultdict(list)
for ym, count in ym_counts.items():
    year = ym[:4] if len(ym) >= 4 else 'unknown'
    months_per_year[year].append(count)

for year in sorted(months_per_year.keys()):
    counts = months_per_year[year]
    total = sum(counts)
    avg = total / len(counts)
    print(f"  {year}: min={min(counts)}, max={max(counts)}, avg={avg:.1f}, total={total}")

# Text coverage
print("\nText coverage:")
text_coverage = sum(1 for a in all_articles if len(a.get('article_text', '').strip()) >= 200)
text_pct = 100 * text_coverage / len(all_articles)
print(f"  Articles with text >= 200 chars: {text_coverage}/{len(all_articles)} ({text_pct:.1f}%)")

print("\n" + "=" * 80)
print("✓ MERGE COMPLETE")
print("=" * 80)

print("\n" + "=" * 80)
print("✓ MERGE COMPLETE")
print("=" * 80)
