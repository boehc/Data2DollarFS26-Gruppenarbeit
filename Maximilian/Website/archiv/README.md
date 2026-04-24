# Archiv — ältere Versionen der Website

Dieser Ordner enthält **ausschliesslich historische Iterationen** des MBI
Career Explorers. Sie dienen der Nachvollziehbarkeit des Entwicklungsverlaufs
und sind **nicht für die Bewertung relevant**.

> ➡ **Für die Abgabe bitte `../interactive_explorer_v4/` öffnen.**

---

## Entwicklungsverlauf

| Version | Ordner | Fokus | Generator-Skript |
|---|---|---|---|
| v1 | `interactive_explorer/` | Proof-of-Concept: Inline-CSS, statische HTML-Seiten pro Profil, Jobkarten mit Skill-Chips | `interactive_explorer.py` |
| v2 | `interactive_explorer_v2/` | Design-Refactor: externes CSS (`base.css`, `components.css`, …), Navigation, Hero-Layout, erstes Self-Assessment (HTML-Fetch-Ansatz) | `interactive_explorer_v2.py` |
| v3 | `interactive_explorer_v3/` | Self-Assessment-Rebuild mit CSV-Daten (ohne Fetch), IDF-Gewichtung, Tech/Soft-Breakdown, Premium-Redesign der Landingpage | `interactive_explorer_v3.py` |
| — | `refactor_pages.py` | Helferskript zum Einfügen des geteilten Headers/Footers in bestehende HTML-Seiten | — |

Die **aktuelle Version v4** ist aus v3 hervorgegangen; Datenpipeline und
Scoring-Algorithmus wurden in ein eigenständiges Python-Skript
(`build_assessment_data.py`) ausgelagert und das UI auf JSON-Daten umgestellt.
