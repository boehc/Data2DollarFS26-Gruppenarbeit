# Trends — Tech Media Analysis

Natalie Kmecova | data2dollar | MBI HSG | April 2026

Dieses Modul analysiert globale Tech-Medientrends aus TechCrunch und HackerNews (2023–2026)
und klassifiziert Artikel mit einem empirisch abgeleiteten Zwei-Ebenen-Keyword-System.
Grundlage für den Vergleich mit Schweizer VC-Investitionsdaten (Chiara Muster).

---

## Ordnerstruktur

Trends_Data/                        — Aggregierte Datensätze (Inputs für Analyse)
Trends_Scripts_analysis/            — Klassifikations- und Analyse-Scripts
Trends_Scripts_processing/          — Datenbereinigung und Merge
Trends_Scripts_scrapers/            — Web Scraper für TechCrunch und HackerNews

---

## Dateien

### Trends_Data/

| Datei | Beschreibung |
|-------|-------------|
| `keyword_monthly_normalized.csv` | Normalisierter Keyword-Anteil pro Monat, Quelle und Keyword. Berechnet als keyword_count / total_articles_that_month × 100. Direkte Input-Datei für Trend-Timeline und Momentum Matrix. |
| `articles_classified_t2.csv` | Alle 8'476 klassifizierten Artikel mit tech_layer, industry_layer und Metadaten. 32 MB — nicht im Repo, via Google Drive verfügbar. |

### Trends_Scripts_analysis/

| Datei | Beschreibung |
|-------|-------------|
| `classify_all_articles.py` | Klassifiziert alle Artikel mit dem Zwei-Ebenen-Keyword-System (11 Tech-Keywords, 18 Industry-Keywords). Threshold 2: mind. 2 Keyword-Treffer pro Kategorie. Output: articles_classified_t2.csv. |
| `analyze_top_terms.py` | Berechnet die 200 häufigsten Begriffe pro Jahr aus dem Artikelkorpus. Grundlage für die empirische Keyword-Ableitung. Output: keyword_monthly_normalized.csv. |
| `classify_startups_v2.py` | Wendet das Keyword-System auf Chiaras Startupticker-Datensatz an. Input: startupticker_enriched_FINAL.csv. Output: startups_classified_v2.csv. |

### Trends_Scripts_processing/

| Datei | Beschreibung |
|-------|-------------|
| `merge_all_datasets.py` | Führt alle Quellen (TechCrunch, HackerNews, The Verge, The Next Web) zusammen. Normalisiert Spaltennamen, entfernt Duplikate, setzt year_month-Feld. |
| `split_and_fix_data.py` | Bereinigt den Merged-Datensatz: entfernt Encoding-Fehler, filtert leere Artikel, behebt Substring-Probleme in LLM-Keywords (rag, bert, bard, palm). |

### Trends_Scripts_scrapers/

| Datei | Beschreibung |
|-------|-------------|
| `techcrunch_historical.py` | Scrapy-Spider für TechCrunch. Scrapet 5 Kategorien (startups, venture, apps, artificial-intelligence, security), max. 50 Artikel pro Kategorie pro Monat, Zeitraum 2023–2026. Stoppt automatisch bei Pre-2023 Artikeln. Output: rohe Artikel-CSV mit Titel, URL, Datum, Kategorie, Autor, Excerpt und Artikeltext. |
| `hackernews_historical.py` | Erhebt HackerNews-Artikel über die öffentliche Algolia Search API, Zeitraum 2023–2026. Output: rohe Artikel-CSV im gleichen Format wie TechCrunch. |

---
## Pipeline

Scraper → merge_all_datasets.py → split_and_fix_data.py
                                          ↓
                              classify_all_articles.py
                                          ↓
                              articles_classified_t2.csv
                                          ↓
                              analyze_top_terms.py
                                          ↓
                          keyword_monthly_normalized.csv

---

## Keyword-System

**Tech-Layer (11):** GenAI, AgentAI, LLM, Robotics, Semiconductors, ComputerVision,
PhysicalAI, Web3, QuantumTech, Cybersecurity, Infrastructure

**Industry-Layer (18):** HealthTech, BioTech, MedTech, DigitalHealth, FinTech,
ClimateTech, DefenseTech, EdTech, HRTech, AgriTech, SpaceTech, Ecommerce,
Enterprise, CreatorEconomy, GameTech, MobilityTech, PropTech, LegalTech

**Threshold:** Mind. 2 Keyword-Treffer pro Artikel (Threshold 2).
Robustness Check: T1 = 81.4% Coverage, T2 = 51.5%, Differenz 29.9%.
