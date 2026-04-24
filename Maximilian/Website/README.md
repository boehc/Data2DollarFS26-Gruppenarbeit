# MBI Career Explorer — Website

Interaktive Analyse von **1'194 Stelleninseraten** aus dem Schweizer Arbeitsmarkt,
zugeordnet zu den **6 Vertiefungsprofilen** des MBI-Studiengangs der Universität
St. Gallen (Frühlingssemester 2026).

---

## 📂 Ordnerstruktur

```
Website/
├── interactive_explorer_v4/   ← AKTUELLE VERSION (für die Bewertung)
├── archiv/                    ← ältere Iterationen (v1, v2, v3, Build-Skripte)
└── README.md                  ← diese Datei
```

Frühere Versionen sind im Ordner `archiv/` abgelegt und dokumentieren den
Entwicklungsverlauf (Rapid-Prototyping → Design-Refactor → datengetriebene Version).

---

## 🚀 Website starten

### Option A — Einfach (Doppelklick)

Im Ordner `interactive_explorer_v4/` die Datei **`index.html`** per Doppelklick
im Browser öffnen. Die Daten werden aus den vor-generierten `data/*_data.js`
Dateien geladen, d. h. es wird **kein Server benötigt**.

### Option B — Lokaler Dev-Server (empfohlen für Self-Assessment)

```bash
cd Maximilian/Website/interactive_explorer_v4
python3 -m http.server 8080
```

Anschliessend im Browser öffnen: <http://localhost:8080/>

> **Warum Option B für Self-Assessment?** Die `assessment.html` lädt zuerst
> per `fetch()` die JSON-Dateien (frische Daten). Fehlt der Server, fällt das
> Script automatisch auf die eingebetteten `*_data.js` zurück — funktioniert
> also beides, aber über einen Server greifen Änderungen am Datenstand sofort.

### Option C — Windows

Im Ordner liegt eine `start_server.bat`, die unter Windows per Doppelklick
Python startet und den Browser öffnet.

---

## 🗂 Seitenstruktur (v4)

| Datei | Inhalt |
|---|---|
| `index.html` | Landingpage mit Markt-Überblick (Plotly-Donut, Kennzahlen) + 6 Profil-Karten |
| `profil_*.html` | 6 Profil-Detailseiten: Top-Skills, Top-Kurse, Stelleninserate mit Skill-Gap-Analyse |
| `assessment.html` | **Self-Assessment**: Student:in wählt belegte Kurse → System zeigt passende Stellen |

Details zur Methodik und zum Self-Assessment stehen in
[`interactive_explorer_v4/README.md`](interactive_explorer_v4/README.md).

---

## 📊 Datenquellen

| Quelle | Zweck |
|---|---|
| `Maximilian/Job Datensatz/Kategorisierung/jobs_kategorisiert_ms_detail.csv` | 1'194 Stelleninserate, automatisch kategorisiert nach Skills und MBI-Profil |
| `Maximilian/Visualisierung MBI Curriculum/mbi_curriculum_kategorisiert.csv` | 84 MBI-Kurse mit Skill-Zuordnung |
| `Maximilian/Visualisierung MBI Curriculum/mbi_curriculum_enriched_keywords.csv` | Aus Kurstexten extrahierte Stichwörter (freier Text-Kanal) |

---

## 👨‍💻 Autor

Maximilian — Data2Dollar FS26, Universität St. Gallen
