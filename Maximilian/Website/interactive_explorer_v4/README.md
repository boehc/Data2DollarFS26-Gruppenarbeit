# Interactive Explorer v4 — aktuelle Version

MBI Career Explorer, Frühlingssemester 2026 · Universität St. Gallen.

Diese Version enthält drei Ebenen:

1. **Landingpage (`index.html`)** — Marktüberblick, Kennzahlen, 6 Profil-Karten
2. **Profil-Seiten (`profil_*.html`)** — pro Vertiefungsprofil eine Detailansicht
   mit Top-Skills, passenden MBI-Kursen und Stelleninseraten inkl. Skill-Gap-Analyse
3. **Self-Assessment (`assessment.html`)** — interaktiv: Student:in wählt
   die bereits belegten Kurse aus; das System gewichtet Skills und zeigt live,
   welche der 1'194 Stellen am besten zum persönlichen Skill-Set passen
   *und* welche Kurse noch fehlen, um eine Ziel-Stelle besser abzudecken

---

## 📂 Dateistruktur

```
interactive_explorer_v4/
├── index.html                  ← Landingpage
├── profil_*.html               ← 6 Profil-Detailseiten
├── assessment.html             ← Self-Assessment
│
├── css/
│   ├── base.css                ← Design-Tokens, Typografie (Syne, DM Sans, DM Mono)
│   ├── components.css          ← Karten, Badges, Chips, Buttons, Overlay-Panel
│   ├── nav.css                 ← Header-Navigation
│   ├── pages.css               ← Seiten-spezifische Layouts (Hero, Grids, Promo)
│   └── assessment.css          ← Self-Assessment-UI (Course-Picker, Score-Ring, Job-List)
│
├── js/
│   ├── nav.js                  ← Mobile-Menü-Toggle
│   ├── profile.js              ← Overlay-Panel auf Profilseiten (Skill-Chips, Kurse)
│   └── assessment.js           ← Scoring-Engine (siehe unten)
│
├── data/                       ← vor-generierte Daten (vom build-Skript erzeugt)
│   ├── courses.json            ← 84 MBI-Kurse mit Skills + Keywords
│   ├── jobs.json               ← 1'158 deduplizierte Stellen mit Skill-Vektor
│   ├── skills.json             ← 68 Skill-Dimensionen inkl. IDF-Gewicht
│   ├── courses_data.js         ← dito, als `window.__COURSES__` eingebettet (file://-Modus)
│   ├── jobs_data.js            ← dito, als `window.__JOBS__`
│   └── skills_data.js          ← dito, als `window.__SKILLS__`
│
├── build_assessment_data.py    ← erzeugt die 3 JSON- + 3 JS-Dateien aus den CSVs
└── start_server.bat            ← Windows-One-Click-Launcher (Python http.server)
```

---

## 🎯 Self-Assessment — so funktioniert's

Ziel: **Student:in wählt belegte Kurse → System matched gegen 1'194 Stellen**,
zeigt passende Jobs, Skill-Gaps und Kurs-Empfehlungen zum Schliessen der Lücken.

### 1. Datenpipeline (`build_assessment_data.py`)

Liest zwei autoritative CSVs und erzeugt daraus die JSON-Dateien für das UI:

| Input-CSV | Herkunft |
|---|---|
| `mbi_curriculum_kategorisiert.csv` | 84 MBI-Kurse, manuell + LLM-gestützt Skill-annotiert |
| `mbi_curriculum_enriched_keywords.csv` | aus Kurstext extrahierte Stichwörter |
| `jobs_kategorisiert_ms_detail.csv` | 1'194 Stelleninserate, Skill-kategorisiert über LLM-Pipeline |

Wichtige Schritte:

- **IDF-Gewichtung pro Skill** — seltene Skills zählen mehr als generische
  (Formel: `log((N+1) / (df+1)) + 1`, analog TF-IDF)
- **Gruppen-Gewichtung** — harte Fachkompetenzen (FD, FK) werden stärker
  gewichtet als generische Soft-Skills (SK, MK, PK)
- **Deduplizierung** — identische Stellen (gleicher Titel + Firma) werden
  zu einem Eintrag verschmolzen (1'194 → 1'158 unique jobs)
- **Seniority-Erkennung** — Regex auf Jobtitel: junior / mid / senior / lead
- **ECTS-Gewicht pro Kurs** — 6 ECTS ≈ 2×, 4 ECTS ≈ 1.3×, 3 ECTS ≈ 1×
- **Sparseness-Flag** — Stellen mit <4 Skills als „dünn" markiert

Neu generieren lässt sich alles per:

```bash
cd interactive_explorer_v4
python3 build_assessment_data.py
```

### 2. Scoring-Engine (`js/assessment.js`)

Für jede Stelle *j* und gewählte Kurs-Skills *U* wird ein Match-Score
zwischen 0 und 1 berechnet:

```
covered(j) = j.skills ∩ U
num   = Σ w(s) · focus(s) · intensity(j,s)   für s ∈ covered(j)
denom = Σ w(s) · focus(s) · intensity(j,s)   für s ∈ j.skills
score = num / denom                         ∈ [0, 1]
```

mit
- `w(s) = IDF(s) × Gruppen-Gewicht`
- `focus(s)` = Slider-Einstellung (Tech-Fit ↔ Profil-Fit)
- `intensity(j,s)` = Bonus, wenn das Skill-Profil der Stelle in der
  jeweiligen Gruppe hohe Scores zeigt

Zusätzliche Signale:

- **Keyword-Kanal** — Fuzzy-Overlap zwischen Kurs-Keywords und Job-Titel
  (fängt Fachbegriffe ein, die in der Skill-Taxonomie fehlen)
- **Profil-Affinität** — Wenn Nutzer ein Wunsch-Profil setzt, bekommen
  passende Stellen einen sanften Boost
- **Seniority / Berufserfahrung** — als Filter, nicht als Score-Komponente

### 3. UI

- **Kurs-Picker links** — Checkbox-Liste mit Suchfeld; Doppelklick
  speichert/lädt ein „Favoriten-Profil" (localStorage)
- **Stelleliste rechts** — sortiert nach Match-Score; pro Karte:
  Score-Badge, abgedeckte Skills (grün), fehlende Skills (rot),
  plus **„Nächst-bester Kurs"**-Hinweis (reverse Skill→Kurs-Index)
- **5-Zell-Summary oben** — ø Match · Top-Skill · grösster Gap ·
  empfohlener Kurs · Profil-Verteilung
- **Controls** — Focus-Slider (Tech ↔ Soft), Seniority-Filter,
  Profil-Filter, Option „Sparse Jobs zeigen"

---

## 🛠 Build-/Run-Rezept

```bash
# 1. (optional) Datenbasis neu erzeugen
python3 build_assessment_data.py

# 2. Website starten
python3 -m http.server 8080
# → http://localhost:8080/

# Alternativ: index.html per Doppelklick öffnen (ohne Server)
```

Python-Abhängigkeiten: **nur Standard-Library** (`csv`, `json`, `re`, `math`).
JavaScript: **pure Vanilla JS + Plotly-CDN** für die Donut-Charts.

---

## 📖 Abgrenzung zu v1–v3

- **v1** (archiv/interactive_explorer) — Proof-of-Concept, inline CSS
- **v2** (archiv/interactive_explorer_v2) — erstes Design-System, HTML-Fetch-Self-Assessment
- **v3** (archiv/interactive_explorer_v3) — CSV-basiertes Assessment mit IDF
- **v4** (hier) — JSON-Datenpipeline, Tech/Soft-Split, Gap→Kurs-Empfehlung,
  deduplizierte Jobs, erklärbare Scoring-Formel

Alle älteren Versionen sind im Ordner `../archiv/` archiviert.
