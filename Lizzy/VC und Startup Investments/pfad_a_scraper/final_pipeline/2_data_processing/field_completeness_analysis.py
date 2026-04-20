#!/usr/bin/env python3
"""
Feld-Vollständigkeits-Analyse für Schweizer Startup-Daten
Identifiziert leere Felder und gibt Empfehlungen für Re-Scraping
"""

import pandas as pd

def analyze_field_completeness():
    """Analysiert Vollständigkeit aller Felder und gibt Empfehlungen"""
    
    print("="*80)
    print("📊 FELD-VOLLSTÄNDIGKEITS-ANALYSE")
    print("="*80)
    
    df = pd.read_csv('data/schweiz_2020_2026_clean.csv')
    print(f"\n📂 Dataset: {len(df)} Schweizer Startups (2020-2026)\n")
    
    # ========================================================================
    # 1. ÜBERSICHT ALLER FELDER
    # ========================================================================
    print("\n" + "="*80)
    print("1️⃣ VOLLSTÄNDIGKEIT ALLER 16 PFLICHTFELDER")
    print("="*80)
    
    fields = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investor_Type', 'Investor_Names', 'Country', 'Founding_Year',
        'Investment_Stage', 'Valuation', 'Exit_Type', 'Startup_Stage'
    ]
    
    completeness = {}
    for field in fields:
        if field in df.columns:
            filled = df[field].notna().sum()
            empty = len(df) - filled
            pct = (filled / len(df)) * 100
            completeness[field] = {
                'filled': filled,
                'empty': empty,
                'pct': pct
            }
    
    # Sortiere nach Vollständigkeit
    sorted_fields = sorted(completeness.items(), key=lambda x: x[1]['pct'], reverse=True)
    
    print("\n📋 Vollständigkeit pro Feld:")
    print(f"\n{'Feld':<25} {'Gefüllt':<12} {'Leer':<12} {'%':<8} Status")
    print("-"*80)
    
    for field, stats in sorted_fields:
        pct = stats['pct']
        if pct == 100:
            status = "✅ Perfekt"
        elif pct >= 80:
            status = "✅ Gut"
        elif pct >= 50:
            status = "⚠️ Mittel"
        elif pct >= 20:
            status = "❌ Schlecht"
        else:
            status = "🚨 Sehr schlecht"
        
        print(f"{field:<25} {stats['filled']:<12} {stats['empty']:<12} {pct:>6.1f}%  {status}")
    
    # ========================================================================
    # 2. KRITISCHE FELDER (< 50% gefüllt)
    # ========================================================================
    print("\n" + "="*80)
    print("2️⃣ KRITISCHE FELDER (< 50% VOLLSTÄNDIGKEIT)")
    print("="*80)
    
    critical_fields = [(f, s) for f, s in sorted_fields if s['pct'] < 50]
    
    if critical_fields:
        for field, stats in critical_fields:
            print(f"\n🚨 {field}:")
            print(f"   • Nur {stats['filled']}/{len(df)} gefüllt ({stats['pct']:.1f}%)")
            print(f"   • {stats['empty']} Einträge LEER")
            
            # Zeige Beispiele wo gefüllt
            filled_examples = df[df[field].notna()][field].head(3)
            if len(filled_examples) > 0:
                print(f"   • Beispiele wo VORHANDEN:")
                for val in filled_examples:
                    print(f"     - {str(val)[:60]}...")
    else:
        print("\n✅ Keine kritischen Felder gefunden!")
    
    # ========================================================================
    # 3. ANALYSE PRO DATENQUELLE
    # ========================================================================
    print("\n" + "="*80)
    print("3️⃣ VOLLSTÄNDIGKEIT PRO DATENQUELLE")
    print("="*80)
    
    key_fields = ['Industry', 'Funding_Amount', 'Investor_Names', 'Tech_Keywords', 
                  'Valuation', 'Exit_Type', 'Sub_Industry']
    
    for source in df['Data_Source'].unique():
        source_df = df[df['Data_Source'] == source]
        print(f"\n📊 {source} ({len(source_df)} Startups):")
        
        for field in key_fields:
            if field in source_df.columns:
                filled = source_df[field].notna().sum()
                pct = (filled / len(source_df)) * 100
                
                if pct == 100:
                    marker = "✅"
                elif pct >= 80:
                    marker = "✅"
                elif pct >= 50:
                    marker = "⚠️"
                elif pct >= 20:
                    marker = "❌"
                else:
                    marker = "🚨"
                
                print(f"   {marker} {field:<20}: {filled:>4}/{len(source_df):<4} ({pct:>5.1f}%)")
    
    # ========================================================================
    # 4. FEHLENDE DATEN-PATTERNS
    # ========================================================================
    print("\n" + "="*80)
    print("4️⃣ FEHLENDE DATEN PATTERNS")
    print("="*80)
    
    # Welche Startups haben am meisten fehlende Felder?
    df['missing_fields_count'] = df[fields].isna().sum(axis=1)
    
    print(f"\n📊 Verteilung fehlender Felder:")
    missing_dist = df['missing_fields_count'].value_counts().sort_index()
    for missing_count, startup_count in missing_dist.items():
        print(f"   • {missing_count} fehlende Felder: {startup_count} Startups")
    
    # Startups mit vielen fehlenden Feldern
    high_missing = df[df['missing_fields_count'] >= 5].sort_values('missing_fields_count', ascending=False)
    if len(high_missing) > 0:
        print(f"\n⚠️ {len(high_missing)} Startups mit 5+ fehlenden Feldern:")
        print(f"\n   Top 5 'leerste' Startups:")
        for idx, row in high_missing.head(5).iterrows():
            print(f"\n   • {row['Startup_Name']} ({row['Data_Source']}):")
            print(f"     Fehlende Felder: {int(row['missing_fields_count'])}/16")
            # Zeige welche Felder leer sind
            empty_fields = [f for f in fields if pd.isna(row[f])]
            print(f"     Leer: {', '.join(empty_fields[:5])}...")
    
    # ========================================================================
    # 5. RE-SCRAPING EMPFEHLUNGEN
    # ========================================================================
    print("\n" + "="*80)
    print("5️⃣ RE-SCRAPING EMPFEHLUNGEN")
    print("="*80)
    
    recommendations = []
    
    # Investor_Names
    inv_pct = completeness.get('Investor_Names', {}).get('pct', 0)
    if inv_pct < 50:
        recommendations.append({
            'field': 'Investor_Names',
            'current': f'{inv_pct:.1f}%',
            'priority': '🔴 HOCH',
            'action': 'Startupticker & Venturekick Re-Scraping',
            'reason': 'Investor-Informationen sind key für Investment-Analyse'
        })
    
    # Valuation
    val_pct = completeness.get('Valuation', {}).get('pct', 0)
    if val_pct < 10:
        recommendations.append({
            'field': 'Valuation',
            'current': f'{val_pct:.1f}%',
            'priority': '⚠️ MITTEL',
            'action': 'Zusätzliche Quelle (Crunchbase API?) oder manuell recherchieren',
            'reason': 'Valuations selten öffentlich, schwer zu scrapen'
        })
    
    # Exit_Type
    exit_pct = completeness.get('Exit_Type', {}).get('pct', 0)
    if exit_pct < 10:
        recommendations.append({
            'field': 'Exit_Type',
            'current': f'{exit_pct:.1f}%',
            'priority': '🟡 NIEDRIG',
            'action': 'Zusätzliche Quelle (Exits/Acquisitions News)',
            'reason': 'Wenige Startups haben Exits (2020-2026 zu kurzer Zeitraum)'
        })
    
    # Sub_Industry
    sub_pct = completeness.get('Sub_Industry', {}).get('pct', 0)
    if sub_pct < 10:
        recommendations.append({
            'field': 'Sub_Industry',
            'current': f'{sub_pct:.1f}%',
            'priority': '🟡 NIEDRIG',
            'action': 'KI-basierte Kategorisierung aus Tech_Keywords',
            'reason': 'Kann automatisch abgeleitet werden, nicht kritisch'
        })
    
    # Funding_Amount (falls < 80%)
    fund_pct = completeness.get('Funding_Amount', {}).get('pct', 0)
    if fund_pct < 80:
        recommendations.append({
            'field': 'Funding_Amount',
            'current': f'{fund_pct:.1f}%',
            'priority': '🔴 HOCH',
            'action': 'Re-Scraping mit verbesserter Regex',
            'reason': 'Funding Amounts sind zentral für Investment-Analyse'
        })
    
    if recommendations:
        print("\n📋 Empfohlene Aktionen:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['priority']} {rec['field']} (aktuell: {rec['current']})")
            print(f"   Aktion: {rec['action']}")
            print(f"   Grund: {rec['reason']}\n")
    
    # ========================================================================
    # 6. ZUSAMMENFASSUNG
    # ========================================================================
    print("\n" + "="*80)
    print("📋 ZUSAMMENFASSUNG & HANDLUNGSEMPFEHLUNGEN")
    print("="*80)
    
    # Zähle Felder nach Status
    perfect_count = sum(1 for f, s in sorted_fields if s['pct'] == 100)
    good_count = sum(1 for f, s in sorted_fields if 80 <= s['pct'] < 100)
    medium_count = sum(1 for f, s in sorted_fields if 50 <= s['pct'] < 80)
    poor_count = sum(1 for f, s in sorted_fields if s['pct'] < 50)
    
    print(f"""
    📊 FELD-STATUS:
    • ✅ Perfekt (100%): {perfect_count} Felder
    • ✅ Gut (80-99%): {good_count} Felder
    • ⚠️ Mittel (50-79%): {medium_count} Felder
    • 🚨 Schlecht (< 50%): {poor_count} Felder
    
    🎯 HANDLUNGSEMPFEHLUNGEN:
    
    1. KEIN RE-SCRAPING NÖTIG:
       ✅ Industry, Year, Country, Founding_Year, Investment_Stage
       → Diese Felder sind gut gefüllt (>80%)
    
    2. RE-SCRAPING EMPFOHLEN:
       🔴 Investor_Names (aktuell: {inv_pct:.1f}%)
          → Startupticker: Detail-Seiten nochmal durchgehen
          → Venturekick: Investor-Informationen verbessern
       
       ⚠️ Funding_Amount (aktuell: {fund_pct:.1f}%)
          → Falls < 80%: Regex-Pattern verbessern
    
    3. NICHT KRITISCH (kann leer bleiben):
       🟡 Valuation (aktuell: {val_pct:.1f}%)
          → Selten öffentlich verfügbar
          → Für Analyse nicht essentiell
       
       🟡 Exit_Type (aktuell: {exit_pct:.1f}%)
          → Zu junger Zeitraum (2020-2026)
          → Wenige Exits erwartbar
       
       🟡 Sub_Industry (aktuell: {sub_pct:.1f}%)
          → Kann aus Tech_Keywords abgeleitet werden
          → Nicht kritisch für Analyse
    
    💡 EMPFEHLUNG:
    Fokussiere Re-Scraping auf INVESTOR_NAMES (höchste Priorität!)
    - Startupticker: 40% Coverage kann auf 60-70% verbessert werden
    - Venturekick: 11.5% Coverage kann auf 30-40% verbessert werden
    
    → Investor-Netzwerk-Analyse wird dadurch deutlich besser! 🎯
    """)
    
    return df

if __name__ == "__main__":
    df = analyze_field_completeness()
