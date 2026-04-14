"""
═══════════════════════════════════════════════════════════════════════════════
MBI Curriculum Database Extractor
Extrahiert strukturierte Daten aus HSG-Merkblättern (PDFs) → CSV-Export
═══════════════════════════════════════════════════════════════════════════════

Technologie:
  - pdfplumber: Robuste PDF-Text-Extraktion mit Formatierungserkennung
  - pandas: CSV-Verarbeitung und Strukturierung
  - regex: Pattern-Matching für Sektionen und Metadaten

Funktionen:
  1. extract_text_from_pdf(pdf_path) → Extrahiert Rohtexte
  2. detect_language(text) → Deutscher vs. Englischer Text
  3. parse_course_content(text, course_id) → Strukturierte Datenextraktion
  4. identify_mbi_profile(text) → Mapping auf 6 Fachrichtungen
  5. save_to_csv(data, output_path) → UTF-8 Speicherung
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import traceback

import pdfplumber
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING KONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('curriculum_extraction.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURATION & KONSTANTEN
# ─────────────────────────────────────────────────────────────────────────────

# MBI Profile / Fachrichtungen (6 offizielle Fokusrichtungen)
MBI_PROFILES = [
    "Business Development",
    "Digital Channel & Customer Relationship Management",
    "Start-up & Scale-up Entrepreneurship",
    "Supply Chain & Operation Management",
    "Technology Solution Architect",
    "Transforming and Managing Digital Business"
]

# Sektion-Keywords (Deutsch).
SECTION_KEYWORDS_DE = {
    'learning_objectives': ['Lernziele', 'Lernziel', 'Kompetenzen'],
    'course_content': ['Kursinhalte', 'Kursinhalt', 'Inhalte', 'Themen'],
    'prerequisites': ['Voraussetzungen', 'Voraussetzung', 'Anforderungen'],
    'learning_methods': ['Lernmethoden', 'Methode', 'Lehrmethoden'],
    'evaluation': ['Leistungsbeurteilung', 'Bewertung', 'Prüfung'],
}

# Section Keywords (English)
SECTION_KEYWORDS_EN = {
    'learning_objectives': ['Learning objectives', 'Learning Objectives', 'Competencies'],
    'course_content': ['Course content', 'Content', 'Topics', 'Contents'],
    'prerequisites': ['Prerequisites', 'Prerequisite', 'Requirements'],
    'learning_methods': ['Learning methods', 'Method', 'Teaching methods'],
    'evaluation': ['Performance assessment', 'Grading', 'Examination'],
}

# Verzeichnisse mit PDFs
PDF_DIRECTORIES = [
    Path("FS26_mbi_ohne_wahlbereich"),
    Path("HS25_mbi_ohne_wahlbereich")
]

OUTPUT_CSV = "mbi_curriculum_database.csv"

# ─────────────────────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN - SPRACH-ERKENNUNG
# ─────────────────────────────────────────────────────────────────────────────

def detect_language(text: str) -> str:
    """
    Erkennt, ob der Text auf Deutsch oder Englisch ist.
    Basiert auf häufige Wörter und Keywords.
    
    Args:
        text: Rohtexte aus PDF
        
    Returns:
        'de' oder 'en'
    """
    text_lower = text.lower()
    
    # Deutsche Indikatoren
    german_indicators = [
        'lernziele', 'kursinhalte', 'voraussetzung', 'leistungsbewertung',
        'lernmethoden', 'unterrichtssprache', 'deutsch', 'lehrkraft', 'prüfung'
    ]
    
    # English indicators
    english_indicators = [
        'learning objectives', 'course content', 'prerequisites', 'assessment',
        'teaching methods', 'language of instruction', 'english', 'instructor', 'examination'
    ]
    
    de_count = sum(1 for indicator in german_indicators if indicator in text_lower)
    en_count = sum(1 for indicator in english_indicators if indicator in text_lower)
    
    # Wenn beide gleich: Prüfe nach "ä", "ö", "ü" (eher Deutsch) vs. häufige englische Wörter
    if de_count == en_count:
        umlaute_count = text.count('ä') + text.count('ö') + text.count('ü')
        if umlaute_count > 5:
            return 'de'
        return 'en'
    
    return 'de' if de_count > en_count else 'en'

# ─────────────────────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN - TEXT-EXTRAKTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrahiert Rohtexte aus PDF mit pdfplumber.
    Erhält Zeilenumbrüche und Zeilenabstände.
    
    Args:
        pdf_path: Pfad zur PDF-Datei
        
    Returns:
        Extrahierter Text
        
    Raises:
        Exception: Falls PDF nicht lesbar
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
                text += "\n"
            return text
    except Exception as e:
        logger.error(f"❌ Fehler beim Lesen von {pdf_path.name}: {str(e)}")
        raise

def clean_text(text: str) -> str:
    """
    Bereinigt Text: entfernt doppelte Leerzeichen, normalisiert Zeilenumbrüche.
    """
    # Entferne doppelte/mehrfache Leerzeilen
    text = re.sub(r'\n\n+', '\n\n', text)
    # Entferne mehrfache Leerzeichen (behalte aber absichtliche Einrückungen)
    text = re.sub(r'  +', ' ', text)
    return text.strip()

def extract_field_by_keywords(text: str, keywords: List[str], language: str = 'de') -> str:
    """
    Findet einen Textabschnitt, der mit einem der Keywords beginnt.
    Extrahiert den darauf folgenden Absatz bis zur nächsten Überschrift.
    
    Args:
        text: Rohtexte
        keywords: Mögliche Überschriften-Keywords
        language: 'de' oder 'en'
        
    Returns:
        Extrahierter Absatz oder ""
    """
    text_lower = text.lower()
    
    # Suche nach jedem Keyword
    for keyword in keywords:
        pattern = re.escape(keyword)
        match = re.search(pattern, text_lower, re.IGNORECASE)
        
        if match:
            start_pos = match.end()
            
            # Definiere Muster für Sektionen-Ende (nächste Überschrift)
            # Das ist typisch: Großbuchstaben am Zeilenanfang oder bekannte Keywords
            all_keywords = list(SECTION_KEYWORDS_DE.values()) + list(SECTION_KEYWORDS_EN.values())
            all_keywords_flat = [kw for sublist in all_keywords for kw in sublist]
            
            # Simple Heuristik: bis zur nächsten Zeile, die mit Großbuchstabe beginnt
            # oder ein bekanntes Sektions-Keyword enthält
            end_pattern = r'\n(?=[A-Z]{2,}|\b(?:' + '|'.join([re.escape(kw) for kw in all_keywords_flat[:15]]) + r'))'
            end_match = re.search(end_pattern, text[start_pos:], re.IGNORECASE)
            
            if end_match:
                end_pos = start_pos + end_match.start()
                content = text[start_pos:end_pos]
            else:
                # Wenn kein Ende gefunden, nimm bis zum Ende
                content = text[start_pos:]
            
            content = clean_text(content)
            if len(content.strip()) > 20:  # Nur wenn substantieller Inhalt
                return content
    
    return ""

# ─────────────────────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN - METADATEN-EXTRAKTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_course_id_from_filename(filename: str) -> str:
    """
    Extrahiert Kursnummer aus Dateinamen.
    Beispiele: "8,045,1.00.pdf" → "8,045" oder "8045"
    
    Args:
        filename: PDF-Dateiname
        
    Returns:
        Kursnummer als String
    """
    # Versuche Muster wie "8,045" zu extrahieren
    match = re.search(r'(\d+[.,]\d+)', filename)
    if match:
        return match.group(1)
    
    # Fallback: nur Zahlen
    match = re.search(r'(\d+)', filename)
    if match:
        return match.group(1)
    
    return "UNKNOWN"

def extract_course_title(text: str) -> str:
    """
    Extrahiert Kurstitel - typisch in Kopfzeile oder nach "Title:" / "Titel:"
    
    Args:
        text: Rohtexte
        
    Returns:
        Kurstitel oder ""
    """
    # Suche nach explizitem "Title:" / "Titel:" Pattern
    match = re.search(r'(?:Title|Titel):\s*([^\n]+)', text, re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    
    # Fallback: Erste Zeile, die nicht leer ist
    lines = text.split('\n')
    for line in lines:
        line_cleaned = line.strip()
        if line_cleaned and len(line_cleaned) > 5 and not any(c.isdigit() for c in line_cleaned[:3]):
            return line_cleaned
    
    return ""

def extract_ects(text: str) -> Optional[int]:
    """
    Extrahiert Anzahl ECTS Credits.
    Muster: "ECTS Credits: 3" oder "3 ECTS" oder "Credits: 3"
    
    Args:
        text: Rohtexte
        
    Returns:
        ECTS als Integer oder None
    """
    # Deutsche und englische Patterns
    patterns = [
        r'ECTS\s*(?:Credits|Punkte)?:?\s*(\d+)',
        r'(?:Credits|Punkte|Leistungspunkte):\s*(\d+)',
        r'(\d+)\s*(?:ECTS|Credits|Leistungspunkte)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
    
    return None

# ─────────────────────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN - MBI PROFILE MATCHING
# ─────────────────────────────────────────────────────────────────────────────

def identify_mbi_profile(text: str) -> str:
    """
    Identifiziert die MBI-Fachrichtung basierend auf Keywords im Text.
    
    Suchmuster:
      - Prerequisites / Voraussetzungen
      - Course information
      - Content keywords
    
    Args:
        text: Rohtexte
        
    Returns:
        Name der erkannten Fachrichtung oder "Not Classified"
    """
    text_lower = text.lower()
    
    # Profile-spezifische Keywords
    profile_keywords = {
        "Business Development": [
            "business development", "market", "strategy", "business model",
            "innovation", "commercial", "geschäftsentwicklung", "markt", "strategie"
        ],
        "Digital Channel & Customer Relationship Management": [
            "digital channel", "customer relationship", "crm", "digital marketing",
            "omnichannel", "customer experience", "kundenbeziehung", "digitaler kanal"
        ],
        "Start-up & Scale-up Entrepreneurship": [
            "startup", "start-up", "scale-up", "entrepreneurship", "venture",
            "gründung", "scaling", "unternehmensgründung"
        ],
        "Supply Chain & Operation Management": [
            "supply chain", "operation", "logistics", "procurement", "manufacturing",
            "supply chain management", "lieferkettenmanagement", "beschaffung"
        ],
        "Technology Solution Architect": [
            "technology", "solution architect", "architecture", "infrastructure",
            "digital transformation", "it", "technologie", "lösungsarchitektur"
        ],
        "Transforming and Managing Digital Business": [
            "digital business", "digital transformation", "change management",
            "agile", "transformation", "digitale transformation", "change"
        ]
    }
    
    # Zähle Matches für jedes Profil
    profile_scores = {}
    for profile, keywords in profile_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            profile_scores[profile] = score
    
    # Gebe Profil mit höchstem Score zurück
    if profile_scores:
        best_profile = max(profile_scores, key=profile_scores.get)
        return best_profile
    
    return "Not Classified"

# ─────────────────────────────────────────────────────────────────────────────
# HAUPTFUNKTION - KOMPLETTE PARSE-LOGIK
# ─────────────────────────────────────────────────────────────────────────────

def parse_content(pdf_path: Path) -> Optional[Dict]:
    """
    Parst ein PDF vollständig und extrahiert alle strukturierten Felder.
    
    Args:
        pdf_path: Pfad zur PDF-Datei
        
    Returns:
        Dictionary mit allen Feldern oder None bei Fehler
    """
    try:
        logger.info(f"📄 Verarbeite: {pdf_path.name}")
        
        # --- SCHRITT 1: Texte extrahieren ---
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text or len(raw_text.strip()) < 100:
            logger.warning(f"⚠️  {pdf_path.name}: Zu wenig Text extrahiert")
            return None
        
        # --- SCHRITT 2: Sprache erkennen ---
        language = detect_language(raw_text)
        logger.debug(f"   → Sprache: {language.upper()}")
        
        # --- SCHRITT 3: Metadaten extrahieren ---
        course_id = extract_course_id_from_filename(pdf_path.name)
        course_title = extract_course_title(raw_text)
        ects = extract_ects(raw_text)
        
        # --- SCHRITT 4: Sektionen extrahieren ---
        keywords_de = SECTION_KEYWORDS_DE if language == 'de' else SECTION_KEYWORDS_EN
        keywords_en = SECTION_KEYWORDS_EN if language == 'de' else SECTION_KEYWORDS_DE
        
        learning_objectives = extract_field_by_keywords(
            raw_text,
            keywords_de['learning_objectives'] + keywords_en['learning_objectives']
        )
        
        course_content = extract_field_by_keywords(
            raw_text,
            keywords_de['course_content'] + keywords_en['course_content']
        )
        
        # --- SCHRITT 5: MBI-Profil identifizieren ---
        mbi_profile = identify_mbi_profile(raw_text)
        
        # --- SCHRITT 6: Validierung ---
        if not course_title:
            logger.warning(f"⚠️  {pdf_path.name}: Keine Kursnummer gefunden")
        if not ects:
            ects = 0
        
        result = {
            'pdf_file': pdf_path.name,
            'course_id': course_id,
            'course_title': course_title or "N/A",
            'ects': ects,
            'language': language.upper(),
            'mbi_profile': mbi_profile,
            'learning_objectives_raw': learning_objectives,
            'course_content_raw': course_content,
        }
        
        logger.info(f"   ✓ {course_id} | {course_title} | {ects} ECTS | {mbi_profile}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Fehler bei {pdf_path.name}: {str(e)}")
        logger.debug(traceback.format_exc())
        return None

# ─────────────────────────────────────────────────────────────────────────────
# HAUPTFUNKTION - CSV-EXPORT
# ─────────────────────────────────────────────────────────────────────────────

def save_to_csv(data: List[Dict], output_path: str) -> bool:
    """
    Speichert die extrahierten Daten in UTF-8 codierter CSV-Datei.
    
    Args:
        data: Liste von Dictionaries mit Kursinformationen
        output_path: Pfad zur Output-CSV-Datei
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        df = pd.DataFrame(data)
        
        # Ordne Spalten logisch
        column_order = [
            'pdf_file', 'course_id', 'course_title', 'ects', 'language',
            'mbi_profile', 'learning_objectives_raw', 'course_content_raw'
        ]
        df = df[column_order]
        
        # Speichere mit UTF-8 Encoding
        df.to_csv(output_path, index=False, encoding='utf-8-sig', quoting=1)
        
        logger.info(f"✅ CSV erfolgreich gespeichert: {output_path}")
        logger.info(f"   → {len(df)} Kurse exportiert")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Fehler beim CSV-Export: {str(e)}")
        logger.debug(traceback.format_exc())
        return False

# ─────────────────────────────────────────────────────────────────────────────
# HAUPTFUNKTION - ORCHESTRATION
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """
    Hauptfunktion: 
      1. Durchsucht alle PDF-Verzeichnisse
      2. Parsed jedes PDF
      3. Speichert Ergebnisse in CSV
    """
    logger.info("=" * 80)
    logger.info("🚀 MBI CURRICULUM DATABASE EXTRACTOR - START")
    logger.info("=" * 80)
    
    all_data = []
    pdf_count = 0
    error_count = 0
    
    # Durchsuche alle definierten Verzeichnisse
    for pdf_dir in PDF_DIRECTORIES:
        if not pdf_dir.exists():
            logger.warning(f"⚠️  Verzeichnis nicht gefunden: {pdf_dir}")
            continue
        
        logger.info(f"\n📂 Verarbeite Verzeichnis: {pdf_dir}")
        
        pdf_files = sorted(pdf_dir.glob("*.pdf"))
        logger.info(f"   → {len(pdf_files)} PDFs gefunden")
        
        for pdf_path in pdf_files:
            pdf_count += 1
            result = parse_content(pdf_path)
            
            if result:
                all_data.append(result)
            else:
                error_count += 1
    
    # --- SCHRITT 7: CSV speichern ---
    logger.info("\n" + "=" * 80)
    logger.info("💾 EXPORTIERE ERGEBNISSE zu CSV...")
    logger.info("=" * 80)
    
    if all_data:
        save_to_csv(all_data, OUTPUT_CSV)
    else:
        logger.error("❌ Keine Daten zum Exportieren gefunden!")
    
    # --- ZUSAMMENFASSUNG ---
    logger.info("\n" + "=" * 80)
    logger.info("📊 ZUSAMMENFASSUNG")
    logger.info("=" * 80)
    logger.info(f"✓ Gesamt PDFs verarbeitet: {pdf_count}")
    logger.info(f"✓ Erfolgreich extrahiert: {len(all_data)}")
    logger.info(f"❌ Fehler: {error_count}")
    logger.info(f"✅ Output-Datei: {OUTPUT_CSV}")
    logger.info("=" * 80)

if __name__ == "__main__":
    main()
