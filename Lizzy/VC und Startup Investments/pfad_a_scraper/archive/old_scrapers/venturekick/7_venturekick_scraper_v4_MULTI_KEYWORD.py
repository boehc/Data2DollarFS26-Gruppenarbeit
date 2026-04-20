"""
Venturekick.ch News Scraper V4 - MULTI-KEYWORD + FULL ARTICLE TEXT
====================================================================

NEW IN V4:
1. ✅ MULTI-KEYWORD Extraction: Returns top 5 keywords per startup (not just 1!)
2. ✅ 80+ keyword categories (added 22 from friend's successful list)
3. ✅ Publication_Date field added (18-field schema)
4. ✅ Article_Text field added (full article body)
5. ✅ Aligned with friend's 37 keywords: GenAI, LLM, Infrastructure, Gaming, etc.

ENHANCED FROM V3:
- Swiss VC Database for investor detection
- Intelligent Business Model defaults
- Extended Sub-Industry granularity (30+ categories)
- German language support
- Fixed Venture Kick investor extraction
"""

import time
import re
from datetime import datetime
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from enhanced_keywords_v6 import extract_tech_keywords_multi


# Swiss VC Database für bessere Investor-Erkennung
SWISS_VCS = [
    # Top Tier VCs
    'Redalpine', 'Founderful', 'Swisscom Ventures', 'Verve Ventures',
    'Creathor Ventures', 'btov Partners', 'Lakestar',
    
    # Banks & Corporate VCs
    'ZKB', 'Zürcher Kantonalbank', 'UBS', 'Credit Suisse',
    'PostFinance', 'Raiffeisen',
    
    # Government & Accelerators
    'Venture Kick', 'Venturelab', 'Innosuisse', 'Investiere',
    'Swiss Founders Fund', 'Gebert Rüf Stiftung',
    
    # International VCs active in CH
    'Index Ventures', 'Sequoia', 'Accel', 'Point Nine',
    'Atomico', 'Balderton', 'General Catalyst',
    
    # Specialized VCs
    'VI Partners', 'Crypto Valley VC', 'CVVC', 'Earlybird',
    'High-Tech Gründerfonds', 'Iris Capital',
    
    # Corporate VCs
    'ABB Ventures', 'ABB Robotics Ventures', 'Nestlé Ventures',
    'Novartis Venture Fund', 'Roche Venture Fund', 'Sika',
    
    # Angel Groups & Other
    'Business Angels Switzerland', 'Swiss ICT Investor Club',
    'Innovaud', 'Auxxo Female Catalyst Fund', 'Cusp Capital',
    'Founderful', 'Maverick Silicon', 'SoftBank Group Corp',
    'Lombard Odier', 'Visionaries Club'
]


def setup_driver():
    """Richtet Selenium Chrome WebDriver ein (headless)."""
    print("Richte Chrome WebDriver ein...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("✓ WebDriver bereit")
    return driver


def validate_startup_name(name):
    """Validiert ob Name ein plausibler Startup-Name ist."""
    if not name or len(name) < 2:
        return False
    
    # Blacklist für generische Wörter
    blacklist = [
        'venture', 'kick', 'turning', 'growth', 'the', 'and', 'receives', 
        'from', 'raises', 'announces', 'launches', 'wins', 'series',
        'chf', 'usd', 'eur', 'million', 'thousand', 'billion'
    ]
    
    if name.lower() in blacklist:
        return False
    
    # Check ob es eine Zahl oder Währung ist
    if re.match(r'^\d+$', name) or name.upper() in ['CHF', 'USD', 'EUR']:
        return False
    
    return True


def extract_startup_name(title):
    """
    Extrahiert Startup-Namen aus News-Titel.
    WICHTIG: "Venture" und "Kick" sind NIEMALS Startup-Namen!
    """
    if not title:
        return None
    
    words = title.split()
    for word in words:
        # Erstes kapitalisiertes Wort mit 3+ Zeichen
        if word and len(word) >= 3 and word[0].isupper():
            clean = re.sub(r'[^\w]', '', word)
            if clean and validate_startup_name(clean):
                return clean
    
    return None


def extract_funding_amount(text):
    """
    ERWEITERTE Funding-Amount Extraktion.
    Patterns: 
    - "CHF 40,000" (Komma-Tausender-Trenner)
    - "CHF 150,000"
    - "USD 2.2 million"
    - "$225 million"
    - "raises USD 75 million"
    - "150K CHF"
    """
    if not text:
        return None
    
    patterns = [
        # Pattern 1: "CHF 150,000" oder "USD 40,000" (Komma-Format)
        r'(CHF|USD|EUR|\$|€)\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?)',
        # Pattern 2: "$225 million" oder "USD 72 Million"
        r'(\$|USD|CHF|EUR|€)\s*(\d+\.?\d*)\s*(million|thousand|billion|mio|k|m|b)',
        # Pattern 3: "72 Million USD" oder "2.2 million CHF"
        r'(\d+\.?\d*)\s*(million|thousand|billion|mio|k|m|b)\s*(\$|USD|CHF|EUR|€)',
        # Pattern 4: "CHF 150K" oder "150K CHF" (K-Format ohne space)
        r'(CHF|USD|EUR|\$|€)?\s*(\d+\.?\d*)\s*([KMB])\s*(CHF|USD|EUR|\$|€)?',
        # Pattern 5: "CHF 150" oder "USD 40" (ohne Einheit)
        r'(CHF|USD|EUR|\$|€)\s*(\d+\.?\d*)\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                groups = match.groups()
                
                amount = None
                unit = None
                currency = None
                
                for g in groups:
                    if not g:
                        continue
                    # Zahl (mit oder ohne Komma/Punkt)
                    if re.match(r'\d+[,\.]?\d*', g.replace(',', '')):
                        amount = float(g.replace(',', ''))
                    elif g.upper() in ['CHF', 'USD', 'EUR', '$', '€']:
                        currency = g.upper().replace('$', 'USD').replace('€', 'EUR')
                    elif g.upper() in ['K', 'M', 'B']:
                        unit = g.upper()
                    elif g.lower() in ['million', 'mio', 'm']:
                        unit = 'M'
                    elif g.lower() in ['billion', 'b']:
                        unit = 'B'
                    elif g.lower() in ['thousand', 'k']:
                        unit = 'K'
                
                if amount and currency:
                    if unit:
                        return f"{amount}{unit} {currency}"
                    else:
                        # Keine Einheit → Konvertiere basierend auf Größe
                        if amount < 1000:
                            return f"{amount}K {currency}"
                        elif amount < 1000000:
                            return f"{amount/1000}K {currency}"
                        else:
                            return f"{amount/1000000}M {currency}"
                
            except:
                continue
    
    return None


def extract_funding_round(text):
    """
    Extrahiert Funding-Round aus Text.
    """
    if not text:
        return 'Undisclosed'
    
    text_lower = text.lower()
    
    # Series Runden
    series_match = re.search(r'series\s+([a-z][\+\d]*)', text_lower)
    if series_match:
        series_letter = series_match.group(1).upper()
        return f'Series {series_letter}'
    
    # Seed Round
    if 'pre-seed' in text_lower or 'preseed' in text_lower:
        return 'Pre-Seed'
    if 'seed' in text_lower:
        return 'Seed'
    
    # Venture Kick Grant (kleine Beträge)
    if 'from venture kick' in text_lower or 'venture kick' in text_lower:
        amount_match = re.search(r'(\d+[,\.]?\d*)', text)
        if amount_match:
            amount_val = float(amount_match.group(1).replace(',', ''))
            if amount_val <= 200:  # <= 200K
                return 'Venture Kick Grant'
    
    # Generic
    if any(kw in text_lower for kw in ['investment', 'funding', 'financing', 'round']):
        return 'Funding Round'
    
    return 'Undisclosed'


def extract_investors_enhanced(text):
    """
    MASSIV VERBESSERTE Investor-Extraktion mit:
    1. WICHTIG: Venture Kick immer extrahieren bei Grants!
    2. Mehr Patterns (backed by, supported by, etc.)
    3. Swiss VC Database
    4. Deutsche Unterstützung
    """
    if not text:
        return None
    
    investors = set()
    text_lower = text.lower()
    
    # KRITISCHER FIX: Venture Kick IMMER bei Grants extrahieren!
    vk_indicators = [
        'from venture kick',
        'venture kick',
        'receives chf',
        'erhält chf'
    ]
    
    if any(indicator in text_lower for indicator in vk_indicators):
        # Prüfe ob es ein VK-Grant ist (typisch 10K, 40K, 150K)
        is_grant = False
        amount_match = re.search(r'(\d+[,\.]?\d*)\s*(k|thousand)', text_lower)
        if amount_match:
            amount = float(amount_match.group(1).replace(',', ''))
            if amount <= 200:  # Grants bis 200K
                is_grant = True
        
        # Auch wenn "from Venture Kick" im Text
        if 'from venture kick' in text_lower or is_grant:
            investors.add('Venture Kick')
    
    # Pattern Matching für andere Investoren
    investor_patterns = [
        # English
        r'led by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s|\n)',
        r'backed by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s|\n)',
        r'supported by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s|\n)',
        r'funded by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\sand\s|\n)',
        r'with backing from ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
        r'investment from ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
        r'round led by ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
        r'investors?\s+(?:include|are)\s+([A-Z][A-Za-z\s,&.-]+?)(?:\.|participated|\n)',
        r'with participation from ([A-Z][A-Za-z\s,&.-]+?)(?:\.|,|\n)',
        
        # German
        r'angeführt von ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
        r'unterstützt von ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
        r'von ([A-Z][A-Za-z\s&,.-]+?)(?:\.|,|\n)',
    ]
    
    for pattern in investor_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            inv_text = match.group(1).strip()
            # Split by comma or "and"
            parts = re.split(r',|\sand\s', inv_text)
            for part in parts[:3]:  # Max 3 pro Pattern
                inv = part.strip()
                if inv and len(inv) > 2 and len(inv) < 60 and validate_startup_name(inv):
                    investors.add(inv)
    
    # Swiss VC Database Matching
    for vc in SWISS_VCS:
        if vc.lower() in text_lower:
            investors.add(vc)
    
    return ', '.join(sorted(investors)[:5]) if investors else None


# V4: Replaced with extract_tech_keywords_multi from enhanced_keywords_v6.py
# This returns TOP 5 keywords instead of just 1
# def extract_tech_keywords_enhanced(text, title=''): 
#     ... old V3 function removed ...
    """
    MASSIV ERWEITERTE Tech-Keyword-Extraktion:
    - 60+ Kategorien (statt 9)
    - HSG-Kurs-Alignment
    - Deutsche Unterstützung
    - Partial Match Support
    - Fallback auf Titel
    """
    # Kombiniere Text + Titel für bessere Extraktion
    combined = ' '.join(filter(None, [text or '', title or '']))
    
    if not combined or len(combined) < 5:
        return None
    
    text_upper = combined.upper()
    
    # ERWEITERTE Tech Keywords
    tech_keywords = {
        # AI/ML - VIEL mehr Varianten + Deutsch
        'AI': [
            'AI ', ' AI,', 'AI-', 'AI.', 'ARTIFICIAL INTELLIGENCE',
            'KI ', ' KI,', 'KI-', 'KÜNSTLICHE INTELLIGENZ',  # Deutsch
            'AI-POWERED', 'AI-BASED', 'AI-DRIVEN', 'AI SOLUTION',
            'MACHINE LEARNING', 'ML ', ' ML,', 'DEEP LEARNING',
            'NEURAL NETWORK', 'COMPUTER VISION', 'NLP',
            'NATURAL LANGUAGE PROCESSING', 'GENERATIVE AI', 'GPT'
        ],
        
        # SaaS & Cloud
        'SaaS': [
            'SAAS', 'SOFTWARE AS A SERVICE', 'CLOUD-BASED',
            'SUBSCRIPTION', 'PLATFORM', 'CLOUD SOFTWARE'
        ],
        'Cloud': [
            'CLOUD COMPUTING', 'CLOUD INFRASTRUCTURE',
            'AWS', 'AZURE', 'GOOGLE CLOUD', 'GCP', 'CLOUD NATIVE'
        ],
        
        # Biotech & Healthtech
        'Biotech': [
            'BIOTECH', 'BIOTECHNOLOGY', 'GENOMICS', 'RNA', 'DNA',
            'GENE', 'GENE THERAPY', 'CELL THERAPY', 'PROTEIN',
            'CRISPR', 'SYNTHETIC BIOLOGY', 'BIOINFORMATICS'
        ],
        'Healthtech': [
            'HEALTHTECH', 'DIGITAL HEALTH', 'MEDICAL DEVICE',
            'PATIENT', 'CLINICAL', 'DIAGNOSIS', 'DIAGNOSTIC',
            'TELEHEALTH', 'TELEMEDICINE', 'WEARABLE', 'HEALTH APP'
        ],
        
        # Fintech & Blockchain
        'Fintech': [
            'FINTECH', 'PAYMENT', 'BANKING', 'NEOBANK',
            'DIGITAL WALLET', 'LENDING', 'INSURANCE', 'INSURTECH',
            'WEALTHTECH', 'REGTECH'
        ],
        'Blockchain': [
            'BLOCKCHAIN', 'CRYPTO', 'CRYPTOCURRENCY', 'WEB3',
            'NFT', 'DECENTRALIZED', 'SMART CONTRACT', 'DEFI',
            'BITCOIN', 'ETHEREUM', 'TOKEN', 'DAO'
        ],
        
        # IoT & Hardware
        'IoT': [
            'IOT', 'INTERNET OF THINGS', 'SENSOR', 'SENSORS',
            'CONNECTED DEVICE', 'SMART DEVICE', 'EMBEDDED'
        ],
        
        # Mobility & Transport
        'Mobility': [
            'MOBILITY', 'AUTONOMOUS', 'SELF-DRIVING', 'ADAS',
            'ELECTRIC VEHICLE', 'EV ', ' EV,', 'TRANSPORTATION',
            'AUTOMOTIVE', 'FLEET', 'RIDESHARE', 'MICRO-MOBILITY'
        ],
        
        # Cleantech & Sustainability
        'Cleantech': [
            'CLEANTECH', 'CLEAN ENERGY', 'RENEWABLE', 'SOLAR',
            'WIND ENERGY', 'CARBON', 'CO2', 'SUSTAINABILITY',
            'CLIMATE TECH', 'GREEN TECH', 'CIRCULAR ECONOMY',
            'EMISSION', 'NET ZERO', 'CARBON CAPTURE'
        ],
        
        # Robotics & Automation
        'Robotics': [
            'ROBOT', 'ROBOTICS', 'AUTOMATION', 'AUTONOMOUS SYSTEM',
            'DRONE', 'UAV', 'INDUSTRIAL AUTOMATION', 'COBOTS'
        ],
        
        # AR/VR/XR
        'AR/VR': [
            ' AR ', 'AR,', 'AR.', 'AUGMENTED REALITY',
            'VIRTUAL REALITY', ' VR ', 'VR,', 'MIXED REALITY',
            'METAVERSE', ' XR ', 'IMMERSIVE', '3D '
        ],
        
        # Cybersecurity
        'Cybersecurity': [
            'CYBERSECURITY', 'SECURITY', 'ENCRYPTION',
            'DATA PROTECTION', 'PRIVACY', 'ZERO TRUST',
            'THREAT DETECTION', 'FIREWALL', 'PENETRATION TEST'
        ],
        
        # Data & Analytics
        'Analytics': [
            'DATA ANALYTICS', 'BIG DATA', 'BUSINESS INTELLIGENCE',
            'INSIGHTS', 'DATA SCIENCE', 'PREDICTIVE ANALYTICS',
            'DATA VISUALIZATION', 'ANALYTICS PLATFORM'
        ],
        
        # EdTech
        'EdTech': [
            'EDTECH', 'EDUCATION TECHNOLOGY', 'LEARNING PLATFORM',
            'E-LEARNING', 'ONLINE LEARNING', 'TRAINING SOFTWARE',
            'LMS', 'LEARNING MANAGEMENT'
        ],
        
        # PropTech
        'PropTech': [
            'PROPTECH', 'REAL ESTATE', 'PROPERTY TECHNOLOGY',
            'SMART BUILDING', 'PROPERTY MANAGEMENT', 'FACILITY MANAGEMENT'
        ],
        
        # AgTech
        'AgTech': [
            'AGTECH', 'AGRICULTURE', 'FARMING TECHNOLOGY',
            'FOOD TECH', 'PRECISION FARMING', 'VERTICAL FARMING',
            'AGRITECH', 'SMART FARMING'
        ],
        
        # Manufacturing & Industry 4.0
        'Manufacturing': [
            'MANUFACTURING', 'PRODUCTION', 'INDUSTRIAL',
            'INDUSTRY 4.0', 'SMART FACTORY', 'DIGITAL TWIN',
            'PREDICTIVE MAINTENANCE'
        ],
        
        # Logistics & Supply Chain
        'Logistics': [
            'LOGISTICS', 'SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY',
            'FULFILLMENT', 'LAST-MILE', 'SHIPPING', 'FREIGHT'
        ],
        
        # E-Commerce
        'E-Commerce': [
            'E-COMMERCE', 'ECOMMERCE', 'ONLINE SHOP', 'MARKETPLACE',
            'RETAIL TECH', 'D2C', 'DIRECT-TO-CONSUMER', 'ONLINE RETAIL'
        ],
        
        # ===== HSG COURSE-ALIGNED KEYWORDS =====
        
        # Design Thinking & UX
        'Design Thinking': [
            'DESIGN THINKING', 'USER EXPERIENCE', 'UX ', ' UX,',
            'USER INTERFACE', ' UI ', 'HUMAN-CENTERED', 'HUMAN CENTERED',
            'PROTOTYP', 'USER RESEARCH', 'ITERATIVE', 'RAPID PROTOTYPING',
            'USER TEST', 'FEEDBACK', 'EMPATHY', 'IDEATION'
        ],
        
        # Lean Startup & MVP
        'Lean Startup': [
            'LEAN STARTUP', 'MVP', 'MINIMUM VIABLE PRODUCT',
            'PIVOT', 'PRODUCT-MARKET FIT', 'CUSTOMER VALIDATION',
            'BUSINESS MODEL VALIDATION', 'LEAN METHODOLOGY',
            'BUILD-MEASURE-LEARN', 'VALIDATED LEARNING'
        ],
        
        # Venture Capital & Funding
        'Venture Capital': [
            'VENTURE CAPITAL', 'VC ', ' VC,', 'SEED FUNDING',
            'SERIES A', 'SERIES B', 'SERIES C', 'DUE DILIGENCE',
            'TERM SHEET', 'VALUATION', 'CAP TABLE', 'INVESTMENT MEMO',
            'PITCH DECK', 'INVESTOR', 'ANGEL INVESTOR'
        ],
        
        # Go-to-Market & Growth
        'Go-to-Market': [
            'GO-TO-MARKET', 'GTM', 'CUSTOMER ACQUISITION', 'CAC',
            'LTV', 'LIFETIME VALUE', 'GROWTH STRATEGY', 'SALES FUNNEL',
            'MARKET ENTRY', 'CHANNEL STRATEGY', 'DISTRIBUTION',
            'CUSTOMER JOURNEY', 'CONVERSION'
        ],
        
        # Scalable & Platform Business
        'Scalable': [
            'SCALABLE', 'SCALE-UP', 'GROWTH HACKING', 'SCALING',
            'NETWORK EFFECT', 'PLATFORM BUSINESS', 'TWO-SIDED MARKET',
            'EXPONENTIAL GROWTH', 'VIRAL GROWTH', 'HYPERGROWTH'
        ],
        
        # ===== TECH STACK KEYWORDS (HSG) =====
        
        'Next.js': ['NEXT.JS', 'NEXTJS', 'NEXT JS'],
        'React': ['REACT', 'REACT.JS', 'REACTJS'],
        'TypeScript': ['TYPESCRIPT', 'TS '],
        'Python': ['PYTHON', 'DJANGO', 'FLASK', 'FASTAPI'],
        'Node.js': ['NODE.JS', 'NODEJS', 'NODE JS', 'EXPRESS'],
        'AWS': ['AWS', 'AMAZON WEB SERVICES', 'EC2', 'S3', 'LAMBDA'],
        'Azure': ['AZURE', 'MICROSOFT CLOUD', 'MICROSOFT AZURE'],
        'GCP': ['GOOGLE CLOUD', 'GCP', 'GOOGLE CLOUD PLATFORM'],
        'Tailwind CSS': ['TAILWIND', 'TAILWIND CSS'],
        'Vercel': ['VERCEL', 'DEPLOYMENT PLATFORM'],
        'Docker': ['DOCKER', 'KUBERNETES', 'K8S', 'CONTAINER'],
        'GraphQL': ['GRAPHQL', 'APOLLO'],
        'REST API': ['REST API', 'RESTFUL', 'REST '],
    }
    
    found_keywords = set()
    
    # Durchsuche Text nach allen Keyword-Patterns
    for keyword, patterns in tech_keywords.items():
        for pattern in patterns:
            if pattern in text_upper:
                found_keywords.add(keyword)
                break  # Ein Match reicht
    
    return ', '.join(sorted(found_keywords)) if found_keywords else None


def extract_sub_industry_enhanced(text, title='', industry=''):
    """
    MASSIV ERWEITERTE Sub-Industry Extraktion:
    - 30+ Sub-Industries (statt 8)
    - Mehr Granularität
    - Fallback auf Industry
    """
    combined = ' '.join(filter(None, [text or '', title or '']))
    
    if not combined or len(combined) < 5:
        # Fallback auf Industry
        return get_default_sub_industry(industry)
    
    text_lower = combined.lower()
    
    # ERWEITERTE Sub-Industries
    sub_industries = {
        # Healthcare (6 sub-types)
        'Drug Discovery': ['drug', 'pharmaceutical', 'therapy', 'therapeutic', 'clinical trial', 'antibody', 'molecule'],
        'Medical Devices': ['medical device', 'diagnostics', 'implant', 'surgical', 'medical equipment', 'instrument'],
        'Digital Health': ['digital health', 'telehealth', 'telemedicine', 'health app', 'remote monitoring'],
        'Biotech': ['biotech', 'genomics', 'rna', 'dna', 'gene therapy', 'cell therapy'],
        'MedTech': ['medtech', 'medical technology', 'clinical', 'medical imaging'],
        'HealthTech': ['healthtech', 'patient monitoring', 'wearable', 'health tracking'],
        
        # Fintech (6 sub-types)
        'Payments': ['payment', 'transaction', 'pos', 'digital wallet', 'payment processing'],
        'Banking': ['neobank', 'digital bank', 'lending', 'credit', 'banking platform'],
        'Insurance': ['insurtech', 'insurance', 'underwriting', 'policy'],
        'Crypto': ['crypto', 'blockchain', 'defi', 'web3', 'cryptocurrency'],
        'WealthTech': ['wealth management', 'investment', 'robo-advisor', 'portfolio'],
        'RegTech': ['regtech', 'compliance', 'kyc', 'aml', 'regulatory'],
        
        # Software (5 sub-types)
        'SaaS': ['saas', 'software as a service', 'platform', 'cloud software'],
        'Enterprise Software': ['enterprise', 'b2b software', 'business software', 'erp'],
        'Analytics': ['analytics', 'data', 'insights', 'business intelligence', 'data visualization'],
        'Cloud': ['cloud', 'infrastructure', 'devops', 'cloud platform'],
        'Collaboration Tools': ['collaboration', 'team tool', 'productivity tool', 'workflow'],
        
        # AI/ML (3 sub-types)
        'AI/ML': ['ai', 'machine learning', 'deep learning', 'artificial intelligence'],
        'Computer Vision': ['computer vision', 'image recognition', 'visual', 'object detection'],
        'NLP': ['nlp', 'natural language', 'language processing', 'chatbot', 'conversational ai'],
        
        # Cleantech (3 sub-types)
        'Renewable Energy': ['solar', 'wind energy', 'renewable energy', 'clean energy'],
        'Climate Tech': ['climate', 'carbon', 'co2', 'emissions', 'carbon capture'],
        'Circular Economy': ['recycling', 'circular', 'waste', 'sustainability', 'upcycling'],
        
        # Mobility (3 sub-types)
        'Electric Vehicles': ['ev', 'electric vehicle', 'battery', 'charging'],
        'Autonomous': ['autonomous', 'self-driving', 'adas', 'autonomous vehicle'],
        'Logistics': ['logistics', 'supply chain', 'transport', 'freight', 'delivery'],
        
        # E-Commerce (2 sub-types)
        'E-Commerce': ['online shop', 'e-commerce', 'retail platform'],
        'Marketplace': ['marketplace', 'two-sided', 'peer-to-peer', 'p2p'],
        
        # Manufacturing (2 sub-types)
        'Manufacturing': ['production', 'factory', 'manufacturing'],
        'Industrial Automation': ['industrial automation', 'industry 4.0', 'smart factory'],
        
        # Robotics (3 sub-types)
        'Industrial Robotics': ['industrial robot', 'manufacturing', 'automation'],
        'Service Robotics': ['service robot', 'delivery', 'autonomous'],
        'Drones': ['drone', 'uav', 'aerial'],
        
        # AgTech (2 sub-types)
        'Precision Agriculture': ['precision farming', 'agtech', 'smart farming'],
        'Food Tech': ['food tech', 'alternative protein', 'plant-based'],
        
        # PropTech (2 sub-types)
        'Property Management': ['property management', 'facility management'],
        'Smart Buildings': ['smart building', 'building automation'],
    }
    
    # Durchsuche nach spezifischster Sub-Industry
    for sub_ind, keywords in sub_industries.items():
        if any(kw in text_lower for kw in keywords):
            return sub_ind
    
    # Fallback auf Industry-basierte Default
    return get_default_sub_industry(industry)


def get_default_sub_industry(industry):
    """Fallback Sub-Industry basierend auf Haupt-Industry."""
    defaults = {
        'SOFTWARE': 'SaaS',
        'HEALTHCARE': 'Digital Health',
        'FINTECH': 'Payments',
        'AI/ML': 'AI/ML',
        'CLEANTECH': 'Climate Tech',
        'MOBILITY': 'Electric Vehicles',
        'INDUSTRIALS': 'Manufacturing',
        'ROBOTICS': 'Industrial Robotics',
        'AGTECH': 'Precision Agriculture',
        'EDUCATION': 'EdTech',
    }
    return defaults.get(industry)


def extract_business_model_enhanced(text, title='', industry=''):
    """
    INTELLIGENTE Business Model Extraktion mit Industry-Defaults.
    """
    combined = ' '.join(filter(None, [text or '', title or '']))
    text_lower = combined.lower()
    
    # Explizite B2C Indicators
    b2c_keywords = [
        'consumer', 'retail', 'ecommerce', 'marketplace', 'fashion',
        'lifestyle', 'gaming', 'entertainment', 'b2c', 'direct-to-consumer',
        'd2c', 'customer-facing', 'end user'
    ]
    if any(kw in text_lower for kw in b2c_keywords):
        return 'B2C'
    
    # Explizite B2G Indicators
    b2g_keywords = [
        'government', 'public sector', 'municipality', 'civic',
        'b2g', 'public service', 'governmental'
    ]
    if any(kw in text_lower for kw in b2g_keywords):
        return 'B2G'
    
    # Explizite B2B Indicators
    b2b_keywords = [
        'enterprise', 'saas', 'platform', 'b2b', 'business',
        'industrial', 'manufacturing', 'supply chain', 'corporate',
        'business-to-business'
    ]
    if any(kw in text_lower for kw in b2b_keywords):
        return 'B2B'
    
    # INTELLIGENTE DEFAULTS basierend auf Industry
    b2b_industries = [
        'SOFTWARE', 'AI/ML', 'FINTECH', 'CLEANTECH',
        'INDUSTRIALS', 'ROBOTICS', 'AGTECH'
    ]
    b2c_industries = ['CONSUMER', 'EDUCATION']
    
    if industry in b2b_industries:
        return 'B2B'
    elif industry in b2c_industries:
        return 'B2C'
    
    return 'Unknown'


def extract_industry_from_keywords(text, title=''):
    """
    Leitet Industry aus Keywords ab.
    """
    combined = ' '.join(filter(None, [text or '', title or '']))
    text_lower = combined.lower()
    
    industry_keywords = {
        'FINTECH': ['fintech', 'financial', 'payment', 'banking', 'blockchain', 'crypto', 'insurance', 'insurtech'],
        'HEALTHCARE': ['health', 'medical', 'biotech', 'pharma', 'therapeutic', 'diagnostics', 'medtech', 'clinical', 'patient'],
        'SOFTWARE': ['saas', 'software', 'platform', 'cloud', 'enterprise software', 'app'],
        'AI/ML': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'ki', 'künstliche intelligenz'],
        'INDUSTRIALS': ['manufacturing', 'industrial', 'construction', 'engineering', 'supply chain'],
        'CLEANTECH': ['climate', 'energy', 'sustainability', 'cleantech', 'renewable', 'carbon', 'green', 'solar', 'co2'],
        'AGTECH': ['agriculture', 'agtech', 'farming', 'food'],
        'MOBILITY': ['mobility', 'transport', 'automotive', 'ev', 'electric vehicle', 'logistics'],
        'CONSUMER': ['consumer', 'ecommerce', 'retail', 'marketplace', 'fashion', 'lifestyle'],
        'EDUCATION': ['education', 'edtech', 'learning', 'training'],
        'AEROSPACE': ['space', 'satellite', 'aerospace', 'aviation', 'drone'],
        'ROBOTICS': ['robotics', 'robot', 'automation', 'autonomous'],
    }
    
    for industry, keywords in industry_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return industry
    
    return None


def parse_date(date_str):
    """Parse Datum: DD.MM.YYYY → Year"""
    if not date_str:
        return None
    
    try:
        parts = date_str.split('.')
        if len(parts) == 3:
            day, month, year = parts
            return int(year)
    except:
        pass
    
    return None


def scrape_venturekick_news(driver):
    """Scraped alle News von Venturekick.ch."""
    url = 'https://www.venturekick.ch/index.cfm?page=135424'
    
    print(f"Öffne {url}")
    driver.get(url)
    
    print("Warte auf Seiteninhalt...")
    time.sleep(5)
    
    body = driver.find_element(By.TAG_NAME, 'body')
    body_text = body.text
    
    print(f"✓ Body-Text extrahiert ({len(body_text)} Zeichen)")
    
    lines = body_text.split('\n')
    news_items = []
    date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    
    print("\nParse News-Items...")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if re.match(date_pattern, line):
            date_str = line
            
            # V4: Capture FULL article text (multiple lines until next date or end)
            article_lines = []
            j = i + 1
            
            # Collect all lines until we hit the next date or end
            while j < len(lines):
                next_line = lines[j].strip()
                
                # Stop if we hit another date
                if re.match(date_pattern, next_line):
                    break
                
                # Add non-empty lines to article
                if next_line and len(next_line) > 5:
                    article_lines.append(next_line)
                
                j += 1
            
            # Combine all lines into full article text
            full_text = ' '.join(article_lines)
            
            if full_text and len(full_text) > 20:
                news_items.append({
                    'date': date_str,
                    'title': article_lines[0] if article_lines else '',  # First line as title
                    'full_text': full_text  # V4: Full article text
                })
                
                i = j  # Jump to next date
                continue
        
        i += 1
    
    print(f"✓ {len(news_items)} News-Items gefunden")
    
    return news_items


def map_to_schema(news_items):
    """
    Mappt News-Items zu 16-Felder Schema mit allen Enhancements.
    """
    if not news_items:
        return pd.DataFrame()
    
    mapped_data = []
    skipped_count = 0
    
    for item in news_items:
        year = parse_date(item['date'])
        
        # FILTER: 2020-2026
        if not year or year < 2020 or year > 2026:
            skipped_count += 1
            continue
        
        startup_name = extract_startup_name(item['title'])
        
        if not startup_name or not validate_startup_name(startup_name):
            skipped_count += 1
            continue
        
        # V4: Publication date from the 'date' field (format: DD.MM.YYYY)
        publication_date = item.get('date')  # Use the actual date from news item
        
        # V4: Get full article text for better keyword extraction
        full_text = item.get('full_text', item['title'])
        
        # Extraktionen mit ENHANCED Functions - use full_text!
        funding_amount = extract_funding_amount(full_text)
        funding_round = extract_funding_round(full_text)
        investors = extract_investors_enhanced(full_text)  # ENHANCED!
        tech_keywords = extract_tech_keywords_multi(full_text, [], item['title'])  # V4: MULTI-KEYWORD with full text!
        
        # Industry
        industry = extract_industry_from_keywords(full_text, item['title'])
        if not industry:
            industry = 'Unknown'
        
        # Business Model (ENHANCED mit Industry-Defaults!)
        business_model = extract_business_model_enhanced(full_text, item['title'], industry)
        
        # Sub-Industry (ENHANCED mit Fallback!)
        sub_industry = extract_sub_industry_enhanced(full_text, item['title'], industry)
        
        # Investment Stage
        investment_stage = 'Early Stage'
        
        if funding_round:
            round_lower = funding_round.lower()
            if 'pre-seed' in round_lower or 'venture kick grant' in round_lower:
                investment_stage = 'Pre-Seed'
            elif 'seed' in round_lower:
                investment_stage = 'Seed'
            elif 'series a' in round_lower:
                investment_stage = 'Series A'
            elif 'series b' in round_lower:
                investment_stage = 'Series B'
            elif 'series c' in round_lower:
                investment_stage = 'Series C'
            elif 'series d' in round_lower or 'series e' in round_lower:
                investment_stage = 'Growth'
        
        # Fallback auf Amount
        if investment_stage == 'Early Stage' and funding_amount:
            amount_match = re.search(r'(\d+\.?\d*)', str(funding_amount))
            if amount_match:
                amount_val = float(amount_match.group(1))
                if 'M' in funding_amount:
                    amount_val *= 1000
                elif 'B' in funding_amount:
                    amount_val *= 1000000
                
                if amount_val < 50:
                    investment_stage = 'Pre-Seed'
                elif amount_val < 200:
                    investment_stage = 'Seed'
                elif amount_val < 3000:
                    investment_stage = 'Series A'
                elif amount_val < 10000:
                    investment_stage = 'Series B'
                elif amount_val < 30000:
                    investment_stage = 'Series C'
                else:
                    investment_stage = 'Growth'
        
        mapped_data.append({
            'Startup_Name': startup_name,
            'Industry': industry,
            'Sub_Industry': sub_industry or None,
            'Business_Model_Type': business_model,
            'Tech_Keywords': tech_keywords or None,
            'Publication_Date': publication_date or None,  # V4: NEW
            'Article_Text': full_text or None,  # V4: NEW (full article text, not just title!)
            'Year': year,
            'Funding_Amount': funding_amount or None,
            'Funding_Round': funding_round,
            'Investment_Stage': investment_stage,
            'Investor_Names': investors or None,
            'Location': 'Switzerland',
            'City': None,
            'Canton': None,
            'Founded_Year': None,
            'Employees': None,
            'Website': None
        })
    
    df = pd.DataFrame(mapped_data)
    
    print(f"\n✓ {len(df)} Einträge gemappt (2020-2026)")
    print(f"⚠️  {skipped_count} Einträge übersprungen")
    
    # V4: Updated Schema (18 Felder - added Publication_Date and Article_Text)
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Publication_Date', 'Article_Text',  # V4: NEW
        'Year', 'Funding_Amount', 'Funding_Round',
        'Investment_Stage', 'Investor_Names', 'Location', 'City',
        'Canton', 'Founded_Year', 'Employees', 'Website'
    ]
    
    return df[required_columns]


def main():
    """Hauptfunktion."""
    print("="*70)
    print("VENTUREKICK.CH SCRAPER V4 - MULTI-KEYWORD + FULL TEXT")
    print("="*70)
    print("NEW: Returns TOP 5 keywords per startup!")
    print("NEW: 80+ keyword categories (GenAI, LLM, Infrastructure, etc.)")
    print("NEW: Publication_Date and Article_Text fields")
    print("="*70)
    
    Path('./data').mkdir(exist_ok=True)
    
    driver = None
    try:
        driver = setup_driver()
        
        news_items = scrape_venturekick_news(driver)
        
        if not news_items:
            print("⚠ Keine News-Items gescraped")
            return
        
        print("\n🔄 Mappe zu Schema...")
        mapped_df = map_to_schema(news_items)
        
        if len(mapped_df) == 0:
            print("⚠ Keine Daten nach Mapping")
            return
        
        output_path = './data/venturekick_startups_v4.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Gespeichert: {output_path}")
        
        # ERWEITERTE ZUSAMMENFASSUNG
        print("\n" + "="*70)
        print("ZUSAMMENFASSUNG")
        print("="*70)
        print(f"Anzahl Startups: {len(mapped_df)}")
        
        print(f"\nVollständigkeit:")
        for col in ['Startup_Name', 'Industry', 'Tech_Keywords', 'Sub_Industry', 
                    'Business_Model_Type', 'Year', 'Funding_Amount', 'Investor_Names']:
            non_null = mapped_df[col].notna().sum()
            pct = (non_null / len(mapped_df) * 100)
            print(f"  {col}: {pct:.1f}%")
        
        print(f"\nTop 10 Startups:")
        print(mapped_df[['Startup_Name', 'Year', 'Tech_Keywords', 'Investor_Names']].head(10).to_string())
        
        if mapped_df['Year'].notna().sum() > 0:
            print(f"\nJahresverteilung:")
            year_counts = mapped_df['Year'].value_counts().sort_index(ascending=False)
            for year, count in year_counts.items():
                if pd.notna(year):
                    print(f"  {int(year)}: {count} Startups")
        
        if mapped_df['Industry'].notna().sum() > 0:
            print(f"\nIndustry-Verteilung:")
            ind_counts = mapped_df['Industry'].value_counts()
            for ind, count in ind_counts.items():
                print(f"  {ind}: {count} Startups")
        
        if mapped_df['Business_Model_Type'].notna().sum() > 0:
            print(f"\nBusiness Model-Verteilung:")
            bm_counts = mapped_df['Business_Model_Type'].value_counts()
            for bm, count in bm_counts.items():
                print(f"  {bm}: {count} Startups")
        
        # NEUE STATISTIK: Tech Keywords
        if mapped_df['Tech_Keywords'].notna().sum() > 0:
            print(f"\n🔑 Top Tech Keywords:")
            all_keywords = []
            for kw_str in mapped_df['Tech_Keywords'].dropna():
                keywords = [k.strip() for k in str(kw_str).split(',')]
                all_keywords.extend(keywords)
            
            from collections import Counter
            keyword_counts = Counter(all_keywords)
            for kw, count in keyword_counts.most_common(15):
                print(f"  {kw}: {count} Startups")
        
        print("\n✓ ERFOLGREICH ABGESCHLOSSEN")
        
    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("WebDriver geschlossen")


if __name__ == "__main__":
    main()
