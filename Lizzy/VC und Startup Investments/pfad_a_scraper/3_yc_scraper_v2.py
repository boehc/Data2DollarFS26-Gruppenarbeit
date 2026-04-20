"""
Y Combinator Companies Scraper V2
Verbesserte Version mit korrektem Parsing der Company-Cards.
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
    
    Format der YC Company Card:
    Zeile 1: NameLocation (z.B. "AirbnbSan Francisco, CA, USA")
    Zeile 2: Description
    Zeile 3: BATCH (z.B. "WINTER 2009")
    Zeile 4: INDUSTRY (z.B. "CONSUMER")
    Zeile 5: SUB_INDUSTRY (z.B. "TRAVEL, LEISURE AND TOURISM")
    
    Args:
        text (str): Roher Text vom Company-Link
        
    Returns:
        dict: Geparste Company-Daten
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
    # Format: "CompanyNameCity, State, Country" oder "CompanyNameCity, Country"
    first_line = lines[0]
    
    # Suche nach Komma (trennt Name von Location)
    # Heuristic: Nach dem ersten Großbuchstaben-Wort kommt ein Komma
    # Beispiel: "AirbnbSan Francisco" → "Airbnb" + "San Francisco"
    
    # Versuche Location zu finden (enthält Komma)
    comma_pos = first_line.find(',')
    if comma_pos > 0:
        # Arbeite rückwärts vom Komma zum Anfang der Stadt
        before_comma = first_line[:comma_pos]
        
        # Finde wo der Name endet (letzter zusammenhängender Großbuchstaben-Start)
        # Beispiel: "AirbnbSan" → "Airbnb" ist Name, "San" ist Start der Stadt
        words = re.findall(r'[A-Z][a-z]*', before_comma)
        
        if len(words) >= 2:
            # Name ist erstes Wort(er), Location ist Rest
            name_end = before_comma.find(words[-1])
            company['name'] = before_comma[:name_end].strip()
            location_str = first_line[name_end:].strip()
        else:
            # Fallback: alles vor Komma ist Name+Stadt gemischt
            company['name'] = words[0] if words else before_comma
            location_str = first_line[len(words[0]) if words else 0:].strip()
        
        # Parse Location (City, State, Country oder City, Country)
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
        # Kein Komma gefunden - gesamte Zeile als Name
        company['name'] = first_line
    
    # Zeile 2: Description
    if len(lines) > 1:
        company['description'] = lines[1]
    
    # Zeile 3+: Batch, Industry, Sub-Industry
    # Batch ist eindeutig: WINTER YYYY oder SUMMER YYYY
    batch_pattern = r'^(WINTER|SUMMER)\s+\d{4}$'
    
    for i in range(2, len(lines)):
        line = lines[i]
        if re.match(batch_pattern, line):
            company['batch'] = line
            # Nächste Zeilen sind Industry und Sub-Industry
            if i + 1 < len(lines):
                company['industry'] = lines[i + 1]
            if i + 2 < len(lines):
                company['sub_industry'] = lines[i + 2]
            break
    
    return company


def batch_to_year(batch):
    """
    Konvertiert YC Batch zu Jahr.
    WINTER 2021 → 2021, SUMMER 2020 → 2020
    """
    if not batch:
        return None
    year_match = re.search(r'\d{4}', batch)
    if year_match:
        return int(year_match.group(0))
    return None


def scrape_yc_companies(driver, max_companies=1000):
    """
    Scraped Y Combinator Companies.
    
    Args:
        driver: Selenium WebDriver
        max_companies: Maximale Anzahl zu scrapender Companies
        
    Returns:
        list: Liste von Company-Dicts
    """
    print("Öffne https://www.ycombinator.com/companies")
    driver.get('https://www.ycombinator.com/companies')
    
    print("Warte auf Seiteninhalt...")
    wait = WebDriverWait(driver, 20)
    
    try:
        # Warte auf Company-Links
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/companies/"]')))
        print("✓ Company-Links gefunden")
        time.sleep(3)
        
        # Scrolle um mehr Companies zu laden
        print("Scrolle für Lazy Loading...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 20
        
        while scroll_attempts < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"  Keine neuen Inhalte mehr (Scroll {scroll_attempts})")
                break
            last_height = new_height
            scroll_attempts += 1
            print(f"  Scroll {scroll_attempts}/{max_scrolls}")
        
        # Extrahiere Company-Links
        company_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/companies/"]')
        print(f"Gefundene Company-Links: {len(company_links)}")
        
        # Parse Companies
        companies = []
        seen_names = set()
        
        for link in company_links[:max_companies]:
            try:
                text_content = link.text
                
                if not text_content or len(text_content) < 10:
                    continue
                
                # Parse Company
                company = parse_company_text(text_content)
                
                if not company['name']:
                    continue
                    
                if company['name'] in seen_names:
                    continue
                    
                seen_names.add(company['name'])
                companies.append(company)
                
                if len(companies) % 100 == 0:
                    print(f"  Verarbeitet: {len(companies)} Companies...")
                    
            except Exception as e:
                continue
        
        print(f"✓ {len(companies)} Companies extrahiert")
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
    
    # Mapping zu standardisiertem Schema
    mapped_df = pd.DataFrame()
    
    mapped_df['Startup_Name'] = df['name']
    mapped_df['Industry'] = df['industry']
    mapped_df['Sub_Industry'] = df['sub_industry']
    mapped_df['Tech_Keywords'] = df['sub_industry']  # Sub-Industry als Keywords
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
    print("Y COMBINATOR COMPANIES SCRAPER V2")
    print("="*60)
    
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        driver = setup_driver()
        companies = scrape_yc_companies(driver, max_companies=1000)
        
        if not companies:
            print("⚠ Keine Companies gescraped - Erstelle leere CSV")
            companies = []
        
        mapped_df = map_to_schema(companies)
        
        output_path = './data/yc_companies.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Gespeichert: {output_path}")
        
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Anzahl Companies: {len(mapped_df)}")
        
        if len(mapped_df) > 0:
            print(f"\nVollständigkeit:")
            for col in mapped_df.columns:
                non_null = mapped_df[col].notna().sum()
                pct = (non_null / len(mapped_df) * 100)
                print(f"  {col}: {pct:.1f}%")
            
            print(f"\nTop 5 Länder:")
            print(mapped_df['Country'].value_counts().head())
            
            print(f"\nTop 5 Industries:")
            print(mapped_df['Industry'].value_counts().head())
        
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
