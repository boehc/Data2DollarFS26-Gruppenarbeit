"""Show complete extracted sections v5"""

import fitz
from pathlib import Path
import re

pdf_path = Path("FS26_mbi_ohne_wahlbereich/8,000,1.00.pdf")
doc = fitz.open(pdf_path)
raw_text = ""
for page in doc:
    raw_text += page.get_text()

def extract_objectives_direct(text):
    text_lower = text.lower()
    start_idx = -1
    for kw in ['lernziele', 'learning objectives']:
        idx = text_lower.find(kw)
        if idx != -1:
            start_idx = idx
            break
    if start_idx == -1:
        return ""
    start_idx = text_lower.find('\n', start_idx) + 1
    end_idx = len(text)
    for kw in ['inhalt', 'content']:
        idx = text_lower.find(kw, start_idx)
        if idx != -1:
            nl_idx = text_lower.rfind('\n', start_idx, idx)
            if nl_idx != -1:
                end_idx = nl_idx
            break
    content = text[start_idx:end_idx].strip()
    content = re.sub(r'[\n\r]+', ' ', content)
    content = re.sub(r' +', ' ', content)
    content = content.replace('³', 'ü').replace('õ', 'ö').replace('á', 'ä')
    content = re.sub(r'^[\s·\-\*À]+', '', content)
    content = re.sub(r'[\s·\-\*À]+$', '', content)
    return content

def extract_content_direct(text):
    text_lower = text.lower()
    start_idx = -1
    for kw in ['inhalt', 'content']:
        idx = text_lower.find(kw)
        if idx != -1:
            start_idx = idx
            break
    if start_idx == -1:
        return ""
    start_idx = text_lower.find('\n', start_idx) + 1
    end_idx = len(text)
    for kw in ['lehrform', 'teaching method', 'lehrmethode', 'prüfung', 'assessment', 'leistungsnachweis']:
        idx = text_lower.find(kw, start_idx)
        if idx != -1:
            nl_idx = text_lower.rfind('\n', start_idx, idx)
            if nl_idx != -1:
                end_idx = nl_idx
            break
    content = text[start_idx:end_idx].strip()
    content = re.sub(r'[\n\r]+', ' ', content)
    content = re.sub(r' +', ' ', content)
    content = content.replace('³', 'ü').replace('õ', 'ö').replace('á', 'ä')
    content = re.sub(r'^[\s·\-\*À]+', '', content)
    content = re.sub(r'[\s·\-\*À]+$', '', content)
    return content

obj = extract_objectives_direct(raw_text)
cont = extract_content_direct(raw_text)

print("="*80)
print(f"LEARNING OBJECTIVES ({len(obj)} chars)")
print("="*80)
print(obj)
print(f"\n{'='*80}")
print(f"COURSE CONTENT ({len(cont)} chars)")
print("="*80)
print(cont)
