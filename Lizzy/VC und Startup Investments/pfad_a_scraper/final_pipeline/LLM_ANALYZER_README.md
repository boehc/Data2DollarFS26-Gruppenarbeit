# 🤖 LLM Article Analyzer - Comprehensive Data Extraction

## Overview

This script uses **OpenAI GPT-4** to analyze startup articles and extract comprehensive structured data including:

- **Basic Info**: Startup name, publication date, year
- **Funding Data**: Amount, round type, investors
- **Location**: City, canton
- **Company Details**: Founded year, employees, website
- **Classification**: Industry, sub-industry, business model type
- **Keywords**: Primary & secondary technology keywords

## Setup

### 1. Install Dependencies

```bash
pip install openai pandas
```

### 2. Set OpenAI API Key

You need an OpenAI API key. Get one at: https://platform.openai.com/api-keys

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

**Option B: Add to your shell profile**
Add to `~/.bash_profile` or `~/.zshrc`:
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

Then reload:
```bash
source ~/.bash_profile  # or ~/.zshrc
```

### 3. Verify Setup

Test that everything is configured correctly:

```bash
python3 test_llm_setup.py
```

## Usage

### Basic Run

Process all articles:

```bash
cd /Users/chiaraboehme/Data2Dollar/Data2Dollar\ -\ Gruppenarbeit/Data2DollarFS26-Gruppenarbeit/pfad_a_scraper
python3 8_llm_article_analyzer.py
```

### Resume from Checkpoint

If the process is interrupted, simply run it again. It will automatically resume from where it left off using the checkpoint file.

### Monitor Progress

The script logs progress to:
- **Console**: Real-time updates
- **Log file**: `llm_analyzer_v8.log`

```bash
# Watch progress in real-time
tail -f llm_analyzer_v8.log
```

## Configuration

Edit these variables in `8_llm_article_analyzer.py`:

```python
# Model Selection
MODEL = 'gpt-4o'  # Options: 'gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'

# Processing Speed
BATCH_SIZE = 10  # Save checkpoint every N articles
RATE_LIMIT_DELAY = 1.0  # Seconds between API calls

# Quality vs Speed
TEMPERATURE = 0.1  # Lower = more consistent (0.0 - 1.0)
MAX_TOKENS = 2000  # Max response length
```

### Model Comparison

| Model | Quality | Speed | Cost/1K tokens |
|-------|---------|-------|----------------|
| `gpt-4o` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $2.50 in / $10 out |
| `gpt-4-turbo` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $10 in / $30 out |
| `gpt-3.5-turbo` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0.50 in / $1.50 out |

**Recommendation**: Use `gpt-4o` for best quality/speed/cost balance.

## Output

### Output File
`data/startupticker_analyzed_v8.csv`

### Columns

```
startup_name              - Company legal name (e.g., "Delta Labs AG")
publication_date          - Article date (YYYY-MM-DD)
year                      - Publication year
funding_amount            - Normalized amount (e.g., "4.4M EUR")
funding_round_raw         - Original text (e.g., "seed round")
funding_round             - Standardized (e.g., "Seed")
investor_names            - Comma-separated investors
city                      - Headquarters city
canton                    - 2-letter canton code (ZH, GE, VD, etc.)
founded_year              - Year company was founded
employees                 - Current headcount
website                   - Company website
location                  - Usually "Switzerland"
industry                  - Main category (AI/ML, FinTech, etc.)
sub_industry              - Specific segments (Applied AI, etc.)
business_model_type       - B2B-SaaS, B2C, etc.
primary_keywords          - Core technologies
secondary_keywords        - Adjacent technologies
article_id                - Original article ID
article_url               - Source URL
article_title             - Article headline
```

## Cost Estimation

**For ~50 articles with GPT-4o:**
- Average article length: ~500 words (750 tokens)
- Average prompt size: ~3,000 tokens
- Average response: ~500 tokens
- **Total cost**: ~$0.50 - $1.00

**For all articles in dataset:**
- Count articles: 
  ```bash
  python3 -c "import json; print(len(json.load(open('data/startupticker_articles_for_llm.json'))))"
  ```
- Estimated cost = (article_count / 50) × $1.00

## Examples

### Example Extraction

**Article**: "Delta Labs raises EUR 4.4 million..."

**Extracted Data**:
```json
{
  "startup_name": "Delta Labs AG",
  "funding_amount": "4.4M EUR",
  "funding_round": "Seed",
  "investor_names": "Cusp Capital, Auxxo Female Catalyst Fund",
  "city": "Zurich",
  "canton": "ZH",
  "founded_year": 2022,
  "industry": "AI/ML",
  "sub_industry": "Applied AI, Simulation",
  "business_model_type": "B2B-SaaS",
  "primary_keywords": "AI, GenAI",
  "secondary_keywords": "Enterprise"
}
```

## Troubleshooting

### Issue: "OPENAI_API_KEY not set"

**Solution**: 
```bash
export OPENAI_API_KEY='your-key-here'
echo $OPENAI_API_KEY  # Verify it's set
```

### Issue: "Rate limit exceeded"

**Solution**: Increase `RATE_LIMIT_DELAY`:
```python
RATE_LIMIT_DELAY = 2.0  # Increase delay between calls
```

### Issue: "Invalid JSON response"

**Solution**: The script has automatic retry logic. If it persists:
1. Check if your API key has sufficient credits
2. Try a more stable model like `gpt-4-turbo`

### Issue: Process interrupted

**Solution**: Just run the script again. It automatically resumes from the checkpoint file.

## Advanced Usage

### Process Specific Date Range

Edit the script to filter articles:

```python
# In process_all_articles(), after loading articles:
articles = [a for a in articles if a['year'] == 2026]
```

### Test on Sample

Process just 5 articles first:

```python
# In process_all_articles(), after loading articles:
articles = articles[:5]  # First 5 only
```

### Custom Prompt

Modify the prompt in `build_extraction_prompt()` to:
- Add new fields
- Change extraction logic
- Adjust keyword categories

## Quality Checks

After processing, run quality checks:

```python
import pandas as pd

df = pd.read_csv('data/startupticker_analyzed_v8.csv')

# Check completeness
print("Completeness rates:")
print(f"Startup names: {df['startup_name'].notna().sum() / len(df) * 100:.1f}%")
print(f"Funding amounts: {df['funding_amount'].notna().sum() / len(df) * 100:.1f}%")
print(f"Industries: {df['industry'].notna().sum() / len(df) * 100:.1f}%")
print(f"Cities: {df['city'].notna().sum() / len(df) * 100:.1f}%")

# Check industry distribution
print("\nTop industries:")
print(df['industry'].value_counts().head(10))

# Find articles with missing critical data
missing_name = df[df['startup_name'].isna()]
print(f"\n{len(missing_name)} articles without startup name")
```

## Files Generated

- `data/startupticker_analyzed_v8.csv` - Main output file
- `llm_analyzer_v8.log` - Processing log
- `data/llm_analyzer_checkpoint_v8.json` - Checkpoint (deleted after completion)

## Support

For issues or questions:
1. Check the log file for detailed error messages
2. Verify API key and credits
3. Test with a smaller sample first
4. Review the prompt template for customization

---

**Ready to start?**

```bash
# 1. Set API key
export OPENAI_API_KEY='your-key-here'

# 2. Test setup
python3 test_llm_setup.py

# 3. Run analyzer
python3 8_llm_article_analyzer.py
```
