"""
Quality Analysis Script for LLM-extracted data.
Analyzes completeness, validates data, and provides insights.
"""

import pandas as pd
import json
from datetime import datetime


INPUT_FILE = 'data/startupticker_analyzed_v8.csv'


def analyze_completeness(df):
    """Analyze field completeness rates."""
    print("="*80)
    print("📊 COMPLETENESS ANALYSIS")
    print("="*80)
    
    total = len(df)
    
    fields = {
        'startup_name': 'Startup Name',
        'funding_amount': 'Funding Amount',
        'funding_round': 'Funding Round',
        'investor_names': 'Investors',
        'city': 'City',
        'canton': 'Canton',
        'founded_year': 'Founded Year',
        'employees': 'Employees',
        'website': 'Website',
        'industry': 'Industry',
        'sub_industry': 'Sub-Industry',
        'business_model_type': 'Business Model',
        'primary_keywords': 'Primary Keywords',
        'secondary_keywords': 'Secondary Keywords'
    }
    
    print(f"\nTotal articles analyzed: {total}\n")
    print(f"{'Field':<25} {'Present':<10} {'%':<10} {'Missing':<10}")
    print("-" * 80)
    
    for field, label in fields.items():
        present = df[field].notna().sum()
        missing = total - present
        pct = (present / total * 100) if total > 0 else 0
        
        # Color coding
        status = "✅" if pct >= 80 else "⚠️" if pct >= 50 else "❌"
        
        print(f"{status} {label:<23} {present:<10} {pct:>5.1f}%   {missing:<10}")


def analyze_funding_data(df):
    """Analyze funding-related data."""
    print("\n" + "="*80)
    print("💰 FUNDING ANALYSIS")
    print("="*80)
    
    # Filter articles with funding
    funding_df = df[df['funding_amount'].notna()]
    
    print(f"\nArticles with funding data: {len(funding_df)} / {len(df)}")
    
    # Funding rounds
    if 'funding_round' in funding_df.columns:
        print("\n📈 Funding Rounds:")
        rounds = funding_df['funding_round'].value_counts()
        for round_type, count in rounds.items():
            print(f"   {round_type:<20} {count:>4}")
    
    # Funding amounts (parse numeric values)
    print("\n💵 Funding Amounts:")
    
    # Extract numeric values
    amounts = []
    currencies = []
    
    for amt in funding_df['funding_amount']:
        if pd.notna(amt) and amt != 'undisclosed':
            try:
                # Parse format like "4.4M EUR"
                parts = str(amt).split()
                if len(parts) >= 2:
                    num_str = parts[0].replace('M', '')
                    num = float(num_str)
                    currency = parts[1]
                    amounts.append(num)
                    currencies.append(currency)
            except:
                pass
    
    if amounts:
        print(f"   Total amounts parsed: {len(amounts)}")
        print(f"   Mean: {sum(amounts)/len(amounts):.2f}M")
        print(f"   Median: {sorted(amounts)[len(amounts)//2]:.2f}M")
        print(f"   Min: {min(amounts):.2f}M")
        print(f"   Max: {max(amounts):.2f}M")
        
        # Currency distribution
        from collections import Counter
        currency_counts = Counter(currencies)
        print(f"\n💱 Currencies:")
        for currency, count in currency_counts.most_common():
            print(f"   {currency}: {count}")
    
    # Top investors
    if 'investor_names' in funding_df.columns:
        print("\n🏦 Top Investors (by mentions):")
        all_investors = []
        for investors in funding_df['investor_names'].dropna():
            all_investors.extend([inv.strip() for inv in str(investors).split(',')])
        
        from collections import Counter
        investor_counts = Counter(all_investors)
        for investor, count in investor_counts.most_common(10):
            print(f"   {investor:<40} {count:>3}")


def analyze_location_data(df):
    """Analyze location distribution."""
    print("\n" + "="*80)
    print("🗺️  LOCATION ANALYSIS")
    print("="*80)
    
    # Canton distribution
    if 'canton' in df.columns:
        print("\n📍 By Canton:")
        cantons = df['canton'].value_counts()
        for canton, count in cantons.items():
            pct = count / len(df) * 100
            print(f"   {canton}: {count:>3} ({pct:>5.1f}%)")
    
    # City distribution
    if 'city' in df.columns:
        print("\n🏙️  Top Cities:")
        cities = df['city'].value_counts().head(15)
        for city, count in cities.items():
            print(f"   {city:<20} {count:>3}")


def analyze_industry_data(df):
    """Analyze industry classification."""
    print("\n" + "="*80)
    print("🏭 INDUSTRY ANALYSIS")
    print("="*80)
    
    # Main industries
    if 'industry' in df.columns:
        print("\n📊 Main Industries:")
        industries = df['industry'].value_counts()
        for industry, count in industries.items():
            pct = count / len(df[df['industry'].notna()]) * 100
            bar = "█" * int(pct / 2)
            print(f"   {industry:<20} {count:>3} ({pct:>5.1f}%) {bar}")
    
    # Sub-industries
    if 'sub_industry' in df.columns:
        print("\n🔍 Top Sub-Industries:")
        all_subs = []
        for subs in df['sub_industry'].dropna():
            all_subs.extend([s.strip() for s in str(subs).split(',')])
        
        from collections import Counter
        sub_counts = Counter(all_subs)
        for sub, count in sub_counts.most_common(15):
            print(f"   {sub:<35} {count:>3}")
    
    # Business models
    if 'business_model_type' in df.columns:
        print("\n💼 Business Models:")
        models = df['business_model_type'].value_counts()
        for model, count in models.items():
            print(f"   {model:<20} {count:>3}")


def analyze_keywords(df):
    """Analyze keyword distribution."""
    print("\n" + "="*80)
    print("🔑 KEYWORD ANALYSIS")
    print("="*80)
    
    # Primary keywords
    if 'primary_keywords' in df.columns:
        print("\n⭐ Primary Keywords:")
        all_primary = []
        for keywords in df['primary_keywords'].dropna():
            all_primary.extend([k.strip() for k in str(keywords).split(',')])
        
        from collections import Counter
        primary_counts = Counter(all_primary)
        for keyword, count in primary_counts.most_common(20):
            print(f"   {keyword:<25} {count:>3}")
    
    # Secondary keywords
    if 'secondary_keywords' in df.columns:
        print("\n➕ Secondary Keywords:")
        all_secondary = []
        for keywords in df['secondary_keywords'].dropna():
            all_secondary.extend([k.strip() for k in str(keywords).split(',')])
        
        from collections import Counter
        secondary_counts = Counter(all_secondary)
        for keyword, count in secondary_counts.most_common(20):
            print(f"   {keyword:<25} {count:>3}")


def analyze_temporal_data(df):
    """Analyze temporal patterns."""
    print("\n" + "="*80)
    print("📅 TEMPORAL ANALYSIS")
    print("="*80)
    
    # Publication year
    if 'year' in df.columns:
        print("\n📆 By Publication Year:")
        years = df['year'].value_counts().sort_index(ascending=False)
        for year, count in years.items():
            print(f"   {year}: {count:>3}")
    
    # Founded year
    if 'founded_year' in df.columns:
        print("\n🏢 By Founded Year:")
        founded = df[df['founded_year'].notna()]['founded_year'].value_counts().sort_index(ascending=False).head(15)
        for year, count in founded.items():
            print(f"   {int(year)}: {count:>3}")


def find_data_quality_issues(df):
    """Find potential data quality issues."""
    print("\n" + "="*80)
    print("🔍 DATA QUALITY CHECKS")
    print("="*80)
    
    issues = []
    
    # Missing startup names
    missing_names = df[df['startup_name'].isna()]
    if len(missing_names) > 0:
        issues.append(f"⚠️  {len(missing_names)} articles missing startup name")
        print(f"\n⚠️  {len(missing_names)} articles missing startup name:")
        for _, row in missing_names[['article_title']].head(5).iterrows():
            print(f"   - {row['article_title'][:70]}...")
    
    # Articles with funding amount but no round type
    if 'funding_amount' in df.columns and 'funding_round' in df.columns:
        has_amount_no_round = df[df['funding_amount'].notna() & df['funding_round'].isna()]
        if len(has_amount_no_round) > 0:
            issues.append(f"⚠️  {len(has_amount_no_round)} articles have funding amount but no round type")
            print(f"\n⚠️  {len(has_amount_no_round)} articles have funding amount but no round type")
    
    # Articles with city but no canton
    if 'city' in df.columns and 'canton' in df.columns:
        has_city_no_canton = df[df['city'].notna() & df['canton'].isna()]
        if len(has_city_no_canton) > 0:
            issues.append(f"⚠️  {len(has_city_no_canton)} articles have city but no canton")
            print(f"\n⚠️  {len(has_city_no_canton)} articles have city but no canton")
    
    # Invalid founded years (too old or in future)
    if 'founded_year' in df.columns:
        current_year = datetime.now().year
        invalid_years = df[(df['founded_year'] < 1900) | (df['founded_year'] > current_year)]
        if len(invalid_years) > 0:
            issues.append(f"⚠️  {len(invalid_years)} articles have invalid founded year")
            print(f"\n⚠️  {len(invalid_years)} articles have invalid founded year")
    
    if not issues:
        print("\n✅ No major data quality issues found!")
    
    return issues


def generate_summary_stats(df):
    """Generate summary statistics."""
    print("\n" + "="*80)
    print("📈 SUMMARY STATISTICS")
    print("="*80)
    
    stats = {
        'Total Articles': len(df),
        'With Startup Name': df['startup_name'].notna().sum(),
        'With Funding Data': df['funding_amount'].notna().sum(),
        'With Location Data': df['city'].notna().sum(),
        'With Industry Data': df['industry'].notna().sum(),
        'With Keywords': df['primary_keywords'].notna().sum(),
    }
    
    print()
    for key, value in stats.items():
        pct = (value / len(df) * 100) if len(df) > 0 else 0
        print(f"{key:<25} {value:>5} ({pct:>5.1f}%)")
    
    return stats


def main():
    """Run all analyses."""
    print("\n" + "="*80)
    print("🔬 LLM ANALYZER - QUALITY ANALYSIS REPORT")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Input file: {INPUT_FILE}")
    
    try:
        df = pd.read_csv(INPUT_FILE)
        
        # Run analyses
        analyze_completeness(df)
        analyze_funding_data(df)
        analyze_location_data(df)
        analyze_industry_data(df)
        analyze_keywords(df)
        analyze_temporal_data(df)
        find_data_quality_issues(df)
        generate_summary_stats(df)
        
        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nDataset contains {len(df)} analyzed articles")
        print(f"Coverage: {df['startup_name'].notna().sum() / len(df) * 100:.1f}% with startup names")
        print()
        
    except FileNotFoundError:
        print(f"\n❌ ERROR: File not found: {INPUT_FILE}")
        print("   Make sure you've run the analyzer first:")
        print("   python3 8_llm_article_analyzer.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == '__main__':
    main()
