"""
Startupticker.ch News Scraper V7 - STEP 2 (Batch Processing with Copilot)

This script creates batches of articles that you can send to me (Copilot) in chat.
I'll process them and return JSON, which you can save directly.

INPUT:  data/startupticker_articles_for_llm.json
OUTPUT: data/startupticker_startups_v7_step2.csv

WORKFLOW:
1. Run script to generate a batch file with 10-50 articles
2. Ask me: "Process this batch and extract startup data"
3. I'll return a JSON array with all extracted data
4. Save the output and repeat for next batch
"""

import json
import pandas as pd
from pathlib import Path

# Configuration
INPUT_FILE = './data/startupticker_articles_for_llm.json'
OUTPUT_FILE = './data/startupticker_startups_v7_step2.csv'
BATCH_FILE = './data/current_batch.json'

# Batch settings
BATCH_SIZE = 20  # Process 20 articles at a time (manageable for Copilot)
START_INDEX = 0   # Change this to process different batches

# V3 Extraction Instructions (simplified for Copilot)
EXTRACTION_INSTRUCTIONS = """
EXTRACTION RULES (V3):

For each article, extract these fields (use null if not found):

1. startup_name - The company name (look near bottom of article before date)
   - FILTER: Return null if this is a VC fund close, ecosystem roundup, or no single company subject
   
2. funding_amount - Normalize to "XM CURRENCY" format
   Examples: "EUR 4.4 million" → "4.4M EUR", "siebenstellig" → "undisclosed"
   
3. funding_round_raw - Exact phrase from article (e.g., "seed round", "Seed-Runde")

4. funding_round - Map to standard labels:
   Pre-Seed | Seed | Seed Extension | Series A | Series B | Series C | Series D+ |
   Strategic Investment | Acquisition | Grant | Award | Debt | Undisclosed
   
5. investor_names - Comma-separated list of investors in THIS round
   
6. city - Zurich, Geneva, Lausanne, Basel, Bern, Lucerne, Zug, St. Gallen, Lugano, 
   Winterthur, Rapperswil, Carouge, Biel (standard English spelling)
   
7. canton - 2-letter code (ZH, GE, VD, BS, BE, ZG, TI, SG, LU, etc.)

8. founded_year - 4-digit integer

9. employees - Integer headcount

10. website - Company's own domain (.ch, .com, .io, etc.)

11. industry - ONE of: AI/ML | HealthTech | BioTech | MedTech | FinTech | CleanTech |
    DeepTech | Robotics | Cybersecurity | PropTech | FoodTech | AgriTech | EdTech |
    HRTech | Logistics | Industry 4.0 | Enterprise SaaS | B2C Tech | Other
    
12. sub_industry - Up to 3 segments, comma-separated

13. business_model_type - ONE of: B2B-SaaS | B2B-Hardware | B2B-Services | B2B2C |
    B2C | Marketplace | Deep Tech / IP | Unknown
    
14. primary_keywords - 2-4 canonical keywords (company's core tech)

15. secondary_keywords - 1-3 canonical keywords (adjacent tech)

CANONICAL KEYWORDS:
Generative AI, Large Language Models (LLM), Computer Vision, Natural Language Processing (NLP),
Predictive Analytics, Machine Learning, AI Agents, Reinforcement Learning, 
Simulation & Synthetic Data, EEG / Brain Signal Processing, Digital Therapeutics,
Remote Patient Monitoring, Drug Discovery, mRNA / Gene Therapy, Immunology, Diagnostics,
CRISPR / Gene Editing, Wearable Sensors, Federated Learning, Cybersecurity / Zero Trust,
Post-Quantum Cryptography, Blockchain / DLT, Smart Contracts, Solar / Photovoltaics,
Battery Storage, Carbon Capture, Energy Grid Management, Robotics / Autonomous Systems,
Digital Twin, Computer-Aided Manufacturing, Semiconductor Design, High-Speed Connectivity,
Edge Computing, IoT Sensors, SaaS / Cloud Platform, API Integration, Workflow Automation,
Marketplace / Platform, B2B Data Network, Satellite / Space Tech, Quantum Computing,
Synthetic Biology, Fermentation Technology, Precision Fermentation

MULTILINGUAL PATTERNS:
- English: "Zurich-based", "founded in 2021", "raised EUR 4.4 million"
- German: "Das Zürcher Startup", "gegründet 2021", "4,4 Millionen Euro"
- French: "basée à Genève", "fondée en 2021", "levée de fonds"
"""


def load_articles():
    """Load JSON articles."""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_batch(articles, start, size):
    """Create a batch of articles for processing."""
    end = min(start + size, len(articles))
    batch = articles[start:end]
    
    # Simplify for processing (keep only essential fields)
    simplified_batch = []
    for article in batch:
        simplified_batch.append({
            'id': article['id'],
            'url': article['url'],
            'title': article['title'],
            'publication_date': article['publication_date'],
            'year': article['year'],
            'article_text': article['article_text']
        })
    
    return simplified_batch, end


def save_batch(batch, filename):
    """Save batch to file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)


def main():
    """Create batch for Copilot processing."""
    print("="*80)
    print("BATCH CREATOR FOR COPILOT PROCESSING")
    print("="*80)
    print(f"Input:  {INPUT_FILE}")
    print(f"Batch:  {BATCH_SIZE} articles starting from #{START_INDEX + 1}")
    print(f"Output: {BATCH_FILE}")
    print("="*80)
    print()
    
    # Load articles
    articles = load_articles()
    print(f"✓ Loaded {len(articles)} total articles")
    
    # Create batch
    batch, next_index = create_batch(articles, START_INDEX, BATCH_SIZE)
    print(f"✓ Created batch: Articles {START_INDEX + 1} to {next_index}")
    
    # Save batch
    save_batch(batch, BATCH_FILE)
    print(f"✓ Saved to: {BATCH_FILE}")
    print()
    
    # Display sample
    print("="*80)
    print("SAMPLE FROM BATCH (Article #1):")
    print("="*80)
    if batch:
        first = batch[0]
        print(f"ID:    {first['id']}")
        print(f"Title: {first['title']}")
        print(f"Date:  {first['publication_date']}")
        print(f"Text:  {first['article_text'][:200]}...")
    
    print()
    print("="*80)
    print("NEXT STEPS:")
    print("="*80)
    print()
    print(f"1. Open {BATCH_FILE} in VS Code")
    print()
    print("2. Copy the entire JSON array and paste it in chat with this prompt:")
    print()
    print("-"*80)
    print("PROMPT TO USE:")
    print("-"*80)
    print()
    print(f"Process this batch of {len(batch)} articles and extract structured startup data.")
    print()
    print("For each article, extract: startup_name, funding_amount, funding_round,")
    print("investor_names, city, canton, founded_year, employees, website, industry,")
    print("sub_industry, business_model_type, primary_keywords, secondary_keywords.")
    print()
    print("Use the V3 extraction rules:")
    print("- Filter out VC fund closes and ecosystem roundups (return null for startup_name)")
    print("- Normalize funding to 'XM CURRENCY' format")
    print("- Map funding_round to standard labels (Seed, Series A, etc.)")
    print("- Extract city in English (Zurich, Geneva, etc.) and canton code (ZH, GE, etc.)")
    print("- Classify industry and select keywords from canonical list")
    print()
    print("Return a JSON array with one object per article, maintaining the same ID.")
    print("Include publication_date and year from the input.")
    print("Add Article_URL, Article_Title, Article_Text to each output object.")
    print()
    print("-"*80)
    print()
    print(f"3. Save my response to: data/batch_{START_INDEX//BATCH_SIZE + 1}_results.json")
    print()
    print(f"4. To process next batch, change START_INDEX to {next_index} and run again")
    print()
    print(f"5. After all batches, merge the results into {OUTPUT_FILE}")
    print()
    print("="*80)
    
    # Show progress
    total_batches = (len(articles) + BATCH_SIZE - 1) // BATCH_SIZE
    current_batch = START_INDEX // BATCH_SIZE + 1
    print()
    print(f"📊 Progress: Batch {current_batch} of {total_batches}")
    print(f"   Remaining: {len(articles) - next_index} articles")
    print()


if __name__ == "__main__":
    main()
