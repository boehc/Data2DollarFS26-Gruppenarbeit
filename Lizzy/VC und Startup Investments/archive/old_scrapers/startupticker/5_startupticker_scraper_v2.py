"""
Startupticker.ch News Scraper V3 (Optimiert)
Scraped Schweizer Startup-News mit Detail-Seiten für Investor-Extraktion.
Limit: 1000 Artikel total (effizient, ohne alle Seiten zu laden)
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

# LIMIT für Artikel-Scraping (total)
MAX_ARTICLES = 1000


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
    """Extrahiert Company-Namen aus Artikel-Titel."""
    words = title.split()
    for word in words:
        if word and word[0].isupper() and len(word) >= 3:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word:
                return clean_word
    return None


def extract_funding_info(text):
    """Extrahiert Funding-Informationen aus Text (verbessert)."""
    if not text:
        return None, None
    
    # Erweiterte Patterns
    patterns = [
        # "CHF 5.2 million", "$10M", "€3.5M"
        r'(USD|CHF|EUR|€|\$)\s*(\d+[\.,]?\d*)\s*(million|mio|m\b)',
        r'(\d+[\.,]?\d*)\s*(million|mio|m\b)\s*(USD|CHF|EUR|€|\$)',
        # "5 million francs", "10 million dollars"
        r'(\d+[\.,]?\d*)\s*million\s*(francs?|dollars?|euros?)',
        # "raises $5M", "secures CHF 10M"
        r'(?:raises?|secures?|receives?)\s+(USD|CHF|EUR|\$)\s*(\d+[\.,]?\d*)\s*([MK]|million)?',
        # Deutsch: "erhält CHF 5 Millionen"
        r'(?:erhält|bekommt|sichert)\s+(CHF|USD|EUR)\s*(\d+[\.,]?\d*)\s*Million',
        # "undisclosed amount", "Millionenbetrag"
        r'undisclosed\s+(?:amount|sum|round)',
        r'Millionenbetrag',
        # K-Format: "CHF 150K", "$500K"
        r'(USD|CHF|EUR|\$)\s*(\d+[\.,]?\d*)\s*K\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                if 'undisclosed' in match.group(0).lower() or 'Millionenbetrag' in match.group(0):
                    return 'undisclosed', 'Funding Round'
                
                amount = None
                currency = None
                unit = 'M'  # Default Million
                
                groups = match.groups()
                for g in groups:
                    if g and re.match(r'\d+[\.,]?\d*', g):
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
                
                if amount:
                    full_amount = f"{amount}{unit} {currency}" if currency else f"{amount}{unit}"
                    return full_amount, 'Seed/Series A'
            except Exception as e:
                print(f"   Funding extraction error: {e}")
                pass
    
    return None, None


def extract_investors(text):
    """Extrahiert Investor-Namen aus Artikel-Text (verbessert)."""
    if not text:
        return None
    
    investors = []
    
    # Pattern 1: "led by X" / "angeführt von X"
    led_patterns = [
        r'led by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s|with|\n)',
        r'angeführt von ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
        r'headed by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,)',
    ]
    
    for pattern in led_patterns:
        match = re.search(pattern, text)
        if match:
            inv = match.group(1).strip()
            if len(inv) > 2 and len(inv) < 60:  # Plausibilitätscheck
                investors.append(inv)
    
    # Pattern 2: "from X" / "von X"
    from_patterns = [
        r'from ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s|\n)',
        r'von ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
    ]
    
    for pattern in from_patterns:
        match = re.search(pattern, text)
        if match:
            inv = match.group(1).strip()
            if inv not in investors and len(inv) > 2 and len(inv) < 60:
                investors.append(inv)
    
    # Pattern 3: "investors include X, Y" / "with participation from X"
    list_patterns = [
        r'investors?\s+(?:include|are)\s+([A-Z][A-Za-z\s,&.-]+?)(?:\.|participated|\n)',
        r'with participation from ([A-Z][A-Za-z\s,&.-]+?)(?:\.|,|\n)',
        r'backed by ([A-Z][A-Za-z\s,&.-]+?)(?:\.|,|\n)',
        r'supported by ([A-Z][A-Za-z\s,&.-]+?)(?:\.|,|\n)',
    ]
    
    for pattern in list_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            inv_list = match.group(1)
            # Split by comma or "and"
            parts = re.split(r',|\sand\s', inv_list)
            for part in parts:
                inv = part.strip()
                if inv and inv not in investors and len(inv) > 2 and len(inv) < 60:
                    investors.append(inv)
    
    # Pattern 4: Known VC names (case-insensitive search)
    known_vcs = [
        'Founderful', 'Redalpine', 'Swisscom Ventures', 'Verve Ventures',
        'Venturelab', 'btov Partners', 'Zürcher Kantonalbank', 'ZKB',
        'Creathor Ventures', 'Investiere', 'High-Tech Gründerfonds',
        'VI Partners', 'Crypto Valley Venture Capital', 'CVVC'
    ]
    
    for vc in known_vcs:
        if vc.lower() in text.lower() and vc not in investors:
            investors.append(vc)
    
    return ', '.join(investors[:5]) if investors else None  # Max 5


def extract_tech_keywords(text, tags=[]):
    """Extrahiert Tech-Keywords aus Text und Tags."""
    if not text:
        text = ""
    
    text_upper = text.upper()
    
    # Tech-Keyword Dictionary
    tech_keywords = {
        'AI': ['ARTIFICIAL INTELLIGENCE', 'MACHINE LEARNING', 'DEEP LEARNING', 'NEURAL NETWORK', ' AI ', 'AI-'],
        'SaaS': ['SAAS', 'SOFTWARE AS A SERVICE', 'CLOUD SOFTWARE', 'PLATFORM'],
        'Biotech': ['BIOTECH', 'BIOTECHNOLOGY', 'GENOMICS', 'RNA', 'DNA', 'GENE', 'CELL THERAPY', 'PROTEIN'],
        'Fintech': ['FINTECH', 'PAYMENT', 'BANKING', 'CRYPTO', 'BLOCKCHAIN', 'DIGITAL WALLET', 'FINANCE TECHNOLOGY'],
        'E-Commerce': ['E-COMMERCE', 'ECOMMERCE', 'ONLINE SHOP', 'MARKETPLACE', 'ONLINE RETAIL'],
        'IoT': ['IOT', 'INTERNET OF THINGS', 'SMART DEVICE', 'CONNECTED DEVICES'],
        'Mobility': ['MOBILITY', 'AUTONOMOUS', 'ELECTRIC VEHICLE', 'TRANSPORTATION', 'AUTOMOTIVE'],
        'Healthtech': ['HEALTHTECH', 'DIGITAL HEALTH', 'MEDICAL DEVICE', 'PATIENT', 'CLINICAL', 'DIAGNOSIS'],
        'Cleantech': ['CLEANTECH', 'CLEAN ENERGY', 'RENEWABLE', 'SOLAR', 'CARBON', 'SUSTAINABILITY', 'CLIMATE TECH'],
        'Robotics': ['ROBOT', 'ROBOTICS', 'AUTOMATION', 'DRONE'],
        'AR/VR': [' AR ', 'AUGMENTED REALITY', 'VIRTUAL REALITY', ' VR ', 'MIXED REALITY'],
        'Cloud': ['CLOUD COMPUTING', 'CLOUD INFRASTRUCTURE', 'AWS', 'AZURE'],
        'Cybersecurity': ['CYBERSECURITY', 'SECURITY', 'ENCRYPTION', 'DATA PROTECTION', 'PRIVACY'],
        'Analytics': ['DATA ANALYTICS', 'BIG DATA', 'BUSINESS INTELLIGENCE', 'INSIGHTS'],
        'EdTech': ['EDTECH', 'EDUCATION TECHNOLOGY', 'LEARNING PLATFORM', 'TRAINING SOFTWARE'],
        'PropTech': ['PROPTECH', 'REAL ESTATE', 'PROPERTY TECHNOLOGY'],
        'AgTech': ['AGTECH', 'AGRICULTURE', 'FARMING TECHNOLOGY', 'FOOD TECH'],
        'Manufacturing': ['MANUFACTURING', 'PRODUCTION', 'INDUSTRIAL AUTOMATION'],
        'Logistics': ['LOGISTICS', 'SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY']
    }
    
    found_keywords = set()
    
    # Aus Text
    for keyword, patterns in tech_keywords.items():
        if any(pattern in text_upper for pattern in patterns):
            found_keywords.add(keyword)
    
    # Aus Tags
    for tag in tags:
        tag_upper = tag.upper()
        for keyword, patterns in tech_keywords.items():
            if any(pattern in tag_upper for pattern in patterns):
                found_keywords.add(keyword)
    
    return ', '.join(sorted(found_keywords)) if found_keywords else None


def extract_sub_industry(text, tags=[]):
    """Leitet Sub-Industry aus Text/Tags ab."""
    if not text:
        return None
    
    text_upper = text.upper()
    
    sub_industries = {
        'SOFTWARE & PLATFORMS': ['SOFTWARE', 'PLATFORM', 'SAAS', 'APPLICATION'],
        'MEDICAL DEVICES': ['MEDICAL DEVICE', 'DIAGNOSTICS', 'IMPLANT', 'INSTRUMENT'],
        'DRUG DISCOVERY': ['DRUG', 'PHARMACEUTICAL', 'THERAPY', 'TREATMENT'],
        'FINANCIAL SERVICES': ['BANKING', 'PAYMENT', 'INSURANCE', 'LENDING'],
        'E-COMMERCE': ['ONLINE SHOP', 'E-COMMERCE', 'MARKETPLACE'],
        'MOBILITY SERVICES': ['RIDESHARE', 'CAR SHARING', 'TRANSPORTATION SERVICE'],
        'MANUFACTURING': ['PRODUCTION', 'FACTORY', 'MANUFACTURING'],
        'LOGISTICS': ['SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY', 'SHIPPING']
    }
    
    for sub_ind, patterns in sub_industries.items():
        if any(pattern in text_upper for pattern in patterns):
            return sub_ind
    
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
            
            # Scrolle für Lazy Loading
            for scroll in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            items = driver.find_elements(By.CSS_SELECTOR, 'div.item.news')
            new_items_found = 0
            
            for item in items:
                # Stop wenn Limit erreicht
                if len(news_items) >= max_articles:
                    print(f"✅ Limit von {max_articles} Artikeln erreicht!")
                    break
                    
                try:
                    title_el = item.find_element(By.CSS_SELECTOR, 'h2, h3, a')
                    title = title_el.text.strip()
                    
                    link_el = item.find_element(By.TAG_NAME, 'a')
                    url = link_el.get_attribute('href')
                    
                    if url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    new_items_found += 1
                    
                    try:
                        date_el = item.find_element(By.CSS_SELECTOR, '[class*="date"], time')
                        date = date_el.text.strip()
                    except:
                        date = None
                    
                    tags = []
                    try:
                        tag_elements = item.find_elements(By.CSS_SELECTOR, '[class*="tag"], [class*="label"]')
                        tags = [t.text.strip() for t in tag_elements if t.text.strip()]
                    except:
                        pass
                    
                    news_items.append({
                        'title': title,
                        'url': url,
                        'date': date,
                        'tags': ', '.join(tags) if tags else None
                    })
                    
                except:
                    continue
            
            if new_items_found == 0:
                no_new_items_count += 1
                if no_new_items_count >= 2:
                    break
            else:
                no_new_items_count = 0
            
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


def scrape_article_detail(driver, url, tags_str=''):
    """Scraped Details aus einem Artikel."""
    try:
        driver.get(url)
        time.sleep(1.5)
        
        content = None
        try:
            content_selectors = [
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
        
        investors = extract_investors(content) if content else None
        funding_from_content, _ = extract_funding_info(content) if content else (None, None)
        
        # NEU: Extrahiere Tech Keywords und Sub-Industry
        tags_list = tags_str.split(', ') if tags_str else []
        tech_keywords = extract_tech_keywords(content, tags_list)
        sub_industry = extract_sub_industry(content, tags_list)
        
        return {
            'content': content,
            'investors': investors,
            'funding_from_content': funding_from_content,
            'tech_keywords': tech_keywords,
            'sub_industry': sub_industry
        }
        
    except Exception as e:
        return {
            'content': None,
            'investors': None,
            'funding_from_content': None
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
        
        # FILTER: Nur 2020-2026
        if year and year < 2020:
            continue
        
        # Funding: Priorität Content > Titel
        funding_amount = item.get('funding_from_content') or extract_funding_info(item['title'])[0]
        funding_round = extract_funding_info(item['title'])[1]
        
        # Industry aus Tags + Titel
        tags_str = item.get('tags', '') or ''
        title_lower = item['title'].lower()
        combined_text = (tags_str + ' ' + title_lower).lower()
        
        industry = None
        if any(kw in combined_text for kw in ['fintech', 'financial', 'payment', 'banking']):
            industry = 'FINTECH'
        elif any(kw in combined_text for kw in ['health', 'medtech', 'biotech', 'pharma', 'medical']):
            industry = 'HEALTHCARE'
        elif any(kw in combined_text for kw in ['ai', 'software', 'saas', 'platform', 'data', 'analytics']):
            industry = 'B2B'
        elif any(kw in combined_text for kw in ['climate', 'energy', 'sustainability', 'cleantech', 'industrial']):
            industry = 'INDUSTRIALS'
        elif any(kw in combined_text for kw in ['food', 'agriculture', 'agritech', 'farming']):
            industry = 'CONSUMER'
        elif any(kw in combined_text for kw in ['ecommerce', 'retail', 'consumer', 'marketplace']):
            industry = 'CONSUMER'
        elif any(kw in combined_text for kw in ['education', 'edtech', 'learning']):
            industry = 'EDUCATION'
        else:
            industry = 'B2B'
        
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
        
        # Tech Keywords und Sub-Industry aus Detail-Scraping
        tech_keywords = item.get('tech_keywords')
        sub_industry = item.get('sub_industry')
        
        mapped_data.append({
            'Startup_Name': startup_name,
            'Industry': industry,
            'Sub_Industry': sub_industry,  # NEU: aus Detail-Scraping
            'Business_Model_Type': None,
            'Tech_Keywords': tech_keywords,  # NEU: strukturierte Keywords statt nur Tags
            'Year': year,
            'Funding_Amount': funding_amount,
            'Funding_Round': funding_round,
            'Investor_Type': 'VC Fund',
            'Investor_Name': investor_name,
            'Country': 'Switzerland',
            'Founding_Year': year,
            'Investment_Stage': investment_stage,
            'Valuation': None,
            'Exit_Type': None,
            'Startup_Stage': 'Active'
        })
    
    df = pd.DataFrame(mapped_data)
    
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    return df[required_columns]


def main():
    """Hauptfunktion."""
    print("="*60)
    print("STARTUPTICKER.CH SCRAPER V2")
    print("="*60)
    
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        driver = setup_driver()
        
        # PHASE 1: News Übersicht
        print("\n🔍 PHASE 1: Sammle News-Übersicht...")
        news_items = scrape_news_overview(driver, max_pages=50)
        
        if not news_items:
            print("⚠ Keine News-Items")
            return
        
        print(f"✓ {len(news_items)} News-Items gesammelt (Limit: {MAX_ARTICLES})")
        
        # PHASE 2: Detail-Scraping (alle gesammelten Items)
        print(f"\n📄 PHASE 2: Scrape {len(news_items)} Detail-Seiten...")
        for i, item in enumerate(news_items, 1):
            if i % 50 == 0 or i == 1:
                print(f"  Fortschritt: {i}/{len(news_items)}...")
            
            try:
                details = scrape_article_detail(driver, item['url'], item.get('tags', ''))
                item['investors'] = details.get('investors')
                item['funding_from_content'] = details.get('funding_from_content')
                item['tech_keywords'] = details.get('tech_keywords')  # NEU
                item['sub_industry'] = details.get('sub_industry')  # NEU
            except:
                pass
            
            time.sleep(0.3)  # Rate limiting
        
        print(f"✓ Detail-Scraping abgeschlossen")
        
        # PHASE 3: Mapping
        print("\n🔄 PHASE 3: Mappe zu Schema...")
        mapped_df = map_to_schema(news_items)
        
        output_path = './data/startupticker_startups.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Gespeichert: {output_path}")
        
        # ZUSAMMENFASSUNG
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Anzahl Startups: {len(mapped_df)}")
        
        if len(mapped_df) > 0:
            print(f"\nVollständigkeit:")
            for col in ['Startup_Name', 'Industry', 'Year', 'Funding_Amount', 'Investor_Name', 'Investment_Stage']:
                non_null = mapped_df[col].notna().sum()
                pct = (non_null / len(mapped_df) * 100)
                print(f"  {col}: {pct:.1f}%")
            
            print(f"\nTop 10 Startups:")
            print(mapped_df[['Startup_Name', 'Year', 'Funding_Amount', 'Investment_Stage', 'Investor_Name']].head(10).to_string())
            
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
            
            if mapped_df['Investment_Stage'].notna().sum() > 0:
                print(f"\nInvestment Stage-Verteilung:")
                stage_counts = mapped_df['Investment_Stage'].value_counts()
                for stage, count in stage_counts.items():
                    print(f"  {stage}: {count} Startups")
        
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
