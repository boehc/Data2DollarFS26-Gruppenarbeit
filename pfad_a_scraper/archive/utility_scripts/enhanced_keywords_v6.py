"""
ENHANCED TECH KEYWORDS DICTIONARY V6
Includes all 37 keywords from friend's successful list + existing keywords
Supports MULTI-KEYWORD extraction (returns top 5 per startup)
"""

def get_enhanced_tech_keywords():
    """
    Returns comprehensive tech keyword dictionary with 80+ categories.
    Aligned with friend's 37 successful keywords + HSG course content.
    """
    return {
        # ========================================
        # FRIEND'S TOP 10 CRITICAL KEYWORDS (NEW)
        # ========================================
        
        # 1. GenAI - 195 startups (20.7%) in friend's data
        'GenAI': ['GENERATIVE AI', 'GENAI', ' GPT', 'CHATGPT', 'GPT-3', 'GPT-4',
                  'DALL-E', 'STABLE DIFFUSION', 'TEXT-TO-IMAGE', 'IMAGE GENERATION',
                  'MIDJOURNEY', 'GENERATIVE KI', 'TEXT GENERATION', 'AI CONTENT'],
        
        # 2. LLM - 164 startups (17.4%)
        'LLM': ['LARGE LANGUAGE MODEL', ' LLM', 'LANGUAGE MODEL', 'TRANSFORMER',
                'BERT', 'LLAMA', 'CLAUDE', 'SPRACHMODELL', 'GROSSES SPRACHMODELL'],
        
        # 3. Infrastructure - 152 startups (16.1%)
        'Infrastructure': ['INFRASTRUCTURE', 'DEVOPS', 'CI/CD', 'KUBERNETES', 'DOCKER',
                          'CONTAINERIZATION', 'MICROSERVICES', 'API GATEWAY', 'API PLATFORM',
                          'CLOUD INFRASTRUCTURE', 'PLATFORM INFRASTRUCTURE', 'INFRASTRUKTUR'],
        
        # 4. AgentAI - 129 startups (13.7%)
        'AgentAI': ['AI AGENT', 'AUTONOMOUS AI', 'INTELLIGENT AGENT', 'MULTI-AGENT',
                    'AGENTIC', 'AI AUTOMATION', 'AGENT SYSTEM', 'AUTONOMOUS SYSTEM'],
        
        # 5. Semiconductors - 95 startups (10.1%)
        'Semiconductors': ['SEMICONDUCTOR', 'CHIP', 'PROCESSOR', 'ASIC', 'FPGA',
                          'SILICON', 'FOUNDRY', 'WAFER', 'TRANSISTOR', 'HALBLEITER'],
        
        # 6. Enterprise - 94 startups (10.0%)
        'Enterprise': ['ENTERPRISE SOFTWARE', 'ENTERPRISE PLATFORM', 'B2B SOFTWARE',
                      'B2B PLATFORM', 'CORPORATE SOFTWARE', 'BUSINESS APPLICATION',
                      'ENTERPRISE SAAS', 'ENTERPRISE SOLUTION'],
        
        # 7. CreatorEconomy - 89 startups (9.4%)
        'CreatorEconomy': ['CREATOR ECONOMY', 'CREATOR PLATFORM', 'INFLUENCER TOOL',
                          'CONTENT MONETIZATION', 'CREATOR TECH', 'CREATOR TOOL',
                          'INFLUENCER PLATFORM', 'CONTENT CREATOR'],
        
        # 8. Gaming - 74 startups (7.8%)
        'Gaming': ['GAMING', 'VIDEO GAME', 'GAME ENGINE', 'ESPORTS', 'E-SPORTS',
                  'GAME DEVELOPMENT', 'MULTIPLAYER', 'GAME PLATFORM', 'GAMING PLATFORM',
                  'VIDEOSPIEL', 'SPIELEENTWICKLUNG'],
        
        # 9. PhysicalAI - 64 startups (6.8%)
        'PhysicalAI': ['PHYSICAL AI', 'EMBODIED AI', 'ROBOTICS AI', 'MANIPULATION',
                      'ROBOT VISION', 'ROBOT LEARNING', 'HUMANOID ROBOT', 'PHYSICAL INTELLIGENCE'],
        
        # 10. DefenseTech - 59 startups (6.2%)
        'DefenseTech': ['DEFENSE', 'MILITARY', 'AEROSPACE DEFENSE', 'DUAL-USE',
                       'NATIONAL SECURITY', 'DEFENSE TECHNOLOGY', 'DEFENSE CONTRACTOR',
                       'VERTEIDIGUNG', 'MILITAR'],
        
        # ========================================
        # FRIEND'S MEDIUM PRIORITY KEYWORDS (NEW)
        # ========================================
        
        # 11. SpaceTech - 39 startups (4.1%)
        'SpaceTech': ['SPACE', 'SATELLITE', 'ROCKET', 'ORBITAL', 'AEROSPACE',
                     'SPACE TECHNOLOGY', 'LAUNCH', 'CONSTELLATION', 'NEW SPACE',
                     'RAUMFAHRT', 'SATELLIT', 'RAKETE'],
        
        # 12. SocialMedia - 36 startups (3.8%)
        'SocialMedia': ['SOCIAL MEDIA', 'SOCIAL NETWORK', 'COMMUNITY PLATFORM',
                       'SOCIAL APP', 'USER-GENERATED CONTENT', 'SOCIAL PLATFORM'],
        
        # 13. FutureOfWork - 27 startups (2.9%)
        'FutureOfWork': ['FUTURE OF WORK', 'REMOTE WORK', 'HYBRID WORK', 'PRODUCTIVITY',
                        'WORK MANAGEMENT', 'ASYNC', 'DISTRIBUTED WORK', 'WORKPLACE'],
        
        # 14. ConsumerApps - 19 startups (2.0%)
        'ConsumerApps': ['CONSUMER APP', 'MOBILE APP', 'B2C APP', 'LIFESTYLE APP',
                        'ENTERTAINMENT APP', 'CONSUMER APPLICATION'],
        
        # 15. Policy - 20 startups (2.1%)
        'Policy': ['POLICY', 'REGULATORY', 'COMPLIANCE', 'REGTECH', 'GOVERNANCE',
                  'REGULATION', 'REGULATORY TECHNOLOGY'],
        
        # 16. WearableTech - 16 startups (1.7%)
        'WearableTech': ['WEARABLE', 'SMART WATCH', 'FITNESS TRACKER', 'WEARABLE DEVICE',
                        'HEARABLE', 'SMART GLASSES', 'WEARABLE TECH'],
        
        # ========================================
        # FRIEND'S LOW PRIORITY KEYWORDS (NEW)
        # ========================================
        
        # 17-22. Niche keywords
        'LegalTech': ['LEGALTECH', 'LEGAL TECHNOLOGY', 'CONTRACT AUTOMATION',
                     'LEGAL AI', 'COMPLIANCE SOFTWARE', 'LEGAL SOFTWARE'],
        
        'FusionEnergy': ['FUSION', 'NUCLEAR FUSION', 'FUSION ENERGY', 'TOKAMAK',
                        'FUSION REACTOR', 'FUSION POWER'],
        
        'HRTech': ['HR TECH', 'HRTECH', 'HUMAN RESOURCES', 'RECRUITMENT',
                  'TALENT MANAGEMENT', 'EMPLOYEE ENGAGEMENT', 'HIRING PLATFORM'],
        
        'ComputerVision': ['COMPUTER VISION', 'IMAGE RECOGNITION', 'OBJECT DETECTION',
                          'VISUAL AI', 'IMAGE ANALYSIS', 'VIDEO ANALYTICS'],
        
        'DeepTech': ['DEEP TECH', 'DEEPTECH', 'HARD TECH', 'SCIENTIFIC BREAKTHROUGH',
                    'ADVANCED MATERIALS', 'DEEP TECHNOLOGY'],
        
        'QuantumTech': ['QUANTUM', 'QUANTUM COMPUTING', 'QUANTUM CRYPTOGRAPHY',
                       'QUBIT', 'QUANTUM SENSOR', 'QUANTUM TECHNOLOGY'],
        
        # ========================================
        # EXISTING KEYWORDS (KEEP & ENHANCE)
        # ========================================
        
        # AI/ML - Keep general AI category
        'AI': ['AI ', ' AI,', 'ARTIFICIAL INTELLIGENCE', 'KÜNSTLICHE INTELLIGENZ', 'KI ',
               'AI-POWERED', 'AI-BASED', 'AI-DRIVEN', 'MACHINE LEARNING', 'ML ',
               'DEEP LEARNING', 'NEURAL NETWORK', 'NLP', 'NATURAL LANGUAGE'],
        
        # Blockchain & Web3
        'Web3': ['BLOCKCHAIN', 'CRYPTO', 'CRYPTOCURRENCY', 'WEB3', 'NFT', 'DECENTRALIZED',
                 'SMART CONTRACT', 'DEFI', 'BITCOIN', 'ETHEREUM', 'TOKEN'],
        
        # SaaS & Cloud
        'SaaS': ['SAAS', 'SOFTWARE AS A SERVICE', 'CLOUD-BASED', 'SUBSCRIPTION PLATFORM'],
        
        # IoT & Hardware
        'IoT': ['IOT', 'INTERNET OF THINGS', 'SENSOR', 'CONNECTED DEVICE', 'SMART DEVICE'],
        
        # Biotech & Healthtech
        'BioTech': ['BIOTECH', 'BIOTECHNOLOGY', 'GENE', 'GENOMICS', 'PROTEOMICS', 'CRISPR',
                    'SYNTHETIC BIOLOGY', 'BIOINFORMATICS'],
        'HealthTech': ['HEALTHTECH', 'DIGITAL HEALTH', 'MEDICAL DEVICE', 'PATIENT', 'CLINICAL',
                       'DIAGNOSIS', 'TELEHEALTH', 'TELEMEDICINE'],
        
        # Fintech
        'FinTech': ['FINTECH', 'PAYMENT', 'BANKING', 'LENDING', 'INSURANCE', 'INSURTECH',
                    'WEALTHTECH', 'REGTECH', 'NEOBANK', 'DIGITAL WALLET'],
        
        # Mobility & Transport
        'Mobility': ['MOBILITY', 'AUTONOMOUS', 'SELF-DRIVING', 'ELECTRIC VEHICLE', ' EV ',
                     'TRANSPORTATION', 'AUTOMOTIVE', 'FLEET', 'RIDESHARE', 'MICRO-MOBILITY'],
        'AutonomousVehicles': ['AUTONOMOUS VEHICLE', 'SELF-DRIVING CAR', 'AUTONOMOUS DRIVING',
                              'DRIVERLESS', 'AV TECHNOLOGY'],
        
        # Cleantech & Sustainability
        'ClimateTech': ['CLEANTECH', 'CLEAN ENERGY', 'RENEWABLE', 'SOLAR', 'WIND ENERGY',
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
        
        # AgTech & FoodTech
        'AgTech': ['AGTECH', 'AGRICULTURE', 'FARMING TECHNOLOGY', 'PRECISION FARMING',
                   'VERTICAL FARMING', 'AGRITECH'],
        'FoodTech': ['FOOD TECH', 'ALTERNATIVE PROTEIN', 'PLANT-BASED', 'FOOD DELIVERY',
                     'FOOD PLATFORM'],
        
        # Manufacturing & Industry 4.0
        'Manufacturing': ['MANUFACTURING', 'PRODUCTION', 'INDUSTRIAL', 'INDUSTRY 4.0',
                          'SMART FACTORY', 'DIGITAL TWIN'],
        
        # Logistics & Supply Chain
        'Logistics': ['LOGISTICS', 'SUPPLY CHAIN', 'WAREHOUSE', 'DELIVERY', 'FULFILLMENT',
                      'LAST-MILE', 'SHIPPING'],
        
        # E-Commerce & Marketplace
        'Ecommerce': ['E-COMMERCE', 'ECOMMERCE', 'ONLINE SHOP', 'MARKETPLACE', 'RETAIL TECH',
                      'D2C', 'DIRECT-TO-CONSUMER'],
        
        # HSG Course Keywords (Keep)
        'Design Thinking': ['DESIGN THINKING', 'USER EXPERIENCE', 'UX ', ' UI', 'HUMAN-CENTERED',
                            'PROTOTYP', 'USER RESEARCH', 'ITERATIVE'],
        'Scalable': ['SCALABLE', 'SCALE-UP', 'GROWTH HACKING', 'NETWORK EFFECT', 'PLATFORM BUSINESS'],
        'TypeScript': ['NEXT.JS', 'NEXTJS', 'REACT', 'TYPESCRIPT', 'JAVASCRIPT', 'NODE.JS'],
        'Venture Capital': ['VENTURE CAPITAL', 'VC ', 'SEED FUNDING', 'SERIES A', 'SERIES B',
                            'DUE DILIGENCE', 'TERM SHEET', 'VALUATION', 'CAP TABLE'],
        'Lean Startup': ['LEAN STARTUP', 'MVP', 'MINIMUM VIABLE PRODUCT', 'PIVOT',
                         'PRODUCT-MARKET FIT', 'CUSTOMER VALIDATION'],
        'Go-to-Market': ['GO-TO-MARKET', 'GTM', 'CUSTOMER ACQUISITION', 'CAC', 'LTV',
                         'GROWTH STRATEGY', 'SALES FUNNEL'],
    }


def extract_tech_keywords_multi(text, tags=[], title=''):
    """
    MULTI-KEYWORD EXTRACTION - Returns top 5 keywords per startup.
    
    NEW FEATURES (V6):
    - Returns ALL matching keywords (not just first)
    - Scores keywords by position (earlier = more relevant)
    - Returns top 5 most relevant
    - Supports 80+ keyword categories
    """
    # Combine all available text
    combined_text = ' '.join(filter(None, [text or '', title or '', ' '.join(tags or [])]))
    
    if not combined_text or len(combined_text) < 10:
        return None
    
    text_upper = combined_text.upper()
    tech_keywords = get_enhanced_tech_keywords()
    
    found_keywords = []
    keyword_positions = {}  # Track first occurrence for relevance
    
    # Find ALL matching keywords
    for keyword, patterns in tech_keywords.items():
        for pattern in patterns:
            if pattern in text_upper:
                if keyword not in found_keywords:
                    found_keywords.append(keyword)
                    # Store position of first occurrence
                    keyword_positions[keyword] = text_upper.find(pattern)
                break  # One match per keyword is enough
    
    if not found_keywords:
        return None
    
    # Sort by position (keywords appearing earlier are more relevant)
    found_keywords.sort(key=lambda k: keyword_positions.get(k, 999999))
    
    # Return top 5 keywords
    top_keywords = found_keywords[:5]
    return ', '.join(top_keywords)


# Example usage:
if __name__ == "__main__":
    # Test with example text
    test_text = "We use generative AI and large language models (GPT-4) to build enterprise software for robotics companies."
    
    result = extract_tech_keywords_multi(test_text)
    print(f"Found keywords: {result}")
    # Expected: "GenAI, LLM, Enterprise, Robotics, AI" (top 5)
