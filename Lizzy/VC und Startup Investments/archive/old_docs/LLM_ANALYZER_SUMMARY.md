# 📊 LLM Article Analysis - Complete Solution

## What This Does

Analyzes 50+ Swiss startup articles (2023-2026) and extracts **18 structured data fields** using OpenAI GPT-4:

### Extracted Fields

1. **Basic Info**: startup_name, publication_date, year
2. **Funding**: funding_amount, funding_round_raw, funding_round, investor_names
3. **Location**: city, canton, location
4. **Company**: founded_year, employees, website
5. **Classification**: industry, sub_industry, business_model_type
6. **Keywords**: primary_keywords, secondary_keywords

## Files Created

| File | Purpose |
|------|---------|
| `8_llm_article_analyzer.py` | Main extraction script using GPT-4 |
| `test_llm_setup.py` | Test setup and API connection |
| `9_quality_analysis.py` | Analyze results quality |
| `LLM_ANALYZER_README.md` | Full documentation |
| `QUICK_START_LLM.md` | Quick start guide |

## Usage Flow

```
1. Install dependencies
   ↓
2. Set OpenAI API key
   ↓
3. Test setup → test_llm_setup.py
   ↓
4. Run analyzer → 8_llm_article_analyzer.py
   ↓
5. Analyze results → 9_quality_analysis.py
```

## Quick Start (5 minutes)

```bash
# 1. Install
pip install openai pandas

# 2. Set API key
export OPENAI_API_KEY='sk-your-key-here'

# 3. Test
python3 test_llm_setup.py

# 4. Run (test with 5 articles first)
# Edit line 555 in 8_llm_article_analyzer.py:
# articles = articles[:5]
python3 8_llm_article_analyzer.py

# 5. Analyze results
python3 9_quality_analysis.py
```

## Input

**File**: `data/startupticker_articles_for_llm.json`

**Structure**:
```json
[
  {
    "id": 1,
    "url": "...",
    "title": "...",
    "publication_date": "2026-04-02",
    "year": 2026,
    "article_text": "..."
  }
]
```

## Output

**File**: `data/startupticker_analyzed_v8.csv`

**Example row**:
```csv
startup_name,publication_date,year,funding_amount,funding_round,investor_names,city,canton,founded_year,employees,website,location,industry,sub_industry,business_model_type,primary_keywords,secondary_keywords
Delta Labs AG,2026-04-02,2026,4.4M EUR,Seed,"Cusp Capital, Auxxo Female Catalyst Fund",Zurich,ZH,2022,30,deltalabs.ai,Switzerland,AI/ML,"Applied AI, Simulation",B2B-SaaS,"AI, GenAI",Enterprise
```

## Features

### ✅ Robust
- Automatic retry on API failures
- Checkpoint/resume functionality
- Error logging and tracking

### ✅ Accurate
- GPT-4o model for best quality
- Low temperature (0.1) for consistency
- Structured JSON output format

### ✅ Complete
- 18 data fields extracted
- Multi-language support (EN/DE/FR)
- Canonical keyword list (80+ categories)

### ✅ Efficient
- Rate limiting to avoid API limits
- Batch checkpoint saving
- Cost-optimized (~$0.50-1.00 for 50 articles)

## Cost Breakdown

**Model**: GPT-4o

**Per article**:
- Input: ~3,000 tokens (article + prompt)
- Output: ~500 tokens (JSON response)
- Cost: ~$0.01-0.02 per article

**Total for 50 articles**: ~$0.50-1.00

## Field Extraction Logic

### Startup Name
- Looks for legal entity form (AG, SA, GmbH)
- Extracts from article footer tags
- Avoids investor names and generic words

### Funding Amount
- Normalizes to format: `{number}M {CURRENCY}`
- Handles multilingual patterns (EN/DE/FR)
- Returns "undisclosed" for unspecified amounts

### Funding Round
- Maps to standardized taxonomy:
  - Pre-Seed, Seed, Seed Extension
  - Series A/B/C/D+
  - Strategic Investment, Grant, Award, Debt
- Preserves original text in `funding_round_raw`

### Location
- Extracts city from multilingual patterns
- Auto-maps to canton codes (ZH, GE, VD, etc.)
- Supports 17 Swiss cantons

### Industry Classification
- Primary taxonomy (19 categories):
  - AI/ML, HealthTech, BioTech, MedTech
  - FinTech, CleanTech, DeepTech, Robotics
  - And 11 more...
- Sub-industry (70+ segments)
- Based on product/customer, not article topic

### Business Model
- 7 types: B2B-SaaS, B2B-Hardware, B2B-Services, B2B2C, B2C, Marketplace, Deep Tech/IP
- Determined by: who pays, what's delivered, channel

### Keywords
- **Primary**: Core technologies built by company
- **Secondary**: Adjacent/integrated technologies
- 80+ canonical keywords from enhanced_keywords_v6.py

## Quality Assurance

Run quality analysis after extraction:

```bash
python3 9_quality_analysis.py
```

**Reports**:
- Completeness rates per field
- Funding distribution (amounts, rounds, investors)
- Location heatmap (cantons, cities)
- Industry breakdown
- Keyword frequency
- Data quality issues

## Example Results

**Completeness (typical)**:
- Startup Name: 95%+
- Funding Amount: 80-90%
- Industry: 95%+
- City: 85-90%
- Keywords: 90%+

**Speed**:
- ~3-5 seconds per article
- 50 articles: ~3-5 minutes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not set | `export OPENAI_API_KEY='sk-...'` |
| Rate limit | Increase `RATE_LIMIT_DELAY` |
| Import error | `pip install --upgrade openai` |
| Interrupted | Run again - auto-resumes |

## Advanced Usage

### Custom Fields

Add to prompt template in `build_extraction_prompt()`:

```python
"new_field"
  Instructions for extraction...
  Return format: ...
```

### Different Model

Edit configuration:

```python
MODEL = 'gpt-3.5-turbo'  # Faster, cheaper, less accurate
# or
MODEL = 'gpt-4-turbo'  # Slower, more expensive, most accurate
```

### Filter Articles

Process specific year:

```python
# In process_all_articles(), after loading:
articles = [a for a in articles if a['year'] == 2026]
```

### Export to Different Format

After extraction:

```python
import pandas as pd
df = pd.read_csv('data/startupticker_analyzed_v8.csv')

# JSON
df.to_json('output.json', orient='records', indent=2)

# Excel
df.to_excel('output.xlsx', index=False)

# Parquet
df.to_parquet('output.parquet')
```

## Next Steps

After extraction, you can:

1. **Merge with other datasets**
   ```python
   df1 = pd.read_csv('startupticker_analyzed_v8.csv')
   df2 = pd.read_csv('other_source.csv')
   merged = pd.merge(df1, df2, on='startup_name', how='outer')
   ```

2. **Build visualizations**
   - Funding trends over time
   - Geographic distribution
   - Industry breakdown
   - Investor network

3. **Machine learning**
   - Predict funding success
   - Classify industries
   - Extract patterns

4. **Database import**
   - PostgreSQL
   - MySQL
   - MongoDB

## Resources

- **OpenAI Docs**: https://platform.openai.com/docs
- **API Pricing**: https://openai.com/pricing
- **Usage Dashboard**: https://platform.openai.com/usage

## Support

Check these in order:

1. **Log file**: `llm_analyzer_v8.log`
2. **Test setup**: `python3 test_llm_setup.py`
3. **README**: `LLM_ANALYZER_README.md`
4. **API Status**: https://status.openai.com/

---

**Created by**: Data2Dollar Team  
**Date**: April 2026  
**Version**: 8.0
