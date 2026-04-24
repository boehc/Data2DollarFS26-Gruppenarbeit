"""
===============================================================================
INTERAKTIVE MBI CAREER EXPLORER v3 – Premium UI Redesign
===============================================================================
Design-Prinzipien angewandt:
  - Refactoring UI: Hierarchy via weight/color, fewer borders, offset shadows,
    accent borders, generous whitespace, 8px spacing grid
  - Nielsen Heuristics: System status visibility, consistency, aesthetic
    minimalism, recognition over recall
  - Laws of UX: Chunking, Proximity, Common Region, Aesthetic-Usability Effect
  - Inter font via Google Fonts for premium typography
  - Smooth micro-interactions und animations
  - Card-based layout statt roher Tabellen

Datenquellen:
  - jobs_final.csv
  - mbi_curriculum_kategorisiert.csv

Output:
  - interactive_explorer/index.html
  - interactive_explorer/profil_*.html
===============================================================================
"""

import pandas as pd
import plotly.graph_objects as go
import os
import re
import html as html_lib
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. KONFIGURATION
# =============================================================================
OUT_DIR = "interactive_explorer"
os.makedirs(OUT_DIR, exist_ok=True)

# Refined, more sophisticated color palette (HSL-tuned for harmony)
PROFIL_COLORS = {
    "Business Development":                    "#059669",   # emerald-600
    "Digital Channel & CRM":                   "#7c3aed",   # violet-600
    "Start-up & Scale-up Entrepreneurship":    "#d97706",   # amber-600
    "Supply Chain & Operations Management":    "#dc2626",   # red-600
    "Technology Solution Architect":           "#2563eb",   # blue-600
    "Transforming & Managing Digital Business": "#475569",   # slate-600
}

# Lighter tint for backgrounds
PROFIL_BG = {
    "Business Development":                    "#ecfdf5",
    "Digital Channel & CRM":                   "#f5f3ff",
    "Start-up & Scale-up Entrepreneurship":    "#fffbeb",
    "Supply Chain & Operations Management":    "#fef2f2",
    "Technology Solution Architect":           "#eff6ff",
    "Transforming & Managing Digital Business": "#f8fafc",
}

PROFIL_SHORT = {
    "Business Development":                   "Business Dev.",
    "Digital Channel & CRM":                  "Digital Channel",
    "Start-up & Scale-up Entrepreneurship":   "Startup & Scale-up",
    "Supply Chain & Operations Management":   "Supply Chain",
    "Technology Solution Architect":          "Tech Architect",
    "Transforming & Managing Digital Business": "Digital Business",
}

PROFIL_ICONS = {
    "Business Development":                   "📈",
    "Digital Channel & CRM":                  "📱",
    "Start-up & Scale-up Entrepreneurship":   "🚀",
    "Supply Chain & Operations Management":   "🔗",
    "Technology Solution Architect":          "🏗️",
    "Transforming & Managing Digital Business": "🔄",
}

# Skill category styling
CAT_META = {
    "Fachkompetenz":     {"icon": "🎓", "color": "#2563eb", "bg": "#eff6ff", "border": "#bfdbfe"},
    "TechSkill":         {"icon": "💻", "color": "#c2410c", "bg": "#fff7ed", "border": "#fed7aa"},
    "Sozialkompetenz":   {"icon": "🤝", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0"},
    "Methodenkompetenz": {"icon": "📋", "color": "#d97706", "bg": "#fffbeb", "border": "#fde68a"},
    "Personalkompetenz": {"icon": "💡", "color": "#db2777", "bg": "#fdf2f8", "border": "#fbcfe8"},
}

CAT_ORDER = ["Fachkompetenz", "TechSkill", "Sozialkompetenz", "Methodenkompetenz", "Personalkompetenz"]


def clean_skill(col):
    name = col.split("_", 1)[1] if "_" in col else col
    return name.replace("_", " ")


def safe_filename(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def categorize_skill(col):
    if col.startswith("FK_"): return "Fachkompetenz"
    if col.startswith("FD_"): return "TechSkill"
    if col.startswith("SK_"): return "Sozialkompetenz"
    if col.startswith("MK_"): return "Methodenkompetenz"
    if col.startswith("PK_"): return "Personalkompetenz"
    return "Andere"


# =============================================================================
# 2. DATEN LADEN
# =============================================================================
print("Lade Daten...")
df_jobs = pd.read_csv("jobs_final.csv")
df_curr = pd.read_csv("mbi_curriculum_kategorisiert.csv", sep=";")

skill_cols = [c for c in df_jobs.columns
              if c.startswith(("FK_", "FD_", "SK_", "MK_", "PK_"))
              and c != "FD_Berufserfahrung_Jahre"]
curr_skill_cols = [c for c in skill_cols if c in df_curr.columns]

print(f"  Jobs: {len(df_jobs)}, Kurse: {len(df_curr)}, Skills: {len(skill_cols)}")

# =============================================================================
# 3. KURS-EMPFEHLUNGS-ENGINE
# =============================================================================
def get_job_skills(job_row):
    return [c for c in skill_cols if job_row.get(c, 0) == 1]


def get_matching_courses(required_skills, max_courses=5):
    if not required_skills:
        return []
    course_scores = []
    for _, course in df_curr.iterrows():
        covered = [s for s in required_skills
                   if s in curr_skill_cols and course.get(s, 0) == 1]
        if covered:
            course_scores.append((course["course_title"], covered, len(covered)))
    course_scores.sort(key=lambda x: -x[2])
    return course_scores[:max_courses]


def get_skill_gaps(required_skills, recommended_courses, max_gaps=3):
    covered_by_courses = set()
    for _, covered, _ in recommended_courses:
        covered_by_courses.update(covered)
    gaps = [s for s in required_skills if s not in covered_by_courses]
    return gaps[:max_gaps]


# =============================================================================
# 4. PRO JOB: DATEN VORBERECHNEN
# =============================================================================
print("Berechne Kurs-Empfehlungen für jeden Job...")

job_tooltips = {}
for idx, job in df_jobs.iterrows():
    skills = get_job_skills(job)
    courses = get_matching_courses(skills)
    gaps = get_skill_gaps(skills, courses)
    job_tooltips[idx] = {"skills": skills, "courses": courses, "gaps": gaps}

print(f"  ✓ {len(job_tooltips)} Jobs verarbeitet")


# =============================================================================
# 5. SHARED CSS (Design System)
# =============================================================================
SHARED_CSS = """
    /* ── Reset & Base ── */
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f8fafc;
        color: #1e293b;
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* ── Typography Scale ── */
    .t-xs  { font-size: 0.75rem; }   /* 12px */
    .t-sm  { font-size: 0.8125rem; } /* 13px */
    .t-base{ font-size: 0.875rem; }  /* 14px */
    .t-md  { font-size: 1rem; }      /* 16px */
    .t-lg  { font-size: 1.25rem; }   /* 20px */
    .t-xl  { font-size: 1.5rem; }    /* 24px */
    .t-2xl { font-size: 1.75rem; }   /* 28px */
    .t-3xl { font-size: 2.25rem; }   /* 36px */

    /* ── Spacing helpers (8px grid) ── */
    .gap-1  { gap: 0.25rem; }
    .gap-2  { gap: 0.5rem; }
    .gap-3  { gap: 0.75rem; }
    .gap-4  { gap: 1rem; }
    .gap-6  { gap: 1.5rem; }

    /* ── Card System ── */
    .card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        /* Refactoring UI: offset shadow instead of border */
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 24px rgba(0,0,0,0.06);
    }
    .card-title {
        font-size: 0.6875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 16px;
    }

    /* ── Badge System ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 100px;
        font-size: 0.6875rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        white-space: nowrap;
    }
    .badge-blue   { background: #eff6ff; color: #1d4ed8; }
    .badge-violet { background: #f5f3ff; color: #6d28d9; }
    .badge-amber  { background: #fffbeb; color: #b45309; }
    .badge-green  { background: #ecfdf5; color: #047857; }

    /* ── Chip System (Skills) ── */
    .chip-group { margin-bottom: 14px; }
    .chip-group-label {
        font-size: 0.6875rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .chip-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }
    .chip {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.8125rem;
        font-weight: 500;
        line-height: 1.3;
        transition: transform 0.1s ease;
    }
    .chip:hover { transform: translateY(-1px); }
    .chip-sm {
        padding: 2px 8px;
        font-size: 0.75rem;
        border-radius: 6px;
        background: #f1f5f9;
        color: #64748b;
    }
    .chip-gap {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }

    /* ── Course Cards ── */
    .course-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        border-left: 3px solid #e2e8f0;
        transition: border-color 0.15s ease;
    }
    .course-card:hover { border-left-color: #7c3aed; }
    .course-title {
        font-weight: 600;
        font-size: 0.8125rem;
        color: #1e293b;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .course-meta {
        font-size: 0.75rem;
        color: #94a3b8;
    }

    /* ── Success / Warning States ── */
    .state-success {
        background: #ecfdf5;
        color: #065f46;
        padding: 14px 18px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8125rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .state-empty {
        color: #94a3b8;
        font-size: 0.8125rem;
        font-style: italic;
        padding: 8px 0;
    }

    /* ── Animations ── */
    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to   { transform: translateX(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
"""


# =============================================================================
# 6. HTML BUILDER FUNCTIONS
# =============================================================================
def build_skill_chips(skill_list):
    """Farbige Chips pro Kategorie mit visueller Gruppierung (Law of Common Region)."""
    by_cat = {}
    for s in skill_list:
        cat = categorize_skill(s)
        by_cat.setdefault(cat, []).append(clean_skill(s))

    if not by_cat:
        return "<p class='state-empty'>Keine Skills erkannt</p>"

    parts = []
    for cat in CAT_ORDER:
        if cat not in by_cat:
            continue
        m = CAT_META[cat]
        chips = "".join(
            f"<span class='chip' style='background:{m['bg']};color:{m['color']};'>{name}</span>"
            for name in by_cat[cat]
        )
        parts.append(
            f"<div class='chip-group'>"
            f"<div class='chip-group-label' style='color:{m['color']};'>"
            f"<span>{m['icon']}</span> {cat}</div>"
            f"<div class='chip-grid'>{chips}</div>"
            f"</div>"
        )
    return "".join(parts)


def build_courses_html(courses):
    if not courses:
        return "<p class='state-empty'>Keine passenden Kurse gefunden</p>"
    lines = []
    for i, (cname, covered, count) in enumerate(courses):
        covered_chips = "".join(
            f"<span class='chip-sm'>{clean_skill(s)}</span>"
            for s in covered[:5]
        )
        lines.append(
            f"<div class='course-card'>"
            f"<div class='course-title'>"
            f"<span style='opacity:0.5;font-size:0.75rem;'>#{i+1}</span> "
            f"{html_lib.escape(cname)}</div>"
            f"<div class='course-meta'>Deckt ab: </div>"
            f"<div class='chip-grid' style='margin-top:6px;'>{covered_chips}</div>"
            f"</div>"
        )
    return "".join(lines)


def build_gaps_html(gaps):
    if not gaps:
        return "<div class='state-success'><span>✅</span> Alle Skills durch MBI-Kurse abgedeckt!</div>"
    chips = "".join(
        f"<span class='chip chip-gap'>{clean_skill(g)}</span>"
        for g in gaps
    )
    return f"<div class='chip-grid'>{chips}</div>"


# =============================================================================
# 7. PROFIL-SEITEN (Ebene 2 + 3)
# =============================================================================
print("\nErstelle Profil-Seiten...")

profil_files = {}

for profil_name in PROFIL_COLORS:
    profil_jobs = df_jobs[df_jobs["mbi_profil"] == profil_name].copy()
    n_jobs = len(profil_jobs)
    short = PROFIL_SHORT[profil_name]
    color = PROFIL_COLORS[profil_name]
    bg_color = PROFIL_BG[profil_name]
    icon = PROFIL_ICONS[profil_name]
    filename = f"profil_{safe_filename(profil_name)}.html"
    profil_files[profil_name] = filename

    avg_skills = profil_jobs[skill_cols].sum(axis=1).mean()
    avg_tech = profil_jobs['Fachdetail_Score'].mean()

    # Top-Skills Barplot (clean Plotly chart)
    skill_freq = profil_jobs[skill_cols].mean() * 100
    top_skills = skill_freq.sort_values(ascending=False).head(15)

    fig_skills = go.Figure()
    bar_colors = [CAT_META.get(categorize_skill(s), {}).get("color", "#94a3b8") for s in top_skills.index]

    fig_skills.add_trace(go.Bar(
        y=[clean_skill(s) for s in top_skills.index],
        x=top_skills.values,
        orientation="h",
        marker_color=bar_colors,
        marker_line_width=0,
        hovertemplate="%{y}: <b>%{x:.1f}%</b><extra></extra>",
    ))
    fig_skills.update_layout(
        xaxis_title="% der Stelleninserate",
        yaxis=dict(autorange="reversed", showgrid=False),
        height=420,
        margin=dict(l=180, r=24, t=16, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#475569"),
        xaxis=dict(gridcolor="#f1f5f9", showline=False, zeroline=False),
    )
    skills_chart_html = fig_skills.to_html(full_html=False, include_plotlyjs=False)

    # Job-Karten als Listeneinträge
    job_items = []
    for idx, job in profil_jobs.iterrows():
        tt = job_tooltips[idx]
        title_text = html_lib.escape(str(job["job_title"]))
        n_skills = len(tt["skills"])
        n_courses = len(tt["courses"])
        n_gaps = len(tt["gaps"])

        # Detail-Panel content
        skills_html = build_skill_chips(tt["skills"])
        courses_html = build_courses_html(tt["courses"])
        gaps_html = build_gaps_html(tt["gaps"])

        panel_content = (
            f"<div class='panel-section'>"
            f"<div class='panel-section-header'>"
            f"<span class='panel-section-icon'>🎯</span>"
            f"<div><div class='panel-section-title'>Benötigte Skills</div>"
            f"<div class='panel-section-count'>{n_skills} erkannt</div></div>"
            f"</div>"
            f"<div class='panel-section-body'>{skills_html}</div>"
            f"</div>"
            f"<div class='panel-section'>"
            f"<div class='panel-section-header'>"
            f"<span class='panel-section-icon'>📚</span>"
            f"<div><div class='panel-section-title'>Empfohlene MBI-Kurse</div>"
            f"<div class='panel-section-count'>{n_courses} Kursempfehlungen</div></div>"
            f"</div>"
            f"<div class='panel-section-body'>{courses_html}</div>"
            f"</div>"
            f"<div class='panel-section'>"
            f"<div class='panel-section-header'>"
            f"<span class='panel-section-icon'>⚡</span>"
            f"<div><div class='panel-section-title'>Skill-Gaps</div>"
            f"<div class='panel-section-count'>Selbst zu erwerben (max. 3)</div></div>"
            f"</div>"
            f"<div class='panel-section-body'>{gaps_html}</div>"
            f"</div>"
        )

        gap_indicator = (
            f"<span class='badge badge-amber'>{n_gaps} Gap{'s' if n_gaps != 1 else ''}</span>"
            if n_gaps > 0
            else "<span class='badge badge-green'>✓ Abgedeckt</span>"
        )

        job_items.append(
            f"<div class='job-card' data-panel=\"{html_lib.escape(panel_content)}\" "
            f"data-title=\"{html_lib.escape(title_text)}\">"
            f"<div class='job-card-main'>"
            f"<div class='job-card-title'>{title_text}</div>"
            f"<div class='job-card-badges'>"
            f"<span class='badge badge-blue'>{n_skills} Skills</span>"
            f"<span class='badge badge-violet'>{n_courses} Kurse</span>"
            f"{gap_indicator}"
            f"</div>"
            f"</div>"
            f"<div class='job-card-arrow'>→</div>"
            f"</div>"
        )

    jobs_html = "\n".join(job_items)

    # ─── PROFIL PAGE HTML ───
    page_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{short} – MBI Career Explorer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        {SHARED_CSS}

        /* ── Page Header ── */
        .page-header {{
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 0;
        }}
        .header-inner {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 24px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .header-left {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .header-icon {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            background: {bg_color};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            /* Refactoring UI: accent border adds color to bland design */
            border: 2px solid {color}20;
        }}
        .header-text h1 {{
            font-size: 1.25rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.3;
        }}
        .breadcrumb {{
            font-size: 0.8125rem;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .breadcrumb a {{
            color: #64748b;
            text-decoration: none;
            transition: color 0.15s;
        }}
        .breadcrumb a:hover {{ color: {color}; }}
        .breadcrumb-sep {{ color: #cbd5e1; }}

        .back-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 0.8125rem;
            font-weight: 600;
            color: #475569;
            text-decoration: none;
            background: #f1f5f9;
            transition: all 0.15s ease;
        }}
        .back-btn:hover {{
            background: #e2e8f0;
            color: #1e293b;
        }}

        /* ── Container ── */
        .container {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 32px 40px 64px;
        }}

        /* ── KPI Grid ── */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }}
        .kpi-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
            /* Refactoring UI: accent border top */
            border-top: 3px solid {color};
        }}
        .kpi-value {{
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1;
            margin-bottom: 4px;
        }}
        .kpi-label {{
            font-size: 0.8125rem;
            color: #94a3b8;
            font-weight: 500;
        }}

        /* ── Content Grid ── */
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}

        /* ── Search ── */
        .search-wrap {{
            position: relative;
            margin-bottom: 20px;
        }}
        .search-icon {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: #94a3b8;
            font-size: 14px;
            pointer-events: none;
        }}
        .search-input {{
            width: 100%;
            padding: 14px 16px 14px 44px;
            font-size: 0.9375rem;
            font-family: inherit;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            outline: none;
            background: white;
            color: #1e293b;
            transition: all 0.2s ease;
        }}
        .search-input:focus {{
            border-color: {color};
            box-shadow: 0 0 0 4px {color}15;
        }}
        .search-input::placeholder {{ color: #cbd5e1; }}

        /* ── Job count ── */
        .results-count {{
            font-size: 0.8125rem;
            color: #94a3b8;
            margin-bottom: 16px;
            font-weight: 500;
        }}
        .results-count strong {{
            color: #475569;
            font-weight: 700;
        }}

        /* ── Job Cards (Fitts's Law: large targets) ── */
        .job-list {{ display: flex; flex-direction: column; gap: 2px; }}

        .job-card {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            background: white;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.15s ease;
            border: 1px solid transparent;
        }}
        .job-card:hover {{
            background: {bg_color};
            border-color: {color}20;
            transform: translateX(4px);
        }}
        .job-card.active {{
            background: {bg_color};
            border-color: {color}40;
            box-shadow: inset 3px 0 0 {color};
        }}

        .job-card-main {{ flex: 1; min-width: 0; }}
        .job-card-title {{
            font-weight: 600;
            font-size: 0.9375rem;
            color: #1e293b;
            margin-bottom: 6px;
            /* Prevent overflow */
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .job-card-badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .job-card-arrow {{
            color: #cbd5e1;
            font-size: 1.125rem;
            flex-shrink: 0;
            margin-left: 16px;
            transition: color 0.15s, transform 0.15s;
        }}
        .job-card:hover .job-card-arrow {{
            color: {color};
            transform: translateX(3px);
        }}

        /* ── Legend ── */
        .legend {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 20px;
            padding: 12px 16px;
            background: #f8fafc;
            border-radius: 10px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.75rem;
            color: #64748b;
            font-weight: 500;
        }}
        .legend-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        /* ── Overlay + Detail Panel ── */
        .overlay {{
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.4);
            z-index: 999;
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }}
        .overlay.visible {{
            display: block;
            animation: fadeIn 0.2s ease;
        }}

        .detail-panel {{
            display: none;
            position: fixed;
            right: 0;
            top: 0;
            width: min(520px, 90vw);
            height: 100vh;
            background: white;
            z-index: 1000;
            overflow-y: auto;
            /* Refactoring UI: multi-layer shadow for depth */
            box-shadow:
                -4px 0 6px rgba(0,0,0,0.02),
                -16px 0 36px rgba(0,0,0,0.06),
                -40px 0 80px rgba(0,0,0,0.04);
        }}
        .detail-panel.visible {{
            display: block;
            animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .panel-top {{
            position: sticky;
            top: 0;
            z-index: 10;
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 20px 28px;
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .panel-close {{
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: none;
            background: #f1f5f9;
            border-radius: 10px;
            cursor: pointer;
            color: #64748b;
            font-size: 1rem;
            flex-shrink: 0;
            transition: all 0.15s ease;
        }}
        .panel-close:hover {{
            background: #e2e8f0;
            color: #1e293b;
        }}
        .panel-job-title {{
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.35;
            flex: 1;
            min-width: 0;
        }}

        .panel-body {{
            padding: 24px 28px 48px;
        }}

        /* ── Panel Sections (Chunking / Law of Common Region) ── */
        .panel-section {{
            margin-bottom: 28px;
        }}
        .panel-section:last-child {{ margin-bottom: 0; }}

        .panel-section-header {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 16px;
        }}
        .panel-section-icon {{
            font-size: 1.25rem;
            line-height: 1;
            flex-shrink: 0;
            margin-top: 2px;
        }}
        .panel-section-title {{
            font-size: 0.875rem;
            font-weight: 700;
            color: #1e293b;
        }}
        .panel-section-count {{
            font-size: 0.75rem;
            color: #94a3b8;
            font-weight: 500;
            margin-top: 1px;
        }}
        .panel-section-body {{
            padding-left: 36px;
        }}
        /* Divider between sections */
        .panel-section + .panel-section {{
            padding-top: 24px;
            border-top: 1px solid #f1f5f9;
        }}

        /* ── Responsive ── */
        @media (max-width: 960px) {{
            .content-grid {{ grid-template-columns: 1fr; }}
            .kpi-grid {{ grid-template-columns: 1fr; }}
            .header-inner {{ flex-direction: column; align-items: flex-start; gap: 12px; }}
            .container {{ padding: 24px 20px 48px; }}
        }}
        @media (max-width: 640px) {{
            .detail-panel {{ width: 100vw; }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="page-header">
        <div class="header-inner">
            <div class="header-left">
                <div class="header-icon">{icon}</div>
                <div class="header-text">
                    <div class="breadcrumb">
                        <a href="index.html">MBI Career Explorer</a>
                        <span class="breadcrumb-sep">/</span>
                        <span style="color:#475569;">{short}</span>
                    </div>
                    <h1>{profil_name}</h1>
                </div>
            </div>
            <a href="index.html" class="back-btn">
                <span>←</span> Zur Übersicht
            </a>
        </div>
    </header>

    <div class="container">
        <!-- KPIs -->
        <div class="kpi-grid" style="animation: slideUp 0.4s ease both;">
            <div class="kpi-card">
                <div class="kpi-value">{n_jobs}</div>
                <div class="kpi-label">Stelleninserate</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{avg_skills:.1f}</div>
                <div class="kpi-label">Ø Skills pro Stelle</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{avg_tech:.1f}</div>
                <div class="kpi-label">Ø TechSkill Score</div>
            </div>
        </div>

        <!-- Chart + Stats -->
        <div class="content-grid" style="animation: slideUp 0.5s ease both;">
            <div class="card">
                <div class="card-title">Top 15 gefragte Skills</div>
                {skills_chart_html}
            </div>
            <div class="card">
                <div class="card-title">Skill-Kategorien im Vergleich</div>
                <div style="padding: 16px 0;">
                    {"".join(f'''<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                        <div style="width:44px;height:44px;border-radius:12px;background:{CAT_META[cat]['bg']};display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">{CAT_META[cat]['icon']}</div>
                        <div style="flex:1;min-width:0;">
                            <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
                                <span style="font-weight:600;font-size:0.8125rem;color:#1e293b;">{cat}</span>
                                <span style="font-weight:700;font-size:0.8125rem;color:{CAT_META[cat]['color']};">{profil_jobs[[c for c in skill_cols if categorize_skill(c)==cat]].mean(axis=1).mean()*100:.0f}%</span>
                            </div>
                            <div style="height:6px;border-radius:3px;background:#f1f5f9;overflow:hidden;">
                                <div style="height:100%;width:{min(profil_jobs[[c for c in skill_cols if categorize_skill(c)==cat]].mean(axis=1).mean()*100*4, 100):.0f}%;background:{CAT_META[cat]['color']};border-radius:3px;transition:width 0.6s ease;"></div>
                            </div>
                        </div>
                    </div>''' for cat in CAT_ORDER if any(categorize_skill(c)==cat for c in skill_cols))}
                </div>
            </div>
        </div>

        <!-- Job List -->
        <div class="card" style="animation: slideUp 0.6s ease both;">
            <div class="card-title">Stelleninserate</div>

            <div class="search-wrap">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
                </svg>
                <input type="text" class="search-input" id="searchInput"
                       placeholder="Jobtitel durchsuchen...">
            </div>

            <div class="legend">
                <div class="legend-item"><span class="legend-dot" style="background:#1d4ed8;"></span> Skills</div>
                <div class="legend-item"><span class="legend-dot" style="background:#6d28d9;"></span> Kursempfehlungen</div>
                <div class="legend-item"><span class="legend-dot" style="background:#b45309;"></span> Skill-Gaps</div>
                <div class="legend-item"><span class="legend-dot" style="background:#047857;"></span> Abgedeckt</div>
            </div>

            <div class="results-count" id="resultsCount">
                <strong>{n_jobs}</strong> Stellen gefunden
            </div>

            <div class="job-list" id="jobList">
                {jobs_html}
            </div>
        </div>
    </div>

    <!-- Overlay + Detail Panel -->
    <div class="overlay" id="overlay"></div>
    <div class="detail-panel" id="detailPanel">
        <div class="panel-top">
            <button class="panel-close" id="closeBtn" title="Schliessen (Esc)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                    <path d="M18 6 6 18M6 6l12 12"/>
                </svg>
            </button>
            <div class="panel-job-title" id="panelTitle">–</div>
        </div>
        <div class="panel-body" id="panelBody"></div>
    </div>

    <script>
        // ── Search with result count (System Status Visibility) ──
        const searchInput = document.getElementById('searchInput');
        const resultsCount = document.getElementById('resultsCount');
        const allCards = document.querySelectorAll('.job-card');

        searchInput.addEventListener('input', function() {{
            const q = this.value.toLowerCase();
            let visible = 0;
            allCards.forEach(c => {{
                const match = c.textContent.toLowerCase().includes(q);
                c.style.display = match ? '' : 'none';
                if (match) visible++;
            }});
            resultsCount.innerHTML = '<strong>' + visible + '</strong> Stellen gefunden';
        }});

        // ── Panel open (Fitts's Law: whole card is clickable) ──
        allCards.forEach(card => {{
            card.addEventListener('click', function() {{
                document.getElementById('panelTitle').textContent = this.dataset.title;
                document.getElementById('panelBody').innerHTML = this.dataset.panel;
                document.getElementById('detailPanel').classList.add('visible');
                document.getElementById('overlay').classList.add('visible');
                document.body.style.overflow = 'hidden';
                allCards.forEach(c => c.classList.remove('active'));
                this.classList.add('active');
            }});
        }});

        // ── Panel close (User Control & Freedom) ──
        function closePanel() {{
            document.getElementById('detailPanel').classList.remove('visible');
            document.getElementById('overlay').classList.remove('visible');
            document.body.style.overflow = '';
            allCards.forEach(c => c.classList.remove('active'));
        }}
        document.getElementById('closeBtn').addEventListener('click', closePanel);
        document.getElementById('overlay').addEventListener('click', closePanel);
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closePanel();
        }});
    </script>
</body>
</html>"""

    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  ✓ {short}: {filename} ({n_jobs} Jobs)")


# =============================================================================
# 8. ÜBERSICHTSSEITE (Ebene 1)
# =============================================================================
print("\nErstelle Übersichtsseite...")

profil_stats = []
for profil_name in PROFIL_COLORS:
    subset = df_jobs[df_jobs["mbi_profil"] == profil_name]
    profil_stats.append({
        "name": profil_name,
        "short": PROFIL_SHORT[profil_name],
        "count": len(subset),
        "color": PROFIL_COLORS[profil_name],
        "bg": PROFIL_BG[profil_name],
        "icon": PROFIL_ICONS[profil_name],
        "avg_skills": subset[skill_cols].sum(axis=1).mean(),
        "avg_tech": subset["Fachdetail_Score"].mean(),
        "file": profil_files[profil_name],
    })

profil_stats.sort(key=lambda x: -x["count"])

total_jobs = len(df_jobs)
total_avg_skills = df_jobs[skill_cols].sum(axis=1).mean()

# ── Donut Chart (cleaner than sunburst) ──
fig = go.Figure(go.Pie(
    labels=[ps["short"] for ps in profil_stats],
    values=[ps["count"] for ps in profil_stats],
    marker=dict(colors=[ps["color"] for ps in profil_stats]),
    hole=0.6,
    textinfo="label+percent",
    textposition="outside",
    textfont=dict(size=12, family="Inter, sans-serif"),
    hovertemplate="<b>%{label}</b><br>%{value} Stellen (%{percent})<extra></extra>",
    pull=[0.02] * len(profil_stats),
    sort=False,
))
fig.update_layout(
    margin=dict(t=20, l=20, r=20, b=20),
    height=380,
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, -apple-system, sans-serif", color="#475569"),
    annotations=[dict(
        text=f"<b>{total_jobs}</b><br><span style='font-size:12px;color:#94a3b8'>Stellen</span>",
        x=0.5, y=0.5, font_size=28, showarrow=False, font_color="#0f172a",
        font_family="Inter, sans-serif",
    )]
)
chart_html = fig.to_html(full_html=False, include_plotlyjs=False)

# ── Profile Cards ──
cards_html = ""
for i, ps in enumerate(profil_stats):
    pct = ps["count"] / total_jobs * 100
    cards_html += f"""
    <a href="{ps['file']}" class="profile-card" style="animation-delay: {0.1 + i*0.06}s;">
        <div class="profile-card-accent" style="background: {ps['color']};"></div>
        <div class="profile-card-body">
            <div class="profile-card-header">
                <div class="profile-card-icon" style="background:{ps['bg']};">
                    {ps['icon']}
                </div>
                <div>
                    <div class="profile-card-name">{ps['short']}</div>
                    <div class="profile-card-sub">{ps['count']} Stellen · {pct:.0f}%</div>
                </div>
            </div>
            <div class="profile-card-stats">
                <div class="profile-card-stat">
                    <div class="profile-card-stat-val" style="color:{ps['color']};">{ps['avg_skills']:.0f}</div>
                    <div class="profile-card-stat-lbl">Ø Skills</div>
                </div>
                <div class="profile-card-stat">
                    <div class="profile-card-stat-val" style="color:{ps['color']};">{ps['avg_tech']:.1f}</div>
                    <div class="profile-card-stat-lbl">Ø Tech</div>
                </div>
                <div class="profile-card-stat">
                    <div class="profile-card-stat-val" style="color:{ps['color']};">{ps['count']}</div>
                    <div class="profile-card-stat-lbl">Stellen</div>
                </div>
            </div>
            <div class="profile-card-cta" style="color:{ps['color']};">
                Profil erkunden <span>→</span>
            </div>
        </div>
    </a>"""

# ── Kennzahlen Table ──
table_rows = ""
for ps in profil_stats:
    table_rows += f"""<tr>
        <td>
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="width:10px;height:10px;border-radius:50%;background:{ps['color']};flex-shrink:0;"></span>
                <span style="font-weight:600;">{ps['short']}</span>
            </div>
        </td>
        <td style="text-align:right;font-weight:700;font-variant-numeric:tabular-nums;">{ps['count']}</td>
        <td style="text-align:right;font-variant-numeric:tabular-nums;">{ps['avg_skills']:.0f}</td>
        <td style="text-align:right;font-variant-numeric:tabular-nums;">{ps['avg_tech']:.1f}</td>
    </tr>"""

index_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MBI Career Explorer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        {SHARED_CSS}

        /* ── Hero Section ── */
        .hero {{
            background: #0f172a;
            color: white;
            padding: 64px 40px 56px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        /* Subtle geometric decoration */
        .hero::before {{
            content: '';
            position: absolute;
            top: -60%;
            left: -20%;
            width: 140%;
            height: 200%;
            background: radial-gradient(ellipse at 30% 50%, rgba(37, 99, 235, 0.12) 0%, transparent 60%),
                        radial-gradient(ellipse at 70% 50%, rgba(124, 58, 237, 0.08) 0%, transparent 60%);
            pointer-events: none;
        }}
        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 680px;
            margin: 0 auto;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 16px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 100px;
            font-size: 0.8125rem;
            font-weight: 500;
            color: rgba(255,255,255,0.7);
            margin-bottom: 20px;
            backdrop-filter: blur(8px);
        }}
        .hero h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.15;
            margin-bottom: 16px;
        }}
        .hero p {{
            font-size: 1.0625rem;
            color: rgba(255,255,255,0.6);
            line-height: 1.65;
            max-width: 540px;
            margin: 0 auto;
        }}

        /* ── Main Container ── */
        .main {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 40px 80px;
        }}

        /* ── Overview Grid ── */
        .overview-grid {{
            display: grid;
            grid-template-columns: 5fr 7fr;
            gap: 24px;
            margin-bottom: 48px;
        }}

        /* ── Kennzahlen Table ── */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }}
        .data-table thead th {{
            text-align: left;
            padding: 10px 12px;
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94a3b8;
            border-bottom: 2px solid #e2e8f0;
        }}
        .data-table tbody td {{
            padding: 12px 12px;
            color: #475569;
            border-bottom: 1px solid #f1f5f9;
        }}
        .data-table tbody tr:last-child td {{
            border-bottom: none;
        }}
        .data-table tfoot td {{
            padding: 12px 12px;
            font-weight: 700;
            color: #1e293b;
            border-top: 2px solid #e2e8f0;
        }}

        /* ── Section Header ── */
        .section-header {{
            margin-bottom: 24px;
        }}
        .section-title {{
            font-size: 1.375rem;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.02em;
        }}
        .section-desc {{
            font-size: 0.9375rem;
            color: #94a3b8;
            margin-top: 4px;
        }}

        /* ── Profile Card Grid ── */
        .profile-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 20px;
        }}
        .profile-card {{
            display: block;
            text-decoration: none;
            color: inherit;
            border-radius: 16px;
            overflow: hidden;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            animation: slideUp 0.5s ease both;
        }}
        .profile-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 16px 40px rgba(0,0,0,0.08);
        }}
        /* Refactoring UI: accent border via colored top bar */
        .profile-card-accent {{
            height: 4px;
            width: 100%;
        }}
        .profile-card-body {{
            padding: 24px;
        }}
        .profile-card-header {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 20px;
        }}
        .profile-card-icon {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            flex-shrink: 0;
        }}
        .profile-card-name {{
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
        }}
        .profile-card-sub {{
            font-size: 0.8125rem;
            color: #94a3b8;
            font-weight: 500;
        }}
        .profile-card-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 18px;
            padding: 14px 0;
            border-top: 1px solid #f1f5f9;
            border-bottom: 1px solid #f1f5f9;
        }}
        .profile-card-stat {{ text-align: center; }}
        .profile-card-stat-val {{
            font-size: 1.375rem;
            font-weight: 800;
            line-height: 1;
            font-variant-numeric: tabular-nums;
        }}
        .profile-card-stat-lbl {{
            font-size: 0.6875rem;
            color: #94a3b8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: 4px;
        }}
        .profile-card-cta {{
            font-size: 0.875rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .profile-card-cta span {{
            transition: transform 0.2s ease;
        }}
        .profile-card:hover .profile-card-cta span {{
            transform: translateX(4px);
        }}

        /* ── How it works ── */
        .how-it-works {{
            display: flex;
            gap: 4px;
            margin-bottom: 48px;
            background: white;
            border-radius: 16px;
            padding: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        }}
        .step {{
            flex: 1;
            padding: 20px 24px;
            border-radius: 12px;
            transition: background 0.2s ease;
        }}
        .step:hover {{ background: #f8fafc; }}
        .step-num {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: #eff6ff;
            color: #2563eb;
            font-size: 0.8125rem;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .step-title {{
            font-size: 0.875rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 4px;
        }}
        .step-desc {{
            font-size: 0.8125rem;
            color: #94a3b8;
            line-height: 1.5;
        }}

        /* ── Responsive ── */
        @media (max-width: 900px) {{
            .overview-grid {{ grid-template-columns: 1fr; }}
            .how-it-works {{ flex-direction: column; }}
            .hero h1 {{ font-size: 1.75rem; }}
            .main {{ padding: 24px 20px 60px; }}
        }}
    </style>
</head>
<body>
    <!-- Hero -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-badge">🎓 MBI-Studiengang · FHNW</div>
            <h1>Career Explorer</h1>
            <p>Interaktive Analyse von {total_jobs} Stelleninseraten,
               zugeordnet zu den 6 Vertiefungsprofilen des MBI-Studiengangs.
               Finde deinen Weg vom Studium in den Arbeitsmarkt.</p>
        </div>
    </section>

    <div class="main">
        <!-- How it works -->
        <div class="how-it-works" style="animation: slideUp 0.4s ease both;">
            <div class="step">
                <div class="step-num">1</div>
                <div class="step-title">Profil wählen</div>
                <div class="step-desc">Wähle eines der 6 MBI-Vertiefungsprofile aus.</div>
            </div>
            <div class="step">
                <div class="step-num">2</div>
                <div class="step-title">Stellen erkunden</div>
                <div class="step-desc">Durchsuche passende Stelleninserate aus dem Markt.</div>
            </div>
            <div class="step">
                <div class="step-num">3</div>
                <div class="step-title">Skills & Kurse</div>
                <div class="step-desc">Sieh benötigte Skills, passende MBI-Kurse und Gaps.</div>
            </div>
        </div>

        <!-- Overview -->
        <div class="overview-grid" style="animation: slideUp 0.5s ease both;">
            <div class="card" style="display:flex;flex-direction:column;">
                <div class="card-title">Verteilung nach Profil</div>
                <div style="flex:1;display:flex;align-items:center;">
                    {chart_html}
                </div>
            </div>
            <div class="card">
                <div class="card-title">Kennzahlen</div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Profil</th>
                            <th style="text-align:right;">Stellen</th>
                            <th style="text-align:right;">Ø Skills</th>
                            <th style="text-align:right;">Ø Tech</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td>Total</td>
                            <td style="text-align:right;">{total_jobs}</td>
                            <td style="text-align:right;">{total_avg_skills:.0f}</td>
                            <td style="text-align:right;">{df_jobs['Fachdetail_Score'].mean():.1f}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>

        <!-- Profile Cards -->
        <div class="section-header">
            <div class="section-title">Profile erkunden</div>
            <div class="section-desc">Wähle ein Profil, um die zugehörigen Stelleninserate zu sehen.</div>
        </div>
        <div class="profile-grid">
            {cards_html}
        </div>
    </div>
</body>
</html>"""

index_path = os.path.join(OUT_DIR, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"  ✓ Übersicht: index.html")

# =============================================================================
# FERTIG
# =============================================================================
print(f"\n{'='*60}")
print("INTERAKTIVER EXPLORER v3 – PREMIUM UI ERSTELLT!")
print(f"{'='*60}")
print(f"\n  Öffne: {os.path.abspath(index_path)}")
print(f"\n  Dateien in '{OUT_DIR}/':")
print(f"    index.html")
for ps in profil_stats:
    print(f"    {profil_files[ps['name']]:45s} ({ps['count']} Jobs)")
print(f"\n  Design-Prinzipien:")
print(f"    ✓ Inter Font (Google Fonts)")
print(f"    ✓ 8px Spacing Grid")
print(f"    ✓ Offset Shadows (Refactoring UI)")
print(f"    ✓ Accent Borders statt voller Borders")
print(f"    ✓ Visual Hierarchy via Weight+Color")
print(f"    ✓ Micro-Interactions & Animations")
print(f"    ✓ Chunking & Law of Proximity")
