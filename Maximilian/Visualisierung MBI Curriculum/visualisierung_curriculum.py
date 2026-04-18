"""
===============================================================================
SKILL-ANALYSE DES MBI CURRICULUMS
===============================================================================
Gleiche Visualisierungen wie für jobs_kategorisiert, angewandt auf die
kategorisierten Kursinhalte des MBI-Studiengangs.

Plots:
  1)  Hauptkategorien – Durchschnittliche Scores nach Profil
  2)  Unterkategorien – 4 Heatmaps (FK, SK, MK, PK)
  3)  Unterkategorien – Horizontale Barplots (Gesamtranking)
  4a-d) Unterkategorien – Grouped Barplot nach Profil
  6a) TechSkills – Gesamtranking
  6b) TechSkills – Heatmap nach Profil
  6c) TechSkills – Grouped Barplot nach Profil
  7a) FK vs. TechSkills – Kombinierter Barplot
  7b) FK + FD – Kombinierte Heatmap nach Profil
  7c) TechSkills vs. FK – Boxplot + Violin

Datenquelle: 84 MBI-Kurse, kategorisiert mit dem Kompetenz-Framework (VL4)
Output:       plots_curriculum/
===============================================================================
"""

# =============================================================================
# 1. IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os
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
# 3. OUTPUT-ORDNER
# =============================================================================
OUT_DIR = "plots_curriculum"
os.makedirs(OUT_DIR, exist_ok=True)

def save_plot(filename):
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Gespeichert: {path}")

# =============================================================================
# 4. DATEN LADEN
# =============================================================================
print("Lade Daten...")
df = pd.read_csv("mbi_curriculum_kategorisiert.csv", sep=";")
n_kurse = len(df)
print(f"  → {n_kurse} Kurse geladen")

# =============================================================================
# 5. PROFIL-DEFINITIONEN
# =============================================================================
PROFIL_COLS = {
    "Business Development":        "Business Dev.",
    "Digital Channel & CRM":       "Digital Channel",
    "Startup & Scale-up":          "Startup/Scale-up",
    "Supply Chain & Operations":   "Supply Chain",
    "Technology Architecture":     "Tech Architect",
    "Digital Transformation":      "Digital Business",
}

PROFIL_PALETTE = {
    "Business Dev.":     "#4CAF50",
    "Digital Channel":   "#9C27B0",
    "Startup/Scale-up":  "#FF9800",
    "Supply Chain":      "#F44336",
    "Tech Architect":    "#2196F3",
    "Digital Business":  "#607D8B",
}

# Profil-Verteilung ausgeben
print(f"\n  Profil-Zuordnung (Kurse können mehreren Profilen zugehören):")
for full_name, short_name in PROFIL_COLS.items():
    count = int(df[full_name].sum())
    print(f"    {short_name:20s}  {count:3d} Kurse  ({count/n_kurse*100:.0f}%)")

# =============================================================================
# 6. HILFSFUNKTIONEN
# =============================================================================

# Profil-Long-Format: Ein Kurs pro Profil-Zugehörigkeit (für Profilvergleiche)
def build_profil_long(df_in, value_cols):
    """
    Erzeugt ein Long-Format-DataFrame: für jedes Profil, dem ein Kurs
    zugeordnet ist, wird eine Zeile erstellt.
    """
    rows = []
    for _, row in df_in.iterrows():
        for full_name, short_name in PROFIL_COLS.items():
            if row.get(full_name, 0) == 1:
                entry = {"profil_kurz": short_name}
                for c in value_cols:
                    entry[c] = row[c]
                rows.append(entry)
    return pd.DataFrame(rows)


# Spaltendefinitionen
haupt_scores = [
    "Fachkompetenz_Score",
    "Sozialkompetenz_Score",
    "Methodenkompetenz_Score",
    "Personalkompetenz_Score",
]

fk_cols = [c for c in df.columns if c.startswith("FK_")]
sk_cols = [c for c in df.columns if c.startswith("SK_")]
mk_cols = [c for c in df.columns if c.startswith("MK_")]
pk_cols = [c for c in df.columns if c.startswith("PK_")]
fd_cols = [c for c in df.columns if c.startswith("FD_")]

all_skill_cols = fk_cols + sk_cols + mk_cols + pk_cols + fd_cols

# Long-Format für Profil-Analysen
df_profil = build_profil_long(df, haupt_scores + all_skill_cols)

# Profil-Reihenfolge nach Häufigkeit
profil_order = (
    df_profil["profil_kurz"]
    .value_counts()
    .index.tolist()
)
print(f"\n  Profil-Reihenfolge (nach Häufigkeit): {profil_order}")


def clean_label(col, prefix_len=3):
    return col[prefix_len:].replace("_", " ")


def create_heatmap_data(df_in, cols, prefix_len=3):
    """Berechnet % Nennungshäufigkeit pro Profil."""
    grouped = df_in.groupby("profil_kurz")[cols].mean() * 100
    grouped.columns = [clean_label(c, prefix_len) for c in cols]
    order = grouped.mean().sort_values(ascending=False).index
    return grouped[order]


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 1: HAUPTKATEGORIEN – Durchschnittliche Scores nach Profil         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 1] Hauptkategorien – Grouped Barplot...")

df_haupt_long = df_profil.melt(
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
    "MBI Curriculum: Durchschnittliche Kompetenz-Scores nach Profil\n"
    f"(n = {n_kurse} Kurse, Fehlerbalken = 95%-KI)",
    fontweight="bold", pad=15,
)
ax.set_xlabel("")
ax.set_ylabel("Durchschnittlicher Score", fontweight="bold")
ax.legend(title="MBI-Profil", title_fontsize=10,
          bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
ax.set_ylim(0, ax.get_ylim()[1] * 1.1)
plt.tight_layout()
save_plot("plot1_hauptkategorien_scores.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 2: UNTERKATEGORIEN – 4 Heatmaps                                   ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 2] Unterkategorien – 4 Heatmaps...")

fk_heatmap = create_heatmap_data(df_profil, fk_cols)
sk_heatmap = create_heatmap_data(df_profil, sk_cols)
mk_heatmap = create_heatmap_data(df_profil, mk_cols)
pk_heatmap = create_heatmap_data(df_profil, pk_cols)

fig, axes = plt.subplots(2, 2, figsize=(24, 18))
fig.suptitle(
    "MBI Curriculum: Abdeckung der Skill-Unterkategorien nach Profil\n"
    f"(n = {n_kurse} Kurse · Angaben in % der Kurse)",
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
        cbar_kws={"label": "% der Kurse", "shrink": 0.8}, ax=ax,
    )
    ax.set_title(f"{title}", fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel(""); ax.set_ylabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=9)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])
save_plot("plot2_unterkategorien_heatmaps.png")


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
    ax.set_xlabel("% der Kurse")
    ax.set_ylabel("")
    ax.set_xlim(0, 105)

fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle(
    "MBI Curriculum: Häufigkeit der Skill-Abdeckung nach Hauptkategorie\n"
    f"(n = {n_kurse} Kurse · Anteil in %)",
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
save_plot("plot3_unterkategorien_barplots.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 4: UNTERKATEGORIEN – Grouped Barplot nach Profil (4 Plots)        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 4] Unterkategorien – Grouped Barplot nach Profil...")

all_sub_cols = fk_cols + sk_cols + mk_cols + pk_cols
sub_to_haupt = {}
for c in fk_cols: sub_to_haupt[c] = "Fachkompetenz"
for c in sk_cols: sub_to_haupt[c] = "Sozialkompetenz"
for c in mk_cols: sub_to_haupt[c] = "Methodenkompetenz"
for c in pk_cols: sub_to_haupt[c] = "Personalkompetenz"

df_sub_long = df_profil.melt(
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
        f"MBI Curriculum – {haupt}: Abdeckung nach Profil\n"
        f"(n = {n_kurse} Kurse · Angaben in %)",
        fontsize=14, fontweight="bold", pad=12,
    )
    ax.set_xlabel("% der Kurse", fontweight="bold")
    ax.set_ylabel("")
    ax.set_xlim(0, 105)
    ax.legend(title="MBI-Profil", title_fontsize=10,
              bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
    plt.tight_layout()
    save_plot(f"plot4_{haupt.lower()}_nach_profil.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 6a: TECHSKILLS (FD_) – Gesamtranking                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 6a] TechSkills – Gesamtranking...")

fd_freq = df[fd_cols].mean() * 100
fd_freq.index = [clean_label(c, 3) for c in fd_cols]
fd_freq = fd_freq.sort_values(ascending=True)

# Nur Skills mit >0% anzeigen
fd_freq_nonzero = fd_freq[fd_freq > 0]

fig, ax = plt.subplots(figsize=(14, max(8, len(fd_freq_nonzero) * 0.38 + 2)))
colors = sns.color_palette("viridis", n_colors=len(fd_freq_nonzero))
sns.barplot(
    x=fd_freq_nonzero.values, y=fd_freq_nonzero.index,
    palette=colors, edgecolor="white", linewidth=0.5, ax=ax,
)
for i, val in enumerate(fd_freq_nonzero.values):
    ax.text(val + 0.3, i, f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")

ax.set_title(
    "MBI Curriculum: TechSkills (Fachdetail-Kompetenzen) – Abdeckung\n"
    f"(n = {n_kurse} Kurse · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Kurse", fontweight="bold")
ax.set_ylabel("")
ax.set_xlim(0, max(fd_freq_nonzero.values) * 1.25)
plt.tight_layout()
save_plot("plot6a_techskills_gesamt.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 6b: TECHSKILLS – Heatmap nach Profil                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 6b] TechSkills – Heatmap nach Profil...")

fd_heatmap = create_heatmap_data(df_profil, fd_cols)

fig, ax = plt.subplots(figsize=(22, 8))
sns.heatmap(
    fd_heatmap.reindex(profil_order).dropna(how="all"),
    annot=True, fmt=".1f", cmap="YlGnBu",
    vmin=0, linewidths=0.5, linecolor="white",
    cbar_kws={"label": "% der Kurse", "shrink": 0.8}, ax=ax,
)
ax.set_title(
    "MBI Curriculum: TechSkills nach Profil – Abdeckung (%)\n"
    f"(n = {n_kurse} Kurse)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel(""); ax.set_ylabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=9)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
plt.tight_layout()
save_plot("plot6b_techskills_heatmap.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 6c: TECHSKILLS – Grouped Barplot nach Profil                      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 6c] TechSkills – Grouped Barplot nach Profil...")

df_fd_long = df_profil.melt(
    id_vars=["profil_kurz"], value_vars=fd_cols,
    var_name="Skill", value_name="Vorhanden",
)
df_fd_long["Skill_Label"] = df_fd_long["Skill"].apply(lambda x: clean_label(x, 3))

df_fd_agg = (
    df_fd_long.groupby(["profil_kurz", "Skill_Label"])["Vorhanden"]
    .mean().reset_index()
)
df_fd_agg["Prozent"] = df_fd_agg["Vorhanden"] * 100

# Nur TechSkills mit >0% Gesamthäufigkeit
relevant_fd = df_fd_agg.groupby("Skill_Label")["Prozent"].mean()
relevant_fd = relevant_fd[relevant_fd > 0].index.tolist()
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
    "MBI Curriculum: TechSkills nach Profil (nur Skills mit Abdeckung > 0%)\n"
    f"(n = {n_kurse} Kurse · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Kurse", fontweight="bold")
ax.set_ylabel("")
ax.legend(title="MBI-Profil", title_fontsize=10,
          bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, edgecolor="gray")
plt.tight_layout()
save_plot("plot6c_techskills_nach_profil.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 7a: FK vs. TECHSKILLS – Kombinierter Barplot                      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 7a] FK vs. FD – Kombinierter Barplot...")

df["hat_techskill"] = (df[fd_cols].sum(axis=1) > 0).astype(int)

fk_plus_tech = fk_cols + ["hat_techskill"]
fk_plus_freq = df[fk_plus_tech].mean() * 100

labels = [clean_label(c, 3) for c in fk_cols] + ["Mind. 1 TechSkill"]
fk_plus_freq.index = labels
fk_plus_freq = fk_plus_freq.sort_values(ascending=True)

bar_colors = ["#2196F3" if lab != "Mind. 1 TechSkill" else "#FF5722" for lab in fk_plus_freq.index]

fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(
    x=fk_plus_freq.values, y=fk_plus_freq.index,
    palette=bar_colors, edgecolor="white", linewidth=0.5, ax=ax,
)
for i, val in enumerate(fk_plus_freq.values):
    ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")

ax.set_title(
    "MBI Curriculum: Fachkompetenz vs. TechSkills (Fachdetails)\n"
    f"(n = {n_kurse} · Rot = mind. 1 TechSkill · Blau = FK-Unterkategorien)",
    fontsize=13, fontweight="bold", pad=12,
)
ax.set_xlabel("% der Kurse", fontweight="bold")
ax.set_ylabel("")
ax.set_xlim(0, 105)
plt.tight_layout()
save_plot("plot7a_fk_vs_techskills_vergleich.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 7b: FK + FD – Kombinierte Heatmap nach Profil                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 7b] FK + FD – Kombinierte Heatmap nach Profil...")

fk_fd_cols = fk_cols + fd_cols
fk_fd_heatmap = create_heatmap_data(df_profil, fk_fd_cols)

fk_fd_colors = []
for orig_col in fk_fd_heatmap.columns:
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
    cbar_kws={"label": "% der Kurse", "shrink": 0.8}, ax=ax,
)
ax.set_title(
    "MBI Curriculum: Fachkompetenz (FK) + TechSkills (FD) kombiniert nach Profil\n"
    f"(n = {n_kurse} · Angaben in %)",
    fontsize=14, fontweight="bold", pad=12,
)
ax.set_xlabel(""); ax.set_ylabel("")
xticklabels = ax.get_xticklabels()
for label, color in zip(xticklabels, fk_fd_colors):
    label.set_color(color)
ax.set_xticklabels(xticklabels, rotation=45, ha="right", fontsize=8)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)

legend_elements = [
    Patch(facecolor="#2196F3", label="Fachkompetenz (FK)"),
    Patch(facecolor="#FF5722", label="TechSkills / Fachdetails (FD)"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, frameon=True)

plt.tight_layout()
save_plot("plot7b_fk_fd_kombinierte_heatmap.png")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  PLOT 7c: TECHSKILLS vs. FK – Boxplot + Violin                          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
print("\n[Plot 7c] TechSkills vs. FK – Boxplot + Violin...")

df["TechSkill_Gruppe"] = df["hat_techskill"].map({1: "Mind. 1 TechSkill", 0: "Kein TechSkill"})
df["n_techskills"] = df[fd_cols].sum(axis=1)

# Profil-Long für Violin
df_violin = build_profil_long(df, ["n_techskills"])

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Links: Boxplot FK-Score nach TechSkill-Präsenz
sns.boxplot(
    data=df, x="TechSkill_Gruppe", y="Fachkompetenz_Score",
    palette={"Mind. 1 TechSkill": "#FF5722", "Kein TechSkill": "#BDBDBD"},
    width=0.5, ax=axes[0],
)
sns.stripplot(
    data=df, x="TechSkill_Gruppe", y="Fachkompetenz_Score",
    color="black", alpha=0.15, size=4, jitter=True, ax=axes[0],
)
axes[0].set_title("Fachkompetenz-Score:\nKurse mit vs. ohne TechSkills", fontweight="bold")
axes[0].set_xlabel("")
axes[0].set_ylabel("Fachkompetenz-Score", fontweight="bold")

# Rechts: Violin Anzahl TechSkills pro Kurs nach Profil
sns.violinplot(
    data=df_violin, x="profil_kurz", y="n_techskills",
    order=profil_order, palette=PROFIL_PALETTE,
    inner="box", cut=0, ax=axes[1],
)
axes[1].set_title("Anzahl abgedeckter TechSkills pro Kurs\nnach MBI-Profil", fontweight="bold")
axes[1].set_xlabel("")
axes[1].set_ylabel("Anzahl TechSkills", fontweight="bold")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=25, ha="right")

plt.tight_layout()
save_plot("plot7c_techskills_fk_vergleich.png")


# =============================================================================
# ZUSAMMENFASSUNG
# =============================================================================
print("\n" + "=" * 70)
print("ALLE PLOTS ERFOLGREICH ERSTELLT!")
print("=" * 70)
print(f"""
Datenquelle: {n_kurse} MBI-Kurse (mbi_curriculum_kategorisiert.csv)

Generierte Dateien in '{OUT_DIR}/':
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
""")
