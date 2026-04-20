# 📊 VC und Startup Investments — Schweizer Ökosystem Analyse

**Projekt:** Data2Dollar – MBI Gruppenarbeit FS26  
**Autor:** Chiara Boehme  
**Datum:** April 2026

---

## 🎯 Zusammenfassung

Analyse des **Schweizer Startup-Ökosystems 2023–2026** mit 1'327 Finanzierungsrunden aus 14 Branchen. Ziel: Datenbasierte Gründungsempfehlungen für MBI-Studierende.

### Kernaussagen
| Signal | Branchen | Begründung |
|--------|----------|------------|
| 🟢 **STRONG BUY** | GenAI, Robotics | +168% / +109% Momentum |
| 🟢 **BUY** | BioTech, MedTech | Stabile Marktführer |
| 🟡 **HOLD** | HealthTech, Ecommerce | Neutral |
| 🔴 **AVOID** | ClimateTech, FinTech | Sinkende Dynamik |

---

## 📁 Ordnerstruktur

```
VC und Startup Investments/
├── README.md                 ← Diese Datei
├── code/                     ← Python-Scripts (15 Dateien)
│   ├── 1_data_collection/    ← Scraper
│   ├── 2_data_processing/    ← Bereinigung & LLM
│   └── 3_analysis/           ← Trend-Analyse
├── docs/                     ← Dokumentation (7 Dateien)
│   ├── PROFESSOR_OVERVIEW.md ← ⭐ Kurzübersicht für Bewertung
│   ├── EXECUTIVE_SUMMARY.md  ← Kernaussagen
│   └── ...
├── results/                  ← Finale CSV-Ergebnisse (16 Dateien)
│   ├── SIMPLE_SUMMARY.csv    ← One-Pager
│   ├── INVESTMENT_RECOMMENDATIONS.csv
│   └── ...
├── rohdaten/                 ← Gescrapte Originaldaten
│   ├── startupticker_enriched_FINAL.csv (1564 Zeilen)
│   ├── startups_classified_v2.csv (1327 Zeilen)
│   └── archiv/               ← Ältere Datenversionen
└── archive/                  ← Alte Script-Versionen
    ├── old_scrapers/         ← Frühere Scraper-Iterationen
    ├── old_docs/             ← Entwicklungsdokumentation
    └── ...
```

---

## 📊 Datenquellen

### Verwendet (finale Analyse)
| Quelle | Datei | Beschreibung |
|--------|-------|--------------|
| **Startupticker.ch** | `5_startupticker_scraper_v7_STEP1_ONLY.py` | Hauptquelle: CH Startup-News & Deals |
| **Venture Kick** | `7_venturekick_scraper_v5_STEP1_ONLY.py` | CH VC-Förderungsdaten |

### Exploriert, nicht verwendet
| Quelle | Grund |
|--------|-------|
| Kaggle | Daten zu alt, nicht CH-spezifisch |
| Y Combinator | US-fokussiert |
| VCLense | Datenqualität unzureichend |

---

## ⚠️ Methodische Hinweise

### GenAI als Kategorie
> **Disclaimer:** "GenAI" bezeichnet hier **AI-Native Startups** – Unternehmen deren Kernprodukt auf KI basiert. Technisch ist GenAI eine Querschnittstechnologie, die in vielen Branchen angewendet wird. Die 44 Startups in dieser Kategorie wurden von Startupticker.ch als "AI/ML" klassifiziert.

### Momentum-Berechnung
- Momentum = Veränderung des **Marktanteils** (nicht absolute Deals)
- Beispiel: FinTech -12.3% = sinkender Marktanteil, aber stabile absolute Zahlen

---

## 🚀 Quick Start

### Für Professor (Kurzübersicht)
```
docs/PROFESSOR_OVERVIEW.md    → 2-3 Min Lesezeit
results/SIMPLE_SUMMARY.csv    → One-Page Ergebnisse
```

### Für technische Prüfung
```bash
# Alle Python-Dateien syntaktisch prüfen
cd code && python3 -m py_compile 1_data_collection/*.py 2_data_processing/*.py 3_analysis/*.py

# Daten validieren
python3 -c "import pandas as pd; df=pd.read_csv('rohdaten/startups_classified_v2.csv'); print(f'Total: {len(df)} Deals')"
```

---

## 📎 Wichtige Dateien

| Priorität | Datei | Beschreibung |
|-----------|-------|--------------|
| ⭐⭐⭐ | `docs/PROFESSOR_OVERVIEW.md` | Zusammenfassung für Bewertung |
| ⭐⭐⭐ | `results/INVESTMENT_RECOMMENDATIONS.csv` | Buy/Hold/Avoid Signale |
| ⭐⭐ | `results/SIMPLE_SUMMARY.csv` | One-Pager aller Branchen |
| ⭐⭐ | `rohdaten/startups_classified_v2.csv` | Bereinigte Rohdaten |
| ⭐ | `code/3_analysis/step2_industry_trends.py` | Hauptanalyse-Script |

---

*Erstellt: 20. April 2026*
