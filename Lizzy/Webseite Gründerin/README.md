# 🌐 Webseite Gründerin – data2dollar

> Interaktive, datengetriebene Website für MBI-Studierende: **Wo lohnt sich eine Gründung aus dem MBI?**

---

## 📂 Was ist in diesem Ordner?

Dieser Ordner enthält die **vollständige Dokumentation und Planung** für die data2dollar-Website (Pfad A: Gründen). Die Website kombiniert:

1. **Globale Tech-Trends** (2'817 Artikel, 2023–2026)
2. **Schweizer VC-Investments** (Venture Kick + Swiss Startups)
3. **HSG MBI-Curriculum** (86 Kurse mit Skills-Mapping)

**Ziel:** MBI-Studierenden zeigen, in welcher Branche eine Gründung sinnvoll ist – basierend auf Daten, nicht Bauchgefühl.

---

## 📄 Dokumentation (Start hier!)

| Datei | Beschreibung |
|-------|--------------|
| **`PROMPT.md`** | 🚀 **VOLLSTÄNDIGES BRIEFING** für GitHub Copilot – Alle Pages, Charts, Datenstrukturen, Design-System |
| **`DATA_MAPPING.md`** | 📊 **Datenquellen-Mapping** – Welche CSV-Dateien werden wo verwendet? |
| **`VISUAL_OVERVIEW.md`** | 🗺️ **Datenfluss-Diagramm** – Von CSV über Python-Skripte zu JSON zu Website |
| **`QUICK_REFERENCE.md`** | 🎯 **Kompakte Übersicht** – Schneller Überblick für Entwicklung |

---

## 🎯 Website-Struktur (5 Pages)

```
1️⃣ Landing Page (index.html)
   → Projekt-Übersicht, Hero-Metriken, Navigation

2️⃣ Trends (trends.html)
   → Tech- & Industry-Keyword Trends (2023–2026 Q1)

3️⃣ Investments (investments.html)
   → VC Deals in der Schweiz (Deal Count, Funding, Stages, Kanton-Karte)

4️⃣ Opportunity (opportunity.html)
   → Momentum Matrix + Co-Occurrence Heatmap + Empfehlung

5️⃣ Courses (courses.html)
   → MBI-Kursabgleich: EC Self-Assessment + Sektor-Kurse
```

---

## 📁 Datenquellen (bereits vorhanden)

### ✅ **Lizzy/Trends/Trends_Data/**
- `keyword_monthly_normalized.csv` → Tech & Industry Trends
- `articles_classified_t2.csv` → Co-Occurrence Heatmap

### ✅ **chiara/results/**
- `F1_deal_count_quarterly.csv` → Deal Count Charts
- `D_momentum.csv` → Momentum Matrix
- `C_funding_share_pct.csv` → Funding-Volumen
- `INVESTMENT_RECOMMENDATIONS.csv` → Empfehlungen

### ✅ **Curriculum MBI/**
- `0_mbi_curriculum_final.csv` → 86 MBI-Kurse

### ⚠️ **Fehlt (manuell erstellen):**
- `data/ec_domains.json` → 12 EC-Domains mit MBI-Abdeckung
- `data/sector_matrix.json` → EC × Sektoren × Kurse
- `data/canton_map.json` → Kanton-Karte (optional)

---

## 🔄 Workflow: Von CSV zu Website

```
1. CSV-Dateien (Lizzy, chiara, Curriculum MBI)
   ↓
2. Python-Skripte (create_*.py)
   ↓
3. JSON-Dateien (data/*.json)
   ↓
4. Website (HTML/CSS/JS + Plotly.js)
   ↓
5. GitHub Pages Deployment
```

---

## 🛠️ Tech-Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript (ODER React mit Vite)
- **Charts:** Plotly.js
- **Fonts:** Google Fonts (Syne + DM Sans)
- **Deployment:** GitHub Pages (statische Site)
- **Daten:** JSON-Dateien (keine Datenbank)

---

## 🎨 Design-System

```css
:root {
  --bg-dark:       #0D1117;   /* Haupt-Hintergrund */
  --accent-green:  #00E5A0;   /* Primär-Akzent */
  --accent-blue:   #4A9EFF;   /* Sekundär-Akzent */
  --accent-orange: #FF7A45;   /* Warnung */
  --accent-purple: #C77DFF;   /* "Doppelt wertvoll" Badge */
  --text-primary:  #E6EDF3;   /* Haupttext */
}
```

**Fonts:**
- Headings: **Syne** (Bold, 700)
- Body: **DM Sans** (Regular/Medium, 400/500)

---

## 📋 Nächste Schritte

### **1. Datenvorbereitung**
- [ ] Python-Skripte schreiben (`create_tech_trends.py`, `create_deal_count.py`, ...)
- [ ] JSON-Dateien generieren (`data/tech_trends.json`, `data/deal_count.json`, ...)
- [ ] EC-Domains manuell erstellen (`data/ec_domains.json`)

### **2. Website-Entwicklung**
- [ ] HTML-Struktur (5 Pages)
- [ ] CSS Design-System (`css/main.css`)
- [ ] Navigation (`js/components/nav.js`)
- [ ] Plotly.js Charts (`js/charts/tech-trends.js`, ...)
- [ ] Interaktive Komponenten (EC Self-Assessment)

### **3. Deployment**
- [ ] GitHub Pages Setup
- [ ] Performance-Optimierung
- [ ] Barrierefreiheit (ARIA-Labels, Alt-Texte)

---

## 🚀 Quick Start (für Entwicklung)

### **1. Lies die Dokumentation:**
```bash
# Start hier:
cat PROMPT.md           # Vollständiges Briefing
cat DATA_MAPPING.md     # Datenquellen-Mapping
cat QUICK_REFERENCE.md  # Kompakte Übersicht
```

### **2. Erstelle Python-Skripte:**
```bash
# Beispiel: Tech Trends
python create_tech_trends.py
# Output: data/tech_trends.json
```

### **3. Starte Website-Entwicklung:**
```bash
# HTML/CSS/JS
open index.html
```

---

## 📞 Kontakt & Support

- **Projekt:** data2dollar – Pfad A: Gründen
- **Zielgruppe:** MBI-Studierende (HSG)
- **Erstellt:** April 2026
- **Datenquellen:** Venture Kick, Swiss Startups, StealthSpy, AICrunch, HSG MBI Curriculum

---

## 📚 Weiterführende Links

- [Plotly.js Dokumentation](https://plotly.com/javascript/)
- [GitHub Pages Guide](https://pages.github.com/)
- [EntreComp Framework](https://joint-research-centre.ec.europa.eu/entrecomp-entrepreneurship-competence-framework_en)

---

*Viel Erfolg beim Aufbau der Website! 🚀*
