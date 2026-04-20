# Production Code - Swiss Startup Data Pipeline

## Overview
This folder contains the production-ready data pipeline for collecting and analyzing Swiss startup ecosystem data (2023-2026).

## Pipeline Structure

### 1_data_collection/
Web scrapers for data collection:
- `1_kaggle_downloader.py` - Download base datasets from Kaggle
- `2_vclense_scraper.py` - Scrape VClense startup database
- `3_yc_scraper_v2.py` - Y Combinator startup data (FINAL version)
- `5_startupticker_scraper_v7_STEP1_ONLY.py` - StartupTicker scraper (FINAL)
- `7_venturekick_scraper_v5_STEP1_ONLY.py` - VentureKick scraper (FINAL)

### 2_data_processing/
Data cleaning and processing scripts:
- `4_merge_and_clean.py` - Merge datasets and remove duplicates
- `8_llm_article_analyzer.py` - LLM-based article content extraction
- `9_quality_analysis.py` - Data quality checks and validation
- `10_automated_llm_extraction.py` - Automated extraction pipeline
- Plus 4 helper scripts for data cleaning

### 3_analysis/
Analysis and insights:
- `step2_industry_trends.py` - Industry trend analysis (2023-2026)
- `schweiz_overview.py` - Swiss ecosystem overview

## Installation

```bash
pip install -r requirements.txt
```

## Usage

See `../docs/README_FINAL.md` for detailed usage instructions.

## Key Features
- ✅ 5 production web scrapers
- ✅ Multi-step data processing pipeline
- ✅ LLM-enhanced content extraction
- ✅ Comprehensive quality validation
- ✅ Industry trend analysis across 14 categories
- ✅ 1,327 startups analyzed (2023-2026)

**Author:** Chiara Boehme  
**Date:** April 2026

