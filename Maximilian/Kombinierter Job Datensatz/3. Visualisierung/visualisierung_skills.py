"""
===============================================================================
SKILL-ANALYSE FÜR BUSINESS INNOVATION STUDIERENDE
===============================================================================
Statistische Visualisierung der Kompetenz-Anforderungen in Stelleninseraten
Erstellt mit Seaborn für publikationsreife Grafiken.

Fragestellungen:
  1) Häufigkeit der 4 Hauptkategorien (Fach-, Sozial-, Methoden-, Personalkompetenz)
  2) Detailansicht der Unterkategorien innerhalb jeder Hauptkategorie
  3) BONUS: Detaillierte MS-Tools-Analyse (aus jobs_kategorisiert_ms_detail.csv)

Datenquelle: 1'194 Stelleninserate, 5 Jobprofile
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
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 2. SEABORN THEME-SETUP (Publikationsreif)
# =============================================================================
# Whitegrid gibt eine saubere Basis mit dezenten Hilfslinien
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
        "legend.fontsize": 10,
        "figure.titlesize": 16,
    }
)

# Professionelle Farbpalette für 5 Jobprofile
PROFIL_PALETTE = {
    "IT Manager": "#2196F3",                          # Blau
    "Business Developer": "#4CAF50",                   # Grün
    "Startup & Technology Entrepreneur": "#FF9800",    # Orange
    "Digital Channel & Relationship Manager": "#9C27B0",  # Lila
    "Supply Chain & Operations Manager": "#F44336",    # Rot
}

# Kurzbezeichnungen für Jobprofile (platzsparend in Plots)
PROFIL_SHORT = {
    "IT Manager": "IT Manager",
    "Business Developer": "Business Dev.",
    "Startup & Technology Entrepreneur": "Startup/Tech",
    "Digital Channel & Relationship Manager": "Digital Channel",
    "Supply Chain & Operations Manager": "Supply Chain",
}

# Farben für die 4 Hauptkategorien
HAUPT_PALETTE = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63"]

# =============================================================================
# 3. DATEN LADEN
# =============================================================================
print("Lade Daten...")
df_raw = pd.read_csv("jobs_kategorisiert.csv")
df_ms_raw = pd.read_csv("jobs_kategorisiert_ms_detail.csv")

n_jobs_total = len(df_raw)
print(f"  → {n_jobs_total} Stelleninserate geladen (gesamt)")

# Zeilen ohne Jobprofil entfernen (für die profilbezogene Analyse)
df = df_raw.dropna(subset=["job_profil"]).copy()
df_ms = df_ms_raw.dropna(subset=["job_profil"]).copy()
n_jobs = len(df)
n_dropped = n_jobs_total - n_jobs
print(f"  → {n_dropped} Inserate ohne Jobprofil entfernt")
print(f"  → {n_jobs} Inserate für Analyse (mit Jobprofil)")
print(f"  → {df['job_profil'].nunique()} Jobprofile: {', '.join(df['job_profil'].unique())}")

# Kurzbezeichnungen für Plot-Labels
df["profil_kurz"] = df["job_profil"].map(PROFIL_SHORT)
df_ms["profil_kurz"] = df_ms["job_profil"].map(PROFIL_SHORT)

# =============================================================================
# 4. SPALTENDEFINITIONEN
# =============================================================================
# Hauptkategorien (Score-Spalten, aggregiert)
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

# MS-Tools (binäre 0/1 Spalten, ohne den Score)
ms_cols = [c for c in df_ms.columns if c.startswith("MS_") and c != "MS_Tools_Score"]

# Schöne Label-Namen für Unterkategorien (Prefix entfernen, Underscores → Spaces)
def clean_label(col, prefix_len=3):
    """Entfernt den Prefix (FK_, SK_ etc.) und ersetzt Underscores."""
    return col[prefix_len:].replace("_", " ")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 1: HAUPTKATEGORIEN – Durchschnittliche Scores nach Jobprofil      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 1] Hauptkategorien – Grouped Barplot...")

# Daten in Long-Format für Seaborn transformieren
df_haupt_long = df.melt(
    id_vars=["job_profil", "profil_kurz"],
    value_vars=haupt_scores,
    var_name="Kategorie",
    value_name="Score",
)

# Schöne Kategorie-Labels
kategorie_labels = {
    "Fachkompetenz_Score": "Fachkompetenz",
    "Sozialkompetenz_Score": "Sozialkompetenz",
    "Methodenkompetenz_Score": "Methodenkompetenz",
    "Personalkompetenz_Score": "Personalkompetenz",
}
df_haupt_long["Kategorie"] = df_haupt_long["Kategorie"].map(kategorie_labels)

# --- Figure erstellen ---
fig, ax = plt.subplots(figsize=(14, 7))

sns.barplot(
    data=df_haupt_long,
    x="Kategorie",
    y="Score",
    hue="profil_kurz",
    palette=list(PROFIL_PALETTE.values()),
    ci=95,                  # 95%-Konfidenzintervall (schwarze Fehlerbalken)
    edgecolor="white",
    linewidth=0.8,
    ax=ax,
)

# Styling
ax.set_title(
    "Durchschnittliche Kompetenz-Scores nach Jobprofil\n"
    f"(n = {n_jobs} Stelleninserate, Fehlerbalken = 95%-KI)",
    fontweight="bold", pad=15,
)
ax.set_xlabel("")
ax.set_ylabel("Durchschnittlicher Score", fontweight="bold")
ax.legend(
    title="Jobprofil", title_fontsize=11,
    bbox_to_anchor=(1.02, 1), loc="upper left",
    frameon=True, edgecolor="gray",
)
ax.set_ylim(0, ax.get_ylim()[1] * 1.1)

# Dezente Baseline
ax.axhline(y=0, color="gray", linewidth=0.5)

plt.tight_layout()
plt.savefig("plot1_hauptkategorien_scores.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot1_hauptkategorien_scores.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 2: UNTERKATEGORIEN – Heatmaps der Nennungshäufigkeit              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 2] Unterkategorien – 4 Heatmaps...")

def create_heatmap_data(df, cols, prefix_len=3):
    """
    Berechnet die prozentuale Nennungshäufigkeit jeder Unterkategorie
    pro Jobprofil. Ergebnis: DataFrame (Profil × Skill).
    """
    grouped = df.groupby("profil_kurz")[cols].mean() * 100  # in Prozent
    grouped.columns = [clean_label(c, prefix_len) for c in cols]
    # Sortiere nach Gesamthäufigkeit (häufigste oben/links)
    order = grouped.mean().sort_values(ascending=False).index
    return grouped[order]

fk_heatmap = create_heatmap_data(df, fk_cols)
sk_heatmap = create_heatmap_data(df, sk_cols)
mk_heatmap = create_heatmap_data(df, mk_cols)
pk_heatmap = create_heatmap_data(df, pk_cols)

# Profil-Reihenfolge konsistent (nach Gesamtzahl Jobs)
profil_order = list(PROFIL_SHORT.values())

fig, axes = plt.subplots(2, 2, figsize=(22, 16))
fig.suptitle(
    "Nennungshäufigkeit der Skill-Unterkategorien nach Jobprofil\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in % der Inserate)",
    fontsize=16, fontweight="bold", y=0.98,
)

heatmap_data = [
    (fk_heatmap, "Fachkompetenz", "Blues"),
    (sk_heatmap, "Sozialkompetenz", "Greens"),
    (mk_heatmap, "Methodenkompetenz", "Oranges"),
    (pk_heatmap, "Personalkompetenz", "RdPu"),
]

for idx, (data, title, cmap) in enumerate(heatmap_data):
    ax = axes[idx // 2, idx % 2]

    # Stelle sicher, dass alle Profile vorhanden und geordnet sind
    data_sorted = data.reindex(profil_order).dropna(how="all")

    sns.heatmap(
        data_sorted,
        annot=True,           # Prozentwerte in Zellen anzeigen
        fmt=".0f",            # Ganzzahlig (%)
        cmap=cmap,
        vmin=0,
        vmax=100,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "% der Inserate", "shrink": 0.8},
        ax=ax,
    )
    ax.set_title(f"{title}", fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=9)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot2_unterkategorien_heatmaps.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot2_unterkategorien_heatmaps.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 3: UNTERKATEGORIEN – Horizontale Barplots (Top Skills gesamt)     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 3] Top Skills – Horizontale Barplots je Hauptkategorie...")

def create_horizontal_barplot(df, cols, prefix_len, title, color, ax):
    """
    Erstellt einen horizontalen Barplot der Unterkategorien,
    sortiert nach Häufigkeit, mit Prozentwerten als Annotation.
    """
    # Berechne Gesamthäufigkeit (über alle Jobprofile)
    freq = df[cols].mean() * 100
    freq.index = [clean_label(c, prefix_len) for c in cols]
    freq = freq.sort_values(ascending=True)  # ascending für horizontale Darstellung

    sns.barplot(
        x=freq.values,
        y=freq.index,
        color=color,
        edgecolor="white",
        linewidth=0.5,
        ax=ax,
    )

    # Prozentwerte neben den Balken
    for i, (val, name) in enumerate(zip(freq.values, freq.index)):
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

barplot_specs = [
    (fk_cols, 3, "Fachkompetenz", "#2196F3", axes[0, 0]),
    (sk_cols, 3, "Sozialkompetenz", "#4CAF50", axes[0, 1]),
    (mk_cols, 3, "Methodenkompetenz", "#FF9800", axes[1, 0]),
    (pk_cols, 3, "Personalkompetenz", "#E91E63", axes[1, 1]),
]

for cols, prefix_len, title, color, ax in barplot_specs:
    create_horizontal_barplot(df, cols, prefix_len, title, color, ax)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("plot3_unterkategorien_barplots.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot3_unterkategorien_barplots.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 4: UNTERKATEGORIEN – Grouped Barplot nach Jobprofil (Faceted)     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 4] Unterkategorien – Faceted Barplot nach Jobprofil...")

# Für jede Hauptkategorie: Lange Darstellung aller Unterkategorien nach Profil
all_sub_cols = fk_cols + sk_cols + mk_cols + pk_cols

# Mapping: Unterkategorie → Hauptkategorie
sub_to_haupt = {}
for c in fk_cols: sub_to_haupt[c] = "Fachkompetenz"
for c in sk_cols: sub_to_haupt[c] = "Sozialkompetenz"
for c in mk_cols: sub_to_haupt[c] = "Methodenkompetenz"
for c in pk_cols: sub_to_haupt[c] = "Personalkompetenz"

# Long-Format erstellen
df_sub_long = df.melt(
    id_vars=["job_profil", "profil_kurz"],
    value_vars=all_sub_cols,
    var_name="Skill",
    value_name="Vorhanden",
)
df_sub_long["Hauptkategorie"] = df_sub_long["Skill"].map(sub_to_haupt)
df_sub_long["Skill_Label"] = df_sub_long["Skill"].apply(
    lambda x: clean_label(x, 3)
)

# Aggregiere: % pro Skill pro Profil
df_sub_agg = (
    df_sub_long
    .groupby(["profil_kurz", "Hauptkategorie", "Skill_Label"])["Vorhanden"]
    .mean()
    .reset_index()
)
df_sub_agg["Prozent"] = df_sub_agg["Vorhanden"] * 100

# Erstelle 4 separate Plots (einen pro Hauptkategorie) mit FacetGrid-Logik
for haupt, color in zip(
    ["Fachkompetenz", "Sozialkompetenz", "Methodenkompetenz", "Personalkompetenz"],
    ["#2196F3", "#4CAF50", "#FF9800", "#E91E63"],
):
    subset = df_sub_agg[df_sub_agg["Hauptkategorie"] == haupt].copy()

    # Sortiere Skills nach Gesamthäufigkeit
    skill_order = (
        subset.groupby("Skill_Label")["Prozent"]
        .mean()
        .sort_values(ascending=True)
        .index.tolist()
    )

    fig, ax = plt.subplots(figsize=(14, max(6, len(skill_order) * 0.6 + 2)))

    sns.barplot(
        data=subset,
        y="Skill_Label",
        x="Prozent",
        hue="profil_kurz",
        order=skill_order,
        palette=list(PROFIL_PALETTE.values()),
        edgecolor="white",
        linewidth=0.5,
        ax=ax,
    )

    ax.set_title(
        f"{haupt}: Anforderungshäufigkeit nach Jobprofil\n"
        f"(n = {n_jobs} Stelleninserate · Angaben in %)",
        fontsize=14, fontweight="bold", pad=12,
    )
    ax.set_xlabel("% der Stelleninserate", fontweight="bold")
    ax.set_ylabel("")
    ax.set_xlim(0, 105)
    ax.legend(
        title="Jobprofil", title_fontsize=10,
        bbox_to_anchor=(1.02, 1), loc="upper left",
        frameon=True, edgecolor="gray",
    )

    plt.tight_layout()
    fname = f"plot4_{haupt.lower()}_nach_profil.png"
    plt.savefig(fname, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Gespeichert: {fname}")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 5 (BONUS): MS TOOLS – Detailanalyse                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 5] BONUS – MS Tools Detailanalyse...")

# --- 5a: Gesamthäufigkeit aller MS-Tools ---
ms_freq = df_ms[ms_cols].mean() * 100
ms_freq.index = [clean_label(c, 3) for c in ms_cols]
ms_freq = ms_freq.sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))

bars = sns.barplot(
    x=ms_freq.values,
    y=ms_freq.index,
    palette="Blues_d",
    edgecolor="white",
    linewidth=0.5,
    ax=ax,
)

# Prozentwerte annotieren
for i, (val, name) in enumerate(zip(ms_freq.values, ms_freq.index)):
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

# --- 5b: MS-Tools nach Jobprofil (Heatmap) ---
ms_heatmap = create_heatmap_data(df_ms, ms_cols)

fig, ax = plt.subplots(figsize=(16, 6))

sns.heatmap(
    ms_heatmap.reindex(profil_order).dropna(how="all"),
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    vmin=0,
    linewidths=0.5,
    linecolor="white",
    cbar_kws={"label": "% der Inserate", "shrink": 0.8},
    ax=ax,
)

ax.set_title(
    "Microsoft Tools nach Jobprofil: Nennungshäufigkeit (%)\n"
    f"(n = {n_jobs} Stelleninserate)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)

plt.tight_layout()
plt.savefig("plot5b_ms_tools_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Gespeichert: plot5b_ms_tools_heatmap.png")


# --- 5c: Top MS-Tools nach Jobprofil (Grouped Barplot, nur Tools > 1%) ---
ms_long = df_ms.melt(
    id_vars=["job_profil", "profil_kurz"],
    value_vars=ms_cols,
    var_name="Tool",
    value_name="Vorhanden",
)
ms_long["Tool_Label"] = ms_long["Tool"].apply(lambda x: clean_label(x, 3))

ms_agg = (
    ms_long
    .groupby(["profil_kurz", "Tool_Label"])["Vorhanden"]
    .mean()
    .reset_index()
)
ms_agg["Prozent"] = ms_agg["Vorhanden"] * 100

# Nur Tools mit >1% Gesamthäufigkeit (sonst wird der Plot zu unübersichtlich)
relevant_tools = ms_agg.groupby("Tool_Label")["Prozent"].mean()
relevant_tools = relevant_tools[relevant_tools > 1].index.tolist()
ms_agg_filtered = ms_agg[ms_agg["Tool_Label"].isin(relevant_tools)]

tool_order = (
    ms_agg_filtered.groupby("Tool_Label")["Prozent"]
    .mean()
    .sort_values(ascending=True)
    .index.tolist()
)

fig, ax = plt.subplots(figsize=(14, 8))

sns.barplot(
    data=ms_agg_filtered,
    y="Tool_Label",
    x="Prozent",
    hue="profil_kurz",
    order=tool_order,
    palette=list(PROFIL_PALETTE.values()),
    edgecolor="white",
    linewidth=0.5,
    ax=ax,
)

ax.set_title(
    "Microsoft Tools nach Jobprofil (nur Tools > 1% Gesamthäufigkeit)\n"
    f"(n = {n_jobs} Stelleninserate · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Stelleninserate", fontweight="bold")
ax.set_ylabel("")
ax.legend(
    title="Jobprofil", title_fontsize=10,
    bbox_to_anchor=(1.02, 1), loc="upper left",
    frameon=True, edgecolor="gray",
)

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
print("""
Generierte Dateien:
  1. plot1_hauptkategorien_scores.png
     → Grouped Barplot: Durchschnittliche Kompetenz-Scores pro Jobprofil
     → Zeigt, welche Kompetenzkategorie wo am stärksten gefragt ist

  2. plot2_unterkategorien_heatmaps.png
     → 4 Heatmaps (eine pro Hauptkategorie): Nennungshäufigkeit in %
     → Schneller Überblick über alle 40 Einzelskills × 5 Jobprofile

  3. plot3_unterkategorien_barplots.png
     → 4 horizontale Barplots: Gesamthäufigkeit jedes Skills
     → Zeigt die wichtigsten Skills pro Hauptkategorie

  4. plot4_fachkompetenz_nach_profil.png
     plot4_sozialkompetenz_nach_profil.png
     plot4_methodenkompetenz_nach_profil.png
     plot4_personalkompetenz_nach_profil.png
     → Grouped Barplots: Jede Unterkategorie aufgeschlüsselt nach Profil
     → Detaillierter Profilvergleich

  5. plot5a_ms_tools_gesamt.png
     → Gesamthäufigkeit aller Microsoft Tools
  5b. plot5b_ms_tools_heatmap.png
     → MS-Tools × Jobprofil als Heatmap
  5c. plot5c_ms_tools_nach_profil.png
     → Grouped Barplot: MS-Tools nach Jobprofil (nur relevante Tools)
""")

# Aufräumen der temporären Hilfsdatei
import os
if os.path.exists("analyse_daten.py"):
    os.remove("analyse_daten.py")
