# Chiara's Contributions

## Swiss Startup Ecosystem Analysis (2023-2026)

This folder contains my contributions to the Data2Dollar project:
- Web scrapers for Swiss startup data
- Data processing pipeline
- Industry trend analysis
- Interactive visualizations

**Author:** Chiara Boehme  
**Date:** April 2026  
**Project:** MBI Gruppenarbeit - Data2Dollar

---

## 📊 Datenquellen & Scraper

### Verwendete Scraper (finale Analyse)
| Scraper | Datei | Beschreibung |
|---------|-------|--------------|
| **Startupticker** | `5_startupticker_scraper_v7_STEP1_ONLY.py` | Schweizer Startup-News & Deals (Hauptquelle) |
| **Venture Kick** | `7_venturekick_scraper_v5_STEP1_ONLY.py` | Schweizer VC-Förderungsdaten |

### Exploriert, aber nicht verwendet
| Scraper | Datei | Grund |
|---------|-------|-------|
| **Kaggle** | `1_kaggle_downloader.py` | Daten zu alt / nicht CH-spezifisch |
| **Y Combinator** | `3_yc_scraper_v2.py` | US-fokussiert, nicht relevant für CH |
| **VCLense** | `2_vclense_scraper.py` | Datenqualität unzureichend, nicht verwendet |

> ⚠️ **Hinweis:** Die Scraper für Kaggle, YC und VCLense wurden initial entwickelt und getestet, aber die Datenqualität war für die Schweizer Startup-Analyse nicht ausreichend. Die finalen Analysen basieren ausschliesslich auf **Startupticker** und **Venture Kick**.

---

## 📁 Rohdaten

Die Grund-Datei mit allen gescrapten Rohdaten liegt in:
```
pfad_a_scraper/data/startupticker_enriched_FINAL.csv  (1564 Zeilen)
```

Die bereinigte & klassifizierte Version für die Webseite:
```
pfad_a_scraper/data/startups_classified_v2.csv  (1327 Zeilen)
```

---

## 📂 Ordnerstruktur

```
chiara/
├── code/
│   ├── 1_data_collection/    ← Scraper (siehe oben)
│   ├── 2_data_processing/    ← Bereinigung, LLM-Extraktion
│   └── 3_analysis/           ← Trend-Analysen
├── docs/                     ← Dokumentation
├── results/                  ← 16 fertige CSV-Dateien
└── visualization/            ← Dashboard-Code
```

---

## 🔗 Verbindung zur Webseite "Lizzys"

Die Daten aus `results/` fliessen in die Webseite (`Webseite Gründerin/`):
- `F1_deal_count_quarterly.csv` → `investments.js`
- `D_momentum.csv` → `opportunity.js` (Ranking-Signale)
- `INVESTMENT_RECOMMENDATIONS.csv` → Fazit-Section

---

## ⚠️ Wichtige Hinweise zur Daten-Interpretation

### GenAI als Kategorie (Methodische Anmerkung)
> **Disclaimer:** Die Kategorie "GenAI" (bzw. "AI/ML" in den Rohdaten) bezeichnet hier **AI-Native Startups** – also Unternehmen, deren Kernprodukt auf Künstlicher Intelligenz basiert.
>
> Technisch ist GenAI eine **Querschnittstechnologie**, die in vielen Branchen angewendet wird (HealthTech+AI, FinTech+AI, etc.). Die 44 Startups in dieser Kategorie wurden von Startupticker.ch als "AI/ML" klassifiziert, da deren Hauptprodukt AI-basiert ist und sich nicht primär einer anderen Branche zuordnen lässt.

### Momentum-Berechnung
Die Momentum-Werte in `D_momentum.csv` basieren auf der **Veränderung des Marktanteils** (nicht der absoluten Deal-Zahlen):
- **FinTech**: -12.3% Momentum bedeutet sinkender *Marktanteil*, obwohl absolute Deals stabil sind
- **HealthTech**: -39.5% Momentum, aber absolute Deals +70% → Markt wächst langsamer als Gesamtmarkt

### Quartals-Daten
- **2026-Q2** enthält nur 5 Deals (Datenerhebung April 2026 → Quartal unvollständig)
- Für Analysen empfohlen: Daten bis **2026-Q1** verwenden

### Datenkonsistenz
| Metrik | chiara/results | Webseite | Status |
|--------|---------------|----------|--------|
| Total Deals | 1'327 | 1'322 | ⚠️ Webseite exkludiert 2026-Q2 |
| Branchen | 14 | 8 (Fokus) | ✅ Webseite zeigt Top-Branchen |
| Zeitraum | Q1/2023–Q2/2026 | Q1/2023–Q1/2026 | ✅ Webseite exkludiert unvollst. Q2 |


