# ✅ Data Preparation Complete - Ready for Analysis

**Date:** April 6, 2026  
**Status:** ✅ READY FOR COMBINED ANALYSIS  
**Datasets:** startups_classified_v2.csv + articles_classified_t2.csv

---

## 🎯 Mission Accomplished

### Output Files
1. **`data/startups_classified_v2.csv`** - 1,327 classified Swiss startups
2. **`prepare_startups_classification.py`** - Reproducible classification script
3. **`CLASSIFICATION_RESULTS.md`** - Detailed methodology & results

---

## 📊 Quick Stats

| Dataset | Rows | Keywords | Time Range |
|---------|------|----------|------------|
| **Startups (Chiara)** | 1,327 | 14 | 2023-Q1 to 2026-Q2 |
| **Articles (Natalie)** | 8,476 | 28 | 2023-01 to 2026-03 |

---

## ✅ Compatibility Check

### Perfect Keyword Overlap
**All 14 startup keywords** are present in Natalie's articles dataset:
- ✅ AgriTech
- ✅ BioTech  
- ✅ ClimateTech
- ✅ Cybersecurity
- ✅ Ecommerce
- ✅ EdTech
- ✅ Enterprise
- ✅ FinTech
- ✅ GenAI
- ✅ HealthTech
- ✅ MedTech
- ✅ PropTech
- ✅ Robotics
- ✅ SpaceTech

**Additional keywords** only in articles (can be used for trend context):
- AgentAI, LLM, ComputerVision, PhysicalAI, Semiconductors, QuantumTech, Web3
- CreatorEconomy, DefenseTech, DigitalHealth, GameTech, HRTech, Infrastructure, MobilityTech

---

## 🔬 Data Quality Metrics

### Startups Dataset
```
Total entries:     1,327
Complete data:     100% (all required fields)
With funding:      62.3% (827 startups)
Total funding:     CHF 40,586 Mio.
Geographic data:   Canton/City available
Time coverage:     14 quarters (3.5 years)
```

### Classification Accuracy
```
Successfully mapped:    84.8% (1,327 of 1,564)
Excluded (Other):       7.9% (127 startups)
Excluded (no match):    7.3% (110 startups - B2C logistics, etc.)
```

---

## 📈 Analysis Possibilities

### 1. Funding Trends vs. Media Coverage
- Compare startup funding amounts with article volume per keyword
- Identify hot sectors: media hype vs. actual investment

### 2. Tech Layer vs. Industry Layer
- Startups: 78 tech_layer (5.9%) vs. 1,249 industry_layer (94.1%)
- Articles: Can analyze which tech trends get most coverage

### 3. Geographic Analysis
- Swiss startups: Canton/City distribution
- Compare with article sources (TechCrunch = global, startupticker = Swiss)

### 4. Time Series Analysis
- Quarterly startup funding trends (2023-Q1 to 2026-Q2)
- Monthly article trends (2023-01 to 2026-03)
- Lead/lag relationships

### 5. Keyword Dominance
```
Startups Top 3:
  1. FinTech (35.1%)
  2. BioTech (31.2%)
  3. ClimateTech (12.7%)

Can compare with article coverage patterns
```

---

## 🚀 Next Steps - Ready to Analyze

### For Combined Analysis
```python
import pandas as pd

# Load both datasets
startups = pd.read_csv('data/startups_classified_v2.csv')
articles = pd.read_csv('path/to/articles_classified_t2.csv')

# Example: Funding vs. Article Volume
funding_by_kw = startups.groupby('keyword')['funding_chf'].sum()
# ... analyze article trends by same keywords

# Example: Time series
startups_quarterly = startups.groupby(['quarter', 'keyword']).size()
# ... compare with monthly article trends
```

### Visualization Ideas
1. **Dual-axis chart**: Funding amount + Article count per keyword
2. **Heat map**: Quarterly startup activity vs. monthly article trends
3. **Geographic map**: Swiss canton activity (startups only)
4. **Bubble chart**: Keyword size = funding, color = media coverage
5. **Time series**: Overlay startup funding rounds with article volume spikes

---

## 📝 Data Dictionary

### startups_classified_v2.csv (10 columns)
```
startup_name      str      Company name with legal form (AG/SA/GmbH)
industry          str      Original category from startupticker
keyword           str      Mapped keyword (Natalie's system)
layer_type        str      'tech_layer' or 'industry_layer'
funding_chf       float    Funding amount in CHF millions (NaN if undisclosed)
has_funding       bool     True/False funding indicator
quarter           str      Format: '2023-Q1' to '2026-Q2'
publication_date  date     ISO format YYYY-MM-DD
canton            str      Swiss canton (ZH, VD, GE, etc.)
city              str      City name
```

---

## 🎓 Methodology Notes

### Classification Logic (3-tier priority)
1. **Direct mapping** (9 categories): FinTech, BioTech, CleanTech→ClimateTech, etc.
2. **AI/ML fallback** (tag-based): GenAI, LLM, AgentAI based on article tags
3. **B2C Tech fallback** (tag-based): Ecommerce, MobilityTech, etc.

### Funding Conversion
- USD → CHF: 0.90 rate
- EUR → CHF: 0.95 rate
- Format: "10M USD" → 9.0 CHF millions
- UNDISCLOSED → NaN (excluded from totals)

### Time Normalization
- Startups: Quarterly buckets (better for sparse data)
- Articles: Monthly granularity (more data points)
- Overlap period: 2023-Q1 to 2026-Q2 (3.5 years)

---

## ⚠️ Known Limitations

1. **Missing Keywords in Startups**
   - No LLM, AgentAI (all AI/ML → GenAI due to tag limitations)
   - No MobilityTech (most B2C logistics excluded)
   - No HRTech, GameTech, etc. (not in startupticker categories)

2. **Time Granularity Mismatch**
   - Startups: Quarterly (coarser)
   - Articles: Monthly (finer)
   - Solution: Aggregate articles to quarters or keep separate scales

3. **Geographic Bias**
   - Startups: 100% Switzerland-focused
   - Articles: Mix of global (TechCrunch) + Swiss (startupticker subset)

4. **Sample Size Imbalance**
   - Some keywords have few startups (SpaceTech: 4, EdTech: 6)
   - Use percentage/normalized metrics for comparison

---

## ✨ Success Metrics

✅ **Data Quality:** 100% complete required fields  
✅ **Keyword Compatibility:** 100% overlap with articles  
✅ **Time Coverage:** 14 quarters of consistent data  
✅ **Funding Data:** 62% with amounts, CHF 40.6B total  
✅ **Classification Rate:** 85% successfully mapped  
✅ **Reproducibility:** Fully documented pipeline  

---

## 🎉 Ready for Analysis!

**Status:** All data prepared and validated  
**Compatibility:** 100% with Natalie's articles  
**Quality:** Production-ready  
**Documentation:** Complete  

**You can now:**
- Run trend analysis
- Create visualizations
- Compare media coverage with funding reality
- Identify emerging keywords
- Analyze geographic patterns

---

*Generated: April 6, 2026*  
*Script: prepare_startups_classification.py*  
*Questions? Check CLASSIFICATION_RESULTS.md for detailed methodology*
