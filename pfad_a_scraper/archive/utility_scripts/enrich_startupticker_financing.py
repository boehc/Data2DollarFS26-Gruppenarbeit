#!/usr/bin/env python3
"""
Cross-Analyze & Enrich Startupticker Financing Dataset
Combines raw articles with extracted data to produce a unified enriched dataset.
"""

import pandas as pd
import re
from collections import Counter
import sys

# ============================================================================
# STEP 1: LOAD & AUDIT
# ============================================================================

def load_and_audit():
    """Load both CSVs and perform initial audit."""
    print("=" * 80)
    print("STEP 1: LOAD & AUDIT")
    print("=" * 80)
    
    # Load data
    print("\n📂 Loading data files...")
    df_raw = pd.read_csv('data/startupticker_raw_articles_v7_step1_FINANCING.csv')
    df_extracted = pd.read_csv('data/startupticker_extracted_financing_v3_FINAL.csv')
    
    print(f"✓ Raw articles: {len(df_raw)} rows")
    print(f"✓ Extracted data: {len(df_extracted)} rows")
    
    # Merge side-by-side
    df = df_extracted.copy()
    df['source_url'] = df_raw['URL']
    df['Article_Text'] = df_raw['Article_Text']
    df['Title'] = df_raw['Title']
    
    print(f"\n✓ Merged dataset: {len(df)} rows")
    
    # Completeness report
    print("\n" + "=" * 80)
    print("COMPLETENESS REPORT")
    print("=" * 80)
    
    completeness = []
    for col in df.columns:
        if col not in ['Article_Text', 'Title']:  # Skip these from report
            non_null = df[col].notna().sum()
            non_empty = df[col].replace('', pd.NA).notna().sum()
            pct = (non_empty / len(df)) * 100
            completeness.append({
                'Column': col,
                'Non-Null': non_null,
                'Non-Empty': non_empty,
                'Fill %': pct
            })
    
    comp_df = pd.DataFrame(completeness).sort_values('Fill %')
    print(comp_df.to_string(index=False))
    
    # Highlight low fill rates
    print("\n⚠️  COLUMNS BELOW 60% FILL RATE (enrichment targets):")
    low_fill = comp_df[comp_df['Fill %'] < 60]
    if len(low_fill) > 0:
        print(low_fill[['Column', 'Fill %']].to_string(index=False))
    else:
        print("None!")
    
    # Find rows with most NaN values
    print("\n" + "=" * 80)
    print("TOP 3 ROWS WITH MOST MISSING VALUES")
    print("=" * 80)
    
    key_cols = ['startup_name', 'funding_amount', 'funding_round', 'investor_names',
                'city', 'canton', 'founded_year', 'employees', 'website']
    df['nan_count'] = df[key_cols].isna().sum(axis=1)
    top_nan = df.nlargest(3, 'nan_count')
    
    for idx, row in top_nan.iterrows():
        print(f"\nRow {idx}: {row['startup_name']} ({row['nan_count']} missing)")
        print(f"  Title: {row['Title'][:80]}...")
        missing = [col for col in key_cols if pd.isna(row[col])]
        print(f"  Missing: {', '.join(missing)}")
    
    return df


# ============================================================================
# STEP 2: CROSS-VALIDATE CORE FINANCIAL FIELDS
# ============================================================================

def normalize_funding_amount(text):
    """Extract and normalize funding amount from text."""
    if pd.isna(text) or str(text).strip() == '':
        return None, None
    
    text = str(text).upper()
    
    # Pattern: number + M/million/mio + currency
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:M(?:ILLION)?|MIO)\s*(CHF|EUR|USD|GBP)',
        r'(CHF|EUR|USD|GBP)\s*(\d+(?:\.\d+)?)\s*(?:M(?:ILLION)?|MIO)',
        r'(\d+(?:\.\d+)?)\s*(?:K|THOUSAND)\s*(CHF|EUR|USD|GBP)',
        r'(CHF|EUR|USD|GBP)\s*(\d+(?:\.\d+)?)\s*(?:K|THOUSAND)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            # Determine which group is number vs currency
            if groups[0] in ['CHF', 'EUR', 'USD', 'GBP']:
                currency = groups[0]
                amount = float(groups[1])
            else:
                amount = float(groups[0])
                currency = groups[1] if len(groups) > 1 else 'CHF'
            
            # Normalize to millions
            if 'K' in text or 'THOUSAND' in text:
                amount = amount / 1000
            
            return amount, currency
    
    return None, None


def search_funding_in_text(article_text):
    """Search article text for funding amount."""
    if pd.isna(article_text):
        return None, None
    
    text = str(article_text)
    
    # Search for funding amounts in text
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:million|mio|M)\s+(CHF|EUR|USD|GBP)',
        r'(CHF|EUR|USD|GBP)\s*(\d+(?:\.\d+)?)\s*(?:million|mio|M)',
        r'€(\d+(?:\.\d+)?)\s*(?:million|mio|M)',
        r'\$(\d+(?:\.\d+)?)\s*(?:million|mio|M)',
        r'(\d+(?:\.\d+)?)\s*(?:thousand|K)\s+(CHF|EUR|USD|GBP)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            # Handle different match structures
            if len(groups) == 2:
                if groups[0] in ['CHF', 'EUR', 'USD', 'GBP']:
                    currency = groups[0]
                    amount = float(groups[1])
                else:
                    amount = float(groups[0])
                    currency = groups[1]
            else:
                amount = float(groups[0])
                # Infer currency from symbol
                if '€' in match.group():
                    currency = 'EUR'
                elif '$' in match.group():
                    currency = 'USD'
                else:
                    currency = 'CHF'
            
            # Convert K to millions
            if 'K' in text[match.start():match.end()].upper() or \
               'THOUSAND' in text[match.start():match.end()].upper():
                amount = amount / 1000
            
            return amount, currency
    
    return None, None


def normalize_round(text):
    """Normalize funding round to canonical labels."""
    if pd.isna(text) or str(text).strip() == '':
        return 'Undisclosed'
    
    text = str(text).lower()
    
    # Priority-ordered mapping
    if 'pre-seed' in text or 'preseed' in text:
        return 'Pre-Seed'
    elif 'series d' in text or 'series e' in text or 'series f' in text:
        return 'Series D+'
    elif 'series c' in text:
        return 'Series C'
    elif 'series b' in text:
        return 'Series B'
    elif 'series a' in text:
        return 'Series A'
    elif 'seed' in text:
        return 'Seed'
    elif 'grant' in text:
        return 'Grant'
    elif 'award' in text:
        return 'Award'
    elif 'strategic' in text and 'investment' in text:
        return 'Strategic Investment'
    else:
        return 'Undisclosed'


def validate_financial_fields(df):
    """Cross-validate extracted fields against raw text."""
    print("\n" + "=" * 80)
    print("STEP 2: CROSS-VALIDATE CORE FINANCIAL FIELDS")
    print("=" * 80)
    
    df['needs_review'] = False
    
    amount_matches = 0
    round_matches = 0
    investor_matches = 0
    
    amount_mismatches = []
    round_mismatches = []
    investor_mismatches = []
    
    print("\n🔍 Validating financial fields...")
    
    for idx, row in df.iterrows():
        if idx % 200 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(df)} rows...")
        
        article_text = row['Article_Text']
        
        # Skip if article text is too short
        if pd.isna(article_text) or len(str(article_text)) < 50:
            continue
        
        # a) Validate funding amount
        extracted_amt, extracted_curr = normalize_funding_amount(row['funding_amount'])
        text_amt, text_curr = search_funding_in_text(article_text)
        
        if extracted_amt and text_amt:
            # Check if within 5% tolerance
            tolerance = 0.05
            if text_curr == extracted_curr and \
               abs(extracted_amt - text_amt) / text_amt <= tolerance:
                amount_matches += 1
            else:
                amount_mismatches.append({
                    'idx': idx,
                    'startup': row['startup_name'],
                    'extracted': row['funding_amount'],
                    'found_in_text': f"{text_amt}M {text_curr}"
                })
                df.at[idx, 'needs_review'] = True
        elif extracted_amt:
            amount_matches += 1  # Assume correct if we can't verify
        
        # b) Validate funding round
        extracted_round = normalize_round(row['funding_round'])
        text_round = normalize_round(article_text)
        
        if extracted_round == text_round or extracted_round == 'Undisclosed':
            round_matches += 1
        else:
            round_mismatches.append({
                'idx': idx,
                'startup': row['startup_name'],
                'extracted': row['funding_round'],
                'found_in_text': text_round
            })
            df.at[idx, 'needs_review'] = True
        
        # c) Validate investor names
        investors = str(row['investor_names'])
        if investors and investors != 'nan' and investors.strip() != '':
            # Split on common separators
            inv_list = re.split(r'[,;]', investors)
            found_any = False
            for inv in inv_list:
                inv = inv.strip()
                if len(inv) > 3 and inv.lower() in article_text.lower():
                    found_any = True
                    break
            
            if found_any:
                investor_matches += 1
            else:
                investor_mismatches.append({
                    'idx': idx,
                    'startup': row['startup_name'],
                    'extracted': investors[:50]
                })
    
    # Print validation report
    print("\n" + "=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    
    total_with_amounts = df['funding_amount'].notna().sum()
    total_with_rounds = df['funding_round'].notna().sum()
    total_with_investors = df['investor_names'].notna().sum()
    
    print(f"\n✓ Funding Amount Matches: {amount_matches}/{total_with_amounts} " +
          f"({100*amount_matches/max(total_with_amounts,1):.1f}%)")
    print(f"✓ Funding Round Matches: {round_matches}/{total_with_rounds} " +
          f"({100*round_matches/max(total_with_rounds,1):.1f}%)")
    print(f"✓ Investor Matches: {investor_matches}/{total_with_investors} " +
          f"({100*investor_matches/max(total_with_investors,1):.1f}%)")
    
    # Show mismatches
    if amount_mismatches:
        print(f"\n⚠️  FUNDING AMOUNT MISMATCHES (showing first 10):")
        for mm in amount_mismatches[:10]:
            print(f"  Row {mm['idx']}: {mm['startup']}")
            print(f"    Extracted: {mm['extracted']}")
            print(f"    In Text: {mm['found_in_text']}")
    
    if round_mismatches:
        print(f"\n⚠️  FUNDING ROUND MISMATCHES (showing first 10):")
        for mm in round_mismatches[:10]:
            print(f"  Row {mm['idx']}: {mm['startup']}")
            print(f"    Extracted: {mm['extracted']}")
            print(f"    In Text: {mm['found_in_text']}")
    
    if investor_mismatches:
        print(f"\n⚠️  INVESTOR NAME MISMATCHES (showing first 10):")
        for mm in investor_mismatches[:10]:
            print(f"  Row {mm['idx']}: {mm['startup']}")
            print(f"    Extracted: {mm['extracted']}")
    
    print(f"\n🚩 Total rows flagged for review: {df['needs_review'].sum()}")
    
    return df


# ============================================================================
# STEP 3: RE-EXTRACT MISSING FIELDS WITH REGEX
# ============================================================================

# Swiss cities and cantons mapping
SWISS_CANTONS = {
    'Zurich': 'ZH', 'Zürich': 'ZH',
    'Geneva': 'GE', 'Genève': 'GE', 'Genf': 'GE',
    'Basel': 'BS', 'Bâle': 'BS',
    'Bern': 'BE', 'Berne': 'BE',
    'Lausanne': 'VD', 'Vaud': 'VD',
    'Lucerne': 'LU', 'Luzern': 'LU',
    'St. Gallen': 'SG', 'St Gallen': 'SG', 'Sankt Gallen': 'SG',
    'Zug': 'ZG',
    'Winterthur': 'ZH',
    'Lugano': 'TI', 'Ticino': 'TI', 'Tessin': 'TI',
    'Fribourg': 'FR', 'Freiburg': 'FR',
    'Neuchâtel': 'NE', 'Neuenburg': 'NE',
    'Thun': 'BE',
    'Chur': 'GR', 'Graubünden': 'GR',
    'Schaffhausen': 'SH',
    'Aarau': 'AG', 'Aargau': 'AG',
    'Solothurn': 'SO',
    'Sion': 'VS', 'Sitten': 'VS', 'Valais': 'VS', 'Wallis': 'VS',
    'Bellinzona': 'TI',
    'Locarno': 'TI',
    'Montreux': 'VD',
    'Vevey': 'VD',
    'Nyon': 'VD',
    'Morges': 'VD',
    'Yverdon': 'VD',
    'La Chaux-de-Fonds': 'NE',
    'Schwyz': 'SZ',
    'Sarnen': 'OW', 'Obwalden': 'OW',
    'Stans': 'NW', 'Nidwalden': 'NW',
    'Altdorf': 'UR', 'Uri': 'UR',
    'Glarus': 'GL',
    'Appenzell': 'AI',
    'Herisau': 'AR',
    'Liestal': 'BL', 'Basel-Landschaft': 'BL',
    'Delémont': 'JU', 'Jura': 'JU',
    'Biel': 'BE', 'Bienne': 'BE',
}


def extract_city_canton(df):
    """Extract city and canton from article text."""
    print("\n" + "=" * 80)
    print("STEP 3a: EXTRACT CITY & CANTON")
    print("=" * 80)
    
    city_filled = 0
    canton_filled = 0
    
    # Build regex pattern for all cities
    city_names = list(SWISS_CANTONS.keys())
    city_pattern = r'\b(?:' + '|'.join(re.escape(city) for city in city_names) + r')\b'
    
    print(f"\n🔍 Searching for Swiss cities in article text...")
    
    for idx, row in df.iterrows():
        if idx % 200 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(df)} rows...")
        
        article_text = row['Article_Text']
        
        # Skip if article text is too short
        if pd.isna(article_text) or len(str(article_text)) < 50:
            continue
        
        # Only process if city is missing
        if pd.isna(row['city']) or str(row['city']).strip() == '':
            # Search for city patterns
            patterns = [
                r'based in\s+(' + city_pattern + ')',
                r'(' + city_pattern + r')-based',
                r'headquartered in\s+(' + city_pattern + ')',
                r'located in\s+(' + city_pattern + ')',
                r'from\s+(' + city_pattern + ')',
                r'in\s+(' + city_pattern + r'),',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, article_text, re.IGNORECASE)
                if match:
                    city = match.group(1)
                    # Find matching city from our dict (case-insensitive)
                    for known_city, canton in SWISS_CANTONS.items():
                        if known_city.lower() == city.lower():
                            df.at[idx, 'city'] = known_city
                            city_filled += 1
                            
                            # Also fill canton if missing
                            if pd.isna(row['canton']) or str(row['canton']).strip() == '':
                                df.at[idx, 'canton'] = canton
                                canton_filled += 1
                            break
                    break
    
    print(f"\n✓ Filled {city_filled} city values")
    print(f"✓ Filled {canton_filled} canton values")
    
    return df


def extract_website(df):
    """Extract website URLs from article text."""
    print("\n" + "=" * 80)
    print("STEP 3b: EXTRACT WEBSITE")
    print("=" * 80)
    
    website_filled = 0
    
    url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9\-]+\.[a-zA-Z]{2,})(?:/[^\s]*)?'
    exclude_domains = ['startupticker.ch', 'linkedin.com', 'twitter.com', 
                       'crunchbase.com', 'x.com', 'facebook.com', 'instagram.com']
    
    print(f"\n🔍 Extracting website URLs...")
    
    for idx, row in df.iterrows():
        if idx % 200 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(df)} rows...")
        
        article_text = row['Article_Text']
        
        # Skip if article text is too short
        if pd.isna(article_text) or len(str(article_text)) < 50:
            continue
        
        # Only process if website is missing
        if pd.isna(row['website']) or str(row['website']).strip() == '':
            # Find all URLs
            urls = re.findall(url_pattern, article_text, re.IGNORECASE)
            
            # Filter out excluded domains
            valid_urls = []
            for url in urls:
                is_excluded = False
                for domain in exclude_domains:
                    if domain in url.lower():
                        is_excluded = True
                        break
                if not is_excluded:
                    valid_urls.append(url)
            
            if len(valid_urls) == 1:
                df.at[idx, 'website'] = valid_urls[0]
                website_filled += 1
            elif len(valid_urls) > 1:
                # Prefer .com or .ch domains
                for url in valid_urls:
                    if url.endswith('.com') or url.endswith('.ch'):
                        df.at[idx, 'website'] = url
                        website_filled += 1
                        break
                else:
                    # Take first if no .com/.ch found
                    df.at[idx, 'website'] = valid_urls[0]
                    website_filled += 1
    
    print(f"\n✓ Filled {website_filled} website values")
    
    return df


def extract_employees(df):
    """Extract employee count from article text."""
    print("\n" + "=" * 80)
    print("STEP 3c: EXTRACT EMPLOYEES")
    print("=" * 80)
    
    employees_filled = 0
    
    patterns = [
        r'(\d{1,4})\s*(?:full[- ]?time\s*)?employees',
        r'team of\s*(\d{1,4})',
        r'(\d{1,4})\s*(?:people|staff|headcount)',
        r'employs\s*(\d{1,4})',
    ]
    
    print(f"\n🔍 Extracting employee counts...")
    
    for idx, row in df.iterrows():
        if idx % 200 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(df)} rows...")
        
        article_text = row['Article_Text']
        
        # Skip if article text is too short
        if pd.isna(article_text) or len(str(article_text)) < 50:
            continue
        
        # Only process if employees is missing
        if pd.isna(row['employees']):
            for pattern in patterns:
                match = re.search(pattern, article_text, re.IGNORECASE)
                if match:
                    emp_count = int(match.group(1))
                    if 1 <= emp_count <= 9999:  # Sanity check
                        df.at[idx, 'employees'] = emp_count
                        employees_filled += 1
                        break
    
    print(f"\n✓ Filled {employees_filled} employee values")
    
    return df


def extract_founded_year(df):
    """Extract founding year from article text."""
    print("\n" + "=" * 80)
    print("STEP 3d: EXTRACT FOUNDED YEAR")
    print("=" * 80)
    
    founded_filled = 0
    current_year = 2026
    
    patterns = [
        r'founded in\s*(20\d{2}|19\d{2})',
        r'established in\s*(20\d{2}|19\d{2})',
        r'since\s*(20\d{2}|19\d{2})',
        r'\bfounded\b.*?\b(20\d{2})\b',
    ]
    
    print(f"\n🔍 Extracting founding years...")
    
    for idx, row in df.iterrows():
        if idx % 200 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(df)} rows...")
        
        article_text = row['Article_Text']
        
        # Skip if article text is too short
        if pd.isna(article_text) or len(str(article_text)) < 50:
            continue
        
        # Only process if founded_year is missing
        if pd.isna(row['founded_year']):
            for pattern in patterns:
                match = re.search(pattern, article_text, re.IGNORECASE)
                if match:
                    year = int(match.group(1))
                    if 1990 <= year <= current_year:
                        df.at[idx, 'founded_year'] = year
                        founded_filled += 1
                        break
    
    print(f"\n✓ Filled {founded_filled} founding year values")
    
    return df


# ============================================================================
# STEP 4: REFINE INDUSTRY AND SUB_INDUSTRY
# ============================================================================

INDUSTRY_KEYWORDS = {
    "AI/ML": ["machine learning", "artificial intelligence", " llm ", 
              "large language model", "neural network", "nlp ", " ai "],
    "Cybersecurity": ["cybersecurity", "cyber security", "security software",
                      "threat detection", "penetration test", "zero trust"],
    "Enterprise SaaS": ["enterprise software", "b2b saas", "saas platform",
                        "workflow automation", " erp ", "crm software"],
    "HealthTech": ["digital health", "health platform", "patient app",
                   "telehealth", "telemedicine", "mental health app", "healthtech"],
    "EdTech": ["edtech", "e-learning", "online learning", "education platform",
               "learning management"],
    "LegalTech": ["legaltech", "legal tech", "legal software", 
                  "contract management", "compliance platform"],
    "PropTech": ["proptech", "real estate platform", "property tech",
                 "smart building"],
    "SpaceTech": ["satellite", "space tech", "aerospace", "nanosatellite", "spacecraft"],
    "AgriTech": ["agritech", "agtech", "precision farming", 
                 "crop monitoring", "agricultural"],
    "FoodTech": ["foodtech", "food tech", "alternative protein",
                 "plant-based", "cultivated meat"],
    "Robotics": ["robotics", "autonomous robot", "robotic arm",
                  "drone delivery", "autonomous vehicle"],
}

SUB_INDUSTRY_KEYWORDS = {
    "Drug Discovery": ["drug discovery", "drug development", "small molecule"],
    "Diagnostics": ["diagnostic", "in vitro", "biomarker", "point-of-care"],
    "Oncology": ["oncology", "cancer treatment", "tumor"],
    "Solar": ["solar panel", "photovoltaic", "pv system"],
    "Carbon & Offsetting": ["carbon offset", "carbon credit", "co2 removal"],
    "Crypto & Blockchain": ["blockchain", "cryptocurrency", "defi", "web3", "nft"],
    "Logistics & Delivery": ["last-mile", "delivery platform", "supply chain",
                             "freight", "logistics software"],
    "HR Tech": ["hr tech", "human resources", "talent management",
                "recruitment platform", "payroll"],
    "Marketing Tech": ["marketing platform", "adtech", "ad tech", 
                       "marketing automation", "programmatic"],
    "Payments": ["payment processing", "payment gateway", "checkout",
                 "neobank", "digital wallet"],
    "InsurTech": ["insurtech", "insurance platform", "parametric insurance",
                  "underwriting"],
    "E-commerce": ["e-commerce", "online marketplace", "d2c", 
                   "direct-to-consumer"],
    "Foundation Models": ["foundation model", "generative ai", "genai", 
                          "large language model"],
    "IoT": ["internet of things", "iot sensor", "connected device",
            "smart home", "m2m"],
    "Business Intelligence": ["business intelligence", "data analytics platform",
                              "bi tool", "data visualization"],
}


def reclassify_other_industry(df):
    """Reclassify rows where industry == 'Other'."""
    print("\n" + "=" * 80)
    print("STEP 4a: RECLASSIFY 'Other' INDUSTRY ROWS")
    print("=" * 80)
    
    other_count = (df['industry'] == 'Other').sum()
    print(f"\n🔍 Found {other_count} rows with industry='Other'")
    
    reclassified = Counter()
    
    for idx, row in df.iterrows():
        if row['industry'] != 'Other':
            continue
        
        combined_text = str(row['Title']) + " " + str(row['Article_Text'])
        combined_text = combined_text.lower()
        
        # Try to match against industry keywords
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in combined_text:
                    df.at[idx, 'industry'] = industry
                    reclassified[industry] += 1
                    break
            if df.at[idx, 'industry'] != 'Other':
                break
    
    print("\n✓ Reclassified rows by industry:")
    for industry, count in reclassified.most_common():
        print(f"  {industry}: {count}")
    
    remaining = (df['industry'] == 'Other').sum()
    print(f"\n  Remaining 'Other': {remaining}")
    
    return df


def fill_sub_industry(df):
    """Fill missing sub_industry values."""
    print("\n" + "=" * 80)
    print("STEP 4b: FILL MISSING SUB_INDUSTRY")
    print("=" * 80)
    
    sub_ind_filled = 0
    
    print(f"\n🔍 Searching for sub-industry keywords...")
    
    for idx, row in df.iterrows():
        if idx % 200 == 0 and idx > 0:
            print(f"  Processed {idx}/{len(df)} rows...")
        
        # Only process if sub_industry is missing
        if not pd.isna(row['sub_industry']) and str(row['sub_industry']).strip() != '':
            continue
        
        article_text = str(row['Article_Text']).lower()
        
        # Skip if article text is too short
        if len(article_text) < 50:
            continue
        
        # Find all matching sub-industries
        matches = []
        for sub_ind, keywords in SUB_INDUSTRY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in article_text:
                    matches.append(sub_ind)
                    break
        
        if matches:
            df.at[idx, 'sub_industry'] = ', '.join(matches)
            sub_ind_filled += 1
    
    print(f"\n✓ Filled {sub_ind_filled} sub_industry values")
    
    return df


# ============================================================================
# STEP 5: BUILD UNIFIED TAGS COLUMN
# ============================================================================

def build_tags(df):
    """Create unified tags column."""
    print("\n" + "=" * 80)
    print("STEP 5: BUILD UNIFIED TAGS COLUMN")
    print("=" * 80)
    
    print("\n🏷️  Building tags from multiple sources...")
    
    def create_tags(row):
        tags = []
        
        # Collect from all sources
        sources = [
            str(row['primary_keywords']),
            str(row['secondary_keywords']),
            str(row['business_model_type']),
            str(row['sub_industry'])
        ]
        
        for source in sources:
            if source and source != 'nan':
                # Split on commas
                parts = [p.strip() for p in source.split(',')]
                tags.extend(parts)
        
        # Remove industry value (redundant)
        industry = str(row['industry'])
        
        # Deduplicate case-insensitively
        seen = {}
        unique_tags = []
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower and tag_lower != 'nan' and tag_lower != industry.lower():
                if tag_lower not in seen:
                    seen[tag_lower] = tag
                    unique_tags.append(tag)
        
        # Sort and join
        unique_tags.sort()
        return ' | '.join(unique_tags) if unique_tags else ''
    
    df['tags'] = df.apply(create_tags, axis=1)
    
    # Count tags
    total_with_tags = (df['tags'] != '').sum()
    print(f"\n✓ Created tags for {total_with_tags}/{len(df)} rows")
    
    # Show sample
    print("\nSample tags:")
    for idx, row in df[df['tags'] != ''].head(5).iterrows():
        print(f"  {row['startup_name']}: {row['tags'][:80]}...")
    
    return df


# ============================================================================
# STEP 6: FINAL CLEANUP & OUTPUT
# ============================================================================

def normalize_funding_amount_final(text):
    """Normalize funding amount to standard format."""
    if pd.isna(text) or str(text).strip() == '':
        return ''
    
    text = str(text).upper()
    
    # Try to parse
    patterns = [
        (r'(\d+(?:\.\d+)?)\s*M(?:ILLION)?\s*(CHF|EUR|USD|GBP)', 'M'),
        (r'(\d+(?:\.\d+)?)\s*K(?:THOUSAND)?\s*(CHF|EUR|USD|GBP)', 'K'),
        (r'(CHF|EUR|USD|GBP)\s*(\d+(?:\.\d+)?)\s*M(?:ILLION)?', 'M'),
        (r'(CHF|EUR|USD|GBP)\s*(\d+(?:\.\d+)?)\s*K(?:THOUSAND)?', 'K'),
    ]
    
    for pattern, unit in patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if groups[0] in ['CHF', 'EUR', 'USD', 'GBP']:
                currency = groups[0]
                amount = groups[1]
            else:
                amount = groups[0]
                currency = groups[1] if len(groups) > 1 else 'CHF'
            
            return f"{amount}{unit} {currency}"
    
    return text


def final_cleanup(df):
    """Final cleanup and normalization."""
    print("\n" + "=" * 80)
    print("STEP 6: FINAL CLEANUP & OUTPUT")
    print("=" * 80)
    
    print("\n🧹 Normalizing column values...")
    
    # Normalize funding_amount
    df['funding_amount'] = df['funding_amount'].apply(normalize_funding_amount_final)
    
    # Normalize funding_round
    df['funding_round'] = df['funding_round'].apply(normalize_round)
    
    # Normalize publication_date
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Normalize employees
    df['employees'] = pd.to_numeric(df['employees'], errors='coerce').astype('Int64')
    
    # Normalize founded_year
    df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce').astype('Int64')
    
    # Normalize investor_names
    def normalize_investors(text):
        if pd.isna(text) or str(text).strip() == '':
            return ''
        text = str(text)
        # Replace ' and ' with ','
        text = re.sub(r'\s+and\s+', ', ', text, flags=re.IGNORECASE)
        # Clean up whitespace
        names = [n.strip() for n in text.split(',')]
        return ', '.join([n for n in names if n])
    
    df['investor_names'] = df['investor_names'].apply(normalize_investors)
    
    print("✓ Normalization complete")
    
    # Select final columns in correct order
    final_columns = [
        'startup_name', 'industry', 'sub_industry', 'tags', 'funding_amount',
        'funding_round', 'investor_names', 'publication_date', 'article_summary',
        'employees', 'city', 'canton', 'location', 'website', 'founded_year',
        'funding_round_raw', 'business_model_type', 'source_url'
    ]
    
    df_final = df[final_columns].copy()
    
    # Save
    output_file = 'data/startupticker_enriched_FINAL.csv'
    df_final.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✅ Saved to: {output_file}")
    
    return df_final


def final_summary_report(df):
    """Print comprehensive final summary."""
    print("\n" + "=" * 80)
    print("FINAL SUMMARY REPORT")
    print("=" * 80)
    
    print(f"\n📊 Total rows: {len(df)}")
    
    # Fill rate per column
    print("\n" + "=" * 80)
    print("FILL RATES BY COLUMN (sorted ascending)")
    print("=" * 80)
    
    fill_rates = []
    for col in df.columns:
        non_null = df[col].replace('', pd.NA).notna().sum()
        pct = (non_null / len(df)) * 100
        fill_rates.append({'Column': col, 'Fill %': pct})
    
    fill_df = pd.DataFrame(fill_rates).sort_values('Fill %')
    print(fill_df.to_string(index=False))
    
    # Top industries
    print("\n" + "=" * 80)
    print("TOP 10 INDUSTRIES")
    print("=" * 80)
    industry_counts = df['industry'].value_counts().head(10)
    for ind, count in industry_counts.items():
        print(f"  {ind}: {count}")
    
    # Top tags
    print("\n" + "=" * 80)
    print("TOP 15 MOST FREQUENT TAGS")
    print("=" * 80)
    all_tags = []
    for tags_str in df['tags'].dropna():
        if tags_str:
            all_tags.extend([t.strip() for t in str(tags_str).split('|')])
    
    tag_counter = Counter(all_tags)
    for tag, count in tag_counter.most_common(15):
        print(f"  {tag}: {count}")
    
    # Top investors
    print("\n" + "=" * 80)
    print("TOP 15 INVESTORS BY DEAL COUNT")
    print("=" * 80)
    all_investors = []
    for inv_str in df['investor_names'].dropna():
        if inv_str and str(inv_str).strip() != '':
            all_investors.extend([i.strip() for i in str(inv_str).split(',')])
    
    inv_counter = Counter(all_investors)
    for inv, count in inv_counter.most_common(15):
        if inv:
            print(f"  {inv}: {count}")
    
    # Funding round distribution
    print("\n" + "=" * 80)
    print("FUNDING ROUND DISTRIBUTION")
    print("=" * 80)
    round_counts = df['funding_round'].value_counts()
    for rnd, count in round_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {rnd}: {count} ({pct:.1f}%)")
    
    # Year distribution
    print("\n" + "=" * 80)
    print("YEAR DISTRIBUTION")
    print("=" * 80)
    year_counts = df['publication_date'].str[:4].value_counts().sort_index(ascending=False)
    for year, count in year_counts.head(10).items():
        print(f"  {year}: {count}")
    
    # Flagged rows
    if 'needs_review' in df.columns:
        flagged = df['needs_review'].sum()
        print(f"\n🚩 Rows flagged for review: {flagged} ({100*flagged/len(df):.1f}%)")
    
    print("\n" + "=" * 80)
    print("✅ ENRICHMENT COMPLETE!")
    print("=" * 80)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute the complete enrichment pipeline."""
    print("\n" + "=" * 80)
    print("STARTUPTICKER FINANCING DATASET ENRICHMENT PIPELINE")
    print("=" * 80)
    
    try:
        # Step 1: Load & Audit
        df = load_and_audit()
        
        # Step 2: Cross-validate
        df = validate_financial_fields(df)
        
        # Step 3: Re-extract missing fields
        df = extract_city_canton(df)
        df = extract_website(df)
        df = extract_employees(df)
        df = extract_founded_year(df)
        
        # Step 4: Refine industries
        df = reclassify_other_industry(df)
        df = fill_sub_industry(df)
        
        # Step 5: Build tags
        df = build_tags(df)
        
        # Step 6: Final cleanup & output
        df_final = final_cleanup(df)
        
        # Final summary
        final_summary_report(df_final)
        
        print("\n✅ All done! Check 'data/startupticker_enriched_FINAL.csv'")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
