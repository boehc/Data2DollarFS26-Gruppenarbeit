#!/usr/bin/env python3
"""
IMPROVED Extract structured data from scraped articles and output to CSV
Major improvements:
- Better industry classification (reduce "Other" from 37% to <10%)
- Populate sub_industry field (currently 100% empty)
- Smarter keyword extraction (avoid generic "AI" everywhere)
- Better business model detection
"""

import pandas as pd
import re
import json
from pathlib import Path
from collections import Counter

# City to canton mapping
CITY_TO_CANTON = {
    'Zurich': 'ZH', 'Geneva': 'GE', 'Lausanne': 'VD', 'Basel': 'BS',
    'Bern': 'BE', 'Zug': 'ZG', 'Lugano': 'TI', 'St. Gallen': 'SG', 'Lucerne': 'LU',
    'Sarnen': 'OW', 'Stans': 'NW'
}

def extract_startup_name(text, title):
    """Extract company name - improved to handle various formats"""
    
    # SKIP: Articles about VC funds, investor groups, or foundations (not startups)
    skip_keywords = [
        'new vc', 'new fund', 'venture capital', 'vc fund', 'raises fund',
        'investor circle', 'operator circle', 'syndicate', 'angel club',
        'foundation launches', 'foundation to back'
    ]
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in skip_keywords):
        # But allow if article is about a startup WITH the same name
        if not any(word in text[:500] for word in [' AG ', ' SA ', ' GmbH ', ' Sàrl ']):
            return None
    
    # SKIP: Wisekey subsidiary or other subsidiary mentions
    if 'subsidiary' in title_lower:
        return None
    
    # Strategy 1: Extract from title with various patterns
    title_patterns = [
        # "Company Name raises/secures/extends"
        (r'^([A-Z][A-Za-z0-9\s&\'\-\.]+?)(?:\s+raises|\s+secures|\s+extends|\s+sammelt|\s+sichert|\s+erhält)', 'before_verb'),
        # "Company Name hat/has/announced"
        (r'^([A-Z][A-Za-z0-9\s&\'\-\.]+?)\s+(?:hat|has|announced)', 'before_verb'),
        # German: "Company sichert sich" or "Company sammelt"
        (r'^([A-Z][A-Za-z0-9\s&\'\-\.]+?)\s+(?:sichert\s+sich|sammelt)', 'before_verb'),
        # "Investor supports Company"
        (r'unterstützt\s+([A-Z][A-Za-z0-9\s&\'\-\.]+?)(?:\s+beim|\s+bei)', 'after_verb'),
    ]
    
    for pattern, pattern_type in title_patterns:
        match = re.search(pattern, title)
        if match:
            name = match.group(1).strip()
            
            # Clean up common prefixes
            name = re.sub(r'^(The|Der|Die|Das)\s+', '', name, flags=re.IGNORECASE)
            
            # Skip if it's a descriptor phrase
            descriptor_words = ['startup', 'company', 'firm', 'platform', 'service', 'solution']
            if any(word in name.lower() for word in descriptor_words):
                continue
            
            # Try to add legal suffix if missing
            if not re.search(r'\b(AG|SA|GmbH|Sàrl)$', name):
                # Pattern 1: Look for exact name with suffix in text
                suffix_pattern = rf'\b{re.escape(name)}\s+(AG|SA|GmbH|Sàrl)\b'
                suffix_match = re.search(suffix_pattern, text, re.IGNORECASE)
                if suffix_match:
                    name = f"{name} {suffix_match.group(1)}"
                # Pattern 2: Check if name is domain-style (e.g., "Umlaut.bio", "docdok.health")
                elif '.' in name and len(name.split('.')) == 2:
                    # Keep as is - it's a valid domain-style name
                    pass
                else:
                    # Pattern 3: Look for any company with similar start
                    similar_pattern = rf'\b({re.escape(name.split()[0])}[A-Za-z0-9\s&\'\-\.]*?)\s+(AG|SA|GmbH|Sàrl)\b'
                    similar_match = re.search(similar_pattern, text[:800])
                    if similar_match:
                        name = f"{similar_match.group(1)} {similar_match.group(2)}"
            
            # Final validation
            if len(name) > 2 and len(name) < 60 and len(name.split()) <= 6:
                # Skip investor names
                investor_keywords = ['capital', 'ventures', 'fund', 'partners', 'investments', 'participations']
                if not any(keyword in name.lower() for keyword in investor_keywords):
                    return name
    
    # Strategy 2: Look for "More news about [Company AG]" (very reliable)
    more_news_pattern = r'More news about ([A-Z][A-Za-z0-9\s&\'\-\.]+?(?:AG|SA|GmbH|Sàrl))\s*(?:Company profiles|Related|Highlights|$)'
    match = re.search(more_news_pattern, text)
    if match:
        name = match.group(1).strip()
        # Filter out investor names
        bad_words = ['Cusp Capital', 'Auxxo', 'HTGF', 'Founderful', 'UBS', 'Venture Kick', 
                    'InnoBooster', 'Hi inov', 'FINANCING', 'Comments', 'Muhammad Abdullah', 
                    'Principal Investments', 'Related News']
        if not any(bad in name for bad in bad_words) and len(name) < 60:
            return name
    
    # Strategy 3: Find German article patterns "Der/Die/Das Zürcher/Basler/... [Name]"
    german_city_pattern = r'(?:Der|Die|Das)\s+(?:Zürcher|Genfer|Basler|Berner|St\.\s*Galler|Lausanner)\s+([A-Z][A-Za-z0-9\s&\'\-\.]+?)\s+(?:hat|schloss|sichert|sammelt|erhält)'
    match = re.search(german_city_pattern, text[:500])
    if match:
        name = match.group(1).strip()
        # Try to add suffix
        if not re.search(r'\b(AG|SA|GmbH|Sàrl)$', name):
            suffix_match = re.search(rf'\b{re.escape(name)}\s+(AG|SA|GmbH|Sàrl)\b', text[:1000])
            if suffix_match:
                name = f"{name} {suffix_match.group(1)}"
        if len(name) < 60:
            return name
    
    # Strategy 4: Look in article body for companies with legal suffix
    body_pattern = r'\b([A-Z][A-Za-z0-9\s&\'\-\.]{2,45}(?:AG|SA|GmbH|Sàrl))\b'
    matches = re.findall(body_pattern, text[:1000])
    
    if matches:
        bad_words = ['Cusp Capital', 'Auxxo', 'HTGF', 'Founderful', 'UBS', 'Venture Kick', 
                    'InnoBooster', 'Hi inov', 'BaseLaunch', 'Reed Exhibitions', 'TraceOne',
                    'FINANCING', 'Comments', 'More news', 'Related News', 'Company profiles',
                    'Muhammad Abdullah', 'Principal Investments', 'GetYourGuide']
        valid_names = []
        for name in matches:
            name = name.strip()
            # Skip if too many words or contains bad keywords
            if (len(name.split()) <= 5 and 
                len(name) < 60 and
                not any(bad in name for bad in bad_words)):
                valid_names.append(name)
        
        # Return most common valid name
        if valid_names:
            return Counter(valid_names).most_common(1)[0][0]
    
    # Strategy 5: Look for domain-style names (e.g., "Umlaut.bio", "docdok.health")
    domain_pattern = r'\b([A-Z][A-Za-z0-9]+\.[a-z]{2,6})\b'
    match = re.search(domain_pattern, text[:500])
    if match:
        name = match.group(1)
        # Verify it's mentioned multiple times (likely the company)
        if text.count(name) >= 2:
            return name
    
    return None

def extract_funding_amount(text):
    """Extract and normalize funding amount"""
    patterns = [
        (r'(EUR|CHF|USD|\$)\s*([\d,\.]+)\s*million', lambda m: (m.group(2), normalize_currency(m.group(1)))),
        (r'([\d,\.]+)\s*million\s*(EUR|CHF|USD|dollars|francs|euros)', lambda m: (m.group(1), normalize_currency(m.group(2)))),
        (r'([\d,\.]+)\s*Millionen\s*(Euro|Franken|CHF|EUR)', lambda m: (m.group(1), normalize_currency(m.group(2)))),
        (r'CHF\s*([\d,\']+)(?:\s|$|,)', lambda m: (str(float(m.group(1).replace("'", "").replace(",", "")) / 1000000), 'CHF')),
        (r'([\d\']+)\s*(?:Franken|francs)', lambda m: (str(float(m.group(1).replace("'", "").replace(",", "")) / 1000000), 'CHF')),
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
                amount_float = float(amount)
                if amount_float < 1:
                    return f"{amount_float:.2f}M {currency}".replace('.00M', 'M')
                else:
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
        r'((?:pre-?)?seed(?:\s+extension)?(?:\s+round)?)',
        r'(Series [A-D]\+?)',
        r'(Seed-(?:Runde|Erweiterungsrunde))',
        r'(Kapitalerhöhung)',
        r'(strategic investment)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def map_funding_round(raw_round, text):
    """Map to standardized funding round"""
    if not raw_round:
        if 'Venture Kick' in text:
            return 'Award'
        if any(word in text for word in ['prize', 'award', 'gewonnen', 'winner']):
            return 'Award'
        if any(word in text.lower() for word in ['innobooster', 'grant', 'government funding', 'foundation']):
            return 'Grant'
        if any(word in text.lower() for word in ['acquired by', 'acquisition', 'übernommen']):
            return None
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
    """Extract investor names with German patterns and deduplication"""
    patterns = [
        r'led by ([A-Z][A-Za-z0-9\s&,]+(?:Capital|Fund|Ventures|Partners|Participations))',
        r'backed by ([A-Z][A-Za-z0-9\s&,]+)',
        r'investment from ([A-Z][A-Za-z0-9\s&,]+)',
        r'funding from ([A-Z][A-Za-z0-9\s&,]+)',
        r'raised[^.]+from ([A-Z][A-Za-z0-9\s&,]+(?:Capital|Fund|Ventures|Partners))',
        r'angeführt von ([A-Z][A-Za-z0-9\s&,]+)',
        r'unter der Führung von ([A-Z][A-Za-z0-9\s&,]+)',
        r'mit Beteiligung[^.]+?([A-Z][A-Za-z0-9\s&,]+(?:Capital|Fund|Ventures|Partners))',
    ]
    
    investors = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            investor_text = match.group(1)
            stop_words = [', strengthening', ', working', ', which', '. ', ' said', ' commented', 
                         ' added', ' explained', ' through', ' in ', ' is ']
            for stop in stop_words:
                if stop in investor_text:
                    investor_text = investor_text.split(stop)[0]
            
            parts = re.split(r'\s+and\s+|,\s*(?:and\s+)?', investor_text)
            for part in parts:
                part = part.strip()
                part = re.sub(r'^(the|with participation from|with)\s+', '', part, flags=re.IGNORECASE)
                
                if (len(part) > 2 and 
                    'various' not in part.lower() and 
                    'business angels' not in part.lower() and
                    len(part) < 100):
                    investors.append(part)
    
    seen = set()
    unique_investors = []
    for inv in investors:
        inv_lower = inv.lower()
        if inv_lower not in seen:
            seen.add(inv_lower)
            unique_investors.append(inv)
    
    return ', '.join(unique_investors[:5]) if unique_investors else None

def extract_city(text, title):
    """Extract city from text"""
    search_text = title + " " + text[:500]
    
    patterns = [
        r'\b(Zurich|Geneva|Lausanne|Basel|Bern|Lucerne|Zug|St\.\s*Gallen|Lugano)-based',
        r'\bDie\s+(Zürcher|Genfer|Lausanner|Basler|Berner|Luzerner|Zuger|St\.\s*Galler|Tessiner)\s+',
        r'\bDas\s+(Zürcher|Genfer|Lausanner|Basler|Berner|Luzerner|Zuger|St\.\s*Galler|Tessiner)\s+',
        r'\bDer\s+(Zürcher|Genfer|Lausanner|Basler|Berner|Luzerner|Zuger|St\.\s*Galler|Tessiner)\s+',
        r'\b(Sarner|Obwaldner|Nidwaldner)\s+',
        r'basée à (Genève|Zurich|Lausanne|Bâle|Berne|Lucerne|Zoug|Saint-Gall|Lugano)',
        r'située à (Genève|Zurich|Lausanne|Bâle|Berne|Lucerne|Zoug|Saint-Gall|Lugano)',
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
    """Extract founding year"""
    patterns = [
        r'founded in (\d{4})',
        r'established in (\d{4})',
        r'gegründet (\d{4})',
        r'gegründete[sn]?\s+(?:Unternehmen|Startup).*?(\d{4})',
        r'(\d{4})\s+gegründet',
        r'(\d{4})\s+gestartete[sn]?\s+(?:Unternehmen|Startup)',
        r'Das\s+(\d{4})\s+gestartete',
        r'fondée en (\d{4})',
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
    """Extract employee count"""
    patterns = [
        r'team of (\d+)',
        r'(\d+)\s+employees',
        r'(\d+)\s+Mitarbeitende',
        r'(\d+)\s+Mitarbeiter',
        r'(\d+)\s+Personen\s+gewachsen',
        r'auf\s+(\d+)\s+Personen',
        r'bootstrapped\s+auf\s+(\d+)',
        r'Team\s+von\s+(\d+)',
        r'(\d+)\s+employés',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            count = int(match.group(1))
            if 1 <= count <= 100000:
                return count
    return None

def extract_website(text):
    """Extract company website"""
    pattern = r'https?://(?:www\.)?([a-z0-9-]+\.(ch|com|io|ai|net))'
    matches = re.findall(pattern, text.lower())
    for domain, tld in matches:
        full_domain = f"{domain}.{tld}"
        if 'startupticker' not in full_domain and 'figma' not in full_domain:
            return full_domain
    return None

def categorize_industry_and_subindustry(text, title):
    """
    Determine primary industry AND sub-industry together
    This is the CORE improvement - proper classification
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = text_lower + " " + title_lower
    
    # STRATEGY: Most specific patterns first, most general last
    
    # === BIOTECH ===
    if any(phrase in combined for phrase in [
        'drug discovery', 'therapeutic', 'therapy', 'clinical trial', 'pharmaceutical',
        'oncology', 'gene therapy', 'biotech', 'bioscience', 'genomics'
    ]):
        sub = []
        if 'drug discovery' in combined or 'pharmaceutical' in combined:
            sub.append('Drug Discovery')
        if 'gene therapy' in combined or 'genomics' in combined:
            sub.append('Gene Therapy')
        if 'diagnostic' in combined:
            sub.append('Diagnostics')
        if 'oncology' in combined or 'cancer' in combined:
            sub.append('Oncology')
        return 'BioTech', ', '.join(sub[:3]) if sub else None
    
    # === MEDTECH ===
    if any(phrase in combined for phrase in [
        'medical device', 'surgical', 'implant', 'medtech', 'diagnostic device',
        'health monitoring device'
    ]):
        sub = []
        if 'diagnostic' in combined:
            sub.append('Diagnostics')
        if 'surgical' in combined or 'implant' in combined:
            sub.append('Medical Devices')
        return 'MedTech', ', '.join(sub[:3]) if sub else None
    
    # === CLEANTECH ===
    if any(phrase in combined for phrase in [
        'co₂', 'carbon capture', 'carbon offset', 'climate tech', 'cleantech',
        'solar', 'energy storage', 'hydrogen', 'wind energy', 'renewable energy',
        'emissions', 'sustainability'
    ]):
        sub = []
        if 'solar' in combined:
            sub.append('Solar')
        if 'energy storage' in combined or 'battery' in combined:
            sub.append('Energy Storage')
        if 'carbon' in combined or 'co₂' in combined:
            sub.append('Carbon & Offsetting')
        if 'circular economy' in combined or 'recycling' in combined:
            sub.append('Circular Economy')
        return 'CleanTech', ', '.join(sub[:3]) if sub else None
    
    # === HEALTHTECH ===
    if any(phrase in combined for phrase in [
        'digital health', 'patient monitoring', 'telemedicine', 'health data',
        'health platform', 'health app', 'wellness'
    ]):
        sub = []
        if 'patient monitoring' in combined:
            sub.append('Patient Monitoring')
        if 'digital therapeutic' in combined:
            sub.append('Digital Therapeutics')
        if 'health data' in combined:
            sub.append('Health Data')
        return 'HealthTech', ', '.join(sub[:3]) if sub else None
    
    # === FINTECH ===
    if any(phrase in combined for phrase in [
        'payment', 'banking', 'wealth management', 'insurance tech', 'fintech',
        'finance', 'investment', 'crypto', 'blockchain', 'neobank'
    ]):
        sub = []
        if 'payment' in combined:
            sub.append('Payments')
        if 'wealth' in combined:
            sub.append('WealthTech')
        if 'insurance' in combined:
            sub.append('InsurTech')
        if 'banking' in combined:
            sub.append('Banking Infrastructure')
        return 'FinTech', ', '.join(sub[:3]) if sub else None
    
    # === ROBOTICS ===
    if any(phrase in combined for phrase in [
        'robot', 'robotics', 'autonomous', 'drone', 'automation hardware'
    ]):
        return 'Robotics', None
    
    # === CYBERSECURITY ===
    if any(phrase in combined for phrase in [
        'cybersecurity', 'security platform', 'threat detection', 'security'
    ]):
        return 'Cybersecurity', None
    
    # === PROPTECH ===
    if any(phrase in combined for phrase in [
        'real estate', 'proptech', 'property', 'workspace', 'workpod'
    ]):
        return 'PropTech', None
    
    # === FOODTECH ===
    if any(phrase in combined for phrase in [
        'food tech', 'foodtech', 'food delivery', 'restaurant', 'nutrition'
    ]):
        return 'FoodTech', None
    
    # === LEGALTECH ===
    if any(phrase in combined for phrase in [
        'legal tech', 'legaltech', 'legal research', 'law', 'compliance'
    ]):
        return 'Other', 'LegalTech'  # Could add LegalTech as industry
    
    # === AI/ML (only if AI is the PRODUCT, not just used) ===
    if any(phrase in combined for phrase in [
        'ai platform', 'ai-powered platform', 'ai solution provider', 'artificial intelligence platform',
        'machine learning platform', 'llm', 'generative ai platform', 'ai infrastructure'
    ]):
        # Make sure it's NOT a biotech/fintech/etc using AI
        if not any(word in combined for word in ['biotech', 'pharmaceutical', 'banking', 'finance']):
            sub = []
            if 'generative ai' in combined or 'llm' in combined:
                sub.append('Foundation Models')
            if 'ai infrastructure' in combined:
                sub.append('AI Infrastructure')
            else:
                sub.append('Applied AI')
            return 'AI/ML', ', '.join(sub[:3]) if sub else 'Applied AI'
    
    # === ENTERPRISE SAAS ===
    if any(phrase in combined for phrase in [
        'saas', 'software platform', 'enterprise software', 'b2b software',
        'cloud platform', 'software as a service'
    ]):
        return 'Enterprise SaaS', None
    
    # === B2C TECH ===
    if any(phrase in combined for phrase in [
        'consumer app', 'marketplace', 'e-commerce', 'retail', 'cosmetic', 'beauty'
    ]):
        return 'B2C Tech', None
    
    # Fallback
    return 'Other', None

def extract_keywords_smart(text, title, industry, sub_industry):
    """
    Smart keyword extraction based on what company BUILT
    Avoid generic AI everywhere
    """
    text_lower = text.lower()
    combined = (text_lower + " " + title.lower())[:1000]
    
    primary = []
    secondary = []
    
    # Industry-specific keyword mapping
    keyword_detection = {
        # Core tech keywords
        'AI': ['ai platform', 'artificial intelligence platform', 'ai-powered'],
        'GenAI': ['generative ai', 'genai', 'llm', 'large language model'],
        'DeepTech': ['deeptech', 'deep tech', 'quantum', 'photonics'],
        
        # Application keywords
        'BioTech': ['biotech', 'drug', 'therapy', 'pharmaceutical'],
        'HealthTech': ['healthtech', 'digital health', 'patient'],
        'FinTech': ['fintech', 'payment', 'banking', 'finance'],
        'ClimateTech': ['climate', 'carbon', 'cleantech', 'renewable'],
        'SaaS': ['saas', 'software as a service'],
        
        # Domain keywords
        'Enterprise': ['enterprise', 'b2b'],
        'Analytics': ['analytics', 'data analysis'],
        'Automation': ['automation', 'automate'],
        'Robotics': ['robot', 'robotics'],
        'Cybersecurity': ['cybersecurity', 'security'],
        
        # Sector keywords
        'Ecommerce': ['e-commerce', 'online shop', 'retail'],
        'Logistics': ['logistics', 'supply chain'],
        'Manufacturing': ['manufacturing', 'production'],
        'PropTech': ['proptech', 'real estate', 'property'],
        'EdTech': ['edtech', 'education'],
        'AgTech': ['agtech', 'agriculture'],
        'FoodTech': ['foodtech', 'food'],
    }
    
    # Extract based on actual mentions
    for keyword, patterns in keyword_detection.items():
        if any(p in combined for p in patterns):
            # Assign to primary or secondary based on industry match
            if (keyword == industry or 
                (sub_industry and keyword in sub_industry) or
                keyword in ['Enterprise', 'Analytics', 'Automation']):  # These are often secondary
                if len(primary) < 3:
                    primary.append(keyword)
            else:
                if len(secondary) < 3:
                    secondary.append(keyword)
    
    # Fallback based on industry
    if not primary:
        industry_defaults = {
            'BioTech': ['BioTech', 'HealthTech'],
            'MedTech': ['HealthTech'],
            'CleanTech': ['ClimateTech'],
            'HealthTech': ['HealthTech'],
            'FinTech': ['FinTech'],
            'Robotics': ['Robotics'],
            'Cybersecurity': ['Cybersecurity'],
            'AI/ML': ['AI'],
            'Enterprise SaaS': ['SaaS', 'Enterprise'],
        }
        primary = industry_defaults.get(industry, [])
    
    return (', '.join(primary[:4]) if primary else None, 
            ', '.join(secondary[:3]) if secondary else None)

def determine_business_model(text, title, industry):
    """Determine business model type"""
    combined = (text + " " + title).lower()
    
    # B2B-SaaS indicators
    if any(word in combined for word in ['saas', 'enterprise software', 'b2b software', 'platform for businesses']):
        return 'B2B-SaaS'
    
    # B2B-Hardware
    if industry in ['Robotics', 'MedTech'] or any(word in combined for word in ['device', 'hardware', 'robot', 'machine']):
        return 'B2B-Hardware'
    
    # Marketplace
    if any(word in combined for word in ['marketplace', 'platform connects', 'two-sided']):
        return 'Marketplace'
    
    # B2C
    if any(word in combined for word in ['consumer', 'consumer app', 'cosmetic', 'beauty', 'retail']):
        return 'B2C'
    
    # Deep Tech / IP
    if industry in ['BioTech', 'MedTech', 'CleanTech'] or 'deep tech' in combined:
        return 'Deep Tech / IP'
    
    # B2B general (for other B2B services)
    if any(word in combined for word in ['b2b', 'enterprise', 'businesses']):
        return 'B2B-Services'
    
    return 'Unknown'

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
        
        # NEW: Better industry + sub-industry classification
        industry, sub_industry = categorize_industry_and_subindustry(text, title)
        
        # NEW: Smarter keyword extraction
        primary_kw, secondary_kw = extract_keywords_smart(text, title, industry, sub_industry)
        
        # NEW: Better business model detection
        business_model = determine_business_model(text, title, industry)
        
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
            'sub_industry': sub_industry,
            'business_model_type': business_model,
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
    print(f"  - Records with sub-industries: {result_df['sub_industry'].notna().sum()}")
    print(f"  - Records with business models (not Unknown): {(result_df['business_model_type'] != 'Unknown').sum()}")
    
    print("\nIndustry Distribution:")
    print(result_df['industry'].value_counts())
    
    print("\nTop 10 records:")
    print(result_df[['startup_name', 'city', 'industry', 'sub_industry', 'business_model_type']].head(10))

if __name__ == '__main__':
    input_file = 'data/startupticker_raw_articles_v7_step1_FINANCING.csv'
    output_file = 'data/startupticker_extracted_financing_v2.csv'
    
    process_articles(input_file, output_file)
    print("\n✓ Done!")
