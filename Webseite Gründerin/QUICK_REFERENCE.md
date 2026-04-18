# 🎯 Quick Reference – Daten-zu-Website Mapping

## 📊 Übersicht: Welche Daten wohin?

| # | Website-Seite | Sektion | Benötigte Daten | Quelle |
|---|---------------|---------|----------------|--------|
| 1 | `index.html` | Hero-Metriken | Anzahl Artikel, Deals, Branchen | `F1_deal_count_quarterly.csv` |
| 2 | `trends.html` | Tech-Keyword Timeline | GenAI, LLM, AgentAI, Web3, ... (% pro Quartal) | `keyword_monthly_normalized.csv` |
| 3 | `trends.html` | Industry-Keyword Timeline | FinTech, HealthTech, BioTech, ... (% pro Quartal) | `keyword_monthly_normalized.csv` |
| 4 | `investments.html` | Deal Count Charts | Deals pro Quartal & Kategorie | `F1_deal_count_quarterly.csv` |
| 5 | `investments.html` | Funding CHF Chart | Funding-Volumen (CHF) pro Kategorie | `C_funding_share_pct.csv` |
| 6 | `investments.html` | Investment Stages | Pre-Seed, Seed, Series A/B/C, ... | `F1_deal_count_quarterly.csv` (stages) |
| 7 | `investments.html` | Kanton-Karte | Dominante Industrie pro Kanton | ⚠️ **FEHLT** (manuell ergänzen) |
| 8 | `opportunity.html` | Momentum Matrix | Δ Media vs. Δ VC, Funding-Volumen | `D_momentum.csv` |
| 9 | `opportunity.html` | Co-Occurrence Heatmap | Tech × Industry (normalisiert, %) | `articles_classified_t2.csv` |
| 10 | `opportunity.html` | Fazit & Empfehlung | Buy/Hold/Avoid Signale | `INVESTMENT_RECOMMENDATIONS.csv` |
| 11 | `courses.html` | EC Self-Assessment | 12 EC-Domains, MBI-Abdeckung | ⚠️ **FEHLT** (manuell erstellen) |
| 12 | `courses.html` | Sektor-Kurse | Kurse pro Sektor (GenAI, HealthTech, ...) | `0_mbi_curriculum_final.csv` |

---

## 📁 Datenquellen-Verzeichnis

### ✅ **Vorhanden:**
```
Lizzy/Trends/Trends_Data/
├── keyword_monthly_normalized.csv    (Tech & Industry Trends)
└── articles_classified_t2.csv        (Co-Occurrence Heatmap)

chiara/results/
├── F1_deal_count_quarterly.csv       (Deal Count)
├── F2_deal_share_quarterly.csv       (Deal Share %)
├── C_funding_share_pct.csv           (Funding CHF)
├── D_momentum.csv                    (Momentum Matrix)
├── INVESTMENT_RECOMMENDATIONS.csv    (Empfehlungen)
└── TOP_WINNERS_LOSERS.csv            (Rankings)

Curriculum MBI/
└── 0_mbi_curriculum_final.csv        (86 MBI-Kurse)
```

### ⚠️ **Fehlt (manuell erstellen):**
```
data/ec_domains.json          → 12 EC-Domains mit MBI-Abdeckung
data/sector_matrix.json       → EC-Domains × Sektoren × Kurse
data/canton_map.json          → Kanton-Karte (OPTIONAL)
```

---

## 🔄 Transformations-Pipeline

```
CSV-Dateien (roh)
    ↓
Python-Skripte (create_*.py)
    ↓
JSON-Dateien (Webseite Gründerin/data/)
    ↓
Plotly.js Charts (HTML/JS)
```

### Python-Skripte (müssen erstellt werden):
1. `create_tech_trends.py` → `tech_trends.json`
2. `create_industry_trends.py` → `industry_trends.json`
3. `create_deal_count.py` → `deal_count.json`
4. `create_funding_share.py` → `funding_share.json`
5. `create_momentum_matrix.py` → `momentum_matrix.json`
6. `create_co_occurrence.py` → `co_occurrence.json`
7. `create_mbi_courses.py` → `mbi_courses.json`
8. `create_ec_domains.py` → `ec_domains.json` *(manuell)*

---

## 🎨 Website-Struktur

```
Webseite Gründerin/
├── index.html              → Landing Page
├── trends.html             → Tech & Industry Trends
├── investments.html        → VC Investments Schweiz
├── opportunity.html        → Wo einsteigen?
├── courses.html            → MBI-Kursabgleich
├── css/
│   ├── main.css
│   ├── nav.css
│   └── charts.css
├── js/
│   ├── main.js
│   ├── charts/
│   │   ├── tech-trends.js
│   │   ├── deal-count.js
│   │   ├── momentum-matrix.js
│   │   └── co-occurrence.js
│   └── components/
│       ├── nav.js
│       ├── key-message.js
│       └── course-card.js
└── data/
    ├── tech_trends.json
    ├── industry_trends.json
    ├── deal_count.json
    ├── funding_share.json
    ├── momentum_matrix.json
    ├── co_occurrence.json
    ├── mbi_courses.json
    └── ec_domains.json
```

---

## ✅ Checkliste

### **Datenvorbereitung:**
- [ ] Python-Skripte schreiben (create_*.py)
- [ ] JSON-Dateien generieren (data/*.json)
- [ ] EC-Domains manuell erstellen (ec_domains.json)
- [ ] Sektor-Matrix manuell erstellen (sector_matrix.json)
- [ ] Kanton-Karte prüfen (falls verfügbar)

### **Website-Entwicklung:**
- [ ] HTML-Struktur (5 Pages)
- [ ] CSS Design-System (main.css)
- [ ] Navigation (nav.js)
- [ ] Plotly.js Charts (tech-trends.js, deal-count.js, ...)
- [ ] Interaktive Komponenten (EC Self-Assessment)
- [ ] Mobile Responsive (Breakpoints 768px, 1200px)

### **Deployment:**
- [ ] GitHub Pages Setup
- [ ] Relative Pfade prüfen
- [ ] Performance-Optimierung (Lazy-Loading)
- [ ] Barrierefreiheit (Alt-Texte, ARIA-Labels)

---

## 🚀 Nächste Schritte

1. ✅ **Ordner erstellt:** `Webseite Gründerin/`
2. ✅ **Dokumentation:** `PROMPT.md`, `DATA_MAPPING.md`, `VISUAL_OVERVIEW.md`, `QUICK_REFERENCE.md`
3. ⏭️ **Python-Skripte:** CSV → JSON Transformation
4. ⏭️ **Website:** HTML/CSS/JS Entwicklung
5. ⏭️ **Deployment:** GitHub Pages

---

*Erstellt: April 2026 | Projekt: data2dollar – Pfad A: Gründen*
