"""
===============================================================================
INTERAKTIVE MBI CAREER EXPLORER v2
===============================================================================
Verbesserungen gegenüber v1:
  - Schliessbares Detail-Panel mit X-Button + Overlay
  - Ohne Firma/Ort-Spalten (nur Jobtitel + Badges)
  - Übersichtlichere Skills-Darstellung mit farbigen Chips pro Kategorie
  - Besseres Responsive-Design und Animationen

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

CAT_COLORS = {
    "Fachkompetenz":      "#2196F3",
    "TechSkill":          "#FF5722",
    "Sozialkompetenz":    "#4CAF50",
    "Methodenkompetenz":  "#FF9800",
    "Personalkompetenz":  "#E91E63",
}
CAT_BG = {
    "Fachkompetenz":      "#e3f2fd",
    "TechSkill":          "#fbe9e7",
    "Sozialkompetenz":    "#e8f5e9",
    "Methodenkompetenz":  "#fff3e0",
    "Personalkompetenz":  "#fce4ec",
}
CAT_ICONS = {
    "Fachkompetenz": "🎓", "TechSkill": "💻",
    "Sozialkompetenz": "🤝", "Methodenkompetenz": "📋",
    "Personalkompetenz": "💡",
}


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
# 5. SKILL-CHIPS HTML BUILDER
# =============================================================================
def build_skill_chips(skill_list):
    """Erzeugt farbige Chips pro Kategorie, gruppiert in Boxen."""
    by_cat = {}
    for s in skill_list:
        cat = categorize_skill(s)
        by_cat.setdefault(cat, []).append(clean_skill(s))

    if not by_cat:
        return "<p class='empty-msg'>Keine Skills erkannt</p>"

    html_parts = []
    for cat in ["Fachkompetenz", "TechSkill", "Sozialkompetenz", "Methodenkompetenz", "Personalkompetenz"]:
        if cat not in by_cat:
            continue
        icon = CAT_ICONS[cat]
        color = CAT_COLORS[cat]
        bg = CAT_BG[cat]
        chips = "".join(
            f"<span class='chip' style='background:{bg};color:{color};border:1px solid {color}30;'>{name}</span>"
            for name in by_cat[cat]
        )
        html_parts.append(
            f"<div class='skill-group'>"
            f"<div class='skill-group-label' style='color:{color};'>{icon} {cat}</div>"
            f"<div class='chip-wrap'>{chips}</div>"
            f"</div>"
        )
    return "".join(html_parts)


def build_courses_html(courses):
    if not courses:
        return "<p class='empty-msg'>Keine passenden Kurse gefunden</p>"
    lines = []
    for cname, covered, count in courses:
        covered_chips = "".join(
            f"<span class='chip chip-sm'>{clean_skill(s)}</span>"
            for s in covered[:5]
        )
        lines.append(
            f"<div class='course-item'>"
            f"<div class='course-name'>📚 {html_lib.escape(cname)}</div>"
            f"<div class='course-covers'>Deckt ab: {covered_chips}</div>"
            f"</div>"
        )
    return "".join(lines)


def build_gaps_html(gaps):
    if not gaps:
        return "<div class='gaps-ok'>✅ Alle Skills durch MBI-Kurse abgedeckt!</div>"
    chips = "".join(
        f"<span class='chip chip-gap'>⚠️ {clean_skill(g)}</span>"
        for g in gaps
    )
    return f"<div class='chip-wrap'>{chips}</div>"


# =============================================================================
# 6. PROFIL-SEITEN (Ebene 2 + 3)
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

    # Top-Skills Barplot
    skill_freq = profil_jobs[skill_cols].mean() * 100
    top_skills = skill_freq.sort_values(ascending=False).head(15)

    fig_skills = go.Figure()
    bar_colors = [CAT_COLORS.get(categorize_skill(s), "#999") for s in top_skills.index]

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
    skills_chart_html = fig_skills.to_html(full_html=False, include_plotlyjs=False)

    # Tabellenzeilen (nur Jobtitel + Badges)
    table_rows = []
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
            f"<h4>🎯 Benötigte Skills ({n_skills})</h4>"
            f"{skills_html}"
            f"</div>"
            f"<div class='panel-section'>"
            f"<h4>📚 Empfohlene MBI-Kurse ({n_courses})</h4>"
            f"{courses_html}"
            f"</div>"
            f"<div class='panel-section'>"
            f"<h4>🔧 Selbst zu erwerben (max. 3)</h4>"
            f"{gaps_html}"
            f"</div>"
        )

        gap_badge = (
            f"<span class='badge badge-gaps'>{n_gaps} Gaps</span>"
            if n_gaps > 0
            else "<span class='badge badge-ok'>✓</span>"
        )

        table_rows.append(
            f"<tr class='job-row' data-panel=\"{html_lib.escape(panel_content)}\" "
            f"data-title=\"{html_lib.escape(title_text)}\">"
            f"<td class='job-title'>{title_text}</td>"
            f"<td class='badge-cell'>"
            f"<span class='badge badge-skills'>{n_skills} Skills</span>"
            f"<span class='badge badge-courses'>{n_courses} Kurse</span>"
            f"{gap_badge}"
            f"</td>"
            f"</tr>"
        )

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
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa; color: #333;
        }}

        /* ── Header ── */
        .header {{
            background: linear-gradient(135deg, {color}ee, {color}bb);
            color: white; padding: 32px 40px; position: relative;
            box-shadow: 0 2px 16px {color}44;
        }}
        .header h1 {{ font-size: 26px; margin-bottom: 4px; font-weight: 700; }}
        .header p {{ opacity: 0.9; font-size: 15px; }}
        .back-link {{
            position: absolute; top: 22px; right: 30px;
            color: white; text-decoration: none; font-size: 13px;
            background: rgba(255,255,255,0.18); padding: 8px 18px;
            border-radius: 8px; transition: background 0.2s; backdrop-filter: blur(4px);
        }}
        .back-link:hover {{ background: rgba(255,255,255,0.32); }}

        /* ── Layout ── */
        .container {{ max-width: 1400px; margin: 0 auto; padding: 28px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }}
        .card {{
            background: white; border-radius: 14px; padding: 24px;
            box-shadow: 0 1px 8px rgba(0,0,0,0.06); border: 1px solid #e8ecf0;
        }}
        .card h2 {{ font-size: 16px; margin-bottom: 14px; color: #555; font-weight: 600; }}

        .stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
        .stat-box {{
            background: #f8f9fb; border-radius: 10px; padding: 16px; text-align: center;
            border: 1px solid #eef0f4;
        }}
        .stat-box .num {{ font-size: 28px; font-weight: 800; color: {color}; }}
        .stat-box .label {{ font-size: 11px; color: #999; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.5px; }}

        /* ── Search ── */
        .search-bar {{
            width: 100%; padding: 12px 20px; font-size: 15px;
            border: 2px solid #e4e8ec; border-radius: 10px;
            margin-bottom: 16px; outline: none; transition: all 0.2s;
            background: #fafbfc;
        }}
        .search-bar:focus {{ border-color: {color}; background: white; box-shadow: 0 0 0 3px {color}18; }}

        /* ── Table ── */
        .table-wrap {{ overflow-x: auto; }}
        .jobs-table {{
            width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px;
        }}
        .jobs-table thead th {{
            background: #f5f7fa; padding: 11px 16px; text-align: left;
            border-bottom: 2px solid #e4e8ec; position: sticky; top: 0; z-index: 2;
            cursor: pointer; user-select: none; font-weight: 600; color: #666;
            font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px;
        }}
        .jobs-table thead th:hover {{ background: #eceef2; }}
        .jobs-table tbody tr {{
            transition: all 0.15s; cursor: pointer;
        }}
        .jobs-table tbody tr:hover {{ background: #f0f5ff; }}
        .jobs-table tbody tr.active {{ background: {color}12; }}
        .jobs-table td {{ padding: 11px 16px; border-bottom: 1px solid #f2f4f6; }}
        .job-title {{ font-weight: 600; color: #222; }}

        /* ── Badges ── */
        .badge-cell {{ white-space: nowrap; text-align: right; }}
        .badge {{
            display: inline-block; padding: 4px 10px; border-radius: 20px;
            font-size: 11px; font-weight: 600; margin-left: 5px;
        }}
        .badge-skills {{ background: #e3f2fd; color: #1565c0; }}
        .badge-courses {{ background: #f3e5f5; color: #7b1fa2; }}
        .badge-gaps {{ background: #fff3e0; color: #e65100; }}
        .badge-ok {{ background: #e8f5e9; color: #2e7d32; }}

        /* ── Overlay + Detail Panel ── */
        .overlay {{
            display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.35);
            z-index: 999; backdrop-filter: blur(2px);
            animation: fadeIn 0.2s ease;
        }}
        .overlay.visible {{ display: block; }}

        .detail-panel {{
            display: none; position: fixed; right: 0; top: 0;
            width: 480px; height: 100vh;
            background: white; z-index: 1000;
            box-shadow: -8px 0 40px rgba(0,0,0,0.15);
            overflow-y: auto;
            animation: slideIn 0.25s ease;
        }}
        .detail-panel.visible {{ display: block; }}

        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }} to {{ opacity: 1; }}
        }}

        .panel-header {{
            position: sticky; top: 0; z-index: 10;
            background: {color}; color: white;
            padding: 20px 24px; display: flex; align-items: flex-start;
            justify-content: space-between; gap: 12px;
        }}
        .panel-header h3 {{
            font-size: 16px; font-weight: 700; line-height: 1.3; flex: 1;
        }}
        .close-btn {{
            background: rgba(255,255,255,0.2); border: none; color: white;
            width: 32px; height: 32px; border-radius: 8px; cursor: pointer;
            font-size: 18px; display: flex; align-items: center; justify-content: center;
            flex-shrink: 0; transition: background 0.15s;
        }}
        .close-btn:hover {{ background: rgba(255,255,255,0.35); }}

        .panel-body {{ padding: 20px 24px 40px; }}

        .panel-section {{ margin-bottom: 22px; }}
        .panel-section h4 {{
            font-size: 13px; font-weight: 700; color: #444;
            margin-bottom: 10px; padding-bottom: 6px;
            border-bottom: 2px solid #f0f2f5;
        }}

        /* ── Skill Chips ── */
        .skill-group {{ margin-bottom: 12px; }}
        .skill-group-label {{
            font-size: 11px; font-weight: 700; margin-bottom: 5px;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .chip-wrap {{ display: flex; flex-wrap: wrap; gap: 5px; }}
        .chip {{
            display: inline-block; padding: 4px 10px; border-radius: 6px;
            font-size: 12px; font-weight: 500; white-space: nowrap;
        }}
        .chip-sm {{
            font-size: 11px; padding: 2px 7px; background: #f0f2f5;
            color: #555; border-radius: 4px;
        }}
        .chip-gap {{
            background: #fff3e0; color: #e65100; border: 1px solid #ffcc80;
        }}

        /* ── Courses ── */
        .course-item {{
            background: #fafbfc; border: 1px solid #eef0f4; border-radius: 10px;
            padding: 12px 14px; margin-bottom: 8px;
        }}
        .course-name {{ font-weight: 600; font-size: 13px; margin-bottom: 5px; color: #333; }}
        .course-covers {{ font-size: 11px; color: #777; }}
        .course-covers .chip-sm {{ margin-top: 3px; }}

        .gaps-ok {{
            background: #e8f5e9; color: #2e7d32; padding: 12px 16px;
            border-radius: 10px; font-weight: 600; font-size: 13px;
        }}
        .empty-msg {{ color: #aaa; font-size: 13px; font-style: italic; }}

        /* ── Legende ── */
        .legend {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; font-size: 11px; color: #777; }}
        .legend-dot {{ width: 8px; height: 8px; border-radius: 3px; }}

        @media (max-width: 900px) {{
            .grid {{ grid-template-columns: 1fr; }}
            .detail-panel {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{profil_name}</h1>
        <p>{n_jobs} Stelleninserate aus dem Arbeitsmarkt</p>
        <a href="index.html" class="back-link">← Übersicht</a>
    </div>

    <div class="container">
        <div class="grid">
            <div class="card">
                <h2>Profil auf einen Blick</h2>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="num">{n_jobs}</div>
                        <div class="label">Stellen</div>
                    </div>
                    <div class="stat-box">
                        <div class="num">{profil_jobs[skill_cols].sum(axis=1).mean():.1f}</div>
                        <div class="label">Ø Skills / Job</div>
                    </div>
                    <div class="stat-box">
                        <div class="num">{profil_jobs['Fachdetail_Score'].mean():.1f}</div>
                        <div class="label">Ø TechScore</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <h2>Top 15 gefragte Skills</h2>
                {skills_chart_html}
            </div>
        </div>

        <div class="card">
            <h2>Stellen in diesem Profil</h2>
            <input type="text" class="search-bar" id="searchInput"
                   placeholder="🔍 Jobtitel durchsuchen...">
            <div class="legend">
                <div class="legend-item"><span class="legend-dot" style="background:#1565c0;"></span> Skills</div>
                <div class="legend-item"><span class="legend-dot" style="background:#7b1fa2;"></span> Kursempfehlungen</div>
                <div class="legend-item"><span class="legend-dot" style="background:#e65100;"></span> Skill-Gaps</div>
                <div class="legend-item"><span class="legend-dot" style="background:#2e7d32;"></span> Vollständig abgedeckt</div>
            </div>
            <div class="table-wrap">
                <table class="jobs-table" id="jobsTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">Jobtitel ↕</th>
                            <th style="text-align:right;" onclick="sortTable(1)">Übersicht ↕</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_html}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Overlay + Detail-Seitenpanel -->
    <div class="overlay" id="overlay"></div>
    <div class="detail-panel" id="detailPanel">
        <div class="panel-header">
            <h3 id="panelTitle">–</h3>
            <button class="close-btn" id="closeBtn" title="Schliessen">✕</button>
        </div>
        <div class="panel-body" id="panelBody"></div>
    </div>

    <script>
        // ── Suche ──
        document.getElementById('searchInput').addEventListener('input', function() {{
            const q = this.value.toLowerCase();
            document.querySelectorAll('#jobsTable tbody tr').forEach(r => {{
                r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none';
            }});
        }});

        // ── Panel öffnen ──
        document.querySelectorAll('.job-row').forEach(row => {{
            row.addEventListener('click', function() {{
                document.getElementById('panelTitle').textContent = this.dataset.title;
                document.getElementById('panelBody').innerHTML = this.dataset.panel;
                document.getElementById('detailPanel').classList.add('visible');
                document.getElementById('overlay').classList.add('visible');
                document.querySelectorAll('.job-row').forEach(r => r.classList.remove('active'));
                this.classList.add('active');
            }});
        }});

        // ── Panel schliessen ──
        function closePanel() {{
            document.getElementById('detailPanel').classList.remove('visible');
            document.getElementById('overlay').classList.remove('visible');
            document.querySelectorAll('.job-row').forEach(r => r.classList.remove('active'));
        }}
        document.getElementById('closeBtn').addEventListener('click', closePanel);
        document.getElementById('overlay').addEventListener('click', closePanel);
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closePanel();
        }});

        // ── Sortierung ──
        let sortDir = [true, true];
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
# 7. ÜBERSICHTSSEITE (Ebene 1)
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

profil_stats.sort(key=lambda x: -x["count"])

# Sunburst
fig = go.Figure(go.Sunburst(
    labels=[ps["short"] for ps in profil_stats],
    parents=[""] * len(profil_stats),
    values=[ps["count"] for ps in profil_stats],
    marker=dict(colors=[ps["color"] for ps in profil_stats]),
    textinfo="label+value+percent root",
    hovertemplate="<b>%{label}</b><br>%{value} Stellen (%{percentRoot:.1%})<extra></extra>",
    insidetextorientation="radial",
))
fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=450)
sunburst_html = fig.to_html(full_html=False, include_plotlyjs=False)

# Profil-Karten
cards_html = ""
for ps in profil_stats:
    cards_html += f"""
    <a href="{ps['file']}" class="profil-card" style="--accent:{ps['color']};">
        <div class="profil-card-top">
            <span class="profil-dot" style="background:{ps['color']};"></span>
            <h3>{ps['short']}</h3>
        </div>
        <div class="profil-stats">
            <div><span class="num" style="color:{ps['color']};">{ps['count']}</span><span class="label">Stellen</span></div>
            <div><span class="num" style="color:{ps['color']};">{ps['avg_skills']:.0f}</span><span class="label">Ø Skills</span></div>
            <div><span class="num" style="color:{ps['color']};">{ps['avg_tech']:.1f}</span><span class="label">Ø TechScore</span></div>
        </div>
        <div class="profil-cta">Stellen erkunden →</div>
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
            background: #f5f7fa; color: #333;
        }}
        .hero {{
            background: linear-gradient(135deg, #0d1b4a, #1b3a7b);
            color: white; padding: 56px 40px 48px; text-align: center;
        }}
        .hero h1 {{ font-size: 34px; margin-bottom: 10px; font-weight: 800; letter-spacing: -0.5px; }}
        .hero p {{ font-size: 16px; opacity: 0.8; max-width: 640px; margin: 0 auto; line-height: 1.5; }}

        .container {{ max-width: 1200px; margin: 0 auto; padding: 30px; }}
        .section-title {{ font-size: 20px; font-weight: 700; margin-bottom: 18px; color: #1a237e; }}

        .info-box {{
            background: white; border-left: 4px solid #3f51b5;
            border-radius: 8px; padding: 16px 20px; margin-bottom: 28px;
            font-size: 14px; line-height: 1.6; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        }}
        .info-box strong {{ color: #1a237e; }}

        .overview-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 36px; }}
        .chart-card {{
            background: white; border-radius: 14px; padding: 24px;
            box-shadow: 0 1px 8px rgba(0,0,0,0.06); border: 1px solid #e8ecf0;
        }}

        /* Table in overview */
        .overview-table {{ width: 100%; font-size: 14px; border-collapse: collapse; }}
        .overview-table th {{
            text-align: left; padding: 10px 12px; border-bottom: 2px solid #e0e0e0;
            font-size: 11px; text-transform: uppercase; color: #888; letter-spacing: 0.4px;
        }}
        .overview-table td {{ padding: 10px 12px; border-bottom: 1px solid #f2f4f6; }}
        .overview-table tr:last-child {{ font-weight: 700; }}
        .overview-table tr:last-child td {{ border-top: 2px solid #e0e0e0; }}
        .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; vertical-align: middle; }}

        .profil-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 18px;
        }}
        .profil-card {{
            display: block; background: white; border-radius: 14px;
            padding: 22px; text-decoration: none; color: #333;
            box-shadow: 0 1px 8px rgba(0,0,0,0.06);
            border: 1px solid #e8ecf0; border-top: 4px solid var(--accent);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .profil-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }}
        .profil-card-top {{ display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }}
        .profil-card-top h3 {{ font-size: 16px; font-weight: 700; }}
        .profil-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
        .profil-stats {{
            display: grid; grid-template-columns: repeat(3, 1fr);
            gap: 8px; margin-bottom: 14px;
        }}
        .profil-stats div {{ text-align: center; }}
        .profil-stats .num {{ display: block; font-size: 22px; font-weight: 800; }}
        .profil-stats .label {{ font-size: 10px; color: #999; text-transform: uppercase; letter-spacing: 0.4px; }}
        .profil-cta {{
            color: var(--accent); font-weight: 600; font-size: 13px;
            padding-top: 10px; border-top: 1px solid #f0f2f5;
        }}

        @media (max-width: 700px) {{ .overview-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>🎓 MBI Career Explorer</h1>
        <p>Interaktive Analyse von {len(df_jobs)} Stelleninseraten, zugeordnet zu den
           6 Vertiefungsprofilen des MBI-Studiengangs.</p>
    </div>

    <div class="container">
        <div class="info-box">
            <strong>So funktioniert's:</strong> Wähle eines der 6 Profile unten aus.
            Auf der Profilseite siehst du alle zugehörigen Stelleninserate.
            Klicke auf einen Job, um die benötigten Skills, passende MBI-Kurse
            und allfällige Skill-Gaps im Detail zu sehen.
        </div>

        <div class="overview-grid">
            <div class="chart-card">
                <h2 class="section-title">Verteilung</h2>
                {sunburst_html}
            </div>
            <div class="chart-card" style="display:flex; flex-direction:column; justify-content:center;">
                <h2 class="section-title">Kennzahlen</h2>
                <table class="overview-table">
                    <tr><th>Profil</th><th style="text-align:right;">Stellen</th><th style="text-align:right;">Ø Skills</th><th style="text-align:right;">Ø Tech</th></tr>
                    {"".join(f'''<tr>
                        <td><span class="dot" style="background:{ps['color']};"></span>{ps['short']}</td>
                        <td style="text-align:right;font-weight:600;">{ps['count']}</td>
                        <td style="text-align:right;">{ps['avg_skills']:.0f}</td>
                        <td style="text-align:right;">{ps['avg_tech']:.1f}</td>
                    </tr>''' for ps in profil_stats)}
                    <tr>
                        <td>Total</td>
                        <td style="text-align:right;">{len(df_jobs)}</td>
                        <td style="text-align:right;">{df_jobs[skill_cols].sum(axis=1).mean():.0f}</td>
                        <td style="text-align:right;">{df_jobs['Fachdetail_Score'].mean():.1f}</td>
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
print("INTERAKTIVER EXPLORER v2 ERSTELLT!")
print(f"{'='*60}")
print(f"\n  Öffne: {os.path.abspath(index_path)}")
print(f"\n  Dateien in '{OUT_DIR}/':")
print(f"    index.html")
for ps in profil_stats:
    print(f"    {profil_files[ps['name']]:45s} ({ps['count']} Jobs)")
