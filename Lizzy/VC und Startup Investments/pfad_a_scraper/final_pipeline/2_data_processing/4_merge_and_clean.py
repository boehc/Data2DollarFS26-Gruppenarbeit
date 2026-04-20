"""
Merge, Clean & Enrich
Kombiniert alle Datenquellen, bereinigt und reichert Daten an.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re


def load_datasets():
    """
    Lädt alle drei CSV-Dateien.
    
    Returns:
        tuple: (kaggle_df, vclense_df, yc_df)
    """
    print("Lade Datasets...")
    
    data_dir = Path('./data')
    
    kaggle_path = data_dir / 'kaggle_crunchbase.csv'
    vclense_path = data_dir / 'vclense_startups.csv'
    yc_path = data_dir / 'yc_companies.csv'
    
    dfs = []
    names = ['Kaggle/Crunchbase', 'VCLense', 'Y Combinator']
    paths = [kaggle_path, vclense_path, yc_path]
    
    for name, path in zip(names, paths):
        if path.exists():
            df = pd.read_csv(path, low_memory=False)
            print(f"  ✓ {name}: {len(df)} Zeilen")
            dfs.append(df)
        else:
            print(f"  ⚠ {name}: Datei nicht gefunden, überspringe...")
            dfs.append(pd.DataFrame())
    
    return tuple(dfs)


def normalize_columns(df):
    """
    Normalisiert Spaltennamen zu unserem Schema.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: Normalisierter DataFrame
    """
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    # Stelle sicher, dass alle Spalten existieren
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    # Nur die erforderlichen Spalten behalten
    df = df[required_columns].copy()
    
    return df


def derive_investor_type(investor_name):
    """
    Leitet Investor-Typ vom Namen ab.
    
    Args:
        investor_name (str): Name des Investors
        
    Returns:
        str: Investor-Typ
    """
    if pd.isna(investor_name):
        return 'Unknown'
    
    name_lower = str(investor_name).lower()
    
    # VC Fund Keywords
    vc_keywords = ['ventures', 'capital', 'vc', 'fund', 'partners', 'investment']
    if any(keyword in name_lower for keyword in vc_keywords):
        return 'VC Fund'
    
    # Angel Investor Keywords
    angel_keywords = ['angel', 'individual']
    if any(keyword in name_lower for keyword in angel_keywords):
        return 'Angel Investor'
    
    # Accelerator Keywords
    accelerator_keywords = ['accelerator', 'combinator', 'techstars', 'incubator']
    if any(keyword in name_lower for keyword in accelerator_keywords):
        return 'Accelerator'
    
    # Corporate VC Keywords
    cvc_keywords = ['corporate', 'labs', 'innovation']
    if any(keyword in name_lower for keyword in cvc_keywords):
        return 'Corporate VC'
    
    return 'Other'


def derive_business_model(industry, tech_keywords):
    """
    Leitet Business Model Type von Industry/Keywords ab.
    
    Args:
        industry (str): Industry
        tech_keywords (str): Tech Keywords
        
    Returns:
        str: Business Model Type
    """
    combined = f"{industry} {tech_keywords}".lower() if pd.notna(industry) or pd.notna(tech_keywords) else ""
    
    # SaaS
    saas_keywords = ['saas', 'software', 'platform', 'subscription', 'cloud', 'api']
    if any(keyword in combined for keyword in saas_keywords):
        return 'SaaS'
    
    # Marketplace
    marketplace_keywords = ['marketplace', 'ecommerce', 'e-commerce', 'platform', 'retail']
    if any(keyword in combined for keyword in marketplace_keywords):
        return 'Marketplace'
    
    # Hardware
    hardware_keywords = ['hardware', 'device', 'robotics', 'iot', 'sensor', 'wearable']
    if any(keyword in combined for keyword in hardware_keywords):
        return 'Hardware'
    
    # Fintech
    fintech_keywords = ['fintech', 'payments', 'banking', 'finance', 'crypto', 'blockchain']
    if any(keyword in combined for keyword in fintech_keywords):
        return 'Fintech'
    
    # Healthcare/Biotech
    health_keywords = ['health', 'medical', 'biotech', 'pharmaceutical', 'therapy']
    if any(keyword in combined for keyword in health_keywords):
        return 'Healthcare/Biotech'
    
    # Consumer
    consumer_keywords = ['consumer', 'b2c', 'social', 'media', 'entertainment']
    if any(keyword in combined for keyword in consumer_keywords):
        return 'Consumer'
    
    return 'Other'


def enrich_data(df):
    """
    Reichert Daten mit abgeleiteten Feldern an.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: Angereicherter DataFrame
    """
    print("\nReichere Daten an...")
    
    # 1. Investor_Type ableiten
    if 'Investor_Type' in df.columns:
        mask = df['Investor_Type'].isna() & df['Investor_Name'].notna()
        df.loc[mask, 'Investor_Type'] = df.loc[mask, 'Investor_Name'].apply(derive_investor_type)
        print(f"  ✓ Investor_Type: {mask.sum()} Werte abgeleitet")
    
    # 2. Business_Model_Type ableiten
    if 'Business_Model_Type' in df.columns:
        mask = df['Business_Model_Type'].isna()
        df.loc[mask, 'Business_Model_Type'] = df.loc[mask].apply(
            lambda row: derive_business_model(row.get('Industry'), row.get('Tech_Keywords')),
            axis=1
        )
        print(f"  ✓ Business_Model_Type: {mask.sum()} Werte abgeleitet")
    
    # 3. Year aus Founding_Year ableiten wenn Year fehlt
    if 'Year' in df.columns and 'Founding_Year' in df.columns:
        mask = df['Year'].isna() & df['Founding_Year'].notna()
        df.loc[mask, 'Year'] = df.loc[mask, 'Founding_Year']
        print(f"  ✓ Year: {mask.sum()} Werte aus Founding_Year abgeleitet")
    
    # 4. Country normalisieren
    if 'Country' in df.columns:
        country_mapping = {
            'USA': 'United States',
            'US': 'United States',
            'UK': 'United Kingdom',
            'CH': 'Switzerland',
            'DE': 'Germany',
            'DEU': 'Germany',
        }
        df['Country'] = df['Country'].replace(country_mapping)
    
    # 5. Funding_Amount zu numerisch konvertieren
    if 'Funding_Amount' in df.columns:
        def parse_funding(value):
            if pd.isna(value):
                return None
            
            value_str = str(value).upper().replace(',', '').replace('$', '').strip()
            
            # Handle Million/Billion notations
            multiplier = 1
            if 'M' in value_str:
                multiplier = 1_000_000
                value_str = value_str.replace('M', '')
            elif 'B' in value_str:
                multiplier = 1_000_000_000
                value_str = value_str.replace('B', '')
            
            try:
                return float(value_str) * multiplier
            except:
                return None
        
        df['Funding_Amount'] = df['Funding_Amount'].apply(parse_funding)
    
    return df


def deduplicate(df):
    """
    Entfernt Duplikate basierend auf Startup_Name + Year.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: Deduplizierter DataFrame
    """
    print("\nEntferne Duplikate...")
    
    before = len(df)
    
    # Normalisiere Namen für besseres Matching
    df['_name_normalized'] = df['Startup_Name'].str.lower().str.strip()
    
    # Dedupliziere auf normalisiertem Namen + Jahr
    df = df.drop_duplicates(subset=['_name_normalized', 'Year'], keep='first')
    
    # Entferne Hilfsspalte
    df = df.drop(columns=['_name_normalized'])
    
    after = len(df)
    removed = before - after
    
    print(f"  ✓ {removed} Duplikate entfernt ({before} → {after} Zeilen)")
    
    return df


def fill_missing_strategically(df):
    """
    Füllt fehlende Werte strategisch.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame mit gefüllten Werten
    """
    print("\nFülle fehlende Werte...")
    
    # Country: Default zu "Unknown" wenn leer
    if 'Country' in df.columns:
        before = df['Country'].isna().sum()
        df['Country'] = df['Country'].fillna('Unknown')
        print(f"  ✓ Country: {before} Werte gefüllt")
    
    # Startup_Stage: Default zu "Operating" wenn leer
    if 'Startup_Stage' in df.columns:
        before = df['Startup_Stage'].isna().sum()
        df['Startup_Stage'] = df['Startup_Stage'].fillna('Operating')
        print(f"  ✓ Startup_Stage: {before} Werte gefüllt")
    
    # Investor_Type: Default zu "Unknown" wenn leer
    if 'Investor_Type' in df.columns:
        before = df['Investor_Type'].isna().sum()
        df['Investor_Type'] = df['Investor_Type'].fillna('Unknown')
        print(f"  ✓ Investor_Type: {before} Werte gefüllt")
    
    # Business_Model_Type: Default zu "Other" wenn leer
    if 'Business_Model_Type' in df.columns:
        before = df['Business_Model_Type'].isna().sum()
        df['Business_Model_Type'] = df['Business_Model_Type'].fillna('Other')
        print(f"  ✓ Business_Model_Type: {before} Werte gefüllt")
    
    return df


def print_summary(df):
    """
    Druckt Zusammenfassung des finalen Datasets.
    
    Args:
        df (pd.DataFrame): Final DataFrame
    """
    print("\n" + "="*60)
    print("FINAL DATASET ZUSAMMENFASSUNG")
    print("="*60)
    
    print(f"\nAnzahl Datenpunkte: {len(df)}")
    
    print("\nVollständigkeit pro Spalte:")
    for col in df.columns:
        total = len(df)
        non_null = df[col].notna().sum()
        percentage = (non_null / total * 100) if total > 0 else 0
        print(f"  {col:25s}: {non_null:6d} / {total:6d} ({percentage:5.1f}%)")
    
    print("\nTop 10 Industries:")
    if 'Industry' in df.columns:
        top_industries = df['Industry'].value_counts().head(10)
        for industry, count in top_industries.items():
            print(f"  {industry}: {count}")
    
    print("\nTop 10 Countries:")
    if 'Country' in df.columns:
        top_countries = df['Country'].value_counts().head(10)
        for country, count in top_countries.items():
            print(f"  {country}: {count}")
    
    print("\nBusiness Model Types:")
    if 'Business_Model_Type' in df.columns:
        bm_types = df['Business_Model_Type'].value_counts()
        for bm_type, count in bm_types.items():
            print(f"  {bm_type}: {count}")
    
    print("\nInvestor Types:")
    if 'Investor_Type' in df.columns:
        inv_types = df['Investor_Type'].value_counts()
        for inv_type, count in inv_types.items():
            print(f"  {inv_type}: {count}")
    
    print("\nJahresverteilung:")
    if 'Year' in df.columns:
        year_dist = df['Year'].value_counts().sort_index(ascending=False).head(10)
        for year, count in year_dist.items():
            print(f"  {year}: {count}")


def main():
    """Hauptfunktion: Orchestriert Merge, Clean & Enrich Prozess."""
    print("="*60)
    print("MERGE, CLEAN & ENRICH")
    print("="*60)
    
    try:
        # 1. Datasets laden
        kaggle_df, vclense_df, yc_df = load_datasets()
        
        # 2. Alle normalisieren
        print("\nNormalisiere Spalten...")
        dfs = []
        for name, df in [('Kaggle', kaggle_df), ('VCLense', vclense_df), ('YC', yc_df)]:
            if not df.empty:
                normalized = normalize_columns(df)
                dfs.append(normalized)
                print(f"  ✓ {name}: {len(normalized)} Zeilen normalisiert")
        
        if not dfs:
            print("✗ Keine Daten zum Mergen vorhanden!")
            return
        
        # 3. Zusammenführen
        print("\nFühre Datasets zusammen...")
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"  ✓ Kombiniert: {len(combined_df)} Zeilen")
        
        # 4. Daten anreichern
        enriched_df = enrich_data(combined_df)
        
        # 5. Deduplizieren
        deduped_df = deduplicate(enriched_df)
        
        # 6. Fehlende Werte füllen
        final_df = fill_missing_strategically(deduped_df)
        
        # 7. Nur Zeilen mit Startup_Name behalten
        final_df = final_df[final_df['Startup_Name'].notna()]
        print(f"\n✓ Final: {len(final_df)} Zeilen (nach Entfernung leerer Namen)")
        
        # 8. Speichern
        output_path = './data/final_dataset.csv'
        final_df.to_csv(output_path, index=False)
        print(f"\n✓ Gespeichert: {output_path}")
        
        # 9. Summary
        print_summary(final_df)
        
        # 10. Beispieldaten
        print("\n" + "="*60)
        print("BEISPIELDATEN (erste 5 Zeilen)")
        print("="*60)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(final_df.head(5).to_string())
        
        print("\n✓ ERFOLGREICH ABGESCHLOSSEN")
        
        if len(final_df) < 1000:
            print(f"\n⚠ WARNUNG: Nur {len(final_df)} Datenpunkte (Ziel: 1000+)")
            print("  Mögliche Gründe:")
            print("  - VCLense/YC Scraping hat nicht funktioniert")
            print("  - Websites haben sich geändert")
            print("  Tipp: Kaggle Dataset alleine sollte bereits >1000 Zeilen liefern")
        
    except Exception as e:
        print(f"\n✗ FEHLER: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
