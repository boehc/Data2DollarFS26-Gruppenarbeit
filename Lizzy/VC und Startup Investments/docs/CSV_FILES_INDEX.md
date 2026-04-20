# 📊 Industry Trends — CSV Files Index

**Total Files:** 15 CSV files + 4 documentation files  
**Last Updated:** 6. April 2026

---

## 🎯 QUICK NAVIGATION

### For Quick Decisions (Start Here!)
1. **INVESTMENT_RECOMMENDATIONS.csv** ⭐ — Buy/Hold/Avoid for each industry
2. **TOP_WINNERS_LOSERS.csv** ⭐ — Quick ranking of winners and losers
3. **SIMPLE_SUMMARY.csv** ⭐ — One-page overview of all industries

### For Deep Analysis
4. **E_industry_classification.csv** — Complete classification with all metrics
5. **YEARLY_COMPARISON.csv** — Year-over-year metrics side by side
6. **MOMENTUM_LEADERS.csv** — Industries ranked by acceleration

### For Specific Questions
7. **TOP5_PER_YEAR.csv** — Who dominated each year?
8. **FUNDING_ANALYSIS.csv** — Who gets the biggest deals?
9. **RECENT_QUARTERS_TREND.csv** — What's happening RIGHT NOW?

### Raw Data for Charts
10. **A_market_share_pct.csv** — Market share percentages
11. **B_rankings_by_year.csv** — Rankings 2023-2026
12. **C_funding_share_pct.csv** — Funding distribution
13. **D_momentum.csv** — Momentum calculations
14. **F1_deal_count_quarterly.csv** — Quarterly deal counts
15. **F2_deal_share_quarterly.csv** — Quarterly percentages

---

## 📋 DETAILED FILE DESCRIPTIONS

### 1️⃣ INVESTMENT_RECOMMENDATIONS.csv ⭐⭐⭐
**Use Case:** "Where should I focus my efforts in 2026?"

**Columns:**
- `keyword` — Industry name
- `classification` — Emerging/Growing/Stable/Slowing/Declining
- `market_share_2025` — Current market size (%)
- `momentum_pct` — Acceleration rate
- `share_change` — Change 2023→2025
- `recommendation` — Clear action: STRONG BUY / BUY / HOLD / AVOID / SELL

**Example Row:**
```
GenAI, Emerging 🌱, 4.1%, +168%, +2.3pp, STRONG BUY - High Growth
```

**Best For:** Founders, investors, accelerators deciding where to focus

---

### 2️⃣ TOP_WINNERS_LOSERS.csv ⭐⭐⭐
**Use Case:** "Who's winning and who's losing?"

**Columns:**
- `keyword` — Industry name
- `share_2023` — Market share in 2023
- `share_2025` — Market share in 2025
- `change_pp` — Change in percentage points
- `direction` — '+' / '-' / '='
- `category` — WINNER 🏆 / LOSER 📉 / NEUTRAL →

**Example Rows:**
```
BioTech,    27.7%, 30.9%, +3.2pp, +, WINNER 🏆
ClimateTech, 16.9%, 9.8%, -7.1pp, -, LOSER 📉
```

**Best For:** Quick executive summary, presentations

---

### 3️⃣ SIMPLE_SUMMARY.csv ⭐⭐⭐
**Use Case:** "Give me everything on one page"

**Columns:**
- `keyword` — Industry name
- `total_deals_2023_2026` — Total deals over 4 years
- `deals_2023` — Deals in 2023
- `deals_2025` — Deals in 2025
- `growth_2023_2025` — Absolute change
- `classification` — Category
- `momentum_pct` — Acceleration
- `market_share_2025` — Current size

**Best For:** Overview, comparing multiple metrics at once

---

### 4️⃣ E_industry_classification.csv ⭐⭐
**Use Case:** "Show me the complete analysis"

**Columns:**
- `keyword` — Industry
- `share_2023` — Starting point
- `share_2025` — Current state
- `share_change_pct` — Change
- `momentum_pct` — Acceleration
- `classification` — Final category

**This is the MASTER classification file** — combines market share + momentum

**Best For:** Academic analysis, detailed reports

---

### 5️⃣ YEARLY_COMPARISON.csv ⭐⭐
**Use Case:** "How did each year compare?"

**Columns:**
- `deals_2023`, `deals_2024`, `deals_2025`, `deals_2026` — Absolute counts
- `share_pct_2023`, `share_pct_2024`, etc. — Percentages
- `deals_change_2023_2024` — Year-over-year changes
- `deals_change_2024_2025` — Next year's change

**Best For:** Spotting year-over-year patterns, seasonality

---

### 6️⃣ MOMENTUM_LEADERS.csv ⭐⭐
**Use Case:** "Who's accelerating fastest RIGHT NOW?"

**Columns:**
- `earlier_avg` — Avg deals in first 4 quarters
- `recent_avg` — Avg deals in last 4 quarters
- `momentum_pct` — % change
- `classification` — Accelerating/Growing/Stable/Slowing/Declining
- `rank` — 1 = highest momentum
- `interpretation` — Plain English description

**Example:**
```
GenAI, 1.8, 5.0, +168%, Accelerating 🚀, Rank 1, "Explosive Growth"
```

**Best For:** Understanding current dynamics, not just historical

---

### 7️⃣ TOP5_PER_YEAR.csv ⭐
**Use Case:** "Who were the top 5 each year?"

**Columns:**
- `year` — 2023/2024/2025/2026
- `rank` — 1-5
- `keyword` — Industry
- `deals` — Number of deals
- `market_share_pct` — % of all deals

**Example:**
```
2023, 1, FinTech,    146, 36.8%
2023, 2, BioTech,    110, 27.7%
2025, 1, FinTech,    151, 36.1%
2025, 2, BioTech,    129, 30.9%
2025, 5, GenAI,       17,  4.1%  ← New entrant!
```

**Best For:** Tracking leadership changes, spotting newcomers

---

### 8️⃣ FUNDING_ANALYSIS.csv ⭐
**Use Case:** "Who gets the big money?"

**Columns:**
- `deals_with_funding` — How many deals have funding data
- `total_funding_chf` — Total CHF raised
- `avg_funding_chf` — Average deal size
- `median_funding_chf` — Median (less affected by outliers)
- `pct_of_total_funding` — % of all funding
- `avg_deal_size` — Large/Medium/Small

**Key Insight:** BioTech has 31% of deals but 58% of funding → Large deals!

**Best For:** Investors, understanding deal sizes

---

### 9️⃣ RECENT_QUARTERS_TREND.csv
**Use Case:** "What's the trend in the last 4 quarters?"

**Columns:**
- 4 most recent quarter columns (e.g., 2025-Q3, 2025-Q4, 2026-Q1, 2026-Q2)
- `avg_per_quarter` — Average deals per quarter
- `trend` — % change (first 2 quarters vs last 2 quarters)
- `direction` — ↑ Rising / ↓ Falling / → Stable

**Best For:** Short-term trends, understanding recent shifts

---

### 🔟 A_market_share_pct.csv
**Use Case:** Raw data for "Market Share Shift" analysis

**Columns:** Year columns (2023-2026) + share_change_pct + direction

**Best For:** Creating market share charts

---

### 1️⃣1️⃣ B_rankings_by_year.csv
**Use Case:** Raw data for "Who's climbing/falling?"

**Columns:** rank_2023, rank_2024, rank_2025, rank_2026, rank_change, trend

**Best For:** Creating ranking evolution charts

---

### 1️⃣2️⃣ C_funding_share_pct.csv
**Use Case:** Raw data for "Funding distribution shift"

**Columns:** Year columns + funding_change_pp + deal_share_change + signal

**Best For:** Understanding deal size vs deal count dynamics

---

### 1️⃣3️⃣ D_momentum.csv
**Use Case:** Raw data for "Acceleration calculation"

**Columns:** earlier_avg, recent_avg, momentum_pct, classification

**Best For:** Understanding momentum methodology

---

### 1️⃣4️⃣ F1_deal_count_quarterly.csv
**Use Case:** Raw quarterly data (absolute counts)

**Columns:** 14 quarter columns + TOTAL

**Best For:** Time series charts, detailed quarterly analysis

---

### 1️⃣5️⃣ F2_deal_share_quarterly.csv
**Use Case:** Raw quarterly data (percentages)

**Columns:** 14 quarter columns (each row sums to 100%) + TOTAL

**Best For:** Stacked area charts, composition over time

---

## 🎓 RECOMMENDED WORKFLOWS

### For Founders: "Where should I build my startup?"
1. Start with **INVESTMENT_RECOMMENDATIONS.csv**
2. Look for "STRONG BUY" or "BUY" recommendations
3. Check **MOMENTUM_LEADERS.csv** to see current acceleration
4. Verify with **TOP_WINNERS_LOSERS.csv** to confirm trends
5. Decision: Focus on Emerging/Growing industries

**Result:** GenAI and Robotics are your best bets in 2026

---

### For Investors: "Where should I deploy capital?"
1. Start with **FUNDING_ANALYSIS.csv** to understand deal sizes
2. Check **INVESTMENT_RECOMMENDATIONS.csv** for signals
3. Use **YEARLY_COMPARISON.csv** to see historical patterns
4. Review **RECENT_QUARTERS_TREND.csv** for current momentum
5. Decision: Diversify across Emerging (high risk/reward) + Growing (safer)

**Result:** GenAI/Robotics (early stage) + BioTech (late stage)

---

### For Researchers: "What are the market dynamics?"
1. Start with **E_industry_classification.csv** (master file)
2. Dig into **YEARLY_COMPARISON.csv** for patterns
3. Analyze **F1/F2_deal_count_quarterly.csv** for seasonality
4. Compare **A_market_share_pct.csv** with **C_funding_share_pct.csv**
5. Check **MOMENTUM_LEADERS.csv** for acceleration dynamics

**Result:** Comprehensive understanding of market shifts

---

### For Executives: "Give me the highlights"
1. Read **EXECUTIVE_SUMMARY.md** (markdown document)
2. Open **TOP_WINNERS_LOSERS.csv** (1-page view)
3. Glance at **TOP5_PER_YEAR.csv** (who dominated when)
4. Check **SIMPLE_SUMMARY.csv** for complete overview
5. Decision: Ready for board presentation

**Result:** Clear strategic direction in 5 minutes

---

### For Accelerators: "What should our thesis be?"
1. **INVESTMENT_RECOMMENDATIONS.csv** → Focus areas
2. **MOMENTUM_LEADERS.csv** → Current hot topics
3. **RECENT_QUARTERS_TREND.csv** → What's working NOW
4. **TOP5_PER_YEAR.csv** → Market size validation
5. Decision: Batch composition (50% Emerging, 30% Growing, 20% Stable)

**Result:** Data-driven accelerator strategy

---

## 📈 VISUALIZATION IDEAS

### Must-Have Charts
1. **Line Chart:** F1_deal_count_quarterly.csv → Show quarterly evolution
2. **Bar Chart:** TOP_WINNERS_LOSERS.csv → Winners vs Losers
3. **Bubble Chart:** E_industry_classification.csv → Market Share (x) vs Momentum (y), Size = Funding
4. **Stacked Area:** F2_deal_share_quarterly.csv → Composition over time
5. **Table:** INVESTMENT_RECOMMENDATIONS.csv → Decision matrix

### Advanced Charts
6. **Heatmap:** YEARLY_COMPARISON.csv → Year-over-year changes
7. **Sankey Diagram:** TOP5_PER_YEAR.csv → Ranking flows 2023→2026
8. **Scatter Plot:** FUNDING_ANALYSIS.csv → Deal count vs Avg size
9. **Waterfall Chart:** A_market_share_pct.csv → Market share changes

---

## 🔍 KEY INSIGHTS BY FILE

### INVESTMENT_RECOMMENDATIONS.csv
- ✅ 2 industries: STRONG BUY (GenAI, Robotics)
- ✅ 2 industries: BUY (BioTech, MedTech)
- ⚖️ 5 industries: HOLD (HealthTech, Ecommerce, PropTech, AgriTech, Cybersecurity)
- ⚠️ 5 industries: AVOID (FinTech, Enterprise, ClimateTech, EdTech, SpaceTech)

### TOP_WINNERS_LOSERS.csv
- 🏆 Winners: BioTech (+3.2pp), Robotics (+3.1pp), GenAI (+2.3pp)
- 📉 Losers: ClimateTech (-7.1pp), Enterprise (-1.8pp), SpaceTech (-0.8pp)

### MOMENTUM_LEADERS.csv
- 🚀 Explosive: GenAI (+168%), Robotics (+109%)
- 💀 Collapsing: SpaceTech (-89%), EdTech (-67%), ClimateTech (-47%)

### FUNDING_ANALYSIS.csv
- 💰 BioTech: 58% of all funding with only 31% of deals → LARGE DEALS
- 📊 FinTech: 22% of funding but 36% of deals → many small deals

### TOP5_PER_YEAR.csv
- 2023 Top 3: FinTech, BioTech, ClimateTech
- 2025 Top 3: FinTech, BioTech, ClimateTech (same but ClimateTech shrinking)
- 2025 Top 5 includes: GenAI and Robotics (newcomers!)

---

## 📞 SUPPORT

### File Not Loading?
- Ensure you're in the correct directory: `output/industry_trends/`
- Files are UTF-8 encoded, comma-separated
- Use Excel, Google Sheets, pandas, or any CSV viewer

### Need Different Format?
- Current: CSV (universal)
- Can generate: Excel (.xlsx), JSON, or SQL database
- Let us know your preferred format

### Want More Metrics?
Current files cover:
- ✅ Market share (deals %)
- ✅ Rankings
- ✅ Funding distribution
- ✅ Momentum/acceleration
- ✅ Classification

Additional metrics available:
- Geographic distribution (if data exists)
- Funding stage breakdown (Seed/Series A/B/C)
- Founder demographics (if data exists)
- Success rate / exit analysis

---

## 🎯 ONE-PAGE RECOMMENDATION

**If you only read ONE file, read:**  
→ **INVESTMENT_RECOMMENDATIONS.csv**

**If you only read TWO files, add:**  
→ **TOP_WINNERS_LOSERS.csv**

**If you only read THREE files, add:**  
→ **SIMPLE_SUMMARY.csv**

**These 3 files give you 80% of the insights in 5 minutes.**

---

**Last Updated:** 6. April 2026  
**Total Industries Analyzed:** 14  
**Total Data Points:** 1'327 startups across 14 quarters  
**Coverage:** 2023-Q1 to 2026-Q2
