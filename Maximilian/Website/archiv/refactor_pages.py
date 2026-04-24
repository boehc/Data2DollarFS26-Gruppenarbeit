#!/usr/bin/env python3
"""
refactor_pages.py — Wandelt interactive_explorer/ → interactive_explorer_v2/
in das Premium-Light-Design um.

Kernidee:
- Body extrahieren, <style>-Blöcke + alte .page-header + alte kpi-grid
  entfernen, Plotly-Fonts (Inter) → DM Sans ersetzen.
- Einheitliche <nav>, Breadcrumb, Profile-Hero (inkl. KPIs) voranstellen.
- Einheitlichen <footer> anhängen.
"""
import re
from pathlib import Path

SRC = Path(__file__).parent / "interactive_explorer"
DST = Path(__file__).parent / "interactive_explorer_v2"

# ----------------------------------------------------------------------
PROFILES = {
    "profil_transforming_managing_digital_business.html": {
        "name": "Digital Business", "subtitle": "Transforming & Managing Digital Business",
        "color": "#475569", "tint": "#F1F5F9", "stats": "651 Stellen · 55% der Inserate",
    },
    "profil_technology_solution_architect.html": {
        "name": "Tech Architect", "subtitle": "Technology Solution Architect",
        "color": "#2563EB", "tint": "#EFF6FF", "stats": "204 Stellen · 17%",
    },
    "profil_business_development.html": {
        "name": "Business Dev.", "subtitle": "Business Development",
        "color": "#059669", "tint": "#ECFDF5", "stats": "129 Stellen · 11%",
    },
    "profil_supply_chain_operations_management.html": {
        "name": "Supply Chain", "subtitle": "Supply Chain & Operations Management",
        "color": "#DC2626", "tint": "#FEF2F2", "stats": "82 Stellen · 7%",
    },
    "profil_digital_channel_crm.html": {
        "name": "Digital Channel", "subtitle": "Digital Channel & CRM",
        "color": "#7C3AED", "tint": "#F5F3FF", "stats": "66 Stellen · 6%",
    },
    "profil_start_up_scale_up_entrepreneurship.html": {
        "name": "Startup & Scale-up", "subtitle": "Startup, Scale-up & Entrepreneurship",
        "color": "#D97706", "tint": "#FFFBEB", "stats": "62 Stellen · 5%",
    },
}

HEAD_LINKS = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/base.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/nav.css">
    <link rel="stylesheet" href="css/pages.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="js/nav.js" defer></script>"""

NAV_HTML = """    <header class="nav">
      <div class="nav-inner">
        <a href="index.html" class="nav-logo" aria-label="MBI Explorer – Home">
          <span class="nav-logo-mark">M</span>
          <span class="nav-logo-text">
            MBI Explorer
            <small>Career Intelligence</small>
          </span>
        </a>
        <nav class="nav-links" aria-label="Hauptnavigation">
          <a href="index.html" class="nav-link">Übersicht</a>
          <a href="index.html#profile" class="nav-link">Profile</a>
          <a href="index.html#how" class="nav-link">So funktioniert's</a>
        </nav>
        <div class="nav-cta">
          <a href="index.html#profile" class="btn btn-primary btn-sm">Profil wählen</a>
          <button class="nav-toggle" aria-label="Menü" aria-expanded="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
        </div>
      </div>
    </header>
"""

FOOTER_HTML = """    <footer class="footer">
      <div class="container-wide">
        <div class="footer-grid">
          <div class="footer-brand">
            <a href="index.html" class="nav-logo">
              <span class="nav-logo-mark">M</span>
              <span class="nav-logo-text">
                MBI Explorer
                <small>Career Intelligence</small>
              </span>
            </a>
            <p>Interaktive Analyse von 1'194 Stelleninseraten, zugeordnet zu den 6 Vertiefungsprofilen des MBI-Studiengangs der FHNW.</p>
          </div>
          <div class="footer-col">
            <h5>Navigation</h5>
            <ul>
              <li><a href="index.html">Übersicht</a></li>
              <li><a href="index.html#profile">Profile</a></li>
              <li><a href="index.html#how">So funktioniert's</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h5>Profile</h5>
            <ul>
              <li><a href="profil_transforming_managing_digital_business.html">Digital Business</a></li>
              <li><a href="profil_technology_solution_architect.html">Tech Architect</a></li>
              <li><a href="profil_business_development.html">Business Dev.</a></li>
              <li><a href="profil_supply_chain_operations_management.html">Supply Chain</a></li>
              <li><a href="profil_digital_channel_crm.html">Digital Channel</a></li>
              <li><a href="profil_start_up_scale_up_entrepreneurship.html">Startup & Scale-up</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <div>© 2026 MBI Explorer · Data2Dollar FS26 · FHNW</div>
          <div>Built with care · Maximilian</div>
        </div>
      </div>
    </footer>
"""


def build_head(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
{HEAD_LINKS}
</head>
"""


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def extract_body_inner(html: str) -> str:
    m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("<body> not found")
    return m.group(1)


def plotly_fonts_to_dmsans(html: str) -> str:
    """Plotly-Charts auf DM Sans umstellen (statt Inter)."""
    # JSON-String-Variante
    html = html.replace('"Inter, -apple-system, sans-serif"', '"DM Sans, sans-serif"')
    html = html.replace('"Inter, sans-serif"', '"DM Sans, sans-serif"')
    # Light greys to match premium palette
    html = html.replace('"#f1f5f9"', '"#EEEAE2"')  # gridline warm
    return html


def extract_balanced_div(html: str, open_pattern: str):
    """Findet `<div class="…">` (per Regex) und liefert den *balanced*
    inneren Content bis zum passenden `</div>` – zählt dabei verschachtelte
    `<div>`s korrekt. Gibt (inner, start, end) zurück oder None.
    """
    m = re.search(open_pattern, html)
    if not m:
        return None
    # Position nach dem `>` des öffnenden <div …>
    i = m.end()
    depth = 1
    n = len(html)
    # Suche iterativ nach <div ...> oder </div>
    tag_re = re.compile(r"<(/?)div\b[^>]*>", re.IGNORECASE)
    while i < n:
        tm = tag_re.search(html, i)
        if not tm:
            return None
        if tm.group(1) == "/":
            depth -= 1
            if depth == 0:
                inner = html[m.end(): tm.start()]
                return inner, m.start(), tm.end()
        else:
            depth += 1
        i = tm.end()
    return None


# ----------------------------------------------------------------------
# INDEX
# ----------------------------------------------------------------------
def rebuild_index(src_html: str, dst_path: Path) -> None:
    body = extract_body_inner(src_html)
    title = "MBI Explorer – Dein Weg vom Studium in den Arbeitsmarkt"

    # Plotly fonts
    body = plotly_fonts_to_dmsans(body)

    new_hero = """    <section class="hero">
      <div class="container">
        <div class="hero-inner">
          <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            MBI-Studiengang · FHNW · FS26
          </div>
          <h1>Dein Weg vom <em>Studium</em><br>in den Arbeitsmarkt.</h1>
          <p>Interaktive Analyse von 1'194 Stelleninseraten, zugeordnet zu den 6 Vertiefungsprofilen des MBI-Studiengangs.</p>
          <div class="hero-cta">
            <a href="#profile" class="btn btn-primary">Profile erkunden</a>
            <a href="#how" class="btn btn-ghost">So funktioniert's</a>
          </div>
          <div class="hero-stats">
            <div class="hero-stat"><div class="hero-stat-val">1'194</div><div class="hero-stat-lbl">Stelleninserate</div></div>
            <div class="hero-stat"><div class="hero-stat-val">6</div><div class="hero-stat-lbl">Vertiefungsprofile</div></div>
            <div class="hero-stat"><div class="hero-stat-val">14</div><div class="hero-stat-lbl">Ø Skills / Stelle</div></div>
            <div class="hero-stat"><div class="hero-stat-val">1.9</div><div class="hero-stat-lbl">Ø Tech-Stack</div></div>
          </div>
        </div>
      </div>
    </section>
"""

    new_how = """    <section id="how" class="section-sm">
      <div class="container">
        <div class="section-head left">
          <span class="eyebrow">So funktioniert's</span>
          <h2>In drei Schritten zu deinem Profil</h2>
        </div>
        <div class="how-grid">
          <div class="how-step"><div class="how-num">1</div><div class="how-title">Profil wählen</div><div class="how-desc">Wähle eines der 6 MBI-Vertiefungsprofile aus, die zu deinen Interessen passen.</div></div>
          <div class="how-step"><div class="how-num">2</div><div class="how-title">Stellen erkunden</div><div class="how-desc">Durchsuche passende Stelleninserate aus dem Schweizer Arbeitsmarkt.</div></div>
          <div class="how-step"><div class="how-num">3</div><div class="how-title">Skills & Kurse</div><div class="how-desc">Sieh benötigte Skills, passende MBI-Kurse und identifiziere deine Gaps.</div></div>
        </div>
      </div>
    </section>
"""

    # Extract .main content (chart + table + profile grid)
    main_match = re.search(r'<div class="main">(.*?)</div>\s*(?:</body>|$)',
                           body, re.DOTALL)
    if main_match:
        main_inner = main_match.group(1)
    else:
        main_inner = body

    # --- Overview (chart + Kennzahlen table) ---
    overview = extract_balanced_div(
        main_inner, r'<div\s+class="overview-grid"[^>]*>')
    overview_block = ""
    if overview:
        overview_inner, o_start, o_end = overview
        overview_block = f"""    <section id="market" class="section-tight">
      <div class="container">
        <div class="section-head left">
          <span class="eyebrow">Marktüberblick</span>
          <h2>Verteilung nach Profil</h2>
          <p>Wie sich die 1'194 Stellen auf die 6 MBI-Vertiefungsprofile aufteilen.</p>
        </div>
        <div class="overview-grid">{overview_inner}</div>
      </div>
    </section>
"""
        main_inner = main_inner[:o_start] + main_inner[o_end:]

    # --- Profile grid ---
    pg = extract_balanced_div(
        main_inner, r'<div\s+class="profile-grid"[^>]*>')
    profile_block = ""
    if pg:
        profile_inner, _, _ = pg
        profile_block = f"""    <section id="profile" class="section-lg">
      <div class="container">
        <div class="section-head left">
          <span class="eyebrow">Profile</span>
          <h2>Welches Profil passt zu dir?</h2>
          <p>Wähle ein Vertiefungsprofil, um die zugehörigen Stelleninserate, Skills und MBI-Kurse zu erkunden.</p>
        </div>
        <div class="profile-grid">{profile_inner}</div>
      </div>
    </section>
"""

    out = build_head(title) + "<body>\n"
    out += NAV_HTML
    out += new_hero
    out += new_how
    out += overview_block
    out += profile_block
    out += FOOTER_HTML
    out += "</body>\n</html>\n"

    dst_path.write_text(out, encoding="utf-8")
    print(f"  ✓ {dst_path.name}")


# ----------------------------------------------------------------------
# PROFILE PAGES
# ----------------------------------------------------------------------
def extract_kpis(body: str):
    """Parse (value, label) from old .kpi-grid."""
    kpis = []
    for m in re.finditer(
        r'<div class="kpi-card">\s*<div class="kpi-value">([^<]+)</div>\s*<div class="kpi-label">([^<]+)</div>',
        body):
        kpis.append((m.group(1).strip(), m.group(2).strip()))
    return kpis


def rebuild_profile(src_html: str, dst_path: Path, key: str) -> None:
    cfg = PROFILES[key]
    body = extract_body_inner(src_html)

    # Plotly fonts → DM Sans
    body = plotly_fonts_to_dmsans(body)

    # 1) Remove original <header class="page-header">...</header>
    body = re.sub(r'<header\s+class="page-header">.*?</header>\s*',
                  '', body, count=1, flags=re.DOTALL)

    # 2) Extract KPIs
    kpis = extract_kpis(body)

    # 3) Remove original kpi-grid (we'll show KPIs in the hero instead).
    #    Simplest: drop everything between <!-- KPIs --> and <!-- Chart -->.
    body = re.sub(
        r'<!--\s*KPIs\s*-->.*?(?=<!--\s*Chart)',
        '', body, count=1, flags=re.DOTALL)

    # 4) Find and unwrap outermost <div class="container">...</div>
    # We just strip the first opening "<div class=\"container\">" (with optional whitespace)
    # and the last "</div>" before the overlay/panel.
    body = re.sub(r'<div class="container">\s*', '', body, count=1)
    # The matching closing </div> is right before <!-- Overlay + Detail Panel -->
    body = re.sub(r'</div>\s*(?=<!--\s*Overlay)', '', body, count=1)

    title = f"{cfg['name']} – MBI Explorer"

    # Build KPI HTML
    kpi_html = ""
    if kpis:
        items = "".join(
            f'<div class="profile-kpi"><div class="profile-kpi-val">{v}</div>'
            f'<div class="profile-kpi-lbl">{l}</div></div>'
            for v, l in kpis)
        kpi_html = f'        <div class="profile-kpis">{items}</div>\n'

    breadcrumb = f"""    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">MBI Explorer</a>
        <span class="breadcrumb-sep">/</span>
        <a href="index.html#profile">Profile</a>
        <span class="breadcrumb-sep">/</span>
        <span class="breadcrumb-current">{cfg['name']}</span>
      </nav>
    </div>
"""

    profile_hero = f"""    <section class="profile-hero" style="--profile-color:{cfg['color']};--profile-tint:{cfg['tint']};">
      <div class="container">
        <div class="profile-hero-tag">
          <span class="profile-hero-dot" style="background:{cfg['color']};"></span>
          {cfg['stats']}
        </div>
        <h1>{cfg['subtitle']}</h1>
        <p>Stelleninserate, Skills und passende MBI-Kurse für das Vertiefungsprofil <strong>{cfg['name']}</strong>.</p>
{kpi_html}      </div>
    </section>
"""

    out = build_head(title) + "<body>\n"
    out += NAV_HTML
    out += breadcrumb
    out += profile_hero
    out += f'    <section class="profile-content section-tight" style="--profile-color:{cfg["color"]};--profile-tint:{cfg["tint"]};"><div class="container">\n'
    out += body.strip() + "\n"
    out += '    </div></section>\n'
    out += FOOTER_HTML
    out += "</body>\n</html>\n"

    dst_path.write_text(out, encoding="utf-8")
    print(f"  ✓ {dst_path.name}")


# ----------------------------------------------------------------------
def main():
    print(f"Source: {SRC}")
    print(f"Target: {DST}\n")

    print("Index:")
    rebuild_index((SRC / "index.html").read_text(encoding="utf-8"),
                  DST / "index.html")

    print("\nProfiles:")
    for fname in PROFILES:
        src_file = SRC / fname
        if not src_file.exists():
            print(f"  ✗ {fname} (missing)")
            continue
        rebuild_profile(src_file.read_text(encoding="utf-8"),
                        DST / fname, fname)

    print("\n✓ Done.")


if __name__ == "__main__":
    main()
