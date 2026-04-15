# 🚀 Quick Start Guide — CSV Analysis Files

**You have 15 CSV files ready for analysis!**

---

## ⚡ 30-SECOND START

### Step 1: Open This File First
```
INVESTMENT_RECOMMENDATIONS.csv
```
This shows you STRONG BUY / BUY / HOLD / AVOID for each industry.

### Step 2: Quick Validation
```
TOP_WINNERS_LOSERS.csv
```
Confirms who's winning (BioTech, Robotics, GenAI) and losing (ClimateTech).

### Step 3: Done!
You now know where to focus in 2026. 🎯

---

## 📊 OPEN IN EXCEL/GOOGLE SHEETS

### Import Instructions

**Excel:**
1. Open Excel
2. File → Open → Select any `.csv` file
3. Data will auto-format
4. Create PivotTables / Charts as needed

**Google Sheets:**
1. Open Google Sheets
2. File → Import → Upload file
3. Choose "Comma" as separator
4. Import data
5. Use built-in charting

**Recommended First Files:**
- `INVESTMENT_RECOMMENDATIONS.csv` — Decision support
- `TOP5_PER_YEAR.csv` — Leadership over time
- `SIMPLE_SUMMARY.csv` — One-page overview

---

## 🐍 OPEN IN PYTHON

### Quick Analysis Script
```python
import pandas as pd

# Load investment recommendations
df = pd.read_csv('output/industry_trends/INVESTMENT_RECOMMENDATIONS.csv')

# Show STRONG BUY recommendations
strong_buy = df[df['recommendation'].str.contains('STRONG BUY')]
print("🚀 STRONG BUY Industries:")
print(strong_buy[['keyword', 'momentum_pct', 'market_share_2025']])

# Load winners/losers
winners = pd.read_csv('output/industry_trends/TOP_WINNERS_LOSERS.csv')
print("\n🏆 Top 3 Winners:")
print(winners.head(3))

# Load funding analysis
funding = pd.read_csv('output/industry_trends/FUNDING_ANALYSIS.csv')
print("\n💰 Industries with Largest Average Deals:")
print(funding.nlargest(3, 'avg_funding_chf')[['keyword', 'avg_funding_chf']])
```

---

## 📈 CREATE CHARTS

### Recommended Visualizations

#### 1. Winners vs Losers Bar Chart
```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('output/industry_trends/TOP_WINNERS_LOSERS.csv')

plt.figure(figsize=(12, 6))
colors = ['green' if x > 0 else 'red' for x in df['change_pp']]
plt.barh(df['keyword'], df['change_pp'], color=colors)
plt.xlabel('Market Share Change (percentage points)')
plt.title('Industry Winners & Losers (2023-2025)')
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
plt.tight_layout()
plt.savefig('winners_losers.png')
plt.show()
```

#### 2. Quarterly Trend Line Chart
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output/industry_trends/F1_deal_count_quarterly.csv', index_col=0)

# Plot top 5 industries
top_industries = ['FinTech', 'BioTech', 'ClimateTech', 'GenAI', 'Robotics']

plt.figure(figsize=(14, 6))
for industry in top_industries:
    if industry in df.columns:
        plt.plot(df.index, df[industry], marker='o', label=industry, linewidth=2)

plt.xlabel('Quarter')
plt.ylabel('Number of Deals')
plt.title('Deal Count Trend by Quarter (Top 5 Industries)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('quarterly_trends.png')
plt.show()
```

#### 3. Bubble Chart (Market Share vs Momentum)
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output/industry_trends/E_industry_classification.csv', index_col=0)

plt.figure(figsize=(12, 8))
colors = {'Emerging  🌱': 'green', 'Growing   ↑': 'lightgreen', 
          'Stable    →': 'gray', 'Slowing   ↓': 'orange', 'Declining 📉': 'red'}

for category in colors.keys():
    subset = df[df['classification'] == category]
    plt.scatter(subset['share_2025'], subset['momentum_pct'], 
                s=subset['share_2025']*20, alpha=0.6, 
                color=colors[category], label=category)

for idx, row in df.iterrows():
    plt.annotate(idx, (row['share_2025'], row['momentum_pct']), 
                 fontsize=9, alpha=0.8)

plt.xlabel('Market Share 2025 (%)')
plt.ylabel('Momentum (%)')
plt.title('Industry Classification: Market Share vs Momentum')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('bubble_chart.png')
plt.show()
```

---

## 🔍 ANSWER SPECIFIC QUESTIONS

### Q: Which industry should I start a company in?
**File:** `INVESTMENT_RECOMMENDATIONS.csv`  
**Look for:** "STRONG BUY" recommendations  
**Answer:** GenAI or Robotics

### Q: Who are the top 5 industries right now?
**File:** `TOP5_PER_YEAR.csv`  
**Filter:** year == 2025  
**Answer:** FinTech, BioTech, ClimateTech, MedTech, GenAI/Robotics (tied)

### Q: Which industry has the biggest deals?
**File:** `FUNDING_ANALYSIS.csv`  
**Sort by:** `avg_funding_chf` descending  
**Answer:** BioTech (large deals), then MedTech

### Q: What's accelerating fastest right now?
**File:** `MOMENTUM_LEADERS.csv`  
**Sort by:** `momentum_pct` descending  
**Answer:** GenAI (+168%), Robotics (+109%)

### Q: What happened to ClimateTech?
**File:** `TOP_WINNERS_LOSERS.csv`  
**Look at:** ClimateTech row  
**Answer:** Lost 7.1 percentage points (16.9% → 9.8%), biggest loser

### Q: Is FinTech still relevant?
**File:** `SIMPLE_SUMMARY.csv` or `YEARLY_COMPARISON.csv`  
**Look at:** FinTech metrics  
**Answer:** Still largest (36%) but momentum declining (-12%)

### Q: What about the last few quarters?
**File:** `RECENT_QUARTERS_TREND.csv`  
**Look at:** direction column  
**Answer:** GenAI ↑ Rising, ClimateTech ↓ Falling

---

## 💡 PRO TIPS

### Tip 1: Use Multiple Files Together
Don't rely on just one file. Cross-reference:
- Check `INVESTMENT_RECOMMENDATIONS.csv` for decision
- Validate with `MOMENTUM_LEADERS.csv` for current trend
- Confirm with `TOP_WINNERS_LOSERS.csv` for historical context

### Tip 2: Focus on Recent Data
2026 data is incomplete (only 2 quarters). Focus on:
- 2023-2025 for year-over-year comparisons
- Last 4 quarters for momentum analysis

### Tip 3: Watch the Signals
**File:** `C_funding_share_pct.csv`  
**Column:** `signal`
- "Grosse Deals ↑" = Funding growing faster than deals → Quality
- "Viele Deals ↑" = Deals growing faster than funding → Quantity

### Tip 4: Classifications Matter
**File:** `E_industry_classification.csv`
- Emerging 🌱 = High risk, high reward
- Growing ↑ = Solid growth, moderate risk
- Stable → = Safe but not exciting
- Slowing ↓ = Mature or declining
- Declining 📉 = Avoid

### Tip 5: Context is Key
A small industry (1-2%) growing fast (+100% momentum) is different from
a large industry (30%) growing slowly (+5% momentum).

Check both:
- Absolute size (`market_share_2025`)
- Growth rate (`momentum_pct`)

---

## 🎯 USE CASES BY ROLE

### For Founders
1. Open `INVESTMENT_RECOMMENDATIONS.csv`
2. Look for STRONG BUY or BUY
3. Check `MOMENTUM_LEADERS.csv` to confirm acceleration
4. Read `FUNDING_ANALYSIS.csv` to understand deal sizes
5. **Decision:** Pick an Emerging/Growing industry with strong momentum

### For Investors (VC)
1. Open `FUNDING_ANALYSIS.csv` to see deal economics
2. Check `INVESTMENT_RECOMMENDATIONS.csv` for signals
3. Review `YEARLY_COMPARISON.csv` for consistency
4. Look at `TOP5_PER_YEAR.csv` to validate market size
5. **Decision:** Build portfolio with mix of Emerging + Growing

### For Consultants
1. Open `SIMPLE_SUMMARY.csv` for client overview
2. Use `TOP_WINNERS_LOSERS.csv` in presentations
3. Reference `YEARLY_COMPARISON.csv` for trends
4. Show `MOMENTUM_LEADERS.csv` for current dynamics
5. **Deliverable:** Data-driven industry report

### For Researchers
1. Start with `E_industry_classification.csv` (master file)
2. Analyze `F1_deal_count_quarterly.csv` for patterns
3. Compare `A_market_share_pct.csv` with `C_funding_share_pct.csv`
4. Study `MOMENTUM_LEADERS.csv` for methodology
5. **Output:** Academic paper on market dynamics

---

## 📱 MOBILE-FRIENDLY OPTIONS

### Google Sheets (Mobile)
1. Upload CSV files to Google Drive
2. Open with Google Sheets app
3. View/edit on phone or tablet
4. Share with team

### Excel Mobile
1. Upload to OneDrive
2. Open with Excel mobile app
3. View/filter data
4. Create simple charts

### CSV Viewer Apps
- **iOS:** CSV Touch, TableFlip
- **Android:** CSV Reader, Simple Spreadsheet

---

## 🔗 FILE RELATIONSHIPS

```
SIMPLE_SUMMARY.csv
    ↓ (detailed classification)
E_industry_classification.csv
    ↓ (breakdown)
    ├─→ A_market_share_pct.csv (market share data)
    ├─→ D_momentum.csv (momentum data)
    └─→ INVESTMENT_RECOMMENDATIONS.csv (actionable output)

YEARLY_COMPARISON.csv
    ↓ (quarterly breakdown)
F1_deal_count_quarterly.csv + F2_deal_share_quarterly.csv
    ↓ (recent focus)
RECENT_QUARTERS_TREND.csv

FUNDING_ANALYSIS.csv
    ↓ (distribution over time)
C_funding_share_pct.csv

TOP_WINNERS_LOSERS.csv
    ↓ (year-by-year detail)
TOP5_PER_YEAR.csv
    ↓ (ranking evolution)
B_rankings_by_year.csv
```

---

## ⚠️ IMPORTANT NOTES

### Data Limitations
- ✅ 2023-2025: Complete data, reliable
- ⚠️ 2026: Only 2 quarters (Q1, Q2), incomplete
- ✅ Funding: 62% of deals have funding data
- ⚠️ Small industries (SpaceTech, EdTech): High volatility

### When to Update
- Quarterly: After each quarter ends
- Annually: Full year review
- Ad-hoc: When major market shifts occur

### File Versions
Current files are based on:
- **Input:** `startups_classified_v2.csv`
- **Date:** April 2026
- **Quarters:** 2023-Q1 to 2026-Q2 (14 quarters)

---

## 🎉 YOU'RE READY!

### Minimum Viable Analysis (5 minutes)
1. Open `INVESTMENT_RECOMMENDATIONS.csv`
2. Sort by `recommendation`
3. Done ✅

### Standard Analysis (30 minutes)
1. `INVESTMENT_RECOMMENDATIONS.csv` → Decisions
2. `TOP_WINNERS_LOSERS.csv` → Context
3. `SIMPLE_SUMMARY.csv` → Overview
4. `MOMENTUM_LEADERS.csv` → Current state
5. Done ✅

### Deep Dive (2 hours)
1. All files above
2. `YEARLY_COMPARISON.csv` → Historical patterns
3. `FUNDING_ANALYSIS.csv` → Economics
4. `F1_deal_count_quarterly.csv` → Time series
5. Create charts in Excel/Python
6. Write report
7. Done ✅

---

**Happy Analyzing! 🚀**

For questions or issues, refer to:
- `CSV_FILES_INDEX.md` — Detailed file descriptions
- `README.md` — Technical methodology
- `ANALYSIS_SUMMARY.md` — Key findings
- `EXECUTIVE_SUMMARY.md` — One-page overview
