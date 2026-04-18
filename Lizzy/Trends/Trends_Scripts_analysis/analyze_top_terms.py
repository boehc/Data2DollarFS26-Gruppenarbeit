#!/usr/bin/env python3
"""
Analyze top terms and phrases per year
"""
import csv
import re
from collections import defaultdict, Counter
import os

# File paths
base_path = "/Users/nataliekmecova/Documents/tech_trends_project/tech_trends"
input_file = f"{base_path}/data/articles_slim.csv"
output_dir = f"{base_path}/data"

# Stopwords
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "it",
    "this", "that", "for", "of", "in", "on", "at", "to",
    "by", "with", "from", "and", "or", "but", "not", "be",
    "has", "have", "had", "will", "would", "could", "should",
    "also", "its", "their", "they", "we", "our", "as", "about",
    "after", "before", "more", "than", "when", "which", "who",
    "been", "being", "into", "through", "during", "company",
    "said", "says", "new", "one", "two", "three", "year",
    "years", "million", "billion", "percent", "can", "use",
    "used", "using", "get", "make", "made", "s", "re", "how",
    "what", "why", "now", "just", "like", "first", "last",
    "up", "out", "over", "all", "so", "do", "did", "if",
    "there", "her", "his", "him", "she", "he", "they", "them",
    "their", "these", "those", "some", "any", "no", "may",
    "might", "must", "need", "want", "well", "back", "down", "me"
}

print("=" * 80)
print("ANALYZING TOP TERMS BY YEAR")
print("=" * 80)

# Step 1: Read CSV
print("\n[1/6] Reading input file...")
articles_by_year = defaultdict(list)
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = row.get('year', '')
            title = row.get('title', '')
            excerpt = row.get('article_excerpt', '')
            if year and (title or excerpt):
                articles_by_year[year].append((title, excerpt))
    
    print(f"  ✓ Loaded articles by year:")
    for year in sorted(articles_by_year.keys()):
        print(f"    {year}: {len(articles_by_year[year])} articles")
except FileNotFoundError:
    print(f"  ✗ File not found: {input_file}")
    exit(1)

# Step 2: Extract terms per year
print("\n[2/6] Extracting terms (unigrams + bigrams)...")

def tokenize_and_filter(text):
    """Tokenize text and remove stopwords"""
    # Lowercase and remove punctuation
    text = text.lower()
    # Replace punctuation with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Split into words
    words = text.split()
    # Filter out stopwords and empty strings
    filtered = [w for w in words if w and w not in STOPWORDS and len(w) > 1]
    return filtered

terms_by_year = {}
for year in sorted(articles_by_year.keys()):
    all_words = []
    for title, excerpt in articles_by_year[year]:
        text = f"{title} {excerpt}"
        words = tokenize_and_filter(text)
        all_words.extend(words)
    
    # Count unigrams
    unigrams = Counter(all_words)
    
    # Extract bigrams
    bigrams = Counter()
    for i in range(len(all_words) - 1):
        bigram = f"{all_words[i]} {all_words[i+1]}"
        bigrams[bigram] += 1
    
    # Combine and get top 200
    combined = dict(unigrams)
    combined.update(dict(bigrams))
    top_terms = dict(sorted(combined.items(), key=lambda x: -x[1])[:200])
    
    terms_by_year[year] = top_terms
    print(f"  ✓ {year}: {len(top_terms)} unique terms")

# Step 3: Create comparison table
print("\n[3/6] Creating term comparison table...")

all_terms = set()
for terms in terms_by_year.values():
    all_terms.update(terms.keys())

comparison = []
for term in all_terms:
    row = {
        'term': term,
        'count_2023': terms_by_year.get('2023', {}).get(term, 0),
        'count_2024': terms_by_year.get('2024', {}).get(term, 0),
        'count_2025': terms_by_year.get('2025', {}).get(term, 0),
        'count_2026': terms_by_year.get('2026', {}).get(term, 0),
    }
    row['total'] = row['count_2023'] + row['count_2024'] + row['count_2025'] + row['count_2026']
    
    # Growth ratio: 2026 vs 2023
    if row['count_2023'] > 0:
        row['growth_ratio'] = row['count_2026'] / row['count_2023']
    else:
        row['growth_ratio'] = 0.0
    
    comparison.append(row)

# Sort by total
comparison.sort(key=lambda x: -x['total'])

print(f"  ✓ Created comparison table: {len(comparison)} terms")

# Step 4: Save top_terms_by_year.csv
print("\n[4/6] Saving output files...")

output_file1 = f"{output_dir}/top_terms_by_year.csv"
with open(output_file1, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['term', 'count_2023', 'count_2024', 'count_2025', 'count_2026', 'total', 'growth_ratio'])
    writer.writeheader()
    writer.writerows(comparison)
print(f"  ✓ Saved {output_file1}")

# Step 5: Save growing_terms.csv
output_file2 = f"{output_dir}/growing_terms.csv"
growing = [r for r in comparison if r['count_2026'] > r['count_2023'] * 2]
growing.sort(key=lambda x: -x['growth_ratio'])
with open(output_file2, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['term', 'count_2023', 'count_2024', 'count_2025', 'count_2026', 'total', 'growth_ratio'])
    writer.writeheader()
    writer.writerows(growing)
print(f"  ✓ Saved {output_file2} ({len(growing)} terms)")

# Step 6: Save new_terms_2026.csv
output_file3 = f"{output_dir}/new_terms_2026.csv"
new_2026 = [r for r in comparison if r['count_2023'] == 0 and r['count_2026'] >= 5]
new_2026.sort(key=lambda x: -x['count_2026'])
with open(output_file3, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['term', 'count_2023', 'count_2024', 'count_2025', 'count_2026', 'total', 'growth_ratio'])
    writer.writeheader()
    writer.writerows(new_2026)
print(f"  ✓ Saved {output_file3} ({len(new_2026)} terms)")

# Step 7: Save declining_terms.csv
output_file4 = f"{output_dir}/declining_terms.csv"
declining = [r for r in comparison if r['count_2023'] > 10 and r['count_2026'] < r['count_2023'] * 0.5]
declining.sort(key=lambda x: -x['count_2023'])
with open(output_file4, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['term', 'count_2023', 'count_2024', 'count_2025', 'count_2026', 'total', 'growth_ratio'])
    writer.writeheader()
    writer.writerows(declining)
print(f"  ✓ Saved {output_file4} ({len(declining)} terms)")

# Step 8: Print statistics
print("\n" + "=" * 80)
print("TOP 100 TERMS PER YEAR")
print("=" * 80)

for year in sorted(terms_by_year.keys()):
    print(f"\n{year}:")
    print("-" * 50)
    top_100 = sorted(terms_by_year[year].items(), key=lambda x: -x[1])[:100]
    for i, (term, count) in enumerate(top_100[:20], 1):
        print(f"  {i:2d}. {term:30s} {count:5d}")
    if len(top_100) > 20:
        print(f"  ... ({len(top_100)} total top terms)")

print("\n" + "=" * 80)
print("TOP 50 GROWING TERMS (2026 > 2023*2)")
print("=" * 80)
print()
for i, row in enumerate(growing[:50], 1):
    growth = f"{row['growth_ratio']:.1f}x" if row['count_2023'] > 0 else "new"
    print(f"{i:2d}. {row['term']:30s} 2023:{row['count_2023']:4d} → 2026:{row['count_2026']:4d} ({growth})")
if len(growing) > 50:
    print(f"\n... ({len(growing)} total growing terms)")

print("\n" + "=" * 80)
print("TOP 30 NEW TERMS IN 2026 (only 2026, >=5 count)")
print("=" * 80)
print()
for i, row in enumerate(new_2026[:30], 1):
    print(f"{i:2d}. {row['term']:40s} count: {row['count_2026']:4d}")
if len(new_2026) > 30:
    print(f"\n... ({len(new_2026)} total new terms)")

print("\n" + "=" * 80)
print("TOP 30 DECLINING TERMS (>10 in 2023, <50% in 2026)")
print("=" * 80)
print()
for i, row in enumerate(declining[:30], 1):
    decline = 100 * (1 - row['count_2026'] / row['count_2023'])
    print(f"{i:2d}. {row['term']:30s} 2023:{row['count_2023']:4d} → 2026:{row['count_2026']:4d} ({decline:.0f}% down)")
if len(declining) > 30:
    print(f"\n... ({len(declining)} total declining terms)")

print("\n" + "=" * 80)
print("✓ ANALYSIS COMPLETE")
print("=" * 80)
