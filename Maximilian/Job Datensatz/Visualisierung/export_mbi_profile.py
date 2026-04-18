"""
Exportiert jobs_kategorisiert.csv mit der neuen MBI-Profil-Zuordnung
für alle 1194 Stelleninserate.
"""
import pandas as pd
import re

df = pd.read_csv("jobs_kategorisiert.csv")

PROFILE_RULES = {
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
    "Start-up & Scale-up Entrepreneurship": [
        r"start.?up", r"entrepreneur", r"gr[üu]nd", r"founder",
        r"venture", r"scale.?up", r"incubat", r"accelerat",
        r"innovation", r"product.?manag", r"product.?own",
        r"product.?develop", r"product.?design", r"product.?lead",
        r"chief.*innovation", r"new.?business", r"business.?model",
        r"growth.?(manager|lead|specialist|hacker)",
        r"go.?to.?market",
    ],
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
    "Transforming & Managing Digital Business": [
        r".*",
    ],
}


def classify_job(title):
    if pd.isna(title):
        return "Transforming & Managing Digital Business"
    title_lower = str(title).lower()
    if re.search(r"business.?develop", title_lower):
        return "Business Development"
    if re.search(r"business.?analyst|business.?consult|business.?process", title_lower):
        return "Transforming & Managing Digital Business"
    for profil, patterns in PROFILE_RULES.items():
        if profil == "Transforming & Managing Digital Business":
            return profil
        for pattern in patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                return profil
    return "Transforming & Managing Digital Business"


df["mbi_profil"] = df["job_title"].apply(classify_job)

# Alte Profil-Spalte entfernen
if "job_profil" in df.columns:
    df.drop(columns=["job_profil"], inplace=True)

# mbi_profil direkt nach job_title einfügen
cols = df.columns.tolist()
cols.remove("mbi_profil")
idx = cols.index("job_title") + 1
cols.insert(idx, "mbi_profil")
df = df[cols]

output = "jobs_kategorisiert_mbi_profile.csv"
df.to_csv(output, index=False)

n = len(df)
print(f"Gespeichert: {output} ({n} Zeilen, {len(df.columns)} Spalten)")
print()
for profil, count in df["mbi_profil"].value_counts().items():
    print(f"  {profil:45s}  {count:4d}  ({count/n*100:.1f}%)")
