"""
Startupticker.ch News Scraper V7 - STEP 2 (Interactive Copilot Processing)

This script helps you process articles interactively with GitHub Copilot.
It loads the JSON, displays articles one by one, and you can ask Copilot
to extract the data in our chat.

INPUT:  data/startupticker_articles_for_llm.json
OUTPUT: data/startupticker_startups_v7_step2_manual.csv

WORKFLOW:
1. Run this script to see articles one by one
2. Copy the article text and ask me (Copilot) to extract the data
3. I'll return the structured JSON
4. You paste it back and the script saves it
"""

import json
import pandas as pd
from pathlib import Path

# Files
INPUT_FILE = './data/startupticker_articles_for_llm.json'
OUTPUT_FILE = './data/startupticker_startups_v7_step2_manual.csv'

# How many articles to process
START_INDEX = 0  # Change this to resume from a specific article
BATCH_SIZE = 10  # Process 10 articles at a time

def load_articles():
    """Load the JSON file."""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    return articles

def display_article_for_extraction(article):
    """Format article for easy extraction."""
    print("\n" + "="*80)
    print(f"ARTICLE #{article['id']}")
    print("="*80)
    print(f"URL:   {article['url']}")
    print(f"TITLE: {article['title']}")
    print(f"DATE:  {article['publication_date']}")
    print(f"YEAR:  {article['year']}")
    print("-"*80)
    print("TEXT:")
    print(article['article_text'])
    print("="*80)
    print("\n📋 COPY THIS AND ASK COPILOT:")
    print(f"Extract structured data from article #{article['id']}")
    print("\nOr copy this prompt:")
    print("-"*80)
    extraction_prompt = f"""
Extract startup data from this article using the V3 extraction rules:

ARTICLE:
{article['article_text']}

DATE: {article['publication_date']}
YEAR: {article['year']}

Return ONLY a JSON object with these fields:
- startup_name
- funding_amount
- funding_round_raw
- funding_round
- investor_names
- city
- canton
- founded_year
- employees
- website
- industry
- sub_industry
- business_model_type
- primary_keywords
- secondary_keywords

Use null for unknown fields. Filter out if this is a VC fund close or ecosystem roundup (not a startup event).
"""
    print(extraction_prompt)
    print("-"*80)

def main():
    """Display articles for manual processing."""
    print("="*80)
    print("INTERACTIVE ARTICLE PROCESSOR FOR COPILOT")
    print("="*80)
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Batch:  Articles {START_INDEX+1} to {START_INDEX+BATCH_SIZE}")
    print("="*80)
    
    # Load articles
    articles = load_articles()
    print(f"\n✓ Loaded {len(articles)} articles\n")
    
    # Display batch
    end_index = min(START_INDEX + BATCH_SIZE, len(articles))
    
    for i in range(START_INDEX, end_index):
        article = articles[i]
        display_article_for_extraction(article)
        
        input(f"\n⏸️  Press ENTER to see next article (or Ctrl+C to stop)...")
    
    print("\n" + "="*80)
    print(f"✅ Displayed {end_index - START_INDEX} articles")
    print("="*80)
    print("\nNEXT STEPS:")
    print("1. For each article, ask me (Copilot) to extract the data")
    print("2. I'll return structured JSON")
    print("3. Save the results to a CSV manually or collect them")
    print(f"4. To continue with next batch, change START_INDEX to {end_index}")
    print("="*80)

if __name__ == "__main__":
    main()
