#!/usr/bin/env python3
"""
Daten-Bereinigung für Schweizer Startup-Daten
Korrigiert Industry/Business Model Vermischung und extrahiert echte Industries
"""

import pandas as pd
import re
from collections import Counter

def extract_tech_keywords(text):
    """Extrahiert strukturierte Tech-Keywords aus Text"""
    if pd.isna(text):
        return ""
    
    text = str(text).upper()
    
    # Tech-Keyword Dictionary
    tech_keywords = {
        'AI': ['AI', 'ARTIFICIAL INTELLIGENCE', 'MACHINE LEARNING', 'ML', 'DEEP LEARNING', 'NEURAL NETWORK'],
        'SaaS': ['SAAS', 'SOFTWARE AS A SERVICE', 'CLOUD SOFTWARE', 'PLATFORM'],
        'Biotech': ['BIOTECH', 'BIOTECHNOLOGY', 'GENOMICS', 'RNA', 'DNA', 'GENE', 'CELL', 'PROTEIN'],
        'Fintech': ['FINTECH', 'PAYMENT', 'BANKING', 'CRYPTO', 'BLOCKCHAIN', 'DIGITAL WALLET'],
        'E-Commerce': ['E-COMMERCE', 'ECOMMERCE', 'ONLINE SHOP', 'MARKETPLACE', 'RETAIL'],
        'IoT': ['IOT', 'INTERNET OF THINGS', 'SENSOR', 'SMART DEVICE'],
        'Mobility': ['MOBILITY', 'TRANSPORT', 'VEHICLE', 'AUTONOMOUS', 'ELECTRIC VEHICLE', 'EV'],
        'Healthtech': ['HEALTH', 'MEDICAL', 'DIAGNOSIS', 'THERAPY', 'PATIENT', 'CLINICAL'],
        'Cleantech': ['CLEAN', 'RENEWABLE', 'ENERGY', 'SOLAR', 'CARBON', 'SUSTAINABILITY', 'CLIMATE'],
        'Robotics': ['ROBOT', 'AUTOMATION', 'DRONE'],
        'AR/VR': ['AR', 'VR', 'AUGMENTED REALITY', 'VIRTUAL REALITY', 'XR'],
        'Cloud': ['CLOUD', 'AWS', 'AZURE', 'INFRASTRUCTURE'],
        'Cybersecurity': ['SECURITY', 'CYBER', 'ENCRYPTION', 'PRIVACY'],
        'Analytics': ['ANALYTICS', 'DATA', 'BIG DATA', 'INSIGHTS'],
        'EdTech': ['EDUCATION', 'LEARNING', 'EDTECH', 'TRAINING'],
        'PropTech': ['PROPTECH', 'REAL ESTATE', 'PROPERTY'],
        'AgTech': ['AGTECH', 'AGRICULTURE', 'FARMING', 'FOOD TECH'],
        'Manufacturing': ['MANUFACTURING', 'PRODUCTION', 'FACTORY', 'INDUSTRIAL'],
        'Logistics': ['LOGISTICS', 'SUPPLY CHAIN', 'DELIVERY', 'WAREHOUSE']
    }
    
    found_keywords = []
    for keyword, patterns in tech_keywords.items():
        if any(pattern in text for pattern in patterns):
            found_keywords.append(keyword)
    
    return ', '.join(found_keywords) if found_keywords else ""

def derive_industry_from_keywords(tech_kw, current_industry):
    """Leitet echte Industry aus Tech Keywords ab"""
    
    # Wenn bereits eine gültige Industry vorhanden (nicht B2B/CONSUMER), behalte sie
    valid_industries = ['HEALTHCARE', 'MOBILITY', 'CLEANTECH', 'FINTECH', 'INDUSTRIALS', 
                       'AGTECH', 'AEROSPACE', 'EDUCATION']
    
    if current_industry in valid_industries:
        return current_industry
    
    if pd.isna(tech_kw) or tech_kw == "":
        # Fallback: verwende aktuelle Industry (auch wenn B2B)
        return current_industry if pd.notna(current_industry) else "UNKNOWN"
    
    tech_kw_str = str(tech_kw).upper()
    
    # Industry-Mapping basierend auf Keywords
    industry_mapping = {
        'HEALTHCARE': ['HEALTH', 'BIOTECH', 'MEDICAL', 'PATIENT', 'CLINICAL', 'THERAPY', 'DIAGNOSIS'],
        'FINTECH': ['FINTECH', 'PAYMENT', 'BANKING', 'CRYPTO', 'BLOCKCHAIN'],
        'MOBILITY': ['MOBILITY', 'TRANSPORT', 'VEHICLE', 'AUTONOMOUS', 'ELECTRIC VEHICLE'],
        'CLEANTECH': ['CLEANTECH', 'CLEAN', 'RENEWABLE', 'ENERGY', 'SOLAR', 'CARBON', 'CLIMATE'],
        'AGTECH': ['AGTECH', 'AGRICULTURE', 'FARMING', 'FOOD'],
        'AEROSPACE': ['AEROSPACE', 'SPACE', 'SATELLITE', 'AVIATION'],
        'EDUCATION': ['EDUCATION', 'EDTECH', 'LEARNING', 'TRAINING'],
        'PROPTECH': ['PROPTECH', 'REAL ESTATE', 'PROPERTY'],
        'CYBERSECURITY': ['SECURITY', 'CYBER', 'ENCRYPTION', 'PRIVACY'],
        'E-COMMERCE': ['E-COMMERCE', 'ECOMMERCE', 'MARKETPLACE', 'RETAIL', 'ONLINE SHOP'],
        'SAAS': ['SAAS', 'SOFTWARE AS A SERVICE', 'CLOUD SOFTWARE'],
        'AI/ML': ['AI', 'ARTIFICIAL INTELLIGENCE', 'MACHINE LEARNING', 'DEEP LEARNING'],
        'INDUSTRIALS': ['MANUFACTURING', 'PRODUCTION', 'FACTORY', 'INDUSTRIAL', 'SUPPLY CHAIN', 'LOGISTICS'],
    }
    
    # Finde passende Industry
    for industry, keywords in industry_mapping.items():
        if any(keyword in tech_kw_str for keyword in keywords):
            return industry
    
    # Wenn nichts gefunden, prüfe ob SaaS-Patterns
    if any(word in tech_kw_str for word in ['PLATFORM', 'SOFTWARE', 'CLOUD', 'SAAS']):
        return 'SAAS'
    
    # Fallback auf B2B nur wenn wirklich nichts passt
    return current_industry if pd.notna(current_industry) else "B2B"

def extract_business_model(current_industry, tech_kw):
    """Extrahiert Business Model aus aktuellem Industry-Feld oder Context"""
    
    # Wenn aktuelles Industry = B2B/B2C/CONSUMER, nutze das als Business Model (KLAR!)
    if pd.notna(current_industry):
        industry_str = str(current_industry).upper()
        if industry_str == 'B2B':  # Nur wenn explizit "B2B" als Industry
            return 'B2B'
        if 'B2C' in industry_str or industry_str == 'CONSUMER':  # Explizit B2C/Consumer
            return 'B2C'
    
    # Leite aus Keywords ab - NUR wenn KLAR
    if pd.notna(tech_kw):
        tech_str = str(tech_kw).upper()
        
        # B2C Indicators (sehr spezifisch)
        b2c_keywords = ['CONSUMER', 'RETAIL', 'E-COMMERCE', 'ECOMMERCE', 'MARKETPLACE', 'SHOP', 'DIRECT-TO-CONSUMER', 'D2C']
        if any(kw in tech_str for kw in b2c_keywords):
            return 'B2C'
        
        # B2B Indicators (sehr spezifisch - nur eindeutige Enterprise-Begriffe)
        b2b_keywords = ['ENTERPRISE', 'B2B', 'CORPORATE']
        if any(kw in tech_str for kw in b2b_keywords):
            return 'B2B'
        
        # SaaS ist fast immer B2B (Platform-as-a-Service für Unternehmen)
        if 'SAAS' in tech_str or 'SOFTWARE AS A SERVICE' in tech_str:
            return 'B2B'
    
    # Default: Unknown (wenn nicht eindeutig identifizierbar)
    # Healthcare, Mobility, Fintech, AI/ML können beides sein - daher Unknown
    return 'Unknown'

def clean_swiss_data():
    """Hauptfunktion zur Datenbereinigung"""
    
    print("="*80)
    print("🧹 SCHWEIZER STARTUP-DATEN BEREINIGUNG")
    print("="*80)
    
    # Lade Daten
    print("\n📂 Lade schweiz_2020_2026.csv...")
    df = pd.read_csv('data/schweiz_2020_2026.csv')
    print(f"   ✓ {len(df)} Einträge geladen")
    
    # Backup erstellen
    print("\n💾 Erstelle Backup...")
    df.to_csv('data/schweiz_2020_2026_backup.csv', index=False)
    print("   ✓ Backup gespeichert als schweiz_2020_2026_backup.csv")
    
    # ========================================================================
    # 1. EXTRAHIERE STRUKTURIERTE TECH KEYWORDS
    # ========================================================================
    print("\n" + "="*80)
    print("1️⃣ EXTRAHIERE STRUKTURIERTE TECH KEYWORDS")
    print("="*80)
    
    print("\n   Verarbeite Tech_Keywords...")
    df['Tech_Keywords_Original'] = df['Tech_Keywords']
    df['Tech_Keywords_Clean'] = df['Tech_Keywords_Original'].apply(extract_tech_keywords)
    
    cleaned_count = df['Tech_Keywords_Clean'].notna().sum()
    print(f"   ✓ {cleaned_count}/{len(df)} Einträge haben strukturierte Keywords")
    
    # Zeige Beispiele
    print("\n   📋 Vorher/Nachher Beispiele:")
    sample = df[df['Tech_Keywords_Clean'] != ""].head(3)
    for idx, row in sample.iterrows():
        print(f"\n   • {row['Startup_Name']}:")
        print(f"     Vorher: {str(row['Tech_Keywords_Original'])[:60]}...")
        print(f"     Nachher: {row['Tech_Keywords_Clean']}")
    
    # ========================================================================
    # 2. KORRIGIERE INDUSTRY-FELD
    # ========================================================================
    print("\n" + "="*80)
    print("2️⃣ KORRIGIERE INDUSTRY-FELD (Entferne B2B, füge echte Industries ein)")
    print("="*80)
    
    print("\n   Analysiere und korrigiere Industry...")
    df['Industry_Original'] = df['Industry']
    df['Industry_New'] = df.apply(
        lambda row: derive_industry_from_keywords(row['Tech_Keywords_Original'], row['Industry_Original']),
        axis=1
    )
    
    # Statistik
    b2b_before = (df['Industry_Original'] == 'B2B').sum()
    b2b_after = (df['Industry_New'] == 'B2B').sum()
    
    print(f"\n   📊 Ergebnis:")
    print(f"   • B2B vorher: {b2b_before} ({b2b_before/len(df)*100:.1f}%)")
    print(f"   • B2B nachher: {b2b_after} ({b2b_after/len(df)*100:.1f}%)")
    print(f"   • Korrigiert: {b2b_before - b2b_after} Einträge")
    
    # Neue Industry-Verteilung
    print(f"\n   📊 Neue Industry-Verteilung:")
    for ind, count in df['Industry_New'].value_counts().head(10).items():
        marker = "✅" if ind != 'B2B' else "⚠️"
        print(f"   {marker} {ind}: {count} ({count/len(df)*100:.1f}%)")
    
    # Zeige Beispiele von Korrekturen
    print("\n   📋 Beispiele von Korrekturen:")
    corrected = df[df['Industry_Original'] != df['Industry_New']].head(5)
    for idx, row in corrected.iterrows():
        print(f"\n   • {row['Startup_Name']}:")
        print(f"     Vorher: {row['Industry_Original']}")
        print(f"     Nachher: {row['Industry_New']} ✅")
        if pd.notna(row['Tech_Keywords_Clean']):
            print(f"     Keywords: {row['Tech_Keywords_Clean']}")
    
    # ========================================================================
    # 3. BEFÜLLE BUSINESS_MODEL_TYPE
    # ========================================================================
    print("\n" + "="*80)
    print("3️⃣ BEFÜLLE BUSINESS_MODEL_TYPE FELD")
    print("="*80)
    
    print("\n   Extrahiere Business Models...")
    df['Business_Model_Type'] = df.apply(
        lambda row: extract_business_model(row['Industry_Original'], row['Tech_Keywords_Original']),
        axis=1
    )
    
    print(f"\n   📊 Business Model Verteilung:")
    for bm, count in df['Business_Model_Type'].value_counts().items():
        print(f"   • {bm}: {count} ({count/len(df)*100:.1f}%)")
    
    # ========================================================================
    # 4. ERSETZE ALTE FELDER MIT NEUEN
    # ========================================================================
    print("\n" + "="*80)
    print("4️⃣ FINALISIERE BEREINIGTE DATEN")
    print("="*80)
    
    # Ersetze alte Werte mit neuen
    df['Industry'] = df['Industry_New']
    df['Tech_Keywords'] = df['Tech_Keywords_Clean']
    
    # Entferne temporäre Spalten
    df = df.drop(columns=['Industry_Original', 'Industry_New', 'Tech_Keywords_Original', 'Tech_Keywords_Clean'])
    
    # ========================================================================
    # 5. EXPORTIERE BEREINIGTE DATEN
    # ========================================================================
    print("\n" + "="*80)
    print("5️⃣ EXPORTIERE BEREINIGTE DATEN")
    print("="*80)
    
    # Sortiere nach Jahr (neueste zuerst) und Name
    df = df.sort_values(['Year', 'Startup_Name'], ascending=[False, True])
    
    # Exportiere
    output_file = 'data/schweiz_2020_2026_clean.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n   ✅ Bereinigte Daten exportiert:")
    print(f"   • Datei: {output_file}")
    print(f"   • Zeilen: {len(df)}")
    print(f"   • Spalten: {len(df.columns)}")
    
    # Überschreibe auch die Original-Datei
    df.to_csv('data/schweiz_2020_2026.csv', index=False)
    print(f"\n   ✅ Original-Datei überschrieben:")
    print(f"   • schweiz_2020_2026.csv aktualisiert")
    
    # ========================================================================
    # 6. ZUSAMMENFASSUNG
    # ========================================================================
    print("\n" + "="*80)
    print("📊 BEREINIGUNG ABGESCHLOSSEN!")
    print("="*80)
    
    print(f"""
    ✅ DURCHGEFÜHRTE KORREKTUREN:
    
    1. Tech Keywords strukturiert
       • Vorher: Artikel-Texte (Ø 104 Zeichen)
       • Nachher: Strukturierte Keywords (AI, SaaS, Biotech, etc.)
       • Coverage: {(df['Tech_Keywords'].notna().sum() / len(df) * 100):.1f}%
    
    2. Industry korrigiert
       • B2B-Einträge reduziert: {b2b_before} → {b2b_after}
       • Echte Industries extrahiert: {len(df['Industry'].unique())} Kategorien
       • Top Industry: {df['Industry'].value_counts().index[0]} ({df['Industry'].value_counts().iloc[0]} Einträge)
    
    3. Business_Model_Type befüllt
       • Vorher: 0% gefüllt
       • Nachher: 100% gefüllt
       • B2B: {(df['Business_Model_Type'] == 'B2B').sum()} ({(df['Business_Model_Type'] == 'B2B').sum() / len(df) * 100:.1f}%)
       • B2C: {(df['Business_Model_Type'] == 'B2C').sum()} ({(df['Business_Model_Type'] == 'B2C').sum() / len(df) * 100:.1f}%)
    
    📁 DATEIEN:
    • Original (überschrieben): data/schweiz_2020_2026.csv
    • Bereinigt (neu): data/schweiz_2020_2026_clean.csv
    • Backup (Sicherheit): data/schweiz_2020_2026_backup.csv
    
    🎯 NÄCHSTE SCHRITTE:
    1. Prüfe schweiz_2020_2026_clean.csv in Excel/Numbers
    2. Validiere Industry-Kategorisierung
    3. Analysiere Business Model Verteilung
    4. Verwende für deine MBI-Analyse!
    """)

if __name__ == "__main__":
    clean_swiss_data()
