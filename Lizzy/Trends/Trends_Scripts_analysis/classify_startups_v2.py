#!/usr/bin/env python3
"""
Startup Classification System
Classifies startup articles by Technology and Industry keywords
"""
import csv
from collections import defaultdict, Counter

# File paths
base_path = "/Users/nataliekmecova/Documents/tech_trends_project/tech_trends"
input_file = f"{base_path}/data/01_Startupticker_Chiara/startupticker_raw_articles_v7_step1_FINANCING.csv"
output_file = f"{base_path}/data/05_JoinData_Natalie&ChiaraV2/startups_classified_v2.csv"

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
print("STARTUP CLASSIFICATION SYSTEM")
print("=" * 90)

# Step 1: Read articles
print("\n[1/4] Reading startup articles...")
articles = []
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)
    print(f"  ✓ Loaded {len(articles)} startup articles")
except FileNotFoundError:
    print(f"  ✗ File not found: {input_file}")
    exit(1)

# Step 2: Define classification function
print("\n[2/4] Defining classification function...")

def classify_article(article, threshold):
    """Classify article with given threshold"""
    # Get text from Article_Text column
    text = article.get('Article_Text', '').lower()
    
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
print("\n[3/4] Classifying with threshold=1...")
classified = []
for article in articles:
    tech, industry = classify_article(article, threshold=1)
    classified.append({
        'URL': article.get('URL', ''),
        'Title': article.get('Title', ''),
        'Publication_Date': article.get('Publication_Date', ''),
        'Year': article.get('Year', ''),
        'tech_layer': tech,
        'industry_layer': industry,
        'total_tech_keywords': len(tech.split(';')) if tech else 0,
        'total_industry_keywords': len(industry.split(';')) if industry else 0,
    })

coverage = sum(1 for a in classified if a['tech_layer'] or a['industry_layer'])
pct = 100 * coverage / len(classified)
print(f"  ✓ Classified {len(classified)} articles (coverage: {pct:.1f}%)")

# Step 4: Save output
print("\n[4/4] Saving classification results...")

output_columns = ['URL', 'Title', 'Publication_Date', 'Year', 'tech_layer', 
                  'industry_layer', 'total_tech_keywords', 'total_industry_keywords']

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=output_columns)
    writer.writeheader()
    writer.writerows(classified)
print(f"  ✓ Saved {output_file}")

# Print statistics
print("\n" + "=" * 90)
print("CLASSIFICATION SUMMARY")
print("=" * 90)

print(f"\nCoverage Statistics:")
print(f"  Total articles:       {len(classified):5d}")
print(f"  Classified articles:  {coverage:5d} ({pct:5.1f}%)")
print(f"  Unclassified:         {len(classified) - coverage:5d} ({100 - pct:5.1f}%)")

# Coverage by year
print(f"\nCoverage by Year:")
year_coverage = defaultdict(lambda: {'total': 0, 'classified': 0})
for article in classified:
    year = article.get('Year', '')
    if year:
        year_coverage[year]['total'] += 1
        if article['tech_layer'] or article['industry_layer']:
            year_coverage[year]['classified'] += 1

for year in sorted(year_coverage.keys()):
    stats = year_coverage[year]
    pct_year = 100 * stats['classified'] / stats['total'] if stats['total'] > 0 else 0
    print(f"  {year}: {stats['classified']:4d}/{stats['total']:4d} ({pct_year:5.1f}%)")

# Top 15 tech keywords
print(f"\nTop 15 Tech Keywords:")
tech_counter = Counter()
for article in classified:
    if article['tech_layer']:
        for tech in article['tech_layer'].split(';'):
            if tech:
                tech_counter[tech] += 1

for i, (tech, count) in enumerate(tech_counter.most_common(15), 1):
    pct_kw = 100 * count / len(classified)
    print(f"  {i:2d}. {tech:20s} {count:4d} ({pct_kw:5.1f}%)")

# Top 15 industry keywords
print(f"\nTop 15 Industry Keywords:")
industry_counter = Counter()
for article in classified:
    if article['industry_layer']:
        for ind in article['industry_layer'].split(';'):
            if ind:
                industry_counter[ind] += 1

for i, (ind, count) in enumerate(industry_counter.most_common(15), 1):
    pct_kw = 100 * count / len(classified)
    print(f"  {i:2d}. {ind:20s} {count:4d} ({pct_kw:5.1f}%)")

print("\n" + "=" * 90)
print("✓ STARTUP CLASSIFICATION COMPLETE")
print("=" * 90)
