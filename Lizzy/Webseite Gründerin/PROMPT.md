# 🚀 GitHub Copilot Prompt – data2dollar Website (Pfad A: Gründen)

> Dieses Dokument ist ein vollständiges Briefing für GitHub Copilot (oder einen anderen KI-Coding-Assistenten), um die data2dollar-Website zu bauen. Es dient gleichzeitig als README im GitHub Repo.

---

## 🎯 Projektziel

Baue eine **interaktive, datengetriebene Website**, die zeigt, wo und wie sich in der Schweiz ein Startup gründen lohnt. Die Website kombiniert drei Datenwelten: globale Tech-Trends (2'817 Artikel), Schweizer Startup-Investments (Venture Kick, Swiss Startups) und das HSG MBI-Curriculum.

**Primäre Nutzerin:** Lizzy – MBI-Studentin an der HSG, die in naher Zukunft gründen will. Sie hat die Analyse für sich selbst erstellt und stellt sie anschliessend auch anderen MBI-Studierenden zur Verfügung.

**Erzählperspektive:** Die Website spricht Nutzer:innen direkt an – nicht als Lizzy-Protagonist:in, sondern als Tool, das die Frage beantwortet: *„In welcher Branche lohnt sich eine Gründung aus dem MBI heraus?"*

---

## 🗂️ Technologie-Stack

- **Framework:** Vanilla HTML/CSS/JavaScript ODER React (mit Vite)
- **Charts:** [Plotly.js](https://plotly.com/javascript/) (bevorzugt, da Python-Daten leicht konvertierbar) ODER Chart.js
- **Styling:** CSS Custom Properties (keine externen UI-Libraries nötig)
- **Fonts:** Google Fonts – `Syne` (Display/Headings) + `DM Sans` (Body)
- **Daten:** JSON-Dateien im `/data/` Ordner (werden separat eingefügt)
- **Deployment:** GitHub Pages (statische Site, alle Pfade relativ)

---

## 🎨 Design-System

### Farbpalette
```css
:root {
  --bg-dark:       #0D1117;   /* Haupt-Hintergrund */
  --bg-card:       #161B22;   /* Karten-Hintergrund */
  --bg-card-hover: #1C2128;   /* Hover-State */
  --accent-green:  #00E5A0;   /* Primär-Akzent (Calls-to-Action, Highlights) */
  --accent-blue:   #4A9EFF;   /* Sekundär-Akzent (Links, Labels) */
  --accent-orange: #FF7A45;   /* Warnung / fallende Trends */
  --accent-purple: #C77DFF;   /* Badge: "Doppelt wertvoll" */
  --text-primary:  #E6EDF3;   /* Haupttext */
  --text-muted:    #7D8590;   /* Sekundärtext, Labels */
  --border:        #30363D;   /* Card-Borders */
}
```

### Typografie
```css
/* Headings: Syne, 700 */
/* Body: DM Sans, 400/500 */
/* Monospace (Zahlen, Metriken): DM Mono */
```

### Chart-Farben (konsistent über alle Charts)
```javascript
const CHART_COLORS = {
  BioTech:      '#4A9EFF',
  FinTech:      '#00E5A0',
  ClimateTech:  '#FF7A45',
  HealthTech:   '#C77DFF',
  GenAI:        '#FFD166',
  MedTech:      '#06D6A0',
  Robotics:     '#EF476F',
  Other:        '#7D8590'
};
```

---

## 📄 Seitenstruktur (Multi-Page mit Navigation)

Die Website hat **5 Pages** + eine **Navigation**:

```
/index.html          → Landing Page (Projekt-Übersicht & Daten-Einstieg)
/trends.html         → Seite 1: Tech & Industry Trends
/investments.html    → Seite 2: VC Investments Schweiz
/opportunity.html    → Seite 3: Wo lohnt es sich einzusteigen?
/courses.html        → Seite 4: MBI-Kursabgleich
```

---

## 🧭 Navigation (Sticky Top-Bar, erscheint auf allen Seiten)

```
[data2dollar]   [Trends]   [Investments]   [Opportunity]   [MBI-Kurse]   [→ Empfehlung]
```

- Dark background (`#0D1117`), sticky beim Scrollen
- Aktive Seite mit `--accent-green` unterstrichen
- Mobile: Hamburger-Menü
- Rechts: CTA-Button „→ Empfehlung" scrollt direkt zu `#fazit` auf `opportunity.html`

---

## 📑 Page 1: Landing Page (`index.html`)

### Hero Section
- **Headline:** `Wo lohnt sich eine Gründung aus dem MBI?` (72px, Syne Bold)
- **Subheadline:** `Eine datenbasierte Analyse von Schweizer Startup-Investments, globalen Tech-Trends und dem HSG MBI-Curriculum – damit die Entscheidung nicht auf Bauchgefühl basiert.`
- **CTA:** `→ Analyse starten` (verlinkt auf `trends.html`)
- Hintergrund: dunkle Farbfläche mit subtiler Dot-Grid-Textur (CSS)

### Daten-Übersicht (4 grosse Zahlen)
```
2'817 Artikel analysiert   |   Venture Kick & Swiss Startups   |   14 Branchen   |   2023–2026 Q1
```

### Navigations-Karten (3 Karten nebeneinander, verlinkt auf die jeweiligen Pages)
```
[🌍 Globale Trends]            [🇨🇭 Schweizer VC]             [🎯 Deine Chance]
"Was bewegt sich global        "Wohin fliesst Kapital          "Wo ist der Sweet Spot
 in der Tech-Welt?"             in der Schweiz?"                für MBI-Gründer?"
→ trends.html                  → investments.html              → opportunity.html
```

### Methodik-Hinweis (foldable/akkordeon, kein Standard-Akkordeon-Design)
- Datenquellen: **Venture Kick**, **Swiss Startups** (CH VC-Daten), **StealthSpy / AICrunch** (Tech-News, 2'817 reine Artikel), **HSG MBI Curriculum** (Kurse)
- Zeitraum: 2023 Q1 – 2026 Q1
- Normalisierung und Schwellenwert-Logik kurz erklären (Threshold 2, Co-Occurrence normalisiert pro Tech-Keyword)

---

## 📑 Page 2: Trends (`trends.html`)

**Fragestellung:** *„Was bewegt sich gerade global in der Tech-Welt?"*

### Section 2.1 – Tech-Keyword Trend-Timeline
- **Chart-Typ:** Stacked Area Chart (Plotly)
- **X-Achse:** Quartale 2023 Q1 – 2026 Q1
- **Y-Achse:** Medien-Anteil der Keywords (% aller 2'817 Artikel)
- **Datenquelle:** `data/tech_trends.json`
- **Keywords (Linien):** GenAI, AgentAI, LLM, PhysicalAI, Robotics, Web3, Blockchain, CloudTech, CyberSecurity, GreenTech, BioInformatics
- **Key Message Box** (grüne Karte unter Chart):
  > 💡 **GenAI dominiert** den globalen Tech-Diskurs. **AgentAI explodiert** von 0 auf 9% – der nächste grosse Trend. Web3 ist rückläufig.

### Section 2.2 – Industry-Keyword Trend-Timeline
- **Chart-Typ:** Multi-Line Chart mit Toggle-Buttons pro Branche (klickbar zum Isolieren)
- **Keywords:** FinTech, DefenseTech, HealthTech, BioTech, ClimateTech, MedTech, MobilityTech, SpaceTech, EdTech, RetailTech, AgriTech, PropTech, InsurTech, LegalTech, HRTech, FoodTech, EnergyTech
- **Key Message Box:**
  > 💡 **FinTech dominiert** global (3–6%). **DefenseTech wächst** auf 4% in 2026 Q1 – stärkster Aufsteiger. BioTech ist medial kaum sichtbar, trotz starkem CH-Investment.

### Übergangs-Teaser
```
→ Du weisst jetzt, was global läuft. Aber wohin fliesst Kapital in der Schweiz?
[Weiter zu Investments →]
```

---

## 📑 Page 3: Investments (`investments.html`)

**Fragestellung:** *„Wohin fliesst Kapital in der Schweiz – und ist jetzt ein guter Zeitpunkt?"*

**Datenquellen:** Venture Kick + Swiss Startups

### Section 3.1 – Marktübersicht (Hero-Metriken)
```
~80–120 Deals/Quartal   |   9 Mrd. CHF in 2026 Q1   |   14 Kategorien   |   ↑ Wachsender Markt
```

### Section 3.2 – Deal Count: Top 5 Stacked Area
- **Chart-Typ:** Stacked Area (Plotly)
- **Kategorien:** BioTech, FinTech, ClimateTech, HealthTech, GenAI + „Übrige"
- **Datenquelle:** `data/deal_count.json`
- **Key Message:** > 💡 BioTech + FinTech dominieren konstant. **ClimateTech verliert Anteile seit 2024.**

### Section 3.3 – Deal Count: Einzellinien (klickbar)
- **Chart-Typ:** Multi-Line Chart, jede Kategorie togglebar
- **Key Message:** > 💡 **GenAI in der Schweiz ist zeitverzögert:** erst 1–8 Deals/Quartal. Gut für First-Mover.

### Section 3.4 – Deal Count: Small Multiples
- **Chart-Typ:** 14 Mini-Sparklines (2-Spalten-Grid), mit Total-Deals-Zahl, sortiert absteigend
- **Key Message:** > 💡 **MedTech (65) + Robotics (28):** wachsende Kurven – attraktiv mit wenig Kapital.

### Section 3.5 – Funding CHF: Top 5 Stacked Area
- **Chart-Typ:** Stacked Area (Mio. CHF)
- **Key Message:** > 💡 BioTech zieht 2–3 Mrd. CHF/Quartal – **ohne Bio-Expertise schwer einzusteigen.**

### Section 3.6 – Investment Stages
- **Chart-Typ:** Stacked Bar Chart (Pre-Seed, Seed, Series A/B/C+, Grant, Award)
- **Key Message:** > 💡 **Seed dominiert.** Pre-Seed wächst. CH-Markt ist Early-Stage-fokussiert – gut für Gründer.

### Section 3.7 – Kanton-Karte Schweiz
- **Chart-Typ:** Choropleth Map per Kanton (Plotly GeoJSON oder SVG-Karte)
- **Farbe:** Dominante Industrie pro Kanton nach Deal-Anzahl
- **Hover-Tooltip:** Kanton, Top-3 Industrien, Anzahl Deals
- **Datenquelle:** `data/canton_map.json`
- **Key Message:** > 💡 **Zürich = FinTech-Hub.** Basel/Genf/Lausanne = BioTech-Dreieck. Bern = CleanTech. Zug = FinTech/Crypto.

### Übergangs-Teaser
```
→ Du kennst Branchen und Kapital. Aber wo ist der Sweet Spot für dich als MBI-Gründer:in?
[Weiter zu Opportunity →]
```

---

## 📑 Page 4: Opportunity (`opportunity.html`)

**Fragestellung:** *„Wo überschneiden sich globaler Buzz, CH-Investment UND Einstiegschance?"*

### Section 4.1 – Momentum Matrix (Bubble Chart)
- **Chart-Typ:** Scatter/Bubble Chart (Plotly)
- **X-Achse:** Δ Medien-Anteil 2023→2025 (global)
- **Y-Achse:** Δ VC-Deal-Anteil 2023→2025 (CH)
- **Bubble-Grösse:** Absolutes Funding-Volumen 2025
- **Bubble-Farbe:** Nach Kategorie (CHART_COLORS)
- **4 Quadranten mit Labels:**
  - Oben Rechts: 🏆 Emerging Winner
  - Oben Links: 🤫 Silent Growth (CH investiert, Medien ignorieren)
  - Unten Rechts: 📣 Hype ohne Kapital
  - Unten Links: ❄️ Abkühlung
- **Datenquelle:** `data/momentum_matrix.json`
- **Key Message:** > 💡 **MedTech + HealthTech = Silent Opportunity.** Steigendes CH-Investment, kaum globale Medienkonkurrenz.

### Section 4.2 – Co-Occurrence Heatmap
- **Chart-Typ:** Heatmap (Plotly, custom grüne Colorscale)
- **Zeilen (Y):** Tech-Keywords (GenAI, LLM, AgentAI, PhysicalAI, Web3, Blockchain, Robotics, etc.)
- **Spalten (X):** Industry-Keywords (FinTech, HealthTech, BioTech, MedTech, etc.)
- **Werte:** Normalisierter Co-Occurrence-Anteil (%) pro Tech-Keyword
- **Erklärungstext über Chart:** Zeigt, welche Technologie in welcher Branche am häufigsten zusammen erwähnt wird. Basis: 2'817 Artikel.
- **Datenquelle:** `data/co_occurrence.json`
- **Key Message:** > 💡 **GenAI × FinTech (24%)** ist der häufigste Schnittpunkt. Wenn du LLMs bauen kannst: **FinTech oder HealthTech** bieten die meiste Aufmerksamkeit.

### Section 4.3 – Fazit & Empfehlung (ID: `#fazit`)
Grosse visuelle Empfehlungs-Karte:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  🎯  Empfehlung für MBI-Gründer:innen – April 2026                       │
│                                                                           │
│  MedTech oder HealthTech mit einer GenAI-Komponente,                     │
│  gebaut in Zürich oder Basel.                                             │
│                                                                           │
│  ✅ Kapitalverfügbarkeit (steigendes CH-VC)                              │
│  ✅ Medialer Whitespace (wenig globale Konkurrenz)                       │
│  ✅ Schweizer Ökosystem-Stärke (Netzwerke, Talente)                     │
│  ✅ MBI-Skills (GenAI + Business Know-how)                              │
└──────────────────────────────────────────────────────────────────────────┘
```

### Übergangs-Teaser
```
→ Du weisst jetzt wo. Aber bist du auch bereit dafür? Welche MBI-Kurse helfen dir?
[Weiter zu MBI-Kurse →]
```

---

## 📑 Page 5: MBI-Kursabgleich (`courses.html`)

**Fragestellung:** *„Welche MBI-Kurse decken Gründerkompetenzen ab – und wo sind die blinden Flecken?"*

**Kernbotschaft (immer sichtbar, kein Chart nötig):**
> ⚠️ Das MBI deckt vieles gut ab – aber **Opportunity-Erkennung und Pitching** sind die blinden Flecken, genau dort wo es für Gründer:innen am meisten zählt.

Diese Seite ist in **zwei klar getrennte Bereiche** unterteilt:

---

### Bereich A – EC Self-Assessment (Entrepreneurial Competencies)

**Ziel:** Nutzer:innen bewerten ihre eigenen Stärken in den 12 EC-Domains und sehen sofort, welche MBI-Kurse ihre Lücken schliessen.

#### A.1 – Interaktive EC-Domain-Karten (12 Karten im Grid)

- **Darstellung:** 12 klickbare Karten, je eine pro EC-Domain
- **Jede Karte zeigt:**
  - Domain-Name (z.B. „Opportunity Recognition")
  - Anzahl MBI-Kurse, die diese Domain trainieren
  - Selbstbewertungs-Buttons: `💪 Stark` | `👍 Okay` | `⚠️ Lücke`
- **Interaktion:** Beim Klick auf einen Button wird der Karten-Status gesetzt (grün/gelb/rot Highlight)
- **State:** Bewertungen werden im `localStorage` gespeichert (bleiben beim Reload erhalten)

**Die 12 EC-Domains:**
```
1. Opportunity Recognition        7. Mobilising Resources
2. Opportunity Assessment         8. Leading & Managing
3. Vision & Value Creation        9. Learning Through Failure
4. Ethical & Sustainable Thinking 10. Coping with Uncertainty
5. Creativity & Innovation        11. Self-Awareness & Motivation
6. Pitching & Communication       12. Networking & Collaboration
```

#### A.2 – Dynamische Kursliste (erscheint sobald ≥1 Lücke markiert)

- Erscheint **unterhalb der 12 Karten** dynamisch
- **Titel:** „Empfohlene Kurse für deine Lücken"
- **Zeigt nur:** Kurse die mindestens eine als „Lücke" markierte Domain abdecken
- **Sortierung:** Nach Score (Kurs deckt mehrere Lücken → weiter oben)
- **Jede Kurskarte zeigt:**
  - Kursname (bold)
  - Welche Lücken-Domains er abdeckt (farbige Badges)
  - ECTS + Semester
  - Ggf. `🏆 Doppelt wertvoll` Badge (wenn auch Sektor-Relevanz)
- **Beispiel-Text:** *„Für deine Lücke in Opportunity empfiehlt sich: Technology Entrepreneurship (3 ECTS)"*

#### A.3 – Radar Chart: MBI-Abdeckung vs. meine Stärken

- **Chart-Typ:** Radar/Spider Chart (Plotly)
- **Achsen:** Die 12 EC-Domains
- **Zwei Datenserien:**
  - `MBI-Abdeckung`: Wie gut deckt das MBI diese Domain ab (0–5, aus `ec_domains.json`)
  - `Meine Stärke`: Nutzer:innen-Bewertung (stark=5, okay=3, Lücke=1), dynamisch aus Self-Assessment
- **Datenquelle:** `data/ec_domains.json` + dynamisch aus localStorage
- **Visuelle Hervorhebung:** Domains mit Score ≤ 2 im MBI werden rot markiert (Opportunity Recognition, Pitching & Communication)

---

### Bereich B – Sektor-Kurse

**Ziel:** Nutzer:innen wählen ihren Zielsektor und sehen, welche MBI-Kurse direkt relevant sind.

#### B.1 – Sektor-Tab-Navigation

5 Tabs (horizontal, klickbar):
```
[GenAI]   [HealthTech]   [MedTech]   [BioTech]   [Robotics]
```
- Aktiver Tab hervorgehoben (`--accent-green`)
- Beim Wechsel wird die Kursliste darunter ausgetauscht

#### B.2 – Kursliste pro Sektor

- **Darstellung:** Karten-Grid (2–3 Spalten), je Kurs eine Karte:
  - Kursname (bold)
  - Skill-Tags als farbige Badges
  - ECTS + Semester (klein unten)
  - Hover: Kurzbeschreibung einblenden
  - `🏆 Doppelt wertvoll` Badge (lila, `--accent-purple`) wenn der Kurs **gleichzeitig** eine EC-Domain trainiert

#### B.3 – Hinweis-Box für schwach abgedeckte Sektoren

Für die Tabs **MedTech**, **BioTech** und **Robotics** erscheint zusätzlich:

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  Diese Domäne ist kaum im MBI abgedeckt                 │
│  Für eine Gründung in [Sektor] sind externe Ressourcen      │
│  nötig. Empfehlungen: [Coursera-Kurs] [Buch] [Community]   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Datenstruktur (`/data/` Ordner)

### `data/tech_trends.json`
```json
{
  "quarters": ["2023 Q1", "2023 Q2", "...", "2026 Q1"],
  "total_articles": 2817,
  "keywords": {
    "GenAI":   [9, 11, 13, 14, 15, 16, 18, 19, 20, 21, 21, 20, 19],
    "AgentAI": [0, 0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  9],
    "Web3":    [8, 7,  6,  6,  5,  5,  4,  4,  3,  3,  2,  2,  2]
  }
}
```

### `data/deal_count.json`
```json
{
  "source": "Venture Kick + Swiss Startups",
  "quarters": ["2023 Q1", "..."],
  "categories": {
    "BioTech":     [28, 30, 32, 35, 33, 31, 30, 34, 36, 38, 35, 37, 39],
    "FinTech":     [40, 42, 50, 45, 44, 48, 46, 44, 42, 43, 41, 40, 38],
    "ClimateTech": [15, 14, 13, 12, 11, 10, 9,  8,  8,  7,  7,  6,  6],
    "HealthTech":  [10, 11, 12, 13, 12, 13, 14, 14, 15, 16, 15, 16, 17],
    "GenAI":       [1,  1,  2,  2,  3,  3,  4,  5,  6,  7,  7,  8,  8]
  }
}
```

### `data/momentum_matrix.json`
```json
[
  { "name": "BioTech",    "delta_media": 0.5,  "delta_vc": 1.2,  "funding_mio": 2800, "quadrant": "emerging_winner" },
  { "name": "MedTech",    "delta_media": 0.2,  "delta_vc": 0.8,  "funding_mio": 180,  "quadrant": "silent_growth" },
  { "name": "HealthTech", "delta_media": 0.3,  "delta_vc": 0.7,  "funding_mio": 150,  "quadrant": "silent_growth" },
  { "name": "ClimateTech","delta_media": -0.4, "delta_vc": -0.8, "funding_mio": 320,  "quadrant": "cooling" },
  { "name": "GenAI",      "delta_media": 1.8,  "delta_vc": 0.3,  "funding_mio": 90,   "quadrant": "hype_no_capital" }
]
```

### `data/co_occurrence.json`
```json
{
  "tech_keywords": ["GenAI", "LLM", "AgentAI", "PhysicalAI", "Web3", "Blockchain", "Robotics"],
  "industry_keywords": ["FinTech", "HealthTech", "BioTech", "MedTech", "MobilityTech", "EdTech"],
  "matrix": [
    [24, 21, 12, 5,  8,  6],
    [15, 18, 10, 8,  4,  9],
    [12, 14, 8,  6,  3,  7],
    [3,  4,  5,  2,  84, 1],
    [44, 8,  3,  2,  5,  3],
    [40, 7,  4,  2,  4,  2],
    [8,  6,  9,  12, 22, 4]
  ]
}
```

### `data/ec_domains.json`
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
]
```

### `data/mbi_courses.json`
```json
[
  {
    "name": "Technology Entrepreneurship",
    "ects": 3,
    "semester": 2,
    "mbi_profil": "Gründen",
    "ec_domains": ["opportunity_recognition", "vision_value_creation"],
    "sektoren": ["GenAI", "HealthTech"],
    "skill_tags": ["Opportunity", "Business Model", "Strategy"],
    "beschreibung": "Von der Idee zur skalierbaren Tech-Firma.",
    "double_value": true
  }
]
```

---

## 🧩 Wiederverwendbare Komponenten

| Komponente | Datei | Verwendung |
|---|---|---|
| Navigation | `components/nav.js` | Alle Seiten |
| KeyMessage Box | `components/key-message.js` | Nach jedem Chart |
| MetricCard | `components/metric-card.js` | Grosse Zahlen |
| ChartWrapper | `components/chart-wrapper.js` | Plotly-Chart mit Titel + Loading State |
| ECDomainCard | `components/ec-domain-card.js` | Self-Assessment Karten (12 Domains) |
| CourseCard | `components/course-card.js` | Kurs-Darstellung inkl. Double-Value Badge |
| WarningBox | `components/warning-box.js` | Hinweis bei MedTech/BioTech/Robotics |

---

## ♿ Technische Anforderungen

- **Responsive:** Mobile-first, Breakpoints bei 768px und 1200px
- **Performance:** Charts lazy-laden (Intersection Observer)
- **Barrierefreiheit:** Alt-Texte auf allen Charts, ARIA-Labels auf Navigation
- **Dark Mode:** Default, kein Toggle nötig
- **State-Persistenz:** EC Self-Assessment-Bewertungen in `localStorage` speichern
- **GitHub Pages:** Alle Pfade relativ, kein Backend

---

## 🗂️ Dateistruktur (Ziel)

```
data2dollar/
├── index.html
├── trends.html
├── investments.html
├── opportunity.html
├── courses.html
├── css/
│   ├── main.css           ← Design-System & CSS-Variablen
│   ├── nav.css
│   └── charts.css
├── js/
│   ├── main.js
│   ├── charts/
│   │   ├── tech-trends.js
│   │   ├── deal-count.js
│   │   ├── momentum-matrix.js
│   │   ├── co-occurrence.js
│   │   ├── canton-map.js
│   │   └── ec-radar.js
│   └── components/
│       ├── nav.js
│       ├── key-message.js
│       ├── ec-domain-card.js
│       ├── course-card.js
│       └── warning-box.js
└── data/
    ├── tech_trends.json
    ├── deal_count.json
    ├── momentum_matrix.json
    ├── co_occurrence.json
    ├── canton_map.json
    ├── ec_domains.json
    └── mbi_courses.json
```

---

## 🚀 Copilot Einstiegs-Prompt

Kopiere diesen Text direkt in GitHub Copilot Chat:

```
I'm building a static multi-page data visualization website called "data2dollar" 
about Swiss startup investment opportunities for MBI students considering entrepreneurship.

Data sources: Venture Kick + Swiss Startups (CH VC data), StealthSpy/AICrunch 
(2817 tech articles 2023-2026), HSG MBI curriculum.

Tech stack: Vanilla HTML/CSS/JS, Plotly.js for charts, Google Fonts (Syne + DM Sans).
Design: Dark theme (#0D1117 background), accent color #00E5A0 (green), #4A9EFF (blue).
All data loaded from local JSON files in /data/. Deployed to GitHub Pages (no backend).

Please start by creating:
1. css/main.css – full design system with all CSS variables, typography scale, card styles, badge styles, key-message box styles
2. js/components/nav.js – reusable sticky navigation web component (highlights active page)
3. index.html – landing page with: hero headline, 4 data metric cards, 3 navigation cards, collapsible methodology section

The full project spec (pages, charts, data schemas, component list) is in README.md.
Follow the exact file structure, JSON formats, and component patterns described there.
After finishing these 3 files, ask me which page to build next.
```

---

*Erstellt für: data2dollar Gruppenarbeit – Pfad A: Gründen | MBI HSG | April 2026*
*Datenquellen: Venture Kick, Swiss Startups, StealthSpy, AICrunch, HSG MBI Curriculum*
