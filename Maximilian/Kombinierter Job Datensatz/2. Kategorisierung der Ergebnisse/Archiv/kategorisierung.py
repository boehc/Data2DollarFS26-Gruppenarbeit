"""
Kategorisierung von Stelleninseraten nach dem Kompetenz-Framework (Beck, Bartscher et al. 2012)
mit datengetriebener Aufschlüsselung der Fachkompetenzen.

Framework-Dimensionen:
1. Fachkompetenzen (+ detaillierte Skills)
2. Soziale Kompetenz
3. Methodenkompetenz
4. Personale Kompetenz

Output: jobs_kategorisiert.csv
"""

import pandas as pd
import re

# ──────────────────────────────────────────────────
# 1) DATEN LADEN
# ──────────────────────────────────────────────────
df = pd.read_csv('jobs_combined.csv')

# Textfeld für Kategorisierung: requirements + anforderungen_sektion + full_description
def build_text(row):
    parts = []
    for col in ['requirements', 'anforderungen_sektion', 'full_description']:
        if pd.notna(row.get(col)):
            parts.append(str(row[col]))
    return ' '.join(parts).lower()

df['_text'] = df.apply(build_text, axis=1)


# ──────────────────────────────────────────────────
# 2) HILFSFUNKTION: Keyword-Matching
# ──────────────────────────────────────────────────
def match_any(text, patterns):
    """Gibt 1 zurück wenn mindestens ein Pattern matched."""
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return 1
    return 0


# ──────────────────────────────────────────────────
# 3) FRAMEWORK-KATEGORIEN MIT KEYWORD-PATTERNS
# ──────────────────────────────────────────────────

# === FACHKOMPETENZEN (Oberkategorien nach Framework) ===
fachkompetenzen = {
    'FK_Waren_Produktkenntnisse': [
        r'\bproduktkenntnis\w*\b', r'\bwarenkenn\w*\b', r'\bproduktportfolio\b',
        r'\bprodukt\w*wissen\b', r'\bproduct knowledge\b', r'\bmarket knowledge\b',
        r'\bbranchenkenntnis\w*\b', r'\bmarktkenntn\w*\b', r'\bdomain knowledge\b',
        r'\bfachkenntn\w*\b', r'\bfachgebiet\b', r'\bexpertise\b',
    ],
    'FK_Komplexe_Fertigkeiten': [
        r'\bkomplexe?\s+fertigk\w*\b', r'\btechnische?\s+fertigk\w*\b',
        r'\bprogrammier\w*\b', r'\bsoftware\s*entwickl\w*\b', r'\bsoftware\s*engineer\w*\b',
        r'\bcoding\b', r'\bcode\b', r'\bdevelop\w*\b', r'\bengineering\b',
        r'\barchitect\w*\b', r'\bdesign pattern\b', r'\bsystem design\b',
        r'\bimplementier\w*\b', r'\bimplementat\w*\b',
        r'\bdata model\w*\b', r'\bdatenmodell\w*\b',
        r'\bautomati\w+\b', r'\bskripting\b', r'\bscripting\b',
    ],
    'FK_Fremdsprachen': [
        r'\bfremdsprach\w*\b', r'\bsprachkenntn\w*\b', r'\blanguage skills?\b',
        r'\benglisch\b', r'\benglish\b', r'\bfranzösisch\b', r'\bfrench\b',
        r'\bitalienisch\b', r'\bitalian\b', r'\bspanisch\b', r'\bspanish\b',
        r'\bdeutsch\b', r'\bgerman\b', r'\bmutterspra\w*\b', r'\bnative speaker\b',
        r'\bfluent\b', r'\bfliessend\b', r'\bfließend\b', r'\bbilingual\b',
        r'\bfrankophone?\b', r'\bmehrsprachig\w*\b', r'\bmultilingual\b',
    ],
    'FK_Fuehrerschein': [
        r'\bführerschein\b', r'\bfahrausweis\b', r'\bdriver.?s?\s*licen[cs]e\b',
        r'\bkfz\b', r'\bfahrzeug\b', r'\breisetätigkeit\b', r'\breisebereit\w*\b',
        r'\btravel\s*(?:required|willingness)\b',
    ],
    'FK_Auslandserfahrung': [
        r'\bauslandserfahrung\b', r'\binternational\w*\s+(?:experience|erfahrung)\b',
        r'\bglobal\s+(?:experience|erfahrung)\b', r'\bcross[- ]?cultural\b',
        r'\binterkulturell\w*\b', r'\babroad\b', r'\binternational\w*\s+umfeld\b',
        r'\bmultinational\b', r'\binternational\w*\s+(?:environment|context)\b',
    ],
    'FK_Vertriebserfahrung': [
        r'\bvertrieb\w*\b', r'\bsales\b', r'\bselling\b', r'\bakquise\b',
        r'\bacquisition\b', r'\bkundenbetreu\w*\b', r'\baccount\s*manage\w*\b',
        r'\bbusiness\s*develop\w*\b', r'\bkey\s*account\b', r'\bneukundeng\w*\b',
        r'\bverhandlung\w*\b', r'\bvertragsverhandl\w*\b',
    ],
    'FK_Projekterfahrung': [
        r'\bprojekterfahrung\b', r'\bproject\s*(?:experience|erfahrung)\b',
        r'\bprojektleit\w*\b', r'\bproject\s*(?:lead|manag)\w*\b',
        r'\bprojektarbeit\b', r'\bprojektmitarbeit\w*\b',
        r'\bprogram\s*manage\w*\b',
    ],
    'FK_EDV_Kenntnisse': [
        r'\bedv\b', r'\bit[- ]?kenntn\w*\b', r'\binformatik\w*\b',
        r'\bcomputer\s*(?:science|skills?|kenntn\w*)\b',
        r'\bsoftware\b', r'\btool\w*\b', r'\bdigital\w*\b',
        r'\btechnolog\w*\b', r'\btechnisch\w*\b', r'\btechnical\b',
        r'\bcloud\b', r'\bsaas\b', r'\binfrastruktur\b', r'\binfrastructure\b',
    ],
    'FK_Berufsausbildung': [
        r'\bberufsausbildung\b', r'\bausbildung\b', r'\blehre\b',
        r'\bstudium\b', r'\bhochschul\w*\b', r'\buniversit\w*\b',
        r'\bbachelor\b', r'\bmaster\b', r'\bmba\b', r'\bphd\b', r'\bdoktor\w*\b',
        r'\bdiplom\b', r'\bfh\b', r'\beth\b', r'\bdegree\b',
        r'\babgeschlossen\w*\s+(?:studium|ausbildung)\b',
        r'\bqualifikat\w*\b', r'\bcertificat\w*\b', r'\bzertifik\w*\b',
        r'\bweiterbildung\b', r'\bfachausbildung\b', r'\bfachhochschul\w*\b',
    ],
    'FK_Branchenerfahrung': [
        r'\bbranchenerfahrung\b', r'\bbranchen\w*kenntn\w*\b',
        r'\bindustry\s*(?:experience|knowledge|expertise)\b',
        r'\bsector\s*(?:experience|knowledge)\b',
        r'\bberufserfahrung\b', r'\bwork\s*experience\b', r'\bjahre?\s+(?:erfahrung|experience)\b',
        r'\bprofessional\s*experience\b', r'\berfahrung\s+(?:in|im|als|with)\b',
        r'\bsenior\b', r'\bjunior\b', r'\b\d+\+?\s*(?:jahre?|years?)\s*(?:erfahrung|experience|berufserfahrung)\b',
    ],
}

# === SOZIALE KOMPETENZ ===
soziale_kompetenz = {
    'SK_Kooperationsfaehigkeit': [
        r'\bkooperation\w*\b', r'\bzusammenarbeit\b', r'\bcollaboration\b',
        r'\bcooperati\w*\b', r'\bteamwork\b', r'\bcross[- ]?functional\b',
        r'\binterdisziplin\w*\b', r'\binterdisciplin\w*\b',
        r'\bschnittstelle\w*\b', r'\bstakeholder\b',
    ],
    'SK_Verhandlungsgeschick': [
        r'\bverhandlung\w*\b', r'\bnegotiat\w*\b', r'\bvertragsverhandl\w*\b',
        r'\bdiplomati\w*\b', r'\bkompromiss\w*\b', r'\bmediat\w*\b',
    ],
    'SK_Durchsetzungsvermoegen': [
        r'\bdurchsetzung\w*\b', r'\bassertiv\w*\b', r'\büberzeugungs\w*\b',
        r'\bpersuasi\w*\b', r'\bdecisive\w*\b', r'\bentscheidungsst\w*\b',
        r'\bentscheidungsfr\w*\b',
    ],
    'SK_Kritikfaehigkeit': [
        r'\bkritikfähig\w*\b', r'\bfeedback\b', r'\bconstructive\s*criticism\b',
        r'\bselbstkritisch\b', r'\breflexion\w*\b', r'\bopen\s*to\s*feedback\b',
        r'\bkritisch\w*\s+denk\w*\b', r'\bcritical\s+think\w*\b',
    ],
    'SK_Teamfaehigkeit': [
        r'\bteamfähig\w*\b', r'\bteamplayer\b', r'\bteam\s*(?:player|spirit|orient\w*|fähig\w*)\b',
        r'\bteamarbeit\b', r'\bteam\b', r'\bim\s+team\b', r'\bin\s+(?:a|the)\s+team\b',
        r'\bkollegen\b', r'\bcolleague\w*\b', r'\bmitarbeiter\w*\b',
    ],
    'SK_Hilfsbereitschaft': [
        r'\bhilfsbereit\w*\b', r'\bsupport\w*\b', r'\bunterstütz\w*\b',
        r'\bhelpful\b', r'\bmentor\w*\b', r'\bcoach\w*\b',
    ],
    'SK_Fairness': [
        r'\bfairness\b', r'\bfair\b', r'\bintegrität\b', r'\bintegrit\w*\b',
        r'\bethik\w*\b', r'\bethic\w*\b', r'\btransparenz\b', r'\btransparenc\w*\b',
    ],
    'SK_Kundenorientierung': [
        r'\bkundenorientier\w*\b', r'\bcustomer\s*(?:orient\w*|focus\w*|centric)\b',
        r'\bkundenfokus\w*\b', r'\bkunden\w*bezieh\w*\b', r'\bcustomer\s*relation\w*\b',
        r'\bkundenbed\w*\b', r'\bcustomer\s*(?:need|satisfaction|service)\w*\b',
        r'\bserviceorientier\w*\b', r'\bservice[- ]?orient\w*\b',
        r'\bklientel\b', r'\bclient\b',
    ],
    'SK_Vorurteilsfreiheit': [
        r'\bvorurteilsfrei\w*\b', r'\bdiversit\w*\b', r'\binclusi\w*\b',
        r'\binklusi\w*\b', r'\bunbiased\b', r'\bequal\s*opportunit\w*\b',
        r'\bchancengleich\w*\b', r'\bvielfalt\b',
    ],
    'SK_Respekt': [
        r'\brespekt\w*\b', r'\brespect\w*\b', r'\bwertschätzung\b',
        r'\bwertschätzend\b', r'\bappreciat\w*\b',
    ],
}

# === METHODENKOMPETENZ ===
methodenkompetenz = {
    'MK_Konzeptionelle_Staerke': [
        r'\bkonzeptionell\w*\b', r'\bconceptual\b', r'\bkonzept\w*\b',
        r'\bconcept\w*\b', r'\bstrategisch\w*\s+denk\w*\b', r'\bstrategic\s*think\w*\b',
        r'\banalytisch\w*\b', r'\banalytic\w*\b', r'\banalyse\w*\b', r'\banalysis\b',
    ],
    'MK_Effektives_Arbeiten': [
        r'\beffektiv\w*\b', r'\befficient\w*\b', r'\beffizienz\b', r'\beffizient\b',
        r'\bproduktiv\w*\b', r'\bproductiv\w*\b', r'\bergebnisorient\w*\b',
        r'\bresult\w*[\s-]*orient\w*\b', r'\bgoal[\s-]*orient\w*\b',
        r'\bzielorient\w*\b', r'\bstrukturiert\w*\b', r'\bstructured\b',
        r'\bsorgfältig\w*\b', r'\bgenau\w*\b', r'\bdetail\w*\b',
        r'\bgewissenhaft\b', r'\bthorough\b', r'\bpräzis\w*\b',
    ],
    'MK_Projektmanagement': [
        r'\bprojektmanagement\b', r'\bproject\s*management\b', r'\bprojektsteuer\w*\b',
        r'\bprojektplan\w*\b', r'\bproject\s*plan\w*\b', r'\bmeilenstein\w*\b',
        r'\bmilestone\w*\b', r'\btimeline\w*\b', r'\bdeadline\w*\b',
        r'\bressourcenplan\w*\b', r'\bresource\s*plan\w*\b',
        r'\bprojektbudget\b', r'\bgantt\b', r'\bpmp\b', r'\bprince2\b',
    ],
    'MK_Strategieentwicklung': [
        r'\bstrategie\w*\b', r'\bstrateg\w*\b', r'\bvision\b',
        r'\bgeschäftsentwickl\w*\b', r'\bbusiness\s*strateg\w*\b',
        r'\blangfristig\w*\b', r'\blong[\s-]*term\b', r'\broadmap\b',
    ],
    'MK_Praesentation': [
        r'\bpräsentation\w*\b', r'\bpresentation\w*\b', r'\bpräsentier\w*\b',
        r'\bpresent\w*\b(?=.*(?:skills?|fähig|kompetenz|results))',
        r'\bvortrag\w*\b', r'\bstorytelling\b',
        r'\bkommunikation\w*\b', r'\bcommunicat\w*\b',
    ],
    'MK_Selbstmanagement': [
        r'\bselbstmanagement\b', r'\bselbstorganis\w*\b', r'\bself[\s-]*manag\w*\b',
        r'\bselbständig\w*\b', r'\bselbstständig\w*\b', r'\beigenständig\w*\b',
        r'\bindependent\w*\b', r'\bautonomo?\w*\b', r'\bself[\s-]*(?:start|direct|motiv)\w*\b',
        r'\beigenverantwort\w*\b', r'\bproaktiv\b', r'\bproactive\b',
        r'\beigeninitiativ\w*\b', r'\binitiativ\w*\b',
    ],
    'MK_Moderationstechnik': [
        r'\bmoderation\w*\b', r'\bfacilitat\w*\b', r'\bmoderieren\b',
        r'\bworkshop\s*(?:leitung|facilitati|moderati)\w*\b',
        r'\bworkshops?\b',
    ],
    'MK_Koordination': [
        r'\bkoordinat\w*\b', r'\bcoordinat\w*\b', r'\borganisiern?\b',
        r'\borganisier\w*\b', r'\borganis\w*talent\b', r'\borganiz\w*\b',
        r'\bplanning\b', r'\bplanung\b', r'\bprioris\w*\b', r'\bprioritiz\w*\b',
    ],
    'MK_Kreatives_Denken': [
        r'\bkreativ\w*\b', r'\bcreativ\w*\b', r'\binnovati\w*\b',
        r'\bdesign\s*think\w*\b', r'\bquer\s*denk\w*\b', r'\bout[\s-]*of[\s-]*the[\s-]*box\b',
        r'\bneu\w*\s+ideen\b', r'\bnew\s*ideas?\b',
    ],
    'MK_Stressmanagement': [
        r'\bstressmanagement\b', r'\bstress\s*(?:manage|resilien)\w*\b',
        r'\bbelastbar\w*\b', r'\bresilien\w*\b', r'\bstress\w*resist\w*\b',
        r'\brunter\s*druck\b', r'\bunder\s*pressure\b', r'\bdeadline\w*\b',
        r'\bhigh[\s-]*pressure\b', r'\bhektisch\w*\b', r'\bdynamisch\w*\b',
        r'\bfast[\s-]*paced\b',
    ],
}

# === PERSONALE KOMPETENZ ===
personale_kompetenz = {
    'PK_Ausstrahlung_Charisma': [
        r'\bausstrahlung\b', r'\bcharisma\w*\b', r'\bpersönlichkeit\b',
        r'\bpersonality\b', r'\bauftreten\b', r'\bpresence\b',
        r'\brepräsentativ\w*\b',
    ],
    'PK_Aufgeschlossenheit': [
        r'\baufgeschlossen\w*\b', r'\boffen\w*\b', r'\bopen[\s-]*minded\w*\b',
        r'\bneugier\w*\b', r'\bcurious\w*\b', r'\bcuriosity\b',
        r'\blernbereit\w*\b', r'\bwilling\w*\s*to\s*learn\b', r'\blernfähig\w*\b',
        r'\bwissbegier\w*\b', r'\beager\s*to\s*learn\b',
    ],
    'PK_Unternehmerisches_Denken': [
        r'\bunternehmerisch\w*\b', r'\bentrepreneurial\b',
        r'\bbusiness[\s-]*(?:mind|acumen|sense|orient)\w*\b',
        r'\bgeschäftssinn\b', r'\bownership\b', r'\bverantwortungsbewuss\w*\b',
        r'\bhands[\s-]*on\b', r'\banpackend\b',
    ],
    'PK_Menschenkenntnis': [
        r'\bmenschenkenntnis\b', r'\bempathy\b', r'\bpeople\s*skills?\b',
        r'\bsoziale?\s*kompetenz\w*\b', r'\bsocial\s*skills?\b',
        r'\binterpersonal\b', r'\bfingerspitzengefühl\b',
        r'\beinfühlungsvermögen\b',
    ],
    'PK_Empathie': [
        r'\bempathie\b', r'\bempathy\b', r'\beinfühlungsvermögen\b',
        r'\bempathisch\b', r'\bempathetic\b', r'\bverständnisvoll\b',
    ],
    'PK_Auffassungsgabe': [
        r'\bauffassungsgabe\b', r'\bschnelle\s*auffassung\b',
        r'\bquick\s*learn\w*\b', r'\bfast\s*learn\w*\b',
        r'\bschnell\w*\s+(?:einarbeit|lern|versteh)\w*\b',
        r'\badaptab\w*\b', r'\banpassungsfähig\w*\b', r'\bflexib\w*\b',
    ],
    'PK_Motivation': [
        r'\bmotivation\b', r'\bmotiviert\b', r'\bmotivated\b',
        r'\bengagiert\b', r'\bengaged\b', r'\bengagement\b',
        r'\bleidenschaft\w*\b', r'\bpassion\w*\b', r'\bbegeisterung\w*\b',
        r'\benthusias\w*\b', r'\bdrive\b', r'\bdriven\b',
    ],
    'PK_Interesse': [
        r'\binteresse\b', r'\binterest\b', r'\baffinität\b', r'\baffinity\b',
        r'\bbegeisterung\b', r'\bfaszination\b',
    ],
    'PK_Belastbarkeit': [
        r'\bbelastbar\w*\b', r'\bresilien\w*\b', r'\bstressresist\w*\b',
        r'\bstressresistent\b', r'\bhigh[\s-]*pressure\b', r'\brunter\s*druck\b',
        r'\bunder\s*pressure\b', r'\bausdauer\b', r'\bendurance\b',
        r'\bstamina\b',
    ],
    'PK_Entschlossenheit': [
        r'\bentschlossenheit\b', r'\bentschlossen\b', r'\bdetermin\w*\b',
        r'\bzielstre\w*\b', r'\bgoal[\s-]*orient\w*\b', r'\bzielorient\w*\b',
        r'\bambiti\w*\b', r'\behrgeiz\w*\b', r'\btatkräftig\b',
    ],
}


# === DETAILLIERTE FACHKOMPETENZEN (datengetrieben) ===
fach_detail = {
    # Programmiersprachen & Frameworks
    'FD_Python': [r'\bpython\b'],
    'FD_Java': [r'\bjava\b(?!\s*script)'],
    'FD_JavaScript_TypeScript': [r'\bjavascript\b', r'\btypescript\b', r'\bjs\b', r'\bts\b'],
    'FD_CSharp': [r'\bc#\b', r'\b\.net\b', r'\bdotnet\b'],
    'FD_SQL': [r'\bsql\b', r'\bnosql\b', r'\bmysql\b', r'\bpostgres\w*\b', r'\bmongodb\b'],
    'FD_R_Statistik': [r'\b(?:r studio|rstudio)\b', r'\bstatistik\b', r'\bstatistic\w*\b', r'\bspss\b', r'\bsas\b', r'\bstata\b'],
    'FD_HTML_CSS': [r'\bhtml\b', r'\bcss\b'],
    'FD_PHP_Ruby_andere': [r'\bphp\b', r'\bruby\b', r'\bscala\b', r'\bkotlin\b', r'\bswift\b', r'\brust\b', r'\bgolang\b'],

    # Cloud & Infrastruktur
    'FD_Cloud_AWS_Azure_GCP': [r'\baws\b', r'\bazure\b', r'\bgcp\b', r'\bgoogle cloud\b', r'\bcloud\b'],
    'FD_Docker_Kubernetes': [r'\bdocker\b', r'\bkubernetes\b', r'\bk8s\b', r'\bcontainer\w*\b'],
    'FD_DevOps_CICD': [r'\bdevops\b', r'\bci\/?cd\b', r'\bjenkins\b', r'\bgithub actions\b', r'\bterraform\b', r'\bansible\b'],

    # Daten & Analytics
    'FD_Data_Science_ML': [r'\bdata science\b', r'\bmachine learning\b', r'\bml\b', r'\bdeep learning\b', r'\bdata scientist\b'],
    'FD_AI_KI': [r'\bartificial intelligence\b', r'\bkünstliche intelligenz\b', r'\b(?:ki|ai)\b', r'\bgenerative ai\b', r'\bgen\s?ai\b'],
    'FD_NLP_LLM': [r'\bnlp\b', r'\bllm\b', r'\blarge language\b', r'\bchatgpt\b', r'\bopenai\b', r'\bnatural language\b'],
    'FD_Data_Analysis_BI': [r'\bdata analy\w+\b', r'\bdatenanalyse\b', r'\bpower\s?bi\b', r'\btableau\b', r'\breporting\b', r'\bdashboard\w*\b', r'\bvisualisierung\b'],
    'FD_Data_Engineering_ETL': [r'\bdata engineer\w*\b', r'\betl\b', r'\bpipeline\w*\b', r'\bspark\b', r'\bkafka\b', r'\bdatabricks\b', r'\bsnowflake\b', r'\bairflow\b'],

    # Business Software
    'FD_SAP': [r'\bsap\b'],
    'FD_Salesforce': [r'\bsalesforce\b'],
    'FD_ERP': [r'\berp\b'],
    'FD_CRM': [r'\bcrm\b'],
    'FD_MS_Office': [r'\bms office\b', r'\bmicrosoft office\b', r'\boffice 365\b', r'\bm365\b', r'\bexcel\b', r'\bword\b', r'\bpowerpoint\b', r'\boutlook\b'],
    'FD_Jira_Confluence': [r'\bjira\b', r'\bconfluence\b', r'\batlassian\b'],

    # Security & Compliance
    'FD_Cyber_Security': [r'\bcyber\s?security\b', r'\bit.?sicherheit\b', r'\binformation security\b', r'\binfosec\b', r'\bsecurity\b'],
    'FD_Datenschutz_DSGVO': [r'\bdsgvo\b', r'\bgdpr\b', r'\bdatenschutz\b', r'\bcompliance\b', r'\bregulat\w*\b'],

    # UX/UI & Design
    'FD_UX_UI_Design': [r'\bux\b', r'\bui\b', r'\buser experience\b', r'\buser interface\b', r'\bfigma\b', r'\bdesign\b'],

    # Web & APIs
    'FD_API_Webentwicklung': [r'\bapi\b', r'\brest\b', r'\bgraphql\b', r'\bmicroservice\w*\b', r'\bwebentwickl\w*\b', r'\bweb\s*develop\w*\b', r'\bfrontend\b', r'\bbackend\b', r'\bfull[\s-]*stack\b'],
    'FD_Scraping_Automatisierung': [r'\bscraping\b', r'\bweb scraping\b', r'\bcrawl\w*\b', r'\brpa\b', r'\bautomation\b', r'\bautomatisierung\b'],

    # Agile & Methoden
    'FD_Agile_Scrum': [r'\bagile\b', r'\bscrum\b', r'\bkanban\b', r'\bsafe\b', r'\bsprint\w*\b'],

    # Erfahrung
    'FD_Berufserfahrung_Jahre': [r'\b\d+\+?\s*(?:jahre?|years?)\s*(?:erfahrung|experience|berufserfahrung)\b', r'\bberufserfahrung\b', r'\bwork\s*experience\b', r'\bprofessional\s*experience\b'],
}


# ──────────────────────────────────────────────────
# 4) KATEGORISIERUNG DURCHFÜHREN
# ──────────────────────────────────────────────────
print("Kategorisierung läuft...")

all_categories = {}
all_categories.update(fachkompetenzen)
all_categories.update(soziale_kompetenz)
all_categories.update(methodenkompetenz)
all_categories.update(personale_kompetenz)
all_categories.update(fach_detail)

# Kategorien berechnen
for col_name, patterns in all_categories.items():
    df[col_name] = df['_text'].apply(lambda text: match_any(text, patterns))

# Aggregierte Dimensionen (Summe der Unterkategorien pro Hauptdimension)
fk_cols = [c for c in fachkompetenzen.keys()]
sk_cols = [c for c in soziale_kompetenz.keys()]
mk_cols = [c for c in methodenkompetenz.keys()]
pk_cols = [c for c in personale_kompetenz.keys()]
fd_cols = [c for c in fach_detail.keys()]

df['Fachkompetenz_Score'] = df[fk_cols].sum(axis=1)
df['Sozialkompetenz_Score'] = df[sk_cols].sum(axis=1)
df['Methodenkompetenz_Score'] = df[mk_cols].sum(axis=1)
df['Personalkompetenz_Score'] = df[pk_cols].sum(axis=1)
df['Fachdetail_Score'] = df[fd_cols].sum(axis=1)


# ──────────────────────────────────────────────────
# 5) OUTPUT
# ──────────────────────────────────────────────────
# Spaltenreihenfolge definieren
meta_cols = ['job_profil', 'job_title', 'company', 'location', 'veroeffentlicht_am', 'url', 'quelle']
score_cols = ['Fachkompetenz_Score', 'Sozialkompetenz_Score', 'Methodenkompetenz_Score', 'Personalkompetenz_Score', 'Fachdetail_Score']
output_cols = meta_cols + score_cols + fk_cols + fd_cols + sk_cols + mk_cols + pk_cols

df_out = df[output_cols]
df_out.to_csv('jobs_kategorisiert.csv', index=False, encoding='utf-8-sig')

print(f"\nOutput: jobs_kategorisiert.csv ({len(df_out)} Zeilen, {len(output_cols)} Spalten)")
print(f"\nSpalten-Übersicht:")
print(f"  Meta-Daten: {len(meta_cols)}")
print(f"  Score-Aggregationen: {len(score_cols)}")
print(f"  Fachkompetenz (Framework): {len(fk_cols)}")
print(f"  Fachkompetenz (Detail): {len(fd_cols)}")
print(f"  Soziale Kompetenz: {len(sk_cols)}")
print(f"  Methodenkompetenz: {len(mk_cols)}")
print(f"  Personale Kompetenz: {len(pk_cols)}")

print(f"\n=== Zusammenfassung der Häufigkeiten ===")
print("\n--- Fachkompetenzen (Framework) ---")
for c in fk_cols:
    print(f"  {c}: {df[c].sum()}")

print("\n--- Fachkompetenzen (Detail) ---")
for c in sorted(fd_cols, key=lambda x: -df[x].sum()):
    if df[c].sum() > 0:
        print(f"  {c}: {df[c].sum()}")

print("\n--- Soziale Kompetenz ---")
for c in sorted(sk_cols, key=lambda x: -df[x].sum()):
    print(f"  {c}: {df[c].sum()}")

print("\n--- Methodenkompetenz ---")
for c in sorted(mk_cols, key=lambda x: -df[x].sum()):
    print(f"  {c}: {df[c].sum()}")

print("\n--- Personale Kompetenz ---")
for c in sorted(pk_cols, key=lambda x: -df[x].sum()):
    print(f"  {c}: {df[c].sum()}")
