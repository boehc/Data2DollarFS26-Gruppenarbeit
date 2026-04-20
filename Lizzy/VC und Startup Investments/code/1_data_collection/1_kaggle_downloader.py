"""
Kaggle Dataset Downloader
Lädt Crunchbase Startup Investment Daten via Kaggle API herunter.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

# Environment Variables laden
load_dotenv()


def check_kaggle_credentials():
    """
    Prüft ob Kaggle Credentials vorhanden sind.
    
    Returns:
        bool: True wenn Credentials gefunden wurden
    """
    # Option 1: .env Datei
    username = os.getenv('KAGGLE_USERNAME')
    key = os.getenv('KAGGLE_KEY')
    
    if username and key:
        os.environ['KAGGLE_USERNAME'] = username
        os.environ['KAGGLE_KEY'] = key
        print("✓ Kaggle Credentials aus .env geladen")
        return True
    
    # Option 2: kaggle.json
    kaggle_json = Path.home() / '.kaggle' / 'kaggle.json'
    if kaggle_json.exists():
        print(f"✓ Kaggle Credentials gefunden in {kaggle_json}")
        return True
    
    print("✗ FEHLER: Keine Kaggle Credentials gefunden!")
    print("Bitte .env Datei erstellen oder kaggle.json in ~/.kaggle/ platzieren")
    print("Siehe README.md für Details")
    return False


def download_dataset():
    """
    Lädt den Crunchbase Startup Investment Dataset von Kaggle herunter.
    
    Returns:
        Path: Pfad zur heruntergeladenen CSV Datei
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        print("Initialisiere Kaggle API...")
        api = KaggleApi()
        api.authenticate()
        
        dataset_name = 'arindam235/startup-investments-crunchbase'
        download_path = './data'
        
        print(f"Lade Dataset herunter: {dataset_name}")
        print("Dies kann einige Minuten dauern...")
        
        # Dataset herunterladen
        api.dataset_download_files(
            dataset_name,
            path=download_path,
            unzip=True
        )
        
        print(f"✓ Download erfolgreich nach {download_path}")
        
        # Finde die heruntergeladene CSV (Original-Datei, nicht die konvertierte)
        data_dir = Path(download_path)
        
        # Suche nach investments_VC.csv (Original-Datei)
        original_csv = data_dir / 'investments_VC.csv'
        if original_csv.exists():
            return original_csv
        
        # Fallback: finde beliebige CSV außer kaggle_crunchbase.csv
        csv_files = [f for f in data_dir.glob('*.csv') if f.name != 'kaggle_crunchbase.csv']
        
        if not csv_files:
            raise FileNotFoundError("Keine CSV Datei im Download gefunden")
        
        return csv_files[0]
        
    except Exception as e:
        print(f"✗ Fehler beim Download: {e}")
        raise


def map_to_schema(df):
    """
    Mappt Crunchbase Spalten zu unserem Schema.
    
    Args:
        df (pd.DataFrame): Original Crunchbase DataFrame
        
    Returns:
        pd.DataFrame: Gemappter DataFrame
    """
    print("Mappe Spalten zu unserem Schema...")
    
    # Mapping Dictionary
    column_mapping = {
        'name': 'Startup_Name',
        'company_name': 'Startup_Name',
        'category_list': 'Industry',
        'category_code': 'Sub_Industry',
        'market ': 'Sub_Industry',  # Spalte mit Leerzeichen
        'country_code': 'Country',
        'founded_year': 'Founding_Year',
        ' funding_total_usd ': 'Funding_Amount',  # Spalte mit Leerzeichen
        'funding_total_usd': 'Funding_Amount',
        'funding_rounds': 'Funding_Round',
        'status': 'Exit_Type',
        'raised_amount_usd': 'Funding_Amount',
    }
    
    # Verfügbare Spalten anzeigen
    print(f"Verfügbare Spalten im Dataset: {df.columns.tolist()}")
    
    # Neue DataFrame mit gemappten Spalten erstellen
    mapped_df = pd.DataFrame()
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            mapped_df[new_col] = df[old_col]
    
    # Tech_Keywords aus category_list extrahieren
    if 'Industry' in mapped_df.columns:
        mapped_df['Tech_Keywords'] = mapped_df['Industry']
    
    # Year aus Founding_Year ableiten wenn möglich
    if 'Founding_Year' in mapped_df.columns:
        mapped_df['Year'] = mapped_df['Founding_Year']
    
    # Startup_Stage aus Exit_Type ableiten
    if 'Exit_Type' in mapped_df.columns:
        def derive_stage(status):
            if pd.isna(status):
                return 'Operating'
            status_lower = str(status).lower()
            if 'acquired' in status_lower:
                return 'Acquired'
            elif 'ipo' in status_lower:
                return 'IPO'
            elif 'closed' in status_lower:
                return 'Closed'
            else:
                return 'Operating'
        
        mapped_df['Startup_Stage'] = mapped_df['Exit_Type'].apply(derive_stage)
    
    # Fehlende Spalten mit NaN initialisieren
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Name', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    for col in required_columns:
        if col not in mapped_df.columns:
            mapped_df[col] = None
    
    # Spalten in korrekter Reihenfolge
    mapped_df = mapped_df[required_columns]
    
    print(f"✓ Gemappt: {len(mapped_df)} Zeilen")
    return mapped_df


def main():
    """Hauptfunktion: Orchestriert den Download und Mapping Prozess."""
    print("="*60)
    print("KAGGLE DATASET DOWNLOADER")
    print("="*60)
    
    # 1. Credentials prüfen
    if not check_kaggle_credentials():
        sys.exit(1)
    
    # 2. Data Ordner erstellen
    Path('./data').mkdir(exist_ok=True)
    
    try:
        # 3. Dataset herunterladen
        csv_path = download_dataset()
        print(f"CSV Datei: {csv_path}")
        
        # 4. CSV laden
        print("Lade CSV Datei...")
        df = pd.read_csv(csv_path, low_memory=False, encoding='latin-1')
        print(f"✓ Geladen: {len(df)} Zeilen, {len(df.columns)} Spalten")
        
        # 5. Zu unserem Schema mappen
        mapped_df = map_to_schema(df)
        
        # 6. Speichern
        output_path = './data/kaggle_crunchbase.csv'
        mapped_df.to_csv(output_path, index=False)
        print(f"✓ Gespeichert: {output_path}")
        
        # 7. Summary
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Anzahl Datenpunkte: {len(mapped_df)}")
        print(f"Vollständigkeit pro Spalte:")
        for col in mapped_df.columns:
            completeness = (mapped_df[col].notna().sum() / len(mapped_df)) * 100
            print(f"  {col}: {completeness:.1f}%")
        
        print("\n✓ ERFOLGREICH ABGESCHLOSSEN")
        
    except Exception as e:
        print(f"\n✗ FEHLER: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
