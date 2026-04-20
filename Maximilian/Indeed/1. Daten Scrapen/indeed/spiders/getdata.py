"""
Indeed Job Scraper - Scrapy + Selenium
======================================
Extrahiert Jobtitel, Firma, Standort und Requirements von
Indeed-Stellenanzeigen (ch.indeed.com) fuer "Business Developer" in Zuerich.

Strategie:
  - Seite 1 wird direkt per URL geladen (keine Anmeldung noetig).
  - Seiten 2-10 werden durch Klick auf den Weiter-Button erreicht
    (Indeed verlangt Login, wenn man paginierte URLs direkt aufruft).
  - Zwischen den Seiten: menschliche Pausen.
  - Fuer jeden Job-Key wird die Detailseite /viewjob?jk=... geladen,
    um die vollstaendige Beschreibung + Requirements zu extrahieren.
  - Bereits gescrapte Jobs (aus indeed_jobs.csv) werden uebersprungen.
  - CSV wird im Append-Modus geschrieben.

Ausfuehrung:
    cd /Users/Oliver/Documents/Gruppenarbeit/indeed
    scrapy crawl getdata                    # alle Seiten
    scrapy crawl getdata -a max_pages=5     # nur 5 Seiten
    scrapy crawl getdata -a headless=true   # unsichtbar (oft geblockt)
"""

import csv
import os
import re
import time
import random

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)


class GetdataSpider(scrapy.Spider):
    name = "getdata"

    SEARCH_URL = (
        "https://ch.indeed.com/jobs?q=business+developer"
        "&l=Z%C3%BCrich%2C+ZH&from=searchOnHP"
    )

    MAX_PAGES = 10

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0,
        "CONCURRENT_REQUESTS": 1,
        "LOG_LEVEL": "INFO",
    }

    CSV_FILE = "indeed_jobs.csv"
    CSV_FIELDS = [
        "job_title", "company", "location", "requirements",
        "full_description", "job_url",
    ]

    # ----------------------------------------------------------------
    # Init
    # ----------------------------------------------------------------

    def __init__(self, headless="false", max_pages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_headless = headless.lower() == "true"
        self.driver = None
        self.jobs_scraped = 0
        self.max_pages = int(max_pages) if max_pages else self.MAX_PAGES

        self.seen_job_keys = self._load_existing_job_keys()
        if self.seen_job_keys:
            self.logger.info(
                "Bereits %d Jobs in %s vorhanden -> werden uebersprungen",
                len(self.seen_job_keys), self.CSV_FILE,
            )

        file_exists = os.path.isfile(self.CSV_FILE) and os.path.getsize(self.CSV_FILE) > 0
        self._csv_file = open(self.CSV_FILE, "a", newline="", encoding="utf-8-sig")
        self._csv_writer = csv.DictWriter(
            self._csv_file, fieldnames=self.CSV_FIELDS, extrasaction="ignore",
        )
        if not file_exists:
            self._csv_writer.writeheader()

    def _load_existing_job_keys(self):
        keys = set()
        if not os.path.isfile(self.CSV_FILE):
            return keys
        try:
            with open(self.CSV_FILE, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get("job_url", "")
                    if "jk=" in url:
                        keys.add(url.split("jk=")[-1].split("&")[0])
            return keys
        except Exception:
            return keys

    # ----------------------------------------------------------------
    # Chrome WebDriver
    # ----------------------------------------------------------------

    def _create_driver(self):
        opts = Options()
        if self.use_headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--lang=de-CH")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        )
        driver = webdriver.Chrome(options=opts)
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'},
        )
        self.logger.info("Chrome gestartet (%s)", "headless" if self.use_headless else "sichtbar")
        return driver

    # ----------------------------------------------------------------
    # Scrapy entry
    # ----------------------------------------------------------------

    def start_requests(self):
        yield scrapy.Request(url=self.SEARCH_URL, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.driver = self._create_driver()

        self.logger.info("Lade Seite 1: %s", self.SEARCH_URL)
        self.driver.get(self.SEARCH_URL)
        self._wait_for_cloudflare()
        self._dismiss_overlays()

        last_search_url = self.driver.current_url

        for page_num in range(1, self.max_pages + 1):
            self.logger.info("=== SEITE %d / %d ===", page_num, self.max_pages)

            if self._is_blocked():
                self.logger.warning("Seite %d: Blockiert oder Login-Prompt -> stoppe", page_num)
                self._save_screenshot("blocked_page%d.png" % page_num)
                break

            job_infos = self._extract_job_cards(page_num)

            if not job_infos:
                self.logger.warning("Seite %d: Keine neuen Jobs gefunden", page_num)
            else:
                self.logger.info(
                    "Seite %d: %d neue Jobs, lade Detailseiten",
                    page_num, len(job_infos),
                )
                last_search_url = self.driver.current_url

                for info in job_infos:
                    item = self._scrape_job_detail(info, page_num)
                    if item:
                        self.jobs_scraped += 1
                        self._csv_writer.writerow(item)
                        self._csv_file.flush()

                self.logger.info(
                    "Seite %d fertig. Gesamt: %d Jobs", page_num, self.jobs_scraped,
                )

                # Navigate back to search page
                self.logger.info("Navigiere zurueck zur Suchseite...")
                self.driver.get(last_search_url)
                time.sleep(3)
                self._wait_for_cloudflare()
                self._dismiss_overlays()

            # Next page
            if page_num < self.max_pages:
                if not self._click_next_page(page_num):
                    self.logger.info("Keine weitere Seite verfuegbar -> Ende")
                    break
                wait = random.uniform(3.0, 6.0)
                self.logger.info("Pause: %.1fs vor Seite %d...", wait, page_num + 1)
                time.sleep(wait)

    # ----------------------------------------------------------------
    # Extract job cards from current search page
    # ----------------------------------------------------------------

    def _extract_job_cards(self, page_num):
        try:
            WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.job_seen_beacon, td.resultContent, div.jobsearch-ResultsList")
                )
            )
            time.sleep(2)
        except TimeoutException:
            self.logger.error("Seite %d: Timeout, keine Jobkarten gefunden", page_num)
            self._save_screenshot("error_page%d.png" % page_num)
            return []

        self._dismiss_overlays()
        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
        self.logger.info("Seite %d: %d Jobkarten im DOM", page_num, len(cards))

        job_infos = []
        for card in cards:
            info = self._extract_card_info(card)
            if not info:
                continue
            jk = info.get("job_key")
            if jk and jk in self.seen_job_keys:
                continue
            if jk:
                self.seen_job_keys.add(jk)
            job_infos.append(info)
        return job_infos

    def _extract_card_info(self, card):
        try:
            job_key = None
            try:
                link = card.find_element(
                    By.CSS_SELECTOR, "h2.jobTitle a[data-jk], a.jcs-JobTitle[data-jk]",
                )
                job_key = link.get_attribute("data-jk")
            except NoSuchElementException:
                try:
                    link = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                    link_id = link.get_attribute("id") or ""
                    if "_" in link_id:
                        job_key = link_id.split("_", 1)[1]
                except NoSuchElementException:
                    pass

            if not job_key:
                return None

            job_title = "Titel nicht gefunden"
            for sel in ["h2.jobTitle a span[title]", "h2.jobTitle a span", "h2.jobTitle"]:
                try:
                    text = card.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if text:
                        job_title = text
                        break
                except NoSuchElementException:
                    continue

            company = self._safe_text(
                card, '[data-testid="company-name"], span.css-1h7lukg, span.companyName',
            )
            location = self._safe_text(
                card, '[data-testid="text-location"], div.css-1restlb, div.companyLocation',
            )

            return {
                "job_key": job_key,
                "job_title": job_title,
                "company": company,
                "location": location,
            }
        except Exception as e:
            self.logger.debug("Fehler bei Karten-Extraktion: %s", e)
            return None

    # ----------------------------------------------------------------
    # Pagination
    # ----------------------------------------------------------------

    def _click_next_page(self, current_page):
        if not self._has_job_cards():
            self.logger.warning("Nicht auf Suchseite, kann nicht paginieren")
            return False

        next_selectors = [
            'a[data-testid="pagination-page-next"]',
            'a[aria-label="Next Page"]',
            'a[aria-label="N\u00e4chste Seite"]',
            'nav[role="navigation"] a:last-child',
        ]
        for sel in next_selectors:
            try:
                btn = self.driver.find_element(By.CSS_SELECTOR, sel)
                if btn.is_displayed():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        btn,
                    )
                    time.sleep(1)
                    btn.click()
                    self.logger.info("Weiter-Button geklickt (%s)", sel)
                    time.sleep(3)
                    self._wait_for_cloudflare()
                    return True
            except (NoSuchElementException, TimeoutException):
                continue
            except Exception as e:
                self.logger.debug("Fehler bei Selektor %s: %s", sel, e)

        # Fallback: search by text
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, 'nav[role="navigation"] a')
            for lnk in links:
                txt = lnk.text.strip().lower()
                if txt in ("next", "weiter", "\u203a", "\u00bb"):
                    lnk.click()
                    self.logger.info("Weiter-Link per Text geklickt: %s", txt)
                    time.sleep(3)
                    self._wait_for_cloudflare()
                    return True
        except Exception:
            pass

        self.logger.warning("Kein Weiter-Button auf Seite %d", current_page)
        return False

    def _has_job_cards(self):
        try:
            return len(self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")) > 0
        except Exception:
            return False

    # ----------------------------------------------------------------
    # Detail page
    # ----------------------------------------------------------------

    def _scrape_job_detail(self, info, page_num):
        job_key = info["job_key"]
        detail_url = "https://ch.indeed.com/viewjob?jk=" + job_key

        try:
            time.sleep(random.uniform(3.0, 6.0))
            self.driver.get(detail_url)
            self._wait_for_cloudflare()

            if self._is_blocked():
                self.logger.warning("Blockiert bei jk=%s -> ueberspringe", job_key)
                return None

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            time.sleep(1)

            desc_el = self.driver.find_element(By.ID, "jobDescriptionText")
            full_description = desc_el.text.strip()
            requirements = self._extract_requirements(full_description)

            self.logger.info(
                "  OK %s @ %s (jk=%s)", info["job_title"], info["company"], job_key,
            )

            return {
                "job_title": info["job_title"],
                "company": info["company"],
                "location": info["location"],
                "requirements": requirements,
                "full_description": full_description,
                "job_url": detail_url,
            }
        except TimeoutException:
            self.logger.warning("  TIMEOUT bei jk=%s (%s)", job_key, info["job_title"])
            self._save_screenshot("error_detail_%s.png" % job_key)
        except Exception as e:
            self.logger.warning(
                "  FEHLER bei jk=%s: %s: %s", job_key, type(e).__name__, e,
            )
        return None

    # ----------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------

    def _is_blocked(self):
        try:
            src = self.driver.page_source[:5000].lower()
            indicators = [
                "anfrage blockiert",
                "sie wurden gesperrt",
                "request blocked",
                "you have been blocked",
                "access denied",
                "code in ihrem posteingang",
                "code eingeben",
                "erstellen sie jetzt ein konto",
                "melden sie sich an, um mehr als eine seite",
            ]
            return any(ind in src for ind in indicators)
        except Exception:
            return False

    def _wait_for_cloudflare(self, timeout=15):
        start = time.time()
        while time.time() - start < timeout:
            title = self.driver.title.lower()
            snippet = self.driver.page_source[:2000].lower()
            cfs = [
                "just a moment", "checking your browser", "cloudflare",
                "challenge-platform", "cf-browser-verification",
            ]
            if not any(c in title or c in snippet for c in cfs):
                return
            time.sleep(1)
        self.logger.warning(
            "Cloudflare-Challenge nicht innerhalb von %ds geloest", timeout,
        )

    def _safe_text(self, parent, css):
        try:
            return parent.find_element(By.CSS_SELECTOR, css).text.strip()
        except NoSuchElementException:
            return ""

    def _dismiss_overlays(self):
        for sel in [
            "#onetrust-accept-btn-handler",
            'button[id*="accept"]',
            "#mosaic-desktopserpjapopup button",
        ]:
            try:
                btn = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                btn.click()
                self.logger.info("Overlay geschlossen: %s", sel)
                time.sleep(0.5)
            except (TimeoutException, NoSuchElementException):
                continue

    def _extract_requirements(self, full_text):
        if not full_text:
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
            full_text,
            re.DOTALL | re.MULTILINE,
        )
        if match:
            return match.group(0).strip()
        return full_text

    def _save_screenshot(self, filename):
        try:
            self.driver.save_screenshot(filename)
            self.logger.info("Screenshot gespeichert: %s", filename)
        except Exception:
            pass

    # ----------------------------------------------------------------
    # Cleanup
    # ----------------------------------------------------------------

    def closed(self, reason):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.logger.info("Browser geschlossen")
        if hasattr(self, "_csv_file") and self._csv_file:
            self._csv_file.close()
        self.logger.info(
            "=== FERTIG: %d neue Jobs in %s ===", self.jobs_scraped, self.CSV_FILE,
        )
