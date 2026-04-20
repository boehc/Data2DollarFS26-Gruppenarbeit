# 🎓 Data2Dollar FS26 – Gruppenarbeit

> **MBI HSG Projekt | April 2026**  
> Datengetriebene Entscheidungshilfe für MBI-Studierende: Gründen oder Anstellen lassen?

---

## 📋 Projekt-Übersicht

Dieses Repository enthält die **vollständige Gruppenarbeit** des Data2Dollar-Moduls im Frühjahrssemester 2026. Das Projekt beantwortet die zentrale Frage:

> **Wo lohnt sich eine Gründung aus dem MBI – und welche Fähigkeiten werden am Arbeitsmarkt gesucht?**

Wir analysieren **drei Pfade** für MBI-Absolvent:innen:
- **Pfad A:** Gründen (Startup-Investments & Trends)
- **Pfad B:** Angestellt werden (Jobmarkt-Analyse)
- **Curriculum:** MBI-Kurskatalog mit Skills-Mapping

---

## 📁 Ordnerstruktur

```
Data2DollarFS26-Gruppenarbeit/
├── README.md                    ← Diese Datei (Hauptübersicht)
│
├── Curriculum MBI/              ← MBI-Kurskatalog-Pipeline
│   ├── 0_mbi_curriculum_final.csv     ← ENDRESULTAT: Alle Kurse + Keywords
│   ├── 0_Scraper_*.py                 ← Web-Scraper für HSG-Merkblätter
│   ├── 1_PDF_Extractor_to_CSV.py      ← PDF → CSV Konvertierung
│   ├── 2_extract_keywords_pipeline.py ← OpenAI Keyword-Extraktion
│   ├── ANLEITUNG.txt                  ← ⭐ Vollständige Pipeline-Anleitung
│   └── Kurskataloge/                  ← Heruntergeladene PDF-Merkblätter
│
├── Lizzy/                       ← Pfad A: Gründen
│   ├── VC und Startup Investments/    ← Schweizer VC-Analyse (1'327 Deals)
│   ├── Trends/                        ← Tech-Media Trends (8'476 Artikel)
│   └── Webseite Gründerin/            ← Interaktive Website (HTML/JS)
│
└── Maximilian/                  ← Pfad B: Angestellt werden
    ├── Indeed/                        ← Indeed.ch Scraper + Daten
    ├── JobsCH/                        ← Jobs.ch Scraper + Daten
    ├── Job Datensatz/                 ← Bereinigter Gesamtdatensatz
    ├── Visualisierung MBI Curriculum/ ← Curriculum-Visualisierungen
    └── Website/                       ← Interactive Explorer
```

---

## 🎯 Für Professor:innen: Schnell-Navigation

### ⭐ Wichtigste Dateien für die Bewertung

| Priorität | Pfad | Beschreibung |
|-----------|------|--------------|
| ⭐⭐⭐ | `Lizzy/VC und Startup Investments/docs/PROFESSOR_OVERVIEW.md` | VC-Analyse Zusammenfassung (2-3 Min) |
| ⭐⭐⭐ | `Lizzy/Trends/Anleitung Trends.md` | Tech-Trends Dokumentation |
| ⭐⭐⭐ | `Lizzy/Webseite Gründerin/README.md` | Website-Dokumentation |
| ⭐⭐⭐ | `Curriculum MBI/ANLEITUNG.txt` | Curriculum-Pipeline Anleitung |
| ⭐⭐ | `Maximilian/Job Datensatz/` | Jobmarkt-Gesamtdatensatz |

### 📊 Finale Ergebnisdateien

| Datei | Beschreibung |
|-------|--------------|
| `Curriculum MBI/0_mbi_curriculum_final.csv` | 86 MBI-Kurse mit Keywords & Profil-Flags |
| `Lizzy/VC und Startup Investments/results/INVESTMENT_RECOMMENDATIONS.csv` | Buy/Hold/Avoid Signale pro Branche |
| `Lizzy/Trends/Trends_Data/keyword_monthly_normalized.csv` | Normalisierte Trend-Daten |
| `Maximilian/Job Datensatz/jobs_combined.csv` | Bereinigter Jobmarkt-Datensatz |

---

## 📚 Detaillierte Beschreibung der Ordner

### 1️⃣ Curriculum MBI

**Zweck:** Scrapen und Analysieren des MBI-Kurskatalogs der HSG

**Pipeline:**
1. **Scraper** → Lädt alle PDF-Merkblätter von der HSG-Website
2. **PDF-Extraktion** → Konvertiert PDFs in strukturiertes CSV
3. **Keyword-Extraktion** → OpenAI analysiert Kursbeschreibungen
4. **Startup-Filter** → Filtert gründungsrelevante Keywords

**Endresultat:** `0_mbi_curriculum_final.csv` mit allen Kursen, Metadaten, MBI-Profil-Zuordnungen und relevanten Keywords.

**Dokumentation:** Siehe `ANLEITUNG.txt` für vollständige Schritt-für-Schritt Anleitung.

---

### 2️⃣ Lizzy – Pfad A: Gründen

Enthält drei miteinander verbundene Analysen für Gründungsinteressierte:

#### 📈 VC und Startup Investments
- **Datenquelle:** Startupticker.ch + Venture Kick (2023–2026)
- **Umfang:** 1'327 klassifizierte Startup-Deals
- **Methodik:** LLM-gestützte Branchenklassifikation
- **Output:** Investment-Empfehlungen (Buy/Hold/Avoid) pro Branche
- **Dokumentation:** `VC und Startup Investments/README.md`

#### 📰 Trends (Tech-Media Analyse)
- **Datenquelle:** TechCrunch + HackerNews (2023–2026)
- **Umfang:** 8'476 klassifizierte Artikel
- **Methodik:** Zwei-Ebenen-Keyword-System (Tech + Industry)
- **Output:** Normalisierte Trend-Zeitreihen
- **Dokumentation:** `Trends/Anleitung Trends.md`

#### 🌐 Webseite Gründerin
- **Technologie:** Vanilla HTML/CSS/JS + Plotly.js
- **Features:** Interaktive Charts, Momentum Matrix, Kurs-Matching
- **Seiten:** 
  - Landing Page (Übersicht)
  - Trends (Tech-Trends Timeline)
  - Investments (VC-Deals Schweiz)
  - Opportunity (Momentum Matrix + Empfehlungen)
  - Courses (MBI-Kursabgleich)
- **Dokumentation:** `Webseite Gründerin/README.md`

---

### 3️⃣ Maximilian – Pfad B: Angestellt werden

Analyse des Schweizer Jobmarkts für MBI-Absolvent:innen:

#### 💼 Indeed
- Web-Scraper für Indeed.ch
- Rohdaten + Bereinigungsscripts

#### 💼 JobsCH
- Web-Scraper für Jobs.ch
- Rohdaten + Bereinigungsscripts

#### 📊 Job Datensatz
- **Zusammengeführter Datensatz** aus beiden Quellen
- Kategorisierung nach Branchen
- Visualisierungen der Anforderungen

#### 📈 Visualisierung MBI Curriculum
- Verknüpft Jobmarkt-Anforderungen mit MBI-Kursen
- Kategorisierung der Kurse nach Relevanz
- Plots und Analysen

#### 🖥️ Website
- Interactive Explorer für die Daten
- Mehrere Versionen (v1–v3)

---

## 🔧 Technische Voraussetzungen

### Python-Umgebung
```bash
# Virtuelle Umgebung erstellen
python -m venv .venv

# Aktivieren
source .venv/bin/activate       # Mac/Linux
.venv\Scripts\activate          # Windows

# Dependencies installieren (je nach Modul)
pip install -r requirements.txt
```

### Benötigte Software
- **Python 3.11+**
- **Google Chrome** (für Selenium-Scraper)
- **OpenAI API Key** (für Keyword-Extraktion im Curriculum-Modul)

---

## 👥 Team

| Name | Verantwortungsbereich |
|------|----------------------|
| **Lizzy** | VC-Investments, Tech-Trends, Website Gründerin |
| **Maximilian** | Jobmarkt-Analyse, Curriculum-Visualisierung |
| **Team** | Curriculum MBI Pipeline |

---

## 📅 Zeitraum

- **Datenerhebung:** Januar – April 2026
- **Analysezeitraum:** 2023 – Q1 2026
- **Abgabe:** April 2026

---

## ⚠️ Hinweise zur Datenqualität

1. **Schweizer Fokus:** VC-Daten beziehen sich auf die Schweiz (Startupticker.ch, Venture Kick)
2. **GenAI-Kategorie:** Bezeichnet AI-Native Startups, nicht GenAI als Querschnittstechnologie
3. **Momentum:** Misst Veränderung des Marktanteils, nicht absolute Deal-Zahlen
4. **Jobdaten:** Snapshot vom April 2026, keine historischen Vergleiche

---

## 🚀 Schnellstart für Bewertung

1. **Überblick gewinnen:** Diese README lesen
2. **Pfad A (Gründen):** 
   - `Lizzy/VC und Startup Investments/docs/PROFESSOR_OVERVIEW.md` → 2-3 Min
   - `Lizzy/Trends/Anleitung Trends.md` → Methodik verstehen
3. **Pfad B (Angestellt):**
   - `Maximilian/Job Datensatz/jobs_combined.csv` → Daten prüfen
4. **Curriculum:**
   - `Curriculum MBI/ANLEITUNG.txt` → Pipeline nachvollziehen
5. **Website anschauen:**
   - `Lizzy/Webseite Gründerin/index.html` → Im Browser öffnen

---

*Erstellt: 20. April 2026 | MBI HSG | Data2Dollar FS26*
