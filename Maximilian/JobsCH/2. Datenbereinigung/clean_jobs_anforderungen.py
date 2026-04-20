"""
================================================================================
JOBS ANFORDERUNGEN – DATA CLEANING & FILTERING
================================================================================
Datenquelle:  jobs_anforderungen_raw.csv (Scraping von jobs.ch)
Ziel:         Bereinigter Datensatz für Business-Absolventen
Autor:        Data Cleaning Pipeline
Datum:        2026-03-31
================================================================================
"""

# =============================================================================
# 1. IMPORT
# =============================================================================
import pandas as pd
import numpy as np
import re

# =============================================================================
# 2. DATEN EINLESEN
# =============================================================================
# Encoding: UTF-8 (Standard), Separator: Komma (Standard)
# Pfade relativ zur Skript-Datei, damit es von überall aufrufbar ist
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "jobs_anforderungen_raw.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "jobs_anforderungen_clean.csv")

df_raw = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("SCHRITT 1: ROHDATEN-INSPEKTION")
print("=" * 70)
print(f"\nDatei: {INPUT_FILE}")
print(f"Shape: {df_raw.shape[0]} Zeilen × {df_raw.shape[1]} Spalten")
print(f"\nSpalten: {df_raw.columns.tolist()}")
print(f"\nDatentypen:")
print(df_raw.dtypes)
print(f"\nFehlende Werte pro Spalte:")
print(df_raw.isnull().sum())
print(f"\nDuplikate (alle Spalten): {df_raw.duplicated().sum()}")
print(f"Duplikate (URL):          {df_raw.duplicated(subset='url').sum()}")

# =============================================================================
# 3. DATA CLEANING
# =============================================================================
print("\n" + "=" * 70)
print("SCHRITT 2: DATA CLEANING")
print("=" * 70)

# Arbeitskopie erstellen
df = df_raw.copy()

# --- 3a) Zeilen ohne erkannte Anforderungen entfernen ---
mask_keine_anf = df["anforderungen"] == "(keine Anforderungen erkannt)"
n_keine_anf = mask_keine_anf.sum()
print(f"\n[CLEAN] Zeilen mit '(keine Anforderungen erkannt)': {n_keine_anf}")
df = df[~mask_keine_anf].reset_index(drop=True)

# --- 3b) Missing Values behandeln ---
# unternehmen (1 NaN), arbeitsort (2 NaN), veroeffentlicht_am (1 NaN)
# → Behalten, da die Anforderungen vorhanden sind (Kerninfo für Analyse)
n_missing_before = df.isnull().sum().sum()
df["unternehmen"] = df["unternehmen"].fillna("(unbekannt)")
df["arbeitsort"] = df["arbeitsort"].fillna("(unbekannt)")
df["veroeffentlicht_am"] = df["veroeffentlicht_am"].fillna(pd.NaT)
print(f"[CLEAN] Missing Values gefüllt: {n_missing_before} → 0 verbleibend")

# --- 3c) Datentyp-Korrektur: veroeffentlicht_am als datetime ---
# utc=True nötig, da gemischte Zeitzonen im ISO-Format vorliegen (+01:00, +02:00)
df["veroeffentlicht_am"] = pd.to_datetime(df["veroeffentlicht_am"], utc=True, errors="coerce")
print(f"[CLEAN] 'veroeffentlicht_am' konvertiert zu datetime (UTC)")

# --- 3d) Whitespace in Textspalten bereinigen ---
text_cols = ["titel", "unternehmen", "arbeitsort", "anforderungen"]
for col in text_cols:
    df[col] = df[col].str.strip()
print(f"[CLEAN] Whitespace bereinigt in: {text_cols}")

print(f"\nNach Basis-Cleaning: {df.shape[0]} Zeilen verbleibend")

# =============================================================================
# 4. FILTERUNG – Nur für Business-Absolventen relevante Stellen
# =============================================================================
print("\n" + "=" * 70)
print("SCHRITT 3: FILTERUNG")
print("=" * 70)

# Anforderungstext in Kleinbuchstaben für Pattern-Matching
anf_lower = df["anforderungen"].str.lower()

# -------------------------------------------------------------------------
# FILTER 1: Stellen die "noch im Studium" voraussetzen → ENTFERNEN
#            (Datensatz soll nur Stellen für Absolventen enthalten)
# -------------------------------------------------------------------------
# Patterns, die darauf hindeuten, dass jemand noch studiert
studierend_patterns = [
    r"werkstudent",                          # Werkstudent/in
    r"du\s+bist\s+(?:aktuell\s+)?(?:bachelor|master)?[-\s]*student",
    r"aktuell\s+(?:ein[ea]?\s+)?(?:bachelor|master)?[-\s]*student",
    r"noch\s+(?:im|mindestens)\s+.*studi",   # "noch im Studium", "noch mindestens 12 Monate studieren"
    r"eingeschrieben",                        # "an einer Universität eingeschrieben"
    r"im\s+letzten\s+studienjahr",            # "im letzten Studienjahr"
    r"studierst\s+noch",                      # "studierst noch mindestens..."
    r"weiter\s+zu\s+studieren",               # "planst, weiter zu studieren"
    r"laufendes?\s+studium",                  # "laufendes Studium"
    r"student.in\s+an\s+einer",               # "Student*in an einer Universität"
]
# Kombiniertes Pattern
studierend_regex = "|".join(studierend_patterns)
mask_studierend = anf_lower.str.contains(studierend_regex, regex=True, na=False)

# Zusätzlich: Titel prüfen (Werkstudent im Titel ist eindeutig)
titel_lower = df["titel"].str.lower()
mask_titel_studierend = titel_lower.str.contains(
    r"werkstudent|working\s+student", regex=True, na=False
)

mask_filter_studierend = mask_studierend | mask_titel_studierend
n_studierend = mask_filter_studierend.sum()

print(f"\n[FILTER 1] Stellen für Studierende (nicht Absolventen): {n_studierend}")
if n_studierend > 0:
    print("  Betroffene Stellen:")
    for idx in df[mask_filter_studierend].index:
        print(f"    - [{idx}] {df.loc[idx, 'titel']}")

# -------------------------------------------------------------------------
# FILTER 2: Stellen mit ≥3 Jahre Berufserfahrung → ENTFERNEN
# -------------------------------------------------------------------------
# Pattern 1: Explizite Jahreszahlen (deutsch + englisch)
#   "3 Jahre Erfahrung", "5+ Jahre Berufserfahrung", "3-5 years experience"
#   Auch: "10+ years of global leadership experience", "6 Jahre Berufs- und Führungserfahrung"
exp_patterns = [
    # "X Jahre/years ... erfahrung/experience" (bis zu 5 Wörter dazwischen, inkl. Komposita)
    r"(\d+)\+?\s*(?:[-–]\s*\d+\s*)?(?:jahre?|years?)\s+(?:[\w,-]+\s+){0,5}[\w-]*(?:erfahrung|experience|praxis)",
    # "X-jährige(r) ... Erfahrung" (Adjektivform, z.B. "10-jähriger Bank-Erfahrung")
    r"(\d+)[-\s]?jährig\w*\s+(?:[\w,-]+\s+){0,3}[\w-]*(?:erfahrung|experience)",
    # "X+ years in/of ..." (Englisch, auch ohne "experience" direkt danach)
    r"(\d+)\+?\s*(?:[-–]\s*\d+\s*)?years?\s+(?:of|in)\b",
    # Umgekehrte Reihenfolge: "Erfahrung ... X Jahre" (z.B. "Du hast Erfahrung. Ob 5 oder 25 Jahre")
    r"(?:erfahrung|experience)\w*[.\s]+(?:[\w,-]+\s+){0,8}(\d+)\s*(?:[-–oder]+\s*\d+\s*)?(?:jahre?|years?)",
]

def hat_hohe_erfahrung(text):
    """Prüft ob ≥3 Jahre explizit gefordert werden."""
    if pd.isna(text):
        return False
    text_l = text.lower()
    for pattern in exp_patterns:
        for m in re.finditer(pattern, text_l):
            try:
                if int(m.group(1)) >= 3:
                    return True
            except (ValueError, IndexError):
                pass
    return False

mask_exp_explicit = df["anforderungen"].apply(hat_hohe_erfahrung)

# Pattern 2: "mehrjährige (Berufs-)Erfahrung" → In der Praxis typischerweise 3+ Jahre
#   Auch Komposita wie "Bank-Erfahrung", "Führungserfahrung"
mask_exp_mehrjaehrig = anf_lower.str.contains(
    r"mehrj.hrig\w*\s+(?:[\w,-]+\s+){0,3}[\w-]*erfahrung", regex=True, na=False
)

# Pattern 3: "langjährige Erfahrung" → definitiv 5+ Jahre
mask_exp_langjaehrig = anf_lower.str.contains(
    r"langj.hrig\w*\s+(?:[\w,-]+\s+){0,3}[\w-]*erfahrung", regex=True, na=False
)

# Pattern 4: Englisch "extensive/significant/proven track record/seasoned experience"
mask_exp_extensive_en = anf_lower.str.contains(
    r"(?:extensive|significant|substantial|deep|seasoned)\s+(?:[\w-]+\s+){0,3}experience",
    regex=True, na=False
)

# Pattern 5: "track record" (impliziert signifikante Erfahrung)
mask_exp_track_record = anf_lower.str.contains(
    r"(?:proven\s+)?track\s+record", regex=True, na=False
)

# Kombination: Explizit ≥3 ODER mehrjährig ODER langjährig ODER extensive ODER track record
mask_filter_erfahrung = (
    mask_exp_explicit | mask_exp_mehrjaehrig | mask_exp_langjaehrig
    | mask_exp_extensive_en | mask_exp_track_record
)
n_erfahrung = mask_filter_erfahrung.sum()

print(f"\n[FILTER 2] Stellen mit ≥3 Jahre / mehrjährige Berufserfahrung: {n_erfahrung}")
print(f"  - Davon explizit ≥3 Jahre:     {mask_exp_explicit.sum()}")
print(f"  - Davon 'mehrjährig':           {mask_exp_mehrjaehrig.sum()}")
print(f"  - Davon 'langjährig':           {mask_exp_langjaehrig.sum()}")
print(f"  - Davon 'extensive' (EN):       {mask_exp_extensive_en.sum()}")
print(f"  - Davon 'track record':         {mask_exp_track_record.sum()}")

# -------------------------------------------------------------------------
# FILTER 3: Stellen mit nicht-Business Qualifikation → ENTFERNEN
#            (Behalten: BWL, Wirtschaftsinformatik, Business Innovation etc.)
# -------------------------------------------------------------------------
# Strategie:
# 1. Identifiziere Zeilen, die ein Studium/Abschluss/Ausbildung explizit fordern
# 2. Prüfe ob eine Business-kompatible Fachrichtung akzeptiert wird → behalten
# 3. Prüfe ob technische/nicht-Business Studiengänge oder Berufsausbildungen
#    (EFZ, Lehre, Grundausbildung, Fachausweis, HTL) gefordert werden → entfernen

# Akzeptierte Fachrichtungen (Business-kompatibel, Hochschulniveau)
akzeptiert_pattern = (
    r"betriebswirtschaft|bwl|business|wirtschaftsinformatik|"
    r"wirtschaftswissenschaft|wirtschafts\W|vwl|volkswirtschaft|"
    r"management|ökonomie|ekonomie|commerce|finance|controlling|"
    r"wirtschaftsing|wirtschaftsrecht"
)

# Rein technische / naturwissenschaftliche Fachrichtungen (Hochschulniveau)
technisch_studium_patterns = [
    # Informatik OHNE "Wirtschafts-" davor
    r"(?<!wirtschafts)informatik(?:er)?(?:\s*(?:studium|ausbildung|abschluss|efz|hf\b|fh\b))",
    r"(?:studium|abschluss|ausbildung|bachelor|master|diploma?)\s+(?:in\s+|der\s+)?informatik(?!\s*,\s*wirtschaftsinformatik)",
    r"informatik[\s-]*ausbildung",
    # Ingenieurwissenschaften (deutsch + englisch)
    r"(?:maschinenbau|elektrotechnik|verfahrenstechnik|bauingenieur|mechanical\s+engineering|electrical\s+engineering)",
    r"\bengineering\b",
    r"\bindustrial\s+engineering\b",
    r"\boperations\s+research\b",
    # Architektur / Bauwesen
    r"architektur",
    r"bauingenieurwesen",
    r"hochbauzeichner|konstrukteur",
    # Elektronik / Automation / Systeminformatik
    r"\belektronik\b",
    r"\bsysteminformatik\b",
    r"\bautomation\b",
    r"\bmechatronik\b",
    # Naturwissenschaften
    r"(?:physik|chemie|biologie|biochemie)(?:\s*(?:studium|abschluss))?",
    # Computer Science (englisch, ohne Business-Kontext)
    r"computer\s+science",
    # Medizin / Gesundheit
    r"(?:medizin|pflege|gesundheitswissenschaft|pharma)",
    # Robotik, Data Science (wenn als Studiengang)
    r"(?:robotik|robotics)\s+(?:studium|engineer)",
]

# Patterns für spezifische Berufsausbildungen / Lehren (nicht Hochschulniveau)
berufsausbildung_patterns = [
    # Technische/Kaufmännische Grundausbildung
    r"technische\w?\s+grundausbildung",
    r"kaufmännische\w?\s+grundausbildung",
    # Lehrabschluss / Berufsausbildung als spezifischer Beruf
    r"(?:lehr|berufs)abschluss\s+als\b",
    r"berufsausbildung\s+als\b",
    r"(?:abgeschlossene?|erfolgreiche?r?)\s+(?:\w+\s+)?ausbildung\s+als\b",
    r"(?:abgeschlossene?|erfolgreiche?r?)\s+(?:\w+\s+)?lehre\s+(?:als|im|in)\b",
    # EFZ (Eidgenössisches Fähigkeitszeugnis) – Schweizer Berufslehre
    r"\w+(?:[*:/-]\w+)?\s+efz\b",
    # Fachausweis (eidgenössischer Fachausweis)
    r"(?:eidgenössisch\w*\s+)?fachausweis",
    # HTL (Höhere Technische Lehranstalt)
    r"\bhtl\b",
    # Spezifische technische Berufe in Ausbildungskontexten
    r"(?:ausbildung|lehre|lehrabschluss)\s+(?:\w+\s+){0,3}(?:elektro\w*|informatik\w*|polymechanik\w*|konstrukteur|zeichner\w*|installateur\w*|techniker\w*|automatik\w*|schreiner\w*|schlosser\w*|sanitär\w*|planer\w*)",
]

def ist_nicht_business_qualifikation(text):
    """
    Prüft ob ein Stellenanforderungstext spezifische nicht-Business
    Qualifikationen fordert (ohne Business-Alternative).

    Filtert:
    1. Rein technische/naturwiss. Studiengänge (ohne Business-Alternative)
    2. Spezifische Berufsausbildungen (EFZ, Lehre, Grundausbildung, Fachausweis, HTL)
    
    Gibt True zurück, wenn die Stelle gefiltert werden soll.
    """
    if pd.isna(text):
        return False
    text_l = text.lower()
    
    # Prüfe ob eine akzeptierte Business-Fachrichtung genannt wird
    hat_akzeptiert = bool(re.search(akzeptiert_pattern, text_l))
    if hat_akzeptiert:
        return False  # Business-kompatibel → behalten
    
    # ── Check 1: Spezifische Berufsausbildungen / berufliche Grundbildung ──
    for pattern in berufsausbildung_patterns:
        if re.search(pattern, text_l):
            return True
    
    # ── Check 2: Rein technische Studiengänge ──
    # Prüfe zuerst, ob überhaupt ein Studium/Abschluss gefordert wird
    hat_studium_ref = bool(re.search(
        r"studium|abschluss|bachelor|master|hochschul|universit|fachhochschul|"
        r"ausbildung\s+(?:in|als|im)|degree|diploma",
        text_l
    ))
    if hat_studium_ref:
        for pattern in technisch_studium_patterns:
            if re.search(pattern, text_l):
                return True
    
    return False

mask_filter_technisch = df["anforderungen"].apply(ist_nicht_business_qualifikation)
n_technisch = mask_filter_technisch.sum()

print(f"\n[FILTER 3] Stellen mit nicht-Business Qualifikation: {n_technisch}")
if n_technisch > 0:
    print("  Beispiele (max. 10):")
    for idx in df[mask_filter_technisch].head(10).index:
        # Zeige den relevanten Qualifikations-Kontext
        matches = re.findall(
            r".{0,40}(?:studium|abschluss|ausbildung|bachelor|master|degree|efz|lehre|grundausbildung|fachausweis).{0,60}",
            df.loc[idx, "anforderungen"], re.IGNORECASE
        )
        context = matches[0] if matches else df.loc[idx, "anforderungen"][:100]
        print(f"    - [{idx}] {df.loc[idx, 'titel']}")
        print(f"      → ...{context}...")

# -------------------------------------------------------------------------
# ALLE FILTER KOMBINIEREN UND ANWENDEN
# -------------------------------------------------------------------------
print("\n" + "-" * 70)
mask_filter_gesamt = mask_filter_studierend | mask_filter_erfahrung | mask_filter_technisch

# Überlappung analysieren
print("\nÜberlappungs-Analyse der Filter:")
print(f"  Nur 'Studierende':        {(mask_filter_studierend & ~mask_filter_erfahrung & ~mask_filter_technisch).sum()}")
print(f"  Nur 'Erfahrung ≥3J':      {(mask_filter_erfahrung & ~mask_filter_studierend & ~mask_filter_technisch).sum()}")
print(f"  Nur 'Technisch':          {(mask_filter_technisch & ~mask_filter_studierend & ~mask_filter_erfahrung).sum()}")
print(f"  Mehrere Filter:           {(mask_filter_gesamt.sum() - (mask_filter_studierend & ~mask_filter_erfahrung & ~mask_filter_technisch).sum() - (mask_filter_erfahrung & ~mask_filter_studierend & ~mask_filter_technisch).sum() - (mask_filter_technisch & ~mask_filter_studierend & ~mask_filter_erfahrung).sum())}")
print(f"\n  GESAMT ZU ENTFERNEN:      {mask_filter_gesamt.sum()}")

# Filter anwenden
df_clean = df[~mask_filter_gesamt].reset_index(drop=True)

print(f"\n  Zeilen vorher:  {df.shape[0]}")
print(f"  Zeilen nachher: {df_clean.shape[0]}")
print(f"  Entfernt:       {df.shape[0] - df_clean.shape[0]}")

# =============================================================================
# 5. DATENQUALITÄTS-REPORT
# =============================================================================
print("\n" + "=" * 70)
print("SCHRITT 4: DATENQUALITÄTS-REPORT (BEREINIGTER DATENSATZ)")
print("=" * 70)

print(f"\nShape: {df_clean.shape}")
print(f"\nDatentypen:")
print(df_clean.dtypes)
print(f"\nFehlende Werte:")
print(df_clean.isnull().sum())
print(f"\nStatistische Übersicht (Datum):")
print(f"  Frühestes Datum: {df_clean['veroeffentlicht_am'].min()}")
print(f"  Spätestes Datum: {df_clean['veroeffentlicht_am'].max()}")
print(f"\nTop 10 Arbeitsorte:")
print(df_clean["arbeitsort"].value_counts().head(10))
print(f"\nAnforderungen-Sektionen (bereinigte Daten):")
print(df_clean["anforderungen_sektion"].value_counts().head(10))

# =============================================================================
# 6. ZUSAMMENFASSUNG DER PIPELINE
# =============================================================================
print("\n" + "=" * 70)
print("ZUSAMMENFASSUNG DER CLEANING-PIPELINE")
print("=" * 70)
ueberlappung = (n_studierend + mask_filter_erfahrung.sum() + n_technisch) - mask_filter_gesamt.sum()
print(f"""
  Rohdaten:                          {df_raw.shape[0]} Zeilen
  ─────────────────────────────────────────────
  - '(keine Anforderungen erkannt)': -{n_keine_anf} Zeilen
  - Stellen für Studierende:         -{n_studierend} Zeilen
  - ≥3 Jahre Berufserfahrung:        -{mask_filter_erfahrung.sum()} Zeilen  (inkl. 'mehrjährig')
  - Rein technischer Studiengang:    -{n_technisch} Zeilen
  - (Überlappung zwischen Filtern)   +{ueberlappung} (nicht doppelt gezählt)
  ─────────────────────────────────────────────
  Gefiltert (3 Filter kombiniert):   -{mask_filter_gesamt.sum()} Zeilen
  Bereinigte Daten:                  {df_clean.shape[0]} Zeilen
""")

# =============================================================================
# 7. EXPORT
# =============================================================================
df_clean.to_csv(OUTPUT_FILE, index=False)
print(f"[EXPORT] Bereinigte Daten gespeichert: {OUTPUT_FILE}")
print(f"         {df_clean.shape[0]} Zeilen × {df_clean.shape[1]} Spalten")

# Optional: Auch die gefilterten Zeilen separat speichern (zur Kontrolle)
df_removed = df[mask_filter_gesamt].copy()
df_removed["filter_grund"] = ""
df_removed.loc[mask_filter_studierend, "filter_grund"] += "studierende;"
df_removed.loc[mask_filter_erfahrung, "filter_grund"] += "erfahrung_3plus;"
df_removed.loc[mask_filter_technisch, "filter_grund"] += "technisch;"
df_removed.to_csv(os.path.join(SCRIPT_DIR, "jobs_anforderungen_gefiltert.csv"), index=False)
print(f"[EXPORT] Gefilterte Zeilen (zur Kontrolle): jobs_anforderungen_gefiltert.csv")
print(f"         {df_removed.shape[0]} Zeilen")
