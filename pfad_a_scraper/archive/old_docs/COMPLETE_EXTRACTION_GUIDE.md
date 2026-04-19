# 🚀 COMPLETE EXTRACTION WORKFLOW FOR 1564 ARTICLES

## Summary
- **Total articles**: 1564 (from FINANCING category)
- **Sorted**: Newest → Oldest (April 2026 → 2020)
- **Batches needed**: 157 batches of 10 articles
- **Estimated time**: ~13 hours (5 min per batch, can be parallelized)

---

## 📋 THE EXTRACTION PROMPT (Copy this exactly)

```
You are a precise data extraction assistant analyzing Swiss startup articles. Extract structured data from the articles I provide.

For each article, extract these 18 fields and return ONLY valid JSON (no markdown, no explanations):

FIELD DEFINITIONS:

1. "startup_name": Full legal name (e.g., "Delta Labs AG"). Look for "Company AG/SA/GmbH/Sàrl" near the article end. Never return investor names or generic words like "Labs", "Seed", "CHF", "New".
   SPECIAL CASES:
   - If article mentions 3+ companies with equal weight → set to null
   - If article is about investors, accelerators, ecosystem events (NOT receiving funding) → set to null
   - If multiple companies mentioned, choose the one receiving funding/award/grant
   - Award articles: If multiple winners, create ONE row per winner company

2. "publication_date": If provided value is empty/null, extract from article text (look for date at start like "02.04.2026" or "April 2, 2026"). Format as YYYY-MM-DD.

3. "year": If provided value is empty/null, extract from publication_date or article text

4. "funding_amount": Normalize to "{number}M {CURRENCY}" format
   - "EUR 4.4 million" → "4.4M EUR"
   - "3,5 Millionen Euro" → "3.5M EUR"
   - "CHF 100,000" → "0.1M CHF"
   - "$225 million" → "225M USD"
   - "siebenstelliger Betrag" → "undisclosed"
   - Return null if no funding mentioned

5. "funding_round_raw": Exact phrase used (e.g., "seed round", "Seed-Runde", "Kapitalerhöhung")

6. "funding_round": Map to ONE of: Pre-Seed, Seed, Seed Extension, Series A, Series B, Series C, Series D+, Strategic Investment, Grant, Award, Debt, Undisclosed
   - "seed round" → Seed
   - "Series A" → Series A
   - "Seed-Erweiterungsrunde" → Seed Extension
   - Venture Kick / prize → Award
   - Government / foundation → Grant

7. "investor_names": Comma-separated list. Include only investors in THIS round (exclude advisors, previous investors)

8. "city": Extract from "Zurich-based", "Die Zürcher", "basée à Genève". Use English spelling: Zurich, Geneva, Lausanne, Basel, Bern, Lucerne, Zug, St. Gallen, Lugano

9. "canton": 2-letter code mapped from city:
   - Zurich→ZH, Geneva→GE, Lausanne→VD, Basel→BS, Bern→BE, Zug→ZG, Lugano→TI, St. Gallen→SG, Lucerne→LU

10. "founded_year": 4-digit year from "founded in 2021", "gegründet 2022", "fondée en 2020"

11. "employees": Current headcount from "team of 30", "30 Mitarbeitende", "30 employés"

12. "website": Company domain (.ch/.com/.io/.ai) - not startupticker.ch or investor sites

13. "location": "Switzerland" unless explicitly stated otherwise

14. "industry": ONE of: AI/ML, HealthTech, BioTech, MedTech, FinTech, CleanTech, DeepTech, Robotics, Cybersecurity, PropTech, FoodTech, AgriTech, EdTech, HRTech, Logistics, Industry 4.0, Enterprise SaaS, B2C Tech, Other
    - Based on what company BUILT and who uses it
    - Drug/therapy → BioTech
    - Medical device → MedTech  
    - Clinical software → HealthTech
    - AI platform for enterprises → AI/ML
    - Energy/climate → CleanTech

15. "sub_industry": Up to 3 segments, comma-separated:
    - AI/ML: Applied AI, AI Infrastructure, AI Agents, Foundation Models, MLOps, Simulation
    - HealthTech: Digital Therapeutics, Clinical Decision Support, Patient Monitoring, Health Data
    - BioTech: Drug Discovery, Gene Therapy, Diagnostics, Synthetic Biology, Oncology
    - FinTech: Payments, WealthTech, InsurTech, Banking Infrastructure, RegTech
    - CleanTech: Solar, Energy Storage, Carbon & Offsetting, Circular Economy
    - DeepTech: Semiconductors, Photonics, Quantum, Advanced Materials, Space

16. "business_model_type": ONE of: B2B-SaaS, B2B-Hardware, B2B-Services, B2B2C, B2C, Marketplace, Deep Tech / IP, Unknown
    - Enterprise pays for software → B2B-SaaS
    - Consumer pays → B2C
    - Platform connects two sides → Marketplace
    - Physical product to business → B2B-Hardware

17. "primary_keywords": 2-4 keywords describing core technology the company BUILT. Use ONLY these keywords:
    AI, GenAI, LLM, AgentAI, Infrastructure, Enterprise, Gaming, PhysicalAI, DefenseTech, SpaceTech, SocialMedia, ConsumerApps, Policy, WearableTech, LegalTech, FusionEnergy, HRTech, ComputerVision, DeepTech, QuantumTech, Web3, SaaS, IoT, BioTech, HealthTech, FinTech, Mobility, AutonomousVehicles, ClimateTech, Robotics, AR/VR, Cybersecurity, Analytics, EdTech, PropTech, AgTech, FoodTech, Manufacturing, Logistics, Ecommerce, Semiconductors, CreatorEconomy

18. "secondary_keywords": 1-3 keywords for adjacent/integrated technologies (not core). Same keyword list.

IMPORTANT RULES:
- Return ONLY valid JSON array (no markdown code blocks, no explanations)
- Use null for missing values (not empty strings)
- Use exact field names as shown
- For multi-language articles, extract English equivalents
- MULTI-COMPANY ARTICLES:
  * If 3+ companies with equal weight → return ONE row with startup_name=null
  * If 2-4 companies receiving awards/grants → return ONE row per company
  * If article about ecosystem/investors/events → return ONE row with startup_name=null
- DATE HANDLING: Extract dates from article text if publication_date is null/empty
- AWARD ARTICLES: Create separate rows for each winning company with their specific award details

OUTPUT FORMAT:
[
  {
    "startup_name": "...",
    "publication_date": "2026-04-02",
    "year": 2026,
    "funding_amount": "4.4M EUR",
    "funding_round_raw": "seed round",
    "funding_round": "Seed",
    "investor_names": "Investor A, Investor B",
    "city": "Zurich",
    "canton": "ZH",
    "founded_year": 2022,
    "employees": 30,
    "website": "company.ch",
    "location": "Switzerland",
    "industry": "AI/ML",
    "sub_industry": "Applied AI, Simulation",
    "business_model_type": "B2B-SaaS",
    "primary_keywords": "AI, GenAI",
    "secondary_keywords": "Enterprise"
  }
]

Now I'll provide the articles to analyze. Extract data for ALL articles and return as a JSON array.
```

---

## 🔧 HOW TO USE THIS WORKFLOW

### Step 1: Generate All Batch Prompts

```bash
cd "/Users/chiaraboehme/Data2Dollar/Data2Dollar - Gruppenarbeit/Data2DollarFS26-Gruppenarbeit/pfad_a_scraper"
python3 10_automated_llm_extraction.py
# Choose option 1 (MANUAL MODE)
```

This creates 157 files: `data/batch_001_prompt.txt` through `data/batch_157_prompt.txt`

### Step 2: Process Batches in Claude

**Option A: Sequential Processing (slow but safe)**
```
1. Open data/batch_001_prompt.txt
2. Copy content between COPY markers
3. Paste into Claude
4. Wait for JSON response
5. Save response to data/batch_001.json
6. Repeat for batch_002, batch_003, etc.
```

**Option B: Parallel Processing (RECOMMENDED - 10x faster)**
```
1. Open 10 Claude chat windows/tabs
2. Window 1: Process batches 001-015 (articles 1-150)
3. Window 2: Process batches 016-030 (articles 151-300)
4. Window 3: Process batches 031-045 (articles 301-450)
5. Window 4: Process batches 046-060 (articles 451-600)
6. Window 5: Process batches 061-075 (articles 601-750)
7. Window 6: Process batches 076-090 (articles 751-900)
8. Window 7: Process batches 091-105 (articles 901-1050)
9. Window 8: Process batches 106-120 (articles 1051-1200)
10. Window 9: Process batches 121-135 (articles 1201-1350)
11. Window 10: Process batches 136-157 (articles 1351-1564)
```

**Time Estimate:**
- Sequential: 5 min/batch × 157 = ~13 hours
- Parallel (10 windows): 5 min/batch × 16 batches = **~1.5 hours**

### Step 3: Merge All Results

```bash
python3 10_automated_llm_extraction.py
# Choose option 2 (MERGE MODE)
```

This combines all `batch_*.json` files → `data/startupticker_extracted_llm_FULL.csv`

---

## 📊 Expected Output

**Final CSV columns (18 fields):**
```
startup_name, publication_date, year, funding_amount, funding_round_raw, 
funding_round, investor_names, city, canton, founded_year, employees, 
website, location, industry, sub_industry, business_model_type, 
primary_keywords, secondary_keywords
```

**Estimated row count:**
- Input: 1564 articles
- Output: ~1600-1700 rows (some award articles create multiple rows)
- Null startup_name: ~50-100 rows (ecosystem/multi-company articles)

---

## 💡 Pro Tips

1. **Batch tracking**: Keep a spreadsheet to track which batches are done
2. **Quality check**: After every 20 batches, run merge mode to check output
3. **Save progress**: Don't delete batch JSON files until final merge is verified
4. **Resume anytime**: Script picks up where you left off (skips existing batch_*.json files)
5. **Error handling**: If Claude returns invalid JSON, regenerate that batch

---

## 🚨 Important Notes

- **DO NOT edit the prompt** - it's carefully tuned for consistency
- **Save JSON exactly as Claude returns** - no modifications
- **One batch = one JSON file** - don't combine manually
- **File naming matters**: `batch_001.json`, `batch_002.json`, etc. (3-digit numbers with leading zeros)

---

## ✅ Ready to Start?

Run this command to begin:

```bash
cd "/Users/chiaraboehme/Data2Dollar/Data2Dollar - Gruppenarbeit/Data2DollarFS26-Gruppenarbeit/pfad_a_scraper"
python3 10_automated_llm_extraction.py
```

Then choose option 1 (MANUAL MODE) to generate all 157 batch prompts!
