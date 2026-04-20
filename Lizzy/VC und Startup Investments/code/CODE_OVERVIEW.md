# 🐍 Code-Übersicht — Daten-Pipeline# Production Code - Swiss Startup Data Pipeline



**Ordner:** `code/`  ## Overview

**Anzahl:** 15 Python-Scripts  This folder contains the production-ready data pipeline for collecting and analyzing Swiss startup ecosystem data (2023-2026).

**Autor:** Chiara Boehme  

**Stand:** April 2026## Pipeline Structure



---### 1_data_collection/

Web scrapers for data collection:

## 📋 Zusammenfassung- `1_kaggle_downloader.py` - Download base datasets from Kaggle

- `2_vclense_scraper.py` - Scrape VClense startup database

Diese Pipeline sammelt, verarbeitet und analysiert Schweizer Startup-Daten (2023–2026). Das Ergebnis sind 16 CSV-Dateien mit Branchen-Trends und Investment-Empfehlungen.- `3_yc_scraper_v2.py` - Y Combinator startup data (FINAL version)

- `5_startupticker_scraper_v7_STEP1_ONLY.py` - StartupTicker scraper (FINAL)

### Pipeline-Ablauf- `7_venturekick_scraper_v5_STEP1_ONLY.py` - VentureKick scraper (FINAL)

```

1_data_collection → 2_data_processing → 3_analysis → results/### 2_data_processing/

     (Scraper)         (Bereinigung)      (Trends)     (CSVs)Data cleaning and processing scripts:

```- `4_merge_and_clean.py` - Merge datasets and remove duplicates

- `8_llm_article_analyzer.py` - LLM-based article content extraction

---- `9_quality_analysis.py` - Data quality checks and validation

- `10_automated_llm_extraction.py` - Automated extraction pipeline

## 📁 Ordnerstruktur- Plus 4 helper scripts for data cleaning



### 1_data_collection/ — Web Scraper (5 Dateien)### 3_analysis/

Analysis and insights:

| Script | Zweck | Status |- `step2_industry_trends.py` - Industry trend analysis (2023-2026)

|--------|-------|--------|- `schweiz_overview.py` - Swiss ecosystem overview

| `1_kaggle_downloader.py` | Kaggle-Datasets herunterladen | ⚠️ Nicht verwendet (zu alt) |

| `2_vclense_scraper.py` | VCLense Startup-Datenbank | ⚠️ Nicht verwendet (Qualität) |## Installation

| `3_yc_scraper_v2.py` | Y Combinator Startups | ⚠️ Nicht verwendet (US-fokus) |

| `5_startupticker_scraper_v7_STEP1_ONLY.py` | **Startupticker.ch** | ✅ **Hauptquelle** |```bash

| `7_venturekick_scraper_v5_STEP1_ONLY.py` | **Venture Kick** | ✅ **Verwendet** |pip install -r requirements.txt

```

> **Hinweis:** Nur Startupticker und Venture Kick wurden für die finale Analyse verwendet. Die anderen Scraper wurden exploriert, aber die Datenqualität war für die Schweizer Analyse nicht ausreichend.

## Usage

---

See `../docs/README_FINAL.md` for detailed usage instructions.

### 2_data_processing/ — Datenverarbeitung (8 Dateien)

## Key Features

| Script | Zweck | Input → Output |- ✅ 5 production web scrapers

|--------|-------|----------------|- ✅ Multi-step data processing pipeline

| `4_merge_and_clean.py` | Daten zusammenführen, Duplikate entfernen | Raw CSVs → Merged CSV |- ✅ LLM-enhanced content extraction

| `8_llm_article_analyzer.py` | LLM-basierte Artikel-Analyse | Artikel → Strukturierte Daten |- ✅ Comprehensive quality validation

| `9_quality_analysis.py` | Datenqualität prüfen | CSV → Quality Report |- ✅ Industry trend analysis across 14 categories

| `10_automated_llm_extraction.py` | Automatisierte LLM-Extraktion | Batch-Verarbeitung |- ✅ 1,327 startups analyzed (2023-2026)

| `clean_data.py` | Allgemeine Datenbereinigung | Raw → Clean |

| `clean_venturekick_data.py` | Venture Kick spezifisch | VK Raw → VK Clean |**Author:** Chiara Boehme  

| `data_quality_analysis.py` | Detaillierte Qualitätsanalyse | CSV → Statistiken |**Date:** April 2026

| `field_completeness_analysis.py` | Vollständigkeitsprüfung | CSV → Completeness % |


#### LLM-Extraktion (GPT-4)
Die Scripts `8_llm_article_analyzer.py` und `10_automated_llm_extraction.py` nutzen GPT-4 um:
- Startup-Namen aus Artikeln zu extrahieren
- Branchen automatisch zu klassifizieren
- Funding-Beträge zu erkennen

---

### 3_analysis/ — Trend-Analyse (2 Dateien)

| Script | Zweck | Output |
|--------|-------|--------|
| `schweiz_overview.py` | Schweizer Ökosystem-Übersicht | Basis-Statistiken |
| `step2_industry_trends.py` | **Hauptanalyse** — Branchen-Trends | 16 CSV-Dateien in `results/` |

#### step2_industry_trends.py — Details
Dieses Script ist das Herzstück der Analyse und berechnet:
- **Marktanteile** pro Branche und Jahr
- **Momentum** (Veränderung der Marktanteile)
- **Rankings** nach Deal-Anzahl und Funding
- **Investment-Empfehlungen** (Buy/Hold/Avoid)

---

## 🔧 Installation

```bash
# Im code/ Ordner
pip install -r requirements.txt
```

### Abhängigkeiten
- `pandas` — Datenverarbeitung
- `requests` — Web Scraping
- `beautifulsoup4` — HTML Parsing
- `openai` — LLM-Extraktion (optional)
- `selenium` — Dynamische Webseiten (optional)

---

## ▶️ Ausführung

### Komplette Pipeline (nicht nötig — Daten bereits vorhanden)
```bash
# 1. Daten sammeln
python 1_data_collection/5_startupticker_scraper_v7_STEP1_ONLY.py
python 1_data_collection/7_venturekick_scraper_v5_STEP1_ONLY.py

# 2. Daten verarbeiten
python 2_data_processing/4_merge_and_clean.py

# 3. Analyse ausführen
python 3_analysis/step2_industry_trends.py
```

### Nur Syntax prüfen
```bash
python3 -m py_compile 1_data_collection/*.py 2_data_processing/*.py 3_analysis/*.py
```

---

## 📊 Output

Die Analyse erzeugt 16 CSV-Dateien in `../results/`:

| Datei | Beschreibung |
|-------|--------------|
| `SIMPLE_SUMMARY.csv` | One-Pager aller Branchen |
| `INVESTMENT_RECOMMENDATIONS.csv` | Buy/Hold/Avoid Signale |
| `D_momentum.csv` | Momentum-Werte |
| `F1_deal_count_quarterly.csv` | Quartals-Daten |
| ... | (12 weitere Dateien) |

---

## ✅ Qualitätssicherung

- [x] Alle 15 Python-Dateien syntaktisch korrekt
- [x] Keine externen Abhängigkeiten zur Laufzeit (Daten bereits vorhanden)
- [x] Dokumentation in jedem Script-Header
- [x] Konsistente Namenskonvention (Nummern-Präfix)

---

*Erstellt: April 2026*
