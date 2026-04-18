"""
Profil-Zuordnung aller 1194 Stelleninserate auf 6 neue Profile
basierend auf Jobtitel-Keywords.
"""
import pandas as pd
import re

df = pd.read_csv("jobs_kategorisiert.csv")

# ============================================================================
# 6 PROFILE MIT KEYWORD-REGELN (Prioritätsreihenfolge!)
# ============================================================================
# Jedes Profil hat eine Liste von Regex-Patterns.
# Die Reihenfolge bestimmt die Priorität bei Mehrfach-Treffern:
#   Spezifischere Profile zuerst, generische zuletzt.
# ============================================================================

PROFILE_RULES = {
    # ---- 1. SUPPLY CHAIN & OPERATIONS (sehr spezifisch) ----
    "Supply Chain & Operations Management": [
        r"supply.?chain", r"logisti", r"einkauf", r"beschaffung",
        r"procurement", r"distribution", r"transport", r"lager",
        r"warehouse", r"manufacturing", r"produktions",
        r"operations.*(manager|leiter|director|head|chief|trainee|controlling)",
        r"(leiter|manager|head).*(operations|produktion|fertigung|logistik)",
        r"lean\b", r"industrial.?engineer", r"IE\b.*spezialist",
        r"COO\b", r"supply.?planner", r"demand.?planner",
        r"facility.?manag", r"betriebsleiter",
        r"quality.?(manager|engineer|specialist|assurance)",
        r"production", r"operation analyst",
        r"material", r"inventory", r"fleet",
    ],

    # ---- 2. START-UP & SCALE-UP (Entrepreneurship / Innovation / Product) ----
    "Start-up & Scale-up Entrepreneurship": [
        r"start.?up", r"entrepreneur", r"gr[üu]nd", r"founder",
        r"venture", r"scale.?up", r"incubat", r"accelerat",
        r"innovation", r"product.?manag", r"product.?own",
        r"product.?develop", r"product.?design", r"product.?lead",
        r"chief.*innovation", r"new.?business", r"business.?model",
        r"growth.?(manager|lead|specialist|hacker)",
        r"go.?to.?market",
    ],

    # ---- 3. TECHNOLOGY SOLUTION ARCHITECT (IT-Technik / Entwicklung) ----
    "Technology Solution Architect": [
        r"solution.?(architect|develop|design|engineer)",
        r"software", r"developer\b", r"entwickler",
        r"(full.?stack|backend|frontend|web).?(develop|engineer)",
        r"cloud", r"(IT|ICT).?(architect|engineer|specialist|security)",
        r"data.?(engineer|scientist|architect|analy)",
        r"devops", r"(system|platform|infrastructure).?(engineer|architect|admin)",
        r"machine.?learning", r"\bAI\b", r"\bKI\b", r"\bML\b",
        r"cyber.?security", r"security.?(engineer|analyst|architect|platform|specialist|operation|officer)",
        r"integration.?engineer", r"programmier",
        r"database", r"netzwerk", r"network",
        r"java\b", r"python\b", r"\.net\b", r"\bc#", r"\bphp\b",
        r"BI.?(solution|architect|engineer|developer)",
        r"SAP\b", r"abacus", r"ERP\b",
        r"betriebsinformatik", r"wirtschaftsinformatik",
        r"informatik", r"IT.?(manager|leiter|director|head|lead|strateg|project|koordinat)",
        r"IT.?service", r"IT.?support", r"IT.?admin",
        r"(system|applikation|application).?(admin|manager|engineer|support|specialist)",
        r"test.?(manager|engineer|analyst|autom)",
        r"automation.?engineer",
        r"architect\b", r"tech.?(lead|manager|director|officer|head)",
        r"CTO\b", r"CIO\b",
        r"power.?bi", r"tableau",
        r"API\b", r"microservice",
        r"salesforce", r"dynamics.?365",
        r"sharepoint", r"microsoft.?365", r"m365",
        r"jira", r"confluence",
    ],

    # ---- 4. DIGITAL CHANNEL & CRM ----
    "Digital Channel & CRM": [
        r"digital.?(channel|marketing|media|commerce|campaign|content|manag)",
        r"e.?commerce", r"online.?(market|shop|handel)",
        r"CRM\b", r"customer.?(relationship|experience|journey|success|engage)",
        r"(community|social.?media).?manag",
        r"marketing", r"brand.?manag",
        r"channel.?manag", r"relationship.?manag",
        r"kundenberat", r"kundenberater",
        r"content.?(manager|creator|specialist|strateg)",
        r"SEO\b", r"SEM\b", r"SEA\b", r"campaign",
        r"customer.?service", r"kundendienst", r"kundendienstleiter",
        r"contact.?center", r"call.?center",
        r"kommunikation", r"communication",
        r"UX\b", r"user.?experience",
        r"e.?banking", r"mobile.?banking", r"digital.?banking",
    ],

    # ---- 5. BUSINESS DEVELOPMENT ----
    "Business Development": [
        r"business.?develop", r"\bBD\b",
        r"(key.?)?account.?(manager|executive|director)",
        r"sales", r"vertrieb", r"akquisition",
        r"partner.?(manager|develop|director)",
        r"business.?unit.?(manager|head|lead)",
        r"commercial", r"market.?(develop|expansion)",
        r"recruitment.?consultant", r"personalberater",
        r"business.?controller", r"revenue",
        r"pricing",
    ],

    # ---- 6. TRANSFORMING & MANAGING DIGITAL BUSINESS (Catch-all) ----
    "Transforming & Managing Digital Business": [
        r".*",  # Fängt alles auf, was oben nicht getroffen wurde
    ],
}


def classify_job(title):
    """Ordnet einen Jobtitel dem passendsten Profil zu."""
    if pd.isna(title):
        return "Transforming & Managing Digital Business"
    title_lower = str(title).lower()

    # Explizite Vorab-Regeln für mehrdeutige Titel
    if re.search(r"business.?develop", title_lower):
        return "Business Development"
    if re.search(r"business.?analyst|business.?consult|business.?process", title_lower):
        return "Transforming & Managing Digital Business"

    for profil, patterns in PROFILE_RULES.items():
        if profil == "Transforming & Managing Digital Business":
            return profil  # Catch-all
        for pattern in patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                return profil
    return "Transforming & Managing Digital Business"


# Zuordnung durchführen
df["profil_neu"] = df["job_title"].apply(classify_job)

# Ergebnis anzeigen
print("=" * 70)
print("NEUE PROFIL-ZUORDNUNG (alle 1194 Zeilen)")
print("=" * 70)
print(df["profil_neu"].value_counts().to_string())
print()

# Vergleich alt vs. neu
print("\nKREUZTABELLE: Alt (indeed-Profile) vs. Neu")
print("-" * 70)
ct = pd.crosstab(
    df["job_profil"].fillna("(kein Profil / jobs.ch)"),
    df["profil_neu"],
    margins=True,
)
print(ct.to_string())

# Stichprobe: Was landete wo?
print("\n\nSTICHPROBE PRO NEUEM PROFIL (je 5 Titel):")
print("=" * 70)
for profil in PROFILE_RULES.keys():
    subset = df[df["profil_neu"] == profil]["job_title"].head(5)
    print(f"\n{profil}:")
    for t in subset.values:
        print(f"  → {t}")

# Nicht zugeordnet?
fallback = df[df["profil_neu"] == "Transforming & Managing Digital Business"]
print(f"\n\nFallback (Transforming & Managing Digital Business): {len(fallback)} Zeilen")
print("Davon aus jobs.ch (ohne altes Profil):")
fb_jobsch = fallback[fallback["job_profil"].isna()]
print(f"  {len(fb_jobsch)} Zeilen")
if len(fb_jobsch) > 0:
    print("  Beispiele:")
    for t in fb_jobsch["job_title"].head(10).values:
        print(f"    → {t}")
