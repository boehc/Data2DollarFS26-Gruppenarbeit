# 🚀 Quick Start Guide - LLM Article Analyzer

## Step 1: Install Dependencies (1 minute)

```bash
pip install openai pandas
```

## Step 2: Get OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

## Step 3: Set API Key

```bash
export OPENAI_API_KEY='sk-your-actual-key-here'
```

**Verify it's set:**
```bash
echo $OPENAI_API_KEY
```

## Step 4: Test Setup (30 seconds)

```bash
cd /Users/chiaraboehme/Data2Dollar/Data2Dollar\ -\ Gruppenarbeit/Data2DollarFS26-Gruppenarbeit/pfad_a_scraper
python3 test_llm_setup.py
```

You should see:
```
✅ ALL TESTS PASSED!
```

## Step 5: Run Analyzer

### Option A: Full Run (all articles)

```bash
python3 8_llm_article_analyzer.py
```

### Option B: Test Run (5 articles only)

Edit line in `8_llm_article_analyzer.py`:
```python
# After line: articles = json.load(f)
# Add:
articles = articles[:5]  # Test with 5 articles
```

Then run:
```bash
python3 8_llm_article_analyzer.py
```

## What You'll See

```
🚀 LLM ARTICLE ANALYZER - STARTING
📥 Loading articles from: data/startupticker_articles_for_llm.json
   Found 50 articles to process

📄 Processing article 1/50
   Title: Delta Labs raises EUR 4.4 million...
✅ Extracted: Delta Labs AG
   Industry: AI/ML
   Funding: 4.4M EUR

📄 Processing article 2/50
   Title: UBS makes a strategic investment...
✅ Extracted: Artificialy SA
   Industry: AI/ML
   Funding: undisclosed

💾 Checkpoint saved (10/50)
...
```

## Output Files

After completion:

- **Main output**: `data/startupticker_analyzed_v8.csv`
- **Log file**: `llm_analyzer_v8.log`

## View Results

```bash
# Count rows
wc -l data/startupticker_analyzed_v8.csv

# View first few rows
head -5 data/startupticker_analyzed_v8.csv

# Open in Excel/Numbers
open data/startupticker_analyzed_v8.csv
```

## Analyze Results

```python
import pandas as pd

df = pd.read_csv('data/startupticker_analyzed_v8.csv')

# Basic stats
print(f"Total startups: {len(df)}")
print(f"With funding: {df['funding_amount'].notna().sum()}")

# Top industries
print(df['industry'].value_counts().head(10))

# Top cities
print(df['city'].value_counts().head(10))

# Funding rounds
print(df['funding_round'].value_counts())
```

## Cost Estimate

**For ~50 articles with GPT-4o**: ~$0.50 - $1.00

Check your usage: https://platform.openai.com/usage

## Troubleshooting

### ❌ "OPENAI_API_KEY not set"

```bash
# Set it again
export OPENAI_API_KEY='your-key-here'

# Verify
echo $OPENAI_API_KEY
```

### ❌ "Import openai could not be resolved"

```bash
pip install --upgrade openai
```

### ❌ "Rate limit exceeded"

Wait a minute, then increase delay in script:
```python
RATE_LIMIT_DELAY = 2.0  # Increase from 1.0
```

### ⚠️ Process interrupted

Just run again - it resumes automatically from checkpoint!

## Need Help?

1. Check `llm_analyzer_v8.log` for errors
2. Read full docs: `LLM_ANALYZER_README.md`
3. Verify API credits: https://platform.openai.com/usage

---

**Ready? Let's go! 🚀**

```bash
# Full command sequence:
pip install openai pandas
export OPENAI_API_KEY='your-key-here'
python3 test_llm_setup.py
python3 8_llm_article_analyzer.py
```
