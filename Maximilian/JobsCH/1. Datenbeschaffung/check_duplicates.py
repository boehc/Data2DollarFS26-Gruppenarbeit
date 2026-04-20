"""Prüft, wie viele einzigartige Job-URLs es über alle Suchseiten gibt."""
import re
import subprocess
import time
from urllib.parse import quote, urlencode

BASE = "https://www.jobs.ch/de/stellenangebote/"
PARAMS = {
    "employment-grade-min": "80",
    "employment-grade-max": "100",
    "employment-type": "5",
    "term": (
        "abschluss: mbi hsg business innovation\n"
        'position: "junior" oder "entry level" oder "trainee" '
        'oder "graduate" oder "hochschulabsolvent"\n'
        "suche: business development, digital crm, start-up & scale-up, "
        "technology solution architecture, digital transformation "
        "und supply chain management\n"
    ),
}

all_links = []
unique_links = set()

for page in range(1, 43):
    params = dict(PARAMS)
    if page > 1:
        params["page"] = str(page)
    url = f"{BASE}?{urlencode(params, quote_via=quote)}"

    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
             url],
            capture_output=True, text=True, timeout=20
        )
        html = result.stdout
        links = re.findall(r'href="(/de/stellenangebote/detail/[^"]+)"', html)
        page_unique = set(links)
        new_links = page_unique - unique_links
        all_links.extend(page_unique)
        unique_links.update(page_unique)
        print(
            f"Seite {page:2d}: {len(page_unique):3d} Links, "
            f"davon {len(new_links):3d} NEU "
            f"(total unique: {len(unique_links)})"
        )
    except Exception as e:
        print(f"Seite {page:2d}: FEHLER - {e}")

    time.sleep(0.5)

print(f"\n=== ZUSAMMENFASSUNG ===")
print(f"Links gesamt (inkl. Duplikate): {len(all_links)}")
print(f"Einzigartige Links:             {len(unique_links)}")
print(f"Duplikate entfernt:             {len(all_links) - len(unique_links)}")
