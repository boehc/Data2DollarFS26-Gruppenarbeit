# 🎯 LLM Article Analyzer - Visual Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    📥 INPUT: Articles JSON                          │
│  data/startupticker_articles_for_llm.json                           │
│  50+ Swiss startup articles (2023-2026)                             │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Load articles
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  🤖 LLM PROCESSING (GPT-4o)                          │
│  8_llm_article_analyzer.py                                          │
│                                                                       │
│  For each article:                                                  │
│  1. Build extraction prompt (3000 tokens)                           │
│  2. Call OpenAI API                                                 │
│  3. Parse JSON response (500 tokens)                                │
│  4. Save checkpoint every 10 articles                               │
│                                                                       │
│  Features:                                                          │
│  ✓ Automatic retry on failures                                     │
│  ✓ Resume from checkpoint                                          │
│  ✓ Rate limiting (1 sec/call)                                       │
│  ✓ Structured JSON output                                          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Extract 18 fields
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   📊 OUTPUT: Structured CSV                         │
│  data/startupticker_analyzed_v8.csv                                 │
│                                                                       │
│  18 Fields per article:                                             │
│  ├─ Basic: name, date, year                                         │
│  ├─ Funding: amount, round, investors                               │
│  ├─ Location: city, canton, country                                 │
│  ├─ Company: founded year, employees, website                       │
│  ├─ Classification: industry, sub-industry, business model          │
│  └─ Keywords: primary, secondary                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Analyze results
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   🔬 QUALITY ANALYSIS                               │
│  9_quality_analysis.py                                              │
│                                                                       │
│  Reports:                                                           │
│  ✓ Completeness rates (95%+ for key fields)                        │
│  ✓ Funding distribution (amounts, rounds, investors)               │
│  ✓ Geographic distribution (cantons, cities)                        │
│  ✓ Industry breakdown (AI/ML, FinTech, etc.)                       │
│  ✓ Keyword frequency (80+ categories)                              │
│  ✓ Data quality issues                                             │
└─────────────────────────────────────────────────────────────────────┘
```

## 📋 Extraction Flow per Article

```
┌───────────────┐
│ Article Text  │
│ (500-2000     │
│  words)       │
└───────┬───────┘
        │
        ↓
┌───────────────────────────────────────────────────────────────┐
│ PROMPT TEMPLATE                                               │
│                                                               │
│ Article: "Delta Labs raises EUR 4.4 million..."              │
│                                                               │
│ Extract:                                                      │
│ - startup_name → Look for "Company AG/SA/GmbH"               │
│ - funding_amount → Normalize to "4.4M EUR"                   │
│ - funding_round → Map to: Seed, Series A, etc.               │
│ - investor_names → Parse comma-separated list                │
│ - city → Extract from "Zurich-based", "Zürcher", etc.       │
│ - canton → Map city to ZH, GE, VD, etc.                     │
│ - founded_year → Look for "founded in 2022"                 │
│ - employees → Parse "team of 30", "30 Mitarbeitende"        │
│ - website → Extract .ch/.com/.io domain                     │
│ - industry → Classify: AI/ML, FinTech, etc.                 │
│ - sub_industry → Applied AI, Simulation, etc.               │
│ - business_model_type → B2B-SaaS, B2C, etc.                 │
│ - primary_keywords → Core tech (AI, GenAI, etc.)            │
│ - secondary_keywords → Adjacent tech (Enterprise, etc.)     │
│                                                               │
│ Use 80+ canonical keywords from enhanced_keywords_v6.py      │
└───────────────────────────────────────────────────────────────┘
        │
        ↓
┌───────────────┐
│ GPT-4o API    │
│ Temperature:  │
│   0.1         │
│ Max tokens:   │
│   2000        │
└───────┬───────┘
        │
        ↓
┌───────────────────────────────────────────────────────────────┐
│ JSON RESPONSE                                                 │
│                                                               │
│ {                                                             │
│   "startup_name": "Delta Labs AG",                           │
│   "funding_amount": "4.4M EUR",                              │
│   "funding_round": "Seed",                                   │
│   "investor_names": "Cusp Capital, Auxxo Female Catalyst",   │
│   "city": "Zurich",                                          │
│   "canton": "ZH",                                            │
│   "founded_year": 2022,                                      │
│   "employees": 30,                                           │
│   "website": "deltalabs.ai",                                 │
│   "industry": "AI/ML",                                       │
│   "sub_industry": "Applied AI, Simulation",                  │
│   "business_model_type": "B2B-SaaS",                         │
│   "primary_keywords": "AI, GenAI",                           │
│   "secondary_keywords": "Enterprise"                         │
│ }                                                             │
└───────────────────────────────────────────────────────────────┘
        │
        ↓
┌───────────────┐
│ CSV Row       │
│ Saved!        │
└───────────────┘
```

## 🎯 Field Mapping Logic

### 🏢 Startup Name
```
Text: "Die Zürcher Delta Labs AG entwickelt..."
Pattern: Look for "Company [AG|SA|GmbH|Sàrl]"
Extract: "Delta Labs AG"
```

### 💰 Funding Amount
```
Text: "EUR 4.4 million", "3,5 Millionen Euro", "siebenstelliger Betrag"
Normalize: "4.4M EUR", "3.5M EUR", "undisclosed"
Format: {number}M {CURRENCY}
```

### 🔄 Funding Round
```
Raw: "seed round", "Seed-Runde", "Kapitalerhöhung"
Map: Seed, Seed Extension, Series A, Series B, Strategic Investment, Grant, Award, Debt, Undisclosed
Output: "Seed"
```

### 📍 Location
```
Text: "Zurich-based", "Die Zürcher", "basée à Genève"
City: "Zurich"
Canton: "ZH" (auto-mapped)
```

### 🏭 Industry
```
Logic:
1. What is built? → Drug = BioTech, Device = MedTech, Software = SaaS
2. Who is customer? → Enterprise = B2B, Consumer = B2C
3. What's the tech? → AI core = AI/ML, Finance = FinTech

Output: One of 19 categories
```

### 🔑 Keywords
```
Primary: What company BUILT (AI, GenAI, LLM)
Secondary: What company USES (Enterprise, Infrastructure)

Source: 80+ canonical keywords from enhanced_keywords_v6.py
```

## 📊 Typical Output Statistics

```
Field Completeness:
┌─────────────────────┬──────────┬────────┐
│ Field               │ Present  │ Rate   │
├─────────────────────┼──────────┼────────┤
│ ✅ Startup Name     │ 48/50    │ 96%    │
│ ✅ Industry         │ 47/50    │ 94%    │
│ ⚠️  Funding Amount  │ 42/50    │ 84%    │
│ ✅ City             │ 43/50    │ 86%    │
│ ⚠️  Founded Year    │ 35/50    │ 70%    │
│ ⚠️  Employees       │ 25/50    │ 50%    │
│ ✅ Keywords         │ 45/50    │ 90%    │
└─────────────────────┴──────────┴────────┘

Top Industries:
┌─────────────────────┬────────┐
│ AI/ML               │   18   │
│ HealthTech          │   8    │
│ CleanTech           │   6    │
│ FinTech             │   5    │
│ DeepTech            │   4    │
└─────────────────────┴────────┘

Top Cities:
┌─────────────────────┬────────┐
│ Zurich              │   15   │
│ Lausanne            │   12   │
│ Geneva              │   8    │
│ Zug                 │   5    │
└─────────────────────┴────────┘
```

## ⚙️ Configuration Options

```python
# Model Selection
MODEL = 'gpt-4o'           # Best quality/speed/cost
      = 'gpt-4-turbo'      # Highest quality
      = 'gpt-3.5-turbo'    # Fastest/cheapest

# Quality vs Speed
TEMPERATURE = 0.1          # 0.0 = deterministic, 1.0 = creative
MAX_TOKENS = 2000          # Response length limit

# Processing
BATCH_SIZE = 10            # Checkpoint frequency
RATE_LIMIT_DELAY = 1.0     # Seconds between calls
MAX_RETRIES = 3            # Retry attempts on failure
```

## 💰 Cost Calculator

```
Per Article:
  Input:  ~3,000 tokens × $2.50/1M = $0.0075
  Output:   ~500 tokens × $10/1M  = $0.0050
  Total:                            $0.0125

For 50 articles:  50 × $0.0125 = $0.625
For 100 articles: 100 × $0.0125 = $1.25
For 500 articles: 500 × $0.0125 = $6.25
```

## 🚀 Quick Commands

```bash
# Setup
pip install openai pandas
export OPENAI_API_KEY='sk-...'

# Test
python3 test_llm_setup.py

# Run
python3 8_llm_article_analyzer.py

# Analyze
python3 9_quality_analysis.py
```

## 📁 File Structure

```
pfad_a_scraper/
├── 8_llm_article_analyzer.py      ← Main script
├── 9_quality_analysis.py          ← Results analyzer
├── test_llm_setup.py              ← Setup tester
├── enhanced_keywords_v6.py        ← Keyword taxonomy
│
├── LLM_ANALYZER_README.md         ← Full docs
├── QUICK_START_LLM.md             ← Quick guide
├── LLM_ANALYZER_SUMMARY.md        ← Summary
│
└── data/
    ├── startupticker_articles_for_llm.json    ← Input
    ├── startupticker_analyzed_v8.csv          ← Output
    ├── llm_analyzer_checkpoint_v8.json        ← Checkpoint
    └── llm_analyzer_v8.log                    ← Log
```

---

**Ready to extract? See QUICK_START_LLM.md** 🚀
