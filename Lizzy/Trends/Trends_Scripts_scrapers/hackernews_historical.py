#!/usr/bin/env python3
"""
Fetch HackerNews articles from 2023-2025 via Algolia API.
Standalone script (not a Scrapy spider).
Output: data/hackernews_historical.csv
"""

import requests
import json
import csv
import time
import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configuration
ALGOLIA_BASE_URL = "https://hn.algolia.com/api/v1/search_by_date"
MAX_PER_MONTH = 50
MIN_SCORE = 10
ARTICLE_TEXT_TIMEOUT = 5
BATCH_SLEEP = 0.5  # Between API calls
ARTICLE_SLEEP = 0.1  # Between article fetches

# Relevant terms for filtering
RELEVANT_TERMS = [
    "ai", "startup", "funding", "agent", "model", "robot", "chip",
    "crypto", "saas", "health", "climate", "security", "autonomous",
    "llm", "gpt", "foundation", "venture", "raises", "series",
    "machine learning", "deep learning", "neural", "software",
    "tech", "data", "cloud", "api", "open source", "developer"
]

# Domains to skip (no full text extraction)
SKIP_DOMAINS = ["youtube.com", "twitter.com", "reddit.com", "github.com", "arxiv.org"]

# Output CSV
OUTPUT_CSV = Path(__file__).parent.parent / "data" / "hackernews_historical.csv"
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)


def get_unix_timestamps(year_month):
    """Get start and end Unix timestamps for a month."""
    # Parse "YYYY-MM"
    year, month = map(int, year_month.split("-"))
    
    # Start of month
    start_date = datetime.datetime(year, month, 1, 0, 0, 0)
    start_unix = int(start_date.timestamp())
    
    # End of month (first day of next month, minus 1 second)
    if month == 12:
        end_date = datetime.datetime(year + 1, 1, 1, 0, 0, 0)
    else:
        end_date = datetime.datetime(year, month + 1, 1, 0, 0, 0)
    end_unix = int(end_date.timestamp()) - 1
    
    return start_unix, end_unix


def is_relevant(title, story_text):
    """Check if article contains relevant tech terms."""
    text = f"{title} {story_text}".lower()
    return any(term in text for term in RELEVANT_TERMS)


def fetch_article_text(url):
    """Fetch article text from URL. Returns text or None on failure."""
    if not url:
        return None
    
    # Skip certain domains
    domain = urlparse(url).netloc.replace("www.", "")
    if any(skip in domain for skip in SKIP_DOMAINS):
        return None
    
    try:
        response = requests.get(url, timeout=ARTICLE_TEXT_TIMEOUT)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try multiple selectors
        article = soup.find("article")
        if article:
            text = article.get_text(separator=" ", strip=True)
            return text[:2000] if text else None
        
        main = soup.find("main")
        if main:
            text = main.get_text(separator=" ", strip=True)
            return text[:2000] if text else None
        
        # Fallback to all paragraphs
        paragraphs = soup.find_all("p")
        if paragraphs:
            text = " ".join([p.get_text(strip=True) for p in paragraphs[:10]])
            return text[:2000] if text else None
        
        return None
    except Exception as e:
        return None


def fetch_month_articles(year_month):
    """Fetch articles for a specific month from Algolia."""
    start_unix, end_unix = get_unix_timestamps(year_month)
    
    articles = []
    page = 0
    
    while len(articles) < MAX_PER_MONTH:
        params = {
            "tags": "story",
            "numericFilters": f"created_at_i>{start_unix},created_at_i<{end_unix}",
            "hitsPerPage": 100,
            "page": page,
        }
        
        try:
            response = requests.get(ALGOLIA_BASE_URL, params=params, timeout=10)
            data = response.json()
            
            hits = data.get("hits", [])
            if not hits:
                break
            
            for hit in hits:
                if len(articles) >= MAX_PER_MONTH:
                    break
                
                # Filter by score
                if hit.get("points", 0) < MIN_SCORE:
                    continue
                
                # Filter by required fields
                title = hit.get("title")
                url = hit.get("url")
                if not title or not url:
                    continue
                
                # Filter by relevance
                story_text = hit.get("story_text", "")
                if not is_relevant(title, story_text):
                    continue
                
                articles.append(hit)
            
            # Stop if we got fewer hits than requested
            if len(hits) < 100:
                break
            
            page += 1
            time.sleep(BATCH_SLEEP)
        
        except Exception as e:
            print(f"Error fetching {year_month} page {page}: {e}")
            break
    
    return articles


def article_to_row(article):
    """Convert Algolia article to CSV row."""
    url = article.get("url", "")
    title = article.get("title", "")
    
    # Get or fetch article text
    article_text = article.get("story_text", "")
    if not article_text:
        article_text = fetch_article_text(url) or ""
        time.sleep(ARTICLE_SLEEP)
    
    # Extract article excerpt (first 300 chars)
    article_excerpt = article_text[:300] if article_text else title[:300]
    
    # Parse timestamp
    created_at_i = article.get("created_at_i", 0)
    publication_date = datetime.datetime.fromtimestamp(created_at_i).isoformat()
    year = str(created_at_i)[:4] if created_at_i else "2023"
    year_month = publication_date[:7]
    
    # Extract author
    author = article.get("author", "")
    
    return {
        "source": "HackerNews",
        "category": "community",
        "source_type": "community_news",
        "title": title,
        "url": url,
        "publication_date": publication_date,
        "year": year,
        "year_month": year_month,
        "author": author,
        "article_excerpt": article_excerpt,
        "article_text": article_text,
        "trend_type": "soft_trend",
    }


def main():
    """Main execution."""
    print("=" * 80)
    print("HackerNews Historical Article Fetcher (2023-2025)")
    print("=" * 80)
    print()
    
    # Generate list of months
    months = []
    for year in [2023, 2024, 2025]:
        for month in range(1, 13):
            months.append(f"{year:04d}-{month:02d}")
    
    all_articles = []
    total_by_year = {"2023": 0, "2024": 0, "2025": 0}
    
    # Fetch articles for each month
    for idx, year_month in enumerate(months, 1):
        articles = fetch_month_articles(year_month)
        all_articles.extend(articles)
        year = year_month[:4]
        total_by_year[year] += len(articles)
        
        # Print progress for each month
        print(f"{year_month}: {len(articles)} articles collected")
    
    print()
    print(f"✓ Total articles collected: {len(all_articles)}")
    print(f"  2023: {total_by_year['2023']}")
    print(f"  2024: {total_by_year['2024']}")
    print(f"  2025: {total_by_year['2025']}")
    
    # Calculate average score
    if all_articles:
        avg_score = sum(a.get("points", 0) for a in all_articles) / len(all_articles)
        print(f"  Average score: {avg_score:.1f}")
    
    print()
    
    # Write to CSV
    headers = [
        "source", "category", "source_type", "title", "url",
        "publication_date", "year", "year_month", "author",
        "article_excerpt", "article_text", "trend_type"
    ]
    
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for article in all_articles:
            row = article_to_row(article)
            writer.writerow(row)
    
    print(f"✓ Saved to: {OUTPUT_CSV}")
    print(f"✓ Total rows: {len(all_articles)}")


if __name__ == "__main__":
    main()
