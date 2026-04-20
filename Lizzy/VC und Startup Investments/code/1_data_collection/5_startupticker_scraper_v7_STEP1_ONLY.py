"""
Startupticker.ch News Scraper V7 - STEP 1 ONLY (Deterministic Extraction)

ARCHITECTURE:
╔══════════════════════════════════════════════════════════════╗
║ STEP 1 — Deterministic Extraction (NO LLM, NO INTERPRETATION)║
║   • Extract raw article_text (cleaned HTML body)             ║
║   • Extract publication_date via regex (DD.MM.YYYY)          ║
║   • Extract year (integer from date)                         ║
║   • Extract URL (source link)                                ║
║   • Extract title (article headline)                         ║
╚══════════════════════════════════════════════════════════════╝

OUTPUT: CSV with 5 columns:
- URL (primary key)
- Title
- Publication_Date (YYYY-MM-DD format)
- Year (integer)
- Article_Text (full cleaned text)

STEP 2 (LLM analysis) will be done separately on this output.

WHY STEP 1 ONLY:
✅ 100% reliable (no LLM interpretation)
✅ Fast execution (~2 sec/article)
✅ No API costs
✅ Clean data for STEP 2 processing
✅ Can be re-processed with different STEP 2 strategies
"""

import time
import re
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ============================================================================
# CONFIGURATION
# ============================================================================
MAX_ARTICLES = 5000  # Scrape all articles (will stop when hitting 2022)
MIN_YEAR = 2023  # Only scrape articles from 2023 onwards (stop at 2022)

OUTPUT_FILE = './data/startupticker_raw_articles_v7_step1_FINANCING.csv'


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def setup_driver():
    """Initialize Selenium Chrome WebDriver (headless)."""
    print("🚀 Setting up Chrome WebDriver...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("✓ WebDriver ready\n")
    return driver


def clean_text(text):
    """Clean text by removing excessive whitespace and common boilerplate."""
    if not text:
        return None
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common boilerplate patterns
    boilerplate_patterns = [
        r'Read more about.*?(?=\n|$)',
        r'Accept all cookies.*?(?=\n|$)',
        r'Subscribe to newsletter.*?(?=\n|$)',
        r'Share this article.*?(?=\n|$)',
        r'Follow us on.*?(?=\n|$)',
        r'Cookie (settings|preferences).*?(?=\n|$)',
    ]
    
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Final cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text if len(text) > 50 else None


def extract_article_text(driver, url):
    """
    Extract clean article text from HTML page.
    
    Strategy:
    1. Try StartupTicker-specific selectors first
    2. Fallback to generic article selectors
    3. Final fallback: all <p> tags
    4. Clean the extracted text
    
    Returns: cleaned article text string or None
    """
    try:
        driver.get(url)
        time.sleep(1.5)  # Wait for page load
        
        article_text = None
        
        # StartupTicker-specific selectors (highest priority)
        content_selectors = [
            'div.article-body',      # StartupTicker primary
            'div.news-content',      # StartupTicker secondary
            'main.content',          # StartupTicker main content
            'article.news',          # StartupTicker article wrapper
            'div.news-detail',       # StartupTicker detail view
            # Generic fallbacks
            'article',
            'div.article-content',
            'div.content',
            'div[class*="text"]',
            'main',
            'div.body'
        ]
        
        # Try each selector in order
        for selector in content_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Combine text from all matching elements
                    text = ' '.join([el.text for el in elements if el.text])
                    if text and len(text) > 100:  # Minimum length threshold
                        article_text = text
                        break
            except:
                continue
        
        # Fallback: Extract all <p> tags if selectors failed
        if not article_text or len(article_text) < 100:
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, 'p')
                text = ' '.join([p.text for p in paragraphs if p.text])
                if text and len(text) > 100:
                    article_text = text
            except:
                pass
        
        # Clean the text
        article_text = clean_text(article_text)
        
        return article_text
    
    except Exception as e:
        print(f"      ⚠️  Error extracting text: {str(e)[:50]}")
        return None


def extract_publication_date(article_text):
    """
    Extract publication date via regex.
    
    Pattern: DD.MM.YYYY (appears at beginning after title)
    Example: "Delta Labs raises EUR 4.4 million... 02.04.2026 Lugano-based..."
    
    Returns: (date_str in YYYY-MM-DD format, year as int)
    Example: ("2026-04-02", 2026)
    """
    if not article_text:
        return None, None
    
    # Pattern 1: DD.MM.YYYY (standalone, most common)
    # Look in first 200 characters (date appears right after title)
    search_text = article_text[:200] if len(article_text) > 200 else article_text
    
    # Match DD.MM.YYYY followed by space (not part of a time stamp)
    pattern_standalone = r'(\d{2})\.(\d{2})\.(\d{4})(?!\s*\d{2}:\d{2})'
    
    match = re.search(pattern_standalone, search_text)
    if match:
        day, month, year = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    # Pattern 2: DD.MM.YYYY HH:MM (with time, fallback)
    pattern_with_time = r'(\d{2})\.(\d{2})\.(\d{4})\s+\d{2}:\d{2}'
    
    match = re.search(pattern_with_time, search_text)
    if match:
        day, month, year = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    return None, None


# ============================================================================
# SCRAPING FUNCTIONS
# ============================================================================

def scrape_news_overview(driver, max_articles=MAX_ARTICLES):
    """
    Scrape news overview page to collect article URLs and titles.
    FOCUS: Financing category only
    
    Returns: List of dicts with 'url' and 'title' keys
    """
    base_url = 'https://www.startupticker.ch/en/topics?category=Financing'
    news_items = []
    seen_urls = set()
    
    print(f"🔍 Scraping FINANCING category: {base_url}")
    print(f"🎯 Target: {max_articles} articles\n")
    driver.get(base_url)
    
    time.sleep(3)
    
    try:
        page = 1
        no_new_items_count = 0
        
        while len(news_items) < max_articles:
            print(f"📄 Page {page} (collected: {len(news_items)}/{max_articles})...", end='')
            
            # Scroll for lazy loading
            try:
                for scroll in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
            except Exception:
                pass
            
            # Get all article links directly
            links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/news/"]')
            new_items_found = 0
            
            for link in links:
                if len(news_items) >= max_articles:
                    break
                
                try:
                    url = link.get_attribute('href')
                    
                    # Skip unsubscribe/subscribe links
                    if not url or 'unsubscribe' in url or 'subscribe' in url:
                        continue
                    
                    # Skip if already seen
                    if url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    
                    # Get title from link text or nearby heading
                    title = link.text.strip()
                    if not title or len(title) < 10:
                        # Try to find a heading near this link
                        try:
                            parent = link.find_element(By.XPATH, '..')
                            title_elem = parent.find_element(By.CSS_SELECTOR, 'h2, h3, h4, .title')
                            title = title_elem.text.strip()
                        except:
                            title = "No title"
                    
                    if title and len(title) > 5:  # Ensure we have a reasonable title
                        news_items.append({
                            'url': url,
                            'title': title
                        })
                        new_items_found += 1
                    
                except Exception as e:
                    continue
            
            print(f" +{new_items_found} new")
            
            if new_items_found == 0:
                no_new_items_count += 1
                if no_new_items_count >= 3:
                    print("⚠️  No new items found (3x) - stopping pagination")
                    break
            else:
                no_new_items_count = 0
            
            # Pagination
            if len(news_items) < max_articles:
                try:
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, 
                        'a.next, button[class*="next"], a[class*="more"], button[class*="load"]')
                    
                    if next_buttons:
                        next_buttons[0].click()
                        time.sleep(3)
                        page += 1
                    else:
                        print("⚠️  No next button found - stopping pagination")
                        break
                except Exception as e:
                    print(f"⚠️  Pagination error: {str(e)[:50]}")
                    break
        
        print(f"\n✓ Collected {len(news_items)} article URLs\n")
        return news_items
        
    except Exception as e:
        print(f"\n❌ Error in overview scraping: {e}")
        return news_items


def scrape_article_step1(driver, url, title):
    """
    STEP 1: Deterministic extraction for one article.
    
    Returns dict with:
    - url: Source URL
    - title: Article title
    - article_text: Full cleaned article text
    - publication_date: YYYY-MM-DD format
    - year: Integer year
    """
    # Extract article text
    article_text = extract_article_text(driver, url)
    
    if not article_text:
        return None
    
    # Extract publication date from article text
    publication_date, year = extract_publication_date(article_text)
    
    # Filter by year if specified
    if year and year < MIN_YEAR:
        return None  # Skip old articles
    
    return {
        'URL': url,
        'Title': title,
        'Article_Text': article_text,
        'Publication_Date': publication_date,
        'Year': year
    }


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main scraping logic - STEP 1 ONLY."""
    driver = None
    
    try:
        driver = setup_driver()
        
        print("="*70)
        print("STARTUPTICKER.CH SCRAPER V7 - STEP 1 ONLY")
        print("="*70)
        print("Deterministic Extraction:")
        print("  • Article Text (cleaned HTML)")
        print("  • Publication Date (DD.MM.YYYY → YYYY-MM-DD)")
        print("  • Year (integer)")
        print("  • URL (source)")
        print(f"Filter: Only articles from {MIN_YEAR} onwards")
        print(f"Output: {OUTPUT_FILE}")
        print("="*70)
        print()
        
        # PHASE 1: Collect article URLs
        print("PHASE 1: Collect Article URLs")
        print("-" * 70)
        news_items = scrape_news_overview(driver, max_articles=MAX_ARTICLES)
        
        if not news_items:
            print("⚠️  No articles found")
            return
        
        print(f"✓ Collected {len(news_items)} article URLs\n")
        
        # PHASE 2: Extract article details (STEP 1 only)
        print("PHASE 2: Extract Article Details (STEP 1)")
        print("-" * 70)
        
        scraped_data = []
        skipped_count = 0
        error_count = 0
        old_articles_streak = 0  # Counter for consecutive articles older than MIN_YEAR
        
        for i, item in enumerate(news_items, 1):
            # Progress indicator
            if i % 50 == 0 or i == 1:
                print(f"\n[{i}/{len(news_items)}] Processing articles...")
            
            # Show current article (every 10th or first/last)
            if i % 10 == 0 or i == 1 or i == len(news_items):
                print(f"  [{i:4d}] {item['title'][:50]}...", end='')
            
            try:
                result = scrape_article_step1(driver, item['url'], item['title'])
                
                if result:
                    scraped_data.append(result)
                    old_articles_streak = 0  # Reset streak on successful extraction
                    if i % 10 == 0 or i == 1 or i == len(news_items):
                        print(f" ✓ ({result.get('Year', 'N/A')})")
                else:
                    # Article was skipped (likely due to MIN_YEAR filter)
                    skipped_count += 1
                    old_articles_streak += 1
                    if i % 10 == 0 or i == 1 or i == len(news_items):
                        print(f" ⊘ (skipped - old)")
                    
                    # Early stopping: if we hit 20 consecutive old articles, stop
                    if old_articles_streak >= 20:
                        print(f"\n\n{'='*70}")
                        print(f"⏹️  EARLY STOP: Hit {old_articles_streak} consecutive articles older than {MIN_YEAR}")
                        print(f"   Processed {i}/{len(news_items)} articles")
                        print(f"   Collected {len(scraped_data)} valid articles")
                        print(f"{'='*70}\n")
                        break
                
            except Exception as e:
                error_count += 1
                old_articles_streak = 0  # Reset on errors
                if i % 10 == 0 or i == 1 or i == len(news_items):
                    print(f" ✗ (error)")
                continue
            
            # Rate limiting
            time.sleep(0.3)
            
            # Checkpoint every 100 articles
            if i % 100 == 0:
                print(f"\n{'='*70}")
                print(f"CHECKPOINT: {i}/{len(news_items)} processed")
                print(f"  ✓ Extracted: {len(scraped_data)}")
                print(f"  ⊘ Skipped: {skipped_count}")
                print(f"  ✗ Errors: {error_count}")
                print(f"{'='*70}")
        
        print(f"\n✓ Processing complete\n")
        
        # PHASE 3: Create DataFrame and save
        print("PHASE 3: Save Results")
        print("-" * 70)
        
        if not scraped_data:
            print("⚠️  No data to save")
            return
        
        df = pd.DataFrame(scraped_data)
        
        # Ensure column order
        column_order = ['URL', 'Title', 'Publication_Date', 'Year', 'Article_Text']
        df = df[column_order]
        
        # Save to CSV
        output_path = Path(OUTPUT_FILE)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"✓ Saved: {output_path}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        
        # SUMMARY
        print("\n" + "="*70)
        print("SUMMARY (STEP 1 COMPLETE)")
        print("="*70)
        print(f"Total articles scraped: {len(df)}")
        print(f"Articles skipped: {skipped_count}")
        print(f"Errors: {error_count}")
        
        if len(df) > 0:
            print(f"\n📈 Field Completeness:")
            for col in ['Title', 'Publication_Date', 'Year', 'Article_Text']:
                non_null = df[col].notna().sum()
                pct = (non_null / len(df) * 100)
                print(f"  {col:20s}: {pct:5.1f}% ({non_null}/{len(df)})")
            
            # Year distribution
            if df['Year'].notna().sum() > 0:
                print(f"\n📅 Year Distribution:")
                year_counts = df['Year'].value_counts().sort_index(ascending=False)
                for year, count in year_counts.items():
                    if pd.notna(year):
                        print(f"  {int(year)}: {count} articles")
            
            # Article length statistics
            if df['Article_Text'].notna().sum() > 0:
                print(f"\n📝 Article Text Statistics:")
                article_lengths = df[df['Article_Text'].notna()]['Article_Text'].str.len()
                print(f"  Articles with text: {len(article_lengths)}/{len(df)} ({len(article_lengths)/len(df)*100:.1f}%)")
                print(f"  Average length: {article_lengths.mean():.0f} characters")
                print(f"  Min: {article_lengths.min()}, Max: {article_lengths.max()}")
            
            # Sample records
            print(f"\n📋 Sample Records (first 5):")
            sample_cols = ['Title', 'Publication_Date', 'Year']
            print(df[sample_cols].head(5).to_string(index=False))
        
        print("\n✅ STEP 1 COMPLETED SUCCESSFULLY")
        print(f"\nNext: Run STEP 2 (LLM or other analysis) on {output_path}")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("\n🔒 WebDriver closed")


if __name__ == "__main__":
    main()
