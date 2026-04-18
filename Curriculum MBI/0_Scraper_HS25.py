"""
MBI Kurs-Scraper - Lädt alle Merkblätter des 18MBIh Masters herunter.

Strategie:
  1. Navigiere zum Fachstudium (Master → 18MBIh → Fachstudium)
  2. Klappe ALLE Baumknoten auf (wiederhole bis keine aria-expanded="false" mehr)
  3. Sammle alle Kurslinks (href enthält "event/events/by-term")
  4. Für jeden Kurs: Seite öffnen → Merkblatt-PDF herunterladen → zurück
"""

import logging
import re
import time
from pathlib import Path

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://courses.unisg.ch/event/event-hierarchy/by-term/4d90fc2e-5321-473f-84d5-498a70062b9d"
OUTPUT_DIR = Path("mbi_hs25_ohne_wahlbereich")
OUTPUT_DIR.mkdir(exist_ok=True)

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

logger.info("🚀 Starte Browser...")
driver = uc.Chrome(options=chrome_options, version_main=145)

stealth_js = """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
    });
"""
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": stealth_js})

logger.info("📍 Gehe zu URL...")
driver.get(BASE_URL)
time.sleep(1)

# Handle Alert
try:
    alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
    logger.info("  ⚠️  Alert akzeptiert")
    alert.accept()
    time.sleep(1)
except:
    pass

time.sleep(2)

# ─────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN
# ─────────────────────────────────────────────────────────────

def klick_node(text):
    """Findet einen Baumknoten mit diesem Text und klappt ihn auf."""
    xpath = f"//mat-tree-node[contains(., '{text}')]//button[contains(@class, 'mat-mdc-icon-button')]"
    btn = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    btn.click()
    time.sleep(4)
    logger.info(f"  ✓ '{text}' aufgeklappt")

def alles_aufklappen():
    """
    Klappt NUR die Knoten innerhalb von Fachstudium (18MBIh) auf.
    Bedingung: aria-level >= 4  →  das sind ausschliesslich Kinder von Fachstudium.
    Andere Master (aria-level 1-2) werden NICHT angefasst.
    Wiederholt sich solange, bis kein passender aria-expanded='false' mehr vorhanden ist.
    """
    runde = 0
    while True:
        runde += 1
        # Nur Knoten mit aria-level >= 4 (Pflichtbereich, Vertiefungen, …)
        # Wahlbereich wird NICHT aufgeklappt
        geschlossen = driver.find_elements(
            By.XPATH,
            "//mat-tree-node[@aria-expanded='false' and number(@aria-level) >= 4 "
            "and not(normalize-space(.)='Wahlbereich')]"
            "//button[contains(@class, 'mat-mdc-icon-button')]"
        )
        if not geschlossen:
            logger.info(f"  ✓ Alle Knoten aufgeklappt (nach {runde - 1} Runden)")
            break
        logger.info(f"  → Runde {runde}: {len(geschlossen)} geschlossene Knoten gefunden, klappe auf...")
        for btn in geschlossen:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                time.sleep(0.8)  # kurze Pause zwischen den Klicks
            except Exception:
                pass  # Knoten verschwand inzwischen – kein Problem
        time.sleep(3)  # warte auf Rendering nach jeder Runde

def sammle_kurslinks():
    """
    Gibt alle eindeutigen Kurs-Links zurück die aktuell sichtbar sind.
    Kurslinks enthalten immer 'event/events/by-term' im href.
    """
    elemente = driver.find_elements(
        By.XPATH, "//a[contains(@href, 'event/events/by-term')]"
    )
    # Eindeutige hrefs (Kurs kann in mehreren Vertiefungen auftauchen)
    seen = set()
    kurse = []
    for el in elemente:
        href = el.get_attribute("href")
        name = el.text.strip()
        if href and href not in seen:
            seen.add(href)
            kurse.append({"name": name, "href": href})
    logger.info(f"  ✓ {len(kurse)} eindeutige Kurslinks gesammelt")
    return kurse

def download_merkblatt(kurs_url, kurs_name):
    """
    Öffnet die Kursseite, sucht das Merkblatt-PDF und lädt es herunter.
    Dateiname = Kursnummer (aus der PDF-URL extrahiert).
    Gibt True zurück wenn erfolgreich, sonst False.
    """
    try:
        driver.get(kurs_url)
        time.sleep(3)
        # Warte auf Merkblatt-Link
        wait = WebDriverWait(driver, 10)
        link = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'Merkblatt')]"))
        )
        pdf_url = link.get_attribute("href")

        # Kursnummer aus URL extrahieren:
        # z.B. ".../eventnumber/8,000,1.00.pdf" → "8,000,1.00"
        match = re.search(r"eventnumber/([^/]+\.pdf)", pdf_url)
        if match:
            kursnummer = match.group(1)[:-4]  # ".pdf" abschneiden
        else:
            kursnummer = re.sub(r'[\\/*?:"<>|]', "_", kurs_name)[:80]

        filepath = OUTPUT_DIR / f"{kursnummer}.pdf"

        # Bereits vorhanden? Überspringen
        if filepath.exists():
            logger.info(f"    ⏭  Bereits vorhanden: {filepath.name}")
            return True

        response = requests.get(pdf_url, timeout=15)
        if response.status_code == 200:
            filepath.write_bytes(response.content)
            logger.info(f"    ✅ Gespeichert: {filepath.name}  ({len(response.content)//1024} KB)")
            return True
        else:
            logger.warning(f"    ⚠️  HTTP {response.status_code} für {pdf_url}")
            return False

    except Exception as e:
        logger.warning(f"    ❌ Fehler bei '{kurs_name}': {e}")
        return False

# ─────────────────────────────────────────────────────────────
# HAUPTABLAUF
# ─────────────────────────────────────────────────────────────

logger.info("\n=== SCHRITT 1-3: Navigiere zu Fachstudium ===")
for node in ["Master", "18MBIh", "Fachstudium"]:
    klick_node(node)

logger.info("\n=== SCHRITT 4: Klappe ALLE Unterknoten auf ===")
alles_aufklappen()

logger.info("\n=== SCHRITT 5: Sammle alle Kurslinks ===")
alle_kurse = sammle_kurslinks()

logger.info(f"\n=== SCHRITT 6: Lade {len(alle_kurse)} Merkblätter herunter ===")
ok = 0
fehler = 0
for i, kurs in enumerate(alle_kurse, 1):
    logger.info(f"\n  [{i}/{len(alle_kurse)}] {kurs['name']}")
    if download_merkblatt(kurs["href"], kurs["name"]):
        ok += 1
    else:
        fehler += 1
    time.sleep(1)  # kurze Pause zwischen Downloads

logger.info(f"\n{'='*60}")
logger.info(f"✅ Fertig!  Erfolgreich: {ok}  |  Fehler: {fehler}")
logger.info(f"📁 PDFs gespeichert in: {OUTPUT_DIR.absolute()}")
logger.info(f"{'='*60}")

driver.quit()
