"""
Startupticker.ch News Scraper V7 - STEP 2 (LLM Extraction) - V3

This script processes the raw articles from Step 1 and extracts structured
startup data using Claude via GitHub Copilot agent.

INPUT:  data/startupticker_raw_articles_v7_step1_FINANCING.csv
OUTPUT: data/startupticker_startups_v7_step2.csv

The LLM extracts:
- Startup name, funding details, investors (including acquisitions)
- Location (city, canton)
- Industry classification
- Business model
- Keywords

V3 IMPROVEMENTS:
- Filter out non-events (VC fund closes, ecosystem roundups)
- Support for acquisitions as funding events
- Better startup name extraction rules
- Expanded city coverage
- Article URL and Title in output

NOTE: This script is designed to run interactively with GitHub Copilot.
Each article will be processed one by one, with the LLM extraction
happening through the Copilot agent interface.
"""

import pandas as pd
import json
import time
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_FILE = './data/startupticker_raw_articles_v7_step1_FINANCING.csv'
OUTPUT_FILE = './data/startupticker_startups_v7_step2.csv'
CHECKPOINT_FILE = './data/startupticker_v7_step2_checkpoint.csv'

# Processing settings
TEST_MODE = True  # Set to False to process all articles
TEST_ARTICLES = 10  # Number of articles to process in test mode
CHECKPOINT_INTERVAL = 50  # Save progress every N articles

# Canonical keyword list (placeholder from your prompt)
CANONICAL_KEYWORDS = """Generative AI, Large Language Models (LLM), Computer Vision,
Natural Language Processing (NLP), Predictive Analytics, Machine Learning,
AI Agents, Reinforcement Learning, Simulation & Synthetic Data,
EEG / Brain Signal Processing, Digital Therapeutics, Remote Patient Monitoring,
Drug Discovery, mRNA / Gene Therapy, Immunology, Diagnostics,
CRISPR / Gene Editing, Wearable Sensors,
Federated Learning, Cybersecurity / Zero Trust, Post-Quantum Cryptography,
Blockchain / DLT, Smart Contracts,
Solar / Photovoltaics, Battery Storage, Carbon Capture, Energy Grid Management,
Robotics / Autonomous Systems, Digital Twin, Computer-Aided Manufacturing,
Semiconductor Design, High-Speed Connectivity, Edge Computing, IoT Sensors,
SaaS / Cloud Platform, API Integration, Workflow Automation,
Marketplace / Platform, B2B Data Network,
Satellite / Space Tech, Quantum Computing,
Synthetic Biology, Fermentation Technology, Precision Fermentation"""


# ============================================================================
# LLM PROMPT TEMPLATE (V3)
# ============================================================================

EXTRACTION_PROMPT = """You are a data extraction engine for Swiss startup news articles from startupticker.ch.
Articles may be in English, German, or French.

Extract structured fields from the article below.
Return ONLY a single valid JSON object — no explanation, no markdown, no commentary.
Return null for any field you cannot determine with confidence. Never guess. Never invent defaults.

---

ARTICLE TEXT:
<article_text>
{article_text}
</article_text>

PUBLICATION DATE (extracted in Step 1): {publication_date}
YEAR (extracted in Step 1): {year}

---

FIELD INSTRUCTIONS:

"startup_name"
  The full legal name of the primary company this article is about —
  the one that raised money, launched a product, won an award, or was acquired.
  The most reliable source is the company name tagged near the bottom of the
  article, right before the date stamp. It appears as "Company AG", "Company SA",
  "Company GmbH", "Company Sàrl" or similar legal form.

  In an acquisition, the primary subject is the ACQUIRED company (target),
  not the acquirer.

  Rules:
  - Never return an investor name, acquirer name, event name, or headline fragment.
  - Never return single generic words: "Labs", "Space", "Five", "Seed", "CHF",
    "New", "Continuing", "Zürichbased", "Introducing", "Milestones".
  - If the article is about a VC firm, investment fund, or accelerator raising
    LP capital (a "fund close"), return null. These are not startup financing events.
    Signals: "first closing", "final closing", "fund close", "erste Schliessung",
    "finaler Close", "committed capital", "LP commitments", "target fund size",
    "Fondsgrösse".
  - If the article covers multiple companies equally (award ceremony, ecosystem
    roundup) and no single primary subject exists, return null.

"publication_date"
  Pass through exactly: {publication_date}

"year"
  Pass through exactly: {year}

"funding_amount"
  The total amount raised in the specific round described in this article,
  OR the acquisition price paid for the target company.

  Normalize to: {{number}}M {{CURRENCY}}
  Examples:
    "EUR 4.4 million"               → "4.4M EUR"
    "USD 225 million"               → "225M USD"
    "$225mm"                        → "225M USD"
    "3,5 Millionen Euro"            → "3.5M EUR"    ← German decimal comma
    "CHF 100,000"                   → "0.1M CHF"
    "acquired for CHF 12 million"   → "12M CHF"
    "siebenstelliger Betrag"        → "undisclosed"  ← German: 7-figure amount
    "zweistelliger Millionenbetrag" → "undisclosed"  ← German: double-digit million
    "montant à sept chiffres"       → "undisclosed"  ← French: 7-figure amount
    "einen hohen einstelligen Millionenbetrag" → "undisclosed" ← high single-digit M
    "Übernahmepreis nicht kommuniziert" → "undisclosed" ← German: acquisition price not disclosed
    "Series A announced, amount not disclosed" → "undisclosed"

  Return "undisclosed" if an amount is referenced but not specified.
  Return null if no funding or acquisition event is described at all.

"funding_round_raw"
  Copy the exact phrase the article uses to describe the round type or deal type.
  Preserve the original language.
  Examples:
    "seed round", "Seed-Runde", "Series B", "Kapitalerhöhung",
    "strategic investment", "Seed-Erweiterungsrunde", "Grant", "Förderung",
    "convertible note", "venture debt", "tour de table Série A",
    "acquisition", "Übernahme", "asset deal", "acquis par", "übernommen von"
  Return null if no round or deal type is mentioned at all.

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
    Acquisition
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
    "acquisition" / "Übernahme" / "asset deal" /
      "acquis par" / "übernommen von"                         → Acquisition
    "Kapitalerhöhung" with no round name given                → Undisclosed
    "bridge round" / "Überbrückungsfinanzierung"              → Undisclosed
    Innosuisse / foundation / EU / government money           → Grant
    Venture Kick / FIT prize / competition prize              → Award
    "convertible note" / "venture debt" / "Darlehen" /
      "SAFE" / "Simple Agreement for Future Equity"           → Debt
    Funding confirmed but round type genuinely unclear        → Undisclosed

  IMPORTANT: Do not infer or override based on amount size.
  Map only what the article explicitly states or clearly implies by language.
  Return null if no funding or acquisition event is described.

"investor_names"
  Comma-separated list of all investors or acquirers who participated in THIS round.
  Include: VC firms, corporate venture arms, family offices, business angels, banks.
  In an acquisition, list the acquiring company as the sole entry.
  Exclude: advisors, board members (unless explicitly stated they also co-invested),
           investors from previous rounds not re-investing here.
  Return null if no investors or acquirers are named for this event.

"city"
  City where the startup is headquartered.
  Language patterns to recognize:
    English: "Zurich-based X", "Founded in Lausanne", "headquartered in Basel",
             "X, based in Bern", "based in Winterthur"
    German:  "Das Zürcher Startup", "Die St. Galler X", "das Basler Unternehmen",
             "das Luzerner Startup", "in Zug ansässige", "Die Genfer", "Lausanner",
             "das Winterthurer Unternehmen", "die Rapperswiler"
    French:  "basée à Genève", "startup lausannoise", "société genevoise",
             "implantée à Zurich", "basée à Carouge"
  Return in standard English spelling: Zurich, Geneva, Lausanne, Basel, Bern,
  Lucerne, Zug, St. Gallen, Lugano, Winterthur, Rapperswil, Carouge, Biel.
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

  AI/ML:           Applied AI | AI Infrastructure | AI Agents | Foundation Models | MLOps | Simulation
  HealthTech:      Digital Therapeutics | Clinical Decision Support | Patient Monitoring | Health Data | Neurology
  BioTech:         Drug Discovery | Gene Therapy | Diagnostics | Synthetic Biology | Immunology | Oncology
  MedTech:         Surgical Devices | Wearables | Imaging | Implants | Point-of-Care | Endoscopy
  FinTech:         Payments | WealthTech | InsurTech | Banking Infrastructure | RegTech | DeFi | Lending
  CleanTech:       Solar | Energy Storage | Grid & Infrastructure | Carbon & Offsetting | Water | Circular Economy | Green Hydrogen
  DeepTech:        Semiconductors | Photonics | Quantum | Advanced Materials | Space | Connectivity | Sensors
  Robotics:        Industrial Robotics | Construction Robotics | Logistics Automation | Surgical Robotics | Inspection
  Cybersecurity:   Identity & Access | Endpoint | Network Security | Post-Quantum Cryptography | Compliance
  PropTech:        Real Estate Platforms | Construction Tech | Smart Building | Facility Management
  Logistics:       Last Mile | Supply Chain Visibility | Fleet Management | Freight Tech
  Industry 4.0:    Smart Manufacturing | Digital Twin | Quality Control | Process Automation
  Enterprise SaaS: CRM / Sales Enablement | Marketing Tech | Data & Analytics | Workflow Automation | ERP
  AgriTech:        Precision Agriculture | Vertical Farming | Animal Health | Soil & Crop Analytics
  FoodTech:        Alternative Proteins | Food Safety | Nutrition Tech | Restaurant Tech
  HRTech:          Recruiting | Workforce Management | Payroll | Learning & Development
  EdTech:          Online Learning | Corporate Training | Language Learning | Assessment
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

Return ONLY this JSON object. No markdown. No extra keys. No trailing commas.

{{
  "startup_name": null,
  "publication_date": null,
  "year": null,
  "funding_amount": null,
  "funding_round_raw": null,
  "funding_round": null,
  "investor_names": null,
  "city": null,
  "canton": null,
  "founded_year": null,
  "employees": null,
  "website": null,
  "location": "Switzerland",
  "industry": null,
  "sub_industry": null,
  "business_model_type": null,
  "primary_keywords": null,
  "secondary_keywords": null
}}"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def setup_anthropic_client():
    """Initialize Anthropic API client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable not set.\n"
            "Set it with: export ANTHROPIC_API_KEY='your-api-key-here'"
        )
    return anthropic.Anthropic(api_key=api_key)


def extract_startup_data(client, article_text, publication_date, year):
    """
    Extract structured startup data from article using Claude.
    
    Returns: dict with extracted fields or None on failure
    """
    # Build prompt
    prompt = EXTRACTION_PROMPT.format(
        article_text=article_text,
        publication_date=publication_date,
        year=year,
        canonical_keywords=CANONICAL_KEYWORDS
    )
    
    try:
        # Call Claude API
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract response text
        response_text = message.content[0].text.strip()
        
        # Parse JSON
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        data = json.loads(response_text)
        return data
        
    except json.JSONDecodeError as e:
        print(f"      ❌ JSON parse error: {str(e)[:50]}")
        return None
    except Exception as e:
        print(f"      ❌ API error: {str(e)[:50]}")
        return None


def save_checkpoint(df, checkpoint_file):
    """Save checkpoint CSV."""
    df.to_csv(checkpoint_file, index=False)
    print(f"      💾 Checkpoint saved: {len(df)} rows")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main processing logic - STEP 2 LLM extraction."""
    
    print("="*70)
    print("STARTUPTICKER.CH SCRAPER V7 - STEP 2 (LLM EXTRACTION)")
    print("="*70)
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Model:  {MODEL}")
    if TEST_MODE:
        print(f"🧪 TEST MODE: Processing {TEST_ARTICLES} articles only")
    print("="*70)
    print()
    
    # Load Step 1 data
    print("Loading Step 1 data...")
    try:
        df_input = pd.read_csv(INPUT_FILE)
        print(f"✓ Loaded {len(df_input)} articles\n")
    except Exception as e:
        print(f"❌ Error loading input file: {e}")
        return
    
    # Limit to test articles if in test mode
    if TEST_MODE:
        df_input = df_input.head(TEST_ARTICLES)
    
    # Initialize Anthropic client
    print("Initializing Claude API...")
    try:
        client = setup_anthropic_client()
        print("✓ API client ready\n")
    except Exception as e:
        print(f"❌ {e}")
        return
    
    # Process articles
    print("PROCESSING ARTICLES")
    print("-" * 70)
    
    results = []
    error_count = 0
    filtered_count = 0  # Count of non-events filtered out
    
    for i, row in df_input.iterrows():
        article_num = i + 1
        
        # Progress indicator
        if article_num % 10 == 1 or article_num % 10 == 0:
            print(f"\n[{article_num}/{len(df_input)}] Processing...")
        
        print(f"  [{article_num:4d}] {row['Title'][:50]}...", end='')
        
        try:
            # Extract data using Claude
            extracted = extract_startup_data(
                client,
                row['Article_Text'],
                row['Publication_Date'],
                int(row['Year'])
            )
            
            if extracted:
                # V3: Filter out non-events (VC fund closes, ecosystem roundups)
                # Drop if BOTH startup_name AND funding_round are null
                if extracted.get('startup_name') is None and extracted.get('funding_round') is None:
                    filtered_count += 1
                    print(f" ⊘ (non-event filtered)")
                else:
                    # Add metadata from Step 1
                    extracted['Article_URL'] = row.get('URL', None)
                    extracted['Article_Title'] = row.get('Title', None)
                    extracted['Article_Text'] = row['Article_Text']
                    results.append(extracted)
                    print(f" ✓ ({extracted.get('startup_name', 'N/A')[:30]})")
            else:
                error_count += 1
                print(f" ✗ (extraction failed)")
        
        except Exception as e:
            error_count += 1
            print(f" ✗ (error: {str(e)[:30]})")
        
        # Rate limiting (be nice to the API)
        time.sleep(1)
        
        # Checkpoint save
        if article_num % CHECKPOINT_INTERVAL == 0 and results:
            df_results = pd.DataFrame(results)
            save_checkpoint(df_results, CHECKPOINT_FILE)
    
    print(f"\n✓ Processing complete\n")
    
    # Save final results
    if not results:
        print("⚠️  No data extracted")
        return
    
    print("SAVING RESULTS")
    print("-" * 70)
    
    # Create DataFrame with correct column order (V3 spec)
    df_results = pd.DataFrame(results)
    
    # Define column order (as specified in V3 prompt)
    column_order = [
        'startup_name', 'publication_date', 'year', 'industry', 'sub_industry',
        'business_model_type', 'funding_amount', 'funding_round_raw',
        'funding_round', 'investor_names', 'city', 'canton', 'location',
        'founded_year', 'employees', 'website', 'primary_keywords',
        'secondary_keywords', 'Article_URL', 'Article_Title', 'Article_Text'
    ]
    
    # Reorder columns (keep only columns that exist)
    existing_cols = [col for col in column_order if col in df_results.columns]
    df_results = df_results[existing_cols]
    
    # Rename to match CSV naming convention (capitalize appropriately)
    rename_map = {
        'startup_name': 'Startup_Name',
        'publication_date': 'Publication_Date',
        'year': 'Year',
        'industry': 'Industry',
        'sub_industry': 'Sub_Industry',
        'business_model_type': 'Business_Model_Type',
        'funding_amount': 'Funding_Amount',
        'funding_round_raw': 'Funding_Round_Raw',
        'funding_round': 'Funding_Round',
        'investor_names': 'Investor_Names',
        'city': 'City',
        'canton': 'Canton',
        'location': 'Location',
        'founded_year': 'Founded_Year',
        'employees': 'Employees',
        'website': 'Website',
        'primary_keywords': 'Primary_Keywords',
        'secondary_keywords': 'Secondary_Keywords',
        'Article_URL': 'Article_URL',
        'Article_Title': 'Article_Title',
        'Article_Text': 'Article_Text'
    }
    df_results = df_results.rename(columns=rename_map)
    
    # Save to CSV
    df_results.to_csv(OUTPUT_FILE, index=False)
    print(f"✓ Saved: {OUTPUT_FILE}")
    print(f"  Rows: {len(df_results)}")
    print(f"  Columns: {len(df_results.columns)}")
    
    # Summary statistics
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total articles processed: {len(df_input)}")
    print(f"Successfully extracted: {len(results)}")
    print(f"Non-events filtered: {filtered_count}")
    print(f"Errors: {error_count}")
    print(f"Success rate: {len(results)/len(df_input)*100:.1f}%")
    
    # Field completeness
    print()
    print("📈 Field Completeness:")
    for col in df_results.columns:
        if col != 'Article_Text':
            non_null = df_results[col].notna().sum()
            pct = non_null / len(df_results) * 100
            print(f"  {col:20s}: {pct:5.1f}% ({non_null}/{len(df_results)})")
    
    print()
    print("✅ STEP 2 COMPLETED")
    print()


if __name__ == "__main__":
    main()
