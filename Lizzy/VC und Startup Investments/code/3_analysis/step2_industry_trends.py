"""
=============================================================================
INDUSTRY TRENDS ÜBER ZEIT (2023–2026)
=============================================================================
Projekt:  data2dollar | MBI Gruppenarbeit | April 2026
Input:    startups_classified_v2.csv  (Output aus step1_data_prep.py)
Output:   6 CSV-Dateien in output/industry_trends/

Forschungsfrage: Welche Industrien gewinnen / verlieren 2023→2026?
Nicht absolute Zahlen — relative Verschiebungen sind die Kernaussage.

Analyse-Überblick:
  A  Market Share Shift     — Anteil pro Industrie in % aller Deals pro Jahr
  B  Ranking-Tabelle        — Wer war #1 in 2023, wer ist #1 in 2025/2026?
  C  Funding-Volumen Shift  — CHF-Anteil pro Industrie pro Jahr
  D  Momentum Score         — Beschleunigt oder verlangsamt eine Industrie?
  E  Klassifikation         — Emerging / Growing / Stable / Declining pro Industrie
  F  Quartals-Detail        — Granulare Zeitreihe für alle Keywords
=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = Path("data/startups_classified_v2.csv")
OUTPUT_DIR = Path("output/industry_trends")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Nur vollständige Jahre für Jahres-Analysen (2026 hat noch nicht alle Quartale)
FULL_YEARS   = [2023, 2024, 2025]
ALL_YEARS    = [2023, 2024, 2025, 2026]


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 1 — DATEN LADEN
# ═══════════════════════════════════════════════════════════════════════════

def load(path: Path) -> pd.DataFrame:
    """
    Lädt startups_classified_v2.csv.
    Extrahiert 'year' aus 'quarter' ('2024-Q3' → 2024).
    Gibt vollständigen DataFrame zurück.
    """
    print("\n" + "=" * 60)
    print("SCHRITT 1: Daten laden")
    print("=" * 60)
    
    df = pd.read_csv(path)
    df['year'] = df['quarter'].str[:4].astype(int)
    
    print(f"  ✓ Geladen: {len(df)} Startups, {df['year'].min()}–{df['year'].max()}")
    print(f"  ✓ Keywords: {sorted(df['keyword'].unique())}")
    print(f"  ✓ Deals pro Jahr:")
    for year, count in df['year'].value_counts().sort_index().items():
        print(f"      {year}: {count} Deals")
    
    return df


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 2 — ANALYSE A: MARKET SHARE SHIFT
# ═══════════════════════════════════════════════════════════════════════════

def analyse_market_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kernfrage: Welche Industrie gewinnt / verliert Marktanteile?

    Logik:
      Für jedes Jahr: Anzahl Deals pro keyword / Total Deals dieses Jahres * 100
      → zeigt nicht ob der Markt wächst, sondern ob eine Industrie
        RELATIV MEHR oder WENIGER Aufmerksamkeit bekommt.
    """
    print("\n" + "=" * 60)
    print("ANALYSE A: Market Share Shift")
    print("=" * 60)

    # Berechne Jahres-Totals
    total_per_year = df.groupby('year').size()
    
    # Berechne Deals pro keyword pro Jahr
    counts = df.groupby(['keyword', 'year']).size().unstack(fill_value=0)
    
    # Berechne Share in Prozent
    share = counts.div(total_per_year, axis=1) * 100
    share = share.round(1)
    
    # Behalte nur Jahres-Spalten aus ALL_YEARS die vorhanden sind
    available_years = [y for y in ALL_YEARS if y in share.columns]
    share = share[available_years]
    
    # Berechne share_change_pct (2023 → 2025)
    if 2023 in share.columns and 2025 in share.columns:
        share['share_change_pct'] = (share[2025] - share[2023]).round(1)
    else:
        share['share_change_pct'] = np.nan
    
    # Füge 'direction' hinzu
    def get_direction(change):
        if pd.isna(change):
            return '?'
        elif change > 0.5:
            return '+'
        elif change < -0.5:
            return '-'
        else:
            return '='
    
    share['direction'] = share['share_change_pct'].apply(get_direction)
    
    # Sortiere nach share_change_pct absteigend
    share = share.sort_values('share_change_pct', ascending=False)
    
    # Speichere
    output_path = OUTPUT_DIR / "A_market_share_pct.csv"
    share.to_csv(output_path)
    
    print("\n  Market Share Entwicklung (% aller Deals pro Jahr):")
    print("  " + "─" * 58)
    print(share.to_string())
    print(f"\n  ✓ Gespeichert: {output_path.name}")
    
    return share


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 3 — ANALYSE B: RANKING-TABELLE
# ═══════════════════════════════════════════════════════════════════════════

def analyse_rankings(df: pd.DataFrame) -> None:
    """
    Kernfrage: Wer war #1 in 2023 — ist er es noch in 2026?

    Logik:
      Für jedes Jahr: Rank jeder Industrie nach Deal-Count (1 = meiste Deals).
      Zeige Rank-Veränderung: rank_2023 − rank_2025 (positiv = aufgestiegen).
    """
    print("\n" + "=" * 60)
    print("ANALYSE B: Ranking-Tabelle (wer steigt auf, wer fällt?)")
    print("=" * 60)

    # Berechne Deals pro keyword pro Jahr
    counts = df.groupby(['keyword', 'year']).size().unstack(fill_value=0)
    
    # Berechne Ranks (1 = meiste Deals)
    ranks = counts.rank(ascending=False, method='min').astype(int)
    
    # Benenne Spalten um
    ranks.columns = [f'rank_{col}' for col in ranks.columns]
    
    # Berechne rank_change (2023 → 2025)
    if 'rank_2023' in ranks.columns and 'rank_2025' in ranks.columns:
        ranks['rank_change'] = ranks['rank_2023'] - ranks['rank_2025']
    else:
        ranks['rank_change'] = 0
    
    # Füge 'trend' hinzu
    def get_trend(change):
        if change >= 2:
            return '↑'
        elif change <= -2:
            return '↓'
        else:
            return '→'
    
    ranks['trend'] = ranks['rank_change'].apply(get_trend)
    
    # Sortiere nach rank_2025 aufsteigend (beste zuerst)
    if 'rank_2025' in ranks.columns:
        ranks = ranks.sort_values('rank_2025', ascending=True)
    
    # Speichere
    output_path = OUTPUT_DIR / "B_rankings_by_year.csv"
    ranks.to_csv(output_path)
    
    print("\n  Ranking-Entwicklung (1 = meiste Deals):")
    print("  " + "─" * 58)
    print(ranks.to_string())
    
    # Top 3 Aufsteiger und Absteiger
    print("\n  📈 Top 3 Aufsteiger:")
    climbers = ranks[ranks['rank_change'] >= 2].sort_values('rank_change', ascending=False).head(3)
    if len(climbers) > 0:
        for kw, row in climbers.iterrows():
            print(f"      {kw:20s}  {int(row.get('rank_2023', 0))} → {int(row.get('rank_2025', 0))}  (+{int(row['rank_change'])})")
    else:
        print("      Keine signifikanten Aufsteiger")
    
    print("\n  📉 Top 3 Absteiger:")
    fallers = ranks[ranks['rank_change'] <= -2].sort_values('rank_change', ascending=True).head(3)
    if len(fallers) > 0:
        for kw, row in fallers.iterrows():
            print(f"      {kw:20s}  {int(row.get('rank_2023', 0))} → {int(row.get('rank_2025', 0))}  ({int(row['rank_change'])})")
    else:
        print("      Keine signifikanten Absteiger")
    
    print(f"\n  ✓ Gespeichert: {output_path.name}")


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 4 — ANALYSE C: FUNDING-VOLUMEN SHIFT
# ═══════════════════════════════════════════════════════════════════════════

def analyse_funding_shift(df: pd.DataFrame, share_df: pd.DataFrame) -> None:
    """
    Kernfrage: Welche Industrie bekommt MEHR Geld — auch wenn Deal-Count gleich bleibt?
    """
    print("\n" + "=" * 60)
    print("ANALYSE C: Funding-Volumen Shift")
    print("=" * 60)

    # Filtere auf has_funding == True
    df_funded = df[df['has_funding'] == True].copy()
    
    if len(df_funded) == 0:
        print("  ⚠ Keine Funding-Daten vorhanden — Analyse übersprungen.")
        return
    
    print(f"  ✓ {len(df_funded)} von {len(df)} Deals haben Funding-Daten")
    
    # Berechne Funding-Total pro Jahr
    total_funding = df_funded.groupby('year')['funding_chf'].sum()
    
    # Berechne Funding pro keyword pro Jahr
    vol = df_funded.groupby(['keyword', 'year'])['funding_chf'].sum().unstack(fill_value=0)
    
    # Berechne Share in Prozent
    funding_share = vol.div(total_funding, axis=1) * 100
    funding_share = funding_share.round(1)
    
    # Behalte nur Jahre aus ALL_YEARS
    available_years = [y for y in ALL_YEARS if y in funding_share.columns]
    funding_share = funding_share[available_years]
    
    # Berechne funding_change_pp (2023 → 2025)
    if 2023 in funding_share.columns and 2025 in funding_share.columns:
        funding_share['funding_change_pp'] = (funding_share[2025] - funding_share[2023]).round(1)
    else:
        funding_share['funding_change_pp'] = np.nan
    
    # Hole deal_share_change aus Analyse A
    if 'share_change_pct' in share_df.columns:
        funding_share = funding_share.join(
            share_df[['share_change_pct']].rename(columns={'share_change_pct': 'deal_share_change'}),
            how='left'
        )
    else:
        funding_share['deal_share_change'] = np.nan
    
    # Füge 'signal' hinzu
    def get_signal(row):
        funding_change = row['funding_change_pp']
        deal_change = row.get('deal_share_change', 0)
        
        if pd.isna(funding_change) or pd.isna(deal_change):
            return 'Unbekannt'
        
        if funding_change > deal_change + 2:
            return 'Grosse Deals ↑'
        elif deal_change > funding_change + 2:
            return 'Viele Deals ↑'
        else:
            return 'Gleichmässig'
    
    funding_share['signal'] = funding_share.apply(get_signal, axis=1)
    
    # Sortiere nach funding_change_pp absteigend
    funding_share = funding_share.sort_values('funding_change_pp', ascending=False)
    
    # Speichere
    output_path = OUTPUT_DIR / "C_funding_share_pct.csv"
    funding_share.to_csv(output_path)
    
    print("\n  Funding-Volumen Entwicklung (% des Total-Funding pro Jahr):")
    print("  " + "─" * 58)
    print(funding_share.to_string())
    print(f"\n  ✓ Gespeichert: {output_path.name}")


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 5 — ANALYSE D: MOMENTUM SCORE
# ═══════════════════════════════════════════════════════════════════════════

def analyse_momentum(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kernfrage: Welche Industrie beschleunigt JETZT gerade — nicht nur historisch?
    """
    print("\n" + "=" * 60)
    print("ANALYSE D: Momentum Score (wer beschleunigt gerade?)")
    print("=" * 60)

    # Erstelle Quartals-Pivot
    pivot = df.groupby(['keyword', 'quarter']).size().unstack(fill_value=0)
    
    # Sortiere Spalten chronologisch
    all_quarters = sorted(pivot.columns.tolist())
    pivot = pivot[all_quarters]
    
    print(f"  ✓ Analysiere {len(all_quarters)} Quartale: {all_quarters[0]} bis {all_quarters[-1]}")
    
    # Bestimme erste und letzte 4 Quartale
    first_4 = all_quarters[:4]
    last_4 = all_quarters[-4:]
    
    print(f"  ✓ Earlier period: {first_4}")
    print(f"  ✓ Recent period:  {last_4}")
    
    # Berechne Durchschnitte
    earlier_avg = pivot[first_4].mean(axis=1).round(1)
    recent_avg = pivot[last_4].mean(axis=1).round(1)
    momentum = ((recent_avg - earlier_avg) / (earlier_avg + 0.1) * 100).round(1)
    
    # Baue Result-DataFrame
    result = pd.DataFrame({
        'keyword': pivot.index,
        'earlier_avg': earlier_avg.values,
        'recent_avg': recent_avg.values,
        'momentum_pct': momentum.values
    })
    
    # Füge 'classification' hinzu
    def classify_momentum(pct):
        if pct > 50:
            return 'Accelerating 🚀'
        elif pct > 10:
            return 'Growing ↑'
        elif pct > -10:
            return 'Stable →'
        elif pct > -50:
            return 'Slowing ↓'
        else:
            return 'Declining 📉'
    
    result['classification'] = result['momentum_pct'].apply(classify_momentum)
    
    # Sortiere nach momentum_pct absteigend
    result = result.sort_values('momentum_pct', ascending=False)
    result = result.set_index('keyword')
    
    # Speichere
    output_path = OUTPUT_DIR / "D_momentum.csv"
    result.to_csv(output_path)
    
    print("\n  Momentum-Analyse (frühe vs. späte Quartale):")
    print("  " + "─" * 58)
    print(result.to_string())
    print(f"\n  ✓ Gespeichert: {output_path.name}")
    
    return result


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 6 — ANALYSE E: EMERGING / DECLINING KLASSIFIKATION
# ═══════════════════════════════════════════════════════════════════════════

def analyse_classification(df: pd.DataFrame,
                           share_df: pd.DataFrame,
                           momentum_df: pd.DataFrame) -> None:
    """
    Kombiniert Market Share + Momentum zu einer finalen Klassifikation.
    Dies ist die Zusammenfassung für die Forschungsfrage.
    """
    print("\n" + "=" * 60)
    print("ANALYSE E: Finale Klassifikation (Emerging / Growing / Declining)")
    print("=" * 60)

    # Merge share_df und momentum_df
    result = share_df.copy()
    result = result.join(momentum_df[['momentum_pct']], how='inner')
    
    # Hole relevante Spalten
    cols = []
    if 2023 in result.columns:
        result['share_2023'] = result[2023]
        cols.append('share_2023')
    if 2025 in result.columns:
        result['share_2025'] = result[2025]
        cols.append('share_2025')
    
    cols.extend(['share_change_pct', 'momentum_pct'])
    
    # Bestimme classification
    def classify(row):
        share_change = row['share_change_pct']
        momentum = row['momentum_pct']
        
        if pd.isna(share_change) or pd.isna(momentum):
            return 'Unknown'
        
        # Priorität absteigend
        if share_change > 1.5 and momentum > 30:
            return 'Emerging  🌱'
        elif share_change > 0.5 and momentum > 10:
            return 'Growing   ↑'
        elif abs(share_change) <= 0.5:
            return 'Stable    →'
        elif share_change < -0.5 and momentum < 10:
            return 'Slowing   ↓'
        elif share_change < -1.5 and momentum < -20:
            return 'Declining 📉'
        else:
            # Fallback: basierend auf share_change
            if share_change > 0.5:
                return 'Growing   ↑'
            elif share_change < -0.5:
                return 'Slowing   ↓'
            else:
                return 'Stable    →'
    
    result['classification'] = result.apply(classify, axis=1)
    
    # Definiere Sortier-Reihenfolge
    CLASS_ORDER = [
        'Emerging  🌱',
        'Growing   ↑',
        'Stable    →',
        'Slowing   ↓',
        'Declining 📉',
        'Unknown'
    ]
    result['classification'] = pd.Categorical(
        result['classification'],
        categories=CLASS_ORDER,
        ordered=True
    )
    
    # Sortiere
    result = result.sort_values(['classification', 'momentum_pct'], ascending=[True, False])
    
    # Wähle finale Spalten
    final_cols = cols + ['classification']
    result_final = result[final_cols]
    
    # Speichere
    output_path = OUTPUT_DIR / "E_industry_classification.csv"
    result_final.to_csv(output_path)
    
    print("\n  Finale Industrie-Klassifikation:")
    print("  " + "─" * 58)
    print(result_final.to_string())
    
    # Summary nach Klassifikation
    print("\n  📊 Zusammenfassung:")
    for cls in CLASS_ORDER:
        keywords = result_final[result_final['classification'] == cls].index.tolist()
        if len(keywords) > 0:
            print(f"      {cls:15s}  {len(keywords):2d} Keywords → {keywords}")
    
    print(f"\n  ✓ Gespeichert: {output_path.name}")


# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 7 — ANALYSE F: QUARTALS-DETAIL (granulare Zeitreihe)
# ═══════════════════════════════════════════════════════════════════════════

def analyse_quarterly_detail(df: pd.DataFrame) -> None:
    """
    Vollständige Quartals-Zeitreihe für alle Keywords.
    Weniger Interpretation — mehr rohe Daten für spätere Visualisierung.
    """
    print("\n" + "=" * 60)
    print("ANALYSE F: Quartals-Detail (granulare Zeitreihe)")
    print("=" * 60)

    # OUTPUT F1 — deal_count_by_quarter
    pivot = df.groupby(['quarter', 'keyword']).size().unstack(fill_value=0)
    
    # Sortiere Zeilen chronologisch
    pivot = pivot.sort_index()
    
    # Füge TOTAL-Spalte hinzu
    pivot['TOTAL'] = pivot.sum(axis=1)
    
    # Speichere F1
    output_f1 = OUTPUT_DIR / "F1_deal_count_quarterly.csv"
    pivot.to_csv(output_f1)
    
    print("\n  F1: Deal Count pro Quartal:")
    print("  " + "─" * 58)
    print(pivot.to_string())
    print(f"\n  ✓ Gespeichert: {output_f1.name}")
    
    # OUTPUT F2 — deal_share_by_quarter
    share = pivot.drop(columns='TOTAL').div(pivot['TOTAL'], axis=0) * 100
    share = share.round(1)
    
    # Füge TOTAL = 100.0 hinzu
    share['TOTAL'] = 100.0
    
    # Speichere F2
    output_f2 = OUTPUT_DIR / "F2_deal_share_quarterly.csv"
    share.to_csv(output_f2)
    
    print("\n  F2: Deal Share pro Quartal (%):")
    print("  " + "─" * 58)
    print(share.to_string())
    print(f"\n  ✓ Gespeichert: {output_f2.name}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("Industry Trends Analyse — data2dollar | April 2026")
    print("=" * 60)

    df = load(INPUT_FILE)

    share_df    = analyse_market_share(df)      # gibt DataFrame zurück
    analyse_rankings(df)
    analyse_funding_shift(df, share_df)
    momentum_df = analyse_momentum(df)           # gibt DataFrame zurück
    analyse_classification(df, share_df, momentum_df)
    analyse_quarterly_detail(df)

    print("\n" + "=" * 60)
    print("FERTIG — alle Outputs in:", OUTPUT_DIR.resolve())
    print("=" * 60)
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        rows = sum(1 for _ in open(f)) - 1
        print(f"  {f.name:50s}  ({rows} Zeilen)")


if __name__ == "__main__":
    main()
