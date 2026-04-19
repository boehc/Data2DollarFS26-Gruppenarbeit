"""
Startupticker.ch News Scraper V6 (MULTI-KEYWORD + FULL ARTICLE TEXT)
NEUE VERBESSERUNGEN IN V6:
- MULTI-KEYWORD Extraction: Returns top 5 keywords per startup (not just 1!)
- 80+ keyword categories (added 22 from friend's successful list)
- Publication_Date field added (18-field schema)
- Article_Text field added (full article body)
- Aligned with friend's 37 keywords: GenAI, LLM, Infrastructure, Gaming, etc.
"""

import time
import re
import pandas as pd
from pathlib import Path
from selenium import webdriver
from enhanced_keywords_v6 import extract_tech_keywords_multi
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# LIMIT für Artikel-Scraping (total)
MAX_ARTICLES = 50

# Year filter (only keep startups from this year onwards)
MIN_YEAR = 2023  # Focus on recent data (2023-2026)


def setup_driver():
    """Richtet Selenium Chrome WebDriver ein (headless)."""
    print("Richte Chrome WebDriver ein...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("✓ WebDriver bereit")
    return driver


def extract_company_from_title(title):
    """
    Extrahiert Company-Namen aus Artikel-Titel.
    IMPROVED: Looks for startup name patterns, avoids investor names.
    """
    if not title:
        return None
    
    # Skip common non-company words
    skip_words = {'ANNOUNCES', 'RAISES', 'SECURES', 'RECEIVES', 'WINS', 'LAUNCHES', 
                  'ANNOUNCES', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'MILLION', 'FUNDING'}
    
    words = title.split()
    
    # Pattern 1: "CompanyName raises/secures/announces"
    for i, word in enumerate(words):
        if word.upper() in ['RAISES', 'SECURES', 'ANNOUNCES', 'RECEIVES', 'WINS'] and i > 0:
            candidate = words[i-1]
            clean = re.sub(r'[^\w]', '', candidate)
            if clean and len(clean) >= 2 and clean.upper() not in skip_words:
                return clean
    
    # Pattern 2: First capitalized word (3+ chars) that's not a skip word
    for word in words:
        clean = re.sub(r'[^\w]', '', word)
        if clean and word[0].isupper() and len(clean) >= 3 and clean.upper() not in skip_words:
            return clean
    
    return None


def extract_funding_info(text):
    """
    Extrahiert Funding-Informationen aus Text (verbessert).
    IMPROVED: Better German support, 7-figure detection.
    Follows LLM_EXTRACTION_PROMPT.md guidelines.
    """
    if not text:
        return None, None
    
    # Erweiterte Patterns (English & German)
    patterns = [
        # "CHF 5.2 million", "$10M", "€3.5M"
        r'(USD|CHF|EUR|€|\$)\s*(\d+[\.,]?\d*)\s*(million|mio|m\b)',
        r'(\d+[\.,]?\d*)\s*(million|mio|m\b)\s*(USD|CHF|EUR|€|\$)',
        # "5 million francs", "10 million dollars"
        r'(\d+[\.,]?\d*)\s*million\s*(francs?|dollars?|euros?)',
        # "raises $5M", "secures CHF 10M"
        r'(?:raises?|secures?|receives?)\s+(USD|CHF|EUR|\$)\s*(\d+[\.,]?\d*)\s*([MK]|million)?',
        # Deutsch: "erhält CHF 5 Millionen", "3,5 Millionen Euro"
        r'(?:erhält|bekommt|sichert)\s+(CHF|USD|EUR)\s*(\d+[\.,]?\d*)\s*Million',
        r'(\d+,\d+)\s*Millionen\s+(Euro|Franken|Dollar)',
        # "undisclosed amount", "Millionenbetrag"
        r'undisclosed\s+(?:amount|sum|round)',
        r'Millionenbetrag',
        # German: "siebenstelliger Betrag" (7-figure), "sechsstelliger" (6-figure)
        r'(sieben|sechs|acht|neun)stelliger\s+Betrag',
        # K-Format: "CHF 150K", "$500K"
        r'(USD|CHF|EUR|\$)\s*(\d+[\.,]?\d*)\s*K\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                matched_text = match.group(0)
                
                # Handle "undisclosed" or "Millionenbetrag"
                if 'undisclosed' in matched_text.lower() or 'Millionenbetrag' in matched_text:
                    return 'undisclosed', 'Undisclosed'
                
                # Handle German figure descriptions: "siebenstelliger Betrag"
                if 'stelliger' in matched_text:
                    figure_map = {
                        'sechs': 'undisclosed (6-figure)',
                        'sieben': 'undisclosed (7-figure)',
                        'acht': 'undisclosed (8-figure)',
                        'neun': 'undisclosed (9-figure)'
                    }
                    for word, desc in figure_map.items():
                        if word in matched_text.lower():
                            return desc, 'Undisclosed'
                
                amount = None
                currency = None
                unit = 'M'  # Default Million
                
                groups = match.groups()
                for g in groups:
                    if g and re.match(r'\d+[\.,]?\d*', g):
                        # Handle German comma decimal: 3,5 → 3.5
                        amount = float(g.replace(',', '.'))
                    elif g and g.upper() in ['USD', 'CHF', 'EUR', '$', '€']:
                        currency = g.upper().replace('$', 'USD').replace('€', 'EUR')
                    elif g and g.upper() in ['K', 'M']:
                        unit = g.upper()
                    elif g and any(x in g.lower() for x in ['franc', 'dollar', 'euro']):
                        if 'franc' in g.lower():
                            currency = 'CHF'
                        elif 'dollar' in g.lower():
                            currency = 'USD'
                        elif 'euro' in g.lower():
                            currency = 'EUR'
                
                if amount and currency:
                    # Format: "5.2M USD" or "150K CHF"
                    if unit == 'K':
                        # Convert K to M: 150K → 0.15M
                        amount_m = amount / 1000
                        return f"{amount_m}M {currency}", 'Seed'
                    else:
                        return f"{amount}M {currency}", 'Seed'
                    
            except:
                continue
    
    return None, None


def extract_investors(text):
    """
    Extrahiert Investor-Namen aus Text.
    IMPROVED: Better distinction between current vs past investors.
    """
    if not text:
        return None
    
    patterns = [
        # "led by X", "together with Y"
        r'(?:led by|führt|angeführt von|together with|mit|gemeinsam mit)\s+([A-Z][A-Za-z\s&,.-]+(?:Capital|Ventures|Partners|Fund|AG|GmbH|SA|Ltd))',
        # "investors include X, Y"
        r'(?:investor|Investor)s?\s+(?:include|such as|wie)?\s*:?\s*([A-Z][A-Za-z\s&,.-]+)',
        # "from X Capital"
        r'(?:from|von)\s+([A-Z][A-Za-z\s&,.-]+(?:Capital|Ventures|Partners|Fund))',
        # "strategic investment from X"
        r'(?:investment from|Investition von)\s+([A-Z][A-Z][A-Za-z\s&,.-]+)',
    ]
    
    investors = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            investor = match.group(1).strip()
            # Clean up trailing punctuation
            investor = re.sub(r'[,.:;]+$', '', investor)
            if len(investor) > 3 and investor not in investors:
                # Avoid generic words
                if not any(skip in investor.lower() for skip in ['the startup', 'the company', 'this round']):
                    investors.append(investor)
    
    if investors:
        return ', '.join(investors[:5])  # Top 5 investors
    
    return None


def extract_city_canton(text, title=''):
    """
    Extrahiert City und Canton aus Text.
    NEW: Follows LLM_EXTRACTION_PROMPT.md guidelines.
    Returns: (city, canton) tuple
    """
    if not text and not title:
        return None, None
    
    combined = (text or '') + ' ' + (title or '')
    
    # Swiss cities with their cantons
    city_canton_map = {
        # Major cities
        'ZURICH': ('Zurich', 'ZH'),
        'ZÜRICH': ('Zurich', 'ZH'),
        'GENEVA': ('Geneva', 'GE'),
        'GENÈVE': ('Geneva', 'GE'),
        'GENF': ('Geneva', 'GE'),
        'BASEL': ('Basel', 'BS'),
        'BERN': ('Bern', 'BE'),
        'LAUSANNE': ('Lausanne', 'VD'),
        'LUGANO': ('Lugano', 'TI'),
        'LUCERNE': ('Lucerne', 'LU'),
        'LUZERN': ('Lucerne', 'LU'),
        'ST. GALLEN': ('St. Gallen', 'SG'),
        'ST.GALLEN': ('St. Gallen', 'SG'),
        'SANKT GALLEN': ('St. Gallen', 'SG'),
        'ZUG': ('Zug', 'ZG'),
        'WINTERTHUR': ('Winterthur', 'ZH'),
        'BELLINZONA': ('Bellinzona', 'TI'),
        'RENENS': ('Renens', 'VD'),
        'AARAU': ('Aarau', 'AG'),
        'FRIBOURG': ('Fribourg', 'FR'),
        'NEUCHÂTEL': ('Neuchatel', 'NE'),
        'NEUCHATEL': ('Neuchatel', 'NE'),
        'SION': ('Sion', 'VS'),
        'CHUR': ('Chur', 'GR'),
    }
    
    # Patterns to look for
    patterns = [
        r'([\w\s.]+)-based',
        r'based in ([\w\s.]+)',
        r'Founded in ([\w\s.]+)',
        r'Das ([\w\s.]+) Startup',
        r'Die ([\w\s.]+) Startup',
        r'gegründet in ([\w\s.]+)',
    ]
    
    text_upper = combined.upper()
    
    # Check direct city mentions
    for city_key, (city_name, canton_code) in city_canton_map.items():
        if city_key in text_upper:
            return city_name, canton_code
    
    # Check patterns
    for pattern in patterns:
        match = re.search(pattern, combined, re.IGNORECASE)
        if match:
            city_candidate = match.group(1).strip().upper()
            if city_candidate in city_canton_map:
                return city_canton_map[city_candidate]
    
    return None, None


def extract_founded_year(text):
    """
    Extrahiert Gründungsjahr aus Text.
    NEW: Follows LLM_EXTRACTION_PROMPT.md guidelines.
    """
    if not text:
        return None
    
    patterns = [
        r'founded in (\d{4})',
        r'gegründet (\d{4})',
        r'established in (\d{4})',
        r'seit (\d{4})',
        r'gestartet (\d{4})',
        r'founded\s+in\s+(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            # Sanity check: year between 1990 and 2026
            if 1990 <= year <= 2026:
                return year
    
    return None


def extract_employees(text):
    """
    Extrahiert Mitarbeiteranzahl aus Text.
    NEW: Follows LLM_EXTRACTION_PROMPT.md guidelines.
    """
    if not text:
        return None
    
    patterns = [
        r'team of (\d+)',
        r'(\d+) employees',
        r'(\d+) Mitarbeitende',
        r'(\d+) Personen',
        r'grown to (\d+)',
        r'gewachsen auf (\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            count = int(match.group(1))
            # Sanity check: reasonable employee count
            if 1 <= count <= 10000:
                return count
    
    return None


def extract_website(text):
    """
    Extrahiert Website-URL aus Text.
    NEW: Follows LLM_EXTRACTION_PROMPT.md guidelines.
    """
    if not text:
        return None
    
    # Pattern for URLs
    patterns = [
        r'(?:www\.|https?://)([\w.-]+\.(?:com|ch|io|net|org|ai))',
        r'(?:visit|website|site)\s+(?:at\s+)?([\w.-]+\.(?:com|ch|io|net|org|ai))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group(0) if 'www' in match.group(0) or 'http' in match.group(0) else match.group(1)
            # Exclude startupticker.ch
            if 'startupticker' not in url.lower():
                # Ensure it starts with www or http
                if not url.startswith(('http', 'www')):
                    url = 'www.' + url
                return url
    
    return None


def extract_publication_date(text):
    """
    Extrahiert Publikationsdatum aus Artikel.
    NEW: Follows LLM_EXTRACTION_PROMPT.md - date is at bottom in format DD.MM.YYYY HH:MM
    Returns: (date_str in YYYY-MM-DD format, year as int)
    """
    if not text:
        return None, None
    
    # Pattern: "Company AG DD.MM.YYYY HH:MM" at end of article
    pattern = r'(\d{2})\.(\d{2})\.(\d{4})\s+\d{2}:\d{2}'
    
    # Search in last 200 characters (date is at bottom)
    search_text = text[-200:] if len(text) > 200 else text
    
    match = re.search(pattern, search_text)
    if match:
        day, month, year = match.groups()
        date_str = f"{year}-{month}-{day}"
        year_int = int(year)
        return date_str, year_int
    
    return None, None


# NOTE: extract_tech_keywords_multi is imported from enhanced_keywords_v6.py


def extract_sub_industry_enhanced(text, tags=[], title='', industry=''):
    """
    VERBESSERTE Sub-Industry Extraktion mit mehr Granularität.
    """
    # Nutze alle verfügbaren Infos
    combined_text = ' '.join(filter(None, [text or '', title or '', ' '.join(tags or [])]))
    
    if not combined_text or len(combined_text) < 10:
        return None
    
    text_upper = combined_text.upper()
    
    # ERWEITERTE Sub-Industries mit mehr Detail
    sub_industries = {
        # Software & Platforms
        'SOFTWARE & PLATFORMS': ['SOFTWARE', 'PLATFORM', 'SAAS', 'APPLICATION', 'APP ',
                                  'CLOUD-BASED', 'WEB APP', 'MOBILE APP'],
        
        # Medical & Healthcare
        'MEDICAL DEVICES': ['MEDICAL DEVICE', 'DIAGNOSTICS', 'IMPLANT', 'INSTRUMENT',
                            'SURGICAL', 'MEDICAL EQUIPMENT'],
        'DRUG DISCOVERY': ['DRUG', 'PHARMACEUTICAL', 'THERAPY', 'TREATMENT', 'CLINICAL TRIAL',
                           'ANTIBODY', 'MOLECULE'],
        'DIGITAL HEALTH': ['DIGITAL HEALTH', 'TELEHEALTH', 'TELEMEDICINE', 'HEALTH APP',
                           'REMOTE MONITORING'],
        
        # Financial Services
        'FINANCIAL SERVICES': ['BANKING', 'PAYMENT', 'INSURANCE', 'LENDING', 'WEALTH MANAGEMENT'],
        'BLOCKCHAIN & CRYPTO': ['BLOCKCHAIN', 'CRYPTO', 'DEFI', 'WEB3', 'NFT'],
        
        # Commerce
        'E-COMMERCE': ['ONLINE SHOP', 'E-COMMERCE', 'MARKETPLACE', 'RETAIL PLATFORM'],
        'MARKETPLACE': ['MARKETPLACE', 'TWO-SIDED', 'PEER-TO-PEER', 'P2P'],
        
        # Mobility
        'MOBILITY SERVICES': ['RIDESHARE', 'CAR SHARING', 'TRANSPORTATION SERVICE', 'FLEET'],
        'AUTOMOTIVE TECH': ['AUTOMOTIVE', 'ELECTRIC VEHICLE', 'AUTONOMOUS DRIVING'],
        
        # Manufacturing & Industry
        'MANUFACTURING': ['PRODUCTION', 'FACTORY', 'MANUFACTURING', 'INDUSTRIAL'],
        'INDUSTRIAL AUTOMATION': ['INDUSTRIAL AUTOMATION', 'INDUSTRY 4.0', 'SMART FACTORY'],
        
        # Logistics & Supply Chain
        'LOGISTICS': ['SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY', 'FULFILLMENT', 'LOGISTICS'],
        'LAST-MILE DELIVERY': ['LAST-MILE', 'DELIVERY SERVICE', 'COURIER'],
        
        # Energy & Cleantech
        'RENEWABLE ENERGY': ['SOLAR', 'WIND ENERGY', 'RENEWABLE ENERGY', 'CLEAN ENERGY'],
        'CARBON MANAGEMENT': ['CARBON', 'CO2', 'EMISSION', 'CARBON CAPTURE'],
        
        # AgTech
        'PRECISION AGRICULTURE': ['PRECISION FARMING', 'AGTECH', 'SMART FARMING'],
        'FOOD TECH': ['FOOD TECH', 'ALTERNATIVE PROTEIN', 'PLANT-BASED'],
        
        # PropTech
        'PROPERTY MANAGEMENT': ['PROPERTY MANAGEMENT', 'FACILITY MANAGEMENT'],
        'SMART BUILDINGS': ['SMART BUILDING', 'BUILDING AUTOMATION'],
        
        # Data & Analytics
        'DATA ANALYTICS': ['DATA ANALYTICS', 'BUSINESS INTELLIGENCE', 'DATA VISUALIZATION'],
        'AI PLATFORMS': ['AI PLATFORM', 'ML PLATFORM', 'AI-AS-A-SERVICE'],
        
        # Cybersecurity
        'CYBERSECURITY': ['CYBERSECURITY', 'SECURITY PLATFORM', 'THREAT DETECTION'],
        
        # EdTech
        'LEARNING PLATFORMS': ['LEARNING PLATFORM', 'E-LEARNING', 'ONLINE EDUCATION'],
        'CORPORATE TRAINING': ['CORPORATE TRAINING', 'EMPLOYEE TRAINING'],
        
        # Communication & Collaboration
        'COLLABORATION TOOLS': ['COLLABORATION', 'TEAM TOOL', 'PRODUCTIVITY TOOL'],
        'VIDEO & COMMUNICATION': ['VIDEO CONFERENCING', 'COMMUNICATION PLATFORM'],
    }
    
    # Priorität: Spezifischste zuerst
    for sub_ind, patterns in sub_industries.items():
        if any(pattern in text_upper for pattern in patterns):
            return sub_ind
    
    # Fallback basierend auf Industry
    if industry == 'SOFTWARE':
        return 'SOFTWARE & PLATFORMS'
    elif industry == 'HEALTHCARE':
        return 'DIGITAL HEALTH'
    elif industry == 'FINTECH':
        return 'FINANCIAL SERVICES'
    
    return None


def extract_year_from_date(date_str):
    """Extrahiert Jahr aus Datum-String."""
    if not date_str:
        return None
    year_match = re.search(r'20\d{2}', date_str)
    return int(year_match.group(0)) if year_match else None


def scrape_news_overview(driver, max_articles=MAX_ARTICLES):
    """Scraped News-Übersicht mit Pagination bis max_articles erreicht ist."""
    base_url = 'https://www.startupticker.ch/en/news'
    news_items = []
    seen_urls = set()
    
    print(f"Öffne {base_url}")
    print(f"🎯 Ziel: {max_articles} Artikel")
    driver.get(base_url)
    
    wait = WebDriverWait(driver, 20)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item.news')))
        time.sleep(3)
        
        page = 1
        no_new_items_count = 0
        
        while len(news_items) < max_articles:
            print(f"📄 Scrape Seite {page} (bisher: {len(news_items)}/{max_articles})...")
            
            # Scrolle für Lazy Loading (mit Error-Handling)
            try:
                for scroll in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
            except Exception as scroll_err:
                print(f"⚠️ Scroll-Fehler (ignoriert): {scroll_err}")
                pass
            
            items = driver.find_elements(By.CSS_SELECTOR, 'div.item.news')
            new_items_found = 0
            
            for item in items:
                # Stop wenn Limit erreicht
                if len(news_items) >= max_articles:
                    print(f"✅ Limit von {max_articles} Artikeln erreicht!")
                    break
                
                try:
                    # URL (Primary Key)
                    link_elem = item.find_element(By.CSS_SELECTOR, 'a[href*="/news/"]')
                    url = link_elem.get_attribute('href')
                    
                    if url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    
                    # Titel
                    title_elem = item.find_element(By.CSS_SELECTOR, 'h2, h3, .title')
                    title = title_elem.text.strip()
                    
                    # Datum
                    date_elem = None
                    try:
                        date_elem = item.find_element(By.CSS_SELECTOR, 'time, .date, span.meta')
                        date = date_elem.text.strip()
                    except:
                        date = None
                    
                    # Tags
                    tags = []
                    try:
                        tag_elems = item.find_elements(By.CSS_SELECTOR, 'span.tag, .category, .label')
                        tags = [tag.text.strip() for tag in tag_elems if tag.text.strip()]
                    except:
                        pass
                    
                    news_items.append({
                        'url': url,
                        'title': title,
                        'date': date,
                        'tags': ', '.join(tags) if tags else None
                    })
                    
                    new_items_found += 1
                    
                except Exception as item_err:
                    continue
            
            if new_items_found == 0:
                no_new_items_count += 1
                if no_new_items_count >= 3:
                    print("⚠️ Keine neuen Items mehr gefunden (3x)")
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
        print(f"❌ Fehler: {e}")
        return news_items


def scrape_article_detail(driver, url, tags_str='', title=''):
    """
    Scraped Details aus einem Artikel.
    IMPROVED: Now extracts city, canton, founded_year, employees, website, publication_date.
    Follows LLM_EXTRACTION_PROMPT.md guidelines.
    """
    try:
        driver.get(url)
        time.sleep(1.5)
        
        content = None
        try:
            content_selectors = [
                'div.article-body',     # StartupTicker specific (PRIORITIZED)
                'div.news-content',     # StartupTicker specific (PRIORITIZED)
                'main.content',         # StartupTicker specific (PRIORITIZED)
                'article.news',         # StartupTicker specific (PRIORITIZED)
                'div.news-detail',      # StartupTicker specific (PRIORITIZED)
                'article',
                'div.article-content',
                'div.content',
                'div[class*="text"]',
                'div.body'
            ]
            for selector in content_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        content = ' '.join([el.text for el in elements if el.text])
                        if content and len(content) > 100:
                            break
                except:
                    continue
        except:
            pass
        
        # Falls kein Content, probiere alle <p> Tags
        if not content or len(content) < 100:
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, 'p')
                content = ' '.join([p.text for p in paragraphs if p.text])
            except:
                pass
        
        # Extract all fields
        investors = extract_investors(content) if content else None
        funding_from_content, _ = extract_funding_info(content) if content else (None, None)
        
        # NEW: Extract city, canton, founded_year, employees, website, publication_date
        city, canton = extract_city_canton(content, title) if content else (None, None)
        founded_year = extract_founded_year(content) if content else None
        employees = extract_employees(content) if content else None
        website = extract_website(content) if content else None
        publication_date, pub_year = extract_publication_date(content) if content else (None, None)
        
        # Multi-keyword extraction (returns top 5)
        tags_list = tags_str.split(', ') if tags_str else []
        tech_keywords = extract_tech_keywords_multi(content, tags_list, title)
        
        # Validate multi-keyword return value (IMPROVED V6)
        if tech_keywords and not isinstance(tech_keywords, str):
            tech_keywords = None
        elif tech_keywords:
            # Ensure max 5 keywords
            kw_list = [k.strip() for k in tech_keywords.split(',')]
            if len(kw_list) > 5:
                tech_keywords = ', '.join(kw_list[:5])
        
        sub_industry = extract_sub_industry_enhanced(content, tags_list, title)
        
        return {
            'content': content,
            'investors': investors,
            'funding_from_content': funding_from_content,
            'tech_keywords': tech_keywords,
            'sub_industry': sub_industry,
            'city': city,
            'canton': canton,
            'founded_year': founded_year,
            'employees': employees,
            'website': website,
            'publication_date': publication_date,
            'pub_year': pub_year,
        }
        
    except Exception as e:
        return {
            'content': None,
            'investors': None,
            'funding_from_content': None,
            'tech_keywords': None,
            'sub_industry': None,
            'city': None,
            'canton': None,
            'founded_year': None,
            'employees': None,
            'website': None,
            'publication_date': None,
            'pub_year': None,
        }


def map_to_schema(news_items):
    """Mappt News-Daten zu 16-Felder Schema."""
    if not news_items:
        return pd.DataFrame()
    
    mapped_data = []
    
    for item in news_items:
        startup_name = extract_company_from_title(item['title'])
        
        if not startup_name:
            continue
        
        year = extract_year_from_date(item['date'])
        
        # FILTER: Nur 2023-2026 (configurable via MIN_YEAR)
        if year and year < MIN_YEAR:
            continue
        
        # Funding: Priorität Content > Titel
        funding_amount = item.get('funding_from_content') or extract_funding_info(item['title'])[0]
        funding_round = extract_funding_info(item['title'])[1]
        
        # Industry aus Tags + Titel (ECHTE Industries, nicht B2B!)
        tags_str = item.get('tags', '') or ''
        title_lower = item['title'].lower()
        combined_text = (tags_str + ' ' + title_lower).lower()
        
        industry = None
        if any(kw in combined_text for kw in ['fintech', 'financial', 'payment', 'banking', 'blockchain', 'crypto']):
            industry = 'FINTECH'
        elif any(kw in combined_text for kw in ['health', 'medtech', 'biotech', 'pharma', 'medical', 'diagnostic', 'clinical']):
            industry = 'HEALTHCARE'
        elif any(kw in combined_text for kw in ['ai', 'artificial intelligence', 'machine learning', 'deep learning']):
            industry = 'AI/ML'
        elif any(kw in combined_text for kw in ['saas', 'software', 'platform', 'cloud', 'enterprise software']):
            industry = 'SOFTWARE'
        elif any(kw in combined_text for kw in ['climate', 'energy', 'sustainability', 'cleantech', 'renewable', 'carbon', 'solar']):
            industry = 'CLEANTECH'
        elif any(kw in combined_text for kw in ['mobility', 'automotive', 'ev', 'electric vehicle', 'transport', 'logistics']):
            industry = 'MOBILITY'
        elif any(kw in combined_text for kw in ['manufacturing', 'industrial', 'robotics', 'automation', 'construction']):
            industry = 'INDUSTRIALS'
        elif any(kw in combined_text for kw in ['food', 'agriculture', 'agritech', 'farming']):
            industry = 'AGTECH'
        elif any(kw in combined_text for kw in ['ecommerce', 'retail', 'marketplace', 'fashion', 'consumer']):
            industry = 'CONSUMER'
        elif any(kw in combined_text for kw in ['education', 'edtech', 'learning', 'training']):
            industry = 'EDUCATION'
        elif any(kw in combined_text for kw in ['space', 'satellite', 'aerospace', 'drone']):
            industry = 'AEROSPACE'
        else:
            industry = 'Unknown'
        
        # Business Model Type (B2B/B2C/B2G)
        business_model = 'Unknown'
        if any(kw in combined_text for kw in ['enterprise', 'b2b', 'business', 'saas', 'platform', 'industrial']):
            business_model = 'B2B'
        elif any(kw in combined_text for kw in ['consumer', 'retail', 'ecommerce', 'marketplace', 'b2c']):
            business_model = 'B2C'
        elif any(kw in combined_text for kw in ['government', 'public sector', 'civic', 'b2g']):
            business_model = 'B2G'
        
        # Investment Stage aus Funding Amount
        investment_stage = 'Early Stage'
        if funding_amount and funding_amount != 'undisclosed':
            amount_match = re.search(r'(\d+\.?\d*)', str(funding_amount))
            if amount_match:
                amount_val = float(amount_match.group(1))
                if amount_val < 1:
                    investment_stage = 'Pre-Seed'
                elif amount_val < 3:
                    investment_stage = 'Seed'
                elif amount_val < 10:
                    investment_stage = 'Series A'
                elif amount_val < 30:
                    investment_stage = 'Series B'
                else:
                    investment_stage = 'Series C+'
        
        # Tags-Override
        if tags_str:
            tags_upper = tags_str.upper()
            if 'SERIES A' in tags_upper:
                investment_stage = 'Series A'
            elif 'SERIES B' in tags_upper:
                investment_stage = 'Series B'
            elif 'SERIES C' in tags_upper:
                investment_stage = 'Series C+'
        
        # Investor aus Detail-Content
        investor_name = item.get('investors')
        
        # Tech Keywords und Sub-Industry aus Detail-Scraping (V6: MULTI-KEYWORD!)
        tech_keywords = item.get('tech_keywords')
        sub_industry = item.get('sub_industry')
        
        # V6: Publication Date and Article Text
        publication_date = item.get('publication_date') or item.get('date')  # NEW: Use extracted date first
        article_text = item.get('content')
        
        # NEW: Use extracted year if available, fallback to date parsing
        if item.get('pub_year'):
            year = item.get('pub_year')
        
        # NEW: Use extracted city, canton, founded_year, employees, website
        city = item.get('city')
        canton = item.get('canton')
        founded_year = item.get('founded_year')
        employees = item.get('employees')
        website = item.get('website')
        
        mapped_data.append({
            'Startup_Name': startup_name,
            'Industry': industry,
            'Sub_Industry': sub_industry or None,
            'Business_Model_Type': business_model,
            'Tech_Keywords': tech_keywords or None,
            'Publication_Date': publication_date or None,  # NEW in V6
            'Article_Text': article_text or None,  # NEW in V6
            'Year': year,
            'Funding_Amount': funding_amount or None,
            'Funding_Round': funding_round,
            'Investment_Stage': investment_stage,
            'Investor_Names': investor_name or None,
            'Location': 'Switzerland',
            'City': city or None,  # IMPROVED: Now extracted from article
            'Canton': canton or None,  # IMPROVED: Now extracted from article
            'Founded_Year': founded_year or None,  # IMPROVED: Now extracted from article
            'Employees': employees or None,  # IMPROVED: Now extracted from article
            'Website': website or None  # IMPROVED: Now extracted from article
        })
    
    df = pd.DataFrame(mapped_data)
    
    # V6: Updated Schema (18 Felder - added Publication_Date and Article_Text)
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Publication_Date', 'Article_Text',  # NEW in V6
        'Year', 'Funding_Amount', 'Funding_Round',
        'Investment_Stage', 'Investor_Names', 'Location', 'City',
        'Canton', 'Founded_Year', 'Employees', 'Website'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    df = df[required_columns]
    
    return df


def main():
    """Haupt-Scraping-Logik."""
    driver = None
    
    try:
        driver = setup_driver()
        
        print("\n" + "="*60)
        print("STARTUPTICKER.CH SCRAPER V6 (MULTI-KEYWORD)")
        print("="*60)
        print("NEW: Returns TOP 5 keywords per startup!")
        print("NEW: 80+ keyword categories (added 22 from friend's list)")
        print("NEW: Publication_Date and Article_Text fields")
        print(f"FILTER: Only startups from {MIN_YEAR} onwards")
        print("="*60)
        
        # PHASE 1: News-Übersicht
        print("\n🔍 PHASE 1: Sammle News-Übersicht...")
        news_items = scrape_news_overview(driver, max_articles=MAX_ARTICLES)
        
        if not news_items:
            print("⚠ Keine News-Items")
            return
        
        print(f"✓ {len(news_items)} News-Items gesammelt (Limit: {MAX_ARTICLES})")
        
        # PHASE 2: Detail-Scraping (mit Title-Fallback!)
        print(f"\n📄 PHASE 2: Scrape {len(news_items)} Detail-Seiten...")
        for i, item in enumerate(news_items, 1):
            if i % 100 == 0 or i == 1 or i == len(news_items):
                print(f"  Fortschritt: {i}/{len(news_items)}...")
            
            try:
                # WICHTIG: Übergebe title für Fallback!
                details = scrape_article_detail(driver, item['url'], item.get('tags', ''), item['title'])
                item['investors'] = details.get('investors')
                item['funding_from_content'] = details.get('funding_from_content')
                item['tech_keywords'] = details.get('tech_keywords')
                item['sub_industry'] = details.get('sub_industry')
                item['content'] = details.get('content')  # ✅ FIXED: Store article content!
                # NEW: Store additional extracted fields
                item['city'] = details.get('city')
                item['canton'] = details.get('canton')
                item['founded_year'] = details.get('founded_year')
                item['employees'] = details.get('employees')
                item['website'] = details.get('website')
                item['publication_date'] = details.get('publication_date')
                item['pub_year'] = details.get('pub_year')
            except Exception as e:
                if i % 100 == 0:
                    print(f"  ⚠️ Fehler bei Artikel {i}: {str(e)[:50]}")
                pass
            
            time.sleep(0.3)  # Rate limiting
        
        print(f"✓ Detail-Scraping abgeschlossen")
        
        # PHASE 3: Mapping
        print("\n🔄 PHASE 3: Mappe zu Schema...")
        mapped_df = map_to_schema(news_items)
        
        output_path = './data/startupticker_startups_v6_TEST.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Gespeichert: {output_path}")
        print(f"  Anzahl Zeilen: {len(mapped_df)}")
        print(f"  Anzahl Spalten: {len(mapped_df.columns)}")
        
        # ZUSAMMENFASSUNG
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG V6 (MULTI-KEYWORD)")
        print("="*60)
        print(f"Anzahl Startups: {len(mapped_df)}")
        
        if len(mapped_df) > 0:
            print(f"\nVollständigkeit:")
            for col in ['Startup_Name', 'Industry', 'Tech_Keywords', 'Sub_Industry', 'Publication_Date', 'Article_Text', 
                       'Year', 'Funding_Amount', 'Investor_Names', 'City', 'Canton', 'Founded_Year', 'Employees', 'Website']:
                non_null = mapped_df[col].notna().sum()
                pct = (non_null / len(mapped_df) * 100)
                print(f"  {col}: {pct:.1f}%")
            
            print(f"\nTop 10 Startups mit MULTI-Keywords:")
            keyword_df = mapped_df[mapped_df['Tech_Keywords'].notna()]
            if len(keyword_df) > 0:
                print(keyword_df[['Startup_Name', 'Tech_Keywords', 'Sub_Industry', 'Publication_Date']].head(10).to_string())
            
            # Article Text Statistics
            if mapped_df['Article_Text'].notna().sum() > 0:
                print(f"\n📝 Article Text Statistics:")
                article_lengths = mapped_df[mapped_df['Article_Text'].notna()]['Article_Text'].str.len()
                print(f"  Articles with text: {len(article_lengths)}/{len(mapped_df)} ({len(article_lengths)/len(mapped_df)*100:.1f}%)")
                print(f"  Average length: {article_lengths.mean():.0f} characters")
                print(f"  Min: {article_lengths.min()}, Max: {article_lengths.max()}")
            
            if mapped_df['Year'].notna().sum() > 0:
                print(f"\nJahresverteilung:")
                year_counts = mapped_df['Year'].value_counts().sort_index(ascending=False)
                for year, count in year_counts.items():
                    if pd.notna(year):
                        print(f"  {int(year)}: {count} Startups")
            
            if mapped_df['Industry'].notna().sum() > 0:
                print(f"\nIndustry-Verteilung:")
                ind_counts = mapped_df['Industry'].value_counts()
                for ind, count in ind_counts.items():
                    print(f"  {ind}: {count} Startups")
            
            # NEU: Keyword-Statistik
            if mapped_df['Tech_Keywords'].notna().sum() > 0:
                print(f"\n🔑 Tech Keywords Häufigkeit:")
                all_keywords = []
                for kw_str in mapped_df['Tech_Keywords'].dropna():
                    keywords = [k.strip() for k in str(kw_str).split(',')]
                    all_keywords.extend(keywords)
                
                from collections import Counter
                keyword_counts = Counter(all_keywords)
                for kw, count in keyword_counts.most_common(15):
                    print(f"  {kw}: {count} Startups")
                
                # Multi-Keyword Statistics (ENHANCED V6)
                print(f"\n📊 Multi-Keyword Statistics:")
                multi_kw_df = mapped_df[mapped_df['Tech_Keywords'].notna()]
                if len(multi_kw_df) > 0:
                    multi_counts = multi_kw_df['Tech_Keywords'].str.count(',') + 1
                    print(f"  Startups with keywords: {len(multi_kw_df)}/{len(mapped_df)} ({len(multi_kw_df)/len(mapped_df)*100:.1f}%)")
                    print(f"  Startups with 2+ keywords: {(multi_counts >= 2).sum()} ({(multi_counts >= 2).sum()/len(multi_kw_df)*100:.1f}%)")
                    print(f"  Startups with 3+ keywords: {(multi_counts >= 3).sum()} ({(multi_counts >= 3).sum()/len(multi_kw_df)*100:.1f}%)")
                    print(f"  Startups with 4+ keywords: {(multi_counts >= 4).sum()} ({(multi_counts >= 4).sum()/len(multi_kw_df)*100:.1f}%)")
                    print(f"  Startups with 5 keywords: {(multi_counts >= 5).sum()} ({(multi_counts >= 5).sum()/len(multi_kw_df)*100:.1f}%)")
                    print(f"  Average keywords per startup: {multi_counts.mean():.2f}")
                    print(f"  Max keywords in one startup: {multi_counts.max()}")
        
        print("\n✓ ERFOLGREICH ABGESCHLOSSEN")
        
    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("WebDriver geschlossen")


if __name__ == "__main__":
    main()
