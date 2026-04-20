#!/usr/bin/env python3
"""
Extract structured data from scraped articles and output to CSV
Based on EXTRACTION_PROMPT_ONLY.txt specifications
"""

import pandas as pd
import re
import json
from pathlib import Path

# City to canton mapping
CITY_TO_CANTON = {
    'Zurich': 'ZH', 'Geneva': 'GE', 'Lausanne': 'VD', 'Basel': 'BS',
    'Bern': 'BE', 'Zug': 'ZG', 'Lugano': 'TI', 'St. Gallen': 'SG', 'Lucerne': 'LU',
    'Sarnen': 'OW', 'Stans': 'NW'
}

def extract_startup_name(text, title):
    """Extract company name - look for AG/SA/GmbH/Sàrl"""
    # First try: Extract from title (most reliable)
    title_patterns = [
        r'^([A-Z][A-Za-z0-9\s&\'-]+?)(?:\s+raises|\s+secures|\s+sammelt|\s+sichert|\s+receives|\s+raises)',
        r'^([A-Z][A-Za-z0-9\s&\'-]+?)\s+(?:hat|has|announced)',
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, title)
        if match:
            name = match.group(1).strip()
            # Add legal suffix if missing
            if not re.search(r'\b(AG|SA|GmbH|Sàrl)$', name):
                # Look for it in text
                suffix_match = re.search(rf'\b{re.escape(name)}\s+(AG|SA|GmbH|Sàrl)\b', text)
                if suffix_match:
                    name = f"{name} {suffix_match.group(1)}"
            if len(name) < 50:
                return name
    
    # Second try: Look for "More news about [Company AG]" - cleanest source
    more_news_pattern = r'More news about ([A-Z][A-Za-z0-9\s&\'-]+(?:AG|SA|GmbH|Sàrl))\s*(?:Company profiles|Related|$)'
    match = re.search(more_news_pattern, text)
    if match:
        name = match.group(1).strip()
        # Filter out bad matches
        bad_words = ['Cusp Capital', 'Auxxo', 'HTGF', 'Founderful', 'UBS', 'Venture Kick', 
                    'InnoBooster', 'Hi inov', 'FINANCING', 'Comments', 'More news', 'Related News']
        if not any(bad in name for bad in bad_words) and len(name) < 50:
            # Remove duplicates like "cohaga AG Related News cohaga AG"
            words = name.split()
            if words.count('AG') > 1 or words.count('SA') > 1:
                # Keep only first occurrence
                seen = set()
                cleaned = []
                for word in words:
                    if word not in seen or word not in ['AG', 'SA', 'GmbH', 'Sàrl']:
                        cleaned.append(word)
                        seen.add(word)
                name = ' '.join(cleaned)
            return name
    
    # Third try: Look in article body for company name with legal suffix
    body_pattern = r'\b([A-Z][A-Za-z0-9\s&\'-]{2,40}(?:AG|SA|GmbH|Sàrl))\b'
    matches = re.findall(body_pattern, text[:1000])  # First 1000 chars
    
    if matches:
        # Filter and deduplicate
        bad_words = ['Cusp Capital', 'Auxxo', 'HTGF', 'Founderful', 'UBS', 'Venture Kick', 
                    'InnoBooster', 'Hi inov', 'FINANCING', 'Comments', 'More news', 'Related News',
                    'Muhammad Abdullah', 'Principal Investments']
        valid_names = []
        for name in matches:
            name = name.strip()
            if (not any(bad in name for bad in bad_words) and 
                len(name) < 50 and 
                len(name.split()) <= 5):  # Max 5 words
                valid_names.append(name)
        
        if valid_names:
            # Return most common name
            from collections import Counter
            return Counter(valid_names).most_common(1)[0][0]
    
    return None

def extract_funding_amount(text):
    """Extract and normalize funding amount to {number}M {CURRENCY} format"""
    patterns = [
        # Standard formats
        (r'(EUR|CHF|USD|\$)\s*([\d,\.]+)\s*million', lambda m: (m.group(2), normalize_currency(m.group(1)))),
        (r'([\d,\.]+)\s*million\s*(EUR|CHF|USD|dollars|francs|euros)', lambda m: (m.group(1), normalize_currency(m.group(2)))),
        (r'([\d,\.]+)\s*Millionen\s*(Euro|Franken|CHF|EUR)', lambda m: (m.group(1), normalize_currency(m.group(2)))),
        
        # Swiss format with apostrophe thousands separator: CHF 150'000, 870'000 Franken
        (r'CHF\s*([\d,\']+)(?:\s|$|,)', lambda m: (str(float(m.group(1).replace("'", "").replace(",", "")) / 1000000), 'CHF')),
        (r'([\d\']+)\s*(?:Franken|francs)', lambda m: (str(float(m.group(1).replace("'", "").replace(",", "")) / 1000000), 'CHF')),
        
        # Handle undisclosed
        (r'siebenstellig', lambda m: ('undisclosed', '')),
        (r'Millionenbetrag', lambda m: ('undisclosed', '')),
    ]
    
    for pattern, extractor in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                result = extractor(match)
                if result[0] == 'undisclosed':
                    return 'undisclosed'
                amount = result[0].replace(',', '.').replace("'", "")
                currency = result[1]
                
                # Format with proper precision
                amount_float = float(amount)
                if amount_float < 1:
                    # Show 2 decimals for small amounts
                    return f"{amount_float:.2f}M {currency}".replace('.00M', 'M')
                else:
                    # Show 1 decimal for larger amounts
                    return f"{amount_float:.1f}M {currency}".replace('.0M', 'M')
            except:
                continue
    return None

def normalize_currency(curr):
    """Normalize currency codes"""
    curr_map = {
        '$': 'USD', 'dollars': 'USD', 'euros': 'EUR', 'francs': 'CHF',
        'Euro': 'EUR', 'Franken': 'CHF'
    }
    return curr_map.get(curr, curr.upper())

def extract_funding_round_raw(text):
    """Extract exact funding round phrase"""
    patterns = [
        r'(seed round|Seed-Runde|Series [A-D]|Kapitalerhöhung|strategic investment)',
        r'(Pre-Seed|Seed Extension|Seed-Erweiterungsrunde)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def map_funding_round(raw_round, text):
    """Map to standardized funding round - improved detection"""
    if not raw_round:
        # Check for Venture Kick or awards
        if 'Venture Kick' in text:
            return 'Award'
        if any(word in text for word in ['prize', 'award', 'gewonnen', 'winner']):
            return 'Award'
        if any(word in text.lower() for word in ['innobooster', 'grant', 'government funding', 'foundation']):
            return 'Grant'
        # Check for acquisition (not a funding round)
        if any(word in text.lower() for word in ['acquired by', 'acquisition', 'übernommen']):
            return None  # Acquisitions are not funding rounds
        return 'Undisclosed'
    
    raw_lower = raw_round.lower()
    mapping = {
        'pre-seed': 'Pre-Seed',
        'pre seed': 'Pre-Seed',
        'preseed': 'Pre-Seed',
        'seed round': 'Seed',
        'seed-runde': 'Seed',
        'seed': 'Seed',
        'seed extension': 'Seed Extension',
        'seed-erweiterungsrunde': 'Seed Extension',
        'seed-erweiterung': 'Seed Extension',
        'series a': 'Series A',
        'series b': 'Series B',
        'series c': 'Series C',
        'series d': 'Series D+',
        'kapitalerhöhung': 'Undisclosed',
        'strategic investment': 'Strategic Investment',
    }
    
    for key, value in mapping.items():
        if key in raw_lower:
            return value
    
    return 'Undisclosed'

def extract_investors(text):
    """Extract investor names - improved with German patterns and deduplication"""
    patterns = [
        # English patterns
        r'led by ([A-Z][A-Za-z0-9\s&,]+(?:Capital|Fund|Ventures|Partners|Participations))',
        r'backed by ([A-Z][A-Za-z0-9\s&,]+)',
        r'investment from ([A-Z][A-Za-z0-9\s&,]+)',
        r'funding from ([A-Z][A-Za-z0-9\s&,]+)',
        r'raised[^.]+from ([A-Z][A-Za-z0-9\s&,]+(?:Capital|Fund|Ventures|Partners))',
        
        # German patterns
        r'angeführt von ([A-Z][A-Za-z0-9\s&,]+)',
        r'unter der Führung von ([A-Z][A-Za-z0-9\s&,]+)',
        r'mit Beteiligung[^.]+?([A-Z][A-Za-z0-9\s&,]+(?:Capital|Fund|Ventures|Partners))',
    ]
    
    investors = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            investor_text = match.group(1)
            
            # Stop at certain phrases
            stop_words = [', strengthening', ', working', ', which', '. ', ' said', ' commented', 
                         ' added', ' explained', ' through', ' in ', ' is ']
            for stop in stop_words:
                if stop in investor_text:
                    investor_text = investor_text.split(stop)[0]
            
            # Split by "and" or ","
            parts = re.split(r'\s+and\s+|,\s*(?:and\s+)?', investor_text)
            for part in parts:
                part = part.strip()
                # Clean up articles and conjunctions
                part = re.sub(r'^(the|with participation from|with)\s+', '', part, flags=re.IGNORECASE)
                
                # Filter out generic or too short
                if (len(part) > 2 and 
                    'various' not in part.lower() and 
                    'business angels' not in part.lower() and
                    len(part) < 100):  # Reasonable length
                    investors.append(part)
    
    # Deduplicate while preserving order
    seen = set()
    unique_investors = []
    for inv in investors:
        inv_lower = inv.lower()
        if inv_lower not in seen:
            seen.add(inv_lower)
            unique_investors.append(inv)
    
    return ', '.join(unique_investors[:5]) if unique_investors else None  # Limit to 5

def extract_city(text, title):
    """Extract city from text - improved with more patterns"""
    # Combine title and first 500 chars for better coverage
    search_text = title + " " + text[:500]
    
    patterns = [
        # English patterns
        r'\b(Zurich|Geneva|Lausanne|Basel|Bern|Lucerne|Zug|St\.\s*Gallen|Lugano)-based',
        
        # German patterns - adjective forms
        r'\bDie\s+(Zürcher|Genfer|Lausanner|Basler|Berner|Luzerner|Zuger|St\.\s*Galler|Tessiner)\s+',
        r'\bDas\s+(Zürcher|Genfer|Lausanner|Basler|Berner|Luzerner|Zuger|St\.\s*Galler|Tessiner)\s+',
        r'\bDer\s+(Zürcher|Genfer|Lausanner|Basler|Berner|Luzerner|Zuger|St\.\s*Galler|Tessiner)\s+',
        
        # Regional references
        r'\b(Sarner|Obwaldner|Nidwaldner)\s+',
        
        # French patterns
        r'basée à (Genève|Zurich|Lausanne|Bâle|Berne|Lucerne|Zoug|Saint-Gall|Lugano)',
        r'située à (Genève|Zurich|Lausanne|Bâle|Berne|Lucerne|Zoug|Saint-Gall|Lugano)',
        
        # Pattern: "miros, a Lausanne-based startup"
        r',\s*a\s+(Zurich|Geneva|Lausanne|Basel|Bern|Lucerne|Zug|St\.\s*Gallen|Lugano)-based',
    ]
    
    city_map = {
        'Zürcher': 'Zurich', 'Genfer': 'Geneva', 'Lausanner': 'Lausanne',
        'Basler': 'Basel', 'Berner': 'Bern', 'Luzerner': 'Lucerne',
        'Zuger': 'Zug', 'St. Galler': 'St. Gallen', 'Tessiner': 'Lugano',
        'Genève': 'Geneva', 'Bâle': 'Basel', 'Berne': 'Bern',
        'Zoug': 'Zug', 'Saint-Gall': 'St. Gallen',
        'Sarner': 'Sarnen', 'Obwaldner': 'Sarnen', 'Nidwaldner': 'Stans'
    }
    
    for pattern in patterns:
        match = re.search(pattern, search_text, re.IGNORECASE)
        if match:
            city = match.group(1)
            return city_map.get(city, city)
    return None

def extract_founded_year(text):
    """Extract founding year - improved with German patterns"""
    patterns = [
        # English
        r'founded in (\d{4})',
        r'established in (\d{4})',
        
        # German
        r'gegründet (\d{4})',
        r'gegründete[sn]?\s+(?:Unternehmen|Startup).*?(\d{4})',
        r'(\d{4})\s+gegründet',
        r'(\d{4})\s+gestartete[sn]?\s+(?:Unternehmen|Startup)',
        r'Das\s+(\d{4})\s+gestartete',
        
        # French
        r'fondée en (\d{4})',
        
        # Context patterns
        r'seit\s+(\d{4})',
        r'in\s+(\d{4})',
        r'out of the EPFL ecosystem.*?(\d{4})',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            if 1990 <= year <= 2026:
                return year
    return None

def extract_employees(text):
    """Extract employee count - improved with German patterns"""
    patterns = [
        # English
        r'team of (\d+)',
        r'(\d+)\s+employees',
        
        # German
        r'(\d+)\s+Mitarbeitende',
        r'(\d+)\s+Mitarbeiter',
        r'(\d+)\s+Personen\s+gewachsen',
        r'auf\s+(\d+)\s+Personen',
        r'bootstrapped\s+auf\s+(\d+)',
        r'Team\s+von\s+(\d+)',
        
        # French
        r'(\d+)\s+employés',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            count = int(match.group(1))
            if 1 <= count <= 100000:  # Reasonable range
                return count
    return None

def extract_website(text):
    """Extract company website"""
    pattern = r'https?://(?:www\.)?([a-z0-9-]+\.(ch|com|io|ai|net))'
    matches = re.findall(pattern, text.lower())
    for domain, tld in matches:
        full_domain = f"{domain}.{tld}"
        # Exclude startupticker and common sites
        if 'startupticker' not in full_domain and 'figma' not in full_domain:
            return full_domain
    return None

def categorize_industry(text, title):
    """Determine primary industry - more conservative classification"""
    text_lower = text.lower()
    title_lower = title.lower()
    combined = text_lower + " " + title_lower
    
    # Priority 1: Specific domains (most specific first)
    if any(word in combined for word in ['drug discovery', 'therapy', 'therapeutic', 'clinical trial', 'pharmaceutical', 'oncology', 'gene therapy']):
        return 'BioTech'
    
    if any(word in combined for word in ['medical device', 'surgical', 'implant', 'diagnostic device']):
        return 'MedTech'
    
    if any(word in combined for word in ['co₂', 'carbon capture', 'carbon offset', 'climate tech', 'cleantech', 'solar', 'energy storage', 'hydrogen']):
        return 'CleanTech'
    
    # Priority 2: Tech-enabled sectors
    if any(word in combined for word in ['digital health', 'patient monitoring', 'telemedicine', 'health data platform']):
        return 'HealthTech'
    
    if any(word in combined for word in ['payment', 'banking', 'wealth management', 'insurance tech', 'fintech']):
        return 'FinTech'
    
    if any(word in combined for word in ['robot', 'robotics', 'autonomous', 'drone']):
        return 'Robotics'
    
    if any(word in combined for word in ['cybersecurity', 'security platform', 'threat detection']):
        return 'Cybersecurity'
    
    # Priority 3: AI/ML - only if AI is the PRODUCT
    if any(phrase in combined for phrase in ['ai platform', 'ai-powered', 'ai solution', 'artificial intelligence platform', 
                                              'machine learning platform', 'llm', 'generative ai']):
        # Check if it's NOT just using AI internally
        if not any(word in combined for word in ['biotech', 'pharmaceutical', 'healthcare', 'medical']):
            return 'AI/ML'
    
    # Priority 4: SaaS and Software
    if any(word in combined for word in ['saas', 'software platform', 'enterprise software', 'b2b software']):
        return 'Enterprise SaaS'
    
    # Fallback
    return 'Other'

def extract_keywords(text, industry):
    """Extract primary and secondary keywords"""
    text_lower = text.lower()
    
    primary = []
    secondary = []
    
    keyword_map = {
        'AI': ['ai', 'artificial intelligence'],
        'GenAI': ['generative ai', 'genai', 'llm'],
        'Enterprise': ['enterprise', 'b2b'],
        'SaaS': ['saas', 'software as a service'],
        'HealthTech': ['health', 'medical', 'patient'],
        'BioTech': ['biotech', 'drug', 'therapy'],
        'FinTech': ['fintech', 'payment', 'banking'],
        'ClimateTech': ['climate', 'carbon', 'co₂', 'energy'],
        'Analytics': ['analytics', 'data'],
        'Automation': ['automation', 'workflow'],
    }
    
    for keyword, patterns in keyword_map.items():
        if any(p in text_lower for p in patterns):
            if len(primary) < 3:
                primary.append(keyword)
            elif len(secondary) < 3:
                secondary.append(keyword)
    
    return ', '.join(primary) if primary else None, ', '.join(secondary) if secondary else None

def process_articles(input_csv, output_csv):
    """Main processing function"""
    print(f"Reading articles from {input_csv}...")
    df = pd.read_csv(input_csv)
    print(f"Loaded {len(df)} articles")
    
    results = []
    
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"Processing article {idx+1}/{len(df)}...")
        
        text = row['Article_Text']
        title = row['Title']
        
        # Extract all fields
        startup_name = extract_startup_name(text, title)
        city = extract_city(text, title)
        funding_amount = extract_funding_amount(text)
        funding_round_raw = extract_funding_round_raw(text)
        funding_round = map_funding_round(funding_round_raw, text)
        investors = extract_investors(text)
        founded_year = extract_founded_year(text)
        employees = extract_employees(text)
        website = extract_website(text)
        industry = categorize_industry(text, title)
        primary_kw, secondary_kw = extract_keywords(text, industry)
        
        result = {
            'startup_name': startup_name,
            'publication_date': row['Publication_Date'],
            'year': row['Year'],
            'funding_amount': funding_amount,
            'funding_round_raw': funding_round_raw,
            'funding_round': funding_round,
            'investor_names': investors,
            'city': city,
            'canton': CITY_TO_CANTON.get(city) if city else None,
            'founded_year': founded_year,
            'employees': employees,
            'website': website,
            'location': 'Switzerland',
            'industry': industry,
            'sub_industry': None,  # Requires more detailed analysis
            'business_model_type': 'B2B-SaaS' if 'SaaS' in (primary_kw or '') else 'Unknown',
            'primary_keywords': primary_kw,
            'secondary_keywords': secondary_kw,
        }
        
        results.append(result)
    
    # Create output DataFrame
    result_df = pd.DataFrame(results)
    
    # Save to CSV
    result_df.to_csv(output_csv, index=False)
    print(f"\n✓ Extracted {len(result_df)} records to {output_csv}")
    
    # Print summary
    print("\nSummary:")
    print(f"  - Records with startup names: {result_df['startup_name'].notna().sum()}")
    print(f"  - Records with funding amounts: {result_df['funding_amount'].notna().sum()}")
    print(f"  - Records with cities: {result_df['city'].notna().sum()}")
    print("\nTop 10 records:")
    print(result_df[['startup_name', 'city', 'funding_amount', 'funding_round']].head(10))

if __name__ == '__main__':
    input_file = 'data/startupticker_raw_articles_v7_step1_FINANCING.csv'
    output_file = 'data/startupticker_extracted_financing.csv'
    
    process_articles(input_file, output_file)
    print("\n✓ Done!")
