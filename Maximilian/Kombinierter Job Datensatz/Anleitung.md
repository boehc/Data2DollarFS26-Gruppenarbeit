# Anleitung – Kombinierter Job Datensatz

Dieses Verzeichnis dokumentiert den gesamten Workflow zur Kombination, Kategorisierung und Visualisierung von Stelleninseraten aus zwei unterschiedlichen Quellen. Die Analyse basiert auf dem **Kompetenz-Framework nach Beck, Bartscher et al. (2012)** und ordnet die Inserate den **sechs Vertiefungsprofilen des MBI-Studiengangs** zu.

---

## Übersicht der Ordnerstruktur

```
1. Kombination Job Datensätze/     → Zusammenführung der Rohdaten
2. Kategorisierung der Ergebnisse/ → Kompetenz-Kategorisierung nach Beck
3. Visualisierung/                 → Statistische Auswertung und Grafiken
```

---

## 1. Kombination der Job-Datensätze

**Skript:** `1. Kombination Job Datensätze/merge_jobs.py`

### Ausgangslage

Es liegen zwei unabhängige Datensätze vor:

| Datensatz                               | Quelle   | Beschreibung                                |
|----------------------------------------|----------|---------------------------------------------|
| `indeed_jobs_bereinigt.csv`            | Indeed   | Bereinigte Stelleninserate von Indeed        |
| `jobs_anforderungen_clean (kopie).csv` | Jobs.ch  | Stelleninserate inkl. Anforderungen von Jobs.ch |

### Vorgehen

1. **Spalten vereinheitlichen:** Die unterschiedlichen Spaltennamen beider Quellen werden auf ein gemeinsames Schema gemappt (z. B. `titel` → `job_title`, `unternehmen` → `company`).
2. **Quellenkennung:** Eine Spalte `quelle` wird hinzugefügt (`"indeed"` bzw. `"jobs.ch"`), um die Herkunft nachvollziehbar zu machen.
3. **Zusammenführung:** Beide Datensätze werden per `pd.concat` vertikal kombiniert.
4. **Duplikat-Entfernung:** Anhand der Kombination `job_title + company + location` werden doppelte Einträge entfernt.

### Ergebnis

- **Output:** `jobs_combined.csv`
- **Gemeinsame Spalten:** `job_profil`, `job_title`, `company`, `location`, `anforderungen_sektion`, `requirements`, `full_description`, `veroeffentlicht_am`, `url`, `quelle`

---

## 2. Kategorisierung nach dem Kompetenz-Framework (Beck)

### 2a. Hauptkategorisierung

**Skript:** `2. Kategorisierung der Ergebnisse/kategorisierung.py`

Die Stelleninserate werden anhand von **Keyword-Matching (Regex)** in die vier Kompetenzdimensionen nach Beck, Bartscher et al. (2012) eingeordnet:

| Dimension                | Prefix | Beispiel-Unterkategorien                                         |
|--------------------------|--------|------------------------------------------------------------------|
| **Fachkompetenz**        | `FK_`  | Waren-/Produktkenntnisse, EDV-Kenntnisse, Fremdsprachen, Berufsausbildung |
| **Sozialkompetenz**      | `SK_`  | Teamfähigkeit, Kundenorientierung, Kooperationsfähigkeit          |
| **Methodenkompetenz**    | `MK_`  | Projektmanagement, Selbstmanagement, Kreatives Denken             |
| **Personale Kompetenz**  | `PK_`  | Motivation, Belastbarkeit, Aufgeschlossenheit                     |

Zusätzlich werden **detaillierte Fachkompetenzen** (`FD_`-Spalten) datengetrieben erfasst, z. B.:
- Programmiersprachen: Python, Java, JavaScript/TypeScript, C#, SQL
- Cloud & Infrastruktur: AWS/Azure/GCP, Docker/Kubernetes, DevOps
- Daten & Analytics: Data Science/ML, AI/KI, Data Engineering
- Business Software: SAP, Salesforce, ERP, CRM, MS Office
- Agile Methoden: Scrum, Kanban, SAFe

**Verfahren:**
- Für jedes Inserat wird ein Textfeld aus `requirements`, `anforderungen_sektion` und `full_description` zusammengebaut.
- Pro Unterkategorie wird eine binäre Spalte (0/1) erzeugt: 1 = mindestens ein Keyword-Pattern trifft zu.
- Pro Hauptdimension wird ein aggregierter Score berechnet (Summe der getroffenen Unterkategorien).

**Output:** `jobs_kategorisiert.csv`

### 2b. MS365-Tool-Detailanalyse

**Skript:** `2. Kategorisierung der Ergebnisse/ms_detail.py`

Zusätzlich zur Hauptkategorisierung wird eine **Aufschlüsselung der genannten Microsoft-365-Tools** durchgeführt. Dabei werden folgende Tools einzeln erfasst:

Excel, Word, PowerPoint, Outlook, SharePoint, Teams, Power BI, Power Automate, Power Apps, Dynamics 365, Visio, Project, Intune, Azure AD/Entra, Exchange, Copilot, OneDrive, Office 365 (allgemein).

**Output:** `jobs_kategorisiert_ms_detail.csv` (alle Spalten aus `jobs_kategorisiert.csv` + MS-Tool-Spalten + `MS_Tools_Score`)

---

## 3. Visualisierung der Ergebnisse

### 3a. Profil-Zuordnung auf 6 MBI-Vertiefungsprofile

**Skript:** `3. Visualisierung/profil_zuordnung.py`

Da nicht alle Inserate ein Profil aus der Indeed-Quelle besitzen, werden **alle 1'194 Stelleninserate** über **Keyword-basierte Regeln auf dem Jobtitel** einem der sechs MBI-Vertiefungsprofile zugeordnet:

| Profil                                      | Typische Keywords                                          |
|---------------------------------------------|-----------------------------------------------------------|
| Supply Chain & Operations Management        | supply chain, logistik, einkauf, procurement, lean         |
| Start-up & Scale-up Entrepreneurship        | startup, entrepreneur, innovation, product manager         |
| Technology Solution Architect               | software, developer, cloud, data engineer, IT architect    |
| Digital Channel & CRM                       | digital marketing, e-commerce, CRM, customer experience    |
| Business Development                        | business development, sales, account manager, vertrieb     |
| Transforming & Managing Digital Business    | Catch-all für alle übrigen Inserate                       |

Die Regeln sind **priorisiert** (spezifischere Profile zuerst), sodass jedes Inserat genau einem Profil zugeordnet wird.

**Skript:** `3. Visualisierung/export_mbi_profile.py`
Exportiert die finale CSV mit der neuen `mbi_profil`-Spalte anstelle der alten `job_profil`-Spalte.

### 3b. Statistische Visualisierung

**Skripte:**
- `3. Visualisierung/visualisierung_skills.py` (Version 1 – 5 Indeed-Profile)
- `3. Visualisierung/visualisierung_skills_v2.py` (Version 2 – 6 MBI-Profile, alle Inserate)

Die Visualisierung erzeugt publikationsreife Grafiken mit Seaborn/Matplotlib:

| Plot | Inhalt                                                          | Datei                                  |
|------|-----------------------------------------------------------------|----------------------------------------|
| 1    | Grouped Barplot: Durchschnittliche Kompetenz-Scores nach Profil (mit 95%-Konfidenzintervall) | `plot1_hauptkategorien_scores.png`     |
| 2    | 4 Heatmaps: Nennungshäufigkeit (%) der Unterkategorien pro Profil (FK, SK, MK, PK) | `plot2_unterkategorien_heatmaps.png`   |
| 3    | Horizontale Barplots: Top-Skills je Hauptkategorie (gesamt, in %) | `plot3_unterkategorien_barplots.png`   |

---

## Ablauf zur Reproduktion

Die Skripte sollten in folgender Reihenfolge ausgeführt werden:

```
1. merge_jobs.py                → erzeugt jobs_combined.csv
2. kategorisierung.py           → erzeugt jobs_kategorisiert.csv
3. ms_detail.py                 → erzeugt jobs_kategorisiert_ms_detail.csv
4. profil_zuordnung.py          → Anzeige der Profil-Zuordnung (Kontrolle)
5. export_mbi_profile.py        → erzeugt jobs_kategorisiert_mbi_profile.csv
6. visualisierung_skills_v2.py  → erzeugt Plot-PNGs
```

### Voraussetzungen

- Python 3.x
- Bibliotheken: `pandas`, `numpy`, `seaborn`, `matplotlib`
- Die CSV-Eingabedateien müssen im jeweiligen Ordner vorhanden sein (oder die Pfade entsprechend angepasst werden).
