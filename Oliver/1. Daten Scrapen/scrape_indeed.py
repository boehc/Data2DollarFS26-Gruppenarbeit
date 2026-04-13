#!/usr/bin/env python3
"""
Indeed Job Scraper - Multiple Search Variations
================================================
Indeed requires login for page 2+ of search results.
This script works around that by using DIFFERENT search queries/filters
that each return a different first page of results.

Each variation returns ~15 results. With deduplication,
we collect unique jobs across all variations.

Usage:
    cd /Users/Oliver/Documents/Gruppenarbeit/indeed
    python3.12 scrape_indeed.py
"""

import csv
import os
import re
import time
import random
from urllib.parse import urlencode

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ── Config ──
BASE_URL = "https://ch.indeed.com/jobs"
CSV_FILE = "indeed_jobs.csv"
CSV_FIELDS = ["job_profil", "job_title", "company", "location",
              "requirements", "full_description", "job_url"]

# ── Deutschschweiz Standorte ──
LOCATIONS = [
    "Zürich, ZH",
    "Bern, BE",
    "Basel, BS",
    "Luzern, LU",
    "St. Gallen, SG",
    "Winterthur, ZH",
    "Zug, ZG",
    "Aarau, AG",
    "Baden, AG",
    "Schaffhausen, SH",
    "Thun, BE",
    "Olten, SO",
    "Chur, GR",
    "Solothurn, SO",
    "Biel, BE",
]

# ── Job Profiles: core keyword variations (applied per location) ──
JOB_PROFILES = {
    "Business Developer": [
        {"q": "business developer"},
        {"q": "business developer", "sort": "date"},
        {"q": "business development"},
        {"q": "business developer manager"},
        {"q": "business developer", "fromage": "14"},
        {"q": '"business developer"'},
        {"q": "title:business developer"},
    ],
    "Digital Channel & Relationship Manager": [
        {"q": "digital channel manager"},
        {"q": "relationship manager"},
        {"q": "digital relationship manager"},
        {"q": "channel manager"},
        {"q": "digital customer relationship"},
        {"q": '"relationship manager"'},
        {"q": "title:relationship manager"},
    ],
    "IT Manager": [
        {"q": "IT manager"},
        {"q": "IT manager", "sort": "date"},
        {"q": "IT project manager"},
        {"q": "head of IT"},
        {"q": "IT Leiter"},
        {"q": '"IT manager"'},
        {"q": "title:IT manager"},
    ],
    "Startup & Technology Entrepreneur": [
        {"q": "startup entrepreneur"},
        {"q": "technology entrepreneur"},
        {"q": "startup founder"},
        {"q": "startup manager"},
        {"q": "startup", "sort": "date"},
        {"q": "startup business"},
        {"q": "venture builder"},
        {"q": "title:startup"},
    ],
    "Supply Chain & Operations Manager": [
        {"q": "supply chain manager"},
        {"q": "operations manager"},
        {"q": "supply chain manager", "sort": "date"},
        {"q": "operations manager", "sort": "date"},
        {"q": "supply chain operations"},
        {"q": "logistics manager"},
        {"q": '"supply chain manager"'},
        {"q": "title:operations manager"},
    ],
}


def build_url(params):
    return BASE_URL + "?" + urlencode(params)


def load_existing_keys():
    keys = set()
    if not os.path.isfile(CSV_FILE):
        return keys
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("job_url", "")
            if "jk=" in url:
                keys.add(url.split("jk=")[-1].split("&")[0])
    return keys, reader.fieldnames if 'reader' in dir() else []


def is_blocked(driver):
    src = driver.page_source[:5000].lower()
    indicators = [
        "anfrage blockiert", "request blocked", "access denied",
        "erstellen sie jetzt ein konto",
        "melden sie sich an, um mehr als eine seite",
        "code in ihrem posteingang",
    ]
    return any(i in src for i in indicators)


def wait_for_cloudflare(driver, timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        title = driver.title.lower()
        src = driver.page_source[:2000].lower()
        if not any(c in title or c in src for c in
                   ["just a moment", "checking your browser", "challenge-platform"]):
            return
        time.sleep(1)


def dismiss_overlays(driver):
    for sel in ["#onetrust-accept-btn-handler", 'button[id*="accept"]',
                "#mosaic-desktopserpjapopup button"]:
        try:
            btn = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
            btn.click()
            time.sleep(0.5)
        except (TimeoutException, NoSuchElementException):
            continue


def extract_cards(driver, seen_keys):
    cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
    total = len(cards)
    infos = []
    for card in cards:
        try:
            job_key = None
            try:
                link = card.find_element(
                    By.CSS_SELECTOR, "h2.jobTitle a[data-jk], a.jcs-JobTitle[data-jk]")
                job_key = link.get_attribute("data-jk")
            except NoSuchElementException:
                try:
                    link = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                    lid = link.get_attribute("id") or ""
                    if "_" in lid:
                        job_key = lid.split("_", 1)[1]
                except NoSuchElementException:
                    pass

            if not job_key or job_key in seen_keys:
                continue
            seen_keys.add(job_key)

            title = "N/A"
            for sel in ["h2.jobTitle a span[title]", "h2.jobTitle a span", "h2.jobTitle"]:
                try:
                    t = card.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if t:
                        title = t
                        break
                except NoSuchElementException:
                    pass

            try:
                company = card.find_element(
                    By.CSS_SELECTOR,
                    '[data-testid="company-name"], span.css-1h7lukg, span.companyName'
                ).text.strip()
            except NoSuchElementException:
                company = ""

            try:
                location = card.find_element(
                    By.CSS_SELECTOR,
                    '[data-testid="text-location"], div.css-1restlb, div.companyLocation'
                ).text.strip()
            except NoSuchElementException:
                location = ""

            infos.append({
                "job_key": job_key, "job_title": title,
                "company": company, "location": location,
            })
        except Exception:
            pass
    return infos, total


def extract_requirements(text):
    if not text:
        return ""
    headers = [
        r"REQUIREMENTS?", r"ANFORDERUNGEN", r"QUALIFIKATIONEN?",
        r"QUALIFICATIONS?", r"WHAT WE(?:'RE| ARE) LOOKING FOR",
        r"YOUR PROFILE", r"DEIN PROFIL", r"IHR PROFIL",
        r"MUST[- ]HAVES?",
        r"SKILLS?\s*(?:AND|&)\s*(?:EXPERIENCE|QUALIFICATIONS)",
        r"WHAT YOU BRING", r"WAS DU MITBRINGST", r"WAS SIE MITBRINGEN",
        r"KEY REQUIREMENTS", r"MINIMUM QUALIFICATIONS", r"WHO YOU ARE",
    ]
    pattern = "|".join(headers)
    match = re.search(
        rf"(?im)^\s*({pattern})\s*:?\s*\n(.*?)(?=\n\s*[A-Z\u00c4\u00d6\u00dc][\w\s&'-]{{2,}}:\s*$|\Z)",
        text, re.DOTALL | re.MULTILINE,
    )
    return match.group(0).strip() if match else text


def scrape_detail(driver, info):
    job_key = info["job_key"]
    url = f"https://ch.indeed.com/viewjob?jk={job_key}"
    try:
        time.sleep(random.uniform(3.0, 6.0))
        driver.get(url)
        wait_for_cloudflare(driver)

        if is_blocked(driver):
            print(f"    [BLOCKED] jk={job_key}")
            return None

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "jobDescriptionText")))
        time.sleep(1)

        desc = driver.find_element(By.ID, "jobDescriptionText").text.strip()
        reqs = extract_requirements(desc)

        print(f"    OK: {info['job_title'][:50]} @ {info['company'][:30]}")
        return {
            "job_title": info["job_title"],
            "company": info["company"],
            "location": info["location"],
            "requirements": reqs,
            "full_description": desc,
            "job_url": url,
        }
    except TimeoutException:
        print(f"    [TIMEOUT] jk={job_key}")
    except Exception as e:
        print(f"    [ERROR] jk={job_key}: {e}")
    return None


def migrate_csv_if_needed():
    """Add job_profil column to existing CSV if missing."""
    if not os.path.isfile(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        return
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if "job_profil" in (reader.fieldnames or []):
            return
        rows = list(reader)
    # Rewrite with new column
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            row["job_profil"] = "Business Developer"
            writer.writerow(row)
    print(f"CSV migriert: job_profil-Spalte hinzugefuegt ({len(rows)} Zeilen)")


def scrape_profile(driver, profile_name, variations, seen_keys, writer, csv_f,
                   skip_until=0):
    """Scrape all variations × locations for one job profile."""
    total_new = 0
    combos = [(loc, params) for loc in LOCATIONS for params in variations]
    print(f"\n{'#'*60}")
    print(f"PROFIL: {profile_name}")
    print(f"  {len(variations)} Suchvarianten x {len(LOCATIONS)} Standorte"
          f" = {len(combos)} Kombinationen")
    if skip_until > 0:
        print(f"  Springe zu Kombination {skip_until}...")
    print(f"{'#'*60}")

    for i, (loc, params) in enumerate(combos):
        if i + 1 < skip_until:
            continue
        full_params = {"l": loc, **params}
        url = build_url(full_params)
        query_desc = params.get("q", "?")
        extras = {k: v for k, v in params.items() if k != "q"}
        extra_str = f" [{extras}]" if extras else ""

        print(f"\n  --- {i+1}/{len(combos)}: "
              f"\"{query_desc}\"{extra_str} @ {loc}")

        driver.get(url)
        wait_for_cloudflare(driver)
        time.sleep(2)
        dismiss_overlays(driver)

        if is_blocked(driver):
            print("    [BLOCKED] Skipping")
            time.sleep(10)
            continue

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.job_seen_beacon, td.resultContent")))
            time.sleep(2)
        except TimeoutException:
            print("    [TIMEOUT] No job cards")
            time.sleep(5)
            continue

        infos, total_cards = extract_cards(driver, seen_keys)
        print(f"    {total_cards} cards, {len(infos)} new")

        if not infos:
            time.sleep(random.uniform(5.0, 10.0))
            continue

        scraped = 0
        for info in infos:
            item = scrape_detail(driver, info)
            if item:
                item["job_profil"] = profile_name
                total_new += 1
                scraped += 1
                writer.writerow(item)
                csv_f.flush()

        print(f"    Scraped: {scraped}/{len(infos)}")
        time.sleep(random.uniform(8.0, 15.0))

    return total_new


def main():
    import sys

    # Migrate existing CSV to add job_profil column
    migrate_csv_if_needed()

    seen_keys = load_existing_keys()
    if isinstance(seen_keys, tuple):
        seen_keys = seen_keys[0]
    print(f"Existing jobs in CSV: {len(seen_keys)}")

    # Allow selecting profiles and skip position via CLI
    # Usage: python3.12 scrape_indeed.py [--skip N] [--profile "Name"] ["Profile1" "Profile2" ...]
    skip_until = 0
    selected = []
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--skip" and i + 1 < len(args):
            skip_until = int(args[i + 1])
            i += 2
        elif args[i] == "--profile" and i + 1 < len(args):
            selected.append(args[i + 1])
            i += 2
        else:
            selected.append(args[i])
            i += 1

    if selected:
        profiles = {k: v for k, v in JOB_PROFILES.items() if k in selected}
        if not profiles:
            print(f"Unbekannte Profile: {selected}")
            print(f"Verfuegbar: {list(JOB_PROFILES.keys())}")
            sys.exit(1)
    else:
        profiles = JOB_PROFILES

    total_variations = sum(len(v) for v in profiles.values())
    print(f"Profile: {len(profiles)}, Variationen total: {total_variations}")

    # CSV writer (append mode)
    file_exists = os.path.isfile(CSV_FILE) and os.path.getsize(CSV_FILE) > 0
    csv_f = open(CSV_FILE, "a", newline="", encoding="utf-8-sig")
    writer = csv.DictWriter(csv_f, fieldnames=CSV_FIELDS, extrasaction="ignore")
    if not file_exists:
        writer.writeheader()

    # Start undetected Chrome
    print("Starting undetected Chrome...")
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=de-CH")
    driver = uc.Chrome(options=options, version_main=146)

    grand_total = 0

    try:
        first_profile = True
        for profile_name, variations in profiles.items():
            skip = skip_until if first_profile else 0
            first_profile = False
            n = scrape_profile(driver, profile_name, variations,
                              seen_keys, writer, csv_f, skip_until=skip)
            grand_total += n
            print(f"\n  => {profile_name}: {n} neue Jobs")

            # Longer pause between profiles
            time.sleep(random.uniform(10.0, 20.0))

    finally:
        csv_f.close()
        driver.quit()
        print(f"\n{'='*60}")
        print(f"FERTIG: {grand_total} neue Jobs -> {CSV_FILE}")
        print(f"Unique keys total: {len(seen_keys)}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
