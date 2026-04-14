"""Extract course assignments from MBI-Profilbroschuere PDF"""

import fitz  # PyMuPDF
from pathlib import Path

pdf_path = Path("MBI-Profilbroschuere_Januar_2025.pdf")

if pdf_path.exists():
    doc = fitz.open(pdf_path)
    
    print("\n" + "="*80)
    print("ANALYZING MBI-PROFILBROSCHUERE_JANUAR_2025.PDF")
    print("="*80 + "\n")
    
    print(f"Total Pages: {doc.page_count}\n")
    
    # Extract text from first 10 pages to understand structure
    for page_num in range(min(10, doc.page_count)):
        page = doc[page_num]
        text = page.get_text()
        
        print(f"\n{'='*80}")
        print(f"PAGE {page_num + 1}")
        print(f"{'='*80}\n")
        print(text[:2000])
        print(f"\n... [page has {len(text)} total chars] ...")
        
else:
    print("File not found!")
