"""
Startupticker.ch News Scraper V2
Scraped Schweizer Startup-News mit Detail-Seiten für Investor-Extraktion.
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

# LIMIT für Artikel-Detail-Scraping
MAX_DETAIL_ARTICLES = 400


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
    Beispiele:
    - "Cohaga sammelt Millionenbetrag" → "Cohaga"
    - "Covalo sichert sich Finanzierung" → "Covalo"
    - "Lobby raises USD 2.2 million" → "Lobby"
    """
    # Erstes Wort mit Großbuchstaben ist oft der Company-Name
    words = title.split()
    for word in words:
        # Company-Namen sind meist kapitalisiert und 3+ Zeichen
        if word[0].isupper() and len(word) >= 3:
            # Entferne Satzzeichen
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word:
                return clean_word
    return None


def extract_funding_info(text):
    """
    Extrahiert Funding-Informationen aus Text.
    Patterns: "USD 2.2 million", "CHF 5 Millionen", "€3M", etc.
    """
    if not text:
        return None, None
    
    # Patterns für Funding-Amounts
    patterns = [
        r'(USD|CHF|EUR|€|\$)\s*(\d+\.?\d*)\s*(million|mio|m\b)',
        r'(\d+\.?\d*)\s*(million|mio|m\b)\s*(USD|CHF|EUR|€|\$)',
        r'Millionenbetrag',
        r'(\d+\.?\d*)\s*Millionen',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                if 'Millionenbetrag' in match.group(0):
                    return 'undisclosed', 'Million'
                
                # Extrahiere Betrag und Währung
                amount = None
                currency = None
                
                groups = match.groups()
                for g in groups:
                    if g and re.match(r'\d+\.?\d*', g):
                        amount = float(g)
                    elif g and g.upper() in ['USD', 'CHF', 'EUR', '$', '€']:
                        currency = g.upper().replace('$', 'USD').replace('€', 'EUR')
                
                if amount:
                    # Konvertiere zu voller Zahl (Million)
                    full_amount = f"{amount}M {currency}" if currency else f"{amount}M"
                    return full_amount, 'Seed/Series A'
            except:
                pass
    
    return None, None


def extract_investors(text):
    """
    Extrahiert Investor-Namen aus Artikel-Text.
    Patterns: "led by X", "from X and Y", "investors include X"
    """
    if not text:
        return None
    
    investors = []
    
    # Pattern 1: "led by X" / "angeführt von X"
    led_patterns = [
        r'led by ([A-Z][A-Za-z\s&,]+?)(?:\.|,|\sand\s)',
        r'angeführt von ([A-Z][A-Za-z\s&,]+?)(?:\.|,)',
        r'führte ([A-Z][A-Za-z\s&,]+?)(?:\.|,)',
    ]
    
    for pattern in led_patterns:
        match = re.search(pattern, text)
        if match:
            investors.append(match.group(1).strip())
    
    # Pattern 2: "from X" / "von X"
    from_patterns = [
        r'from ([A-Z][A-Za-z\s&,]+?)(?:\.|,|\sand\s)',
        r'von ([A-Z][A-Za-z\s&,]+?)(?:\.|,)',
    ]
    
    for pattern in from_patterns:
        match = re.search(pattern, text)
        if match:
            inv = match.group(1).strip()
            if inv not in investors:
                investors.append(inv)
    
    # Pattern 3: Liste "X, Y, and Z"
    list_pattern = r'investors?\s+(?:include|are)\s+([A-Z][A-Za-z\s,&]+?)(?:\.|participated)'
    match = re.search(list_pattern, text, re.IGNORECASE)
    if match:
        inv_list = match.group(1)
        # Split by "and" oder ","
        parts = re.split(r',|\sand\s', inv_list)
        for part in parts:
            inv = part.strip()
            if inv and inv not in investors:
                investors.append(inv)
    
    if investors:
        return ', '.join(investors[:3])  # Max 3 Investoren
    return None


def scrape_article_detail(driver, url):
    """
    Scraped Details aus einem einzelnen Artikel.
    Extrahiert: Investor-Namen, detaillierte Funding-Info, Industry-Keywords
    """
    try:
        driver.get(url)
        time.sleep(2)
        
        # Artikel-Content
        content = None
        try:
            content_el = driver.find_element(By.CSS_SELECTOR, 'article, div.content, div[class*="text"]')
            content = content_el.text
        except:
            pass
        
        # Extrahiere Investoren
        investors = extract_investors(content) if content else None
        
        # Bessere Funding-Info aus Content
        funding_amount, funding_round = extract_funding_info(content) if content else (None, None)
        
        return {
            'content': content,
            'investors': investors,
            'funding_amount': funding_amount,
            'funding_round': funding_round
        }
    except Exception as e:
        return None


def extract_year_from_date(date_str):
    """Extrahiert Jahr aus Datum-String (z.B. "02.04.2026" → 2026)."""
    if not date_str:
        return None
    year_match = re.search(r'20\d{2}', date_str)
    if year_match:
        return int(year_match.group(0))
    return None


def scrape_news_overview(driver, max_pages=50):
    """
    Scraped News-Übersicht mit Pagination/Scrolling.
    
    Args:
        driver: Selenium WebDriver
        max_pages: Maximale Anzahl Seiten zu scrapen (erhöht auf 50 für 2020-2026)
        
    Returns:
        list: Liste von News-Item-Dicts
    """
    base_url = 'https://www.startupticker.ch/en/news'
    news_items = []
    seen_urls = set()
    
    print(f"Öffne {base_url}")
    driver.get(base_url)
    
    print("Warte auf Seiteninhalt...")
    wait = WebDriverWait(driver, 20)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item.news')))
        print("✓ News-Items gefunden")
        time.sleep(3)
        
        page = 1
        no_new_items_count = 0
        
        while page <= max_pages:
            print(f"\n📄 Scrape Seite {page}...")
            
            # Scrolle um Lazy Loading zu triggern
            for scroll in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Hole alle News-Items
            items = driver.find_elements(By.CSS_SELECTOR, 'div.item.news')
            print(f"  Gefundene Items: {len(items)}")
            
            new_items_found = 0
            
            for item in items:
                try:
                    # Titel
                    title_el = item.find_element(By.CSS_SELECTOR, 'h2, h3, a')
                    title = title_el.text.strip()
                    
                    # URL
                    link_el = item.find_element(By.TAG_NAME, 'a')
                    url = link_el.get_attribute('href')
                    
                    # Skip wenn schon gesehen
                    if url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    new_items_found += 1
                    
                    # Datum
                    try:
                        date_el = item.find_element(By.CSS_SELECTOR, '[class*="date"], time')
                        date = date_el.text.strip()
                    except:
                        date = None
                    
                    # Tags/Kategorien (z.B. "FINANCING LAUNCH")
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
                        'tags': ', '.join(tags) if tags else None,
                        'detail_scraped': False  # Markierung für Detail-Scraping
                    })
                    
                except Exception as e:
                    continue
            
            print(f"  Neue Items: {new_items_found}")
            
            if new_items_found == 0:
                no_new_items_count += 1
                if no_new_items_count >= 2:
                    print("  Keine neuen Items mehr gefunden")
                    break
            else:
                no_new_items_count = 0
            
            # Versuche "Next" Button oder mehr laden
            try:
                # Suche nach Pagination/Load-More Button
                next_buttons = driver.find_elements(By.CSS_SELECTOR, 
                    'a.next, button[class*="next"], a[class*="more"], button[class*="load"]')
                
                if next_buttons:
                    print("  Klicke auf 'Next/Load More'...")
                    next_buttons[0].click()
                    time.sleep(3)
                    page += 1
                else:
                    # Kein Button gefunden, Ende
                    print("  Kein Pagination-Button gefunden")
                    break
            except:
                print("  Pagination nicht möglich")
                break
        
        print(f"\n✓ {len(news_items)} News-Items gesammelt")
        
        # JETZT: Scrape Details von jedem Artikel (für Investoren!)
        print(f"\n📊 Scrape Artikel-Details für Investor-Info...")
        for i, item in enumerate(news_items):
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{len(news_items)} Artikel...")
            
            detail = scrape_article_detail(driver, item['url'])
            if detail:
                item['investors'] = detail.get('investors')
                item['content'] = detail.get('content')
                # Überschreibe Funding-Info mit präziseren Daten aus Content
                if detail.get('funding_amount'):
                    item['funding_amount_detail'] = detail.get('funding_amount')
                item['detail_scraped'] = True
            
            time.sleep(1)  # Rate limiting
        
        print(f"✓ Details gescraped")
        return news_items
        
    except Exception as e:
        print(f"❌ Fehler beim Scraping: {e}")
        import traceback
        traceback.print_exc()
        return news_items


def map_to_schema(news_items):
    """
    Mappt News-Daten zu unserem 16-Felder Schema.
    
    Extrahierte Felder aus News:
    - Startup_Name: Aus Titel
    - Industry: Aus Tags/Kategorien
    - Year: Aus Datum
    - Funding_Amount: Aus Titel/Text
    - Country: Switzerland (alle sind CH-Startups)
    - Investment_Stage: Aus Tags oder Text
    """
    if not news_items:
        print("⚠ Keine Daten zum Mappen vorhanden")
        return pd.DataFrame()
    
    mapped_data = []
    
    for item in news_items:
        # Company-Name aus Titel extrahieren
        startup_name = extract_company_from_title(item['title'])
        
        if not startup_name:
            continue  # Skip wenn kein Company-Name gefunden
        
        # Jahr aus Datum
        year = extract_year_from_date(item['date'])
        
        # FILTER: Nur 2020-2026
        if year and year < 2020:
            continue
        
        # Funding-Info aus Titel extrahieren
        funding_amount, funding_round = extract_funding_info(item['title'])
        
        # Bessere Funding-Info aus Artikel-Content (falls vorhanden)
        if item.get('funding_amount_detail'):
            funding_amount = item['funding_amount_detail']
        
        # Investor-Name aus Detail-Scraping
        investor_name = item.get('investors')
        
        # Industry aus Tags ableiten (verbesserte Logik)
        industry = None
        tags_str = item.get('tags', '') or ''
        title_lower = item['title'].lower()
        combined_text = (tags_str + ' ' + title_lower).lower()
        
        if 'fintech' in combined_text or 'financial' in combined_text or 'payment' in combined_text or 'banking' in combined_text:
            industry = 'FINTECH'
        elif 'health' in combined_text or 'medtech' in combined_text or 'biotech' in combined_text or 'pharma' in combined_text:
            industry = 'HEALTHCARE'
        elif 'ai' in combined_text or 'software' in combined_text or 'saas' in combined_text or 'platform' in combined_text:
            industry = 'B2B'
        elif 'climate' in combined_text or 'energy' in combined_text or 'sustainability' in combined_text or 'cleantech' in combined_text:
            industry = 'INDUSTRIALS'
        elif 'food' in combined_text or 'agriculture' in combined_text or 'agritech' in combined_text:
            industry = 'CONSUMER'
        elif 'ecommerce' in combined_text or 'retail' in combined_text or 'consumer' in combined_text:
            industry = 'CONSUMER'
        elif 'education' in combined_text or 'edtech' in combined_text:
            industry = 'EDUCATION'
        else:
            industry = 'B2B'  # Default für unklare Fälle
        
        # Investment Stage aus Funding Amount und Tags ableiten (nicht nur Seed!)
        investment_stage = None
        if funding_amount:
            # Versuche Betrag zu parsen
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
            else:
                investment_stage = 'Seed'  # undisclosed
        
        # Tags-basierte Stage-Erkennung
        if tags_str:
            tags_upper = tags_str.upper()
            if 'SERIES A' in tags_upper or 'SERIES-A' in tags_upper:
                investment_stage = 'Series A'
            elif 'SERIES B' in tags_upper or 'SERIES-B' in tags_upper:
                investment_stage = 'Series B'
            elif 'SERIES C' in tags_upper or 'SERIES-C' in tags_upper:
                investment_stage = 'Series C+'
            elif 'SEED' in tags_upper and not investment_stage:
                investment_stage = 'Seed'
        
        # Fallback
        if not investment_stage:
            investment_stage = 'Early Stage'
        
        
        mapped_data.append({
            'Startup_Name': startup_name,
            'Industry': industry,
            'Sub_Industry': None,
            'Business_Model_Type': None,
            'Tech_Keywords': item.get('tags'),
            'Year': year,
            'Funding_Amount': funding_amount,
            'Funding_Round': funding_round,
            'Investor_Type': 'VC Fund',  # Annahme für CH-Startups
            'Investor_Name': investor_name,  # Jetzt aus Artikel extrahiert!
            'Country': 'Switzerland',  # Alle sind CH
            'Founding_Year': year,
            'Investment_Stage': investment_stage,
            'Valuation': None,
            'Exit_Type': None,
            'Startup_Stage': 'Active'
        })
    
    df = pd.DataFrame(mapped_data)
    
    # Spalten in korrekter Reihenfolge
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    df = df[required_columns]
    
    print(f"✓ {len(df)} Zeilen gemappt")
    return df


def main():
    """Hauptfunktion."""
    print("="*60)
    print("STARTUPTICKER.CH SCRAPER - SCHWEIZER STARTUPS")
    print("="*60)
    
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        driver = setup_driver()
        
        # Scrape News (max 50 Seiten für 2020-2026 Daten)
        news_items = scrape_news_overview(driver, max_pages=50)
        
        if not news_items:
            print("⚠ Keine News-Items gescraped - Erstelle leere CSV")
            news_items = []
        
        mapped_df = map_to_schema(news_items)
        
        output_path = './data/startupticker_startups.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Gespeichert: {output_path}")
        
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Anzahl Startups: {len(mapped_df)}")
        
        if len(mapped_df) > 0:
            print(f"\nVollständigkeit:")
            for col in ['Startup_Name', 'Industry', 'Year', 'Funding_Amount', 'Investor_Name']:
                non_null = mapped_df[col].notna().sum()
                pct = (non_null / len(mapped_df) * 100)
                print(f"  {col}: {pct:.1f}%")
            
            print(f"\nTop 5 Startups:")
            print(mapped_df[['Startup_Name', 'Year', 'Funding_Amount']].head())
            
            if mapped_df['Year'].notna().sum() > 0:
                print(f"\nJahresverteilung:")
                year_counts = mapped_df['Year'].value_counts().sort_index(ascending=False)
                for year, count in year_counts.head(5).items():
                    if pd.notna(year):
                        print(f"  {int(year)}: {count} Startups")
        
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
