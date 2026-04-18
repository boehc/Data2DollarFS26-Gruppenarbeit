"""
===============================================================================
SKILL-ANALYSE FÜR BUSINESS INNOVATION STUDIERENDE (v2)
===============================================================================
Statistische Visualisierung der Kompetenz-Anforderungen in Stelleninseraten
Erstellt mit Seaborn für publikationsreife Grafiken.

Fragestellungen:
  1) Häufigkeit der 4 Hauptkategorien (Fach-, Sozial-, Methoden-, Personalkompetenz)
  2) Detailansicht der Unterkategorien innerhalb jeder Hauptkategorie
  3) TechSkills-Analyse (FD-Spalten) – einzeln und im Vergleich zu FK-Spalten
  4) BONUS: Detaillierte MS-Tools-Analyse (aus jobs_kategorisiert_ms_detail.csv)

Datenquelle: 1'194 Stelleninserate → alle per Keyword auf 6 Profile zugeordnet
===============================================================================
"""

# =============================================================================
# 1. IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import re
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 2. SEABORN THEME-SETUP (Publikationsreif)
# =============================================================================
sns.set_theme(
    style="whitegrid",
    font_scale=1.1,
    rc={
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9,
        "figure.titlesize": 16,
    }
)

# =============================================================================
# 3. PROFIL-ZUORDNUNG (6 Profile, Keyword-basiert)
# =============================================================================
# Farbpalette für 6 Jobprofile
PROFIL_PALETTE = {
    "Business Dev.":     "#4CAF50",   # Grün
    "Digital Channel":   "#9C27B0",   # Lila
    "Startup/Scale-up":  "#FF9800",   # Orange
    "Supply Chain":      "#F44336",   # Rot
    "Tech Architect":    "#2196F3",   # Blau
    "Digital Business":  "#607D8B",   # Grau-Blau
}

PROFIL_SHORT = {
    "Business Development":                   "Business Dev.",
    "Digital Channel & CRM":                  "Digital Channel",
    "Start-up & Scale-up Entrepreneurship":   "Startup/Scale-up",
    "Supply Chain & Operations Management":   "Supply Chain",
    "Technology Solution Architect":          "Tech Architect",
    "Transforming & Managing Digital Business": "Digital Business",
}

# Keyword-Regeln (Prioritätsreihenfolge!)
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
        r".*",  # Catch-all
    ],
}


def classify_job(title):
    """Ordnet einen Jobtitel dem passendsten der 6 Profile zu."""
    if pd.isna(title):
        return "Transforming & Managing Digital Business"
    title_lower = str(title).lower()

    # Vorab-Regeln für mehrdeutige Titel
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


# =============================================================================
# 4. DATEN LADEN & PROFILE ZUORDNEN
# =============================================================================
print("Lade Daten...")
df = pd.read_csv("jobs_kategorisiert.csv")
df_ms = pd.read_csv("jobs_kategorisiert_ms_detail.csv")

# Neue Profil-Zuordnung für ALLE Zeilen
df["profil_neu"] = df["job_title"].apply(classify_job)
df_ms["profil_neu"] = df_ms["job_title"].apply(classify_job)

# Kurzbezeichnungen
df["profil_kurz"] = df["profil_neu"].map(PROFIL_SHORT)
df_ms["profil_kurz"] = df_ms["profil_neu"].map(PROFIL_SHORT)

n_jobs = len(df)
print(f"  → {n_jobs} Stelleninserate geladen (alle zugeordnet)")
print(f"\n  Profil-Verteilung:")
for profil, count in df["profil_kurz"].value_counts().items():
    print(f"    {profil:20s}  {count:4d}  ({count/n_jobs*100:.1f}%)")

# =============================================================================
# 5. SPALTENDEFINITIONEN
# =============================================================================
# Hauptkategorien (Score-Spalten)
haupt_scores = [
    "Fachkompetenz_Score",
    "Sozialkompetenz_Score",
    "Methodenkompetenz_Score",
    "Personalkompetenz_Score",
]

# Unterkategorien (binäre 0/1 Spalten)
fk_cols = [c for c in df.columns if c.startswith("FK_")]
sk_cols = [c for c in df.columns if c.startswith("SK_")]
mk_cols = [c for c in df.columns if c.startswith("MK_")]
pk_cols = [c for c in df.columns if c.startswith("PK_")]

# TechSkills / Fachdetails (binäre Spalten, FD_ Prefix)
fd_cols = [c for c in df.columns if c.startswith("FD_") and c != "FD_Berufserfahrung_Jahre"]

# MS-Tools (binäre Spalten)
ms_cols = [c for c in df_ms.columns if c.startswith("MS_") and c != "MS_Tools_Score"]

# Profil-Reihenfolge (nach Grösse)
profil_order = (
    df["profil_kurz"]
    .value_counts()
    .index.tolist()
)


def clean_label(col, prefix_len=3):
    """Entfernt den Prefix (FK_, SK_ etc.) und ersetzt Underscores."""
    return col[prefix_len:].replace("_", " ")


def create_heatmap_data(df_in, cols, prefix_len=3):
    """Berechnet % Nennungshäufigkeit pro Profil."""
    grouped = df_in.groupby("profil_kurz")[cols].mean() * 100
    grouped.columns = [clean_label(c, prefix_len) for c in cols]
    order = grouped.mean().sort_values(ascending=False).index
    return grouped[order]


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 1: HAUPTKATEGORIEN – Durchschnittliche Scores nach Jobprofil      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 1] Hauptkategorien – Grouped Barplot...")

df_haupt_long = df.melt(
    id_vars=["profil_kurz"],
    value_vars=haupt_scores,
    var_name="Kategorie",
    value_name="Score",
)
kategorie_labels = {
    "Fachkompetenz_Score": "Fachkompetenz",
    "Sozialkompetenz_Score": "Sozialkompetenz",
    "Methodenkompetenz_Score": "Methodenkompetenz",
    "Personalkompetenz_Score": "Personalkompetenz",
}
df_haupt_long["Kategorie"] = df_haupt_long["Kategorie"].map(kategorie_labels)

fig, ax = plt.subplots(figsize=(16, 7))
sns.barplot(
    data=df_haupt_long,
    x="Kategorie", y="Score",
    hue="profil_kurz",
    hue_order=profil_order,
    palette=PROFIL_PALETTE,
    ci=95, edgecolor="white", linewidth=0.8, ax=ax,
)
ax.set_title(
    "Durchschnittliche Kompetenz-Scores nach Jobprofil\n"
    f"(n = {n_jobs} Stelleninserate, Fehlerbalken = 95%-KI)",
    fontweight="bold", pad=15,
)
ax.set_xlabel("")
ax.set_ylabel("Durchschnittlicher Score", fontweight="bold")
ax.legend(title="Jobprofil", title_fontsize=10,
          bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
ax.set_ylim(0, ax.get_ylim()[1] * 1.1)
plt.tight_layout()
plt.savefig("plot1_hauptkategorien_scores.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot1_hauptkategorien_scores.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 2: UNTERKATEGORIEN – 4 Heatmaps                                   ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 2] Unterkategorien – 4 Heatmaps...")

fk_heatmap = create_heatmap_data(df, fk_cols)
sk_heatmap = create_heatmap_data(df, sk_cols)
mk_heatmap = create_heatmap_data(df, mk_cols)
pk_heatmap = create_heatmap_data(df, pk_cols)

fig, axes = plt.subplots(2, 2, figsize=(24, 18))
fig.suptitle(
    "Nennungshäufigkeit der Skill-Unterkategorien nach Jobprofil\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in % der Inserate)",
    fontsize=16, fontweight="bold", y=0.98,
)
heatmap_specs = [
    (fk_heatmap, "Fachkompetenz", "Blues"),
    (sk_heatmap, "Sozialkompetenz", "Greens"),
    (mk_heatmap, "Methodenkompetenz", "Oranges"),
    (pk_heatmap, "Personalkompetenz", "RdPu"),
]
for idx, (data, title, cmap) in enumerate(heatmap_specs):
    ax = axes[idx // 2, idx % 2]
    data_sorted = data.reindex(profil_order).dropna(how="all")
    sns.heatmap(
        data_sorted, annot=True, fmt=".0f", cmap=cmap,
        vmin=0, vmax=100, linewidths=0.5, linecolor="white",
        cbar_kws={"label": "% der Inserate", "shrink": 0.8}, ax=ax,
    )
    ax.set_title(f"{title}", fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel(""); ax.set_ylabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=9)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot2_unterkategorien_heatmaps.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot2_unterkategorien_heatmaps.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 3: UNTERKATEGORIEN – Horizontale Barplots (Gesamtranking)         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 3] Top Skills – Horizontale Barplots je Hauptkategorie...")

def create_horizontal_barplot(df_in, cols, prefix_len, title, color, ax):
    freq = df_in[cols].mean() * 100
    freq.index = [clean_label(c, prefix_len) for c in cols]
    freq = freq.sort_values(ascending=True)
    sns.barplot(x=freq.values, y=freq.index, color=color, edgecolor="white", linewidth=0.5, ax=ax)
    for i, val in enumerate(freq.values):
        ax.text(val + 1, i, f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("% der Stelleninserate")
    ax.set_ylabel("")
    ax.set_xlim(0, 100)

fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle(
    "Häufigkeit der Skill-Anforderungen nach Hauptkategorie\n"
    f"(n = {n_jobs} Stelleninserate · Anteil in %)",
    fontsize=16, fontweight="bold", y=0.99,
)
for cols, plen, title, color, ax in [
    (fk_cols, 3, "Fachkompetenz", "#2196F3", axes[0, 0]),
    (sk_cols, 3, "Sozialkompetenz", "#4CAF50", axes[0, 1]),
    (mk_cols, 3, "Methodenkompetenz", "#FF9800", axes[1, 0]),
    (pk_cols, 3, "Personalkompetenz", "#E91E63", axes[1, 1]),
]:
    create_horizontal_barplot(df, cols, plen, title, color, ax)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("plot3_unterkategorien_barplots.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot3_unterkategorien_barplots.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 4: UNTERKATEGORIEN – Grouped Barplot nach Jobprofil (4 Plots)     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 4] Unterkategorien – Grouped Barplot nach Jobprofil...")

all_sub_cols = fk_cols + sk_cols + mk_cols + pk_cols
sub_to_haupt = {}
for c in fk_cols: sub_to_haupt[c] = "Fachkompetenz"
for c in sk_cols: sub_to_haupt[c] = "Sozialkompetenz"
for c in mk_cols: sub_to_haupt[c] = "Methodenkompetenz"
for c in pk_cols: sub_to_haupt[c] = "Personalkompetenz"

df_sub_long = df.melt(
    id_vars=["profil_kurz"], value_vars=all_sub_cols,
    var_name="Skill", value_name="Vorhanden",
)
df_sub_long["Hauptkategorie"] = df_sub_long["Skill"].map(sub_to_haupt)
df_sub_long["Skill_Label"] = df_sub_long["Skill"].apply(lambda x: clean_label(x, 3))

df_sub_agg = (
    df_sub_long.groupby(["profil_kurz", "Hauptkategorie", "Skill_Label"])["Vorhanden"]
    .mean().reset_index()
)
df_sub_agg["Prozent"] = df_sub_agg["Vorhanden"] * 100

for haupt, color in zip(
    ["Fachkompetenz", "Sozialkompetenz", "Methodenkompetenz", "Personalkompetenz"],
    ["#2196F3", "#4CAF50", "#FF9800", "#E91E63"],
):
    subset = df_sub_agg[df_sub_agg["Hauptkategorie"] == haupt].copy()
    skill_order = subset.groupby("Skill_Label")["Prozent"].mean().sort_values(ascending=True).index.tolist()

    fig, ax = plt.subplots(figsize=(16, max(6, len(skill_order) * 0.7 + 2)))
    sns.barplot(
        data=subset, y="Skill_Label", x="Prozent",
        hue="profil_kurz", order=skill_order, hue_order=profil_order,
        palette=PROFIL_PALETTE, edgecolor="white", linewidth=0.5, ax=ax,
    )
    ax.set_title(
        f"{haupt}: Anforderungshäufigkeit nach Jobprofil\n"
        f"(n = {n_jobs} Stelleninserate · Angaben in %)",
        fontsize=14, fontweight="bold", pad=12,
    )
    ax.set_xlabel("% der Stelleninserate", fontweight="bold")
    ax.set_ylabel("")
    ax.set_xlim(0, 105)
    ax.legend(title="Jobprofil", title_fontsize=10,
              bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
    plt.tight_layout()
    plt.savefig(f"plot4_{haupt.lower()}_nach_profil.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Gespeichert: plot4_{haupt.lower()}_nach_profil.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 6: TECHSKILLS (FD_) – Einzelanalyse                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 6a] TechSkills – Gesamtranking (horizontaler Barplot)...")

# 6a: Gesamtranking aller TechSkills
fd_freq = df[fd_cols].mean() * 100
fd_freq.index = [clean_label(c, 3) for c in fd_cols]
fd_freq = fd_freq.sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(14, max(8, len(fd_cols) * 0.35 + 2)))
colors = sns.color_palette("viridis", n_colors=len(fd_freq))
sns.barplot(
    x=fd_freq.values, y=fd_freq.index,
    palette=colors, edgecolor="white", linewidth=0.5, ax=ax,
)
for i, val in enumerate(fd_freq.values):
    ax.text(val + 0.3, i, f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")

ax.set_title(
    "TechSkills (Fachdetail-Kompetenzen): Nennungshäufigkeit\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Stelleninserate", fontweight="bold")
ax.set_ylabel("")
ax.set_xlim(0, max(fd_freq.values) * 1.2)
plt.tight_layout()
plt.savefig("plot6a_techskills_gesamt.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot6a_techskills_gesamt.png")


# 6b: TechSkills – Heatmap nach Jobprofil
print("\n[Plot 6b] TechSkills – Heatmap nach Jobprofil...")

fd_heatmap = create_heatmap_data(df, fd_cols)

fig, ax = plt.subplots(figsize=(22, 8))
sns.heatmap(
    fd_heatmap.reindex(profil_order).dropna(how="all"),
    annot=True, fmt=".1f", cmap="YlGnBu",
    vmin=0, linewidths=0.5, linecolor="white",
    cbar_kws={"label": "% der Inserate", "shrink": 0.8}, ax=ax,
)
ax.set_title(
    "TechSkills nach Jobprofil: Nennungshäufigkeit (%)\n"
    f"(n = {n_jobs} Stelleninserate)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel(""); ax.set_ylabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=9)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
plt.tight_layout()
plt.savefig("plot6b_techskills_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot6b_techskills_heatmap.png")


# 6c: TechSkills nach Jobprofil – Grouped Barplot
print("\n[Plot 6c] TechSkills – Grouped Barplot nach Jobprofil...")

df_fd_long = df.melt(
    id_vars=["profil_kurz"], value_vars=fd_cols,
    var_name="Skill", value_name="Vorhanden",
)
df_fd_long["Skill_Label"] = df_fd_long["Skill"].apply(lambda x: clean_label(x, 3))

df_fd_agg = (
    df_fd_long.groupby(["profil_kurz", "Skill_Label"])["Vorhanden"]
    .mean().reset_index()
)
df_fd_agg["Prozent"] = df_fd_agg["Vorhanden"] * 100

# Nur TechSkills mit >2% Gesamthäufigkeit (sonst zu unübersichtlich)
relevant_fd = df_fd_agg.groupby("Skill_Label")["Prozent"].mean()
relevant_fd = relevant_fd[relevant_fd > 2].index.tolist()
df_fd_filtered = df_fd_agg[df_fd_agg["Skill_Label"].isin(relevant_fd)]

fd_order = (
    df_fd_filtered.groupby("Skill_Label")["Prozent"]
    .mean().sort_values(ascending=True).index.tolist()
)

fig, ax = plt.subplots(figsize=(16, max(8, len(fd_order) * 0.7 + 2)))
sns.barplot(
    data=df_fd_filtered, y="Skill_Label", x="Prozent",
    hue="profil_kurz", order=fd_order, hue_order=profil_order,
    palette=PROFIL_PALETTE, edgecolor="white", linewidth=0.5, ax=ax,
)
ax.set_title(
    "TechSkills nach Jobprofil (nur Skills > 2% Gesamthäufigkeit)\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Stelleninserate", fontweight="bold")
ax.set_ylabel("")
ax.legend(title="Jobprofil", title_fontsize=10,
          bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
plt.tight_layout()
plt.savefig("plot6c_techskills_nach_profil.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot6c_techskills_nach_profil.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 7: TECHSKILLS IM VERGLEICH ZU FACHKOMPETENZEN (FK vs. FD)         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 7a] FK vs. FD – Kombinierter Barplot...")

# 7a: Gesamtvergleich FK-Unterkategorien vs. aggregierte TechSkills
# → Wir berechnen den Durchschnitt ALLER FD-Spalten als "FD_TechSkills_gesamt"
#   und vergleichen das mit den einzelnen FK-Unterkategorien

# Berechne aggregierte TechSkill-Quote (mindestens 1 TechSkill genannt)
df["hat_techskill"] = (df[fd_cols].sum(axis=1) > 0).astype(int)

# FK-Spalten + TechSkill-Indikator zusammen
fk_plus_tech = fk_cols + ["hat_techskill"]
fk_plus_freq = df[fk_plus_tech].mean() * 100

labels = [clean_label(c, 3) for c in fk_cols] + ["Mind. 1 TechSkill"]
fk_plus_freq.index = labels
fk_plus_freq = fk_plus_freq.sort_values(ascending=True)

# Farben: FK blau, TechSkill hervorgehoben
bar_colors = ["#2196F3" if lab != "Mind. 1 TechSkill" else "#FF5722" for lab in fk_plus_freq.index]

fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(
    x=fk_plus_freq.values, y=fk_plus_freq.index,
    palette=bar_colors, edgecolor="white", linewidth=0.5, ax=ax,
)
for i, val in enumerate(fk_plus_freq.values):
    ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")

ax.set_title(
    "Fachkompetenz-Unterkategorien vs. TechSkills (Fachdetails)\n"
    f"(n = {n_jobs} · Rot = mind. 1 TechSkill genannt · Blau = FK-Unterkategorien)",
    fontsize=13, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Stelleninserate", fontweight="bold")
ax.set_ylabel("")
ax.set_xlim(0, 105)
plt.tight_layout()
plt.savefig("plot7a_fk_vs_techskills_vergleich.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot7a_fk_vs_techskills_vergleich.png")


# 7b: Stacked View – FK + FD als kombinierte Heatmap nach Profil
print("\n[Plot 7b] FK + FD – Kombinierte Heatmap nach Profil...")

# FK und FD zusammen
fk_fd_cols = fk_cols + fd_cols
fk_fd_heatmap = create_heatmap_data(df, fk_fd_cols)

# Kategorie-Markierung für die Achse
fk_fd_labels = fk_fd_heatmap.columns.tolist()
fk_fd_colors = []
for orig_col in fk_fd_heatmap.columns:
    # Prüfe ob es FK oder FD ist basierend auf dem Original-Label
    matched = False
    for c in fk_cols:
        if clean_label(c, 3) == orig_col:
            fk_fd_colors.append("#2196F3")
            matched = True
            break
    if not matched:
        fk_fd_colors.append("#FF5722")

fig, ax = plt.subplots(figsize=(28, 8))
sns.heatmap(
    fk_fd_heatmap.reindex(profil_order).dropna(how="all"),
    annot=True, fmt=".0f", cmap="YlOrBr",
    vmin=0, linewidths=0.5, linecolor="white",
    cbar_kws={"label": "% der Inserate", "shrink": 0.8}, ax=ax,
)
ax.set_title(
    "Fachkompetenz (FK) + TechSkills (FD) kombiniert nach Jobprofil\n"
    f"(n = {n_jobs} · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel(""); ax.set_ylabel("")
# Achsen-Labels einfärben (FK blau, FD rot)
xticklabels = ax.get_xticklabels()
for label, color in zip(xticklabels, fk_fd_colors):
    label.set_color(color)
ax.set_xticklabels(xticklabels, rotation=45, ha="right", fontsize=8)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)

# Legende für Farbcoding
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2196F3", label="Fachkompetenz (FK)"),
    Patch(facecolor="#FF5722", label="TechSkills / Fachdetails (FD)"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, frameon=True)

plt.tight_layout()
plt.savefig("plot7b_fk_fd_kombinierte_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot7b_fk_fd_kombinierte_heatmap.png")


# 7c: TechSkills vs. FK-Scores – Korrelation
print("\n[Plot 7c] TechSkills-Anteil vs. FK-Score – Boxplot-Vergleich...")

# Boxplot: FK-Score für Jobs MIT vs. OHNE TechSkills
df["TechSkill_Gruppe"] = df["hat_techskill"].map({1: "Mind. 1 TechSkill", 0: "Kein TechSkill"})

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Links: Boxplot FK-Score nach TechSkill-Präsenz
sns.boxplot(
    data=df, x="TechSkill_Gruppe", y="Fachkompetenz_Score",
    palette={"Mind. 1 TechSkill": "#FF5722", "Kein TechSkill": "#BDBDBD"},
    width=0.5, ax=axes[0],
)
sns.stripplot(
    data=df, x="TechSkill_Gruppe", y="Fachkompetenz_Score",
    color="black", alpha=0.1, size=2, jitter=True, ax=axes[0],
)
axes[0].set_title("Fachkompetenz-Score:\nJobs mit vs. ohne TechSkills", fontweight="bold")
axes[0].set_xlabel("")
axes[0].set_ylabel("Fachkompetenz-Score", fontweight="bold")

# Rechts: Anzahl TechSkills pro Job als Violin nach Profil
df["n_techskills"] = df[fd_cols].sum(axis=1)

sns.violinplot(
    data=df, x="profil_kurz", y="n_techskills",
    order=profil_order, palette=PROFIL_PALETTE,
    inner="box", cut=0, ax=axes[1],
)
axes[1].set_title("Anzahl genannter TechSkills pro Stelle\nnach Jobprofil", fontweight="bold")
axes[1].set_xlabel("")
axes[1].set_ylabel("Anzahl TechSkills", fontweight="bold")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=25, ha="right")

plt.tight_layout()
plt.savefig("plot7c_techskills_fk_vergleich.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot7c_techskills_fk_vergleich.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 5: MS TOOLS – Detailanalyse (BONUS)                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 5a] MS Tools – Gesamtranking...")

ms_freq = df_ms[ms_cols].mean() * 100
ms_freq.index = [clean_label(c, 3) for c in ms_cols]
ms_freq = ms_freq.sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(
    x=ms_freq.values, y=ms_freq.index,
    palette="Blues_d", edgecolor="white", linewidth=0.5, ax=ax,
)
for i, val in enumerate(ms_freq.values):
    ax.text(val + 0.3, i, f"{val:.1f}%", va="center", fontsize=10, fontweight="bold")

ax.set_title(
    "Microsoft Tools in Stelleninseraten: Nennungshäufigkeit\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Stelleninserate", fontweight="bold")
ax.set_ylabel("")
ax.set_xlim(0, max(ms_freq.values) * 1.3)
plt.tight_layout()
plt.savefig("plot5a_ms_tools_gesamt.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot5a_ms_tools_gesamt.png")


# 5b: MS-Tools Heatmap nach Profil
print("\n[Plot 5b] MS Tools – Heatmap nach Jobprofil...")
ms_heatmap = create_heatmap_data(df_ms, ms_cols)

fig, ax = plt.subplots(figsize=(18, 7))
sns.heatmap(
    ms_heatmap.reindex(profil_order).dropna(how="all"),
    annot=True, fmt=".1f", cmap="YlOrRd",
    vmin=0, linewidths=0.5, linecolor="white",
    cbar_kws={"label": "% der Inserate", "shrink": 0.8}, ax=ax,
)
ax.set_title(
    "Microsoft Tools nach Jobprofil: Nennungshäufigkeit (%)\n"
    f"(n = {n_jobs} Stelleninserate)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel(""); ax.set_ylabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
plt.tight_layout()
plt.savefig("plot5b_ms_tools_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot5b_ms_tools_heatmap.png")


# 5c: MS-Tools Grouped Barplot
print("\n[Plot 5c] MS Tools – Grouped Barplot nach Jobprofil...")

ms_long = df_ms.melt(
    id_vars=["profil_kurz"], value_vars=ms_cols,
    var_name="Tool", value_name="Vorhanden",
)
ms_long["Tool_Label"] = ms_long["Tool"].apply(lambda x: clean_label(x, 3))
ms_agg = ms_long.groupby(["profil_kurz", "Tool_Label"])["Vorhanden"].mean().reset_index()
ms_agg["Prozent"] = ms_agg["Vorhanden"] * 100

relevant_ms = ms_agg.groupby("Tool_Label")["Prozent"].mean()
relevant_ms = relevant_ms[relevant_ms > 1].index.tolist()
ms_filtered = ms_agg[ms_agg["Tool_Label"].isin(relevant_ms)]

ms_order = ms_filtered.groupby("Tool_Label")["Prozent"].mean().sort_values(ascending=True).index.tolist()

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=ms_filtered, y="Tool_Label", x="Prozent",
    hue="profil_kurz", order=ms_order, hue_order=profil_order,
    palette=PROFIL_PALETTE, edgecolor="white", linewidth=0.5, ax=ax,
)
ax.set_title(
    "Microsoft Tools nach Jobprofil (nur Tools > 1% Gesamthäufigkeit)\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Stelleninserate", fontweight="bold")
ax.set_ylabel("")
ax.legend(title="Jobprofil", title_fontsize=10,
          bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
plt.tight_layout()
plt.savefig("plot5c_ms_tools_nach_profil.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot5c_ms_tools_nach_profil.png")


# =============================================================================
# ZUSAMMENFASSUNG
# =============================================================================
print("\n" + "=" * 70)
print("ALLE PLOTS ERFOLGREICH ERSTELLT!")
print("=" * 70)
print(f"""
Profil-Zuordnung (n = {n_jobs}, alle Zeilen zugeordnet):""")
for profil, count in df["profil_kurz"].value_counts().items():
    print(f"  {profil:20s}  {count:4d}  ({count/n_jobs*100:.1f}%)")

print("""
Generierte Dateien:
  HAUPTKATEGORIEN:
    plot1_hauptkategorien_scores.png          Grouped Barplot: 4 Hauptkat. × 6 Profile
    plot2_unterkategorien_heatmaps.png        4 Heatmaps (FK, SK, MK, PK)
    plot3_unterkategorien_barplots.png        4 horizontale Barplots (Gesamtranking)
    plot4_fachkompetenz_nach_profil.png       Grouped Barplot nach Profil
    plot4_sozialkompetenz_nach_profil.png     Grouped Barplot nach Profil
    plot4_methodenkompetenz_nach_profil.png   Grouped Barplot nach Profil
    plot4_personalkompetenz_nach_profil.png   Grouped Barplot nach Profil

  TECHSKILLS (FD):
    plot6a_techskills_gesamt.png              Gesamtranking aller TechSkills
    plot6b_techskills_heatmap.png             TechSkills × Profil Heatmap
    plot6c_techskills_nach_profil.png         Grouped Barplot TechSkills nach Profil

  TECHSKILLS vs. FACHKOMPETENZ:
    plot7a_fk_vs_techskills_vergleich.png     FK-Unterkategorien vs. TechSkills
    plot7b_fk_fd_kombinierte_heatmap.png      FK + FD kombinierte Heatmap
    plot7c_techskills_fk_vergleich.png        Boxplot + Violin: FK-Score vs. TechSkills

  MS TOOLS (BONUS):
    plot5a_ms_tools_gesamt.png                Gesamtranking MS Tools
    plot5b_ms_tools_heatmap.png               MS Tools × Profil Heatmap
    plot5c_ms_tools_nach_profil.png           Grouped Barplot MS Tools nach Profil
""")
