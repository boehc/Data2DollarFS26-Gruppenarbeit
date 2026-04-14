"""Debug - examine PDF section locations"""
import fitz
from pathlib import Path

pdf_path = Path("FS26_mbi_ohne_wahlbereich/8,000,1.00.pdf")
doc = fitz.open(pdf_path)

text = ""
for page in doc:
    text += page.get_text()

print("=" * 80)
print("SECTION LOCATIONS IN PDF")
print("=" * 80)

keywords = ['lernziele', 'inhalt', 'prüfung', 'literatur']

for kw in keywords:
    idx = text.lower().find(kw)
    if idx != -1:
        start = max(0, idx - 50)
        end = min(len(text), idx + 300)
        
        print(f"\n[{kw}] at position {idx}:")
        print(f"   Context: ...{text[start:end]}...")
    else:
        print(f"\n[NOT FOUND] '{kw}'")

print("\n" + "=" * 80)
print("FIRST 2500 CHARS:")
print("=" * 80)
print(repr(text[:2500]))
