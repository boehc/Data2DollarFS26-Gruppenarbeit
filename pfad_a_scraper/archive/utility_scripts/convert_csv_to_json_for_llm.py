"""
Convert Step 1 CSV to JSON format for LLM batch processing

This script takes the raw articles CSV from Step 1 and converts it to:
1. A JSONL file (one JSON object per line) - for batch API processing
2. Individual JSON files (optional) - for manual review
3. A single JSON array - for testing/debugging

INPUT:  data/startupticker_raw_articles_v7_step1_FINANCING.csv
OUTPUT: data/startupticker_articles_for_llm.jsonl (primary)
        data/startupticker_articles_for_llm.json (full array)
"""

import pandas as pd
import json
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_FILE = './data/startupticker_raw_articles_v7_step1_FINANCING.csv'
OUTPUT_JSONL = './data/startupticker_articles_for_llm.jsonl'
OUTPUT_JSON = './data/startupticker_articles_for_llm.json'

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    print("="*70)
    print("CSV TO JSON CONVERTER - STEP 1 OUTPUT")
    print("="*70)
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_JSONL} (JSONL format)")
    print(f"        {OUTPUT_JSON} (JSON array)")
    print("="*70)
    print()
    
    # Load CSV
    print("Loading CSV...")
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"✓ Loaded {len(df)} articles")
        print(f"  Columns: {', '.join(df.columns)}")
        print()
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Convert to JSON structures
    print("Converting to JSON format...")
    articles_list = []
    
    for i, row in df.iterrows():
        article_obj = {
            "id": i + 1,
            "url": row.get('URL', None),
            "title": row.get('Title', None),
            "publication_date": row.get('Publication_Date', None),
            "year": int(row['Year']) if pd.notna(row.get('Year')) else None,
            "article_text": row.get('Article_Text', None)
        }
        articles_list.append(article_obj)
    
    print(f"✓ Converted {len(articles_list)} articles to JSON objects")
    print()
    
    # Save as JSONL (one JSON per line - for batch processing)
    print("Saving JSONL format...")
    try:
        with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
            for article in articles_list:
                f.write(json.dumps(article, ensure_ascii=False) + '\n')
        print(f"✓ Saved: {OUTPUT_JSONL}")
        print(f"  Format: One JSON object per line (JSONL)")
        print(f"  Lines: {len(articles_list)}")
    except Exception as e:
        print(f"❌ Error saving JSONL: {e}")
    
    print()
    
    # Save as single JSON array (for testing/debugging)
    print("Saving JSON array format...")
    try:
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(articles_list, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved: {OUTPUT_JSON}")
        print(f"  Format: Single JSON array")
        print(f"  Items: {len(articles_list)}")
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
    
    # Show sample
    print()
    print("="*70)
    print("SAMPLE JSON OBJECT (first article):")
    print("="*70)
    if articles_list:
        sample = articles_list[0].copy()
        # Truncate text for display
        if sample.get('article_text'):
            sample['article_text'] = sample['article_text'][:200] + "..."
        print(json.dumps(sample, indent=2, ensure_ascii=False))
    
    print()
    print("="*70)
    print("✅ CONVERSION COMPLETE")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Use the JSONL file for batch LLM processing")
    print("2. Or process the JSON array programmatically")
    print("3. Each object contains all data needed for extraction")
    print()


if __name__ == "__main__":
    main()
