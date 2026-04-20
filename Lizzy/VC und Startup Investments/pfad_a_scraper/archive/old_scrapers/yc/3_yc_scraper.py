"""
Y Combinator Companies Scraper
Scraped Company-Daten von YC Directory.
"""

import time
import json
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
    """
    Richtet Selenium Chrome WebDriver ein (headless).
    
    Returns:
        webdriver.Chrome: Konfigurierter WebDriver
    """
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


def extract_json_from_page(driver):
    """
    Versucht JSON-Daten direkt aus dem Page Source zu extrahieren.
    Viele React Apps haben die Daten im __NEXT_DATA__ Script-Tag.
    
    Args:
        driver: Selenium WebDriver
        
    Returns:
        dict: Extrahierte JSON-Daten oder None
    """
    try:
        # Suche nach __NEXT_DATA__ Script Tag (Next.js Pattern)
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        
        for script in scripts:
            content = script.get_attribute('innerHTML')
            if '__NEXT_DATA__' in content or 'application/json' in script.get_attribute('type'):
                # Versuche JSON zu parsen
                try:
                    # Entferne JavaScript-Wrapper
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(0))
                        print("✓ JSON-Daten im Page Source gefunden")
                        return data
                except json.JSONDecodeError:
                    continue
        
        return None
        
    except Exception as e:
        print(f"⚠ Fehler bei JSON-Extraktion: {e}")
        return None


def scrape_yc_with_scroll(driver):
    """
    Scraped YC Companies durch Scrollen und Element-Extraktion.
    
    Args:
        driver: Selenium WebDriver
        
    Returns:
        list: Liste von Company-Dicts
    """
    url = 'https://www.ycombinator.com/companies'
    print(f"Öffne {url}")
    
    try:
        driver.get(url)
        
        # Warte auf Seiteninhalt
        print("Warte auf Seiteninhalt...")
        wait = WebDriverWait(driver, 20)
        
        # Warte auf Company-Cards oder -Links
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/companies/"]')))
            print("✓ Company-Links gefunden")
        except:
            print("⚠ Timeout beim Warten auf Company-Links")
            time.sleep(5)
        
        # Erst JSON-Extraktion versuchen (schneller!)
        json_data = extract_json_from_page(driver)
        if json_data:
            companies = extract_companies_from_json(json_data)
            if companies:
                print(f"✓ {len(companies)} Companies aus JSON extrahiert")
                return companies
        
        # Fallback: Scrollen und scrapen
        print("Verwende Scroll-Methode...")
        companies = []
        
        # Scroll mehrmals um mehr Startups zu laden
        print("Scrolle für Lazy Loading...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 10  # YC hat viele Companies
        
        while scroll_attempts < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
            print(f"  Scroll {scroll_attempts}/{max_scrolls}")
        
        # Extrahiere Company-Cards
        company_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/companies/"]')
        print(f"Gefundene Company-Links: {len(company_links)}")
        
        # Extrahiere Daten aus jedem Link/Card
        seen_names = set()
        
        for link in company_links[:500]:  # Limit für Performance
            try:
                # Parent Element könnte mehr Infos enthalten
                parent = link.find_element(By.XPATH, './..')
                text_content = parent.text
                
                # Name aus href extrahieren
                href = link.get_attribute('href')
                name_match = re.search(r'/companies/([^/]+)', href)
                name = name_match.group(1).replace('-', ' ').title() if name_match else None
                
                if not name or name in seen_names:
                    continue
                
                seen_names.add(name)
                
                # Versuche weitere Daten zu extrahieren
                lines = text_content.split('\n')
                
                company = {
                    'Startup_Name': name,
                    'one_liner': lines[1] if len(lines) > 1 else None,
                    'tags': ', '.join(lines[2:]) if len(lines) > 2 else None,
                    'batch': extract_batch_from_text(text_content),
                    'website': href,
                }
                
                companies.append(company)
                
                if len(companies) % 100 == 0:
                    print(f"  Verarbeitet: {len(companies)} Companies...")
                    
            except Exception as e:
                continue
        
        print(f"✓ {len(companies)} Companies extrahiert")
        return companies
        
    except Exception as e:
        print(f"✗ Fehler beim Scraping: {e}")
        import traceback
        traceback.print_exc()
        return []


def extract_companies_from_json(data):
    """
    Extrahiert Company-Daten aus JSON-Struktur.
    
    Args:
        data (dict): JSON-Daten
        
    Returns:
        list: Liste von Company-Dicts
    """
    companies = []
    
    try:
        # Durchsuche JSON-Struktur nach Company-Arrays
        def find_companies_recursive(obj, depth=0):
            if depth > 10:  # Prevent infinite recursion
                return
            
            if isinstance(obj, dict):
                # Suche nach typischen Company-Feldern
                if 'name' in obj and 'batch' in obj:
                    companies.append(obj)
                else:
                    for value in obj.values():
                        find_companies_recursive(value, depth + 1)
            elif isinstance(obj, list):
                for item in obj:
                    find_companies_recursive(item, depth + 1)
        
        find_companies_recursive(data)
        
    except Exception as e:
        print(f"⚠ Fehler bei JSON-Parsing: {e}")
    
    return companies


def extract_batch_from_text(text):
    """
    Extrahiert YC Batch (z.B. 'W21', 'S20') aus Text.
    
    Args:
        text (str): Text zum Durchsuchen
        
    Returns:
        str: Batch oder None
    """
    batch_match = re.search(r'[WS]\d{2}', text)
    return batch_match.group(0) if batch_match else None


def map_to_schema(companies):
    """
    Mappt YC Company-Daten zu unserem Schema.
    
    Args:
        companies (list): Liste von Company-Dicts
        
    Returns:
        pd.DataFrame: Gemappter DataFrame
    """
    if not companies:
        print("⚠ Keine Daten zum Mappen vorhanden")
        return pd.DataFrame()
    
    df = pd.DataFrame(companies)
    
    # Mapping
    mapped_df = pd.DataFrame()
    
    mapped_df['Startup_Name'] = df.get('name', df.get('Startup_Name'))
    mapped_df['Industry'] = df.get('tags', df.get('industry'))
    mapped_df['Tech_Keywords'] = df.get('tags', df.get('tags'))
    mapped_df['Country'] = df.get('country', df.get('location', 'USA'))
    mapped_df['Startup_Stage'] = 'Active'
    
    # Batch → Year konvertieren (W21 = Winter 2021)
    def batch_to_year(batch):
        if not batch or not isinstance(batch, str):
            return None
        year_match = re.search(r'\d{2}', batch)
        if year_match:
            year = int(year_match.group(0))
            # YC batches: 00-49 = 2000-2049, 50-99 = 1950-1999
            return 2000 + year if year < 50 else 1900 + year
        return None
    
    if 'batch' in df.columns:
        mapped_df['Year'] = df['batch'].apply(batch_to_year)
        mapped_df['Founding_Year'] = mapped_df['Year']
    
    # Alle fehlenden Spalten
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    for col in required_columns:
        if col not in mapped_df.columns:
            mapped_df[col] = None
    
    # Investor für YC Companies ist immer YC
    mapped_df['Investor_Name'] = 'Y Combinator'
    mapped_df['Investor_Type'] = 'Accelerator'
    mapped_df['Investment_Stage'] = 'Seed'
    
    # Spalten in korrekter Reihenfolge
    mapped_df = mapped_df[required_columns]
    
    print(f"✓ {len(mapped_df)} Zeilen gemappt")
    return mapped_df


def main():
    """Hauptfunktion: Orchestriert den Scraping Prozess."""
    print("="*60)
    print("Y COMBINATOR COMPANIES SCRAPER")
    print("="*60)
    
    # Data Ordner sicherstellen
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        # 1. WebDriver setup
        driver = setup_driver()
        
        # 2. Scraping
        companies = scrape_yc_with_scroll(driver)
        
        if not companies:
            print("\n⚠ WARNUNG: Keine Daten gescraped!")
            print("Erstelle leeres DataFrame als Fallback...")
            
            df = pd.DataFrame(columns=[
                'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
                'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
                'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
                'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
            ])
        else:
            # 3. Zu Schema mappen
            df = map_to_schema(companies)
        
        # 4. Speichern
        output_path = './data/yc_companies.csv'
        df.to_csv(output_path, index=False)
        print(f"✓ Gespeichert: {output_path}")
        
        # 5. Summary
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Anzahl Datenpunkte: {len(df)}")
        if len(df) > 0:
            print(f"Beispiel-Daten:")
            print(df.head(3).to_string())
        
        print("\n✓ ERFOLGREICH ABGESCHLOSSEN")
        
    except Exception as e:
        print(f"\n✗ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("WebDriver geschlossen")


if __name__ == '__main__':
    main()
