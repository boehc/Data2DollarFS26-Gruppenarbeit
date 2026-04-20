"""
=============================================================================
GITHUB COPILOT PROMPT — STEP 1: Datenaufbereitung startupticker
=============================================================================
Projekt:  data2dollar | MBI Gruppenarbeit | April 2026
Input:    startupticker_enriched_FINAL.csv
Output:   startups_classified_v2.csv  (Name wie im Report spezifiziert)

Ziel: Keine Grafiken — nur saubere, analysierbare Tabelle als CSV.
      Entspricht exakt der Spezifikation in projektstand_report_v2.pdf.

Spalten im Output:
  startup_name     | str   — Name des Startups
  industry         | str   — Original-Kategorie (z.B. 'FinTech')
  keyword          | str   — Gemapptes Keyword aus Natalies System
  layer_type       | str   — 'tech_layer' oder 'industry_layer'
  funding_chf      | float — Funding in CHF Mio. (UNDISCLOSED → NaN)
  has_funding      | bool  — True wenn funding_chf nicht NaN
  quarter          | str   — '2023-Q1' bis '2026-Q2'
  publication_date | date  — Original-Datum
  canton           | str   — Schweizer Kanton
  city             | str   — Stadt

Erwartetes Ergebnis laut Report: ~1'388 klassifizierte Startups
  (1'564 total minus 127 Other minus B2C ohne Tag-Match)

COPILOT-ANWEISUNG: Vervollständige alle # >> COPILOT: Abschnitte.
=============================================================================
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Optional, Tuple

# ── Pfade ──────────────────────────────────────────────────────────────────
PATH_STARTUPS = Path("data/startupticker_enriched_FINAL.csv")
OUTPUT_FILE   = Path("data/startups_classified_v2.csv")   # Name laut Report

# ── Konstanten ─────────────────────────────────────────────────────────────

FX_RATES = {"CHF": 1.0, "USD": 0.90, "EUR": 0.95}

# ── Keyword-System (vollständig, aus projektstand_report_v2.pdf Seite 1) ──

TECH_LAYER = [
    "GenAI", "AgentAI", "LLM", "Robotics", "Semiconductors",
    "ComputerVision", "PhysicalAI", "Web3", "QuantumTech",
    "Cybersecurity", "Infrastructure"
]

INDUSTRY_LAYER = [
    "HealthTech", "BioTech", "MedTech", "DigitalHealth", "FinTech",
    "ClimateTech", "DefenseTech", "EdTech", "HRTech", "LegalTech",
    "AgriTech", "SpaceTech", "Ecommerce", "Enterprise",
    "CreatorEconomy", "GameTech", "MobilityTech", "PropTech"
]

# ── Mapping-Tabelle (Report Seite 2) ──────────────────────────────────────
# Direkte industry → (keyword, layer_type) Mappings ohne Tag-Logik
DIRECT_MAP = {
    "FinTech":        ("FinTech",       "industry_layer"),
    "BioTech":        ("BioTech",       "industry_layer"),
    "CleanTech":      ("ClimateTech",   "industry_layer"),  # identisch laut Report
    "MedTech":        ("MedTech",       "industry_layer"),
    "Enterprise SaaS":("Enterprise",    "industry_layer"),
    "HealthTech":     ("HealthTech",    "industry_layer"),
    "Robotics":       ("Robotics",      "tech_layer"),
    "PropTech":       ("PropTech",      "industry_layer"),
    "FoodTech":       ("AgriTech",      "industry_layer"),  # laut Report
    "Cybersecurity":  ("Cybersecurity", "tech_layer"),
    "EdTech":         ("EdTech",        "industry_layer"),
    "SpaceTech":      ("SpaceTech",     "industry_layer"),
    # "B2C Tech" → Tags-Fallback B2C_TAG_FALLBACK
    # "AI/ML"    → Tags-Fallback AIML_TAG_FALLBACK  (NICHT einfach GenAI!)
    # "Other"    → None (herausgefiltert)
}

# Fallback B2C Tech (Report: "Ecommerce/MobilityTech/BioTech je nach Tags")
B2C_TAG_FALLBACK = {
    "ecommerce":  ("Ecommerce",    "industry_layer"),
    "e-commerce": ("Ecommerce",    "industry_layer"),
    "mobility":   ("MobilityTech", "industry_layer"),
    "biotech":    ("BioTech",      "industry_layer"),
    "healthtech": ("HealthTech",   "industry_layer"),
    "fintech":    ("FinTech",      "industry_layer"),
}

# Fallback AI/ML (Report: "GenAI/LLM/AgentAI je nach Tags")
# WICHTIG: Reihenfolge ist Priorität — spezifischste zuerst, 'ai' ist letzter Fallback
AIML_TAG_FALLBACK = {
    "genai":          ("GenAI",   "tech_layer"),
    "gen ai":         ("GenAI",   "tech_layer"),
    "generative":     ("GenAI",   "tech_layer"),
    "foundation":     ("GenAI",   "tech_layer"),  # 'Foundation Models' → GenAI
    "llm":            ("LLM",     "tech_layer"),
    "large language": ("LLM",     "tech_layer"),
    "agent":          ("AgentAI", "tech_layer"),
    "agentic":        ("AgentAI", "tech_layer"),
    "ai":             ("GenAI",   "tech_layer"),  # letzter Fallback
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════

def parse_funding_amount(amount_str) -> Optional[float]:
    """
    Parst '10M USD' → 9.0  (CHF Mio.)
         '1.5M CHF' → 1.5
         '0M CHF'   → None  (kein sinnvoller Wert)
         'UNDISCLOSED' / NaN → None

    Regex-Pattern: r'([\d.]+)M\s*(CHF|USD|EUR)'
    Konvertierung: betrag * FX_RATES[währung]
    """
    # Falls amount_str NaN oder kein String: return None
    if pd.isna(amount_str) or not isinstance(amount_str, str):
        return None
    
    # Falls 'UNDISCLOSED' enthalten: return None
    if 'UNDISCLOSED' in amount_str.upper():
        return None
    
    # Wende Regex-Pattern an
    match = re.match(r'([\d.]+)M\s*(CHF|USD|EUR)', amount_str, re.IGNORECASE)
    if not match:
        return None
    
    # Extrahiere Betrag und Währung
    betrag = float(match.group(1))
    waehrung = match.group(2).upper()
    
    # Falls 0.0: return None
    if betrag == 0.0:
        return None
    
    # Konvertiere zu CHF und runde
    return round(betrag * FX_RATES[waehrung], 3)


def map_keyword(row: pd.Series) -> Tuple[Optional[str], Optional[str]]:
    """
    Mapped eine Zeile auf (keyword, layer_type).
    Gibt (None, None) zurück wenn keine Zuordnung möglich.

    Logik (3 Stufen, Priorität absteigend):
    1. DIRECT_MAP lookup: industry in DIRECT_MAP → return direkt
    2. AI/ML: Tags via AIML_TAG_FALLBACK durchsuchen (Reihenfolge beachten!)
       → Falls kein Tags-Match: return (None, None)
    3. B2C Tech: Tags via B2C_TAG_FALLBACK durchsuchen
       → Falls kein Match: return (None, None)
    4. Other / alles andere: return (None, None)

    Tags-Suche: tags_lower = str(row['tags']).lower()
                key in tags_lower  (substring-Suche)
                str() wandelt NaN → 'nan' → kein Key matcht 'nan' → sicher
    """
    industry = row.get('industry', '')
    
    # Stufe 1: DIRECT_MAP
    if industry in DIRECT_MAP:
        return DIRECT_MAP[industry]
    
    # Stufe 2: AI/ML mit Tags
    if industry == 'AI/ML':
        tags_lower = str(row.get('tags', '')).lower()
        # Iteriere in Definitionsreihenfolge (Python 3.7+ garantiert)
        for key, value in AIML_TAG_FALLBACK.items():
            if key in tags_lower:
                return value
        # Kein Match gefunden
        return (None, None)
    
    # Stufe 3: B2C Tech mit Tags
    if industry == 'B2C Tech':
        tags_lower = str(row.get('tags', '')).lower()
        for key, value in B2C_TAG_FALLBACK.items():
            if key in tags_lower:
                return value
        # Kein Match gefunden
        return (None, None)
    
    # Stufe 4: Other / alles andere
    return (None, None)


def add_quarter_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fügt Spalte 'quarter' hinzu: '2023-Q1', '2024-Q3', etc.
    Basiert auf 'publication_date' (Format YYYY-MM-DD).
    Sortiert DataFrame nach publication_date aufsteigend.
    """
    # Konvertiere zu datetime
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
    
    # Extrahiere Jahr und Quartal
    year = df['publication_date'].dt.year
    q = df['publication_date'].dt.quarter
    
    # Erstelle quarter-Spalte
    df['quarter'] = year.astype(str) + '-Q' + q.astype(str)
    
    # Sortiere nach Datum
    df = df.sort_values('publication_date').reset_index(drop=True)
    
    return df


# ═══════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

def main():

    # ── 1. Laden ───────────────────────────────────────────────────────────
    print("=" * 60)
    print("STEP 1: Lade Daten")
    print("=" * 60)
    
    df = pd.read_csv(PATH_STARTUPS)
    print(f"  Geladen: {len(df)} Zeilen")
    print("\n  Industry-Verteilung (Original):")
    print(df['industry'].value_counts().to_string())

    # ── 2. Keyword-Mapping ─────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 2: Keyword-Mapping")
    print("=" * 60)
    
    result = df.apply(map_keyword, axis=1)
    df['keyword'] = result.apply(lambda x: x[0])
    df['layer_type'] = result.apply(lambda x: x[1])
    
    n_mapped = df['keyword'].notna().sum()
    n_unmapped = df['keyword'].isna().sum()
    print(f"  Gemappt:       {n_mapped} Startups")
    print(f"  Nicht gemappt: {n_unmapped} (Other + B2C ohne Tag-Match)")
    
    print("\n  Keyword-Verteilung:")
    print(df['keyword'].value_counts(dropna=False).to_string())
    
    # Validation: AI/ML muss aufgeteilt sein, NICHT nur GenAI
    aiml = df[df['industry'] == 'AI/ML']['keyword'].value_counts(dropna=False)
    print(f"\n  AI/ML Aufschlüsselung (erwartet: Mix GenAI/LLM/AgentAI):")
    print(aiml.to_string())

    # ── 3. Funding parsen ──────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 3: Funding-Beträge parsen")
    print("=" * 60)
    
    df['funding_chf'] = df['funding_amount'].apply(parse_funding_amount)
    df['has_funding'] = df['funding_chf'].notna()
    print(f"  Mit Funding:    {df['has_funding'].sum()} Startups")
    print(f"  Ohne Funding:   {(~df['has_funding']).sum()} (UNDISCLOSED/fehlt)")
    print(f"  Total (CHF Mio.): {df['funding_chf'].sum():.1f}")

    # ── 4. Quartal ─────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 4: Quartals-Spalte")
    print("=" * 60)
    
    df = add_quarter_column(df)
    print("\n  Einträge pro Quartal:")
    print(df['quarter'].value_counts().sort_index().to_string())

    # ── 5. Filtern & Speichern ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 5: Filtern + Speichern")
    print("=" * 60)
    
    n_before = len(df)
    df_out = df[df['keyword'].notna()].copy()
    n_removed = n_before - len(df_out)
    print(f"  Entfernt:    {n_removed} Zeilen (Other + B2C ohne Match)")
    print(f"  Verbleibend: {len(df_out)} Startups")
    print(f"  Laut Report erwartet: ~1'388")
    
    OUTPUT_COLS = [
        "startup_name", "industry", "keyword", "layer_type",
        "funding_chf", "has_funding",
        "quarter", "publication_date",
        "canton", "city"
    ]
    
    df_out = df_out[OUTPUT_COLS]
    df_out.to_csv(OUTPUT_FILE, index=False)
    print(f"\n  ✓ Gespeichert: {OUTPUT_FILE}")

    # ── 6. Abschluss-Validation ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)
    
    print(f"  Output:           {OUTPUT_FILE}")
    print(f"  Gesamt Startups:  {len(df_out)}  (erwartet ~1'388)")
    print(f"\n  Keywords:         {sorted(df_out['keyword'].unique())}")
    print(f"\n  Quartale:         {sorted(df_out['quarter'].unique())}")
    print(f"\n  Tech-Layer KWs:   {sorted(df_out[df_out['layer_type']=='tech_layer']['keyword'].unique())}")
    print(f"\n  Industry-Layer:   {sorted(df_out[df_out['layer_type']=='industry_layer']['keyword'].unique())}")
    print(f"\n  Mit Funding:      {df_out['has_funding'].sum()} von {len(df_out)}")
    print("\n" + "=" * 60)
    print("✓ Fertig.")
    print("=" * 60)


if __name__ == "__main__":
    main()
