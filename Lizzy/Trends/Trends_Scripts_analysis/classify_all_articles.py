#!/usr/bin/env python3
"""
Two-Level Keyword Classification System
Classifies articles by Technology and Industry keywords
"""
import csv
import random
from collections import defaultdict, Counter

# File paths
base_path = "/Users/nataliekmecova/Documents/tech_trends_project/tech_trends"
input_file = f"{base_path}/data/02_Trendricker_Natalie/articles_raw_merged.csv"
output_t1 = f"{base_path}/data/02_Trendricker_Natalie/articles_classified_t1.csv"
output_t2 = f"{base_path}/data/05_JoinData_Natalie&ChiaraV2/articles_classified_t2.csv"
output_monthly = f"{base_path}/data/02_Trendricker_Natalie/keyword_monthly_normalized.csv"
output_validation = f"{base_path}/data/02_Trendricker_Natalie/validation_sample.csv"

# TECHNOLOGY KEYWORDS
tech_keywords = {
    "GenAI": [
        "generative ai", "generative", "text generation", "image generation",
        "video generation", "chatgpt", "gpt-4", "gpt-3", "gpt4", "gpt3",
        "dall-e", "midjourney", "stable diffusion", "foundation model",
        "text-to-image", "text-to-video", "claude", "anthropic",
        "gemini", "llama", "mistral", "content generation"
    ],
    "AgentAI": [
        "ai agent", "ai agents", "agentic", "autonomous agent",
        "multi-agent", "agent workflow", "autogpt", "auto-gpt", "babyagi",
        "copilot", "assistant agent", "coding agent", "coding assistant"
    ],
    "LLM": [
        "llm", "large language model", "language model", "transformer",
        "fine-tuning", "fine tuning", "retrieval augmented", "retrieval-augmented",
        "open source model", "pre-trained model", "model training", "inference"
    ],
    "Robotics": [
        "robot", "humanoid", "robotic", "autonomous robot",
        "warehouse robot", "delivery robot", "industrial robot",
        "physical robot", "robot arm", "robotic automation"
    ],
    "Semiconductors": [
        "chip", "semiconductor", "gpu", "tpu", "processor",
        "nvidia", "silicon", "foundry", "fabless", "arm chip",
        "inference chip", "ai chip", "hardware accelerator",
        "integrated circuit"
    ],
    "ComputerVision": [
        "computer vision", "image recognition", "object detection",
        "visual ai", "vision model", "image classification",
        "video analysis", "facial recognition"
    ],
    "PhysicalAI": [
        "physical ai", "embodied ai", "self-driving",
        "autonomous vehicle", "autonomous driving", "driverless"
    ],
    "Web3": [
        "web3", "blockchain", "nft", "defi", "decentralized",
        "crypto", "dao", "token", "ethereum", "bitcoin",
        "cryptocurrency", "web 3", "smart contract"
    ],
    "QuantumTech": [
        "quantum", "quantum computing", "qubit",
        "quantum chip", "quantum algorithm"
    ],
    "Cybersecurity": [
        "cybersecurity", "cyber security", "data breach", "ransomware",
        "firewall", "zero trust", "threat detection", "malware",
        "vulnerability", "phishing", "encryption", "hacker attack",
        "security breach", "endpoint security"
    ],
    "Infrastructure": [
        "cloud infrastructure", "data center", "mlops",
        "developer tools", "devops", "open source platform",
        "compute infrastructure", "aws", "azure", "gcp",
        "api platform", "microservices", "kubernetes"
    ]
}

# INDUSTRY KEYWORDS
industry_keywords = {
    "HealthTech": [
        "digital health", "health record", "mental health", "femtech",
        "health ai", "medical ai", "patient care", "hospital",
        "healthcare", "pharma", "wellness platform"
    ],
    "FinTech": [
        "payment", "banking", "neobank", "lending", "insurtech",
        "wealth management", "fintech", "financial technology",
        "embedded finance", "open banking", "trading platform",
        "insurance tech", "mortgage tech", "invoice financing"
    ],
    "ClimateTech": [
        "climate tech", "clean energy", "solar", "carbon capture",
        "sustainability", "net zero", "renewable energy", "cleantech",
        "green energy", "ev battery", "circular economy",
        "emissions reduction", "wind energy", "nuclear fusion",
        "energy storage", "climate startup"
    ],
    "DefenseTech": [
        "defense tech", "defence", "military", "national security",
        "surveillance", "pentagon", "nato", "dual-use technology",
        "warfare", "drone warfare", "autonomous weapons"
    ],
    "EdTech": [
        "edtech", "education technology", "e-learning", "online learning",
        "tutoring platform", "curriculum platform", "learning management",
        "university platform", "classroom technology", "teaching tools"
    ],
    "HRTech": [
        "hr tech", "human resources software", "recruiting platform",
        "talent management", "payroll software", "hiring platform",
        "workforce management", "remote work platform",
        "future of work", "employee platform"
    ],
    "LegalTech": [
        "legaltech", "legal software", "contract management",
        "compliance software", "law firm tech", "e-discovery",
        "legal ai", "regulatory technology", "regtech"
    ],
    "AgriTech": [
        "food tech", "alternative protein", "plant-based food",
        "agritech", "vertical farming", "precision agriculture",
        "food startup", "crop technology", "food delivery platform"
    ],
    "SpaceTech": [
        "spacex", "rocket launch", "satellite technology", "orbital",
        "nasa", "lunar mission", "aerospace startup",
        "launch vehicle", "space tech", "starlink"
    ],
    "Ecommerce": [
        "ecommerce", "e-commerce", "online marketplace",
        "retail tech", "direct-to-consumer", "shopify",
        "logistics tech", "supply chain tech", "last mile delivery"
    ],
    "Enterprise": [
        "enterprise software", "b2b platform", "fortune 500",
        "workflow automation", "erp system", "crm platform",
        "business intelligence", "enterprise ai", "saas b2b"
    ],
    "CreatorEconomy": [
        "creator economy", "content creator platform", "influencer marketing",
        "newsletter platform", "podcast platform", "youtube creator",
        "tiktok creator", "streaming platform", "creator monetization"
    ],
    "GameTech": [
        "gaming platform", "video game", "esports", "game engine",
        "mobile gaming", "game studio", "metaverse gaming",
        "vr gaming", "ar gaming", "game developer tools"
    ],
    "MobilityTech": [
        "autonomous vehicle", "self-driving car", "waymo",
        "electric vehicle startup", "rivian", "urban mobility",
        "ride sharing", "robotaxi service", "transportation tech",
        "mobility startup"
    ],
    "BioTech": [
        "biotech", "biopharma", "drug discovery", "genomics", "gene therapy",
        "crispr", "synthetic biology", "life science", "clinical trial",
        "oncology", "cancer therapy", "antibody", "bioinformatics"
    ],
    "MedTech": [
        "medtech", "medical device", "diagnostics", "patient monitoring",
        "surgical robot", "imaging system", "in vitro", "point of care",
        "wearable health", "implant"
    ],
    "DigitalHealth": [
        "digital health", "telehealth", "telemedicine", "mental health platform",
        "health data", "electronic health record", "ehr", "remote patient",
        "health app", "wellness platform", "longevity"
    ],
    "PropTech": [
        "proptech", "real estate tech", "property technology",
        "smart building", "construction tech", "contech", "real estate platform"
    ]
}

# SPECIFIC TERMS (single match sufficient)
specific_terms = [
    "chatgpt", "gpt-4", "dall-e", "midjourney", "anthropic", "claude",
    "gemini", "llama", "autogpt", "nvidia", "spacex", "waymo", "rivian",
    "crispr", "genomics", "blockchain", "ethereum", "nato", "pentagon",
    "openai", "deepmind", "hugging face", "mistral", "stability ai"
]

print("=" * 90)
print("TWO-LEVEL KEYWORD CLASSIFICATION SYSTEM")
print("=" * 90)

# Step 1: Read articles
print("\n[1/8] Reading articles...")
articles = []
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)
    print(f"  ✓ Loaded {len(articles)} articles")
except FileNotFoundError:
    print(f"  ✗ File not found: {input_file}")
    exit(1)

# Step 2: Define classification function
print("\n[2/8] Defining classification function...")

def classify_article(article, threshold):
    """Classify article with given threshold (1 or 2)"""
    # Get text (prefer article_text, fallback to excerpt+title)
    text = article.get('article_text', '')
    if not text or len(text.strip()) < 10:
        text = (article.get('article_excerpt', '') + ' ' + article.get('title', '')).lower()
    else:
        text = text.lower()
    
    tech_layer = []
    industry_layer = []
    
    # Classify technology keywords
    for category, keywords in tech_keywords.items():
        match_count = sum(1 for kw in keywords if kw in text)
        
        if match_count >= threshold:
            tech_layer.append(category)
    
    # Classify industry keywords
    for category, keywords in industry_keywords.items():
        match_count = sum(1 for kw in keywords if kw in text)
        
        if match_count >= threshold:
            industry_layer.append(category)
    
    return ";".join(tech_layer), ";".join(industry_layer)

print("  ✓ Classification function defined")

# Step 3: Classify with threshold 1
print("\n[3/8] Classifying with threshold=1...")
classified_t1 = []
for article in articles:
    tech, industry = classify_article(article, threshold=1)
    classified_t1.append({
        **article,
        'tech_layer': tech,
        'industry_layer': industry,
        'total_tech_keywords': len(tech.split(';')) if tech else 0,
        'total_industry_keywords': len(industry.split(';')) if industry else 0
    })

coverage_t1 = sum(1 for a in classified_t1 if a['tech_layer'] or a['industry_layer'])
pct_t1 = 100 * coverage_t1 / len(classified_t1)
print(f"  ✓ Classified {len(classified_t1)} articles (coverage: {pct_t1:.1f}%)")

# Step 4: Classify with threshold 2
print("\n[4/8] Classifying with threshold=2...")
classified_t2 = []
for article in articles:
    tech, industry = classify_article(article, threshold=2)
    classified_t2.append({
        **article,
        'tech_layer': tech,
        'industry_layer': industry,
        'total_tech_keywords': len(tech.split(';')) if tech else 0,
        'total_industry_keywords': len(industry.split(';')) if industry else 0
    })

coverage_t2 = sum(1 for a in classified_t2 if a['tech_layer'] or a['industry_layer'])
pct_t2 = 100 * coverage_t2 / len(classified_t2)
print(f"  ✓ Classified {len(classified_t2)} articles (coverage: {pct_t2:.1f}%)")

#Step 5: Save outputs with threshold 1 and 2
print("\n[5/8] Saving classification outputs...")

# Get all columns plus new ones
all_columns = list(articles[0].keys()) + ['tech_layer', 'industry_layer', 'total_tech_keywords', 'total_industry_keywords']

with open(output_t1, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=all_columns)
    writer.writeheader()
    writer.writerows(classified_t1)
print(f"  ✓ Saved {output_t1}")

with open(output_t2, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=all_columns)
    writer.writeheader()
    writer.writerows(classified_t2)
print(f"  ✓ Saved {output_t2}")

# Step 6: Create validation sample
print("\n[6/8] Creating validation sample (random_state=42)...")
random.seed(42)
sample_indices = random.sample(range(len(classified_t2)), min(50, len(classified_t2)))
validation_sample = [classified_t2[i] for i in sorted(sample_indices)]

with open(output_validation, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'article_excerpt', 'tech_layer', 'industry_layer'])
    writer.writeheader()
    for article in validation_sample:
        writer.writerow({
            'title': article.get('title', ''),
            'article_excerpt': article.get('article_excerpt', ''),
            'tech_layer': article.get('tech_layer', ''),
            'industry_layer': article.get('industry_layer', '')
        })
print(f"  ✓ Saved validation sample: {output_validation}")

# Step 7: Create monthly aggregation
print("\n[7/8] Creating monthly keyword aggregation...")

# Use threshold 2 for aggregation
monthly_data = defaultdict(int)
monthly_totals = defaultdict(int)

for article in classified_t2:
    year_month = article.get('year_month', '')
    source = article.get('source', '')
    tech_layer = article.get('tech_layer', '')
    industry_layer = article.get('industry_layer', '')
    
    if not year_month or not source:
        continue
    
    # Count this article
    monthly_totals[(year_month, source)] += 1
    
    # Count tech keywords
    if tech_layer:
        for tech in tech_layer.split(';'):
            if tech:
                monthly_data[(year_month, source, 'tech', tech)] += 1
    
    # Count industry keywords
    if industry_layer:
        for ind in industry_layer.split(';'):
            if ind:
                monthly_data[(year_month, source, 'industry', ind)] += 1

# Build normalized output
monthly_output = []
for (year_month, source, kw_type, keyword), count in monthly_data.items():
    total = monthly_totals[(year_month, source)]
    pct = 100 * count / total if total > 0 else 0
    
    if kw_type == 'tech':
        monthly_output.append({
            'year_month': year_month,
            'source': source,
            'tech_keyword': keyword,
            'industry_keyword': '',
            'article_count': count,
            'total_articles_that_month': total,
            'keyword_pct': f"{pct:.1f}"
        })
    else:
        monthly_output.append({
            'year_month': year_month,
            'source': source,
            'tech_keyword': '',
            'industry_keyword': keyword,
            'article_count': count,
            'total_articles_that_month': total,
            'keyword_pct': f"{pct:.1f}"
        })

with open(output_monthly, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['year_month', 'source', 'tech_keyword', 'industry_keyword', 'article_count', 'total_articles_that_month', 'keyword_pct'])
    writer.writeheader()
    writer.writerows(sorted(monthly_output, key=lambda x: (x['year_month'], x['source'])))
print(f"  ✓ Saved monthly aggregation: {output_monthly}")

# Step 8: Print statistics
print("\n[8/8] Generating statistics...")

print("\n" + "=" * 90)
print("CLASSIFICATION SUMMARY")
print("=" * 90)

print(f"\nThreshold Robustness Check:")
print(f"  Threshold 1 (any match):  {coverage_t1:5d} articles ({pct_t1:5.1f}%)")
print(f"  Threshold 2 (2+ match):   {coverage_t2:5d} articles ({pct_t2:5.1f}%)")
difference = pct_t1 - pct_t2
print(f"  Difference:               {difference:5.1f}%")
if difference < 10:
    print(f"  ✓ Robust (<10% difference) — using Threshold 2 for aggregation")
else:
    print(f"  ⚠ High difference (>10%) — threshold has significant impact")

# Coverage by year (T2)
print(f"\nCoverage by Year (Threshold 2):")
year_coverage = defaultdict(lambda: {'total': 0, 'classified': 0})
for article in classified_t2:
    year = article.get('year', '')
    if year:
        year_coverage[year]['total'] += 1
        if article['tech_layer'] or article['industry_layer']:
            year_coverage[year]['classified'] += 1

for year in sorted(year_coverage.keys()):
    stats = year_coverage[year]
    pct = 100 * stats['classified'] / stats['total'] if stats['total'] > 0 else 0
    print(f"  {year}: {stats['classified']:4d}/{stats['total']:4d} ({pct:5.1f}%)")

# Coverage by source (T2)
print(f"\nCoverage by Source (Threshold 2):")
source_coverage = defaultdict(lambda: {'total': 0, 'classified': 0})
for article in classified_t2:
    source = article.get('source', '')
    if source:
        source_coverage[source]['total'] += 1
        if article['tech_layer'] or article['industry_layer']:
            source_coverage[source]['classified'] += 1

for source in sorted(source_coverage.keys()):
    stats = source_coverage[source]
    pct = 100 * stats['classified'] / stats['total'] if stats['total'] > 0 else 0
    print(f"  {source:12s}: {stats['classified']:4d}/{stats['total']:4d} ({pct:5.1f}%)")

# Top 15 tech keywords
print(f"\nTop 15 Tech Keywords (Threshold 2):")
tech_counter = Counter()
for article in classified_t2:
    if article['tech_layer']:
        for tech in article['tech_layer'].split(';'):
            if tech:
                tech_counter[tech] += 1

for i, (tech, count) in enumerate(tech_counter.most_common(15), 1):
    pct = 100 * count / len(classified_t2)
    print(f"  {i:2d}. {tech:20s} {count:4d} ({pct:5.1f}%)")

# Top 15 industry keywords
print(f"\nTop 15 Industry Keywords (Threshold 2):")
industry_counter = Counter()
for article in classified_t2:
    if article['industry_layer']:
        for ind in article['industry_layer'].split(';'):
            if ind:
                industry_counter[ind] += 1

for i, (ind, count) in enumerate(industry_counter.most_common(15), 1):
    pct = 100 * count / len(classified_t2)
    print(f"  {i:2d}. {ind:20s} {count:4d} ({pct:5.1f}%)")

# Top 20 co-occurrences
print(f"\nTop 20 Tech + Industry Co-occurrences (Threshold 2):")
cooccurrence = Counter()
for article in classified_t2:
    if article['tech_layer'] and article['industry_layer']:
        techs = article['tech_layer'].split(';')
        inds = article['industry_layer'].split(';')
        for tech in techs:
            for ind in inds:
                if tech and ind:
                    cooccurrence[f"{tech}+{ind}"] += 1

for i, (pair, count) in enumerate(cooccurrence.most_common(20), 1):
    tech, ind = pair.split('+')
    print(f"  {i:2d}. {tech:20s} + {ind:20s} {count:4d}")

# Validation sample showcase
print(f"\nValidation Sample (5 random articles for spot-checking):")
print("-" * 90)
for i, article in enumerate(validation_sample[:5], 1):
    print(f"\n{i}. {article['title'][:70]}")
    print(f"   Tech: {article['tech_layer'] if article['tech_layer'] else '(none)'}")
    print(f"   Ind:  {article['industry_layer'] if article['industry_layer'] else '(none)'}")

print("\n" + "=" * 90)
print("✓ CLASSIFICATION COMPLETE")
print("=" * 90)
