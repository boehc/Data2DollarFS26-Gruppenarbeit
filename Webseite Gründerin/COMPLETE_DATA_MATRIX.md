# 📊 Komplette Daten-Matrix – Wo wird was verwendet?

## 🎯 Übersicht: Datenquellen → Website-Komponenten

| Website-Page | Sektion | Chart-Typ | Datenquelle (CSV) | JSON-Output | Python-Skript |
|--------------|---------|-----------|-------------------|-------------|---------------|
| **index.html** | Hero-Metriken | Zahlen-Karten | `F1_deal_count_quarterly.csv` | — | — |
| **index.html** | Navigations-Karten | 3 Karten | — | — | — |
| **trends.html** | Section 2.1 | Stacked Area | `keyword_monthly_normalized.csv` | `tech_trends.json` | `create_tech_trends.py` |
| **trends.html** | Section 2.2 | Multi-Line | `keyword_monthly_normalized.csv` | `industry_trends.json` | `create_industry_trends.py` |
| **investments.html** | Section 3.1 | Hero-Metriken | `F1_deal_count_quarterly.csv` | `deal_count.json` | `create_deal_count.py` |
| **investments.html** | Section 3.2 | Stacked Area | `F1_deal_count_quarterly.csv` | `deal_count.json` | `create_deal_count.py` |
| **investments.html** | Section 3.3 | Multi-Line | `F1_deal_count_quarterly.csv` | `deal_count.json` | `create_deal_count.py` |
| **investments.html** | Section 3.4 | Small Multiples | `F1_deal_count_quarterly.csv` | `deal_count.json` | `create_deal_count.py` |
| **investments.html** | Section 3.5 | Stacked Area | `C_funding_share_pct.csv` | `funding_share.json` | `create_funding_share.py` |
| **investments.html** | Section 3.6 | Stacked Bar | `F1_deal_count_quarterly.csv` (stages) | `deal_count.json` | `create_deal_count.py` |
| **investments.html** | Section 3.7 | Choropleth Map | ⚠️ **FEHLT** | `canton_map.json` | ⚠️ **Manuell** |
| **opportunity.html** | Section 4.1 | Bubble Chart | `D_momentum.csv` | `momentum_matrix.json` | `create_momentum_matrix.py` |
| **opportunity.html** | Section 4.2 | Heatmap | `articles_classified_t2.csv` | `co_occurrence.json` | `create_co_occurrence.py` |
| **opportunity.html** | Section 4.3 | Empfehlungs-Karte | `INVESTMENT_RECOMMENDATIONS.csv` | — | — |
| **courses.html** | Bereich A.1 | 12 EC-Karten | ⚠️ **Manuell** | `ec_domains.json` | `create_ec_domains.py` |
| **courses.html** | Bereich A.2 | Kursliste | `0_mbi_curriculum_final.csv` | `mbi_courses.json` | `create_mbi_courses.py` |
| **courses.html** | Bereich A.3 | Radar Chart | ⚠️ **Manuell** | `ec_domains.json` | `create_ec_domains.py` |
| **courses.html** | Bereich B.1 | Tab-Navigation | `0_mbi_curriculum_final.csv` | `mbi_courses.json` | `create_mbi_courses.py` |
| **courses.html** | Bereich B.2 | Kurskarten | `0_mbi_curriculum_final.csv` | `mbi_courses.json` | `create_mbi_courses.py` |

---

## 📁 Datenquellen-Details

### 1️⃣ **Lizzy/Trends/Trends_Data/keyword_monthly_normalized.csv**
**Spalten:**
- `year_month` (2023-01 bis 2026-01)
- `source` (TechCrunch, HackerNews)
- `tech_keyword` (GenAI, LLM, AgentAI, Web3, Blockchain, ...)
- `industry_keyword` (FinTech, HealthTech, BioTech, ClimateTech, ...)
- `article_count` (Anzahl Artikel mit diesem Keyword)
- `total_articles_that_month` (Gesamt-Artikel in diesem Monat)
- `keyword_pct` (Prozent-Anteil des Keywords)

**Verwendung:**
- ✅ Tech-Keyword Timeline (trends.html – Section 2.1)
- ✅ Industry-Keyword Timeline (trends.html – Section 2.2)

---

### 2️⃣ **Lizzy/Trends/Trends_Data/articles_classified_t2.csv**
**Spalten:**
- Vollständige Artikel-Daten mit Klassifizierung
- Tech-Keywords pro Artikel
- Industry-Keywords pro Artikel

**Verwendung:**
- ✅ Co-Occurrence Heatmap (opportunity.html – Section 4.2)

---

### 3️⃣ **chiara/results/F1_deal_count_quarterly.csv**
**Spalten:**
- Quartale (2023 Q1 bis 2026 Q1)
- Kategorien (BioTech, FinTech, ClimateTech, HealthTech, GenAI, ...)
- Deal-Anzahl pro Quartal & Kategorie

**Verwendung:**
- ✅ Hero-Metriken (index.html + investments.html)
- ✅ Deal Count Charts (investments.html – Section 3.2–3.4)
- ✅ Investment Stages (investments.html – Section 3.6)

---

### 4️⃣ **chiara/results/C_funding_share_pct.csv**
**Spalten:**
- Jahre (2023–2026)
- Kategorien (BioTech, FinTech, ClimateTech, ...)
- Funding-Anteil (% oder CHF)

**Verwendung:**
- ✅ Funding CHF Stacked Area (investments.html – Section 3.5)

---

### 5️⃣ **chiara/results/D_momentum.csv**
**Spalten:**
- `industry` (Kategorie)
- `delta_media` (Δ Medien-Anteil 2023→2025)
- `delta_vc` (Δ VC-Deal-Anteil 2023→2025)
- `funding_2025` (Absolutes Funding-Volumen 2025)

**Verwendung:**
- ✅ Momentum Matrix Bubble Chart (opportunity.html – Section 4.1)

---

### 6️⃣ **chiara/results/INVESTMENT_RECOMMENDATIONS.csv**
**Spalten:**
- Kategorien (BioTech, FinTech, ...)
- Empfehlung (Buy, Hold, Avoid)
- Begründung

**Verwendung:**
- ✅ Fazit & Empfehlung (opportunity.html – Section 4.3)

---

### 7️⃣ **Curriculum MBI/0_mbi_curriculum_final.csv**
**Spalten:**
- `course_title` (Kursname)
- `ects` (Credits)
- `language` (DE/EN)
- `learning_objectives_raw` (Lernziele)
- `course_content_raw` (Kursbeschreibung)
- **Profil-Spalten:** `Business Development`, `Digital Channel & CRM`, `Startup & Scale-up`, `Supply Chain & Operations`, `Technology Architecture`, `Digital Transformation`
- `extracted_keywords` (Keywords)

**Verwendung:**
- ✅ Kurslisten (courses.html – Bereich A + B)
- ⚠️ **Manuell:** Zuordnung zu EC-Domains + Sektoren

---

## ⚠️ Fehlende Daten (manuell erstellen)

### **1. EC-Domains (ec_domains.json)**
**Struktur:**
```json
[
  {
    "id": "opportunity_recognition",
    "name": "Opportunity Recognition",
    "mbi_coverage_score": 1.5,
    "blind_spot": true,
    "courses": ["Technology Entrepreneurship", "Innovation Management"],
    "description": "Marktlücken und Gründungsopportunitäten erkennen"
  },
  {
    "id": "pitching_communication",
    "name": "Pitching & Communication",
    "mbi_coverage_score": 1.0,
    "blind_spot": true,
    "courses": ["Business Communication"],
    "description": "Investoren und Stakeholder überzeugen"
  }
  // ... 10 weitere EC-Domains
]
```

**12 EC-Domains:**
1. Opportunity Recognition
2. Opportunity Assessment
3. Vision & Value Creation
4. Ethical & Sustainable Thinking
5. Creativity & Innovation
6. Pitching & Communication
7. Mobilising Resources
8. Leading & Managing
9. Learning Through Failure
10. Coping with Uncertainty
11. Self-Awareness & Motivation
12. Networking & Collaboration

---

### **2. Sektor-Matrix (sector_matrix.json)**
**Struktur:**
```json
{
  "GenAI": [
    "Technology Entrepreneurship",
    "Data Science und AI for Business",
    "Agentic AI Design, Governance and Management",
    "Leveraging AI for Healthcare"
  ],
  "HealthTech": [
    "Leveraging AI for Healthcare",
    "Sustainable Innovation through Human-centered Design"
  ],
  "MedTech": [
    "Leveraging AI for Healthcare"
  ],
  "BioTech": [],
  "Robotics": [
    "Social Network Analysis"
  ]
}
```

---

### **3. Kanton-Karte (canton_map.json) [OPTIONAL]**
**Struktur:**
```json
[
  {
    "kanton": "Zürich",
    "dominant_industry": "FinTech",
    "top3_industries": ["FinTech", "GenAI", "HealthTech"],
    "total_deals": 450
  },
  {
    "kanton": "Basel-Stadt",
    "dominant_industry": "BioTech",
    "top3_industries": ["BioTech", "MedTech", "HealthTech"],
    "total_deals": 180
  }
  // ... weitere Kantone
]
```

**⚠️ Problem:** Kanton-Daten fehlen in den bestehenden CSVs → entweder manuell ergänzen oder Sektion 3.7 weglassen.

---

## 🔄 Transformations-Workflow

```
1. CSV-Dateien (Lizzy, chiara, Curriculum MBI)
   ↓
2. Python-Skripte (scripts/create_*.py)
   ↓
3. JSON-Dateien (data/*.json)
   ↓
4. Plotly.js Charts (js/charts/*.js)
   ↓
5. Website (HTML Pages)
```

---

## ✅ Checkliste: Datenvorbereitung

### **Automatisch (Python-Skripte):**
- [ ] `create_tech_trends.py` → `tech_trends.json`
- [ ] `create_industry_trends.py` → `industry_trends.json`
- [ ] `create_deal_count.py` → `deal_count.json`
- [ ] `create_funding_share.py` → `funding_share.json`
- [ ] `create_momentum_matrix.py` → `momentum_matrix.json`
- [ ] `create_co_occurrence.py` → `co_occurrence.json`
- [ ] `create_mbi_courses.py` → `mbi_courses.json`

### **Manuell (EntreComp + Mapping):**
- [ ] `ec_domains.json` (12 EC-Domains mit MBI-Abdeckung)
- [ ] `sector_matrix.json` (Sektoren × Kurse)
- [ ] `canton_map.json` (Kanton-Karte) – **OPTIONAL**

---

*Erstellt: April 2026 | Projekt: data2dollar – Pfad A: Gründen*
