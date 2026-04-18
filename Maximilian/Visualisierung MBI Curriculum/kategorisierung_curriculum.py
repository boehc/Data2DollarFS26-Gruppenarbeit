"""
===============================================================================
CURRICULUM-KATEGORISIERUNG NACH KOMPETENZ-FRAMEWORK (VL4)
===============================================================================
Wendet das gleiche Framework an, das für jobs_kategorisiert.csv genutzt wurde:
  - FK_  = Fachkompetenz (10 Unterkategorien)
  - FD_  = Fachdetail / TechSkills (29 Unterkategorien)
  - SK_  = Sozialkompetenz (10 Unterkategorien)
  - MK_  = Methodenkompetenz (10 Unterkategorien)
  - PK_  = Personalkompetenz (10 Unterkategorien)
  + Scores pro Hauptkategorie

Input:  mbi_curriculum_enriched_keywords.csv (84 Kurse)
Output: mbi_curriculum_kategorisiert.csv (erweitert, nichts gelöscht)
===============================================================================
"""

import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. DATEN LADEN
# =============================================================================
df = pd.read_csv("mbi_curriculum_enriched_keywords.csv", sep=";")
print(f"Geladen: {len(df)} Kurse")

# =============================================================================
# 2. KEYWORD-REGELWERK (pro Framework-Spalte)
# =============================================================================
# Für jeden Skill aus dem Framework definieren wir Regex-Patterns,
# die sowohl englische als auch deutsche Begriffe abdecken.
# Gematcht wird gegen:
#   - extracted_keywords
#   - learning_objectives_raw
#   - course_content_raw
#   - course_title
# =============================================================================

SKILL_PATTERNS = {
    # =========================================================================
    # FACHKOMPETENZ (FK)
    # =========================================================================
    "FK_Waren_Produktkenntnisse": [
        r"product\b", r"produkt", r"waren", r"service design",
        r"product.?develop", r"product.?manag", r"product.?design",
        r"product.?portfolio", r"value.?proposition",
        r"service.?innovation", r"offering",
    ],
    "FK_Komplexe_Fertigkeiten": [
        r"complex", r"komplex", r"advanced.?skill",
        r"interdisziplin", r"interdisciplin", r"cross.?function",
        r"system.?thinking", r"systemdenken", r"synthesis",
        r"multi.?disciplin",
    ],
    "FK_Fremdsprachen": [
        r"\benglish\b", r"\benglisch\b", r"\bfrench\b", r"\bfranzös",
        r"fremdsprach", r"language.?skill", r"sprachkenntnisse",
        r"multilingual", r"bilingual", r"foreign.?language",
    ],
    "FK_Fuehrerschein": [
        r"führerschein", r"driver.?licen", r"fahrerlaubnis",
    ],
    "FK_Auslandserfahrung": [
        r"international", r"global", r"abroad", r"ausland",
        r"cross.?border", r"cross.?cultural", r"interkulturell",
        r"emerging.?market", r"entwicklungsländ", r"developing.?countr",
    ],
    "FK_Vertriebserfahrung": [
        r"sales", r"vertrieb", r"go.?to.?market",
        r"commerciali", r"business.?develop",
        r"customer.?acqui", r"akquisition", r"revenue",
        r"pitch", r"investor", r"funding",
    ],
    "FK_Projekterfahrung": [
        r"project", r"projekt", r"praxis.?partner",
        r"real.?world", r"case.?study", r"hands.?on",
        r"industry.?collabor", r"praxisnah", r"anwendung",
        r"FPV\b", r"research.?pra",
    ],
    "FK_EDV_Kenntnisse": [
        r"\bIT\b", r"\bICT\b", r"software", r"digital",
        r"computer", r"technolog", r"edv\b",
        r"information.?system", r"informationssystem",
        r"data", r"daten", r"tool", r"platform",
        r"applikation", r"application",
    ],
    "FK_Berufsausbildung": [
        r"career", r"beruf", r"qualification", r"qualifikation",
        r"professional.?develop", r"curriculum", r"degree",
        r"bachelor", r"master", r"certificate", r"zertifikat",
        r"ausbildung", r"studium", r"graduate",
    ],
    "FK_Branchenerfahrung": [
        r"industr", r"branch", r"sector", r"healthcare",
        r"fintech", r"banking", r"insurance", r"retail",
        r"manufacturing", r"automotive", r"pharma",
        r"logistics", r"telecom", r"energy",
        r"real.?estate", r"consulting",
    ],

    # =========================================================================
    # FACHDETAIL / TECHSKILLS (FD)
    # =========================================================================
    "FD_Python": [
        r"\bpython\b",
    ],
    "FD_Java": [
        r"\bjava\b(?!script)",
    ],
    "FD_JavaScript_TypeScript": [
        r"javascript", r"typescript", r"\bjs\b",
        r"\breact\b", r"\bangular\b", r"\bvue\b", r"\bnode\.?js\b",
    ],
    "FD_CSharp": [
        r"\bc#\b", r"\bcsharp\b", r"\.net\b",
    ],
    "FD_SQL": [
        r"\bsql\b", r"database", r"datenbank", r"\bmongodb\b",
        r"\bnosql\b", r"relational.?data",
    ],
    "FD_R_Statistik": [
        r"\br\b.*statist", r"statistik", r"statistics",
        r"statist.*method", r"\bspss\b", r"\bstata\b",
        r"quantitat.*forsch", r"quantitative.?research",
        r"regression", r"hypothesis",
    ],
    "FD_HTML_CSS": [
        r"\bhtml\b", r"\bcss\b", r"web.?design",
    ],
    "FD_PHP_Ruby_andere": [
        r"\bphp\b", r"\bruby\b", r"\bperl\b", r"\bgo\b.*lang",
        r"\brust\b", r"\bswift\b", r"\bkotlin\b",
    ],
    "FD_Cloud_AWS_Azure_GCP": [
        r"\bcloud\b", r"\baws\b", r"\bazure\b", r"\bgcp\b",
        r"google.?cloud", r"amazon.?web", r"cloud.?comput",
        r"saas\b", r"iaas\b", r"paas\b",
    ],
    "FD_Docker_Kubernetes": [
        r"\bdocker\b", r"\bkubernetes\b", r"\bk8s\b",
        r"container", r"microservice",
    ],
    "FD_DevOps_CICD": [
        r"devops", r"ci.?cd", r"continuous.?integr",
        r"continuous.?deliver", r"continuous.?deploy",
        r"infrastructure.?as.?code",
    ],
    "FD_Data_Science_ML": [
        r"data.?science", r"machine.?learn", r"\bml\b",
        r"deep.?learn", r"neural.?net", r"supervised",
        r"unsupervised", r"classification", r"clustering",
        r"feature.?engineer", r"model.?training",
        r"predictive.?model", r"prediction",
    ],
    "FD_AI_KI": [
        r"\bai\b", r"\bki\b", r"artificial.?intellig",
        r"künstliche.?intellig", r"generative.?ai",
        r"generative.?ki", r"\bchatgpt\b", r"\bgpt\b",
        r"\bgemini\b", r"\bllm\b", r"large.?language",
        r"genai", r"gen.?ai",
    ],
    "FD_NLP_LLM": [
        r"\bnlp\b", r"natural.?language", r"\bllm\b",
        r"large.?language", r"text.?mining", r"text.?analy",
        r"sentiment", r"chatbot", r"conversation.?design",
        r"prompt.?engineer",
    ],
    "FD_Data_Analysis_BI": [
        r"data.?analy", r"datenanalyse", r"business.?intellig",
        r"\bbi\b", r"analytics", r"dashboar", r"report",
        r"data.?visuali", r"visualisierung", r"visualization",
        r"insight", r"kpi\b", r"metric",
    ],
    "FD_Data_Engineering_ETL": [
        r"data.?engineer", r"\betl\b", r"data.?pipeline",
        r"data.?warehouse", r"data.?lake", r"data.?processing",
        r"data.?integr", r"data.?prep",
    ],
    "FD_SAP": [
        r"\bsap\b",
    ],
    "FD_Salesforce": [
        r"\bsalesforce\b",
    ],
    "FD_ERP": [
        r"\berp\b", r"enterprise.?resource",
    ],
    "FD_CRM": [
        r"\bcrm\b", r"customer.?relationship.?manage",
    ],
    "FD_MS_Office": [
        r"ms.?office", r"microsoft.?office",
        r"\bexcel\b", r"\bword\b", r"\bpowerpoint\b",
        r"office.?365", r"microsoft.?365",
    ],
    "FD_Jira_Confluence": [
        r"\bjira\b", r"\bconfluence\b", r"\batlassian\b",
    ],
    "FD_Cyber_Security": [
        r"cyber.?secur", r"information.?secur", r"it.?secur",
        r"security.?engineer", r"penetration",
        r"encryption", r"firewall", r"vulnerability",
    ],
    "FD_Datenschutz_DSGVO": [
        r"datenschutz", r"dsgvo", r"gdpr", r"privacy",
        r"data.?protection", r"compliance",
        r"regulat", r"governance", r"ethik", r"ethic",
        r"responsible.?ai", r"responsible.?use",
        r"socio.?technical.?risk",
    ],
    "FD_UX_UI_Design": [
        r"\bux\b", r"\bui\b", r"user.?experience",
        r"user.?interface", r"user.?centered",
        r"nutzerzentri", r"usability", r"human.?centered",
        r"human.?computer", r"\bhci\b",
        r"interaction.?design", r"interaktionsgestalt",
        r"\bfigma\b", r"prototyp.*interface",
        r"needfinding", r"user.?test",
        r"design.?thinking",
    ],
    "FD_API_Webentwicklung": [
        r"\bapi\b", r"web.?develop", r"web.?app",
        r"rest.?api", r"microservice", r"backend",
        r"frontend", r"full.?stack",
    ],
    "FD_Scraping_Automatisierung": [
        r"scraping", r"automat", r"rpa\b",
        r"robotic.?process", r"web.?scraping",
        r"bot\b", r"workflow.?automat",
    ],
    "FD_Agile_Scrum": [
        r"agile", r"scrum", r"kanban", r"sprint",
        r"lean.?startup", r"lean.?manag",
        r"iterativ", r"iterative",
        r"design.?sprint", r"rapid.?prototyp",
    ],

    # =========================================================================
    # SOZIALKOMPETENZ (SK)
    # =========================================================================
    "SK_Kooperationsfaehigkeit": [
        r"cooperat", r"kooperat", r"collaborat", r"zusammenarbeit",
        r"co.?creat", r"partner", r"gemeinschaft",
        r"gemeinsam", r"co.?develop",
    ],
    "SK_Verhandlungsgeschick": [
        r"negotiat", r"verhandl",
        r"stakeholder.?manag", r"conflict.?resolut",
        r"persuasi", r"überzeugungs",
    ],
    "SK_Durchsetzungsvermoegen": [
        r"assertiv", r"durchsetzung",
        r"entscheidungsfreud", r"decision.?authority",
        r"leadership", r"führung",
    ],
    "SK_Kritikfaehigkeit": [
        r"critical.*reflect", r"kritik", r"critical.*think",
        r"kritisch.*reflect", r"kritisch.*denken",
        r"critical.*assess", r"peer.?review",
        r"konstruktiv.*feedback",
    ],
    "SK_Teamfaehigkeit": [
        r"\bteam\b", r"teamwork", r"teamarbeit", r"group.?work",
        r"gruppenarbeit", r"team.?collaborat",
        r"team.?project", r"team.?based",
        r"kleine.?gruppe", r"small.?group",
    ],
    "SK_Hilfsbereitschaft": [
        r"hilfsbereit", r"helpful", r"support",
        r"mentor", r"coaching", r"peer.?support",
        r"unterstütz",
    ],
    "SK_Fairness": [
        r"fair", r"equity", r"gender.?equal",
        r"gleichstellung", r"gerecht", r"justice",
        r"inclusion", r"inklusion", r"diversity", r"diversit",
    ],
    "SK_Kundenorientierung": [
        r"customer", r"kunden", r"nutzer.*orientier",
        r"user.?need", r"client", r"consumer",
        r"customer.?centric", r"kundenbedürfnis",
        r"customer.?journey", r"user.?research",
        r"nutzerbedürfnis", r"zielgruppe", r"target.?group",
    ],
    "SK_Vorurteilsfreiheit": [
        r"vorurteil", r"unbiased", r"open.?mind",
        r"diversit", r"inclusion", r"interkulturell",
        r"cross.?cultural", r"multicultural",
    ],
    "SK_Respekt": [
        r"respekt", r"respect", r"wertschätzung",
        r"appreciation", r"dignit", r"würde",
    ],

    # =========================================================================
    # METHODENKOMPETENZ (MK)
    # =========================================================================
    "MK_Konzeptionelle_Staerke": [
        r"concept", r"konzept", r"framework",
        r"model", r"modell", r"systematisch",
        r"systematic", r"structur", r"struktur",
        r"architect", r"blueprint", r"design.?principle",
    ],
    "MK_Effektives_Arbeiten": [
        r"effektiv", r"effective", r"efficien",
        r"effizienz", r"produktiv", r"productive",
        r"optimiz", r"optimier", r"lean\b",
        r"process.?improve", r"continuous.?improve",
    ],
    "MK_Projektmanagement": [
        r"project.?manag", r"projektmanag",
        r"projek.*leit", r"project.?lead",
        r"project.?plan", r"mileston",
        r"scope", r"deliverable", r"project.?lifecycle",
        r"project.?phase",
    ],
    "MK_Strategieentwicklung": [
        r"strateg", r"vision", r"roadmap",
        r"long.?term", r"langfrist", r"competitive.?advant",
        r"wettbewerbsvorteil", r"marktposition",
        r"market.?position", r"business.?plan",
    ],
    "MK_Praesentation": [
        r"present", r"präsent", r"pitch",
        r"communicate", r"kommunik",
        r"visualization", r"visualisier",
        r"storytell", r"infographic",
        r"adressatengerecht", r"audience",
    ],
    "MK_Selbstmanagement": [
        r"self.?manag", r"selbstmanag",
        r"selbstorganis", r"self.?organiz",
        r"self.?study", r"selbststudium",
        r"time.?manag", r"zeitmanag",
        r"eigenverantwort", r"independent",
        r"selbst(st)?ändig",
    ],
    "MK_Moderationstechnik": [
        r"moderati", r"facilitat", r"workshop.?lead",
        r"diskussion.*leit", r"group.?discussion",
        r"seminar.*leit",
    ],
    "MK_Koordination": [
        r"koordinat", r"coordinat", r"orchestrat",
        r"stakeholder.?engag", r"abstimm",
        r"cross.?function", r"interdisziplin",
    ],
    "MK_Kreatives_Denken": [
        r"creat", r"kreativ", r"innovat",
        r"ideat", r"brainstorm", r"design.?think",
        r"out.?of.?the.?box", r"imagination",
        r"novel", r"new.?idea", r"neue.?idee",
        r"invention", r"disruption",
    ],
    "MK_Stressmanagement": [
        r"stress", r"resilience", r"resilienz",
        r"pressure", r"belastbar", r"workload",
        r"time.?pressure", r"zeitdruck",
        r"work.?life", r"burnout",
    ],

    # =========================================================================
    # PERSONALKOMPETENZ (PK)
    # =========================================================================
    "PK_Ausstrahlung_Charisma": [
        r"charisma", r"ausstrahlung", r"presence",
        r"überzeugend", r"compelling", r"inspir",
        r"visionary", r"visionär",
    ],
    "PK_Aufgeschlossenheit": [
        r"aufgeschlossen", r"open.?mind", r"curios",
        r"neugier", r"willing.*learn", r"lernbereit",
        r"receptive", r"offen",
    ],
    "PK_Unternehmerisches_Denken": [
        r"entrepreneur", r"unternehmer",
        r"intrapreneur", r"startup",
        r"venture", r"gründ", r"founder",
        r"business.?model", r"geschäftsmodell",
        r"scale.?up", r"opportunity", r"chancen",
    ],
    "PK_Menschenkenntnis": [
        r"menschenkenntnis", r"empathy.*understand",
        r"social.?awareness", r"interperson",
        r"emotional.?intellig",
    ],
    "PK_Empathie": [
        r"empath", r"einfühl", r"perspect.*tak",
        r"understand.*need", r"bedürfnis.*versteh",
        r"human.?centered", r"user.?centered",
        r"nutzerzentri", r"menschzentri",
    ],
    "PK_Auffassungsgabe": [
        r"auffassungsgabe", r"quick.?learner",
        r"comprehension", r"analytical.?skill",
        r"analytisch", r"analytical.*think",
        r"analytisches.*denken", r"critical.*analy",
        r"problem.*analy", r"problem.*solv",
    ],
    "PK_Motivation": [
        r"motivat", r"engage", r"leidenschaft",
        r"passion", r"drive", r"begeister",
        r"commitment", r"dedic",
    ],
    "PK_Interesse": [
        r"interest", r"interesse", r"curios", r"neugier",
        r"explor", r"discover", r"entdeck",
    ],
    "PK_Belastbarkeit": [
        r"belastbar", r"resilient", r"resilience", r"resilienz",
        r"robust", r"stamina", r"endurance",
        r"challenging", r"pressure",
    ],
    "PK_Entschlossenheit": [
        r"entschlossen", r"determined", r"decisive",
        r"proactive", r"proaktiv", r"initiative",
        r"eigeninitiativ", r"self.?starter",
        r"action.?oriented", r"handlungsorientiert",
    ],
}


# =============================================================================
# 3. MATCHING-FUNKTION
# =============================================================================
def match_skill(text, patterns):
    """
    Prüft ob eines der Patterns im Text vorkommt.
    Gibt 1 (Match) oder 0 (kein Match) zurück.
    """
    if pd.isna(text):
        return 0
    text_lower = str(text).lower()
    for pattern in patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return 1
    return 0


def categorize_course(row, skill_patterns):
    """
    Kategorisiert einen Kurs gegen alle Framework-Spalten.
    Sucht in: extracted_keywords, learning_objectives_raw, course_content_raw, course_title
    """
    # Kombiniere alle Textfelder für die Suche
    search_text = " | ".join([
        str(row.get("extracted_keywords", "")),
        str(row.get("learning_objectives_raw", "")),
        str(row.get("course_content_raw", "")),
        str(row.get("course_title", "")),
    ])

    results = {}
    for skill_name, patterns in skill_patterns.items():
        results[skill_name] = match_skill(search_text, patterns)

    return pd.Series(results)


# =============================================================================
# 4. KATEGORISIERUNG DURCHFÜHREN
# =============================================================================
print("Kategorisiere Kurse...")

# Alle Skills matchen
skill_results = df.apply(lambda row: categorize_course(row, SKILL_PATTERNS), axis=1)

# Scores berechnen (Summe der Unterkategorien)
fk_cols = [c for c in skill_results.columns if c.startswith("FK_")]
fd_cols = [c for c in skill_results.columns if c.startswith("FD_") and c != "FD_Berufserfahrung_Jahre"]
sk_cols = [c for c in skill_results.columns if c.startswith("SK_")]
mk_cols = [c for c in skill_results.columns if c.startswith("MK_")]
pk_cols = [c for c in skill_results.columns if c.startswith("PK_")]

skill_results["Fachkompetenz_Score"] = skill_results[fk_cols].sum(axis=1)
skill_results["Sozialkompetenz_Score"] = skill_results[sk_cols].sum(axis=1)
skill_results["Methodenkompetenz_Score"] = skill_results[mk_cols].sum(axis=1)
skill_results["Personalkompetenz_Score"] = skill_results[pk_cols].sum(axis=1)
skill_results["Fachdetail_Score"] = skill_results[fd_cols].sum(axis=1)

# =============================================================================
# 5. ERGEBNIS ZUSAMMENFÜHREN (bestehende Spalten bleiben erhalten!)
# =============================================================================
df_out = pd.concat([df, skill_results], axis=1)

# =============================================================================
# 6. SPEICHERN
# =============================================================================
output_file = "mbi_curriculum_kategorisiert.csv"
df_out.to_csv(output_file, sep=";", index=False)
print(f"\n✓ Gespeichert: {output_file}")
print(f"  → {len(df_out)} Kurse, {len(df_out.columns)} Spalten")

# =============================================================================
# 7. ZUSAMMENFASSUNG
# =============================================================================
print("\n" + "=" * 70)
print("ERGEBNIS-ÜBERSICHT")
print("=" * 70)

print(f"\n  Hauptkategorien-Scores (Durchschnitt über {len(df_out)} Kurse):")
for score in ["Fachkompetenz_Score", "Sozialkompetenz_Score", "Methodenkompetenz_Score",
              "Personalkompetenz_Score", "Fachdetail_Score"]:
    print(f"    {score:30s}  Ø {df_out[score].mean():.1f}  (max {df_out[score].max()})")

print(f"\n  Fachkompetenz-Unterkategorien (Anteil der Kurse mit Match):")
for c in fk_cols:
    hits = skill_results[c].sum()
    pct = hits / len(df_out) * 100
    print(f"    {c:35s}  {hits:3d} Kurse  ({pct:.0f}%)")

print(f"\n  TechSkills / Fachdetails (Anteil der Kurse mit Match):")
for c in sorted(fd_cols, key=lambda x: -skill_results[x].sum()):
    hits = skill_results[c].sum()
    pct = hits / len(df_out) * 100
    if hits > 0:
        print(f"    {c:35s}  {hits:3d} Kurse  ({pct:.0f}%)")

print(f"\n  Sozialkompetenz-Unterkategorien:")
for c in sk_cols:
    hits = skill_results[c].sum()
    pct = hits / len(df_out) * 100
    print(f"    {c:35s}  {hits:3d} Kurse  ({pct:.0f}%)")

print(f"\n  Methodenkompetenz-Unterkategorien:")
for c in mk_cols:
    hits = skill_results[c].sum()
    pct = hits / len(df_out) * 100
    print(f"    {c:35s}  {hits:3d} Kurse  ({pct:.0f}%)")

print(f"\n  Personalkompetenz-Unterkategorien:")
for c in pk_cols:
    hits = skill_results[c].sum()
    pct = hits / len(df_out) * 100
    print(f"    {c:35s}  {hits:3d} Kurse  ({pct:.0f}%)")

# Stichprobe: Kurse mit höchsten Scores
print("\n\n  TOP-5 KURSE nach Gesamtscore:")
df_out["Gesamtscore"] = (df_out["Fachkompetenz_Score"] + df_out["Sozialkompetenz_Score"]
                          + df_out["Methodenkompetenz_Score"] + df_out["Personalkompetenz_Score"]
                          + df_out["Fachdetail_Score"])
top5 = df_out.nlargest(5, "Gesamtscore")[["course_title", "Fachkompetenz_Score",
                                            "Sozialkompetenz_Score", "Methodenkompetenz_Score",
                                            "Personalkompetenz_Score", "Fachdetail_Score", "Gesamtscore"]]
print(top5.to_string(index=False))

# Aufräumen: Gesamtscore war nur für die Anzeige
df_out.drop(columns=["Gesamtscore"], inplace=True)
# Re-save ohne Gesamtscore
df_out.to_csv(output_file, sep=";", index=False)
