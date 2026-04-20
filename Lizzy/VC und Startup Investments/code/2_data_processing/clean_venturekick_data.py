"""
Venturekick Data Cleaning Script
Verbessert Datenqualität durch:
1. Tech_Keywords → Industry Mapping (für Unknown Industries)
2. Industry → Business Model Inference (für Unknown Business Models)
3. Tech_Keywords → Sub_Industry Mapping
"""

import pandas as pd
from pathlib import Path


def tech_keywords_to_industry(tech_keywords):
    """
    Mappt Tech_Keywords zu Industry, wenn Industry = Unknown.
    Prioritäts-basiert (spezifischere Keywords zuerst).
    """
    if pd.isna(tech_keywords) or tech_keywords == '':
        return None
    
    keywords_upper = tech_keywords.upper()
    
    # Priorität 1: Spezifische Tech-Branchen
    if 'BIOTECH' in keywords_upper:
        return 'HEALTHCARE'
    if 'HEALTHTECH' in keywords_upper:
        return 'HEALTHCARE'
    if 'FINTECH' in keywords_upper:
        return 'FINTECH'
    if 'CLEANTECH' in keywords_upper:
        return 'CLEANTECH'
    
    # Priorität 2: Tech-Kategorien
    if 'AI' in keywords_upper or 'MACHINE LEARNING' in keywords_upper:
        return 'AI/ML'
    if 'SAAS' in keywords_upper:
        return 'SOFTWARE'
    if 'ROBOTICS' in keywords_upper:
        return 'ROBOTICS'
    
    # Priorität 3: Generische Tech
    if 'IOT' in keywords_upper:
        return 'SOFTWARE'  # Default: IoT = Software
    if 'AR/VR' in keywords_upper:
        return 'SOFTWARE'  # Default: AR/VR = Software
    
    return None


def industry_to_business_model(industry, tech_keywords):
    """
    Inferiert Business Model aus Industry + Tech_Keywords,
    wenn Business_Model_Type = Unknown.
    """
    if pd.isna(industry):
        return 'Unknown'
    
    # B2C Industries
    if industry in ['CONSUMER', 'EDUCATION']:
        return 'B2C'
    
    # B2B Industries (Default für Tech)
    if industry in ['AI/ML', 'SOFTWARE', 'FINTECH', 'INDUSTRIALS', 'ROBOTICS']:
        return 'B2B'
    
    # Mixed (brauchen mehr Context)
    if industry == 'HEALTHCARE':
        # Biotech/Pharma = B2B, Digital Health = B2C
        if tech_keywords and 'BIOTECH' in tech_keywords.upper():
            return 'B2B'
        return 'Unknown'
    
    if industry in ['CLEANTECH', 'MOBILITY', 'AEROSPACE', 'AGTECH']:
        return 'B2B'  # Meist Enterprise
    
    return 'Unknown'


def tech_keywords_to_sub_industry(tech_keywords, industry):
    """
    Leitet Sub_Industry aus Tech_Keywords ab, wenn Sub_Industry fehlt.
    """
    if pd.isna(tech_keywords) or tech_keywords == '' or pd.isna(industry):
        return None
    
    keywords_upper = tech_keywords.upper()
    
    # Industry-spezifische Mappings
    if industry == 'HEALTHCARE':
        if 'BIOTECH' in keywords_upper:
            return 'Biotech'
        if 'HEALTHTECH' in keywords_upper:
            return 'Digital Health'
    
    if industry == 'AI/ML':
        return 'AI/ML'
    
    if industry == 'SOFTWARE':
        if 'SAAS' in keywords_upper:
            return 'SaaS'
        if 'IOT' in keywords_upper:
            return 'IoT'
        if 'AR/VR' in keywords_upper:
            return 'AR/VR'
    
    if industry == 'FINTECH':
        if 'CRYPTO' in keywords_upper or 'BLOCKCHAIN' in keywords_upper:
            return 'Crypto'
        return 'Fintech'
    
    if industry == 'CLEANTECH':
        return 'Climate Tech'
    
    return None


def clean_venturekick_data(input_file='data/venturekick_startups.csv', 
                           output_file='data/venturekick_startups_clean.csv'):
    """Hauptfunktion: Lädt, cleaned und speichert Daten."""
    
    print("="*70)
    print("VENTUREKICK DATA CLEANING")
    print("="*70)
    
    # Lade Daten
    df = pd.read_csv(input_file)
    print(f"\n📊 Loaded: {len(df)} Startups")
    
    # Backup Original
    df_original = df.copy()
    
    # STEP 1: Tech_Keywords → Industry (für Unknown)
    print("\n🔧 STEP 1: Fill Unknown Industries from Tech_Keywords")
    unknown_industry = df['Industry'] == 'Unknown'
    print(f"   Unknown Industries: {unknown_industry.sum()}")
    
    df.loc[unknown_industry, 'Industry_Inferred'] = df.loc[unknown_industry, 'Tech_Keywords'].apply(tech_keywords_to_industry)
    filled_industry = df['Industry_Inferred'].notna()
    
    # Überschreibe Unknown mit Inferred
    df.loc[unknown_industry & filled_industry, 'Industry'] = df.loc[unknown_industry & filled_industry, 'Industry_Inferred']
    
    improved = (df_original['Industry'] == 'Unknown') & (df['Industry'] != 'Unknown')
    print(f"   ✅ Improved: {improved.sum()} Industries")
    print(f"   Remaining Unknown: {(df['Industry'] == 'Unknown').sum()}")
    
    # STEP 2: Industry → Business Model (für Unknown)
    print("\n🔧 STEP 2: Infer Business Model from Industry")
    unknown_bm = df['Business_Model_Type'] == 'Unknown'
    print(f"   Unknown Business Models: {unknown_bm.sum()}")
    
    df.loc[unknown_bm, 'Business_Model_Inferred'] = df.loc[unknown_bm].apply(
        lambda row: industry_to_business_model(row['Industry'], row['Tech_Keywords']), 
        axis=1
    )
    filled_bm = (df['Business_Model_Inferred'].notna()) & (df['Business_Model_Inferred'] != 'Unknown')
    
    # Überschreibe Unknown mit Inferred
    df.loc[unknown_bm & filled_bm, 'Business_Model_Type'] = df.loc[unknown_bm & filled_bm, 'Business_Model_Inferred']
    
    improved_bm = (df_original['Business_Model_Type'] == 'Unknown') & (df['Business_Model_Type'] != 'Unknown')
    print(f"   ✅ Improved: {improved_bm.sum()} Business Models")
    print(f"   Remaining Unknown: {(df['Business_Model_Type'] == 'Unknown').sum()}")
    
    # STEP 3: Tech_Keywords → Sub_Industry (wenn leer)
    print("\n🔧 STEP 3: Fill Sub_Industry from Tech_Keywords")
    missing_sub = df['Sub_Industry'].isna() | (df['Sub_Industry'] == '')
    print(f"   Missing Sub_Industry: {missing_sub.sum()}")
    
    df.loc[missing_sub, 'Sub_Industry_Inferred'] = df.loc[missing_sub].apply(
        lambda row: tech_keywords_to_sub_industry(row['Tech_Keywords'], row['Industry']), 
        axis=1
    )
    filled_sub = df['Sub_Industry_Inferred'].notna()
    
    # Überschreibe leere Sub_Industry
    df.loc[missing_sub & filled_sub, 'Sub_Industry'] = df.loc[missing_sub & filled_sub, 'Sub_Industry_Inferred']
    
    improved_sub = (df_original['Sub_Industry'].isna() | (df_original['Sub_Industry'] == '')) & df['Sub_Industry'].notna()
    print(f"   ✅ Improved: {improved_sub.sum()} Sub_Industries")
    print(f"   Remaining Missing: {(df['Sub_Industry'].isna() | (df['Sub_Industry'] == '')).sum()}")
    
    # CLEANUP: Remove helper columns
    df = df.drop(columns=['Industry_Inferred', 'Business_Model_Inferred', 'Sub_Industry_Inferred'], errors='ignore')
    
    # ZUSAMMENFASSUNG
    print("\n" + "="*70)
    print("📈 VERBESSERUNGEN:")
    print("="*70)
    
    print(f"\n{'Feld':<25s} {'Vorher':>10s} {'Nachher':>10s} {'Verbesserung':>15s}")
    print("-"*70)
    
    for field in ['Industry', 'Business_Model_Type', 'Sub_Industry']:
        if field in ['Industry', 'Business_Model_Type']:
            # Unknown zählen
            before = (df_original[field] == 'Unknown').sum()
            after = (df[field] == 'Unknown').sum()
            improved = before - after
            print(f"{field:<25s} {before:>10d} {after:>10d} {improved:>15d} (-{improved/before*100:.1f}%)" if before > 0 else f"{field:<25s} {before:>10d} {after:>10d}")
        else:
            # Leere zählen
            before = (df_original[field].isna() | (df_original[field] == '')).sum()
            after = (df[field].isna() | (df[field] == '')).sum()
            improved = before - after
            print(f"{field:<25s} {before:>10d} {after:>10d} {improved:>15d} (-{improved/before*100:.1f}%)" if before > 0 else f"{field:<25s} {before:>10d} {after:>10d}")
    
    # Speichere
    df.to_csv(output_file, index=False)
    print(f"\n✅ Gespeichert: {output_file}")
    
    # FINAL STATS
    print("\n" + "="*70)
    print("FINAL DATA QUALITY")
    print("="*70)
    
    for col in ['Industry', 'Business_Model_Type', 'Sub_Industry', 'Tech_Keywords', 
                'Funding_Amount', 'Investor_Names']:
        filled = (df[col].notna() & (df[col] != '')).sum()
        unknown_count = (df[col] == 'Unknown').sum() if col in ['Industry', 'Business_Model_Type'] else 0
        pct = (filled / len(df) * 100)
        status = "✅" if pct > 75 else "🟡" if pct > 50 else "🔴"
        unknown_str = f" ({unknown_count} Unknown)" if unknown_count > 0 else ""
        print(f"{status} {col:25s}: {filled:3d}/{len(df)} = {pct:5.1f}%{unknown_str}")
    
    print("="*70)
    
    return df


if __name__ == '__main__':
    clean_venturekick_data()
