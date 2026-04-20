# 🤖 Claude Article Analysis Prompt

## How to Use This

1. **Copy the prompt below** (everything in the box)
2. **Paste it into Claude** (this conversation or new chat)
3. **Add 5-10 articles** from your JSON file
4. **Claude will return structured JSON** for all articles
5. **Copy the JSON response** and save to a file
6. **Run the merge script** to combine all batches

---

## 📋 PROMPT TO COPY-PASTE TO CLAUDE

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
   - "siebenstelliger Betrag" → "undisclosed"
   - Return null if no funding mentioned

5. "funding_round_raw": Exact phrase used (e.g., "seed round", "Seed-Runde", "Kapitalerhöhung")

6. "funding_round": Map to ONE of: Pre-Seed, Seed, Seed Extension, Series A, Series B, Series C, Series D+, Strategic Investment, Grant, Award, Debt, Undisclosed
   - "seed round" → Seed
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
    - (See full list in context)

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

## 📝 Example Usage

**You send to Claude:**

```
[Use the prompt above, then add:]

ARTICLES TO ANALYZE:

Article 1:
{
  "id": 1,
  "title": "Delta Labs raises EUR 4.4 million for AI customer simulation platform",
  "publication_date": "2026-04-02",
  "year": 2026,
  "article_text": "Delta Labs raises EUR 4.4 million for AI customer simulation platform 02.04.2026 Delta Labs has raised EUR 4.4 million in a seed round led by Cusp Capital and Auxxo Female Catalyst Fund. The company develops AI-powered customer simulation tools that help businesses anticipate how customers will respond to decisions before they are made..."
}

Article 2:
{
  "id": 2,
  "title": "UBS makes a strategic investment in Artificialy",
  "publication_date": "2026-04-02",
  "year": 2026,
  "article_text": "UBS makes a strategic investment in Artificialy 02.04.2026 Lugano-based Artificialy announced an a strategic investment from UBS..."
}

[Continue with 3-8 more articles]
```

**Claude will respond with:**

```json
[
  {
    "startup_name": "Delta Labs AG",
    "publication_date": "2026-04-02",
    "year": 2026,
    "funding_amount": "4.4M EUR",
    "funding_round_raw": "seed round",
    "funding_round": "Seed",
    "investor_names": "Cusp Capital, Auxxo Female Catalyst Fund",
    "city": "Zurich",
    "canton": "ZH",
    "founded_year": 2022,
    "employees": null,
    "website": null,
    "location": "Switzerland",
    "industry": "AI/ML",
    "sub_industry": "Applied AI, Simulation",
    "business_model_type": "B2B-SaaS",
    "primary_keywords": "AI, GenAI",
    "secondary_keywords": "Enterprise"
  },
  {
    "startup_name": "Artificialy SA",
    "publication_date": "2026-04-02",
    "year": 2026,
    "funding_amount": "undisclosed",
    "funding_round_raw": "strategic investment",
    "funding_round": "Strategic Investment",
    "investor_names": "UBS",
    "city": "Lugano",
    "canton": "TI",
    "founded_year": 2020,
    "employees": null,
    "website": null,
    "location": "Switzerland",
    "industry": "AI/ML",
    "sub_industry": "Applied AI, AI Infrastructure",
    "business_model_type": "B2B-SaaS",
    "primary_keywords": "AI, Enterprise",
    "secondary_keywords": "Infrastructure"
  }
]
```

---

## 💡 Tips

1. **Process in batches of 5-10 articles** (Claude has context limits)
2. **Save each response** to separate JSON files: `batch_1.json`, `batch_2.json`, etc.
3. **Use the merge script** (below) to combine all batches into final CSV
4. **Review the output** - Claude is accurate but check for edge cases

---

## 📊 How Many Batches?

Check your article count:
```bash
python3 -c "import json; articles=json.load(open('data/startupticker_articles_for_llm.json')); print(f'{len(articles)} articles = ~{len(articles)//10 + 1} batches of 10')"
```

---

## ⚡ Quick Workflow

```
1. Copy prompt above
2. Send to Claude with 10 articles
3. Copy JSON response
4. Save as data/batch_1.json
5. Repeat for next 10 articles → batch_2.json
6. After all batches, run: python3 10_merge_claude_batches.py
7. Done! → data/startupticker_analyzed_claude.csv
```
