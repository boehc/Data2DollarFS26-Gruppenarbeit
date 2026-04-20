"""
Startupticker.ch News Scraper V7 (2-STEP PIPELINE WITH LLM)

NEW ARCHITECTURE (V7):
╔══════════════════════════════════════════════════════════════╗
║ STEP 1 — Deterministic Extraction (no LLM)                  ║
║   • Extract raw article_text (clean HTML)                    ║
║   • Extract publication_date via regex (DD.MM.YYYY)          ║
║   • Extract year from date                                   ║
║   • Extract URL                                              ║
╠══════════════════════════════════════════════════════════════╣
║ STEP 2 — LLM Analysis (ONE call per article)                ║
║   • Input: Full cleaned article text                        ║
║   • Output: All structured fields via LLM                   ║
║   • Fields: Startup name, industry, funding, investors,     ║
║             city, canton, keywords, website, etc.           ║
╚══════════════════════════════════════════════════════════════╝

WHY THIS APPROACH:
- Dates are 100% reliable via regex (LLMs miss them)
- LLM gets full context in one call (better extraction)
- Cleaner separation: deterministic vs interpretive
- Single LLM call per article = efficient
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
import json
import os

# ============================================================================
# CONFIGURATION
# ============================================================================
MAX_ARTICLES = 4500
MIN_YEAR = 2023  # Only scrape articles from 2023 onwards
USE_LLM = True  # Set to False to skip LLM calls (test mode)

# LLM Configuration (OpenAI GPT-4 or similar)
LLM_MODEL = "gpt-4o-mini"  # or "gpt-4o" for better quality
LLM_API_KEY = os.getenv("OPENAI_API_KEY")  # Set via: export OPENAI_API_KEY=sk-...


# ============================================================================
# STEP 1 — DETERMINISTIC EXTRACTION
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
    
    print("✓ WebDriver ready")
    return driver


def extract_clean_article_text(driver, url):
    """
    STEP 1a: Extract clean article text from HTML.
    Removes nav, footer, cookie banners, boilerplate.
    Returns: clean article text string
    """
    try:
        driver.get(url)
        time.sleep(1.5)
        
        # Try StartupTicker-specific selectors first (higher priority)
        article_text = None
        
        content_selectors = [
            'div.article-body',      # StartupTicker primary
            'div.news-content',      # StartupTicker secondary
            'main.content',          # StartupTicker main content
            'article.news',          # StartupTicker article wrapper
            'div.news-detail',       # StartupTicker detail view
            'article',               # Generic fallback
            'div.article-content',
            'div.content',
            'div[class*="text"]',
            'div.body'
        ]
        
        for selector in content_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    text = ' '.join([el.text for el in elements if el.text])
                    if text and len(text) > 100:
                        article_text = text
                        break
            except:
                continue
        
        # Fallback: Extract all <p> tags
        if not article_text or len(article_text) < 100:
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, 'p')
                article_text = ' '.join([p.text for p in paragraphs if p.text])
            except:
                pass
        
        # Clean the text
        if article_text:
            # Remove excessive whitespace
            article_text = re.sub(r'\s+', ' ', article_text).strip()
            # Remove common boilerplate
            article_text = re.sub(r'Read more about.*?(?=\n|$)', '', article_text, flags=re.IGNORECASE)
            article_text = re.sub(r'Accept all cookies.*?(?=\n|$)', '', article_text, flags=re.IGNORECASE)
            article_text = re.sub(r'Subscribe to newsletter.*?(?=\n|$)', '', article_text, flags=re.IGNORECASE)
        
        return article_text
    
    except Exception as e:
        print(f"  ⚠️  Error extracting article text: {str(e)[:50]}")
        return None


def extract_publication_date(article_text):
    """
    STEP 1b: Extract publication date via regex.
    Pattern: DD.MM.YYYY HH:MM (appears at bottom after company name)
    
    Returns: (date_str in YYYY-MM-DD format, year as int)
    Example: "02.06.2025" → ("2025-06-02", 2025)
    """
    if not article_text:
        return None, None
    
    # Pattern: DD.MM.YYYY HH:MM (e.g., "Lobby AG 02.06.2025 17:16")
    pattern = r'(\d{2})\.(\d{2})\.(\d{4})\s+\d{2}:\d{2}'
    
    # Search in last 200 characters (date is at bottom)
    search_text = article_text[-200:] if len(article_text) > 200 else article_text
    
    match = re.search(pattern, search_text)
    if match:
        day, month, year = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    # Fallback: Try full text if not found at bottom
    match = re.search(pattern, article_text)
    if match:
        day, month, year = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    return None, None


def scrape_article_deterministic(driver, url):
    """
    STEP 1: Deterministic extraction (no LLM).
    
    Returns dict with:
    - article_text: Full cleaned article text
    - publication_date: YYYY-MM-DD format
    - year: Integer year
    - url: Source URL
    """
    article_text = extract_clean_article_text(driver, url)
    publication_date, year = extract_publication_date(article_text)
    
    return {
        'article_text': article_text,
        'publication_date': publication_date,
        'year': year,
        'url': url
    }


# ============================================================================
# STEP 2 — LLM ANALYSIS
# ============================================================================

def create_llm_extraction_prompt(article_text, url):
    """
    Create the LLM prompt for extracting structured data from article text.
    Returns the full prompt for the LLM.
    """
    prompt = f"""You are a startup data extraction expert. Extract structured information from this Swiss startup news article.

ARTICLE TEXT:
{article_text}

SOURCE URL: {url}

EXTRACT THE FOLLOWING FIELDS (return as JSON):

1. **Startup_Name** (string): Company name being featured. Look for patterns like "CompanyName raises", "CompanyName announces", or capitalized company names.

2. **Industry** (string): Primary industry. Choose from:
   - FINTECH (financial services, payment, banking, blockchain, crypto)
   - HEALTHCARE (health, medtech, biotech, pharma, medical, diagnostics)
   - AI/ML (artificial intelligence, machine learning, deep learning)
   - SOFTWARE (SaaS, software platforms, cloud, enterprise software)
   - CLEANTECH (climate, energy, sustainability, renewable, carbon, solar)
   - MOBILITY (automotive, EV, electric vehicle, transport, logistics)
   - INDUSTRIALS (manufacturing, industrial, robotics, automation, construction)
   - AGTECH (food, agriculture, agritech, farming)
   - CONSUMER (ecommerce, retail, marketplace, fashion)
   - EDUCATION (edtech, learning, training)
   - AEROSPACE (space, satellite, aerospace, drone)
   - Unknown (if unclear)

3. **Sub_Industry** (string or null): More specific category. Examples:
   - Software & Platforms, Medical Devices, Drug Discovery, Digital Health
   - Financial Services, Blockchain & Crypto, E-Commerce, Marketplace
   - Mobility Services, Automotive Tech, Manufacturing, Industrial Automation
   - Logistics, Last-Mile Delivery, Renewable Energy, Carbon Management
   - Precision Agriculture, Food Tech, Data Analytics, AI Platforms
   - Cybersecurity, Learning Platforms, Collaboration Tools

4. **Business_Model_Type** (string): B2B, B2C, B2G, or Unknown

5. **Tech_Keywords** (string): Comma-separated list of up to 5 relevant technology keywords. Examples:
   - AI, Machine Learning, Blockchain, SaaS, Cloud, IoT, Big Data
   - Robotics, Automation, 3D Printing, AR/VR, Quantum Computing
   - Cybersecurity, API, Mobile, Web, DevOps, Microservices
   - GenAI, LLM, Computer Vision, NLP, Recommender Systems

6. **Funding_Amount** (string or null): Extract funding amount mentioned. Format: "5.2M USD" or "undisclosed"

7. **Funding_Round** (string or null): Seed, Series A, Series B, etc.

8. **Investment_Stage** (string): Pre-Seed, Seed, Series A, Series B, Series C+, Early Stage, Growth Stage, or Unknown

9. **Investor_Names** (string or null): Comma-separated list of investors mentioned (up to 5). Distinguish between current round investors vs past investors.

10. **City** (string or null): Swiss city where startup is located. Common cities: Zurich, Geneva, Basel, Bern, Lausanne, Lugano, Zug, St. Gallen

11. **Canton** (string or null): Swiss canton abbreviation (ZH, GE, BS, BE, VD, TI, LU, SG, ZG, etc.)

12. **Founded_Year** (integer or null): Year the startup was founded (if mentioned)

13. **Employees** (integer or null): Number of employees (if mentioned)

14. **Website** (string or null): Company website URL (exclude startupticker.ch). Ensure it starts with www or http

RESPONSE FORMAT (JSON only, no explanation):
{{
  "Startup_Name": "...",
  "Industry": "...",
  "Sub_Industry": "...",
  "Business_Model_Type": "...",
  "Tech_Keywords": "...",
  "Funding_Amount": "...",
  "Funding_Round": "...",
  "Investment_Stage": "...",
  "Investor_Names": "...",
  "City": "...",
  "Canton": "...",
  "Founded_Year": ...,
  "Employees": ...,
  "Website": "..."
}}

Return null for fields not found in the article. Ensure all fields are present in the JSON response.
"""
    return prompt


def call_llm_extraction(article_text, url):
    """
    STEP 2: Call LLM to extract all structured fields from article text.
    
    Returns dict with all extracted fields or None if LLM call fails.
    """
    if not USE_LLM:
        print("  ⚠️  LLM disabled (USE_LLM=False)")
        return None
    
    if not LLM_API_KEY:
        print("  ⚠️  No LLM API key (set OPENAI_API_KEY)")
        return None
    
    if not article_text or len(article_text) < 50:
        print("  ⚠️  Article text too short for LLM")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=LLM_API_KEY)
        
        prompt = create_llm_extraction_prompt(article_text, url)
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a data extraction expert. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for consistent extraction
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if result_text.startswith("```"):
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'```$', '', result_text)
        
        extracted_data = json.loads(result_text)
        
        return extracted_data
    
    except Exception as e:
        print(f"  ❌ LLM extraction error: {str(e)[:100]}")
        return None


# ============================================================================
# SCRAPING ORCHESTRATION
# ============================================================================

def scrape_news_overview(driver, max_articles=MAX_ARTICLES):
    """Scrape news overview page with pagination until max_articles reached."""
    base_url = 'https://www.startupticker.ch/en/news'
    news_items = []
    seen_urls = set()
    
    print(f"🔍 Scraping news overview: {base_url}")
    print(f"🎯 Target: {max_articles} articles")
    driver.get(base_url)
    
    wait = WebDriverWait(driver, 20)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item.news')))
        time.sleep(3)
        
        page = 1
        no_new_items_count = 0
        
        while len(news_items) < max_articles:
            print(f"📄 Page {page} (collected: {len(news_items)}/{max_articles})...")
            
            # Scroll for lazy loading
            try:
                for scroll in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
            except Exception:
                pass
            
            items = driver.find_elements(By.CSS_SELECTOR, 'div.item.news')
            new_items_found = 0
            
            for item in items:
                if len(news_items) >= max_articles:
                    print(f"✅ Reached limit of {max_articles} articles!")
                    break
                
                try:
                    # Extract URL
                    link_elem = item.find_element(By.CSS_SELECTOR, 'a[href*="/news/"]')
                    url = link_elem.get_attribute('href')
                    
                    if url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    
                    # Extract title (for initial filtering)
                    title_elem = item.find_element(By.CSS_SELECTOR, 'h2, h3, .title')
                    title = title_elem.text.strip()
                    
                    news_items.append({
                        'url': url,
                        'title': title
                    })
                    
                    new_items_found += 1
                    
                except Exception:
                    continue
            
            if new_items_found == 0:
                no_new_items_count += 1
                if no_new_items_count >= 3:
                    print("⚠️  No new items found (3x)")
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
                        break
                except:
                    break
        
        return news_items
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return news_items


def scrape_article_2step(driver, url, title):
    """
    Execute 2-step pipeline for one article.
    
    STEP 1: Deterministic extraction (text, date, year, url)
    STEP 2: LLM extraction (all structured fields)
    
    Returns: Combined dict with all fields
    """
    # STEP 1: Deterministic extraction
    step1_data = scrape_article_deterministic(driver, url)
    
    if not step1_data['article_text']:
        print(f"  ⚠️  No article text extracted")
        return None
    
    # Filter by year (MIN_YEAR)
    if step1_data['year'] and step1_data['year'] < MIN_YEAR:
        return None  # Skip old articles
    
    # STEP 2: LLM extraction
    step2_data = call_llm_extraction(step1_data['article_text'], url)
    
    if not step2_data:
        print(f"  ⚠️  LLM extraction failed")
        return None
    
    # Combine STEP 1 + STEP 2 data
    combined = {
        # From STEP 1 (deterministic)
        'Publication_Date': step1_data['publication_date'],
        'Year': step1_data['year'],
        'Article_Text': step1_data['article_text'],
        'URL': step1_data['url'],
        
        # From STEP 2 (LLM)
        'Startup_Name': step2_data.get('Startup_Name'),
        'Industry': step2_data.get('Industry'),
        'Sub_Industry': step2_data.get('Sub_Industry'),
        'Business_Model_Type': step2_data.get('Business_Model_Type'),
        'Tech_Keywords': step2_data.get('Tech_Keywords'),
        'Funding_Amount': step2_data.get('Funding_Amount'),
        'Funding_Round': step2_data.get('Funding_Round'),
        'Investment_Stage': step2_data.get('Investment_Stage'),
        'Investor_Names': step2_data.get('Investor_Names'),
        'City': step2_data.get('City'),
        'Canton': step2_data.get('Canton'),
        'Founded_Year': step2_data.get('Founded_Year'),
        'Employees': step2_data.get('Employees'),
        'Website': step2_data.get('Website'),
        
        # Fixed field
        'Location': 'Switzerland'
    }
    
    return combined


def create_dataframe(scraped_data):
    """Convert scraped data to DataFrame with proper schema."""
    if not scraped_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(scraped_data)
    
    # Define schema (18 fields)
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Publication_Date', 'Article_Text',
        'Year', 'Funding_Amount', 'Funding_Round',
        'Investment_Stage', 'Investor_Names', 'Location', 'City',
        'Canton', 'Founded_Year', 'Employees', 'Website'
    ]
    
    # Ensure all columns exist
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    # Reorder columns
    df = df[required_columns]
    
    return df


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main scraping logic with 2-step pipeline."""
    driver = None
    
    try:
        driver = setup_driver()
        
        print("\n" + "="*70)
        print("STARTUPTICKER.CH SCRAPER V7 (2-STEP PIPELINE WITH LLM)")
        print("="*70)
        print("ARCHITECTURE:")
        print("  STEP 1: Deterministic extraction (text, date, year, url)")
        print("  STEP 2: LLM analysis (all structured fields)")
        print(f"FILTER: Only articles from {MIN_YEAR} onwards")
        print(f"LLM: {'Enabled' if USE_LLM else 'DISABLED'} (model: {LLM_MODEL})")
        print("="*70)
        
        # PHASE 1: Collect article URLs
        print("\n🔍 PHASE 1: Collect article URLs...")
        news_items = scrape_news_overview(driver, max_articles=MAX_ARTICLES)
        
        if not news_items:
            print("⚠️  No articles found")
            return
        
        print(f"✓ Collected {len(news_items)} article URLs")
        
        # PHASE 2: 2-step extraction for each article
        print(f"\n📄 PHASE 2: 2-step extraction ({len(news_items)} articles)...")
        print("  Format: [Article #] Title → STEP1 → STEP2 → Status")
        
        scraped_data = []
        
        for i, item in enumerate(news_items, 1):
            print(f"\n[{i}/{len(news_items)}] {item['title'][:60]}...")
            
            try:
                result = scrape_article_2step(driver, item['url'], item['title'])
                
                if result:
                    scraped_data.append(result)
                    print(f"  ✓ Extracted: {result.get('Startup_Name', 'Unknown')} | "
                          f"{result.get('Industry', 'N/A')} | "
                          f"{result.get('Publication_Date', 'N/A')}")
                else:
                    print(f"  ⚠️  Skipped (no data or old article)")
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:80]}")
                continue
            
            # Rate limiting
            time.sleep(0.5)
            
            # Progress checkpoint every 50 articles
            if i % 50 == 0:
                print(f"\n{'='*70}")
                print(f"CHECKPOINT: {i}/{len(news_items)} articles processed")
                print(f"Successfully extracted: {len(scraped_data)} startups")
                print(f"{'='*70}\n")
        
        # PHASE 3: Create DataFrame and save
        print(f"\n📊 PHASE 3: Creating DataFrame...")
        df = create_dataframe(scraped_data)
        
        output_path = './data/startupticker_startups_v7_LLM.csv'
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"✓ Saved: {output_path}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        
        # SUMMARY
        print("\n" + "="*70)
        print("SUMMARY (V7 - 2-STEP LLM PIPELINE)")
        print("="*70)
        print(f"Total startups: {len(df)}")
        
        if len(df) > 0:
            print(f"\n📈 Field Completeness:")
            for col in ['Startup_Name', 'Industry', 'Tech_Keywords', 'Sub_Industry', 
                       'Publication_Date', 'Year', 'Funding_Amount', 'Investor_Names',
                       'City', 'Canton', 'Founded_Year', 'Employees', 'Website']:
                non_null = df[col].notna().sum()
                pct = (non_null / len(df) * 100)
                print(f"  {col:20s}: {pct:5.1f}% ({non_null}/{len(df)})")
            
            # Year distribution
            if df['Year'].notna().sum() > 0:
                print(f"\n📅 Year Distribution:")
                year_counts = df['Year'].value_counts().sort_index(ascending=False)
                for year, count in year_counts.head(10).items():
                    if pd.notna(year):
                        print(f"  {int(year)}: {count} startups")
            
            # Industry distribution
            if df['Industry'].notna().sum() > 0:
                print(f"\n🏢 Industry Distribution:")
                ind_counts = df['Industry'].value_counts()
                for ind, count in ind_counts.head(10).items():
                    print(f"  {ind}: {count} startups")
            
            # Sample records
            print(f"\n📋 Sample Records (first 5):")
            sample_cols = ['Startup_Name', 'Industry', 'Tech_Keywords', 'City', 'Publication_Date']
            print(df[sample_cols].head(5).to_string(index=False))
        
        print("\n✅ SCRAPING COMPLETED SUCCESSFULLY")
        
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
