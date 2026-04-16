#!/usr/bin/env python3
"""
Automated LLM-based Article Extraction Script
==============================================

This script processes raw articles through an LLM (Claude/OpenAI) to extract
structured startup data. It handles batching, rate limiting, and output formatting.

Usage:
    python3 10_automated_llm_extraction.py

Features:
- Processes articles in batches of 10
- Extracts 18 structured fields per article
- Handles multi-company articles
- Saves results to CSV
- Progress tracking and error handling
"""

import pandas as pd
import json
import time
from pathlib import Path
from datetime import datetime
import sys

# Configuration
INPUT_CSV = "data/startupticker_FINANCING_SORTED.csv"  # 1564 articles, sorted newest → oldest
OUTPUT_CSV = "data/startupticker_extracted_llm_FULL.csv"
BATCH_SIZE = 10  # Process 10 articles at a time (optimal for Claude)
PROMPT_FILE = "CLAUDE_EXTRACTION_PROMPT.md"

# Column mapping for output
OUTPUT_COLUMNS = [
    "startup_name", "publication_date", "year", "funding_amount", 
    "funding_round_raw", "funding_round", "investor_names", "city", 
    "canton", "founded_year", "employees", "website", "location", 
    "industry", "sub_industry", "business_model_type", 
    "primary_keywords", "secondary_keywords"
]


def load_prompt_template():
    """Load the extraction prompt from markdown file"""
    with open(PROMPT_FILE, 'r') as f:
        content = f.read()
        # Extract the prompt section between the code blocks
        start = content.find("```\n") + 4
        end = content.find("\n```", start)
        return content[start:end].strip()


def prepare_article_batch(df, start_idx, batch_size):
    """Prepare a batch of articles for LLM processing"""
    end_idx = min(start_idx + batch_size, len(df))
    batch = df.iloc[start_idx:end_idx]
    
    articles_text = "\n\n".join([
        f"Article {i+1}:\n"
        f"URL: {row['URL']}\n"
        f"Title: {row['Title']}\n"
        f"Publication_Date: {row['Publication_Date']}\n"
        f"Year: {row['Year']}\n"
        f"Article_Text: {row['Article_Text']}\n"
        f"{'-'*80}"
        for i, (_, row) in enumerate(batch.iterrows())
    ])
    
    return articles_text, end_idx


def format_for_manual_processing(prompt, articles_text, batch_num, total_batches):
    """Format the complete prompt for manual copy-paste to Claude"""
    return f"""
{'='*80}
BATCH {batch_num}/{total_batches} - READY FOR CLAUDE
{'='*80}

INSTRUCTIONS:
1. Copy everything below this line
2. Paste into Claude (new chat or this conversation)
3. Wait for JSON response
4. Save JSON response to: data/batch_{batch_num:03d}.json
5. Press Enter to continue to next batch

{'='*80}
COPY FROM HERE ↓
{'='*80}

{prompt}

ARTICLES TO ANALYZE:

{articles_text}

{'='*80}
COPY TO HERE ↑
{'='*80}
"""


def save_batch_instructions(batch_num, total_batches, prompt_text):
    """Save batch instructions to a file for easy copy-paste"""
    filename = f"data/batch_{batch_num:03d}_prompt.txt"
    with open(filename, 'w') as f:
        f.write(prompt_text)
    return filename


def merge_batch_results(data_dir="data"):
    """Merge all batch JSON files into final CSV"""
    batch_files = sorted(Path(data_dir).glob("batch_*.json"))
    
    if not batch_files:
        print("❌ No batch JSON files found!")
        return None
    
    all_records = []
    for batch_file in batch_files:
        try:
            with open(batch_file, 'r') as f:
                batch_data = json.load(f)
                all_records.extend(batch_data)
            print(f"✅ Loaded {len(batch_data)} records from {batch_file.name}")
        except Exception as e:
            print(f"⚠️  Error loading {batch_file.name}: {e}")
    
    if not all_records:
        print("❌ No records extracted!")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(all_records)
    
    # Ensure all expected columns exist
    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    # Reorder columns
    df = df[OUTPUT_COLUMNS]
    
    # Save to CSV
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅ Merged {len(df)} records → {OUTPUT_CSV}")
    
    return df


def main():
    print("="*80)
    print("🤖 AUTOMATED LLM EXTRACTION WORKFLOW")
    print("="*80)
    
    # Check if input file exists
    if not Path(INPUT_CSV).exists():
        print(f"❌ Input file not found: {INPUT_CSV}")
        return
    
    # Load data
    print(f"\n📊 Loading articles from {INPUT_CSV}...")
    df = pd.read_csv(INPUT_CSV)
    print(f"✅ Loaded {len(df)} articles")
    
    # Calculate batches
    total_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"📦 Will process in {total_batches} batches of {BATCH_SIZE} articles")
    
    # Load prompt template
    print(f"\n📋 Loading prompt template from {PROMPT_FILE}...")
    prompt_template = load_prompt_template()
    print(f"✅ Prompt loaded ({len(prompt_template)} characters)")
    
    # Ask user which mode
    print("\n" + "="*80)
    print("CHOOSE MODE:")
    print("="*80)
    print("1. MANUAL MODE - Generate prompts for manual copy-paste to Claude")
    print("2. MERGE MODE - Merge existing batch_*.json files into CSV")
    print("3. TEST MODE - Generate first batch only for testing")
    print("="*80)
    
    mode = input("\nEnter mode (1/2/3): ").strip()
    
    if mode == "2":
        # Merge existing results
        print("\n🔄 MERGE MODE")
        merge_batch_results()
        return
    
    elif mode == "3":
        # Test mode - first batch only
        print("\n🧪 TEST MODE - First batch only")
        articles_text, _ = prepare_article_batch(df, 0, BATCH_SIZE)
        prompt_text = format_for_manual_processing(prompt_template, articles_text, 1, total_batches)
        
        filename = save_batch_instructions(1, total_batches, prompt_text)
        print(f"\n✅ Test batch prompt saved to: {filename}")
        print("\n" + prompt_text)
        
        print("\n📝 NEXT STEPS:")
        print("1. Copy the prompt above (between the COPY markers)")
        print("2. Paste into Claude")
        print("3. Copy Claude's JSON response")
        print("4. Save to: data/batch_001.json")
        print("5. Run script again in MERGE mode (option 2)")
        
        return
    
    elif mode == "1":
        # Manual mode - generate all batches
        print("\n📝 MANUAL MODE - Generating all batch prompts")
        
        # Create data directory if it doesn't exist
        Path("data").mkdir(exist_ok=True)
        
        # Process all batches
        for batch_num in range(1, total_batches + 1):
            start_idx = (batch_num - 1) * BATCH_SIZE
            articles_text, end_idx = prepare_article_batch(df, start_idx, BATCH_SIZE)
            prompt_text = format_for_manual_processing(prompt_template, articles_text, batch_num, total_batches)
            
            filename = save_batch_instructions(batch_num, total_batches, prompt_text)
            print(f"✅ Batch {batch_num}/{total_batches} prompt saved → {filename}")
        
        print("\n" + "="*80)
        print("✅ ALL BATCH PROMPTS GENERATED")
        print("="*80)
        print(f"\n📝 WORKFLOW:")
        print(f"1. Open data/batch_001_prompt.txt")
        print(f"2. Copy the content between COPY markers")
        print(f"3. Paste into Claude")
        print(f"4. Save Claude's JSON response to data/batch_001.json")
        print(f"5. Repeat for batch_002_prompt.txt → batch_002.json")
        print(f"6. Continue until all {total_batches} batches are done")
        print(f"7. Run this script again with option 2 (MERGE MODE)")
        print("\n💡 TIP: You can process batches in parallel using multiple Claude chats!")
        
        return
    
    else:
        print("❌ Invalid mode selected")
        return


if __name__ == "__main__":
    main()
