"""
Datenbereinigung Indeed Jobs – MBI Berufsfelder HSG
====================================================
Schritt 1: Requirements normalisieren (Requirements aus Jobbeschrieb extrahieren)
Schritt 2: Relevanzfilter basierend auf Requirements (nicht Titel)
Schritt 3: Keyword/Skill-Extraktion (statistisch via TF-IDF + n-grams)
Schritt 4: Export als bereinigte CSVs
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# ─── Config ───────────────────────────────────────────────────────────────────
INPUT_FILE = "indeed_jobs.csv"
OUTPUT_CLEAN = "indeed_jobs_bereinigt.csv"
OUTPUT_SKILLS = "skill_haeufigkeiten.csv"

# ─── Schritt 0: Daten laden ──────────────────────────────────────────────────
print("=" * 60)
print("SCHRITT 0: Daten laden")
print("=" * 60)
df = pd.read_csv(INPUT_FILE)
print(f"Geladene Jobs: {len(df)}")
print(f"Verteilung:\n{df['job_profil'].value_counts().to_string()}\n")

# ─── Schritt 1: Requirements normalisieren ───────────────────────────────────
print("=" * 60)
print("SCHRITT 1: Requirements normalisieren")
print("=" * 60)

# Patterns die den Anforderungs-Abschnitt markieren (DE + EN)
REQUIREMENT_SECTION_PATTERNS = [
    # Deutsch
    r'(?:^|\n)\s*(?:anforderungen|dein\s*profil|ihr\s*profil|'
    r'was\s*(?:du|sie)\s*mitbring(?:st|en)|what\s*you\s*bring|'
    r'qualifikation(?:en)?|'
    r'was\s*wir\s*(?:uns\s*)?(?:von\s*dir\s*)?(?:er)?warten|'
    r'das\s*bringst\s*du\s*mit|das\s*bringen\s*sie\s*mit|'
    r'ihre?\s*(?:fähigkeiten|kompetenzen|erfahrung)|'
    r'was\s*(?:dich|sie)\s*auszeichnet|'
    r'voraussetzungen|unsere\s*anforderungen|'
    r'das\s*erwarten\s*wir|das\s*zeichnet\s*(?:dich|sie)\s*aus|'
    r'dein\s*(?:skill|können|hintergrund)|'
    r'das\s*solltest\s*du\s*mitbringen|'
    r'so\s*überzeugst\s*du\s*uns|damit\s*überzeugst\s*du)\s*[:\-]?\s*\n',
    # Englisch
    r'(?:^|\n)\s*(?:requirements|'
    r'your\s*(?:profile|skills|qualifications|experience|background)|'
    r'we\s*(?:are\s*)?look(?:ing)?\s*for|'
    r'(?:must|should)\s*have|nice\s*to\s*have|'
    r'(?:minimum|required|desired)\s*qualifications|'
    r'who\s*you\s*are|what\s*we\s*expect|about\s*you|'
    r'you\s*(?:will\s*)?(?:ideally\s*)?(?:have|bring))\s*[:\-]?\s*\n',
]
req_section_re = re.compile('|'.join(REQUIREMENT_SECTION_PATTERNS), re.IGNORECASE | re.MULTILINE)

# Patterns that mark the END of requirements (start of a new section)
END_SECTION_PATTERNS = [
    r'(?:^|\n)\s*(?:was\s*wir\s*(?:dir\s*)?bieten|what\s*we\s*offer|'
    r'wir\s*bieten|we\s*offer|our\s*offer|unser\s*angebot|'
    r'benefits|your\s*benefits|deine\s*vorteile|ihre\s*vorteile|'
    r'warum\s*(?:du|sie)|why\s*(?:join|us|you)|'
    r'(?:über|about)\s*(?:uns|(?:the\s*)?company)|'
    r'bewirb\s*dich|jetzt\s*bewerben|apply\s*now|how\s*to\s*apply|'
    r'kontakt|contact|aufgaben|your\s*(?:tasks|responsibilities)|'
    r'ihre?\s*aufgaben|your\s*role|deine?\s*(?:aufgaben|rolle|role)|'
    r'verantwortlichkeiten|responsibilities|'
    r'(?:dein|ihr)e?\s*(?:aufgaben|rolle|role|verantwortung)|'
    r'(?:das|wir)\s*bieten\s*(?:wir\s*)?(?:dir|ihnen)|'
    r'stellenbeschreibung|job\s*description|'
    r'(?:so\s*)?(?:bewirbst\s*du\s*dich|bewerben\s*sie\s*sich))\s*[:\-]?\s*\n',
]
end_section_re = re.compile('|'.join(END_SECTION_PATTERNS), re.IGNORECASE | re.MULTILINE)


def extract_requirements(row):
    """Extract requirements from the best available source."""
    req = str(row['requirements']).strip()
    desc = str(row['full_description']).strip()

    # If requirements != full_description AND not too long, scraper already extracted them
    if req != desc and len(req) > 50 and len(req) < 3000:
        return req

    # Use full_description (or requirements if same) and try to extract
    text = desc if desc and desc != 'nan' else req

    # Try all requirement section markers
    matches = list(req_section_re.finditer(text))
    best_extract = ""

    for match in matches:
        start = match.end()
        # Find end of requirements section
        end_match = end_section_re.search(text[start:])
        if end_match:
            extracted = text[start:start + end_match.start()].strip()
        else:
            # Take max 3000 chars from match point
            extracted = text[start:start + 3000].strip()

        # Pick the longest meaningful extraction
        if len(extracted) > len(best_extract) and len(extracted) > 50:
            best_extract = extracted

    if best_extract:
        return best_extract

    # If requirements were already separated but long, still use them
    if req != desc and len(req) > 50:
        return req

    # Fallback: use full text (will still be processed for keywords)
    return req


df['requirements_clean'] = df.apply(extract_requirements, axis=1)

# Stats
already_good = ((df['requirements'] != df['full_description']) &
                (df['requirements'].str.len() < 3000)).sum()
extracted_new = (df['requirements_clean'] != df['requirements']).sum()
still_long = (df['requirements_clean'].str.len() > 3000).sum()

print(f"Requirements bereits separiert (< 3000 Zeichen): {already_good}")
print(f"Requirements neu extrahiert/verbessert: {extracted_new}")
print(f"Requirements noch lang (> 3000 Zeichen): {still_long}")

# Show average lengths
print(f"\nDurchschn. Länge vorher: {df['requirements'].str.len().mean():.0f} Zeichen")
print(f"Durchschn. Länge nachher: {df['requirements_clean'].str.len().mean():.0f} Zeichen")
print()

# ─── Schritt 2: Relevanzfilter basierend auf Requirements ────────────────────
print("=" * 60)
print("SCHRITT 2: Relevanzfilter (basierend auf Requirements)")
print("=" * 60)

# MBI Master HSG Profil:
# - Business Innovation, Digitale Transformation, IT Management
# - Business Development, Strategy, Consulting
# - Data Analytics, Business Intelligence (nicht Data Engineering)
# - Projekt-/Produktmanagement (Agile, Scrum)
# - Digital Marketing, Digital Channels
# - Supply Chain / Operations Management
# - Entrepreneurship, Startups

# ── NEGATIVE Signale in Requirements (klar NICHT MBI) ──
# Wenn Requirements diese Muster stark zeigen → ausschliessen

EXCLUDE_REQ_PATTERNS = [
    # ── Reine Entwickler-/Programmierer-Anforderungen ──
    # (mehrere Programmiersprachen als Kernanforderung)
    (r'(?:proficiency|experience|expertise|kenntnisse)\s+(?:in|with|mit)\s+'
     r'(?:java|python|c\+\+|c#|ruby|golang|rust|php|kotlin|swift|objective-c)\b', -3),
    (r'\b(?:3|4|5|6|7|8|9|10)\+?\s*(?:years?|jahre?)\s*(?:of\s*)?'
     r'(?:software|programming|entwicklung|coding|development)\s*(?:experience|erfahrung)\b', -3),
    (r'\bwrite\s*(?:clean|maintainable|production)?\s*code\b', -2),
    (r'\bclean\s*code\b', -1),
    (r'\bcode\s*review\b', -2),
    (r'\bgit(?:hub|lab)?\s*(?:actions?|ci|pipeline)\b', -1),
    (r'\bunit\s*test(?:s|ing)?\b', -2),
    (r'\btest[\s-]*driven\s*development\b', -2),
    (r'\bci\s*/?\s*cd\s*pipeline\b', -2),
    (r'\bkubernetes\b', -2),
    (r'\bdocker\b', -1),
    (r'\bmicroservices?\b', -2),
    (r'\brest\s*(?:ful)?\s*api\b', -1),
    (r'\bfrontend\s*(?:framework|development|entwicklung)\b', -2),
    (r'\bbackend\s*(?:framework|development|entwicklung)\b', -2),
    (r'\breact\b.*\bangular\b|\bangular\b.*\breact\b', -2),  # multiple JS frameworks
    (r'\btypescript\b.*\breact\b|\breact\b.*\btypescript\b', -2),
    (r'\bios\s*(?:development|entwicklung|sdk)\b', -3),
    (r'\bandroid\s*(?:development|entwicklung|sdk)\b', -3),
    (r'\bmobile\s*(?:app\s*)?(?:development|entwicklung)\b', -2),
    (r'\bcomputer\s*science\s*(?:degree|abschluss|studium)\b', -2),
    (r'\binformatik(?:studium|-studium|abschluss|-abschluss)\b', -1),

    # ── Handwerk, Gastronomie, Pflege, Detailhandel ──
    # Pflege: nur medizinisch/Pflege als Beruf, NICHT "Kundenpflege", "Datenpflege" etc.
    (r'\b(?:koch|köchin|sous\s*chef|küchenchef|bäcker|konditor)\b', -5),
    (r'\b(?:kellner|servicemitarbeiter|barista)\b', -5),
    (r'\b(?:pflegefach(?:person|frau|mann)|krankenpflege|pflegepersonal|pflegedienst|spitex)\b', -5),
    (r'\b(?:chauffeur|lkw[\s-]?fahrer|lastwagen[\s-]?fahrer|lieferfahrer)\b', -5),
    (r'\b(?:verkäufer|verkäuferin)\b(?!.*(?:manage|strateg|digital))', -4),
    (r'\b(?:monteur|elektriker|sanitär|installateur|schreiner|mechaniker|maurer)\b', -5),
    (r'\b(?:zolldeklarant|speditionsleiter)\b', -4),
    (r'\b(?:arztsekretärin|medizinische\s*praxisassistentin|mpa)\b', -5),
    (r'\b(?:coiffeur|coiffeuse|friseur|friseurin)\b', -5),
    (r'\breinigung(?:skraft|spersonal|sdienst)\b', -4),
    (r'\b(?:führerschein\s*(?:kat|kategorie)\s*(?:c|ce|d))\b', -3),
    (r'\b(?:efz\s*im\s*detailhandel|berufslehre\s*im\s*detailhandel)\b', -4),
    (r'\bgastronomie(?:betrieb|erfahrung|branche)\b', -4),

    # ── Reine Wissenschaft / PhD-Stellen ──
    (r'\b(?:doktorand|phd\s*student|dissertation|promotion)\b', -3),
    (r'\b(?:postdoc|post-doctoral|habilitation)\b', -4),
    (r'\bwissenschaftliche[rn]?\s*(?:assistent|mitarbeiter)\b', -3),

    # ── Reine Design/Creative (ohne Business) ──
    (r'\b(?:graphic\s*design|grafikdesign|illustrat(?:or|ion))\b', -3),
    (r'\b(?:ux\s*design(?:er)?|ui\s*design(?:er)?|visual\s*design(?:er)?)\b', -2),
    (r'\b(?:adobe\s*(?:photoshop|illustrator|indesign))\b', -2),
    (r'\bfigma\b.*\bsketch\b|\bsketch\b.*\bfigma\b', -1),

    # ── Reine Finanzmathematik / Aktuariat ──
    (r'\b(?:aktuar|actuari(?:al|y)|versicherungsmathematik)\b', -3),
    (r'\b(?:cfa\s*charter|frm\s*certification)\b', -2),

    # ── Deep technical security/network engineering ──
    (r'\b(?:penetration\s*test|pentest|ethical\s*hack)\b', -3),
    (r'\b(?:ccna|ccnp|ccie)\b', -2),
    (r'\b(?:firewall\s*(?:administration|config)|netzwerktechnik)\b', -2),
]

# ── POSITIVE Signale in Requirements (klar MBI-relevant) ──
INCLUDE_REQ_PATTERNS = [
    # ── Bildung / Studium ──
    (r'\b(?:business\s*(?:administration|innovation|management)|bwl|betriebswirtschaft)\b', +3),
    (r'\b(?:wirtschaftsinformatik|information\s*systems|management\s*information)\b', +4),
    (r'\b(?:wirtschaftswissenschaft|ökonomie|economics|vwl)\b', +2),
    (r'\b(?:mba|master\s*(?:in\s*)?(?:business|management))\b', +3),

    # ── Digitale Transformation / Innovation ──
    (r'\b(?:digital(?:e|er)?\s*transformation)\b', +3),
    (r'\b(?:digital(?:e|er)?\s*(?:business|strategie|strategy))\b', +3),
    (r'\b(?:innovation(?:s)?(?:management)?)\b', +2),
    (r'\b(?:change\s*management)\b', +2),
    (r'\b(?:design\s*thinking)\b', +2),

    # ── Projektmanagement ──
    (r'\b(?:projekt(?:management|leitung|manager|leiter)|project\s*manag(?:ement|er))\b', +3),
    (r'\b(?:agile?|scrum|kanban|safe)\b', +2),
    (r'\b(?:product\s*(?:owner|manager|management))\b', +3),
    (r'\b(?:prince2|pmp|ipma)\b', +2),

    # ── Business Development / Strategie ──
    (r'\b(?:business\s*develop(?:ment|er)?)\b', +3),
    (r'\b(?:strategi(?:e|c|sch)|strategy)\b', +2),
    (r'\b(?:consulting|beratung|consultant|berater)\b', +2),
    (r'\b(?:stakeholder\s*management)\b', +2),

    # ── Datenanalyse / BI (nicht Data Engineering) ──
    (r'\b(?:data\s*analy(?:tics|sis|se)|datenanalyse)\b', +2),
    (r'\b(?:business\s*intelligence|bi[\s\-]?tool)\b', +3),
    (r'\b(?:power\s*bi|tableau|looker)\b', +2),
    (r'\b(?:kpi|dashboards?|reporting)\b', +1),
    (r'\b(?:sql)\b', +1),

    # ── IT Management / Governance ──
    (r'\b(?:it[\s\-]?management|it[\s\-]?governance|it[\s\-]?strateg)\b', +3),
    (r'\b(?:it[\s\-]?(?:service|operations?)\s*manag)\b', +3),
    (r'\b(?:itil|cobit|togaf)\b', +2),
    (r'\b(?:erp|sap)\b.*\b(?:manag|berat|consult|projekt|implement)\b', +2),
    (r'\b(?:enterprise\s*architecture)\b', +2),

    # ── Digital Marketing / Channels ──
    (r'\b(?:digital\s*marketing)\b', +2),
    (r'\b(?:crm|customer\s*relationship\s*management)\b', +2),
    (r'\b(?:e[\s\-]?commerce)\b', +2),
    (r'\b(?:digital\s*channel|online\s*marketing)\b', +2),
    (r'\b(?:marketing\s*(?:automation|strateg))\b', +2),

    # ── Supply Chain / Operations ──
    (r'\b(?:supply\s*chain\s*(?:management|manag))\b', +3),
    (r'\b(?:operations?\s*manag(?:ement|er))\b', +2),
    (r'\b(?:process\s*(?:management|optimization|improvement))\b', +2),
    (r'\b(?:prozess(?:management|optimierung|verbesserung))\b', +2),
    (r'\b(?:lean\s*management|six\s*sigma)\b', +2),
    (r'\b(?:logistik|logistics)\b', +1),

    # ── Entrepreneurship ──
    (r'\b(?:entrepreneur|startup|start-up|gründ(?:er|ung))\b', +2),
    (r'\b(?:business\s*model|geschäftsmodell)\b', +2),
    (r'\b(?:venture|inkubator|incubator|accelerator)\b', +2),

    # ── Allgemeine Business-Kompetenzen ──
    (r'\b(?:requirements?\s*engineer(?:ing)?|business\s*analy(?:st|sis|se))\b', +2),
    (r'\b(?:relationship\s*manag(?:ement|er))\b', +2),
    (r'\b(?:account\s*manag(?:ement|er))\b', +1),
    (r'\b(?:team(?:leitung|führung|lead))\b', +1),
    (r'\b(?:budget|finanzplanung|financial\s*planning)\b', +1),
]

EXCLUDE_COMPILED = [(re.compile(p, re.IGNORECASE), score) for p, score in EXCLUDE_REQ_PATTERNS]
INCLUDE_COMPILED = [(re.compile(p, re.IGNORECASE), score) for p, score in INCLUDE_REQ_PATTERNS]

# ── Titel-basierte Patterns (werden NUR auf den Jobtitel angewandt) ──
# Starke Signale im Titel, die klar auf reine Entwickler/Tech-Rollen hinweisen
TITLE_EXCLUDE_PATTERNS = [
    # Reine Entwickler/Software-Rollen im Titel
    (r'\b(?:software)\s*(?:engineer|developer|entwickler|architect)\b', -5),
    (r'\b(?:frontend|front-end|backend|back-end|fullstack|full-stack|full\s+stack)\s*'
     r'(?:engineer|developer|entwickler)\b', -6),
    (r'\b(?:web)\s*(?:developer|entwickler)\b', -5),
    (r'\b(?:ios|android|mobile)\s*(?:app\s*)?(?:developer|entwickler|engineer)\b', -6),
    (r'\b(?:devops)\s*engineer\b', -5),
    (r'\b(?:data)\s*engineer\b', -5),
    (r'\b(?:platform)\s*(?:developer|engineer)\b', -5),
    (r'\b(?:cloud)\s*(?:software\s*)?engineer\b', -4),
    (r'\b(?:qa|quality)\s*(?:assurance\s*)?engineer\b', -4),
    (r'\b(?:site\s*reliability|sre)\s*engineer\b', -5),
    (r'\b(?:machine\s*learning|ml)\s*engineer\b', -5),
    (r'\b(?:embedded)\s*(?:software\s*)?engineer\b', -6),
    (r'\b(?:test\s*automation)\s*engineer\b', -5),
    (r'\b(?:rust|java|python|php|ruby|golang|\.net|c\+\+|react|angular|node)\s*'
     r'(?:developer|entwickler|engineer|lead)\b', -6),
    (r'\b(?:java|python|php|ruby|golang|\.net|react|angular)\s*'
     r'(?:software\s*)?(?:developer|entwickler|engineer)\b', -6),
    (r'\blead\s*developer\b', -5),
    (r'\b(?:senior\s*)?(?:software|cloud|data)\s*(?:development\s*)?engineer\b', -5),
    (r'\bdevelopment\s*engineer\b', -4),
    (r'\b(?:senior\s*)?(?:backend|frontend)\s*engineer\b', -6),
    (r'\b(?:salesforce|sap|oracle|dynamics)\s*\w*\s*developer\b', -4),
    (r'\b(?:ict|crm)\s*(?:\w+\s+)?developer\b', -3),
    (r'\bcrm[\s-]?entwickler\b', -3),
    (r'\bsoftware\s*(?:quality\s*)?architect\b', -4),
    (r'\b(?:senior\s*)?(?:onestream|informatica|idmc|avaloq|murex)\s*\w*\s*developer\b', -4),
    (r'\bsoftware\s*(?:test|development)\s*engineer\b', -5),
    (r'\bsoftware\s*(?:documentation|doc)\b', -3),
    (r'\b(?:quantitative)\s*developer\b', -5),
    # Genereller Catch-all: "Developer" oder "Entwickler" im Titel,
    # AUSSER es ist "Business Developer" oder "Process Developer"
    (r'(?<!business\s)(?<!process\s)(?<!org\.\-)(?<!org\.\/)\bdeveloper\b(?!\s*relations)', -3),
    (r'(?<!business\s)(?<!process\s)\bentwickler\b', -3),
    # "Full Stack" im Titel (ohne Manager/Lead)
    (r'\bfull[\s-]?stack\b(?!.*\bmanag)', -4),
    # Solution Developer
    (r'\bsolution\s*developer\b', -4),
    # Founding-level Engineer
    (r'\bfounding[\s-]?level\s*engineer\b', -5),

    # Reine Ingenieur-Rollen (nicht Management)
    (r'\b(?:mechanical|electrical|commissioning|control)\s*engineer\b', -5),
    (r'\b(?:system)\s*engineer\b(?!.*(?:manager|management|lead))', -3),
    (r'\b(?:research)\s*(?:scientist|engineer)\b', -5),
    (r'\b(?:r&d)\s*engineer\b', -4),

    # Handwerk/Trades im Titel
    (r'\b(?:chauffeur|fahrer)\b', -6),
    (r'\b(?:koch|köchin|sous\s*chef|küchenchef)\b', -6),
    (r'\b(?:kellner|barista)\b', -6),
    (r'\b(?:monteur|elektriker|sanitär|installateur|schreiner|mechaniker)\b', -6),
    (r'\b(?:klärwerkfachperson|hauswart)\b', -5),
    (r'\b(?:filialleiter)\b', -3),
    (r'\b(?:verkäufer|verkäuferin)\b(?!.*(?:business|manager))', -5),
]

# Positive Titel-Patterns (MBI-typische Jobtitel)
TITLE_INCLUDE_PATTERNS = [
    (r'\b(?:business\s*developer)\b', +4),
    (r'\b(?:project|projekt)\s*manag(?:er|ement)\b', +4),
    (r'\b(?:product)\s*(?:owner|manager)\b', +4),
    (r'\b(?:it)\s*(?:project\s*)?manag(?:er|ement)\b', +4),
    (r'\b(?:business\s*analyst)\b', +3),
    (r'\b(?:consultant|berater)\b', +3),
    (r'\b(?:relationship)\s*manag(?:er|ement)\b', +3),
    (r'\b(?:account)\s*manag(?:er|ement)\b', +2),
    (r'\b(?:digital)\s*(?:transformation|marketing|channel)\b', +3),
    (r'\b(?:operations?)\s*manag(?:er|ement)\b', +3),
    (r'\b(?:supply\s*chain)\b', +3),
    (r'\b(?:sustainability|nachhaltigkeits?)\s*manag(?:er|ement)?\b', +3),
    (r'\b(?:innovation)\s*manag(?:er|ement)?\b', +3),
    (r'\b(?:requirements?\s*engineer)\b', +2),
]

TITLE_EXCLUDE_COMPILED = [(re.compile(p, re.IGNORECASE), score) for p, score in TITLE_EXCLUDE_PATTERNS]
TITLE_INCLUDE_COMPILED = [(re.compile(p, re.IGNORECASE), score) for p, score in TITLE_INCLUDE_PATTERNS]


def score_mbi_relevance(row):
    """Score how relevant a job is for MBI HSG graduates based on requirements AND title."""
    req = str(row['requirements_clean']).lower()
    title = str(row['job_title']).lower()
    desc = str(row.get('full_description', '')).lower()

    # Combine requirement + title for requirement-pattern scoring
    combined = f"{title} {req}"
    # Also check description for positive signals if requirements are short
    if len(req) < 200:
        combined = f"{title} {desc}"

    neg_score = 0
    pos_score = 0
    neg_matches = []
    pos_matches = []

    # Score based on requirements content
    for pattern, score in EXCLUDE_COMPILED:
        matches = pattern.findall(combined)
        if matches:
            neg_score += score * len(matches)
            neg_matches.append(matches[0] if isinstance(matches[0], str) else matches[0][0])

    for pattern, score in INCLUDE_COMPILED:
        matches = pattern.findall(combined)
        if matches:
            pos_score += score
            pos_matches.append(matches[0] if isinstance(matches[0], str) else matches[0][0])

    # Score based on title (strong signals)
    for pattern, score in TITLE_EXCLUDE_COMPILED:
        if pattern.search(title):
            neg_score += score
            neg_matches.append(f"TITEL: {pattern.pattern[:40]}")

    for pattern, score in TITLE_INCLUDE_COMPILED:
        if pattern.search(title):
            pos_score += score
            pos_matches.append(f"TITEL: {pattern.pattern[:40]}")

    total = pos_score + neg_score  # neg_score is already negative
    return total, pos_score, neg_score, pos_matches, neg_matches


# Score all jobs
scores = df.apply(score_mbi_relevance, axis=1, result_type='expand')
df['relevance_score'] = scores[0]
df['pos_score'] = scores[1]
df['neg_score'] = scores[2]
df['pos_matches'] = scores[3]
df['neg_matches'] = scores[4]

# Threshold: exclude if score < -2 (clearly irrelevant)
THRESHOLD = -2
mask_exclude = df['relevance_score'] < THRESHOLD

n_excluded = mask_exclude.sum()
print(f"Durch Requirements-Filter entfernt: {n_excluded}")
print(f"(Schwellenwert: relevance_score < {THRESHOLD})")

# Show what gets removed per profile
print("\nEntfernte Jobs pro Profil:")
excluded_df = df[mask_exclude]
for profil in df['job_profil'].unique():
    removed = excluded_df[excluded_df['job_profil'] == profil]
    if len(removed) > 0:
        print(f"\n  {profil} ({len(removed)} entfernt):")
        for _, r in removed.head(8).iterrows():
            print(f"    - {r['job_title']}")
            print(f"      Score: {r['relevance_score']} (pos={r['pos_score']}, neg={r['neg_score']})")
            if r['neg_matches']:
                print(f"      Neg: {r['neg_matches'][:3]}")
        if len(removed) > 8:
            print(f"    ... und {len(removed)-8} weitere")

# Also show borderline cases (score between -2 and 0 with neg signals)
borderline = df[(df['relevance_score'] >= THRESHOLD) & (df['neg_score'] < 0)]
if len(borderline) > 0:
    print(f"\nGrenzfälle (behalten, aber neg. Signale): {len(borderline)}")
    for _, r in borderline.head(5).iterrows():
        print(f"  - {r['job_title']} (Score: {r['relevance_score']}, "
              f"pos={r['pos_score']}, neg={r['neg_score']})")

df_clean = df[~mask_exclude].copy()

print(f"\nVerbleibende Jobs nach Relevanzfilter: {len(df_clean)}")
print(f"Verteilung:\n{df_clean['job_profil'].value_counts().to_string()}")
print()

# ─── Schritt 2b: Erfahrungs-Filter (max. 3 Jahre) ────────────────────────────
print("=" * 60)
print("SCHRITT 2b: Erfahrungs-Filter (≤ 3 Jahre Berufserfahrung)")
print("=" * 60)

MAX_EXPERIENCE_YEARS = 3

# Patterns um die geforderte Berufserfahrung in Jahren zu extrahieren
EXP_PATTERNS = re.compile(
    r'(\d{1,2})\+?\s*(?:[-–]\s*\d{1,2}\s*)?'
    r'(?:years?|jahre?|ans?)\s*'
    r'(?:of\s*)?(?:experience|erfahrung|berufserfahrung|professional|work|berufs|praxis)'
    r'|'
    r'(?:mindestens|minimum|min\.?|wenigstens|at\s*least|typically)\s*'
    r'(\d{1,2})\s*\+?\s*(?:years?|jahre?)\s*'
    r'(?:of\s*)?(?:experience|erfahrung|berufserfahrung|professional|work|berufs)?'
    r'|'
    r'(?:erfahrung|experience|berufserfahrung)\s*'
    r'(?:von\s*)?(?:mindestens\s*|min\.?\s*)?'
    r'(\d{1,2})\+?\s*(?:years?|jahre?)',
    re.IGNORECASE
)


def extract_max_experience_years(text):
    """Extract the maximum number of years of experience required from text."""
    text = str(text)
    matches = EXP_PATTERNS.findall(text)
    years = []
    for m in matches:
        for val in m:
            if val:
                y = int(val)
                if 1 <= y <= 20:  # realistic range
                    years.append(y)
    return max(years) if years else 0


df_clean['max_experience_years'] = df_clean['requirements_clean'].apply(extract_max_experience_years)

mask_too_experienced = df_clean['max_experience_years'] > MAX_EXPERIENCE_YEARS
n_exp_excluded = mask_too_experienced.sum()

print(f"Jobs mit > {MAX_EXPERIENCE_YEARS} Jahren Erfahrung entfernt: {n_exp_excluded}")
print(f"\nErfahrungs-Verteilung (vor Filter):")
print(df_clean['max_experience_years'].value_counts().sort_index().to_string())

# Show what gets removed per profile
print(f"\nEntfernte Jobs pro Profil (> {MAX_EXPERIENCE_YEARS}J Erfahrung):")
exp_excluded_df = df_clean[mask_too_experienced]
for profil in df_clean['job_profil'].unique():
    removed = exp_excluded_df[exp_excluded_df['job_profil'] == profil]
    if len(removed) > 0:
        print(f"\n  {profil} ({len(removed)} entfernt):")
        for _, r in removed.head(5).iterrows():
            print(f"    - {r['job_title']} ({r['max_experience_years']}J gefordert)")
        if len(removed) > 5:
            print(f"    ... und {len(removed)-5} weitere")

df_clean = df_clean[~mask_too_experienced].copy()

print(f"\nVerbleibende Jobs: {len(df_clean)}")
print(f"Verteilung nach Erfahrungs-Filter:\n{df_clean['job_profil'].value_counts().to_string()}")
print()

# ─── Schritt 3: Keyword/Skill-Extraktion ─────────────────────────────────────
print("=" * 60)
print("SCHRITT 3: Keyword/Skill-Extraktion (TF-IDF + Häufigkeit)")
print("=" * 60)


def clean_text(text):
    """Prepare text for keyword extraction."""
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Keep alphanumeric, German umlauts, hyphens, plus, hash
    text = re.sub(r'[^a-zäöüéèà0-9\s\-\+\#\.]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Stopwords: common words in DE + EN that aren't skills
STOPWORDS = set([
    # ── German basic ──
    'und', 'oder', 'der', 'die', 'das', 'ein', 'eine', 'ist', 'sind', 'wird', 'werden',
    'hat', 'haben', 'für', 'mit', 'von', 'zu', 'im', 'in', 'auf', 'an', 'aus', 'bei',
    'nach', 'über', 'unter', 'durch', 'als', 'auch', 'nicht', 'sich', 'wir', 'sie',
    'du', 'ich', 'es', 'den', 'dem', 'des', 'einer', 'eines', 'einem', 'einen',
    'ihre', 'ihr', 'ihrem', 'ihren', 'seiner', 'seinem', 'seinen', 'seine',
    'deine', 'deinem', 'deinen', 'dein', 'unser', 'unsere', 'unserem', 'unseren',
    'dies', 'diese', 'diesem', 'diesen', 'dieser', 'jede', 'jedem', 'jeden', 'jeder',
    'wenn', 'dass', 'weil', 'aber', 'doch', 'noch', 'schon', 'sehr', 'nur', 'kann',
    'können', 'soll', 'sollte', 'muss', 'müssen', 'will', 'wollen', 'würde', 'würden',
    'gerne', 'sowie', 'bzw', 'etc', 'idealerweise', 'vorzugsweise',
    'mindestens', 'bevorzugt', 'wie', 'zum', 'zur', 'was', 'dich', 'dir', 'uns',
    'dazu', 'dabei', 'damit', 'dann', 'dort', 'hier', 'mehr',
    'neue', 'neuen', 'neuer', 'neues', 'andere', 'anderen', 'anderer', 'anderes',
    'erste', 'ersten', 'erster', 'erstes', 'teil', 'alle', 'allem', 'allen', 'aller',
    'alles', 'bereits', 'ab', 'bis', 'so', 'nun', 'da', 'kein', 'keine', 'keinem',
    'keinen', 'keiner', 'ob', 'vor', 'hin', 'her', 'oben', 'um',

    # ── German job-posting filler (large expansion) ──
    'jahr', 'jahre', 'jahren', 'erfahrung', 'berufserfahrung', 'kenntnisse',
    'wissen', 'fähigkeit', 'fähigkeiten', 'kompetenz', 'kompetenzen',
    'bieten', 'suchen', 'arbeiten', 'arbeit', 'stelle', 'job', 'team', 'unternehmen',
    'firma', 'rolle', 'aufgaben', 'aufgabe',
    # generic adjectives / filler used in job ads
    'gute', 'guter', 'gutes', 'gutem', 'guten',
    'hohe', 'hoher', 'hohes', 'hohem', 'hohen',
    'fundierte', 'fundierter', 'fundiertes', 'fundiertem', 'fundierten',
    'ausgeprägte', 'ausgeprägter', 'ausgeprägtes', 'ausgeprägtem', 'ausgeprägten',
    'selbständige', 'selbständiger', 'selbstständige', 'selbstständiger',
    'strukturierte', 'strukturierter', 'analytische', 'analytischer',
    'mehrjährige', 'mehrjähriger', 'langjährige', 'langjähriger',
    'einschlägige', 'einschlägiger', 'relevante', 'relevanter',
    'nachweisbare', 'nachweisbarer', 'vertiefte', 'vertiefter',
    'umfassende', 'umfassender',
    # verbs / verbal forms common in job ads
    'bist', 'hast', 'bringst', 'verfügst', 'besitzt', 'zeichnest',
    'freust', 'arbeitest', 'denkst', 'bringen', 'verfügen', 'besitzen',
    'zeichnen', 'freuen', 'denken', 'übernehmen', 'verantworten',
    'gestalten', 'entwickeln', 'unterstützen', 'sicherstellen', 'beitragen',
    'mitbringen', 'mitbringst', 'einbringen',
    # nouns common in ads but not real skills
    'profil', 'vorteil', 'bereich', 'umfeld', 'umgebung', 'rahmen',
    'fragen', 'bewerbung', 'kontakt', 'anstellung', 'pensum',
    'stellenprozent', 'angebot', 'möglichkeit', 'möglichkeiten',
    'herausforderung', 'herausforderungen', 'verantwortung',
    'zusammenarbeit', 'zusammenarbeiten',
    'ausbildung', 'weiterbildung', 'studium', 'abschluss',
    'persönlichkeit', 'person', 'personen', 'kandidat', 'kandidaten',
    'bewerber', 'bewerberin', 'mitarbeiter', 'mitarbeiterin', 'mitarbeitende',
    'kolleginnen', 'kollegen', 'vorgesetzten', 'standort', 'büro',
    'arbeitsweise', 'denkweise', 'arbeitsumfeld', 'arbeitsplatz',
    'pensum', 'prozent', 'teilzeit', 'vollzeit',
    'unserer', 'unseres', 'unserem', 'unseren',
    'schweiz', 'zürich', 'basel', 'bern', 'luzern', 'genf',
    'deutschland', 'österreich',
    # filler phrases
    'darüber', 'hinaus', 'rund', 'circa', 'circa', 'je', 'pro',
    'täglich', 'wöchentlich', 'monatlich', 'jährlich',
    'mindestens', 'höchstens', 'optimal', 'optimalerweise',
    'spannende', 'spannenden', 'spannender',
    'attraktive', 'attraktiven', 'attraktiver',
    'dynamische', 'dynamischen', 'dynamischer', 'dynamisches',
    'moderne', 'modernen', 'moderner', 'modernes',
    'flexible', 'flexiblen', 'flexibler', 'flexibles',
    'innovativ', 'innovative', 'innovativen', 'innovativer',
    'abwechslungsreich', 'abwechslungsreiche', 'abwechslungsreichen',
    'verantwortungsvoll', 'verantwortungsvolle', 'verantwortungsvollen',
    'internationalen', 'internationale', 'internationaler', 'internationales',

    # ── English basic ──
    'the', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'shall', 'can', 'need', 'must', 'ought', 'not', 'no', 'nor',
    'but', 'if', 'then', 'else', 'when', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'once', 'here', 'there', 'all', 'each', 'every',
    'both', 'few', 'more', 'most', 'other', 'some', 'such', 'any', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until', 'while',
    'of', 'also', 'an', 'this', 'that', 'these', 'those', 'am', 'it', 'its',
    'we', 'you', 'your', 'they', 'their', 'our', 'my', 'his', 'her', 'he', 'she',
    'who', 'which', 'what', 'where', 'how', 'why', 'whom', 'whose',

    # ── English job-posting filler (large expansion) ──
    'experience', 'work', 'working', 'including', 'within', 'across', 'well',
    'ability', 'strong', 'good', 'excellent', 'proven', 'minimum', 'years', 'year',
    'required', 'preferred', 'knowledge', 'understanding', 'skills', 'skill',
    'proficiency', 'degree', 'equivalent',
    'requirements', 'qualifications', 'responsibilities', 'benefits', 'apply',
    # generic verbs
    'ensure', 'manage', 'support', 'develop', 'provide', 'lead', 'drive',
    'build', 'create', 'deliver', 'enable', 'help', 'make', 'take', 'give',
    'use', 'using', 'used', 'based', 'related', 'relevant',
    'looking', 'seeking', 'hiring', 'join', 'joining',
    # generic nouns / adjectives in job ads
    'role', 'position', 'opportunity', 'company', 'organization', 'employer',
    'candidate', 'candidates', 'applicant', 'applicants',
    'team', 'teams', 'colleagues', 'environment', 'workplace',
    'new', 'key', 'part', 'full', 'time', 'level', 'senior', 'junior',
    'mid', 'entry', 'intern', 'internship',
    'bachelor', 'master', 'phd', 'mba', 'bsc', 'msc',
    'great', 'ideal', 'ideally', 'plus', 'bonus', 'nice', 'asset',
    'highly', 'deeply', 'solid', 'extensive', 'comprehensive', 'broad',
    'hands-on', 'hands', 'track', 'record',
    'passion', 'passionate', 'motivated', 'self-motivated', 'driven',
    'dynamic', 'fast-paced', 'innovative', 'collaborative',
    'diverse', 'inclusive', 'equal', 'employer',
    'competitive', 'attractive', 'exciting', 'challenging',
    'responsible', 'responsible', 'accountable',
    'offer', 'offers', 'offering', 'offered',
    'world', 'global', 'local', 'regional', 'international',
    'zurich', 'geneva', 'basel', 'bern', 'switzerland',
    're', 'we', 'll', 've',  # contractions
    # generic skill filler
    'communication', 'written', 'verbal', 'oral',
    'interpersonal', 'organizational', 'problem-solving', 'problem',
    'solving', 'thinking', 'mindset', 'oriented', 'detail',
    'multi', 'able', 'capable',
    # gender markers
    'a', 'f', 'm', 'w', 'd', 'x', 'mwd', 'wmd', 'fmd', 'genders',
])


def extract_skills_tfidf(texts, profil_name, top_n=50):
    """Extract top skills from a collection of requirement texts using TF-IDF."""
    cleaned = [clean_text(t) for t in texts]

    # Use TF-IDF with uni- and bigrams
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        min_df=2,             # must appear in at least 2 docs
        max_df=0.85,          # ignore terms in >85% of docs
        stop_words=list(STOPWORDS),
        token_pattern=r'(?u)\b[a-zäöüéèà][a-zäöüéèà0-9\+\#\.\-]{1,}\b',
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(cleaned)
    except ValueError:
        print(f"  {profil_name}: Nicht genug Daten für TF-IDF")
        return pd.DataFrame()

    feature_names = vectorizer.get_feature_names_out()

    # Average TF-IDF score per term across all documents
    avg_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).flatten()

    # Document frequency (in how many job postings does this term appear?)
    doc_freq = np.asarray((tfidf_matrix > 0).sum(axis=0)).flatten()

    # Build results
    results = pd.DataFrame({
        'keyword': feature_names,
        'tfidf_score': avg_tfidf,
        'anzahl_jobs': doc_freq,
        'anteil_jobs_pct': (doc_freq / len(texts) * 100).round(1),
    })

    results = results.sort_values('tfidf_score', ascending=False).head(top_n)
    results['berufsfeld'] = profil_name
    return results


all_skills = []

for profil in df_clean['job_profil'].unique():
    subset = df_clean[df_clean['job_profil'] == profil]
    texts = subset['requirements_clean'].tolist()
    print(f"\n{profil} ({len(texts)} Jobs):")

    skills_df = extract_skills_tfidf(texts, profil, top_n=50)
    if not skills_df.empty:
        all_skills.append(skills_df)
        # Print top 15
        print(f"  Top 15 Keywords/Skills:")
        for _, row in skills_df.head(15).iterrows():
            print(f"    {row['keyword']:40s}  TF-IDF: {row['tfidf_score']:.4f}  "
                  f"in {int(row['anzahl_jobs']):3d} Jobs ({row['anteil_jobs_pct']:.1f}%)")

skills_all = pd.concat(all_skills, ignore_index=True)
print()

# ─── Schritt 4: Export ────────────────────────────────────────────────────────
print("=" * 60)
print("SCHRITT 4: Export")
print("=" * 60)

# Bereinigter Datensatz (requirements_clean → requirements für Konsistenz)
export_df = df_clean[['job_profil', 'job_title', 'company', 'location',
                       'requirements_clean', 'full_description', 'job_url']].copy()
export_df.rename(columns={'requirements_clean': 'requirements'}, inplace=True)
export_df.to_csv(OUTPUT_CLEAN, index=False, encoding='utf-8-sig')
print(f"Bereinigter Datensatz: {OUTPUT_CLEAN} ({len(export_df)} Jobs)")

# Skill-Häufigkeiten
skills_export = skills_all[['berufsfeld', 'keyword', 'tfidf_score', 'anzahl_jobs', 'anteil_jobs_pct']]
skills_export = skills_export.sort_values(['berufsfeld', 'tfidf_score'], ascending=[True, False])
skills_export.to_csv(OUTPUT_SKILLS, index=False, encoding='utf-8-sig')
print(f"Skill-Häufigkeiten: {OUTPUT_SKILLS} ({len(skills_export)} Einträge)")

print("\n✅ Bereinigung abgeschlossen!")
