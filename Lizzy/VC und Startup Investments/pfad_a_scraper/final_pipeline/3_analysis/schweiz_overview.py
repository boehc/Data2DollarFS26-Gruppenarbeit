#!/usr/bin/env python3
"""
Schweiz-Fokus: Kombinierte Übersicht aller Schweizer Startups
Quellen: Kaggle Crunchbase, Y Combinator Europa, Startupticker, Venturekick
"""

import pandas as pd
import os

# Pfade zu den Datenquellen
DATA_DIR = "data"
SOURCES = {
    "Kaggle Crunchbase": "kaggle_crunchbase.csv",
    "Y Combinator": "yc_companies.csv",
    "Startupticker": "startupticker_startups.csv",
    "Venturekick": "venturekick_startups.csv"
}

def load_swiss_startups(year_filter=2020):
    """Lädt alle Schweizer Startups aus allen Quellen, optional mit Jahr-Filter"""
    all_swiss = []
    
    for source_name, filename in SOURCES.items():
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️ Datei nicht gefunden: {filename}")
            continue
        
        print(f"\n📂 Lade {source_name}...")
        df = pd.read_csv(filepath)
        
        # Harmonisiere Spaltennamen:
        # Investors → Investor_Names
        # Investor_Name → Investor_Names (YC verwendet singular)
        if 'Investors' in df.columns and 'Investor_Names' not in df.columns:
            df = df.rename(columns={'Investors': 'Investor_Names'})
        if 'Investor_Name' in df.columns and 'Investor_Names' not in df.columns:
            df = df.rename(columns={'Investor_Name': 'Investor_Names'})
        
        # Filtere nur Schweizer Startups (Country = Switzerland oder CH)
        swiss_mask = df['Country'].fillna('').str.contains('Switzerland|Schweiz|CH', case=False, na=False)
        swiss_df = df[swiss_mask].copy()
        
        # Jahr-Filter anwenden (nur >= 2020)
        if year_filter and 'Year' in swiss_df.columns:
            before_filter = len(swiss_df)
            swiss_df = swiss_df[swiss_df['Year'] >= year_filter].copy()
            print(f"   ✓ {len(swiss_df)} Schweizer Startups gefunden (>= {year_filter})")
            print(f"   ⏭️  {before_filter - len(swiss_df)} veraltete Einträge übersprungen")
        else:
            print(f"   ✓ {len(swiss_df)} Schweizer Startups gefunden")
        
        # Füge Datenquelle als Spalte hinzu
        swiss_df['Data_Source'] = source_name
        
        all_swiss.append(swiss_df)
    
    # Kombiniere alle Schweizer Startups
    combined = pd.concat(all_swiss, ignore_index=True)
    return combined

def analyze_swiss_data(df):
    """Analysiert die Schweizer Startup-Daten"""
    print("\n" + "="*80)
    print("🇨🇭 SCHWEIZER STARTUPS - FOKUS 2020-2026 (AKTUELLE DATEN)")
    print("="*80)
    
    # 1. Gesamtzahl
    print(f"\n📊 TOTAL: {len(df)} Schweizer Startups")
    
    # 2. Aufschlüsselung nach Quelle
    print("\n📁 AUFSCHLÜSSELUNG NACH DATENQUELLE:")
    source_counts = df['Data_Source'].value_counts()
    for source, count in source_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {source}: {count} Startups ({percentage:.1f}%)")
    
    # 3. Zeitliche Verteilung
    print("\n📅 ZEITLICHE VERTEILUNG:")
    year_counts = df['Year'].value_counts().sort_index()
    print(f"   Zeitraum: {int(df['Year'].min())} - {int(df['Year'].max())}")
    print(f"\n   Top 5 Jahre:")
    for year, count in year_counts.head(5).items():
        print(f"   • {int(year)}: {count} Startups")
    
    # 4. Top Industrien
    print("\n🏭 TOP 10 INDUSTRIEN:")
    industry_counts = df['Industry'].value_counts().head(10)
    for industry, count in industry_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {industry}: {count} ({percentage:.1f}%)")
    
    # 5. Investment Stages
    print("\n💰 INVESTMENT STAGES:")
    stage_counts = df['Investment_Stage'].value_counts()
    for stage, count in stage_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {stage}: {count} ({percentage:.1f}%)")
    
    # 6. Funding Amounts (nur wo vorhanden)
    funding_available = df[df['Funding_Amount'].notna()]
    print(f"\n💵 FUNDING AMOUNTS:")
    print(f"   Verfügbar: {len(funding_available)} / {len(df)} ({len(funding_available)/len(df)*100:.1f}%)")
    if len(funding_available) > 0:
        pattern = r'([\d.]+)'
        amounts = funding_available['Funding_Amount'].str.extract(pattern).astype(float)
        print(f"   Durchschnitt: {amounts.mean()[0]:.1f}K")
        print(f"   Median: {amounts.median()[0]:.1f}K")
    
    # 7. Investor Coverage
    investors_available = df[df['Investor_Names'].notna()]
    print(f"\n👥 INVESTOR INFORMATION:")
    print(f"   Verfügbar: {len(investors_available)} / {len(df)} ({len(investors_available)/len(df)*100:.1f}%)")
    print(f"\n   Nach Quelle:")
    for source in df['Data_Source'].unique():
        source_df = df[df['Data_Source'] == source]
        source_investors = source_df[source_df['Investor_Names'].notna()]
        coverage = (len(source_investors) / len(source_df)) * 100 if len(source_df) > 0 else 0
        print(f"   • {source}: {len(source_investors)}/{len(source_df)} ({coverage:.1f}%)")
    
    # 8. Top Cities (falls verfügbar)
    if 'City' in df.columns:
        print("\n🏙️ TOP 10 SCHWEIZER STÄDTE:")
        city_counts = df['City'].value_counts().head(10)
        for city, count in city_counts.items():
            percentage = (count / len(df)) * 100
            print(f"   • {city}: {count} ({percentage:.1f}%)")
    else:
        print("\n🏙️ STÄDTE-INFORMATIONEN: Nicht in allen Quellen verfügbar")
    
    # 9. Datenqualität pro Feld
    print("\n✅ DATENQUALITÄT (Vollständigkeit pro Feld):")
    completeness = {}
    for col in df.columns:
        if col != 'Data_Source':
            non_empty = df[col].notna().sum()
            completeness[col] = (non_empty / len(df)) * 100
    
    for col, pct in sorted(completeness.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {col}: {pct:.1f}%")
    
    # 10. Recent Activity (2020-2026)
    recent_df = df[df['Year'] >= 2020]
    print(f"\n🔥 AKTUELLE STARTUPS (2020-2026):")
    print(f"   Total: {len(recent_df)} Startups")
    print(f"   Verteilung:")
    for year in sorted(recent_df['Year'].unique(), reverse=True):
        year_count = len(recent_df[recent_df['Year'] == year])
        print(f"   • {int(year)}: {year_count} Startups")

def export_combined_swiss(df):
    """Exportiert die kombinierte Schweiz-Übersicht als CSV"""
    output_file = os.path.join(DATA_DIR, "schweiz_2020_2026.csv")
    
    # Sortiere nach Jahr (neueste zuerst) und dann alphabetisch
    df_sorted = df.sort_values(['Year', 'Startup_Name'], ascending=[False, True])
    
    # Exportiere
    df_sorted.to_csv(output_file, index=False)
    print(f"\n💾 EXPORT ERFOLGREICH:")
    print(f"   Datei: {output_file}")
    print(f"   Zeilen: {len(df_sorted)}")
    print(f"   Spalten: {len(df_sorted.columns)}")
    
    return output_file

def show_sample_data(df, n=10):
    """Zeigt Beispieldaten aus jeder Quelle"""
    print("\n" + "="*80)
    print("📋 BEISPIEL-DATEN (je 3 Startups pro Quelle)")
    print("="*80)
    
    for source in df['Data_Source'].unique():
        source_df = df[df['Data_Source'] == source].head(3)
        print(f"\n🔹 {source}:")
        for idx, row in source_df.iterrows():
            print(f"\n   Startup: {row['Startup_Name']}")
            print(f"   Jahr: {int(row['Year']) if pd.notna(row['Year']) else 'N/A'}")
            print(f"   Industrie: {row['Industry']}")
            if 'City' in row.index and pd.notna(row['City']):
                print(f"   Stadt: {row['City']}")
            if pd.notna(row['Funding_Amount']):
                print(f"   Funding: {row['Funding_Amount']}")
            if pd.notna(row['Investor_Names']):
                print(f"   Investoren: {row['Investor_Names'][:100]}...")

if __name__ == "__main__":
    print("🇨🇭 SCHWEIZER STARTUP ANALYSE - FOKUS 2020-2026")
    print("="*80)
    
    # Lade alle Schweizer Startups (nur ab 2020)
    swiss_df = load_swiss_startups(year_filter=2020)
    
    # Analysiere die Daten
    analyze_swiss_data(swiss_df)
    
    # Zeige Beispieldaten
    show_sample_data(swiss_df)
    
    # Exportiere kombinierte Daten
    export_file = export_combined_swiss(swiss_df)
    
    print("\n" + "="*80)
    print("✅ ANALYSE ABGESCHLOSSEN!")
    print("="*80)
    print(f"\n📊 Nächste Schritte:")
    print(f"   1. Öffne {export_file} in Excel/Numbers")
    print(f"   2. Prüfe Duplikate (gleicher Name, gleiches Jahr)")
    print(f"   3. Analysiere Investor-Netzwerk (deutlich höhere Coverage!)")
    print(f"   4. Identifiziere aktuelle Trends 2024-2026")
