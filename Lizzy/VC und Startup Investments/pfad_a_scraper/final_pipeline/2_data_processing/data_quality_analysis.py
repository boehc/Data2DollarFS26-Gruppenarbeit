#!/usr/bin/env python3
"""
In-Depth Datenqualitäts-Analyse für Schweizer Startup-Daten
Identifiziert strukturelle Fehler und Inkonsistenzen
"""

import pandas as pd
import re

def analyze_field_issues():
    """Analysiert alle Felder auf logische Fehler"""
    
    df = pd.read_csv('data/schweiz_2020_2026.csv')
    
    print("="*80)
    print("🔍 IN-DEPTH DATENQUALITÄTS-ANALYSE")
    print("="*80)
    print(f"\n📊 Dataset: {len(df)} Schweizer Startups (2020-2026)\n")
    
    # ============================================================================
    # 1. INDUSTRY vs BUSINESS_MODEL_TYPE CONFUSION
    # ============================================================================
    print("\n" + "="*80)
    print("❌ PROBLEM #1: INDUSTRY vs BUSINESS MODEL VERMISCHUNG")
    print("="*80)
    
    # B2B, B2C, B2B2C sind Business Models, NICHT Industries!
    business_models_in_industry = df[df['Industry'].str.contains('B2B|B2C|CONSUMER', case=False, na=False)]
    
    print(f"\n🚨 {len(business_models_in_industry)} Einträge haben Business Models im Industry-Feld:")
    print(f"\n   Industry-Werte die eigentlich Business Models sind:")
    for val, count in df['Industry'].value_counts().items():
        if any(x in str(val).upper() for x in ['B2B', 'B2C', 'CONSUMER']):
            print(f"   • {val}: {count} Einträge ({count/len(df)*100:.1f}%)")
    
    print(f"\n   Aktuelles Business_Model_Type Feld:")
    bm_filled = df['Business_Model_Type'].notna().sum()
    print(f"   • Vollständigkeit: {bm_filled}/{len(df)} ({bm_filled/len(df)*100:.1f}%)")
    if bm_filled > 0:
        print(f"   • Werte: {df['Business_Model_Type'].value_counts().to_dict()}")
    else:
        print(f"   • Status: ❌ KOMPLETT LEER - sollte B2B/B2C enthalten!")
    
    # Zeige Beispiele
    print(f"\n   📋 Beispiele von fehlerhaften Einträgen:")
    sample = business_models_in_industry.head(5)
    for idx, row in sample.iterrows():
        print(f"\n   • Startup: {row['Startup_Name']}")
        print(f"     Industry: {row['Industry']} ❌ (sollte echte Industry sein)")
        print(f"     Business_Model_Type: {row['Business_Model_Type']} (leer)")
        print(f"     Tech_Keywords: {str(row['Tech_Keywords'])[:60]}...")
    
    # ============================================================================
    # 2. FEHLENDE ECHTE INDUSTRIES
    # ============================================================================
    print("\n" + "="*80)
    print("❌ PROBLEM #2: FEHLENDE ECHTE INDUSTRY-KATEGORIEN")
    print("="*80)
    
    print("\n💡 Was echte Industry-Kategorien sein sollten:")
    print("   ✅ Beispiele: Fintech, Healthcare, SaaS, E-Commerce, AI/ML, Biotech, Logistics, etc.")
    print("   ❌ NICHT: B2B, B2C, Consumer (das sind Business Models!)")
    
    valid_industries = ['HEALTHCARE', 'MOBILITY', 'CLEANTECH', 'FINTECH', 'INDUSTRIALS', 
                       'AGTECH', 'AEROSPACE', 'EDUCATION']
    
    print(f"\n   Aktuelle gültige Industries: {len([i for i in df['Industry'].unique() if i in valid_industries])}/{len(df['Industry'].unique())}")
    print(f"   Ungültige/Business-Model Entries: {len(df[~df['Industry'].isin(valid_industries)])}/{len(df)}")
    
    # ============================================================================
    # 3. TECH_KEYWORDS ANALYSE
    # ============================================================================
    print("\n" + "="*80)
    print("⚠️ PROBLEM #3: TECH_KEYWORDS SIND ARTIKEL-TEXTE, KEINE KEYWORDS")
    print("="*80)
    
    tech_kw = df['Tech_Keywords'].dropna()
    print(f"\n   Vollständigkeit: {len(tech_kw)}/{len(df)} ({len(tech_kw)/len(df)*100:.1f}%)")
    
    # Analysiere durchschnittliche Länge
    avg_length = tech_kw.str.len().mean()
    print(f"   Durchschnittliche Länge: {avg_length:.0f} Zeichen")
    print(f"   → Keywords sollten ~5-20 Zeichen sein, nicht {avg_length:.0f}!")
    
    print(f"\n   📋 Beispiele (zeigen: das sind Texte, keine Keywords):")
    for kw in tech_kw.head(3):
        print(f"   • {str(kw)[:100]}...")
    
    print(f"\n   💡 Was Tech_Keywords sein sollten:")
    print(f"      ✅ Beispiel: 'AI, Machine Learning, NLP, Computer Vision'")
    print(f"      ❌ Aktuell: Ganze Artikel-Snippets/Beschreibungen")
    
    # ============================================================================
    # 4. SUB_INDUSTRY NUTZLOSIGKEIT
    # ============================================================================
    print("\n" + "="*80)
    print("⚠️ PROBLEM #4: SUB_INDUSTRY FAST LEER")
    print("="*80)
    
    sub_ind = df['Sub_Industry'].dropna()
    print(f"\n   Vollständigkeit: {len(sub_ind)}/{len(df)} ({len(sub_ind)/len(df)*100:.1f}%)")
    print(f"   → Nur YC hat Sub-Industries, rest ist leer")
    print(f"   → Entweder auffüllen oder Feld entfernen")
    
    # ============================================================================
    # 5. INVESTOR_NAMES COVERAGE PRO QUELLE
    # ============================================================================
    print("\n" + "="*80)
    print("📊 PROBLEM #5: INVESTOR_NAMES COVERAGE ANALYSE")
    print("="*80)
    
    print(f"\n   Gesamt Coverage: {df['Investor_Names'].notna().sum()}/{len(df)} ({df['Investor_Names'].notna().sum()/len(df)*100:.1f}%)")
    print(f"\n   Pro Quelle:")
    
    for source in df['Data_Source'].unique():
        source_df = df[df['Data_Source'] == source]
        inv_coverage = source_df['Investor_Names'].notna().sum()
        print(f"\n   {source}:")
        print(f"   • Total: {len(source_df)}")
        print(f"   • Mit Investoren: {inv_coverage} ({inv_coverage/len(source_df)*100:.1f}%)")
        
        # Zeige Beispiele
        if inv_coverage > 0:
            sample = source_df[source_df['Investor_Names'].notna()]['Investor_Names'].head(2)
            print(f"   • Beispiele:")
            for inv in sample:
                print(f"     - {str(inv)[:60]}...")
    
    # ============================================================================
    # 6. FUNDING_AMOUNT FORMAT-INKONSISTENZEN
    # ============================================================================
    print("\n" + "="*80)
    print("⚠️ PROBLEM #6: FUNDING_AMOUNT FORMAT-INKONSISTENZEN")
    print("="*80)
    
    funding = df['Funding_Amount'].dropna()
    print(f"\n   Vollständigkeit: {len(funding)}/{len(df)} ({len(funding)/len(df)*100:.1f}%)")
    
    # Analysiere verschiedene Formate
    formats = {
        'K CHF/USD': len([x for x in funding if 'K' in str(x)]),
        'M CHF/USD': len([x for x in funding if 'M' in str(x) and 'K' not in str(x)]),
        'undisclosed': len([x for x in funding if 'undisclosed' in str(x).lower()]),
        'Andere': len([x for x in funding if not any(c in str(x) for c in ['K', 'M', 'undisclosed'])])
    }
    
    print(f"\n   Format-Verteilung:")
    for fmt, count in formats.items():
        print(f"   • {fmt}: {count} ({count/len(funding)*100:.1f}%)")
    
    print(f"\n   📋 Beispiele verschiedener Formate:")
    print(f"   • {list(funding.head(5))}")
    
    # ============================================================================
    # 7. DATENQUELLE-SPEZIFISCHE PROBLEME
    # ============================================================================
    print("\n" + "="*80)
    print("🔍 PROBLEM #7: DATENQUELLE-SPEZIFISCHE FEHLER")
    print("="*80)
    
    for source in df['Data_Source'].unique():
        source_df = df[df['Data_Source'] == source]
        print(f"\n   📊 {source} ({len(source_df)} Einträge):")
        
        # Industry-Verteilung
        top_industries = source_df['Industry'].value_counts().head(3)
        print(f"   Top 3 Industries:")
        for ind, count in top_industries.items():
            marker = "❌" if ind in ['B2B', 'CONSUMER'] else "✅"
            print(f"   {marker} {ind}: {count}")
        
        # Feld-Vollständigkeit
        print(f"   Feld-Vollständigkeit:")
        key_fields = ['Industry', 'Funding_Amount', 'Investor_Names', 'Tech_Keywords']
        for field in key_fields:
            filled = source_df[field].notna().sum()
            pct = filled/len(source_df)*100
            marker = "✅" if pct >= 80 else "⚠️" if pct >= 50 else "❌"
            print(f"   {marker} {field}: {pct:.1f}%")
    
    # ============================================================================
    # ZUSAMMENFASSUNG
    # ============================================================================
    print("\n" + "="*80)
    print("📋 ZUSAMMENFASSUNG: GEFUNDENE HAUPTPROBLEME")
    print("="*80)
    
    print("""
    🔴 KRITISCHE FEHLER:
    
    1. INDUSTRY-FELD FALSCH BEFÜLLT
       • 856/1312 (65.2%) haben "B2B" als Industry ❌
       • B2B ist ein Business Model, keine Industry!
       • Echte Industries fehlen (sollte sein: SaaS, E-Commerce, AI, etc.)
    
    2. BUSINESS_MODEL_TYPE KOMPLETT LEER
       • 0/1312 (0%) gefüllt ❌
       • Sollte "B2B", "B2C", "B2B2C" enthalten
       • Diese Info steht fälschlicherweise im Industry-Feld!
    
    3. TECH_KEYWORDS SIND TEXTE, KEINE KEYWORDS
       • Enthält Artikel-Snippets statt strukturierter Keywords
       • Durchschnittlich >100 Zeichen pro "Keyword"
       • Sollte sein: "AI, SaaS, Cloud" statt ganzer Sätze
    
    ⚠️ MITTLERE PROBLEME:
    
    4. SUB_INDUSTRY FAST LEER (0.5%)
       • Nur von YC befüllt
       • Nicht konsistent nutzbar
    
    5. INVESTOR_NAMES NUR 20.9% COVERAGE
       • Venturekick: nur 11.5% (Grants haben oft keine Investor-Namen)
       • Startupticker: 40.2% (gut!)
       • Insgesamt ausbaufähig
    
    ✅ EMPFEHLUNGEN:
    
    1. Industry-Feld neu kategorisieren:
       - Extrahiere echte Industries aus Tech_Keywords/Beschreibungen
       - Kategorien: Fintech, Healthcare, SaaS, E-Commerce, AI/ML, etc.
    
    2. Business_Model_Type befüllen:
       - Verwende aktuelles "B2B" aus Industry-Feld
       - Leite B2C/B2B2C aus Kontext ab
    
    3. Tech_Keywords extrahieren:
       - Parse echte Tech-Keywords aus den Textsnippets
       - Kategorien: AI, ML, SaaS, Cloud, IoT, Blockchain, etc.
    
    4. Sub_Industry optional:
       - Entweder auffüllen oder komplett entfernen
    """)

if __name__ == "__main__":
    analyze_field_issues()
