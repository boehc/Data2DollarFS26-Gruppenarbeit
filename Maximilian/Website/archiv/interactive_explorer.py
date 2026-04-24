"""
===============================================================================
INTERAKTIVE MBI CAREER EXPLORER
===============================================================================
Erstellt eine mehrstufige interaktive HTML-Visualisierung:

  Ebene 1: 6 MBI-Profile (Übersichtsseite)
  Ebene 2: Alle Jobtitel pro Profil (eigene Seite pro Profil)
  Ebene 3: Hover → Skills, Kursvorschläge, Skill-Gaps

Datenquellen:
  - jobs_final.csv (1194 Jobs mit MBI-Profilen + Skills)
  - mbi_curriculum_kategorisiert.csv (84 Kurse mit Skills)

Output:
  - interactive_explorer/index.html  (Übersicht)
  - interactive_explorer/profil_*.html (je Profil)
===============================================================================
"""

import pandas as pd
import plotly.graph_objects as go
import os
import json
import re
import html as html_lib

# =============================================================================
# 1. KONFIGURATION
# =============================================================================
OUT_DIR = "interactive_explorer"
os.makedirs(OUT_DIR, exist_ok=True)

PROFIL_COLORS = {
    "Business Development":                   "#4CAF50",
    "Digital Channel & CRM":                  "#9C27B0",
    "Start-up & Scale-up Entrepreneurship":   "#FF9800",
    "Supply Chain & Operations Management":   "#F44336",
    "Technology Solution Architect":          "#2196F3",
    "Transforming & Managing Digital Business": "#607D8B",
}

PROFIL_SHORT = {
    "Business Development":                   "Business Dev.",
    "Digital Channel & CRM":                  "Digital Channel",
    "Start-up & Scale-up Entrepreneurship":   "Startup/Scale-up",
    "Supply Chain & Operations Management":   "Supply Chain",
    "Technology Solution Architect":          "Tech Architect",
    "Transforming & Managing Digital Business": "Digital Business",
}

# Mapping Curriculum-Profil-Spalten → jobs_final mbi_profil
CURRICULUM_PROFIL_MAP = {
    "Business Development":                   "Business Development",
    "Digital Channel & CRM":                  "Digital Channel & CRM",
    "Startup & Scale-up":                     "Start-up & Scale-up Entrepreneurship",
    "Supply Chain & Operations":              "Supply Chain & Operations Management",
    "Technology Architecture":                "Technology Solution Architect",
    "Digital Transformation":                 "Transforming & Managing Digital Business",
}

def clean_skill(col):
    """FK_Waren_Produktkenntnisse → Waren- & Produktkenntnisse"""
    name = col.split("_", 1)[1] if "_" in col else col
    return name.replace("_", " ")


def safe_filename(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")

# =============================================================================
# 2. DATEN LADEN
# =============================================================================
print("Lade Daten...")
df_jobs = pd.read_csv("jobs_final.csv")
df_curr = pd.read_csv("mbi_curriculum_kategorisiert.csv", sep=";")

# Skill-Spalten (ohne Berufserfahrung_Jahre und Scores)
skill_cols = [c for c in df_jobs.columns
              if c.startswith(("FK_", "FD_", "SK_", "MK_", "PK_"))
              and c != "FD_Berufserfahrung_Jahre"]

# Gleiche Skill-Spalten im Curriculum
curr_skill_cols = [c for c in skill_cols if c in df_curr.columns]

print(f"  Jobs: {len(df_jobs)}, Kurse: {len(df_curr)}, Skills: {len(skill_cols)}")

# =============================================================================
# 3. KURS-EMPFEHLUNGS-ENGINE
# =============================================================================
def get_job_skills(job_row):
    """Gibt Liste der aktiven Skills (=1) für einen Job zurück."""
    return [c for c in skill_cols if job_row.get(c, 0) == 1]


def get_matching_courses(required_skills, max_courses=5):
    """
    Findet Kurse, die die meisten der benötigten Skills abdecken.
    Gibt Liste von (course_title, covered_skills, coverage_count) zurück.
    """
    if not required_skills:
        return []

    course_scores = []
    for _, course in df_curr.iterrows():
        covered = [s for s in required_skills
                   if s in curr_skill_cols and course.get(s, 0) == 1]
        if covered:
            course_scores.append((
                course["course_title"],
                covered,
                len(covered),
            ))

    course_scores.sort(key=lambda x: -x[2])
    return course_scores[:max_courses]


def get_skill_gaps(required_skills, recommended_courses, max_gaps=3):
    """
    Findet Skills, die von keinem der empfohlenen Kurse abgedeckt werden.
    """
    covered_by_courses = set()
    for _, covered, _ in recommended_courses:
        covered_by_courses.update(covered)

    gaps = [s for s in required_skills if s not in covered_by_courses]
    return gaps[:max_gaps]


def categorize_skill(col):
    """Gibt die Hauptkategorie eines Skills zurück."""
    if col.startswith("FK_"): return "Fachkompetenz"
    if col.startswith("FD_"): return "TechSkill"
    if col.startswith("SK_"): return "Sozialkompetenz"
    if col.startswith("MK_"): return "Methodenkompetenz"
    if col.startswith("PK_"): return "Personalkompetenz"
    return "Andere"


# =============================================================================
# 4. PRO JOB: TOOLTIP-DATEN VORBERECHNEN
# =============================================================================
print("Berechne Kurs-Empfehlungen für jeden Job...")

job_tooltips = {}
for idx, job in df_jobs.iterrows():
    skills = get_job_skills(job)
    courses = get_matching_courses(skills)
    gaps = get_skill_gaps(skills, courses)
    job_tooltips[idx] = {
        "skills": skills,
        "courses": courses,
        "gaps": gaps,
    }

print(f"  ✓ {len(job_tooltips)} Jobs verarbeitet")

# =============================================================================
# 5. PROFIL-SEITEN ERSTELLEN (Ebene 2 + 3)
# =============================================================================
print("\nErstelle Profil-Seiten...")

profil_files = {}

for profil_name in PROFIL_COLORS:
    profil_jobs = df_jobs[df_jobs["mbi_profil"] == profil_name].copy()
    n_jobs = len(profil_jobs)
    short = PROFIL_SHORT[profil_name]
    color = PROFIL_COLORS[profil_name]
    filename = f"profil_{safe_filename(profil_name)}.html"
    profil_files[profil_name] = filename

    # --- Skill-Häufigkeiten für dieses Profil ---
    skill_freq = profil_jobs[skill_cols].mean() * 100
    top_skills = skill_freq.sort_values(ascending=False).head(15)

    # --- Top-Skills Barplot ---
    fig_skills = go.Figure()
    bar_colors = []
    for s in top_skills.index:
        cat = categorize_skill(s)
        if cat == "Fachkompetenz": bar_colors.append("#2196F3")
        elif cat == "TechSkill": bar_colors.append("#FF5722")
        elif cat == "Sozialkompetenz": bar_colors.append("#4CAF50")
        elif cat == "Methodenkompetenz": bar_colors.append("#FF9800")
        elif cat == "Personalkompetenz": bar_colors.append("#E91E63")
        else: bar_colors.append("#999")

    fig_skills.add_trace(go.Bar(
        y=[clean_skill(s) for s in top_skills.index],
        x=top_skills.values,
        orientation="h",
        marker_color=bar_colors,
        hovertemplate="%{y}: <b>%{x:.1f}%</b><extra></extra>",
    ))
    fig_skills.update_layout(
        title=f"Top 15 Skills – {short}",
        xaxis_title="% der Stelleninserate",
        yaxis=dict(autorange="reversed"),
        height=450,
        margin=dict(l=200, r=30, t=50, b=40),
        plot_bgcolor="white",
    )
    skills_html = fig_skills.to_html(full_html=False, include_plotlyjs=False)

    # --- Jobtitel-Tabelle mit Hover-Tooltips ---
    table_rows = []
    for idx, job in profil_jobs.iterrows():
        tt = job_tooltips[idx]
        title = html_lib.escape(str(job["job_title"]))
        company = html_lib.escape(str(job.get("company", "")))
        location = html_lib.escape(str(job.get("location", "")))

        # Skills formatieren
        skills_by_cat = {}
        for s in tt["skills"]:
            cat = categorize_skill(s)
            skills_by_cat.setdefault(cat, []).append(clean_skill(s))

        skills_html_parts = []
        cat_icons = {
            "Fachkompetenz": "🎓", "TechSkill": "💻",
            "Sozialkompetenz": "🤝", "Methodenkompetenz": "📋",
            "Personalkompetenz": "💡"
        }
        for cat in ["Fachkompetenz", "TechSkill", "Sozialkompetenz", "Methodenkompetenz", "Personalkompetenz"]:
            if cat in skills_by_cat:
                icon = cat_icons.get(cat, "")
                items = ", ".join(skills_by_cat[cat])
                skills_html_parts.append(f"<b>{icon} {cat}:</b> {items}")

        skills_tooltip = "<br>".join(skills_html_parts) if skills_html_parts else "Keine Skills erkannt"

        # Kurse
        if tt["courses"]:
            course_lines = []
            for cname, covered, count in tt["courses"]:
                covered_names = ", ".join(clean_skill(s) for s in covered[:4])
                course_lines.append(f"📚 <b>{html_lib.escape(cname)}</b><br>&nbsp;&nbsp;&nbsp;→ deckt ab: {covered_names}")
            courses_tooltip = "<br>".join(course_lines)
        else:
            courses_tooltip = "Keine passenden Kurse gefunden"

        # Gaps
        if tt["gaps"]:
            gap_names = [f"⚠️ {clean_skill(g)}" for g in tt["gaps"]]
            gaps_tooltip = "<br>".join(gap_names)
        else:
            gaps_tooltip = "✅ Alle Skills durch MBI-Kurse abgedeckt!"

        # Tooltip zusammensetzen (als data attribute)
        full_tooltip = (
            f"<div class='tt-section'><h4>🎯 Benötigte Skills ({len(tt['skills'])})</h4>{skills_tooltip}</div>"
            f"<div class='tt-section'><h4>📚 Empfohlene MBI-Kurse</h4>{courses_tooltip}</div>"
            f"<div class='tt-section'><h4>🔧 Selbst zu erwerben (max. 3)</h4>{gaps_tooltip}</div>"
        )

        # Kompaktes Skill-Badge
        n_skills = len(tt["skills"])
        n_courses = len(tt["courses"])
        n_gaps = len(tt["gaps"])

        table_rows.append(f"""
        <tr class="job-row" data-tooltip="{html_lib.escape(full_tooltip)}">
            <td class="job-title">{title}</td>
            <td>{company}</td>
            <td>{location}</td>
            <td class="badge-cell">
                <span class="badge badge-skills">{n_skills} Skills</span>
                <span class="badge badge-courses">{n_courses} Kurse</span>
                {"<span class='badge badge-gaps'>" + str(n_gaps) + " Gaps</span>" if n_gaps > 0 else "<span class='badge badge-ok'>✓ Abgedeckt</span>"}
            </td>
        </tr>""")

    table_html = "\n".join(table_rows)

    # --- Vollständige HTML-Seite ---
    page_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{short} – MBI Career Explorer</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f5f5f5; color: #333; }}
        .header {{
            background: linear-gradient(135deg, {color}, {color}dd);
            color: white; padding: 30px 40px; position: relative;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 5px; }}
        .header p {{ opacity: 0.9; font-size: 16px; }}
        .back-link {{
            position: absolute; top: 20px; right: 30px;
            color: white; text-decoration: none; font-size: 14px;
            background: rgba(255,255,255,0.2); padding: 8px 16px;
            border-radius: 6px; transition: background 0.2s;
        }}
        .back-link:hover {{ background: rgba(255,255,255,0.35); }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
        .card {{
            background: white; border-radius: 12px; padding: 25px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}
        .card h2 {{ font-size: 18px; margin-bottom: 15px; color: #444; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
        .stat-box {{
            background: #f8f9fa; border-radius: 8px; padding: 15px;
            text-align: center;
        }}
        .stat-box .num {{ font-size: 28px; font-weight: 700; color: {color}; }}
        .stat-box .label {{ font-size: 12px; color: #888; margin-top: 4px; }}

        /* Suchfunktion */
        .search-bar {{
            width: 100%; padding: 12px 20px; font-size: 15px;
            border: 2px solid #e0e0e0; border-radius: 8px;
            margin-bottom: 15px; outline: none; transition: border 0.2s;
        }}
        .search-bar:focus {{ border-color: {color}; }}

        /* Tabelle */
        .jobs-table {{
            width: 100%; border-collapse: separate; border-spacing: 0;
            font-size: 14px;
        }}
        .jobs-table thead th {{
            background: #f8f9fa; padding: 12px 15px; text-align: left;
            border-bottom: 2px solid #e0e0e0; position: sticky; top: 0;
            cursor: pointer; user-select: none;
        }}
        .jobs-table thead th:hover {{ background: #eee; }}
        .jobs-table tbody tr {{
            transition: background 0.15s; cursor: pointer;
        }}
        .jobs-table tbody tr:hover {{ background: #f0f7ff; }}
        .jobs-table td {{ padding: 10px 15px; border-bottom: 1px solid #f0f0f0; }}
        .job-title {{ font-weight: 600; }}

        /* Badges */
        .badge-cell {{ white-space: nowrap; }}
        .badge {{
            display: inline-block; padding: 3px 8px; border-radius: 12px;
            font-size: 11px; font-weight: 600; margin-right: 4px;
        }}
        .badge-skills {{ background: #e3f2fd; color: #1565c0; }}
        .badge-courses {{ background: #f3e5f5; color: #7b1fa2; }}
        .badge-gaps {{ background: #fff3e0; color: #e65100; }}
        .badge-ok {{ background: #e8f5e9; color: #2e7d32; }}

        /* Tooltip */
        .tooltip-panel {{
            display: none; position: fixed; right: 30px; top: 120px;
            width: 420px; max-height: calc(100vh - 150px);
            background: white; border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.18);
            padding: 25px; overflow-y: auto; z-index: 1000;
            border-left: 4px solid {color};
        }}
        .tooltip-panel.visible {{ display: block; }}
        .tooltip-panel h3 {{
            font-size: 16px; margin-bottom: 15px; color: {color};
            border-bottom: 1px solid #eee; padding-bottom: 10px;
        }}
        .tt-section {{ margin-bottom: 15px; }}
        .tt-section h4 {{ font-size: 13px; margin-bottom: 6px; color: #555; }}
        .tt-section b {{ color: #333; }}

        /* Filter buttons */
        .filter-bar {{ margin-bottom: 15px; display: flex; gap: 8px; flex-wrap: wrap; }}
        .filter-btn {{
            padding: 6px 14px; border-radius: 20px; border: 1px solid #ddd;
            background: white; cursor: pointer; font-size: 12px;
            transition: all 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: {color}; color: white; border-color: {color};
        }}

        @media (max-width: 900px) {{
            .grid {{ grid-template-columns: 1fr; }}
            .tooltip-panel {{ position: static; width: 100%; margin-top: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{profil_name}</h1>
        <p>{n_jobs} Stelleninserate aus dem Arbeitsmarkt</p>
        <a href="index.html" class="back-link">← Zurück zur Übersicht</a>
    </div>

    <div class="container">
        <div class="grid">
            <div class="card">
                <h2>Profil-Statistik</h2>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="num">{n_jobs}</div>
                        <div class="label">Stelleninserate</div>
                    </div>
                    <div class="stat-box">
                        <div class="num">{profil_jobs[skill_cols].sum(axis=1).mean():.1f}</div>
                        <div class="label">Ø Skills pro Job</div>
                    </div>
                    <div class="stat-box">
                        <div class="num">{profil_jobs['Fachdetail_Score'].mean():.1f}</div>
                        <div class="label">Ø TechSkill-Score</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <h2>Top 15 Skills in diesem Profil</h2>
                {skills_html}
            </div>
        </div>

        <div class="card" style="position: relative;">
            <h2>Alle Stellen ({n_jobs})</h2>
            <input type="text" class="search-bar" id="searchInput"
                   placeholder="🔍 Jobtitel, Firma oder Ort suchen...">

            <div style="display: flex; gap: 20px;">
                <div style="flex: 1; overflow-x: auto;">
                    <table class="jobs-table" id="jobsTable">
                        <thead>
                            <tr>
                                <th onclick="sortTable(0)">Jobtitel ↕</th>
                                <th onclick="sortTable(1)">Firma ↕</th>
                                <th onclick="sortTable(2)">Ort ↕</th>
                                <th>Übersicht</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_html}
                        </tbody>
                    </table>
                </div>
                <div class="tooltip-panel" id="tooltipPanel">
                    <h3 id="tooltipTitle">Stelle auswählen</h3>
                    <div id="tooltipContent">
                        <p style="color: #999;">Klicke auf eine Stelle, um Skills, Kursvorschläge und Skill-Gaps zu sehen.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Suche
        document.getElementById('searchInput').addEventListener('input', function() {{
            const q = this.value.toLowerCase();
            const rows = document.querySelectorAll('#jobsTable tbody tr');
            rows.forEach(r => {{
                r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none';
            }});
        }});

        // Tooltip bei Klick
        document.querySelectorAll('.job-row').forEach(row => {{
            row.addEventListener('click', function() {{
                const panel = document.getElementById('tooltipPanel');
                const title = this.querySelector('.job-title').textContent;
                const tooltip = this.getAttribute('data-tooltip');
                document.getElementById('tooltipTitle').textContent = title;
                document.getElementById('tooltipContent').innerHTML = tooltip;
                panel.classList.add('visible');
                // Highlight
                document.querySelectorAll('.job-row').forEach(r => r.style.background = '');
                this.style.background = '#e3f2fd';
            }});
        }});

        // Sortierung
        let sortDir = [true, true, true, true];
        function sortTable(col) {{
            const tbody = document.querySelector('#jobsTable tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            sortDir[col] = !sortDir[col];
            rows.sort((a, b) => {{
                const aText = a.cells[col].textContent.toLowerCase();
                const bText = b.cells[col].textContent.toLowerCase();
                return sortDir[col] ? aText.localeCompare(bText) : bText.localeCompare(aText);
            }});
            rows.forEach(r => tbody.appendChild(r));
        }}
    </script>
</body>
</html>"""

    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  ✓ {short}: {filename} ({n_jobs} Jobs)")


# =============================================================================
# 6. ÜBERSICHTSSEITE (Ebene 1)
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
        "avg_skills": subset[skill_cols].sum(axis=1).mean(),
        "avg_tech": subset["Fachdetail_Score"].mean(),
        "file": profil_files[profil_name],
    })

# Sortiere nach Anzahl
profil_stats.sort(key=lambda x: -x["count"])

# Sunburst-Chart
fig = go.Figure(go.Sunburst(
    labels=[ps["short"] for ps in profil_stats],
    parents=[""] * len(profil_stats),
    values=[ps["count"] for ps in profil_stats],
    marker=dict(colors=[ps["color"] for ps in profil_stats]),
    textinfo="label+value+percent root",
    hovertemplate="<b>%{label}</b><br>%{value} Stellen (%{percentRoot:.1%})<extra></extra>",
    insidetextorientation="radial",
))
fig.update_layout(
    margin=dict(t=10, l=10, r=10, b=10),
    height=450,
)
sunburst_html = fig.to_html(full_html=False, include_plotlyjs=False)

# Profil-Karten
cards_html = ""
for ps in profil_stats:
    cards_html += f"""
    <a href="{ps['file']}" class="profil-card" style="border-top: 4px solid {ps['color']};">
        <div class="profil-card-header">
            <span class="profil-dot" style="background:{ps['color']};"></span>
            <h3>{ps['short']}</h3>
        </div>
        <div class="profil-stats">
            <div><span class="num">{ps['count']}</span><span class="label">Stellen</span></div>
            <div><span class="num">{ps['avg_skills']:.0f}</span><span class="label">Ø Skills</span></div>
            <div><span class="num">{ps['avg_tech']:.1f}</span><span class="label">Ø TechScore</span></div>
        </div>
        <div class="profil-cta">Stellen anzeigen →</div>
    </a>"""

index_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MBI Career Explorer</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5; color: #333;
        }}
        .hero {{
            background: linear-gradient(135deg, #1a237e, #283593);
            color: white; padding: 50px 40px; text-align: center;
        }}
        .hero h1 {{ font-size: 36px; margin-bottom: 10px; }}
        .hero p {{ font-size: 18px; opacity: 0.85; max-width: 700px; margin: 0 auto; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 30px; }}

        .section-title {{
            font-size: 22px; font-weight: 700; margin-bottom: 20px;
            color: #1a237e;
        }}

        .overview-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 30px;
            margin-bottom: 40px;
        }}
        .chart-card {{
            background: white; border-radius: 12px; padding: 25px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}

        .profil-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}
        .profil-card {{
            display: block; background: white; border-radius: 12px;
            padding: 25px; text-decoration: none; color: #333;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s; cursor: pointer;
        }}
        .profil-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        .profil-card-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; }}
        .profil-card-header h3 {{ font-size: 17px; }}
        .profil-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
        .profil-stats {{
            display: grid; grid-template-columns: repeat(3, 1fr);
            gap: 10px; margin-bottom: 15px;
        }}
        .profil-stats div {{ text-align: center; }}
        .profil-stats .num {{ display: block; font-size: 22px; font-weight: 700; }}
        .profil-stats .label {{ font-size: 11px; color: #888; }}
        .profil-cta {{
            color: #1a237e; font-weight: 600; font-size: 14px;
            padding-top: 10px; border-top: 1px solid #f0f0f0;
        }}

        .info-box {{
            background: #e8eaf6; border-radius: 8px; padding: 15px 20px;
            margin-bottom: 25px; font-size: 14px; line-height: 1.5;
        }}
        .info-box strong {{ color: #1a237e; }}

        @media (max-width: 700px) {{
            .overview-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>🎓 MBI Career Explorer</h1>
        <p>Interaktive Analyse von {len(df_jobs)} Stelleninseraten –
           zugeordnet zu den 6 Profilen des MBI-Studiengangs.
           Klicke auf ein Profil, um passende Jobs, Skills und Kursempfehlungen zu sehen.</p>
    </div>

    <div class="container">
        <div class="info-box">
            <strong>So funktioniert's:</strong> Klicke auf eines der 6 Profile unten.
            Auf der Profilseite siehst du alle zugehörigen Stellen.
            Klicke dort auf einen Job, um die benötigten Skills, passende MBI-Kurse
            und allfällige Skill-Gaps zu sehen.
        </div>

        <div class="overview-grid">
            <div class="chart-card">
                <h2 class="section-title">Verteilung der Stelleninserate</h2>
                {sunburst_html}
            </div>
            <div class="chart-card" style="display:flex; flex-direction:column; justify-content:center;">
                <h2 class="section-title">Kennzahlen</h2>
                <table style="width:100%; font-size:14px; border-collapse:collapse;">
                    <tr style="border-bottom:2px solid #e0e0e0;">
                        <th style="text-align:left; padding:8px;">Profil</th>
                        <th style="text-align:right; padding:8px;">Stellen</th>
                        <th style="text-align:right; padding:8px;">Ø Skills</th>
                        <th style="text-align:right; padding:8px;">Ø TechScore</th>
                    </tr>
                    {"".join(f'''
                    <tr style="border-bottom:1px solid #f0f0f0;">
                        <td style="padding:8px;"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{ps['color']};margin-right:6px;"></span>{ps['short']}</td>
                        <td style="text-align:right;padding:8px;font-weight:600;">{ps['count']}</td>
                        <td style="text-align:right;padding:8px;">{ps['avg_skills']:.0f}</td>
                        <td style="text-align:right;padding:8px;">{ps['avg_tech']:.1f}</td>
                    </tr>''' for ps in profil_stats)}
                    <tr style="border-top:2px solid #e0e0e0; font-weight:700;">
                        <td style="padding:8px;">Total</td>
                        <td style="text-align:right;padding:8px;">{len(df_jobs)}</td>
                        <td style="text-align:right;padding:8px;">{df_jobs[skill_cols].sum(axis=1).mean():.0f}</td>
                        <td style="text-align:right;padding:8px;">{df_jobs['Fachdetail_Score'].mean():.1f}</td>
                    </tr>
                </table>
            </div>
        </div>

        <h2 class="section-title">Profile erkunden</h2>
        <div class="profil-grid">
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
print("INTERAKTIVER EXPLORER ERSTELLT!")
print(f"{'='*60}")
print(f"\n  Öffne im Browser: {os.path.abspath(index_path)}")
print(f"\n  Dateien in '{OUT_DIR}/':")
print(f"    index.html                (Übersichtsseite)")
for ps in profil_stats:
    print(f"    {profil_files[ps['name']]:40s} ({ps['count']} Jobs)")
