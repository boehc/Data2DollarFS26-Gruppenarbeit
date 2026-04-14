"""
PDF ANALYSE & DETAILLIERTE STRUKTUR-UNTERSUCHUNG
Ziel: Verstehe die Layout-Struktur um das Parsing zu verbessern
"""
import pdfplumber
from pathlib import Path

pdf_path = Path("FS26_mbi_ohne_wahlbereich/8,000,1.00.pdf")

print("=" * 80)
print("📄 PDF STRUKTUR-ANALYSE: 8,000,1.00.pdf")
print("=" * 80)

with pdfplumber.open(pdf_path) as pdf:
    print(f"\nSeiten im PDF: {len(pdf.pages)}")
    
    page = pdf.pages[0]
    print(f"Seite 1 Dimensionen: {page.width:.0f} x {page.height:.0f} pt\n")
    
    # ─────────────────────────────────────────────────────────────────
    # 1. RAW TEXT EXTRACTION
    # ─────────────────────────────────────────────────────────────────
    text = page.extract_text()
    print("1️⃣  RAW TEXT (erste 2000 Zeichen):")
    print("─" * 80)
    print(text[:2000])
    print("\n")
    
    # ─────────────────────────────────────────────────────────────────
    # 2. WORD-LEVEL ANALYSE (mit Y-Position)
    # ─────────────────────────────────────────────────────────────────
    words = page.extract_words()
    print(f"2️⃣  WORT-POSITIONEN (erste 20 Wörter):")
    print("─" * 80)
    if words and len(words) > 0:
        # Inspect first word structure
        first_word = words[0]
        print(f"  Wort-Keys: {list(first_word.keys())}")
        print(f"  Erstes Wort: {first_word}")
    else:
        print("  Keine Wörter extrahiert?")
    
    # ─────────────────────────────────────────────────────────────────
    # 3. GRUPPIERUNG nach Y-Achse (horizontale Zeilen)
    # ─────────────────────────────────────────────────────────────────
    print(f"\n3️⃣  GRUPPIERUNG nach Y-ACHSE (horizontale Zeilen):")
    print("─" * 80)
    
    # Gruppiere nur wenn Wörter die top0 enthalten
    if words and 'top' in words[0]:
        lines = {}
        for word in words[:60]:
            y_key = round(word['top'] / 3) * 3  # Adapter für 'top' statt 'y0'
            if y_key not in lines:
                lines[y_key] = []
            lines[y_key].append(word)
        
        for y_pos in sorted(lines.keys())[:15]:
            line_text = " ".join(w['text'] for w in lines[y_pos])
            print(f"Y={y_pos:<6.0f} | {line_text[:75]}")
    
    # ─────────────────────────────────────────────────────────────────
    # 4. TABELLEN-ERKENNUNG
    # ─────────────────────────────────────────────────────────────────
    tables = page.extract_tables()
    print(f"\n4️⃣  TABELLEN GEFUNDEN: {len(tables)}")
    if tables:
        for i, table in enumerate(tables[:2]):  # Zeige erste 2 Tabellen
            print(f"\n  Tabelle {i+1}: {len(table)} Zeilen x {len(table[0]) if table else 0} Spalten")
            print(f"  Header: {table[0] if table else 'N/A'}")
    
    # ─────────────────────────────────────────────────────────────────
    # 5. SUCHBEREICH FÜR METADATA
    # ─────────────────────────────────────────────────────────────────
    print(f"\n5️⃣  SEARCH FOR KEY METADATA:")
    print("─" * 80)
    
    # Suche nach spezifischen Patterns
    text_lower = text.lower()
    
    # Kursnummer
    import re
    course_match = re.search(r'(\d{1,2},\d{3})', text)
    if course_match:
        print(f"  ✓ Kursnummer gefunden: {course_match.group(1)}")
    
    # ECTS
    ects_match = re.search(r'(\d+)\s*(?:ECTS|Credits)', text, re.IGNORECASE)
    if ects_match:
        print(f"  ✓ ECTS gefunden: {ects_match.group(1)}")
    
    # Lernziele
    if 'lernziele' in text_lower:
        idx = text_lower.index('lernziele')
        print(f"  ✓ 'Lernziele' gefunden bei Position {idx}")
        print(f"    Text: {text[idx:idx+200]}")
    
    if 'learning objectives' in text_lower:
        idx = text_lower.index('learning objectives')
        print(f"  ✓ 'Learning Objectives' gefunden bei Position {idx}")
        print(f"    Text: {text[idx:idx+200]}")

print("\n" + "=" * 80)
print("✅ ANALYSE ABGESCHLOSSEN")
print("=" * 80)
