"""
VCLense.ch Scraper
Scraped Startup-Daten von der VCLense Dashboard (React SPA).
"""

import time
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


def scrape_vclense(driver):
    """
    Scraped Daten von VCLense Dashboard.
    
    Args:
        driver: Selenium WebDriver
        
    Returns:
        list: Liste von Startup-Dicts
    """
    url = 'https://dashboard.vclense.ch/'
    print(f"Öffne {url}")
    
    try:
        driver.get(url)
        
        # Warte auf das Laden der Seite (max 20 Sekunden)
        print("Warte auf Seiteninhalt...")
        wait = WebDriverWait(driver, 20)
        
        # Versuche verschiedene mögliche Selektoren für die Datentabelle
        possible_selectors = [
            (By.CSS_SELECTOR, 'table'),
            (By.CSS_SELECTOR, '.table'),
            (By.CSS_SELECTOR, '[class*="table"]'),
            (By.CSS_SELECTOR, '.MuiDataGrid-root'),  # Material-UI DataGrid
            (By.CSS_SELECTOR, '[class*="grid"]'),
            (By.TAG_NAME, 'table')
        ]
        
        table_found = False
        for by, selector in possible_selectors:
            try:
                wait.until(EC.presence_of_element_located((by, selector)))
                print(f"✓ Tabelle gefunden mit Selektor: {selector}")
                table_found = True
                break
            except:
                continue
        
        if not table_found:
            print("⚠ Keine Tabelle gefunden, versuche alternativen Ansatz...")
            time.sleep(5)  # Fallback delay
        
        # Page Source für Analyse speichern
        page_source = driver.page_source
        print(f"Page Source Länge: {len(page_source)} Zeichen")
        
        # Scroll zur Bottom für Lazy Loading
        print("Scrolle für Lazy Loading...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 5
        
        while scroll_attempts < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
            print(f"  Scroll {scroll_attempts}/{max_scrolls}")
        
        # Versuche Daten zu extrahieren
        startups = []
        
        # Strategie 1: Tabellen-Zeilen
        try:
            rows = driver.find_elements(By.CSS_SELECTOR, 'tr')
            print(f"Gefundene Tabellenzeilen: {len(rows)}")
            
            for idx, row in enumerate(rows[1:], 1):  # Skip header
                try:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    if len(cells) >= 3:
                        startup = {
                            'Startup_Name': cells[0].text.strip() if len(cells) > 0 else None,
                            'Industry': cells[1].text.strip() if len(cells) > 1 else None,
                            'Funding_Amount': cells[2].text.strip() if len(cells) > 2 else None,
                            'Investor_Name': cells[3].text.strip() if len(cells) > 3 else None,
                            'Country': cells[4].text.strip() if len(cells) > 4 else None,
                            'Year': cells[5].text.strip() if len(cells) > 5 else None,
                            'Investment_Stage': cells[6].text.strip() if len(cells) > 6 else None,
                        }
                        
                        # Nur hinzufügen wenn mindestens Name vorhanden
                        if startup['Startup_Name']:
                            startups.append(startup)
                            
                            if idx % 50 == 0:
                                print(f"  Verarbeitet: {idx} Zeilen...")
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"⚠ Tabellen-Extraktion fehlgeschlagen: {e}")
        
        # Strategie 2: Fallback - Card/List Items
        if len(startups) < 10:
            print("Versuche alternative Extraktion (Cards/Items)...")
            try:
                items = driver.find_elements(By.CSS_SELECTOR, '[class*="item"], [class*="card"], [class*="row"]')
                print(f"Gefundene Items: {len(items)}")
                
                for item in items[:100]:  # Limit für Performance
                    text = item.text
                    if text and len(text) > 10:
                        startup = {
                            'Startup_Name': text.split('\n')[0] if '\n' in text else text[:50],
                            'Industry': None,
                            'Funding_Amount': None,
                            'Investor_Name': None,
                            'Country': 'Switzerland',  # VCLense ist CH-fokussiert
                            'Year': None,
                            'Investment_Stage': None,
                        }
                        startups.append(startup)
                        
            except Exception as e:
                print(f"⚠ Alternative Extraktion fehlgeschlagen: {e}")
        
        print(f"✓ {len(startups)} Startups extrahiert")
        return startups
        
    except Exception as e:
        print(f"✗ Fehler beim Scraping: {e}")
        # Screenshot für Debugging
        try:
            driver.save_screenshot('./data/vclense_error.png')
            print("Debug Screenshot gespeichert: ./data/vclense_error.png")
        except:
            pass
        return []


def map_to_schema(startups):
    """
    Mappt VCLense Daten zu unserem Schema.
    
    Args:
        startups (list): Liste von Startup-Dicts
        
    Returns:
        pd.DataFrame: Gemappter DataFrame
    """
    if not startups:
        print("⚠ Keine Daten zum Mappen vorhanden")
        return pd.DataFrame()
    
    df = pd.DataFrame(startups)
    
    # Alle erforderlichen Spalten sicherstellen
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    # Tech_Keywords aus Industry ableiten
    if 'Industry' in df.columns:
        df['Tech_Keywords'] = df['Industry']
    
    # Spalten in korrekter Reihenfolge
    df = df[required_columns]
    
    print(f"✓ {len(df)} Zeilen gemappt")
    return df


def main():
    """Hauptfunktion: Orchestriert den Scraping Prozess."""
    print("="*60)
    print("VCLENSE.CH SCRAPER")
    print("="*60)
    
    # Data Ordner sicherstellen
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        # 1. WebDriver setup
        driver = setup_driver()
        
        # 2. Scraping
        startups = scrape_vclense(driver)
        
        if not startups:
            print("\n⚠ WARNUNG: Keine Daten gescraped!")
            print("Mögliche Gründe:")
            print("  - Website-Struktur hat sich geändert")
            print("  - JavaScript-Rendering hat nicht funktioniert")
            print("  - Zugriff wurde blockiert")
            print("\nErstelle leeres DataFrame als Fallback...")
            
            # Fallback: Leeres DataFrame mit korrekter Struktur
            df = pd.DataFrame(columns=[
                'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
                'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
                'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
                'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
            ])
        else:
            # 3. Zu Schema mappen
            df = map_to_schema(startups)
        
        # 4. Speichern
        output_path = './data/vclense_startups.csv'
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
