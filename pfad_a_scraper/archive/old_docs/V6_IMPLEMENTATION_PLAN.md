# V6 SCRAPER ENHANCEMENTS - Implementation Plan

## 🎯 New Features in V6

### 1. ✅ MULTI-KEYWORD EXTRACTION (TOP PRIORITY!)
**Current Problem**: Scrapers only return 1 keyword per startup
**Friend's Data**: Shows 2-4 keywords per startup on average

**Solution**:
```python
# OLD (V5) - Returns only first match
for keyword in tech_keywords:
    if keyword in text:
        return keyword  # ❌ STOPS after first!

# NEW (V6) - Returns ALL matches (top 5)
found_keywords = []
for keyword, patterns in tech_keywords.items():
    for pattern in patterns:
        if pattern in text_upper:
            found_keywords.append(keyword)
            break
return ', '.join(found_keywords[:5])  # ✅ Return top 5
```

### 2. ✅ ADD 22 MISSING KEYWORDS FROM FRIEND'S LIST

#### 2A. High Priority (10 keywords - cover 1,000+ startups)
```python
'GenAI': ['GENERATIVE AI', 'GENAI', 'GPT', 'CHATGPT', 'DALL-E', 
          'STABLE DIFFUSION', 'TEXT-TO-IMAGE', 'MIDJOURNEY'],

'LLM': ['LARGE LANGUAGE MODEL', 'LLM', 'GPT-3', 'GPT-4', 
        'LANGUAGE MODEL', 'TRANSFORMER', 'BERT', 'LLAMA'],

'Infrastructure': ['INFRASTRUCTURE', 'DEVOPS', 'CI/CD', 'KUBERNETES', 
                   'DOCKER', 'MICROSERVICES', 'API PLATFORM'],

'AgentAI': ['AI AGENT', 'AUTONOMOUS AI', 'INTELLIGENT AGENT',
            'MULTI-AGENT', 'AGENTIC'],

'Semiconductors': ['SEMICONDUCTOR', 'CHIP', 'PROCESSOR', 'ASIC', 
                   'FPGA', 'SILICON'],

'Enterprise': ['ENTERPRISE SOFTWARE', 'B2B PLATFORM', 
               'BUSINESS APPLICATION'],

'CreatorEconomy': ['CREATOR ECONOMY', 'CREATOR PLATFORM',
                   'INFLUENCER TOOL', 'CONTENT MONETIZATION'],

'Gaming': ['GAMING', 'VIDEO GAME', 'GAME ENGINE', 'ESPORTS',
           'GAME DEVELOPMENT'],

'PhysicalAI': ['PHYSICAL AI', 'EMBODIED AI', 'ROBOT VISION',
               'HUMANOID ROBOT'],

'DefenseTech': ['DEFENSE', 'MILITARY', 'DEFENSE TECHNOLOGY', 
                'DUAL-USE'],
```

#### 2B. Medium Priority (6 keywords - cover 200+ startups)
```python
'SpaceTech': ['SPACE', 'SATELLITE', 'ROCKET', 'ORBITAL', 'LAUNCH'],

'SocialMedia': ['SOCIAL MEDIA', 'SOCIAL NETWORK', 
                'COMMUNITY PLATFORM'],

'FutureOfWork': ['FUTURE OF WORK', 'REMOTE WORK', 'HYBRID WORK',
                 'PRODUCTIVITY TOOL'],

'ConsumerApps': ['CONSUMER APP', 'MOBILE APP', 'B2C APP'],

'Policy': ['POLICY', 'REGULATORY', 'COMPLIANCE', 'REGTECH'],

'WearableTech': ['WEARABLE', 'SMART WATCH', 'FITNESS TRACKER'],
```

#### 2C. Low Priority (6 keywords - long tail)
```python
'LegalTech': ['LEGALTECH', 'LEGAL TECHNOLOGY', 'CONTRACT AUTOMATION'],

'FusionEnergy': ['FUSION', 'NUCLEAR FUSION', 'TOKAMAK'],

'HRTech': ['HR TECH', 'HRTECH', 'RECRUITMENT', 'TALENT MANAGEMENT'],

'ComputerVision': ['COMPUTER VISION', 'IMAGE RECOGNITION', 
                   'OBJECT DETECTION'],

'DeepTech': ['DEEP TECH', 'DEEPTECH', 'HARD TECH'],

'QuantumTech': ['QUANTUM', 'QUANTUM COMPUTING', 'QUBIT'],
```

### 3. ✅ ADD PUBLICATION_DATE FIELD

**New Schema** (17 fields instead of 16):
```python
required_columns = [
    'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
    'Tech_Keywords', 'Publication_Date',  # ← NEW!
    'Year', 'Funding_Amount', 'Funding_Round',
    'Investment_Stage', 'Investor_Names', 'Location', 'City',
    'Canton', 'Founded_Year', 'Employees', 'Website'
]
```

**Implementation**:
```python
# StartupTicker: Extract from article
date_elem = item.find_element(By.CSS_SELECTOR, 'time, .date, span.meta')
publication_date = date_elem.text.strip()

# VentureKick: Extract from news text
date_pattern = r'(\d{1,2}\s+(?:January|February|...|December)\s+\d{4})'
match = re.search(date_pattern, news_item_text)
publication_date = match.group(1) if match else None
```

### 4. ✅ ENHANCE EXISTING AI CATEGORY

**Current**: AI has basic patterns
**New**: Split into AI, GenAI, LLM, AgentAI, PhysicalAI, ComputerVision

```python
# Keep general AI
'AI': ['AI ', ' AI,', 'ARTIFICIAL INTELLIGENCE', 'KI ',
       'AI-POWERED', 'MACHINE LEARNING', 'ML ', 'DEEP LEARNING'],

# NEW separate categories
'GenAI': [...],  # Generative AI specific
'LLM': [...],     # Language models specific  
'AgentAI': [...], # AI agents specific
'PhysicalAI': [...], # Robotics + AI
'ComputerVision': [...], # Vision AI
```

### 5. ✅ GERMAN LANGUAGE SUPPORT ENHANCED

Add German equivalents for friend's keywords:
```python
'GenAI': ['GENERATIVE AI', 'GENAI', 'GENERATIVE KI'],
'LLM': ['LARGE LANGUAGE MODEL', 'SPRACHMODELL', 'GROSSES SPRACHMODELL'],
'Infrastructure': ['INFRASTRUKTUR', 'DEVOPS'],
'Semiconductors': ['HALBLEITER', 'CHIP', 'PROZESSOR'],
'Gaming': ['GAMING', 'VIDEOSPIEL', 'SPIELEENTWICKLUNG'],
'DefenseTech': ['VERTEIDIGUNG', 'MILITAR', 'DEFENSE'],
'SpaceTech': ['RAUMFAHRT', 'SATELLIT', 'RAKETE'],
```

## 📊 Expected Impact

### Before (V5):
```
StartupTicker V4:
- Tech Keywords: 6.3% (285/4,499)
- Keywords per startup: 0-1
- Missing: GenAI, LLM, Infrastructure, Gaming, etc.

VentureKick V3:
- Tech Keywords: 68.9% (619/899)
- Keywords per startup: 0-1
- Top keyword: TypeScript (181)
```

### After (V6):
```
StartupTicker V6:
- Tech Keywords: 75-85% target (3,375-3,824/4,499)
- Keywords per startup: 2-4 average
- Coverage: ALL 37 friend's keywords

VentureKick V4:
- Tech Keywords: 75-85% target (674-764/899)
- Keywords per startup: 2-4 average
- Top keywords: GenAI, LLM, Infrastructure, TypeScript
```

## 🔧 Technical Changes

### Change 1: Modify extract_tech_keywords_enhanced()
```python
def extract_tech_keywords_enhanced(text, tags=[], title=''):
    combined_text = ' '.join(filter(None, [text or '', title or '', ' '.join(tags or [])]))
    if not combined_text or len(combined_text) < 10:
        return None
    
    text_upper = combined_text.upper()
    
    # Add 22 new keyword categories here
    tech_keywords = {
        # ... existing keywords ...
        
        # NEW: Friend's 22 keywords
        'GenAI': [...],
        'LLM': [...],
        # ... etc ...
    }
    
    found_keywords = []  # ← CHANGED from set() to list
    keyword_positions = {}  # Track first occurrence position
    
    for keyword, patterns in tech_keywords.items():
        for pattern in patterns:
            if pattern in text_upper:
                if keyword not in found_keywords:
                    found_keywords.append(keyword)
                    # Track position for relevance scoring
                    keyword_positions[keyword] = text_upper.find(pattern)
                break
    
    # Sort by position (earlier = more relevant)
    found_keywords.sort(key=lambda k: keyword_positions.get(k, 999999))
    
    # Return top 5 keywords
    return ', '.join(found_keywords[:5]) if found_keywords else None
```

### Change 2: Add Publication_Date to schema mapping
```python
def map_to_schema(news_items):
    # ... existing code ...
    
    mapped_data.append({
        'Startup_Name': startup_name,
        'Industry': industry,
        'Sub_Industry': sub_industry or None,
        'Business_Model_Type': business_model,
        'Tech_Keywords': tech_keywords or None,
        'Publication_Date': item.get('date') or item.get('publication_date'),  # ← NEW
        'Year': year,
        # ... rest of fields ...
    })
    
    required_columns = [
        'Startup_Name', 'Industry', 'Sub_Industry', 'Business_Model_Type',
        'Tech_Keywords', 'Publication_Date',  # ← NEW (17th field)
        'Year', 'Funding_Amount', 'Funding_Round',
        'Investment_Stage', 'Investor_Names', 'Location', 'City',
        'Canton', 'Founded_Year', 'Employees', 'Website'
    ]
```

## 📋 Files to Create

1. **`5_startupticker_scraper_v6_MULTI_KEYWORD.py`**
   - Based on V5
   - Add 22 keywords
   - Multi-keyword extraction
   - Publication date field

2. **`7_venturekick_scraper_v4_MULTI_KEYWORD.py`**
   - Based on V3
   - Add 22 keywords
   - Multi-keyword extraction  
   - Publication date field

## ✅ Validation Plan

After running V6 scrapers:
1. Check keyword coverage: Should be 75-85%
2. Check keywords per startup: Should average 2-4
3. Check new keywords found: GenAI, LLM, Infrastructure, etc.
4. Check publication dates: Should be populated 95%+
5. Compare with friend's keywords: Should cover all 37

## 🚀 Next Steps

1. Create `5_startupticker_scraper_v6_MULTI_KEYWORD.py`
2. Create `7_venturekick_scraper_v4_MULTI_KEYWORD.py`
3. Run both scrapers
4. Compare V5 vs V6 results
5. Validate against friend's 37 keywords
