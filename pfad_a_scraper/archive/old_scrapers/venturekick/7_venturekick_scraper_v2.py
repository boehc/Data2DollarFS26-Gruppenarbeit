"""
Venturekick.ch News Scraper V2
VERBESSERUNGEN:
- Bessere Investor-Extraktion aus Artikel-Text
- Tech Keywords aus Beschreibungen
- Sub-Industry aus Detail-Kategorien
Scraped Schweizer Startup-Funding von Venture Kick (Accelerator/Grant Program).
Alle 1,700+ News-Items, Filter 2020-2026, Industry-Tags aus Titel-Keywords.
"""

import time
import re
from datetime import datetime
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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


def extract_startup_name(title):
    """
    Extrahiert Startup-Namen aus News-Titel.
    WICHTIG: "Venture" und "Kick" sind NIEMALS Startup-Namen!
    
    Beispiele:
    - "corpod receives CHF 40,000 from Venture Kick..." → "corpod"
    - "Lobby raises USD 2.2 million..." → "Lobby"
    - "DeltaSpark receives CHF 150,000..." → "DeltaSpark"
    """
    if not title:
        return None
    
    # Blacklist für generische Wörter (KEINE Startup-Namen)
    blacklist = [
        'venture', 'kick', 'turning', 'growth', 'the', 'and', 'receives', 
        'from', 'raises', 'announces', 'launches', 'receives', 'wins',
        'chf', 'usd', 'eur', 'million', 'thousand'
    ]
    
    words = title.split()
    for word in words:
        # Erstes kapitalisiertes Wort mit 3+ Zeichen
        if word and len(word) >= 3 and word[0].isupper():
            clean = re.sub(r'[^\w]', '', word)
            if clean and clean.lower() not in blacklist:
                return clean
    
    return None


def extract_funding_amount(text):
    """
    Extrahiert Funding-Amount aus Text.
    Patterns: 
    - "CHF 40,000" (mit Komma-Tausender-Trenner!)
    - "CHF 150,000"
    - "USD 2.2 million"
    - "$225 million for Kandou..."
    - "raises USD 75 million"
    """
    if not text:
        return None
    
    # Erweiterte Patterns - WICHTIG: Komma-Tausender-Trenner!
    patterns = [
        # Pattern 1: "CHF 150,000" oder "USD 40,000" (Komma-Format)
        r'(CHF|USD|EUR|\$)\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?)',
        # Pattern 2: "$225 million" oder "USD 72 Million"
        r'(\$|USD|CHF|EUR)\s*(\d+\.?\d*)\s*(million|thousand|billion|k|m|b)',
        # Pattern 3: "72 Million USD" oder "2.2 million CHF"
        r'(\d+\.?\d*)\s*(million|thousand|billion|k|m|b)\s*(\$|USD|CHF|EUR)',
        # Pattern 4: "CHF 150" oder "USD 40" (ohne Einheit)
        r'(CHF|USD|EUR|\$)\s*(\d+\.?\d*)\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                groups = match.groups()
                
                # Extrahiere Betrag, Einheit, Währung
                amount = None
                unit = None
                currency = None
                
                for g in groups:
                    if not g:
                        continue
                    # Prüfe auf Zahl (mit oder ohne Komma/Punkt)
                    if re.match(r'\d+[,\.]?\d*', g.replace(',', '')):
                        # Ersetze Komma durch nichts für Parsing
                        amount = float(g.replace(',', ''))
                    elif g.upper() in ['CHF', 'USD', 'EUR', '$']:
                        currency = g.upper().replace('$', 'USD')
                    elif g.lower() in ['million', 'm']:
                        unit = 'M'
                    elif g.lower() in ['billion', 'b']:
                        unit = 'B'
                    elif g.lower() in ['thousand', 'k']:
                        unit = 'K'
                
                if amount and currency:
                    # Formatiere: "40K CHF", "2.2M USD", "150K CHF"
                    if unit:
                        return f"{amount}{unit} {currency}"
                    else:
                        # Keine Einheit → Konvertiere zu K/M basierend auf Größe
                        if amount < 1000:
                            # Kleine Zahlen: 40 → 40K, 150 → 150K
                            return f"{amount}K {currency}"
                        elif amount < 1000000:
                            # Mittlere Zahlen: 40000 → 40K, 150000 → 150K
                            return f"{amount/1000}K {currency}"
                        else:
                            # Große Zahlen: 2200000 → 2.2M
                            return f"{amount/1000000}M {currency}"
                
            except Exception as e:
                # Debug: Zeige Fehler
                # print(f"Parse-Fehler für '{text}': {e}")
                continue
    
    return None


def extract_funding_round(text):
    """
    Extrahiert Funding-Round aus Text.
    Patterns:
    - "Series A/B/C/D/E round"
    - "Seed round"
    - "receives CHF 40,000 from Venture Kick" → Venture Kick Grant
    """
    if not text:
        return 'Undisclosed'
    
    text_lower = text.lower()
    
    # Series Runden
    series_match = re.search(r'series\s+([a-z][\+\d]*)', text_lower)
    if series_match:
        series_letter = series_match.group(1).upper()
        return f'Series {series_letter}'
    
    # Seed Round
    if 'seed' in text_lower:
        if 'pre-seed' in text_lower or 'preseed' in text_lower:
            return 'Pre-Seed'
        return 'Seed'
    
    # Venture Kick spezifisch (nur wenn "from Venture Kick" oder "receives CHF X from VK")
    if 'from venture kick' in text_lower or 'venture kick' in text_lower:
        # Prüfe ob es wirklich ein VK-Grant ist (kleiner Betrag)
        amount_match = re.search(r'(\d+[,\.]?\d*)', text)
        if amount_match:
            amount_val = float(amount_match.group(1).replace(',', ''))
            # Venture Kick gibt typisch 10K, 40K, 150K
            if amount_val <= 200:  # <= 200K
                return 'Venture Kick Grant'
    
    # Investment/Funding (generic)
    if any(kw in text_lower for kw in ['investment', 'funding', 'financing', 'round']):
        return 'Funding Round'
    
    return 'Undisclosed'


def extract_investors(text):
    """
    NEUE FUNKTION: Extrahiert Investor-Namen aus Venturekick-Text.
    Patterns:
    - "led by X"
    - "investors include X, Y"
    - "Series A round with X and Y"
    - Venture Kick selbst bei Grants
    """
    if not text:
        return None
    
    investors = []
    
    # Pattern 1: "led by X"
    led_match = re.search(r'led by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s)', text)
    if led_match:
        inv = led_match.group(1).strip()
        if len(inv) > 2 and len(inv) < 60:
            investors.append(inv)
    
    # Pattern 2: "investors include X, Y" oder "with investors X and Y"
    investors_match = re.search(r'(?:investors?|with)\s+(?:include\s+)?([A-Z][A-Za-z\s,&.-]+?)(?:\.|participated|announced)', text, re.IGNORECASE)
    if investors_match:
        inv_text = investors_match.group(1)
        parts = re.split(r',|\sand\s', inv_text)
        for part in parts[:3]:  # Max 3
            inv = part.strip()
            if inv and len(inv) > 2 and inv not in investors:
                investors.append(inv)
    
    # Pattern 3: Venture Kick bei Grants
    if 'venture kick' in text.lower() and 'receives' in text.lower():
        # Bei VK-Grants ist VK selbst der "Investor" (Accelerator)
        if not investors:  # Nur wenn noch keine anderen Investoren
            investors.append('Venture Kick')
    
    return ', '.join(investors[:3]) if investors else None


def extract_business_model(text):
    """
    NEUE FUNKTION: Extrahiert Business Model (B2B/B2C/B2G).
    B2B ist DEFAULT für Enterprise/Platform Software.
    """
    if not text:
        return 'Unknown'
    
    text_lower = text.lower()
    
    # B2C Indicators (Direct-to-Consumer)
    b2c_keywords = ['consumer', 'retail', 'ecommerce', 'marketplace', 'fashion', 'lifestyle', 'gaming', 'entertainment']
    if any(kw in text_lower for kw in b2c_keywords):
        return 'B2C'
    
    # B2G Indicators (Business-to-Government)
    b2g_keywords = ['government', 'public sector', 'municipality', 'civic']
    if any(kw in text_lower for kw in b2g_keywords):
        return 'B2G'
    
    # B2B Indicators (Default für Enterprise, SaaS, Platform, Industrial)
    b2b_keywords = ['enterprise', 'saas', 'platform', 'b2b', 'business', 'industrial', 'manufacturing', 'supply chain']
    if any(kw in text_lower for kw in b2b_keywords):
        return 'B2B'
    
    return 'Unknown'


def extract_tech_keywords(text):
    """
    NEUE FUNKTION: Extrahiert Tech-Keywords aus Artikel-Text.
    """
    if not text:
        return None
    
    text_upper = text.upper()
    
    tech_keywords = {
        'AI': ['AI', 'ARTIFICIAL INTELLIGENCE', 'MACHINE LEARNING', 'ML', 'DEEP LEARNING'],
        'SaaS': ['SAAS', 'SOFTWARE AS A SERVICE', 'PLATFORM', 'CLOUD SOFTWARE'],
        'Biotech': ['BIOTECH', 'BIOTECHNOLOGY', 'GENOMICS', 'RNA', 'DNA', 'THERAPEUTIC', 'DRUG'],
        'Fintech': ['FINTECH', 'PAYMENT', 'BANKING', 'BLOCKCHAIN', 'CRYPTO'],
        'IoT': ['IOT', 'INTERNET OF THINGS', 'SENSOR', 'CONNECTED'],
        'Healthtech': ['MEDICAL', 'HEALTH', 'DIAGNOSTIC', 'CLINICAL', 'PATIENT'],
        'Cleantech': ['CLEANTECH', 'CLEAN', 'RENEWABLE', 'ENERGY', 'CARBON', 'CLIMATE', 'SOLAR'],
        'Robotics': ['ROBOT', 'AUTOMATION', 'AUTONOMOUS'],
        'AR/VR': ['AR', 'VR', 'AUGMENTED REALITY', 'VIRTUAL REALITY'],
    }
    
    found = []
    for keyword, patterns in tech_keywords.items():
        if any(p in text_upper for p in patterns):
            found.append(keyword)
    
    return ', '.join(found) if found else None


def extract_sub_industry(text, industry):
    """
    NEUE FUNKTION: Leitet Sub-Industry aus Text und Industry ab.
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Sub-Industry Mapping basierend auf Haupt-Industry
    sub_mappings = {
        'HEALTHCARE': {
            'Biotech': ['biotech', 'genomics', 'rna', 'dna', 'gene'],
            'MedTech': ['medical device', 'medtech', 'diagnostic', 'imaging'],
            'Digital Health': ['digital health', 'health app', 'telemedicine', 'patient'],
            'Pharma': ['pharma', 'drug', 'therapeutic', 'medicine']
        },
        'FINTECH': {
            'Payments': ['payment', 'transaction', 'pos', 'wallet'],
            'Banking': ['banking', 'neobank', 'digital bank', 'lending'],
            'Insurance': ['insurance', 'insurtech'],
            'Crypto': ['crypto', 'blockchain', 'defi', 'web3']
        },
        'SOFTWARE': {
            'SaaS': ['saas', 'software as a service', 'platform'],
            'Enterprise Software': ['enterprise', 'b2b software', 'business software'],
            'Analytics': ['analytics', 'data', 'insights', 'business intelligence'],
            'Cloud': ['cloud', 'infrastructure', 'devops']
        },
        'AI/ML': {
            'AI/ML': ['ai', 'machine learning', 'deep learning', 'artificial intelligence'],
            'Computer Vision': ['computer vision', 'image recognition', 'visual'],
            'NLP': ['nlp', 'natural language', 'language processing', 'chatbot']
        },
        'CLEANTECH': {
            'Energy': ['energy', 'solar', 'renewable', 'battery'],
            'Climate Tech': ['climate', 'carbon', 'co2', 'emissions'],
            'Circular Economy': ['recycling', 'circular', 'waste', 'sustainability']
        },
        'MOBILITY': {
            'Electric Vehicles': ['ev', 'electric vehicle', 'battery'],
            'Autonomous': ['autonomous', 'self-driving', 'adas'],
            'Logistics': ['logistics', 'supply chain', 'transport']
        },
        'ROBOTICS': {
            'Industrial Robotics': ['industrial robot', 'manufacturing', 'automation'],
            'Service Robotics': ['service robot', 'delivery', 'autonomous'],
            'Drones': ['drone', 'uav', 'aerial']
        }
    }
    
    if industry in sub_mappings:
        for sub_ind, keywords in sub_mappings[industry].items():
            if any(kw in text_lower for kw in keywords):
                return sub_ind
    
    return None


def extract_industry_from_keywords(text):
    """
    Leitet ECHTE Industry aus Titel-Keywords ab.
    WICHTIG: B2B/B2C sind BUSINESS MODELS, nicht Industries!
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Industry-Keyword-Mapping (NUR echte Industries!)
    industry_keywords = {
        'FINTECH': ['fintech', 'financial', 'payment', 'banking', 'blockchain', 'crypto', 'insurance', 'insurtech'],
        'HEALTHCARE': ['health', 'medical', 'biotech', 'pharma', 'therapeutic', 'diagnostics', 'medtech', 'clinical', 'hospital', 'patient'],
        'SOFTWARE': ['saas', 'software', 'platform', 'cloud', 'enterprise software', 'app'],
        'AI/ML': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning'],
        'INDUSTRIALS': ['manufacturing', 'industrial', 'construction', 'engineering', 'supply chain'],
        'CLEANTECH': ['climate', 'energy', 'sustainability', 'cleantech', 'renewable', 'carbon', 'green', 'solar', 'co2', 'environmental'],
        'AGTECH': ['agriculture', 'agtech', 'farming', 'food'],
        'MOBILITY': ['mobility', 'transport', 'automotive', 'ev', 'electric vehicle', 'logistics'],
        'CONSUMER': ['consumer', 'ecommerce', 'retail', 'marketplace', 'fashion', 'lifestyle'],
        'EDUCATION': ['education', 'edtech', 'learning', 'training'],
        'AEROSPACE': ['space', 'satellite', 'aerospace', 'aviation', 'drone'],
        'ROBOTICS': ['robotics', 'robot', 'automation', 'autonomous'],
    }
    
    for industry, keywords in industry_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return industry
    
    return None  # Unknown - wird später als "Unknown" gespeichert


def parse_date(date_str):
    """Parse Datum: DD.MM.YYYY → Year"""
    if not date_str:
        return None
    
    try:
        # Format: 02.04.2026
        parts = date_str.split('.')
        if len(parts) == 3:
            day, month, year = parts
            return int(year)
    except:
        pass
    
    return None


def scrape_venturekick_news(driver):
    """
    Scraped alle News von Venturekick.ch.
    Text-Parsing Strategie (keine DOM-Selektion).
    """
    url = 'https://www.venturekick.ch/index.cfm?page=135424'
    
    print(f"Öffne {url}")
    driver.get(url)
    
    print("Warte auf Seiteninhalt...")
    time.sleep(5)
    
    # Extrahiere gesamten Body-Text
    body = driver.find_element(By.TAG_NAME, 'body')
    body_text = body.text
    
    print(f"✓ Body-Text extrahiert ({len(body_text)} Zeichen)")
    
    # Parse zeilenweise
    lines = body_text.split('\n')
    
    news_items = []
    date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    
    print("\nParse News-Items...")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Finde Datum-Zeile
        if re.match(date_pattern, line):
            date_str = line
            
            # Nächste Zeile sollte Titel sein
            if i + 1 < len(lines):
                title = lines[i + 1].strip()
                
                # Validiere: Titel sollte länger sein und Wörter enthalten
                if title and len(title) > 10 and ' ' in title:
                    news_items.append({
                        'date': date_str,
                        'title': title
                    })
                
                i += 2  # Skip beide Zeilen
                continue
        
        i += 1
    
    print(f"✓ {len(news_items)} News-Items gefunden")
    
    return news_items


def map_to_schema(news_items):
    """
    Mappt News-Items zu 16-Felder Schema.
    Filter: 2020-2026
    WICHTIG: Duplikate NICHT entfernen (Merge & Clean Phase macht das)
    """
    if not news_items:
        return pd.DataFrame()
    
    mapped_data = []
    skipped_count = 0
    
    for item in news_items:
        # Extrahiere Jahr
        year = parse_date(item['date'])
        
        # FILTER: 2020-2026
        if not year or year < 2020 or year > 2026:
            skipped_count += 1
            continue
        
        # Extrahiere Startup-Name
        startup_name = extract_startup_name(item['title'])
        
        if not startup_name:
            skipped_count += 1
            continue
        
        # Extrahiere Funding
        funding_amount = extract_funding_amount(item['title'])
        funding_round = extract_funding_round(item['title'])
        
        # NEUE EXTRAKTIONEN
        investors = extract_investors(item['title'])
        tech_keywords = extract_tech_keywords(item['title'])
        
        # Industry aus Keywords (ECHTE Industry, nicht B2B!)
        industry = extract_industry_from_keywords(item['title'])
        if not industry:
            industry = 'Unknown'
        
        # Business Model (B2B/B2C/B2G)
        business_model = extract_business_model(item['title'])
        
        # Sub-Industry ableiten
        sub_industry = extract_sub_industry(item['title'], industry)
        
        # Investment Stage basiert auf Funding Round (NICHT nur Amount!)
        investment_stage = 'Early Stage'  # Default
        
        # Priorität 1: Funding Round
        if funding_round:
            round_lower = funding_round.lower()
            if 'pre-seed' in round_lower or 'venture kick grant' in round_lower:
                investment_stage = 'Pre-Seed'
            elif 'seed' in round_lower:
                investment_stage = 'Seed'
            elif 'series a' in round_lower:
                investment_stage = 'Series A'
            elif 'series b' in round_lower:
                investment_stage = 'Series B'
            elif 'series c' in round_lower:
                investment_stage = 'Series C'
            elif 'series d' in round_lower or 'series e' in round_lower:
                investment_stage = 'Growth'
        
        # Priorität 2: Funding Amount (falls kein Round erkannt)
        if investment_stage == 'Early Stage' and funding_amount:
            amount_match = re.search(r'(\d+\.?\d*)', str(funding_amount))
            if amount_match:
                amount_val = float(amount_match.group(1))
                # Konvertiere zu Tausend
                if 'M' in funding_amount:
                    amount_val *= 1000
                elif 'B' in funding_amount:
                    amount_val *= 1000000
                
                if amount_val < 50:
                    investment_stage = 'Pre-Seed'
                elif amount_val < 200:
                    investment_stage = 'Seed'
                elif amount_val < 3000:
                    investment_stage = 'Series A'
                elif amount_val < 10000:
                    investment_stage = 'Series B'
                elif amount_val < 30000:
                    investment_stage = 'Series C'
                else:
                    investment_stage = 'Growth'
        
        mapped_data.append({
            'Startup_Name': startup_name,
            'Industry': industry,
            'Sub_Industry': sub_industry or None,
            'Business_Model_Type': business_model,  # JETZT: B2B/B2C/B2G statt Industry!
            'Tech_Keywords': tech_keywords or None,
            'Year': year,
            'Funding_Amount': funding_amount or None,
            'Funding_Round': funding_round,
            'Investment_Stage': investment_stage,
            'Investor_Names': investors or None,
            'Location': 'Switzerland',
            'City': None,
            'Canton': None,
            'Founded_Year': None,
            'Employees': None,
            'Website': None
        })
    
    df = pd.DataFrame(mapped_data)
    
    print(f"\n✓ {len(df)} Einträge gemappt (2020-2026)")
    print(f"⚠️  {skipped_count} Einträge übersprungen (vor 2020 oder ungültig)")
    
    # Duplikate-Info (aber NICHT entfernen!)
    if len(df) > 0:
        duplicates = df.duplicated(subset=['Startup_Name'], keep=False).sum()
        if duplicates > 0:
            print(f"ℹ️  {duplicates} Duplikate gefunden (werden in Merge & Clean Phase behandelt)")
    
    # Spalten in korrekter Reihenfolge (16-Felder-Schema)
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investment_Stage', 'Investor_Names', 'Location', 'City',
        'Canton', 'Founded_Year', 'Employees', 'Website'
    ]
    
    return df[required_columns]


def main():
    """Hauptfunktion."""
    print("="*70)
    print("VENTUREKICK.CH SCRAPER - SCHWEIZER STARTUP GRANTS")
    print("="*70)
    
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        driver = setup_driver()
        
        # Scrape alle News
        news_items = scrape_venturekick_news(driver)
        
        if not news_items:
            print("⚠ Keine News-Items gescraped")
            return
        
        # Mapping zu Schema
        print("\n🔄 Mappe zu Schema...")
        mapped_df = map_to_schema(news_items)
        
        if len(mapped_df) == 0:
            print("⚠ Keine Daten nach Mapping (Filter 2020-2026)")
            return
        
        # Speichern
        output_path = './data/venturekick_startups.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Gespeichert: {output_path}")
        
        # ZUSAMMENFASSUNG
        print("\n" + "="*70)
        print("ZUSAMMENFASSUNG")
        print("="*70)
        print(f"Anzahl Startups: {len(mapped_df)}")
        
        print(f"\nVollständigkeit:")
        for col in ['Startup_Name', 'Industry', 'Year', 'Funding_Amount', 'Funding_Round', 'Investment_Stage']:
            non_null = mapped_df[col].notna().sum()
            pct = (non_null / len(mapped_df) * 100)
            print(f"  {col}: {pct:.1f}%")
        
        print(f"\nTop 10 Startups:")
        print(mapped_df[['Startup_Name', 'Year', 'Funding_Amount', 'Funding_Round', 'Investment_Stage']].head(10).to_string())
        
        if mapped_df['Year'].notna().sum() > 0:
            print(f"\nJahresverteilung (2020-2026):")
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
        
        # Duplikate-Statistik
        dup_names = mapped_df[mapped_df.duplicated(subset=['Startup_Name'], keep=False)]['Startup_Name'].unique()
        if len(dup_names) > 0:
            print(f"\nℹ️  Startups mit mehreren Funding-Runden (Venture Kick Stages):")
            print(f"  Anzahl: {len(dup_names)}")
            print(f"  Beispiele: {list(dup_names[:10])}")
            print(f"  → Deduplizierung erfolgt in Merge & Clean Phase")
        
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
