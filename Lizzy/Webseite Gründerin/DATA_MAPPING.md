# 📊 Datenübersicht – Wo welche Daten verwendet werden

> Diese Übersicht zeigt, welche bestehenden Datenquellen aus dem Projekt für welche Teile der Website verwendet werden.

---

## 🗂️ Verfügbare Datenquellen im Projekt

### 1️⃣ **Lizzy/Trends/Trends_Data/**
- `keyword_monthly_normalized.csv` – Tech & Industry Keywords mit monatlichen Prozentanteilen (2023-01 bis 2026-01)
- `articles_classified_t2.csv` – Vollständige Artikeldaten mit Klassifizierung

**Verwendung:**
- ✅ **Page 2: Trends** → Tech-Keyword Trend-Timeline (Section 2.1)
- ✅ **Page 2: Trends** → Industry-Keyword Trend-Timeline (Section 2.2)
- ✅ **Page 4: Opportunity** → Co-Occurrence Heatmap (Section 4.2)

---

### 2️⃣ **chiara/results/**
- `F1_deal_count_quarterly.csv` – Quarterly Deal Counts pro Industrie
- `F2_deal_share_quarterly.csv` – Quarterly Deal Share (%)
- `D_momentum.csv` – Momentum-Berechnungen (Delta Media vs. Delta VC)
- `A_market_share_pct.csv` – Market Share pro Jahr
- `C_funding_share_pct.csv` – Funding Share (CHF)
- `INVESTMENT_RECOMMENDATIONS.csv` – Buy/Hold/Avoid Signale
- `TOP_WINNERS_LOSERS.csv` – Gewinner vs. Verlierer Rankings
- `MOMENTUM_LEADERS.csv` – Acceleration Rankings

**Verwendung:**
- ✅ **Landing Page (index.html)** → Hero-Metriken (Anzahl Deals, Funding-Volumen)
- ✅ **Page 3: Investments** → Section 3.1 (Marktübersicht)
- ✅ **Page 3: Investments** → Section 3.2 (Deal Count Top 5 Stacked Area)
- ✅ **Page 3: Investments** → Section 3.3 (Deal Count Einzellinien)
- ✅ **Page 3: Investments** → Section 3.4 (Small Multiples)
- ✅ **Page 3: Investments** → Section 3.5 (Funding CHF Stacked Area)
- ✅ **Page 4: Opportunity** → Section 4.1 (Momentum Matrix)

---

### 3️⃣ **Curriculum MBI/**
- `0_mbi_curriculum_final.csv` – Vollständiger Kurskatalog mit:
  - Kursname, ECTS, Semester, Sprache
  - Learning Objectives, Course Content
  - Profil-Zuordnung (Business Development, Startup & Scale-up, Digital Transformation, etc.)
  - Extrahierte Keywords

**Verwendung:**
- ✅ **Page 5: Courses** → Bereich A (EC Self-Assessment)
- ✅ **Page 5: Courses** → Bereich B (Sektor-Kurse)
- ✅ **Page 4: Opportunity** → Section 4.3 (Empfehlung – welche Skills hat MBI?)

---

### 4️⃣ **Zusätzliche Daten (müssen erstellt werden)**

#### **EC Sector Matrix** (muss manuell erstellt werden)
Mapping zwischen:
- **12 Entrepreneurial Competencies (EC-Domains)**
- **MBI-Kursen** (aus `0_mbi_curriculum_final.csv`)
- **Sektoren** (GenAI, HealthTech, MedTech, BioTech, Robotics)

**Format:** CSV oder JSON
**Verwendung:**
- ✅ **Page 5: Courses** → EC Self-Assessment (A.1–A.3)
- ✅ **Page 5: Courses** → Sektor-Tab-Navigation (B.1–B.2)

---

## 📋 Mapping-Tabelle: Daten → Website-Seiten

| Datenquelle | Herkunft | Website-Seite | Verwendung |
|-------------|----------|---------------|------------|
| **keyword_monthly_normalized.csv** | Lizzy/Trends/Trends_Data/ | `trends.html` | Section 2.1 (Tech-Keyword Timeline) |
| **keyword_monthly_normalized.csv** | Lizzy/Trends/Trends_Data/ | `trends.html` | Section 2.2 (Industry-Keyword Timeline) |
| **articles_classified_t2.csv** | Lizzy/Trends/Trends_Data/ | `opportunity.html` | Section 4.2 (Co-Occurrence Heatmap) |
| **F1_deal_count_quarterly.csv** | chiara/results/ | `investments.html` | Section 3.2–3.4 (Deal Count Charts) |
| **F2_deal_share_quarterly.csv** | chiara/results/ | `investments.html` | Section 3.2 (Stacked Area %) |
| **C_funding_share_pct.csv** | chiara/results/ | `investments.html` | Section 3.5 (Funding CHF) |
| **D_momentum.csv** | chiara/results/ | `opportunity.html` | Section 4.1 (Momentum Matrix) |
| **INVESTMENT_RECOMMENDATIONS.csv** | chiara/results/ | `opportunity.html` | Section 4.3 (Fazit & Empfehlung) |
| **0_mbi_curriculum_final.csv** | Curriculum MBI/ | `courses.html` | Bereich A + B (Kurslisten) |
| **EC Sector Matrix** (TBD) | Manuell erstellen | `courses.html` | EC Self-Assessment + Sektor-Tabs |
| **Kanton-Daten** (TBD) | chiara/results/ (evtl. ergänzen) | `investments.html` | Section 3.7 (Schweizer Kanton-Karte) |

---

## 🔄 Transformations-Pipeline (CSV → JSON)

Für die Website müssen CSV-Daten in **JSON** transformiert werden. Hier ist der Plan:

### **1. Tech Trends (trends.html – Section 2.1)**
**Quelle:** `Lizzy/Trends/Trends_Data/keyword_monthly_normalized.csv`

**Filter:**
- Nur Zeilen mit `tech_keyword != ""` (leere industry_keyword)
- Keywords: GenAI, AgentAI, LLM, PhysicalAI, Robotics, Web3, Blockchain, etc.

**Aggregation:**
- Gruppiere nach `year_month` → summiere `keyword_pct` pro Tech-Keyword
- Konvertiere zu Quartalen (2023-01/02/03 → 2023 Q1)

**Output:** `data/tech_trends.json`
```json
{
  "quarters": ["2023 Q1", "2023 Q2", ...],
  "total_articles": 2817,
  "keywords": {
    "GenAI": [9.2, 11.5, 13.8, ...],
    "AgentAI": [0.1, 0.2, 0.5, ...],
    ...
  }
}
```

---

### **2. Industry Trends (trends.html – Section 2.2)**
**Quelle:** `Lizzy/Trends/Trends_Data/keyword_monthly_normalized.csv`

**Filter:**
- Nur Zeilen mit `industry_keyword != ""` (leere tech_keyword)
- Keywords: FinTech, DefenseTech, HealthTech, BioTech, ClimateTech, etc.

**Aggregation:**
- Gruppiere nach `year_month` → summiere `keyword_pct` pro Industry-Keyword
- Konvertiere zu Quartalen

**Output:** `data/industry_trends.json`

---

### **3. Deal Count (investments.html – Section 3.2–3.4)**
**Quelle:** `chiara/results/F1_deal_count_quarterly.csv`

**Transformation:**
- Direkt lesbar, nur Spalten umbenennen
- Quartale als X-Achse, Kategorien als Y-Werte

**Output:** `data/deal_count.json`

---

### **4. Momentum Matrix (opportunity.html – Section 4.1)**
**Quelle:** `chiara/results/D_momentum.csv`

**Transformation:**
- Verwende Spalten: `industry`, `delta_media`, `delta_vc`, `funding_2025`
- Berechne Quadrant (emerging_winner, silent_growth, hype_no_capital, cooling)

**Output:** `data/momentum_matrix.json`

---

### **5. Co-Occurrence Heatmap (opportunity.html – Section 4.2)**
**Quelle:** `Lizzy/Trends/Trends_Data/articles_classified_t2.csv`

**Berechnung:**
- Für jede Kombination (tech_keyword × industry_keyword):
  - Zähle Artikel mit beiden Keywords
  - Normalisiere: `(Co-Occurrence / Total Tech-Keyword-Mentions) * 100`

**Output:** `data/co_occurrence.json`

---

### **6. MBI Courses (courses.html)**
**Quelle:** `Curriculum MBI/0_mbi_curriculum_final.csv`

**Transformation:**
- Verwende Spalten: `course_title`, `ects`, `learning_objectives_raw`, `extracted_keywords`
- **Manuell:** Zuordnung zu EC-Domains + Sektoren (siehe EC Sector Matrix)

**Output:** `data/mbi_courses.json`

---

### **7. EC Domains (courses.html – A.3 Radar Chart)**
**Quelle:** **Manuell erstellen** (basierend auf EntreComp-Framework)

**Struktur:**
```json
[
  {
    "id": "opportunity_recognition",
    "name": "Opportunity Recognition",
    "mbi_coverage_score": 1.5,
    "blind_spot": true,
    "courses": ["Technology Entrepreneurship", "..."],
    "description": "..."
  },
  ...
]
```

**Output:** `data/ec_domains.json`

---

### **8. Kanton-Karte (investments.html – Section 3.7)**
**Quelle:** `chiara/results/` + **manuell** (Kanton-Zuordnung fehlt)

**Fehlende Daten:**
- Startup-Standorte pro Kanton (Zürich, Basel, Genf, etc.)
- Dominante Industrie pro Kanton

**Alternative:** Falls Kanton-Daten fehlen, **diese Sektion weglassen** oder manuell ergänzen.

**Output:** `data/canton_map.json`

---

## ✅ Checkliste: Was muss erstellt werden?

### **Transformationsskripte (Python)**
- [ ] `create_tech_trends.py` → `data/tech_trends.json`
- [ ] `create_industry_trends.py` → `data/industry_trends.json`
- [ ] `create_deal_count.py` → `data/deal_count.json`
- [ ] `create_momentum_matrix.py` → `data/momentum_matrix.json`
- [ ] `create_co_occurrence.py` → `data/co_occurrence.json`
- [ ] `create_mbi_courses.py` → `data/mbi_courses.json`

### **Manuelle Daten-Erstellung**
- [ ] `data/ec_domains.json` (12 EC-Domains mit MBI-Abdeckung)
- [ ] `data/sector_matrix.json` (EC-Domains × Sektoren × Kurse)
- [ ] `data/canton_map.json` (falls Kanton-Daten verfügbar)

---

## 🚀 Nächste Schritte

1. ✅ **Ordner erstellt:** `Webseite Gründerin/`
2. ✅ **Prompt gespeichert:** `PROMPT.md`
3. ✅ **Datenübersicht erstellt:** `DATA_MAPPING.md`
4. ⏭️ **Transformationsskripte schreiben** (Python)
5. ⏭️ **Website-Struktur aufbauen** (HTML/CSS/JS)

---

*Erstellt: April 2026 | Projekt: data2dollar Pfad A – Gründen*
