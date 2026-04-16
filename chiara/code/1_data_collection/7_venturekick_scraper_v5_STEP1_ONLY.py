"""
Venturekick.ch Scraper V5 - STEP 1 ONLY (Deterministic Extraction)

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

STEP 2 (LLM/regex analysis) will be done separately on this output.

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
MAX_ARTICLES = 500  # VentureKick has fewer articles than StartupTicker
MIN_YEAR = 2023     # Only scrape articles from 2023 onwards

OUTPUT_FILE = './data/venturekick_raw_articles_v5_step1.csv'


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
        r'Read more.*?(?=\n|$)',
        r'Accept all cookies.*?(?=\n|$)',
        r'Subscribe.*?(?=\n|$)',
        r'Share this.*?(?=\n|$)',
        r'Follow us.*?(?=\n|$)',
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
    1. Try VentureKick-specific selectors first
    2. Fallback to generic article selectors
    3. Final fallback: all <p> tags
    4. Clean the extracted text
    
    Returns: cleaned article text string or None
    """
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page load (VentureKick may be slower)
        
        article_text = None
        
        # VentureKick-specific selectors (CFM page structure)
        content_selectors = [
            'div.content',           # VentureKick main content div
            'div#content',           # VentureKick content by ID
            'div.article',           # Article wrapper
            'main',                  # Main content
            'div[class*="text"]',    # Text containers
            'div.body',              # Body content
            # Generic fallbacks
            'article',
            'div.post-content',
            'div.article-content',
            'div.news-content'
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
    
    VentureKick patterns:
    - DD.MM.YYYY (European format)
    - YYYY-MM-DD (ISO format)
    - Month DD, YYYY (English format)
    
    Returns: (date_str in YYYY-MM-DD format, year as int)
    """
    if not article_text:
        return None, None
    
    # Pattern 1: DD.MM.YYYY (e.g., "02.06.2025")
    pattern1 = r'(\d{2})\.(\d{2})\.(\d{4})'
    match = re.search(pattern1, article_text)
    if match:
        day, month, year = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    # Pattern 2: YYYY-MM-DD (e.g., "2025-06-02")
    pattern2 = r'(\d{4})-(\d{2})-(\d{2})'
    match = re.search(pattern2, article_text)
    if match:
        year, month, day = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    # Pattern 3: Month DD, YYYY (e.g., "June 2, 2025")
    months = {
        'january': '01', 'jan': '01',
        'february': '02', 'feb': '02',
        'march': '03', 'mar': '03',
        'april': '04', 'apr': '04',
        'may': '05',
        'june': '06', 'jun': '06',
        'july': '07', 'jul': '07',
        'august': '08', 'aug': '08',
        'september': '09', 'sep': '09',
        'october': '10', 'oct': '10',
        'november': '11', 'nov': '11',
        'december': '12', 'dec': '12'
    }
    
    pattern3 = r'(' + '|'.join(months.keys()) + r')\s+(\d{1,2}),?\s+(\d{4})'
    match = re.search(pattern3, article_text, re.IGNORECASE)
    if match:
        month_name, day, year = match.groups()
        month = months[month_name.lower()]
        day = day.zfill(2)
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    return None, None


# ============================================================================
# SCRAPING FUNCTIONS
# ============================================================================

def scrape_news_overview(driver, max_articles=MAX_ARTICLES):
    """
    Scrape VentureKick news overview page to collect article URLs and titles.
    
    Returns: List of dicts with 'url' and 'title' keys
    """
    # CORRECTED: VentureKick newsroom uses CFM with page parameter
    base_url = 'https://www.venturekick.ch/index.cfm?page=135424'
    news_items = []
    seen_urls = set()
    
    print(f"🔍 Scraping news overview: {base_url}")
    print(f"🎯 Target: {max_articles} articles\n")
    driver.get(base_url)
    
    wait = WebDriverWait(driver, 20)
    
    try:
        # Wait for page to load
        time.sleep(5)  # VentureKick uses CFM, needs more time
        
        # VentureKick-specific: Get all links on the newsroom page
        print(f"📄 Scraping newsroom page...", end='')
        
        # Scroll to load all content
        try:
            for scroll in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
        except Exception:
            pass
        
        # Extract all links that point to news articles
        # VentureKick news articles have URLs like: index.cfm?page=XXXXX
        all_links = driver.find_elements(By.TAG_NAME, 'a')
        
        new_items_found = 0
        
        for link in all_links:
            if len(news_items) >= max_articles:
                break
            
            try:
                url = link.get_attribute('href')
                
                if not url:
                    continue
                
                # VentureKick news articles: index.cfm?page=XXXXXX (6-digit page ID)
                # Skip the main newsroom page (135424) and admin pages
                if 'index.cfm' in url and 'page=' in url:
                    # Extract page parameter
                    page_match = re.search(r'page=(\d+)', url)
                    if page_match:
                        page_id = page_match.group(1)
                        # Skip the newsroom page itself (135424)
                        if page_id == '135424':
                            continue
                        
                        # Skip if we've seen this URL
                        if url in seen_urls:
                            continue
                        
                        seen_urls.add(url)
                        
                        # Get title from link text
                        title = link.text.strip()
                        if not title or len(title) < 5:
                            # Try to get title from parent element
                            try:
                                parent = link.find_element(By.XPATH, '..')
                                title = parent.text.strip()
                            except:
                                title = f"Article {page_id}"
                        
                        # Clean title
                        title = re.sub(r'\s+', ' ', title).strip()
                        if len(title) > 200:
                            title = title[:200] + "..."
                        
                        news_items.append({
                            'url': url,
                            'title': title
                        })
                        
                        new_items_found += 1
                
            except Exception:
                continue
        
        print(f" +{new_items_found} articles found")
        
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
        print("VENTUREKICK.CH SCRAPER V5 - STEP 1 ONLY")
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
        
        for i, item in enumerate(news_items, 1):
            # Progress indicator
            print(f"  [{i:3d}/{len(news_items)}] {item['title'][:50]}...", end='')
            
            try:
                result = scrape_article_step1(driver, item['url'], item['title'])
                
                if result:
                    scraped_data.append(result)
                    print(f" ✓ ({result.get('Year', 'N/A')})")
                else:
                    skipped_count += 1
                    print(f" ⊘ (skipped)")
                
            except Exception as e:
                error_count += 1
                print(f" ✗ (error)")
                continue
            
            # Rate limiting
            time.sleep(0.5)
            
            # Checkpoint every 50 articles
            if i % 50 == 0:
                print(f"\n{'='*70}")
                print(f"CHECKPOINT: {i}/{len(news_items)} processed")
                print(f"  ✓ Extracted: {len(scraped_data)}")
                print(f"  ⊘ Skipped: {skipped_count}")
                print(f"  ✗ Errors: {error_count}")
                print(f"{'='*70}\n")
        
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
