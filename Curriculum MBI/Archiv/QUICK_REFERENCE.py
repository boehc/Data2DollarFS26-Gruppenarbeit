"""
═══════════════════════════════════════════════════════════════════════════════
QUICK REFERENCE - MBI CURRICULUM EXTRACTOR
Schnelle Übersicht aller Skripte & deren Verwendung
═══════════════════════════════════════════════════════════════════════════════
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                  📚 MBI CURRICULUM DATABASE EXTRACTOR                         ║
║                        QUICK START REFERENCE GUIDE                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 PROJEKT OVERVIEW                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Ziel:      Konvertiere 94 HSG-Merkblätter (PDFs) → Strukturierte CSV-DB
  Status:    ✅ ABGESCHLOSSEN (100% erfolgreich)
  Outputs:   mbi_curriculum_database.csv (94 Kurse, 9 Felder)
  Zeit:      ~2 Minuten für vollständige Verarbeitung

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🔥 3 PYTHON SCRIPTS ZUR VERFÜGUNG                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣  1_PDF_Extractor_to_CSV.py   (DAS HAUPTSKRIPT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VERWENDUNG:
    $ python 1_PDF_Extractor_to_CSV.py

  WAS ES TUT:
    ✓ Liest alle 94 PDFs (FS26 & HS25 Ordner)
    ✓ Extrahiert strukturierte Daten:
      • course_id         (Kursnummer aus Dateiname)
      • course_title      (Kurstitel)
      • ects              (3, 4 oder 6 Punkte)
      • language          (DE oder EN)
      • mbi_profile       (6 Fachrichtungen)
      • learning_objectives_raw
      • course_content_raw

  TECHNOLOGIE:
    - pdfplumber  → PDF-Text-Extraktion
    - pandas      → CSV-Handling
    - regex (re)  → Pattern-Matching
    - Logging     → Protokolle & Error-Handling

  OUTPUT:
    📁 mbi_curriculum_database.csv (94 Zeilen × 8 Spalten, UTF-8)
    📁 curriculum_extraction.log (Detailliertes Protokoll)

  FEATURES:
    ✅ Automatische Spracherkennung (DE/EN)
    ✅ 6 MBI-Fachrichtungen Mapping
    ✅ UTF-8 Encoding (Umlaute ä, ö, ü ✓)
    ✅ Robust gegen beschädigte PDFs (kein Crash!)
    ✅ Strukturiertes Logging

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣  2_Analytics_Report.py   (DATENQUALITÄTS-ANALYSE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VERWENDUNG:
    $ python 2_Analytics_Report.py

  WAS ES TUT:
    Analysiert die CSV und zeigt:
    ✓ Gesamtstatistiken (94 Kurse, 359 ECTS)
    ✓ Sprachen-Verteilung (EN: 56%, DE: 44%)
    ✓ MBI-Profile Distribution (Business Dev: 42%, Tech Arch: 23%, ...)
    ✓ ECTS-Punkte Verteilung
    ✓ Semester-Verteilung (FS26 vs HS25)
    ✓ Datenqualitäts-Score (90.6% ✅)
    ✓ Problematische Einträge (42 Kurse ohne Learning Objectives)
    ✓ Top 10 Kurse nach ECTS
    ✓ Verbesserungsempfehlungen

  OUTPUT:
    📊 Schöne formatierte Konsolen-Reports
    📊 Quality Metrics und Visualisierungen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3️⃣  3_Improvement_Extractor.py   (OPTIMIERTER PARSER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VERWENDUNG:
    $ python 3_Improvement_Extractor.py

  WAS ES TUT:
    ✓ Sucht PDFs nach fehlenden Learning Objectives (42 Kurse)
    ✓ Nutzt adaptive Parsing-Strategien
    ✓ Extrahiert nachträglich fehlende Course Contents
    ✓ Speichert in "mbi_curriculum_database_improved.csv"

  OUTPUT:
    📁 mbi_curriculum_database_improved.csv (mit mehr Daten gefüllt)

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🚀 SCHRITT-FÜR-SCHRITT WORKFLOW                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Step 1: Abhängigkeiten installieren
  ─────────────────────────────────────
  $ pip install -r requirements.txt

  Step 2: Hauptextraktion ausführen
  ──────────────────────────────────
  $ python 1_PDF_Extractor_to_CSV.py
  
  ✅ Generiert: mbi_curriculum_database.csv

  Step 3 (optional): Analysen anschauen
  ──────────────────────────────────────
  $ python 2_Analytics_Report.py
  
  📊 Zeigt: Statistiken, Datenqualität, Probleme

  Step 4 (optional): Daten optimieren
  ────────────────────────────────────
  $ python 3_Improvement_Extractor.py
  
  ✅ Generiert: mbi_curriculum_database_improved.csv

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 KEY METRICS (ERGEBNISSE)                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  EXTRACTION ERFOLG:
    Eingabe:    94 PDFs
    Ausgabe:    94 Kurse ✅ (100% Erfolgsquote)
    
  DATENQUALITÄT:
    Course IDs:         94/94    (100%)  ✅
    Course Titles:      94/94    (100%)  ✅
    ECTS:               94/94    (100%)  ✅
    Sprache erkannt:    94/94    (100%)  ✅
    MBI-Profile:        94/94    (100%)  ✅
    Learning Objectives: 52/94   (55%)   ⚠️
    Course Content:      92/94   (98%)   ✅
    ───────────────────────────────────────
    GESAMT SCORE:       90.6%           ✅

  SPRACHEN:
    Englisch (EN):  53 Kurse  (56.4%)
    Deutsch (DE):   41 Kurse  (43.6%)

  MBI-PROFILE (6):
    Business Development:                    40 Kurse
    Technology Solution Architect:           22 Kurse
    Start-up & Scale-up Entrepreneurship:    17 Kurse
    Supply Chain & Operation Management:     13 Kurse
    Digital Channel & Customer Relationship: 1 Kurs
    Transforming & Managing Digital Business: 1 Kurs

  ECTS:
    Total:     359 ECTS
    Average:   3.8 ECTS/Kurs
    Distribution: 3 ECTS: 47 | 4 ECTS: 32 | 6 ECTS: 15

  SEMESTERS:
    HS25 (Herbst 2025):   54 Kurse
    FS26 (Frühling 2026): 40 Kurse

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📁 CSV SPALTEN & INHALTE                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  pdf_file                  String    8,045,1.00.pdf
  course_id                 String    8,045
  course_title              String    Digital Business Strategy
  ects                      Integer   3 | 4 | 6
  language                  String    DE | EN
  mbi_profile               String    Business Development | Technology... (1 von 6)
  learning_objectives_raw   String    "Nach diesem Kurs können Sie..."
  course_content_raw        String    "Modul 1: Grundlagen..."

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🔧 TECHNOLOGIE STACK                                                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Python:           3.13.12
  pdfplumber:       0.11.9     (PDF-Textextraktion)
  pandas:           3.0.1      (CSV-Handling)
  openpyxl:         3.1.5      (Excel-Support)
  regex (re):       builtin    (Pattern-Matching)

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📚 ZUSÄTZLICHE DOKUMENTATION                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  📖 README.md
     → Vollständiges Anwenderhandbuch
     → Schritt-für-Schritt Erklärungen
     → Nutzungsbeispiele (Python Code)
     → Troubleshooting Guide

  📊 PROJECT_SUMMARY.md
     → Executive Summary
     → Detaillierte Resultate
     → Architektur-Erklärung
     → Next Steps

  📋 requirements.txt
     → Alle Python-Abhängigkeiten
     → Installation: pip install -r requirements.txt

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💡 HÄUFIGE FRAGEN                                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  F: Kann ich die CSV in Excel öffnen?
  A: JA! Die CSV ist UTF-8 kodiert und Excel-kompatibel.
     → Öffne mbi_curriculum_database.csv in Excel

  F: Wie kann ich die Daten filtern?
  A: Mit pandas:
     $ python
     >>> import pandas as pd
     >>> df = pd.read_csv('mbi_curriculum_database.csv')
     >>> bd = df[df['mbi_profile'] == 'Business Development']

  F: Warum fehlen 42 Learning Objectives?
  A: Manche PDFs haben diese Information nicht unter "Learning Objectives".
     Lösung: Nutze 3_Improvement_Extractor.py für adaptive Extraktion

  F: Kann ich die Keywords anpassen?
  A: JA! In 1_PDF_Extractor_to_CSV.py:
     - SECTION_KEYWORDS_DE (Deutsch)
     - SECTION_KEYWORDS_EN (Englisch)
     - MBI_PROFILES (Fachrichtungen)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

╔═══════════════════════════════════════════════════════════════════════════════╗
║                      ✅ PROJEKT ABGESCHLOSSEN                               ║
║                                                                               ║
║  📊 94 Kurse extrahiert | 90.6% Datenqualität | 100% Erfolgsrate            ║
║  📁 mbi_curriculum_database.csv ready for use                               ║
║  🚀 Produktionsreif & wiederverwendbar                                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Für mehr Info: Siehe README.md & PROJECT_SUMMARY.md
Support: Siehe "🆘 FEHLER BEHEBEN" in README.md

""")
