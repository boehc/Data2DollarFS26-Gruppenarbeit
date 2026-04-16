# 🗺️ Datenfluss-Übersicht – Von CSV zu Website

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATENQUELLEN (Bestehend)                              │
└─────────────────────────────────────────────────────────────────────────────────┘

📁 Lizzy/Trends/Trends_Data/
├── keyword_monthly_normalized.csv    → 822 Zeilen, 2023-01 bis 2026-01
│   ├── tech_keyword (GenAI, LLM, AgentAI, Web3, ...)
│   ├── industry_keyword (FinTech, HealthTech, BioTech, ...)
│   └── keyword_pct (% aller Artikel in diesem Monat)
└── articles_classified_t2.csv        → Vollständige Artikel-Daten


📁 chiara/results/
├── F1_deal_count_quarterly.csv       → Deal-Anzahl pro Quartal & Industrie
├── F2_deal_share_quarterly.csv       → Deal-Anteil (%) pro Quartal
├── C_funding_share_pct.csv           → Funding-Anteil (CHF) pro Jahr
├── D_momentum.csv                    → Delta Media vs. Delta VC
├── INVESTMENT_RECOMMENDATIONS.csv    → Buy/Hold/Avoid Signale
└── TOP_WINNERS_LOSERS.csv            → Gewinner/Verlierer Rankings


📁 Curriculum MBI/
└── 0_mbi_curriculum_final.csv        → 86 Kurse mit Keywords & Profilen


┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TRANSFORMATION (Python Scripts)                         │
└─────────────────────────────────────────────────────────────────────────────────┘

Python Script                         Input CSV                     Output JSON
──────────────────────────────────────────────────────────────────────────────────
1️⃣ create_tech_trends.py          → keyword_monthly_normalized → tech_trends.json
2️⃣ create_industry_trends.py      → keyword_monthly_normalized → industry_trends.json  
3️⃣ create_deal_count.py           → F1_deal_count_quarterly   → deal_count.json
4️⃣ create_funding_share.py        → C_funding_share_pct       → funding_share.json
5️⃣ create_momentum_matrix.py      → D_momentum                → momentum_matrix.json
6️⃣ create_co_occurrence.py        → articles_classified_t2    → co_occurrence.json
7️⃣ create_mbi_courses.py          → 0_mbi_curriculum_final    → mbi_courses.json
8️⃣ create_ec_domains.py           → Manuell (EntreComp)       → ec_domains.json


┌─────────────────────────────────────────────────────────────────────────────────┐
│                           JSON DATEN (für Website)                              │
└─────────────────────────────────────────────────────────────────────────────────┘

📁 Webseite Gründerin/data/
├── tech_trends.json              ← Tech-Keywords (GenAI, LLM, ...) pro Quartal
├── industry_trends.json          ← Industry-Keywords (FinTech, ...) pro Quartal
├── deal_count.json               ← Deal-Anzahl pro Quartal & Kategorie
├── funding_share.json            ← Funding-Volumen (CHF) pro Kategorie
├── momentum_matrix.json          ← Bubble Chart (Delta Media vs. VC)
├── co_occurrence.json            ← Heatmap (Tech × Industry)
├── mbi_courses.json              ← Kurse mit ECTS, Keywords, Sektoren
├── ec_domains.json               ← 12 EC-Domains mit MBI-Abdeckung
└── canton_map.json (optional)    ← Kanton-Karte (falls Daten verfügbar)


┌─────────────────────────────────────────────────────────────────────────────────┐
│                            WEBSITE-STRUKTUR                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

📄 index.html (Landing Page)
   Datenquelle: F1_deal_count_quarterly.csv (Metriken)
   ├── Hero: "Wo lohnt sich eine Gründung aus dem MBI?"
   ├── 4 Metriken: 2'817 Artikel | Venture Kick & Swiss Startups | 14 Branchen | 2023–2026
   └── 3 Karten: [Trends] [Investments] [Opportunity]


📄 trends.html (Seite 1: Tech & Industry Trends)
   Datenquelle: tech_trends.json + industry_trends.json
   ├── Section 2.1: Tech-Keyword Timeline (Stacked Area)
   │   └── Keywords: GenAI, AgentAI, LLM, PhysicalAI, Robotics, Web3, ...
   └── Section 2.2: Industry-Keyword Timeline (Multi-Line)
       └── Keywords: FinTech, DefenseTech, HealthTech, BioTech, ...


📄 investments.html (Seite 2: VC Investments Schweiz)
   Datenquelle: deal_count.json + funding_share.json
   ├── Section 3.1: Marktübersicht (Hero-Metriken)
   ├── Section 3.2: Deal Count Top 5 (Stacked Area)
   ├── Section 3.3: Deal Count Einzellinien (Multi-Line)
   ├── Section 3.4: Small Multiples (14 Mini-Sparklines)
   ├── Section 3.5: Funding CHF (Stacked Area)
   ├── Section 3.6: Investment Stages (Stacked Bar)
   └── Section 3.7: Kanton-Karte (Choropleth Map) [OPTIONAL]


📄 opportunity.html (Seite 3: Wo lohnt es sich einzusteigen?)
   Datenquelle: momentum_matrix.json + co_occurrence.json
   ├── Section 4.1: Momentum Matrix (Bubble Chart)
   │   └── X: Δ Media | Y: Δ VC | Size: Funding | 4 Quadranten
   ├── Section 4.2: Co-Occurrence Heatmap
   │   └── Tech × Industry (normalisiert, %)
   └── Section 4.3: Fazit & Empfehlung
       └── "MedTech oder HealthTech mit GenAI in Zürich/Basel"


📄 courses.html (Seite 4: MBI-Kursabgleich)
   Datenquelle: mbi_courses.json + ec_domains.json
   ├── Bereich A: EC Self-Assessment
   │   ├── A.1: 12 EC-Domain-Karten (interaktiv)
   │   ├── A.2: Dynamische Kursliste (basierend auf Lücken)
   │   └── A.3: Radar Chart (MBI-Abdeckung vs. Meine Stärken)
   └── Bereich B: Sektor-Kurse
       ├── B.1: Tab-Navigation (GenAI | HealthTech | MedTech | BioTech | Robotics)
       ├── B.2: Kursliste pro Sektor
       └── B.3: Hinweis-Box (für schwach abgedeckte Sektoren)


┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DATEN-ZU-SEITE MAPPING                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

Website-Seite              Chart/Sektion                     Datenquelle
─────────────────────────────────────────────────────────────────────────────────
index.html                 Hero-Metriken                     F1_deal_count_quarterly.csv

trends.html                Section 2.1 (Tech Timeline)       tech_trends.json
trends.html                Section 2.2 (Industry Timeline)   industry_trends.json

investments.html           Section 3.1 (Marktübersicht)      deal_count.json
investments.html           Section 3.2–3.4 (Deal Count)      deal_count.json
investments.html           Section 3.5 (Funding CHF)         funding_share.json
investments.html           Section 3.6 (Investment Stages)   deal_count.json (stages)
investments.html           Section 3.7 (Kanton-Karte)        canton_map.json [TBD]

opportunity.html           Section 4.1 (Momentum Matrix)     momentum_matrix.json
opportunity.html           Section 4.2 (Co-Occurrence)       co_occurrence.json
opportunity.html           Section 4.3 (Fazit)               INVESTMENT_RECOMMENDATIONS.csv

courses.html               Bereich A (EC Assessment)         ec_domains.json
courses.html               Bereich B (Sektor-Kurse)          mbi_courses.json


┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FEHLENDE DATEN (Manuell)                              │
└─────────────────────────────────────────────────────────────────────────────────┘

⚠️  EC Sector Matrix (ec_domains.json)
    └── Zuordnung: 12 EC-Domains × MBI-Kurse × Sektoren
    └── Erstellen: Manuell basierend auf EntreComp-Framework

⚠️  Canton Map Data (canton_map.json) [OPTIONAL]
    └── Startup-Standorte pro Kanton (Zürich, Basel, Genf, ...)
    └── Falls nicht verfügbar: Sektion 3.7 weglassen


┌─────────────────────────────────────────────────────────────────────────────────┐
│                              NÄCHSTE SCHRITTE                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

1. ✅ Ordner erstellt: Webseite Gründerin/
2. ✅ Prompt gespeichert: PROMPT.md
3. ✅ Datenübersicht: DATA_MAPPING.md + VISUAL_OVERVIEW.md
4. ⏭️ Python-Skripte schreiben (create_*.py)
5. ⏭️ JSON-Daten generieren (data/*.json)
6. ⏭️ HTML/CSS/JS Struktur aufbauen
7. ⏭️ Charts mit Plotly.js implementieren
8. ⏭️ GitHub Pages Deployment
```
