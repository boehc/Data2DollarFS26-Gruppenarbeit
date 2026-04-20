"""
Helper script to split articles into batches for Claude processing.
Creates separate JSON files with 10 articles each, ready to copy-paste.
"""

import json
import os

INPUT_FILE = 'data/startupticker_articles_for_llm.json'
OUTPUT_DIR = 'data/claude_batches'
BATCH_SIZE = 10

def create_batches():
    """Split articles into batches and save as JSON files."""
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load articles
    print(f"📥 Loading articles from: {INPUT_FILE}")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    total = len(articles)
    num_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"📊 Total articles: {total}")
    print(f"📦 Creating {num_batches} batches of {BATCH_SIZE} articles each")
    print()
    
    # Create batches
    for i in range(0, total, BATCH_SIZE):
        batch_num = i // BATCH_SIZE + 1
        batch = articles[i:i + BATCH_SIZE]
        
        # Create batch file
        batch_file = f"{OUTPUT_DIR}/batch_{batch_num}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Batch {batch_num:2d}: {len(batch)} articles → {batch_file}")
    
    # Create instructions file
    instructions_file = f"{OUTPUT_DIR}/INSTRUCTIONS.txt"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("CLAUDE BATCH PROCESSING INSTRUCTIONS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total: {total} articles split into {num_batches} batches\n\n")
        f.write("WORKFLOW:\n")
        f.write("1. Copy prompt from: CLAUDE_EXTRACTION_PROMPT.md\n")
        f.write("2. Open batch_1.json and copy contents\n")
        f.write("3. Paste prompt + articles to Claude\n")
        f.write("4. Copy Claude's JSON response\n")
        f.write("5. Save as: results/result_1.json\n")
        f.write("6. Repeat for batch_2.json → result_2.json\n")
        f.write(f"7. After all {num_batches} batches, run: python3 10_merge_claude_batches.py\n\n")
        f.write("BATCH FILES:\n")
        for i in range(1, num_batches + 1):
            f.write(f"  - batch_{i}.json → process → save as result_{i}.json\n")
    
    print()
    print(f"📝 Instructions saved to: {instructions_file}")
    print()
    print("="*80)
    print("✅ BATCHES CREATED!")
    print("="*80)
    print()
    print("NEXT STEPS:")
    print(f"1. Go to: {OUTPUT_DIR}/")
    print("2. Read INSTRUCTIONS.txt")
    print("3. Process each batch_X.json with Claude")
    print("4. Save responses as result_X.json in 'results' folder")
    print()

if __name__ == '__main__':
    create_batches()
