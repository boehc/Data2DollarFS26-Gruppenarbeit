"""Debug - Show FULL section content"""

import fitz
from pathlib import Path
import re

pdf_path = Path("FS26_mbi_ohne_wahlbereich/8,000,1.00.pdf")
doc = fitz.open(pdf_path)
raw_text = ""
for page in doc:
    raw_text += page.get_text()

text_lower = raw_text.lower()

# Learning Objectives
print("="*80)
print("LEARNING OBJECTIVES - FULL CONTENT")
print("="*80)
start = text_lower.find('lernziele')
start = raw_text.find('\n', start) + 1
end = text_lower.find('inhalt', start)
end = text_lower.rfind('\n', start, end)

obj_text = raw_text[start:end]
print(f"CHARACTER COUNT: {len(obj_text)}")
print(f"TEXT:\n{obj_text}")

print("\n" + "="*80)
print("COURSE CONTENT - FULL CONTENT")
print("="*80)
start = text_lower.find('inhalt')
start = raw_text.find('\n', start) + 1
end = text_lower.find('lehr', start)
if end == -1:
    end = text_lower.find('struktur', start)

content_text = raw_text[start:end]
print(f"CHARACTER COUNT: {len(content_text)}")
print(f"TEXT:\n{content_text}")
