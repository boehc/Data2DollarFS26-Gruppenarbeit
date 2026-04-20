"""
LLM-BASED ARTICLE ANALYZER
Extracts comprehensive startup data from articles using OpenAI GPT-4.

Extracts:
- Startup name, publication date, year
- Funding amount, round type, investors
- Location data (city, canton)
- Company data (founded year, employees, website)
- Classification (industry, sub-industry, business model)
- Keywords (primary & secondary)
"""

import json
import os
import pandas as pd
from datetime import datetime
import time
from openai import OpenAI
import re

# Import enhanced keywords
from enhanced_keywords_v6 import get_enhanced_tech_keywords


# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_FILE = 'data/startupticker_articles_for_llm.json'
OUTPUT_FILE = 'data/startupticker_analyzed_v8.csv'
LOG_FILE = 'llm_analyzer_v8.log'
CHECKPOINT_FILE = 'data/llm_analyzer_checkpoint_v8.json'

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL = 'gpt-4o'  # or 'gpt-4-turbo' or 'gpt-3.5-turbo' for faster/cheaper
TEMPERATURE = 0.1  # Low temperature for consistent extraction
MAX_TOKENS = 2000

# Processing Configuration
BATCH_SIZE = 10  # Save checkpoint every N articles
RATE_LIMIT_DELAY = 1.0  # Seconds between API calls
MAX_RETRIES = 3


# ============================================================================
# CANONICAL KEYWORD LIST
# ============================================================================

def get_canonical_keyword_list():
    """
    Returns formatted canonical keyword list for LLM prompt.
    """
    keywords_dict = get_enhanced_tech_keywords()
    
    # Flatten and deduplicate
    all_keywords = []
    for category, patterns in keywords_dict.items():
        all_keywords.append(category)
    
    # Sort and format
    all_keywords = sorted(set(all_keywords))
    return ', '.join(all_keywords)


# ============================================================================
# LLM PROMPT TEMPLATE
# ============================================================================

def build_extraction_prompt(article_text, publication_date, year):
    """
    Builds the LLM prompt for data extraction.
    """
    canonical_keywords = get_canonical_keyword_list()
    
    prompt = f"""You are a precise data extraction assistant. Analyze this Swiss startup article and extract structured data.

ARTICLE TEXT:
\"\"\"
{article_text}
\"\"\"

PUBLICATION DATE (extracted in Step 1): {publication_date}
YEAR (extracted in Step 1): {year}

---

FIELD INSTRUCTIONS:

"startup_name"
  The full legal name of the primary company this article is about —
  the one that raised money, launched a product, or won an award.
  The most reliable source is the company name tagged near the bottom of the
  article, right before the date stamp. It appears as "Company AG", "Company SA",
  "Company GmbH", "Company Sàrl" or similar legal form.
  Rules:
  - Never return an investor name, event name, or headline fragment.
  - Never return single generic words: "Labs", "Space", "Five", "Seed", "CHF",
    "New", "Continuing", "Zürichbased", "Introducing", "Milestones".
  - If the article covers multiple companies equally (award ceremony, ecosystem
    roundup) and no single primary subject exists, return null.

"publication_date"
  Pass through exactly: {publication_date}

"year"
  Pass through exactly: {year}

"funding_amount"
  The total amount raised in the specific round described in this article.
  
  Normalize to: {{number}}M {{CURRENCY}}
  Examples:
    "EUR 4.4 million"               → "4.4M EUR"
    "USD 225 million"               → "225M USD"
    "$225mm"                        → "225M USD"
    "3,5 Millionen Euro"            → "3.5M EUR"    ← German decimal comma
    "CHF 100,000"                   → "0.1M CHF"
    "siebenstelliger Betrag"        → "undisclosed"  ← German: 7-figure amount
    "zweistelliger Millionenbetrag" → "undisclosed"  ← German: double-digit million
    "montant à sept chiffres"       → "undisclosed"  ← French: 7-figure amount
    "einen hohen einstelligen Millionenbetrag" → "undisclosed" ← high single-digit M
  
  Return "undisclosed" if an amount is referenced but not specified.
  Return null if no funding event is described at all.

"funding_round_raw"
  Copy the exact phrase the article uses to describe the round type.
  Preserve the original language.
  Examples:
    "seed round", "Seed-Runde", "Series B", "Kapitalerhöhung",
    "strategic investment", "Seed-Erweiterungsrunde", "Grant", "Förderung",
    "convertible note", "venture debt", "tour de table Série A"
  Return null if no round type is mentioned at all.

"funding_round"
  Map funding_round_raw to exactly ONE standardized label from this list:
    Pre-Seed
    Seed
    Seed Extension
    Series A
    Series B
    Series C
    Series D+
    Strategic Investment
    Grant
    Award
    Debt
    Undisclosed
  
  Mapping rules:
    "seed round" / "Seed-Runde" / "ronde de financement seed"  → Seed
    "Seed-Erweiterungsrunde" / "seed extension"                → Seed Extension
    "Series A" / "Série A" / "Runde A"                        → Series A
    "Series B" / "Série B"                                    → Series B
    "Series C" / "Série C" / "Runde C"                        → Series C
    "Series D" or later                                       → Series D+
    "strategic investment" / "strategische Beteiligung"
      from a named corporate investor                         → Strategic Investment
    "Kapitalerhöhung" with no round name given                → Undisclosed
    Innosuisse / foundation / EU / government money           → Grant
    Venture Kick / FIT prize / competition prize              → Award
    "convertible note" / "venture debt" / "Darlehen"         → Debt
    Funding confirmed but round type genuinely unclear        → Undisclosed
  
  IMPORTANT: Do not infer or override based on amount size.
  Map only what the article explicitly states or clearly implies by language.
  Return null if no funding event is described.

"investor_names"
  Comma-separated list of all investors who participated in THIS round.
  Include: VC firms, corporate venture arms, family offices, business angels, banks.
  Exclude: advisors, board members (unless explicitly stated they also co-invested),
           investors from previous rounds not re-investing here.
  Return null if no investors are named for this round.

"city"
  City where the startup is headquartered.
  Language patterns to recognize:
    English: "Zurich-based X", "Founded in Lausanne", "headquartered in Basel",
             "X, based in Bern"
    German:  "Das Zürcher Startup", "Die St. Galler X", "das Basler Unternehmen",
             "das Luzerner Startup", "in Zug ansässige", "Die Genfer", "Lausanner"
    French:  "basée à Genève", "startup lausannoise", "société genevoise",
             "implantée à Zurich"
  Return in standard English spelling: Zurich, Geneva, Lausanne, Basel, Bern,
  Lucerne, Zug, St. Gallen, Lugano.
  Return null if city is not mentioned. NEVER default to any city.

"canton"
  2-letter Swiss canton code inferred from city. Return null if city is null.
  
  Zurich / Winterthur / Kloten       → ZH
  Geneva / Carouge / Vernier         → GE
  Lausanne / Renens / Nyon / Morges  → VD
  Basel                              → BS
  Bern / Biel                        → BE
  Zug                                → ZG
  Lugano / Locarno / Bellinzona      → TI
  St. Gallen / Rapperswil            → SG
  Lucerne                            → LU
  Sion / Sierre / Martigny / Visp    → VS
  Fribourg                           → FR
  Aarau / Baden / Brugg              → AG
  Neuchâtel / La Chaux-de-Fonds      → NE
  Schaffhausen                       → SH
  Solothurn / Zuchwil                → SO
  Herisau                            → AR
  Chur                               → GR

"founded_year"
  Year the startup was founded. 4-digit integer.
  Language patterns:
    English: "founded in 2021", "established in 2021", "incorporated in 2021"
    German:  "gegründet 2021", "seit 2021", "das 2021 gestartete Unternehmen",
             "das 2020 gegründete Unternehmen", "wurde 2021 gegründet"
    French:  "fondée en 2021", "créée en 2021"
  Return null if not mentioned.

"employees"
  Current headcount. Integer.
  Language patterns:
    English: "team of 30", "30 employees", "a staff of 30", "employs 30"
    German:  "30 Mitarbeitende", "auf 30 Personen gewachsen", "30-köpfige Team",
             "30 Angestellte"
    French:  "30 employés", "une équipe de 30 personnes"
  Return null if not mentioned.

"website"
  The startup's own domain. Look for URLs ending in .ch, .com, .io, .ai, .co, .eu.
  Must clearly belong to the startup — not startupticker.ch, not investor websites,
  not partner sites.
  Return null if not found.

"location"
  Return "Switzerland" unless the article explicitly states the company is
  headquartered in another country.

"industry"
  Classify based on what the company has BUILT and who uses it — not the article topic.
  
  Follow this decision logic in order:
  
  1. What is the core deliverable?
     Drug / therapy / molecule / biologics → BioTech
     Physical medical device or implant    → MedTech
     Clinical software / AI diagnostics    → HealthTech
     Energy / climate / sustainability     → CleanTech
     Physical robot or autonomous hardware → Robotics
     Chip / semiconductor / connectivity   → DeepTech
     Security / identity / cryptography    → Cybersecurity
     Real estate / construction            → PropTech
     Food / agriculture / nutrition        → FoodTech or AgriTech
     Education / learning                  → EdTech
     HR / recruiting / workforce           → HRTech
     Supply chain / freight / last mile    → Logistics
     Factory / industrial process / manufacturing → Industry 4.0
  
  2. If software platform: who is the primary customer?
     Hospitals / patients / clinicians     → HealthTech
     Banks / investors / insurers          → FinTech
     General enterprises — AI at the core → AI/ML
     General enterprises — other software → Enterprise SaaS
     Consumers / individuals               → B2C Tech
  
  Return ONE from:
    AI/ML | HealthTech | BioTech | MedTech | FinTech | CleanTech | DeepTech
    | Robotics | Cybersecurity | PropTech | FoodTech | AgriTech | EdTech
    | HRTech | Logistics | Industry 4.0 | Enterprise SaaS | B2C Tech | Other

"sub_industry"
  One or more specific segments that describe the company. Up to 3 values,
  comma-separated, ordered from most to least relevant.
  
  AI/ML:           Applied AI, AI Infrastructure, AI Agents, Foundation Models, MLOps, Simulation
  HealthTech:      Digital Therapeutics, Clinical Decision Support, Patient Monitoring, Health Data, Neurology
  BioTech:         Drug Discovery, Gene Therapy, Diagnostics, Synthetic Biology, Immunology, Oncology
  MedTech:         Surgical Devices, Wearables, Imaging, Implants, Point-of-Care, Endoscopy
  FinTech:         Payments, WealthTech, InsurTech, Banking Infrastructure, RegTech, DeFi, Lending
  CleanTech:       Solar, Energy Storage, Grid & Infrastructure, Carbon & Offsetting, Water, Circular Economy, Green Hydrogen
  DeepTech:        Semiconductors, Photonics, Quantum, Advanced Materials, Space, Connectivity, Sensors
  Robotics:        Industrial Robotics, Construction Robotics, Logistics Automation, Surgical Robotics, Inspection
  Cybersecurity:   Identity & Access, Endpoint, Network Security, Post-Quantum Cryptography, Compliance
  PropTech:        Real Estate Platforms, Construction Tech, Smart Building, Facility Management
  Logistics:       Last Mile, Supply Chain Visibility, Fleet Management, Freight Tech
  Industry 4.0:    Smart Manufacturing, Digital Twin, Quality Control, Process Automation
  Enterprise SaaS: CRM / Sales Enablement, Marketing Tech, Data & Analytics, Workflow Automation, ERP
  AgriTech:        Precision Agriculture, Vertical Farming, Animal Health, Soil & Crop Analytics
  FoodTech:        Alternative Proteins, Food Safety, Nutrition Tech, Restaurant Tech
  Other:           use the most descriptive label possible, max 3 words per segment
  
  A company can span multiple segments — e.g. "Wearables, Patient Monitoring"
  or "Applied AI, Clinical Decision Support".
  Return null if nothing fits.

"business_model_type"
  Determine by answering these questions from the article:

  Q1 — Who pays?
    A business / enterprise pays      → B2B candidate
    An individual consumer pays       → B2C candidate
    Both sides of a platform transact → Marketplace candidate
    No payment / pure research        → Deep Tech / IP candidate

  Q2 — What is delivered?
    Recurring SaaS / software license → B2B-SaaS or B2C-SaaS
    Per-transaction fee               → Marketplace or Usage-Based
    Physical hardware                 → B2B-Hardware
    Consulting / implementation       → B2B-Services
    IP license or royalties only      → Deep Tech / IP

  Q3 — Channel?
    Sold directly to end user         → B2B or B2C
    Enterprise buys, end user consumes → B2B2C
    Platform connecting two parties   → Marketplace

  Return ONE of:
    B2B-SaaS | B2B-Hardware | B2B-Services | B2B2C | B2C | Marketplace
    | Deep Tech / IP | Unknown

"primary_keywords"
  2 to 4 terms from the CANONICAL KEYWORD LIST below.
  These must describe the company's own core technology — what they built.
  Only use terms from the list. Return comma-separated.
  Return null if no term applies closely.

"secondary_keywords"
  1 to 3 terms from the CANONICAL KEYWORD LIST below.
  These describe adjacent technologies the company integrates with, depends on,
  or operates within — but did not build themselves.
  Only use terms from the list. Return comma-separated.
  Return null if no term applies.

---

CANONICAL KEYWORD LIST:
{canonical_keywords}

---

Return ONLY this JSON object. No markdown. No extra keys. No trailing commas. Use null for missing values, not empty strings.

{{
  "startup_name": "...",
  "publication_date": "{publication_date}",
  "year": {year},
  "funding_amount": "...",
  "funding_round_raw": "...",
  "funding_round": "...",
  "investor_names": "...",
  "city": "...",
  "canton": "...",
  "founded_year": null,
  "employees": null,
  "website": "...",
  "location": "Switzerland",
  "industry": "...",
  "sub_industry": "...",
  "business_model_type": "...",
  "primary_keywords": "...",
  "secondary_keywords": "..."
}}"""
    
    return prompt


# ============================================================================
# LLM API CALL
# ============================================================================

def call_llm_api(prompt, retries=MAX_RETRIES):
    """
    Calls OpenAI API with retry logic.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise data extraction assistant specializing in Swiss startup ecosystem analysis. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            log_message(f"⚠️  API call failed (attempt {attempt + 1}/{retries}): {str(e)}")
            
            if attempt < retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                log_message(f"   Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                log_message(f"❌ Failed after {retries} attempts")
                return None


# ============================================================================
# LOGGING
# ============================================================================

def log_message(message):
    """
    Logs message to both console and file.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')


# ============================================================================
# CHECKPOINT MANAGEMENT
# ============================================================================

def load_checkpoint():
    """
    Loads checkpoint to resume processing.
    """
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            log_message(f"📂 Loaded checkpoint: {checkpoint['processed']} articles already processed")
            return checkpoint
        except:
            log_message("⚠️  Checkpoint file corrupted, starting fresh")
    
    return {'processed': 0, 'results': []}


def save_checkpoint(checkpoint):
    """
    Saves checkpoint to disk.
    """
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)


# ============================================================================
# DATA PROCESSING
# ============================================================================

def process_article(article, article_idx, total_articles):
    """
    Processes a single article through LLM.
    """
    log_message(f"\n{'='*80}")
    log_message(f"📄 Processing article {article_idx + 1}/{total_articles}")
    log_message(f"   Title: {article.get('title', 'N/A')[:80]}...")
    
    # Build prompt
    prompt = build_extraction_prompt(
        article['article_text'],
        article['publication_date'],
        article['year']
    )
    
    # Call LLM
    result = call_llm_api(prompt)
    
    if result:
        # Add metadata
        result['article_id'] = article.get('id')
        result['article_url'] = article.get('url')
        result['article_title'] = article.get('title')
        
        log_message(f"✅ Extracted: {result.get('startup_name', 'Unknown')}")
        log_message(f"   Industry: {result.get('industry', 'N/A')}")
        log_message(f"   Funding: {result.get('funding_amount', 'N/A')}")
        
        return result
    else:
        log_message(f"❌ Failed to extract data")
        return None


def process_all_articles():
    """
    Main processing loop.
    """
    log_message("="*80)
    log_message("🚀 LLM ARTICLE ANALYZER - STARTING")
    log_message("="*80)
    
    # Load input data
    log_message(f"\n📥 Loading articles from: {INPUT_FILE}")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    total_articles = len(articles)
    log_message(f"   Found {total_articles} articles to process")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    start_idx = checkpoint['processed']
    results = checkpoint['results']
    
    if start_idx > 0:
        log_message(f"   Resuming from article {start_idx + 1}")
    
    # Process articles
    for idx in range(start_idx, total_articles):
        article = articles[idx]
        
        # Process article
        result = process_article(article, idx, total_articles)
        
        if result:
            results.append(result)
        
        # Update checkpoint
        checkpoint['processed'] = idx + 1
        checkpoint['results'] = results
        
        # Save checkpoint every BATCH_SIZE articles
        if (idx + 1) % BATCH_SIZE == 0:
            save_checkpoint(checkpoint)
            log_message(f"\n💾 Checkpoint saved ({idx + 1}/{total_articles})")
        
        # Rate limiting
        if idx < total_articles - 1:  # Don't wait after last article
            time.sleep(RATE_LIMIT_DELAY)
    
    # Save final results
    log_message("\n" + "="*80)
    log_message("💾 SAVING FINAL RESULTS")
    log_message("="*80)
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Reorder columns
    column_order = [
        'startup_name', 'publication_date', 'year', 'funding_amount',
        'funding_round_raw', 'funding_round', 'investor_names',
        'city', 'canton', 'founded_year', 'employees', 'website',
        'location', 'industry', 'sub_industry', 'business_model_type',
        'primary_keywords', 'secondary_keywords',
        'article_id', 'article_url', 'article_title'
    ]
    
    # Ensure all columns exist
    for col in column_order:
        if col not in df.columns:
            df[col] = None
    
    df = df[column_order]
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    log_message(f"✅ Saved {len(df)} results to: {OUTPUT_FILE}")
    
    # Print statistics
    log_message("\n" + "="*80)
    log_message("📊 STATISTICS")
    log_message("="*80)
    log_message(f"Total articles processed: {len(df)}")
    log_message(f"With startup names: {df['startup_name'].notna().sum()}")
    log_message(f"With funding data: {df['funding_amount'].notna().sum()}")
    log_message(f"With city data: {df['city'].notna().sum()}")
    
    # Industry distribution
    if 'industry' in df.columns and df['industry'].notna().any():
        log_message("\nTop Industries:")
        industry_counts = df['industry'].value_counts().head(10)
        for industry, count in industry_counts.items():
            log_message(f"  {industry}: {count}")
    
    # Clean up checkpoint
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        log_message(f"\n🗑️  Removed checkpoint file")
    
    log_message("\n" + "="*80)
    log_message("✅ PROCESSING COMPLETE!")
    log_message("="*80)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Check API key
    if not OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY environment variable not set!")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        exit(1)
    
    # Run processing
    try:
        process_all_articles()
    except KeyboardInterrupt:
        log_message("\n\n⚠️  Process interrupted by user")
        log_message("   Progress saved in checkpoint file")
        log_message("   Run again to resume")
    except Exception as e:
        log_message(f"\n\n❌ FATAL ERROR: {str(e)}")
        import traceback
        log_message(traceback.format_exc())
