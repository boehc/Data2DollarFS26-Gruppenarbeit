"""
Startupticker.ch News Scraper V5 (MASSIVELY IMPROVED KEYWORD EXTRACTION)
NEUE VERBESSERUNGEN:
- Erweiterte Keyword-Extraktion basierend auf HSG-Kursinhalten
- Fallback-Strategie: Titel + Tags wenn Content fehlt
- Semantic Keyword Mapping (AI = Künstliche Intelligenz, etc.)
- Business Model Detection verbessert
- Sub-Industry Granularität erhöht
"""

import time
import re
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# LIMIT für Artikel-Scraping (total)
MAX_ARTICLES = 4500


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


def extract_company_from_title(title):
    """Extrahiert Company-Namen aus Artikel-Titel."""
    words = title.split()
    for word in words:
        if word and word[0].isupper() and len(word) >= 3:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word:
                return clean_word
    return None


def extract_funding_info(text):
    """Extrahiert Funding-Informationen aus Text (verbessert)."""
    if not text:
        return None, None
    
    # Erweiterte Patterns
    patterns = [
        # "CHF 5.2 million", "$10M", "€3.5M"
        r'(USD|CHF|EUR|€|\$)\s*(\d+[\.,]?\d*)\s*(million|mio|m\b)',
        r'(\d+[\.,]?\d*)\s*(million|mio|m\b)\s*(USD|CHF|EUR|€|\$)',
        # "5 million francs", "10 million dollars"
        r'(\d+[\.,]?\d*)\s*million\s*(francs?|dollars?|euros?)',
        # "raises $5M", "secures CHF 10M"
        r'(?:raises?|secures?|receives?)\s+(USD|CHF|EUR|\$)\s*(\d+[\.,]?\d*)\s*([MK]|million)?',
        # Deutsch: "erhält CHF 5 Millionen"
        r'(?:erhält|bekommt|sichert)\s+(CHF|USD|EUR)\s*(\d+[\.,]?\d*)\s*Million',
        # "undisclosed amount", "Millionenbetrag"
        r'undisclosed\s+(?:amount|sum|round)',
        r'Millionenbetrag',
        # K-Format: "CHF 150K", "$500K"
        r'(USD|CHF|EUR|\$)\s*(\d+[\.,]?\d*)\s*K\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                if 'undisclosed' in match.group(0).lower() or 'Millionenbetrag' in match.group(0):
                    return 'undisclosed', 'Funding Round'
                
                amount = None
                currency = None
                unit = 'M'  # Default Million
                
                groups = match.groups()
                for g in groups:
                    if g and re.match(r'\d+[\.,]?\d*', g):
                        amount = float(g.replace(',', '.'))
                    elif g and g.upper() in ['USD', 'CHF', 'EUR', '$', '€']:
                        currency = g.upper().replace('$', 'USD').replace('€', 'EUR')
                    elif g and g.upper() in ['K', 'M']:
                        unit = g.upper()
                    elif g and any(x in g.lower() for x in ['franc', 'dollar', 'euro']):
                        if 'franc' in g.lower():
                            currency = 'CHF'
                        elif 'dollar' in g.lower():
                            currency = 'USD'
                        elif 'euro' in g.lower():
                            currency = 'EUR'
                
                if amount and currency:
                    # Format: "5.2M USD"
                    if unit == 'K':
                        return f"{amount}K {currency}", 'Seed/Series A'
                    else:
                        return f"{amount}M {currency}", 'Seed/Series A'
                    
            except:
                continue
    
    return None, None


def extract_investors(text):
    """Extrahiert Investor-Namen aus Text."""
    if not text:
        return None
    
    patterns = [
        r'(?:led by|führt|angeführt von|together with|mit)\s+([A-Z][A-Za-z\s&,.-]+(?:Capital|Ventures|Partners|Fund|AG|GmbH|SA))',
        r'(?:investor|Investor)s?\s+(?:include|such as|wie)?\s*:?\s*([A-Z][A-Za-z\s&,.-]+)',
        r'(?:from|von)\s+([A-Z][A-Za-z\s&,.-]+(?:Capital|Ventures|Partners|Fund))',
    ]
    
    investors = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            investor = match.group(1).strip()
            if len(investor) > 3 and investor not in investors:
                investors.append(investor)
    
    if investors:
        return ', '.join(investors[:5])
    
    return None


def extract_tech_keywords_enhanced(text, tags=[], title=''):
    """
    MASSIV VERBESSERTE Keyword-Extraktion mit HSG-Kurs Alignment.
    
    NEUE FEATURES:
    - Fallback auf Titel + Tags wenn kein Content
    - Mehr Keyword-Varianten (AI, ML, KI, etc.)
    - Semantic Mapping (Künstliche Intelligenz -> AI)
    - Partial Match statt nur Full Phrase
    """
    # WICHTIG: Nutze Titel + Tags als Fallback!
    combined_text = ' '.join(filter(None, [text or '', title or '', ' '.join(tags or [])]))
    
    if not combined_text or len(combined_text) < 10:
        return None
    
    text_upper = combined_text.upper()
    
    # ERWEITERTE Tech Keywords basierend auf HSG-Kursen
    tech_keywords = {
        # AI/ML - VIEL mehr Varianten!
        'AI': ['AI ', ' AI,', 'ARTIFICIAL INTELLIGENCE', 'KÜNSTLICHE INTELLIGENZ', 'KI ', ' KI,', 
               'AI-POWERED', 'AI-BASED', 'AI-DRIVEN', 'MACHINE LEARNING', 'ML ', 'DEEP LEARNING',
               'NEURAL NETWORK', 'COMPUTER VISION', 'NLP', 'NATURAL LANGUAGE'],
        
        # Blockchain & Web3
        'Blockchain': ['BLOCKCHAIN', 'CRYPTO', 'CRYPTOCURRENCY', 'WEB3', 'NFT', 'DECENTRALIZED',
                       'SMART CONTRACT', 'DEFI', 'BITCOIN', 'ETHEREUM', 'TOKEN'],
        
        # SaaS & Cloud
        'SaaS': ['SAAS', 'SOFTWARE AS A SERVICE', 'CLOUD-BASED', 'SUBSCRIPTION', 'PLATFORM'],
        'Cloud': ['CLOUD COMPUTING', 'CLOUD INFRASTRUCTURE', 'AWS', 'AZURE', 'GOOGLE CLOUD'],
        
        # IoT & Hardware
        'IoT': ['IOT', 'INTERNET OF THINGS', 'SENSOR', 'CONNECTED DEVICE', 'SMART DEVICE'],
        
        # Biotech & Healthtech
        'Biotech': ['BIOTECH', 'BIOTECHNOLOGY', 'GENE', 'GENOMICS', 'PROTEOMICS', 'CRISPR',
                    'SYNTHETIC BIOLOGY', 'BIOINFORMATICS'],
        'Healthtech': ['HEALTHTECH', 'DIGITAL HEALTH', 'MEDICAL DEVICE', 'PATIENT', 'CLINICAL',
                       'DIAGNOSIS', 'TELEHEALTH', 'TELEMEDICINE', 'WEARABLE'],
        
        # Fintech
        'Fintech': ['FINTECH', 'PAYMENT', 'BANKING', 'LENDING', 'INSURANCE', 'INSURTECH',
                    'WEALTHTECH', 'REGTECH', 'NEOBANK', 'DIGITAL WALLET'],
        
        # Mobility & Transport
        'Mobility': ['MOBILITY', 'AUTONOMOUS', 'SELF-DRIVING', 'ELECTRIC VEHICLE', 'EV ',
                     'TRANSPORTATION', 'AUTOMOTIVE', 'FLEET', 'RIDESHARE', 'MICRO-MOBILITY'],
        
        # Cleantech & Sustainability
        'Cleantech': ['CLEANTECH', 'CLEAN ENERGY', 'RENEWABLE', 'SOLAR', 'WIND ENERGY',
                      'CARBON', 'SUSTAINABILITY', 'CLIMATE TECH', 'GREEN TECH', 'CIRCULAR ECONOMY'],
        
        # Robotics & Automation
        'Robotics': ['ROBOT', 'ROBOTICS', 'AUTOMATION', 'DRONE', 'AUTONOMOUS SYSTEM',
                     'INDUSTRIAL AUTOMATION', 'COBOTS'],
        
        # AR/VR/XR
        'AR/VR': [' AR ', 'AUGMENTED REALITY', 'VIRTUAL REALITY', ' VR ', 'MIXED REALITY',
                  'METAVERSE', ' XR ', 'IMMERSIVE'],
        
        # Cybersecurity
        'Cybersecurity': ['CYBERSECURITY', 'SECURITY', 'ENCRYPTION', 'DATA PROTECTION',
                          'PRIVACY', 'ZERO TRUST', 'THREAT DETECTION'],
        
        # Data & Analytics
        'Analytics': ['DATA ANALYTICS', 'BIG DATA', 'BUSINESS INTELLIGENCE', 'INSIGHTS',
                      'DATA SCIENCE', 'PREDICTIVE ANALYTICS', 'DATA VISUALIZATION'],
        
        # EdTech
        'EdTech': ['EDTECH', 'EDUCATION TECHNOLOGY', 'LEARNING PLATFORM', 'E-LEARNING',
                   'ONLINE LEARNING', 'TRAINING SOFTWARE', 'LMS'],
        
        # PropTech
        'PropTech': ['PROPTECH', 'REAL ESTATE', 'PROPERTY TECHNOLOGY', 'SMART BUILDING',
                     'PROPERTY MANAGEMENT'],
        
        # AgTech
        'AgTech': ['AGTECH', 'AGRICULTURE', 'FARMING TECHNOLOGY', 'FOOD TECH', 'PRECISION FARMING',
                   'VERTICAL FARMING', 'AGRITECH'],
        
        # Manufacturing & Industry 4.0
        'Manufacturing': ['MANUFACTURING', 'PRODUCTION', 'INDUSTRIAL', 'INDUSTRY 4.0',
                          'SMART FACTORY', 'DIGITAL TWIN'],
        
        # Logistics & Supply Chain
        'Logistics': ['LOGISTICS', 'SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY', 'FULFILLMENT',
                      'LAST-MILE', 'SHIPPING'],
        
        # E-Commerce & Marketplace
        'E-Commerce': ['E-COMMERCE', 'ECOMMERCE', 'ONLINE SHOP', 'MARKETPLACE', 'RETAIL TECH',
                       'D2C', 'DIRECT-TO-CONSUMER'],
        
        # Design & UX (aus HSG-Kursen)
        'Design Thinking': ['DESIGN THINKING', 'USER EXPERIENCE', 'UX ', ' UI', 'HUMAN-CENTERED',
                            'PROTOTYP', 'USER RESEARCH', 'ITERATIVE'],
        
        # Business Model Innovation (aus HSG-Kursen)
        'Scalable': ['SCALABLE', 'SCALE-UP', 'GROWTH HACKING', 'NETWORK EFFECT', 'PLATFORM BUSINESS'],
        
        # Specific Tech (aus HSG-Kursen)
        'Next.js': ['NEXT.JS', 'NEXTJS', 'REACT', 'TYPESCRIPT', 'JAVASCRIPT', 'NODE.JS'],
        'Tailwind CSS': ['TAILWIND', 'CSS FRAMEWORK'],
        'AWS': ['AWS', 'AMAZON WEB SERVICES'],
        'Azure': ['AZURE', 'MICROSOFT CLOUD'],
        'Vercel': ['VERCEL', 'DEPLOYMENT PLATFORM'],
        
        # Venture Capital Keywords (aus HSG-Kursen)
        'Venture Capital': ['VENTURE CAPITAL', 'VC ', 'SEED FUNDING', 'SERIES A', 'SERIES B',
                            'DUE DILIGENCE', 'TERM SHEET', 'VALUATION', 'CAP TABLE'],
        
        # Entrepreneurship Keywords (aus HSG-Kursen)
        'Lean Startup': ['LEAN STARTUP', 'MVP', 'MINIMUM VIABLE PRODUCT', 'PIVOT',
                         'PRODUCT-MARKET FIT', 'CUSTOMER VALIDATION'],
        
        # Marketing & Growth (aus HSG-Kursen)
        'Go-to-Market': ['GO-TO-MARKET', 'GTM', 'CUSTOMER ACQUISITION', 'CAC', 'LTV',
                         'GROWTH STRATEGY', 'SALES FUNNEL'],
    }
    
    found_keywords = set()
    
    # Durchsuche Text nach allen Keyword-Patterns
    for keyword, patterns in tech_keywords.items():
        for pattern in patterns:
            if pattern in text_upper:
                found_keywords.add(keyword)
                break  # Ein Match reicht für dieses Keyword
    
    return ', '.join(sorted(found_keywords)) if found_keywords else None


def extract_sub_industry_enhanced(text, tags=[], title='', industry=''):
    """
    VERBESSERTE Sub-Industry Extraktion mit mehr Granularität.
    """
    # Nutze alle verfügbaren Infos
    combined_text = ' '.join(filter(None, [text or '', title or '', ' '.join(tags or [])]))
    
    if not combined_text or len(combined_text) < 10:
        return None
    
    text_upper = combined_text.upper()
    
    # ERWEITERTE Sub-Industries mit mehr Detail
    sub_industries = {
        # Software & Platforms
        'SOFTWARE & PLATFORMS': ['SOFTWARE', 'PLATFORM', 'SAAS', 'APPLICATION', 'APP ',
                                  'CLOUD-BASED', 'WEB APP', 'MOBILE APP'],
        
        # Medical & Healthcare
        'MEDICAL DEVICES': ['MEDICAL DEVICE', 'DIAGNOSTICS', 'IMPLANT', 'INSTRUMENT',
                            'SURGICAL', 'MEDICAL EQUIPMENT'],
        'DRUG DISCOVERY': ['DRUG', 'PHARMACEUTICAL', 'THERAPY', 'TREATMENT', 'CLINICAL TRIAL',
                           'ANTIBODY', 'MOLECULE'],
        'DIGITAL HEALTH': ['DIGITAL HEALTH', 'TELEHEALTH', 'TELEMEDICINE', 'HEALTH APP',
                           'REMOTE MONITORING'],
        
        # Financial Services
        'FINANCIAL SERVICES': ['BANKING', 'PAYMENT', 'INSURANCE', 'LENDING', 'WEALTH MANAGEMENT'],
        'BLOCKCHAIN & CRYPTO': ['BLOCKCHAIN', 'CRYPTO', 'DEFI', 'WEB3', 'NFT'],
        
        # Commerce
        'E-COMMERCE': ['ONLINE SHOP', 'E-COMMERCE', 'MARKETPLACE', 'RETAIL PLATFORM'],
        'MARKETPLACE': ['MARKETPLACE', 'TWO-SIDED', 'PEER-TO-PEER', 'P2P'],
        
        # Mobility
        'MOBILITY SERVICES': ['RIDESHARE', 'CAR SHARING', 'TRANSPORTATION SERVICE', 'FLEET'],
        'AUTOMOTIVE TECH': ['AUTOMOTIVE', 'ELECTRIC VEHICLE', 'AUTONOMOUS DRIVING'],
        
        # Manufacturing & Industry
        'MANUFACTURING': ['PRODUCTION', 'FACTORY', 'MANUFACTURING', 'INDUSTRIAL'],
        'INDUSTRIAL AUTOMATION': ['INDUSTRIAL AUTOMATION', 'INDUSTRY 4.0', 'SMART FACTORY'],
        
        # Logistics & Supply Chain
        'LOGISTICS': ['SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY', 'FULFILLMENT', 'LOGISTICS'],
        'LAST-MILE DELIVERY': ['LAST-MILE', 'DELIVERY SERVICE', 'COURIER'],
        
        # Energy & Cleantech
        'RENEWABLE ENERGY': ['SOLAR', 'WIND ENERGY', 'RENEWABLE ENERGY', 'CLEAN ENERGY'],
        'CARBON MANAGEMENT': ['CARBON', 'CO2', 'EMISSION', 'CARBON CAPTURE'],
        
        # AgTech
        'PRECISION AGRICULTURE': ['PRECISION FARMING', 'AGTECH', 'SMART FARMING'],
        'FOOD TECH': ['FOOD TECH', 'ALTERNATIVE PROTEIN', 'PLANT-BASED'],
        
        # PropTech
        'PROPERTY MANAGEMENT': ['PROPERTY MANAGEMENT', 'FACILITY MANAGEMENT'],
        'SMART BUILDINGS': ['SMART BUILDING', 'BUILDING AUTOMATION'],
        
        # Data & Analytics
        'DATA ANALYTICS': ['DATA ANALYTICS', 'BUSINESS INTELLIGENCE', 'DATA VISUALIZATION'],
        'AI PLATFORMS': ['AI PLATFORM', 'ML PLATFORM', 'AI-AS-A-SERVICE'],
        
        # Cybersecurity
        'CYBERSECURITY': ['CYBERSECURITY', 'SECURITY PLATFORM', 'THREAT DETECTION'],
        
        # EdTech
        'LEARNING PLATFORMS': ['LEARNING PLATFORM', 'E-LEARNING', 'ONLINE EDUCATION'],
        'CORPORATE TRAINING': ['CORPORATE TRAINING', 'EMPLOYEE TRAINING'],
        
        # Communication & Collaboration
        'COLLABORATION TOOLS': ['COLLABORATION', 'TEAM TOOL', 'PRODUCTIVITY TOOL'],
        'VIDEO & COMMUNICATION': ['VIDEO CONFERENCING', 'COMMUNICATION PLATFORM'],
    }
    
    # Priorität: Spezifischste zuerst
    for sub_ind, patterns in sub_industries.items():
        if any(pattern in text_upper for pattern in patterns):
            return sub_ind
    
    # Fallback basierend auf Industry
    if industry == 'SOFTWARE':
        return 'SOFTWARE & PLATFORMS'
    elif industry == 'HEALTHCARE':
        return 'DIGITAL HEALTH'
    elif industry == 'FINTECH':
        return 'FINANCIAL SERVICES'
    
    return None


def extract_year_from_date(date_str):
    """Extrahiert Jahr aus Datum-String."""
    if not date_str:
        return None
    year_match = re.search(r'20\d{2}', date_str)
    return int(year_match.group(0)) if year_match else None


def scrape_news_overview(driver, max_articles=MAX_ARTICLES):
    """Scraped News-Übersicht mit Pagination bis max_articles erreicht ist."""
    base_url = 'https://www.startupticker.ch/en/news'
    news_items = []
    seen_urls = set()
    
    print(f"Öffne {base_url}")
    print(f"🎯 Ziel: {max_articles} Artikel")
    driver.get(base_url)
    
    wait = WebDriverWait(driver, 20)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item.news')))
        time.sleep(3)
        
        page = 1
        no_new_items_count = 0
        
        while len(news_items) < max_articles:
            print(f"📄 Scrape Seite {page} (bisher: {len(news_items)}/{max_articles})...")
            
            # Scrolle für Lazy Loading (mit Error-Handling)
            try:
                for scroll in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
            except Exception as scroll_err:
                print(f"⚠️ Scroll-Fehler (ignoriert): {scroll_err}")
                pass
            
            items = driver.find_elements(By.CSS_SELECTOR, 'div.item.news')
            new_items_found = 0
            
            for item in items:
                # Stop wenn Limit erreicht
                if len(news_items) >= max_articles:
                    print(f"✅ Limit von {max_articles} Artikeln erreicht!")
                    break
                
                try:
                    # URL (Primary Key)
                    link_elem = item.find_element(By.CSS_SELECTOR, 'a[href*="/news/"]')
                    url = link_elem.get_attribute('href')
                    
                    if url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    
                    # Titel
                    title_elem = item.find_element(By.CSS_SELECTOR, 'h2, h3, .title')
                    title = title_elem.text.strip()
                    
                    # Datum
                    date_elem = None
                    try:
                        date_elem = item.find_element(By.CSS_SELECTOR, 'time, .date, span.meta')
                        date = date_elem.text.strip()
                    except:
                        date = None
                    
                    # Tags
                    tags = []
                    try:
                        tag_elems = item.find_elements(By.CSS_SELECTOR, 'span.tag, .category, .label')
                        tags = [tag.text.strip() for tag in tag_elems if tag.text.strip()]
                    except:
                        pass
                    
                    news_items.append({
                        'url': url,
                        'title': title,
                        'date': date,
                        'tags': ', '.join(tags) if tags else None
                    })
                    
                    new_items_found += 1
                    
                except Exception as item_err:
                    continue
            
            if new_items_found == 0:
                no_new_items_count += 1
                if no_new_items_count >= 3:
                    print("⚠️ Keine neuen Items mehr gefunden (3x)")
                    break
            else:
                no_new_items_count = 0
            
            # Pagination
            if len(news_items) < max_articles:
                try:
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, 
                        'a.next, button[class*="next"], a[class*="more"], button[class*="load"]')
                    
                    if next_buttons:
                        next_buttons[0].click()
                        time.sleep(3)
                        page += 1
                    else:
                        break
                except:
                    break
        
        return news_items
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return news_items


def scrape_article_detail(driver, url, tags_str='', title=''):
    """
    Scraped Details aus einem Artikel.
    WICHTIG: Nutzt jetzt auch title als Fallback für Keywords!
    """
    try:
        driver.get(url)
        time.sleep(1.5)
        
        content = None
        try:
            content_selectors = [
                'article',
                'div.article-content',
                'div.content',
                'div[class*="text"]',
                'div.body'
            ]
            for selector in content_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        content = ' '.join([el.text for el in elements if el.text])
                        if content and len(content) > 100:
                            break
                except:
                    continue
        except:
            pass
        
        # Falls kein Content, probiere alle <p> Tags
        if not content or len(content) < 100:
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, 'p')
                content = ' '.join([p.text for p in paragraphs if p.text])
            except:
                pass
        
        investors = extract_investors(content) if content else None
        funding_from_content, _ = extract_funding_info(content) if content else (None, None)
        
        # NEU: ENHANCED Keyword-Extraktion mit Fallback auf Title
        tags_list = tags_str.split(', ') if tags_str else []
        tech_keywords = extract_tech_keywords_enhanced(content, tags_list, title)
        sub_industry = extract_sub_industry_enhanced(content, tags_list, title)
        
        return {
            'content': content,
            'investors': investors,
            'funding_from_content': funding_from_content,
            'tech_keywords': tech_keywords,
            'sub_industry': sub_industry
        }
        
    except Exception as e:
        return {
            'content': None,
            'investors': None,
            'funding_from_content': None,
            'tech_keywords': None,
            'sub_industry': None
        }


def map_to_schema(news_items):
    """Mappt News-Daten zu 16-Felder Schema."""
    if not news_items:
        return pd.DataFrame()
    
    mapped_data = []
    
    for item in news_items:
        startup_name = extract_company_from_title(item['title'])
        
        if not startup_name:
            continue
        
        year = extract_year_from_date(item['date'])
        
        # FILTER: Nur 2020-2026
        if year and year < 2020:
            continue
        
        # Funding: Priorität Content > Titel
        funding_amount = item.get('funding_from_content') or extract_funding_info(item['title'])[0]
        funding_round = extract_funding_info(item['title'])[1]
        
        # Industry aus Tags + Titel (ECHTE Industries, nicht B2B!)
        tags_str = item.get('tags', '') or ''
        title_lower = item['title'].lower()
        combined_text = (tags_str + ' ' + title_lower).lower()
        
        industry = None
        if any(kw in combined_text for kw in ['fintech', 'financial', 'payment', 'banking', 'blockchain', 'crypto']):
            industry = 'FINTECH'
        elif any(kw in combined_text for kw in ['health', 'medtech', 'biotech', 'pharma', 'medical', 'diagnostic', 'clinical']):
            industry = 'HEALTHCARE'
        elif any(kw in combined_text for kw in ['ai', 'artificial intelligence', 'machine learning', 'deep learning']):
            industry = 'AI/ML'
        elif any(kw in combined_text for kw in ['saas', 'software', 'platform', 'cloud', 'enterprise software']):
            industry = 'SOFTWARE'
        elif any(kw in combined_text for kw in ['climate', 'energy', 'sustainability', 'cleantech', 'renewable', 'carbon', 'solar']):
            industry = 'CLEANTECH'
        elif any(kw in combined_text for kw in ['mobility', 'automotive', 'ev', 'electric vehicle', 'transport', 'logistics']):
            industry = 'MOBILITY'
        elif any(kw in combined_text for kw in ['manufacturing', 'industrial', 'robotics', 'automation', 'construction']):
            industry = 'INDUSTRIALS'
        elif any(kw in combined_text for kw in ['food', 'agriculture', 'agritech', 'farming']):
            industry = 'AGTECH'
        elif any(kw in combined_text for kw in ['ecommerce', 'retail', 'marketplace', 'fashion', 'consumer']):
            industry = 'CONSUMER'
        elif any(kw in combined_text for kw in ['education', 'edtech', 'learning', 'training']):
            industry = 'EDUCATION'
        elif any(kw in combined_text for kw in ['space', 'satellite', 'aerospace', 'drone']):
            industry = 'AEROSPACE'
        else:
            industry = 'Unknown'
        
        # Business Model Type (B2B/B2C/B2G)
        business_model = 'Unknown'
        if any(kw in combined_text for kw in ['enterprise', 'b2b', 'business', 'saas', 'platform', 'industrial']):
            business_model = 'B2B'
        elif any(kw in combined_text for kw in ['consumer', 'retail', 'ecommerce', 'marketplace', 'b2c']):
            business_model = 'B2C'
        elif any(kw in combined_text for kw in ['government', 'public sector', 'civic', 'b2g']):
            business_model = 'B2G'
        
        # Investment Stage aus Funding Amount
        investment_stage = 'Early Stage'
        if funding_amount and funding_amount != 'undisclosed':
            amount_match = re.search(r'(\d+\.?\d*)', str(funding_amount))
            if amount_match:
                amount_val = float(amount_match.group(1))
                if amount_val < 1:
                    investment_stage = 'Pre-Seed'
                elif amount_val < 3:
                    investment_stage = 'Seed'
                elif amount_val < 10:
                    investment_stage = 'Series A'
                elif amount_val < 30:
                    investment_stage = 'Series B'
                else:
                    investment_stage = 'Series C+'
        
        # Tags-Override
        if tags_str:
            tags_upper = tags_str.upper()
            if 'SERIES A' in tags_upper:
                investment_stage = 'Series A'
            elif 'SERIES B' in tags_upper:
                investment_stage = 'Series B'
            elif 'SERIES C' in tags_upper:
                investment_stage = 'Series C+'
        
        # Investor aus Detail-Content
        investor_name = item.get('investors')
        
        # Tech Keywords und Sub-Industry aus Detail-Scraping (ENHANCED!)
        tech_keywords = item.get('tech_keywords')
        sub_industry = item.get('sub_industry')
        
        mapped_data.append({
            'Startup_Name': startup_name,
            'Industry': industry,
            'Sub_Industry': sub_industry or None,
            'Business_Model_Type': business_model,
            'Tech_Keywords': tech_keywords or None,
            'Year': year,
            'Funding_Amount': funding_amount or None,
            'Funding_Round': funding_round,
            'Investment_Stage': investment_stage,
            'Investor_Names': investor_name or None,
            'Location': 'Switzerland',
            'City': None,
            'Canton': None,
            'Founded_Year': None,
            'Employees': None,
            'Website': None
        })
    
    df = pd.DataFrame(mapped_data)
    
    # Korrigiertes Schema (16 Felder)
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Year', 'Funding_Amount', 'Funding_Round',
        'Investment_Stage', 'Investor_Names', 'Location', 'City',
        'Canton', 'Founded_Year', 'Employees', 'Website'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    df = df[required_columns]
    
    return df


def main():
    """Haupt-Scraping-Logik."""
    driver = None
    
    try:
        driver = setup_driver()
        
        print("\n" + "="*60)
        print("STARTUPTICKER.CH SCRAPER V5 (ENHANCED KEYWORDS)")
        print("="*60)
        
        # PHASE 1: News-Übersicht
        print("\n🔍 PHASE 1: Sammle News-Übersicht...")
        news_items = scrape_news_overview(driver, max_articles=MAX_ARTICLES)
        
        if not news_items:
            print("⚠ Keine News-Items")
            return
        
        print(f"✓ {len(news_items)} News-Items gesammelt (Limit: {MAX_ARTICLES})")
        
        # PHASE 2: Detail-Scraping (mit Title-Fallback!)
        print(f"\n📄 PHASE 2: Scrape {len(news_items)} Detail-Seiten...")
        for i, item in enumerate(news_items, 1):
            if i % 100 == 0 or i == 1 or i == len(news_items):
                print(f"  Fortschritt: {i}/{len(news_items)}...")
            
            try:
                # WICHTIG: Übergebe title für Fallback!
                details = scrape_article_detail(driver, item['url'], item.get('tags', ''), item['title'])
                item['investors'] = details.get('investors')
                item['funding_from_content'] = details.get('funding_from_content')
                item['tech_keywords'] = details.get('tech_keywords')
                item['sub_industry'] = details.get('sub_industry')
            except Exception as e:
                if i % 100 == 0:
                    print(f"  ⚠️ Fehler bei Artikel {i}: {str(e)[:50]}")
                pass
            
            time.sleep(0.3)  # Rate limiting
        
        print(f"✓ Detail-Scraping abgeschlossen")
        
        # PHASE 3: Mapping
        print("\n🔄 PHASE 3: Mappe zu Schema...")
        mapped_df = map_to_schema(news_items)
        
        output_path = './data/startupticker_startups_v5.csv'
        mapped_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Gespeichert: {output_path}")
        
        # ZUSAMMENFASSUNG
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Anzahl Startups: {len(mapped_df)}")
        
        if len(mapped_df) > 0:
            print(f"\nVollständigkeit:")
            for col in ['Startup_Name', 'Industry', 'Tech_Keywords', 'Sub_Industry', 'Year', 'Funding_Amount', 'Investor_Names']:
                non_null = mapped_df[col].notna().sum()
                pct = (non_null / len(mapped_df) * 100)
                print(f"  {col}: {pct:.1f}%")
            
            print(f"\nTop 10 Startups mit Keywords:")
            keyword_df = mapped_df[mapped_df['Tech_Keywords'].notna()]
            if len(keyword_df) > 0:
                print(keyword_df[['Startup_Name', 'Tech_Keywords', 'Sub_Industry']].head(10).to_string())
            
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
            
            # NEU: Keyword-Statistik
            if mapped_df['Tech_Keywords'].notna().sum() > 0:
                print(f"\n🔑 Tech Keywords Häufigkeit:")
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
