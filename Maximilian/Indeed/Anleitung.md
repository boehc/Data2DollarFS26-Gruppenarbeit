# Anleitung – Indeed Job Scraping & Bereinigung

Dieses Verzeichnis enthält den gesamten Workflow zur Erhebung und Aufbereitung von Stellenanzeigen der Plattform **ch.indeed.com** für die Gruppenarbeit (MBI HSG Berufsfelder).

Der Prozess ist in zwei Schritte unterteilt:

---

## 1. Daten Scrapen (`1. Daten Scrapen/`)

### Ziel

Stellenanzeigen aus der Deutschschweiz für fünf MBI-relevante Berufsprofile von Indeed extrahieren:

- **Business Developer**
- **Digital Channel & Relationship Manager**
- **IT Manager**
- **Startup & Technology Entrepreneur**
- **Supply Chain & Operations Manager**

### Vorgehen

Es existieren zwei Scraper-Varianten:

| Datei | Technologie | Beschreibung |
|---|---|---|
| `scrape_indeed.py` | Selenium + undetected-chromedriver | **Hauptskript** – nutzt verschiedene Suchvariationen pro Profil und Standort, um die Einschränkung von Indeed (Login ab Seite 2) zu umgehen. |
| `indeed/spiders/getdata.py` | Scrapy + Selenium | Alternativansatz als Scrapy-Spider, paginiert über den „Weiter"-Button. |

#### Funktionsweise (`scrape_indeed.py`)

1. **Suchstrategie:** Für jedes Berufsprofil sind mehrere Keyword-Varianten definiert (z.B. `"business developer"`, `"business development"`, `"title:business developer"` etc.). Diese werden mit 15 Deutschschweizer Standorten (Zürich, Bern, Basel, Luzern usw.) kombiniert.
2. **Browser-Automatisierung:** Ein Chrome-Browser wird über `undetected-chromedriver` gestartet, um die Bot-Erkennung von Indeed/Cloudflare zu umgehen.
3. **Extraktion pro Suchanfrage:** Auf der Ergebnisseite werden alle Jobkarten geparst (Titel, Firma, Standort, Job-URL). Anschliessend wird jede Detailseite aufgerufen, um die vollständige Beschreibung und die Requirements zu extrahieren.
4. **Deduplizierung:** Bereits gescrapte Jobs (anhand des Indeed-Job-Keys `jk`) werden übersprungen.
5. **Export:** Die Daten werden laufend in `indeed_jobs.csv` geschrieben (Append-Modus).

#### Extrahierte Felder

| Feld | Beschreibung |
|---|---|
| `job_profil` | Zugeordnetes Berufsprofil |
| `job_title` | Stellenbezeichnung |
| `company` | Firmenname |
| `location` | Arbeitsort |
| `requirements` | Extrahierte Anforderungen |
| `full_description` | Vollständige Jobbeschreibung |
| `job_url` | Link zur Stellenanzeige |

#### Ausführung

```bash
cd "1. Daten Scrapen"
python3 scrape_indeed.py
```

> **Hinweis:** Zwischen den Anfragen werden zufällige Pausen eingebaut, um ein menschliches Surfverhalten zu simulieren. Das Scraping dient ausschliesslich Lern- und Forschungszwecken.

### Voraussetzungen

- Python 3.12+
- `undetected-chromedriver`, `selenium`
- Google Chrome installiert

---

## 2. Daten Bereinigen (`2. Daten Bereinigen/`)

### Ziel

Die Rohdaten aus Schritt 1 bereinigen, filtern und die wichtigsten Skills/Keywords pro Berufsprofil extrahieren.

### Vorgehen (`bereinigung.py`)

Das Skript durchläuft vier Schritte:

#### Schritt 1 – Requirements normalisieren

Die Requirements sind in den Rohdaten häufig nicht sauber vom Rest der Jobbeschreibung getrennt. Das Skript erkennt mittels Regex-Patterns die Abschnittsüberschriften (z.B. „Ihr Profil", „Requirements", „Was du mitbringst") und extrahiert gezielt den Anforderungsteil aus der vollständigen Beschreibung.

#### Schritt 2 – Relevanzfilter

Jede Stellenanzeige erhält einen **Relevanz-Score**, der anhand von Mustern in den Requirements und im Jobtitel berechnet wird:

- **Positive Signale** (z.B. „Business Administration", „Projektmanagement", „Digital Transformation", „Supply Chain Management") erhöhen den Score.
- **Negative Signale** (z.B. reine Software-Entwickler-Anforderungen, Handwerk, Pflege, PhD-Stellen) senken den Score.
- Jobs mit einem Score unter dem Schwellenwert (< -2) werden als **nicht MBI-relevant** aussortiert.

Zusätzlich wird ein **Erfahrungsfilter** angewandt: Stellen, die mehr als 3 Jahre Berufserfahrung fordern, werden entfernt, da sie für Masterabsolvent:innen nicht realistisch sind.

#### Schritt 3 – Keyword/Skill-Extraktion

Für jedes Berufsprofil werden die häufigsten und relevantesten Keywords mittels **TF-IDF** (Term Frequency – Inverse Document Frequency) mit Uni-, Bi- und Trigrammen extrahiert. Eine umfangreiche Stopwort-Liste (DE + EN) filtert generische Füllwörter heraus.

#### Schritt 4 – Export

| Ausgabedatei | Inhalt |
|---|---|
| `indeed_jobs_bereinigt.csv` | Bereinigte Stellenanzeigen (nach Relevanz- und Erfahrungsfilter) |
| `skill_haeufigkeiten.csv` | Top-Keywords pro Berufsprofil mit TF-IDF-Score und Häufigkeit |

#### Ausführung

```bash
cd "2. Daten Bereinigen"
python3 bereinigung.py
```

### Voraussetzungen

- Python 3.12+
- `pandas`, `numpy`, `scikit-learn`

---

## Zusammenfassung des Workflows

```
1. Daten Scrapen                         2. Daten Bereinigen
┌──────────────────────┐                 ┌──────────────────────────────┐
│  scrape_indeed.py    │                 │  bereinigung.py              │
│                      │                 │                              │
│  ch.indeed.com  ──►  │  indeed_jobs    │  1. Requirements extrahieren │
│  Selenium + Chrome   │──── .csv ──────►│  2. Relevanzfilter (Score)   │
│  15 Standorte        │                 │  3. Erfahrungsfilter (≤ 3J)  │
│  5 Berufsprofile     │                 │  4. TF-IDF Skill-Extraktion  │
└──────────────────────┘                 └──────────┬───────────────────┘
                                                    │
                                         ┌──────────▼───────────────────┐
                                         │  indeed_jobs_bereinigt.csv   │
                                         │  skill_haeufigkeiten.csv     │
                                         └──────────────────────────────┘
```
