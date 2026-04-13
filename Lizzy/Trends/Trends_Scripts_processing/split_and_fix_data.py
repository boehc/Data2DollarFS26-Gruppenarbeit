#!/usr/bin/env python3
"""
Fix and split merged_techcrunch_hackernews_2026_jan_mar.csv
"""
import csv
from datetime import datetime
from pathlib import Path

# Set working directory
input_file = "/Users/nataliekmecova/Documents/tech_trends_project/Final CSV to analyze/merged_techcrunch_hackernews_2026_jan_mar.csv"
tc_output = "/Users/nataliekmecova/Documents/tech_trends_project/tech_trends/data/techcrunch_2026_q1.csv"
hn_output = "/Users/nataliekmecova/Documents/tech_trends_project/tech_trends/data/hackernews_2026_q1.csv"

# Target columns in order
TARGET_COLUMNS = [
    'source', 'category', 'source_type', 'title', 'url',
    'publication_date', 'year', 'year_month', 'author',
    'article_excerpt', 'article_text', 'trend_type'
]

print("=" * 70)
print("PROCESSING MERGED DATA")
print("=" * 70)

# Load and process data
print("\n[1/5] Loading data...")
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    raw_articles = list(reader)

print(f"Loaded {len(raw_articles)} articles")

# Process each row
print("\n[2/5] Processing rows...")
processed_articles = []

for i, row in enumerate(raw_articles):
    # Extract publication_date
    pub_date = row.get('publication_date', '')
    
    # Extract year_month from publication_date
    try:
        if pub_date:
            year_month = pub_date[:7]  # e.g., "2026-01"
        else:
            year_month = ''
    except:
        year_month = ''
    
    # Skip if not Q1 2026
    if year_month not in ["2026-01", "2026-02", "2026-03"]:
        continue
    
    # Fix year column
    year_str = row.get('year', '')
    try:
        if year_str:
            year = str(int(float(year_str)))
        else:
            year = '2026'
    except:
        year = '2026'
    
    # Add/fix category column
    source = row.get('source', '')
    category = row.get('category', '')
    
    if not category or category == '':
        if source == 'TechCrunch':
            category = 'mixed'
        elif source == 'HackerNews':
            category = 'community'
        else:
            category = 'unknown'
    
    # Build new row with all columns
    new_row = {
        'source': source,
        'category': category,
        'source_type': row.get('source_type', ''),
        'title': row.get('title', ''),
        'url': row.get('url', ''),
        'publication_date': pub_date,
        'year': year,
        'year_month': year_month,
        'author': row.get('author', ''),
        'article_excerpt': row.get('article_excerpt', ''),
        'article_text': row.get('article_text', ''),
        'trend_type': row.get('trend_type', '')
    }
    
    processed_articles.append(new_row)

print(f"Processed {len(processed_articles)} articles (Q1 2026 only)")

# Split by source
print("\n[3/5] Splitting by source...")
tc_articles = [a for a in processed_articles if a['source'] == 'TechCrunch']
hn_articles = [a for a in processed_articles if a['source'] == 'HackerNews']

print(f"TechCrunch: {len(tc_articles)} articles")
print(f"HackerNews: {len(hn_articles)} articles")

# Write TechCrunch file
print("\n[4/5] Writing TechCrunch file...")
with open(tc_output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=TARGET_COLUMNS)
    writer.writeheader()
    writer.writerows(tc_articles)

print(f"✓ Saved to {tc_output}")

# Write HackerNews file
print("Writing HackerNews file...")
with open(hn_output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=TARGET_COLUMNS)
    writer.writeheader()
    writer.writerows(hn_articles)

print(f"✓ Saved to {hn_output}")

# Statistics
print("\n" + "=" * 70)
print("STATISTICS")
print("=" * 70)

def print_stats(articles, source_name):
    print(f"\n{source_name}")
    print("-" * 70)
    print(f"Total articles: {len(articles)}")
    
    # By year_month
    month_counts = {}
    for a in articles:
        ym = a.get('year_month', 'unknown')
        month_counts[ym] = month_counts.get(ym, 0) + 1
    
    print("\nBy month:")
    for month in sorted(month_counts.keys()):
        print(f"  {month}: {month_counts[month]}")
    
    # Text coverage
    text_coverage = sum(1 for a in articles if len(a.get('article_text', '')) >= 200)
    print(f"\nArticles with text >= 200 chars: {text_coverage}/{len(articles)} ({100*text_coverage/len(articles):.1f}%)")

print_stats(tc_articles, "TECHCRUNCH")
print_stats(hn_articles, "HACKERNEWS")

print("\n" + "=" * 70)
print("✓ COMPLETE")
print("=" * 70)
