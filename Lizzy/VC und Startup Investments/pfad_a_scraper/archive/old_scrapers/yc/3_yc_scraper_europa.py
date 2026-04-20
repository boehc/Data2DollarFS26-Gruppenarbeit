"""
Y Combinator Companies Scraper - Europa Fokus
Scraped gezielt europäische Startups von YC (2015-2026).
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


def parse_company_text(text):
    """
    Parsed den Text einer YC Company Card.
    
    Format:
    Zeile 1: NameLocation (z.B. "AirbnbSan Francisco, CA, USA")
    Zeile 2: Description
    Zeile 3: BATCH (z.B. "WINTER 2009")
    Zeile 4: INDUSTRY (z.B. "CONSUMER")
    Zeile 5: SUB_INDUSTRY (z.B. "TRAVEL, LEISURE AND TOURISM")
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    company = {
        'name': None,
        'location': None,
        'city': None,
        'state': None,
        'country': None,
        'description': None,
        'batch': None,
        'industry': None,
        'sub_industry': None,
    }
    
    if len(lines) < 3:
        return company
    
    # Zeile 1: Name + Location
    first_line = lines[0]
    comma_pos = first_line.find(',')
    
    if comma_pos > 0:
        before_comma = first_line[:comma_pos]
        words = re.findall(r'[A-Z][a-z]*', before_comma)
        
        if len(words) >= 2:
            name_end = before_comma.find(words[-1])
            company['name'] = before_comma[:name_end].strip()
            location_str = first_line[name_end:].strip()
        else:
            company['name'] = words[0] if words else before_comma
            location_str = first_line[len(words[0]) if words else 0:].strip()
        
        # Parse Location
        location_parts = [p.strip() for p in location_str.split(',')]
        company['location'] = location_str
        
        if len(location_parts) == 3:  # City, State, Country
            company['city'] = location_parts[0]
            company['state'] = location_parts[1]
            company['country'] = location_parts[2]
        elif len(location_parts) == 2:  # City, Country
            company['city'] = location_parts[0]
            company['country'] = location_parts[1]
        elif len(location_parts) == 1:
            company['country'] = location_parts[0]
    else:
        company['name'] = first_line
    
    # Zeile 2: Description
    if len(lines) > 1:
        company['description'] = lines[1]
    
    # Batch, Industry, Sub-Industry
    batch_pattern = r'^(WINTER|SUMMER)\s+\d{4}$'
    
    for i in range(2, len(lines)):
        line = lines[i]
        if re.match(batch_pattern, line):
            company['batch'] = line
            if i + 1 < len(lines):
                company['industry'] = lines[i + 1]
            if i + 2 < len(lines):
                company['sub_industry'] = lines[i + 2]
            break
    
    return company


def batch_to_year(batch):
    """Konvertiert YC Batch zu Jahr."""
    if not batch:
        return None
    year_match = re.search(r'\d{4}', batch)
    if year_match:
        return int(year_match.group(0))
    return None


def scrape_yc_europe(driver, min_year=2015):
    """
    Scraped europäische YC Companies ab einem bestimmten Jahr.
    
    Args:
        driver: Selenium WebDriver
        min_year: Minimales Jahr (default 2015 für aktuelle Daten)
    """
    # URL mit Europa-Filter
    url = 'https://www.ycombinator.com/companies?regions=Europe'
    
    print(f"Öffne YC Companies - Europa Filter")
    print(f"URL: {url}")
    driver.get(url)
    
    print("Warte auf Seiteninhalt...")
    wait = WebDriverWait(driver, 20)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/companies/"]')))
        print("✓ Company-Links gefunden")
        time.sleep(3)
        
        # Aggressives Scrolling um ALLE europäischen Companies zu laden
        print("Scrolle um alle europäischen Companies zu laden...")
        last_count = 0
        scroll_attempts = 0
        max_scrolls = 40  # Mehr Scrolls für vollständige Daten
        no_change_count = 0
        
        while scroll_attempts < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            current_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/companies/"]')
            current_count = len(current_links)
            
            if current_count == last_count:
                no_change_count += 1
                if no_change_count >= 5:
                    print(f"  Keine neuen Companies mehr (Scroll {scroll_attempts})")
                    break
            else:
                no_change_count = 0
                
            if scroll_attempts % 5 == 0:
                print(f"  Scroll {scroll_attempts}: {current_count} companies")
            
            last_count = current_count
            scroll_attempts += 1
        
        # Finale Company-Links
        company_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/companies/"]')
        print(f"Gefundene Company-Links: {len(company_links)}")
        
        # Parse Companies
        companies = []
        seen_names = set()
        skipped_old = 0
        
        for link in company_links:
            try:
                text_content = link.text
                
                if not text_content or len(text_content) < 10:
                    continue
                
                company = parse_company_text(text_content)
                
                if not company['name']:
                    continue
                    
                if company['name'] in seen_names:
                    continue
                
                # Filtere nach Jahr (nur aktuelle Startups)
                year = batch_to_year(company['batch'])
                if year and year < min_year:
                    skipped_old += 1
                    continue
                
                seen_names.add(company['name'])
                companies.append(company)
                
                if len(companies) % 50 == 0:
                    print(f"  Verarbeitet: {len(companies)} Companies (übersprungen: {skipped_old} zu alt)...")
                    
            except Exception as e:
                continue
        
        print(f"✓ {len(companies)} Companies extrahiert (ab Jahr {min_year})")
        print(f"  Übersprungen: {skipped_old} Companies vor {min_year}")
        return companies
        
    except Exception as e:
        print(f"❌ Fehler beim Scraping: {e}")
        import traceback
        traceback.print_exc()
        return []


def map_to_schema(companies):
    """Mappt YC Company-Daten zu unserem Schema."""
    if not companies:
        print("⚠ Keine Daten zum Mappen vorhanden")
        return pd.DataFrame()
    
    df = pd.DataFrame(companies)
    
    mapped_df = pd.DataFrame()
    
    mapped_df['Startup_Name'] = df['name']
    mapped_df['Industry'] = df['industry']
    mapped_df['Sub_Industry'] = df['sub_industry']
    mapped_df['Tech_Keywords'] = df['sub_industry']
    mapped_df['Country'] = df['country']
    mapped_df['Year'] = df['batch'].apply(batch_to_year)
    mapped_df['Founding_Year'] = mapped_df['Year']
    mapped_df['Startup_Stage'] = 'Active'
    mapped_df['Investor_Name'] = 'Y Combinator'
    mapped_df['Investor_Type'] = 'Accelerator'
    mapped_df['Investment_Stage'] = 'Seed'
    
    # Leere Spalten
    mapped_df['Business_Model_Type'] = None
    mapped_df['Funding_Amount'] = None
    mapped_df['Funding_Round'] = None
    mapped_df['Valuation'] = None
    mapped_df['Exit_Type'] = None
    
    # Spalten in korrekter Reihenfolge
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    mapped_df = mapped_df[required_columns]
    
    print(f"✓ {len(mapped_df)} Zeilen gemappt")
    return mapped_df


def main():
    """Hauptfunktion."""
    print("="*60)
    print("Y COMBINATOR - EUROPA SCRAPER (2015-2026)")
    print("="*60)
    
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        driver = setup_driver()
        
        # Scrape europäische Companies ab 2015
        companies = scrape_yc_europe(driver, min_year=2015)
        
        if not companies:
            print("⚠ Keine Companies gescraped - Erstelle leere CSV")
            companies = []
        
        mapped_df = map_to_schema(companies)
        
        output_path = './data/yc_companies.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Gespeichert: {output_path}")
        
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG - EUROPA STARTUPS")
        print("="*60)
        print(f"Anzahl Companies: {len(mapped_df)}")
        
        if len(mapped_df) > 0:
            print(f"\nVollständigkeit:")
            for col in ['Startup_Name', 'Industry', 'Country', 'Year']:
                non_null = mapped_df[col].notna().sum()
                pct = (non_null / len(mapped_df) * 100)
                print(f"  {col}: {pct:.1f}%")
            
            print(f"\nTop 10 Länder:")
            print(mapped_df['Country'].value_counts().head(10))
            
            print(f"\nTop 5 Industries:")
            print(mapped_df['Industry'].value_counts().head())
            
            print(f"\nJahresverteilung:")
            year_counts = mapped_df['Year'].value_counts().sort_index(ascending=False)
            for year, count in year_counts.head(10).items():
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
