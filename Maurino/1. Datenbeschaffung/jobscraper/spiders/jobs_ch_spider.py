"""
=============================================================================
  Spider: jobs.ch Stellenanforderungen Scraper
=============================================================================

Dieser Spider extrahiert die Anforderungen (z.B. "Ihr Profil",
"Anforderungen", "Deine Qualitäten") aus Stelleninseraten auf jobs.ch.

FUNKTIONSWEISE:
1. Startet auf der Suchergebnisseite mit den gewünschten Filtern.
2. Sammelt alle Links zu einzelnen Stelleninseraten.
3. Folgt jedem Link und extrahiert die Anforderungen aus der Detailseite.
4. Navigiert automatisch zur nächsten Seite (Pagination).

TECHNISCHER HINTERGRUND:
- jobs.ch liefert die Stellendetails als JSON-LD (schema.org/JobPosting)
  direkt im HTML-Quellcode aus. Dadurch ist kein JavaScript-Rendering nötig.
- Die Job-Detail-Links sind als <a>-Tags mit href zu /de/stellenangebote/detail/
  im serverseitig gerenderten HTML vorhanden.
- Pagination erfolgt über den "page"-Parameter in der URL.
"""

import json
import re
import scrapy
from urllib.parse import quote, urlencode, urljoin
from jobscraper.items import JobItem


class JobsChSpider(scrapy.Spider):
    """
    Spider für jobs.ch – extrahiert Anforderungen aus Stelleninseraten.
    """

    name = "jobs_ch"
    allowed_domains = ["www.jobs.ch"]

    # -------------------------------------------------------------------------
    # Suchparameter: Passe diese an deine gewünschte Suche an.
    # -------------------------------------------------------------------------
    # Basis-URL für die Stellensuche
    BASE_SEARCH_URL = "https://www.jobs.ch/de/stellenangebote/"

    # Suchparameter als Dictionary (leicht anpassbar)
    SEARCH_PARAMS = {
        "employment-grade-min": "80",
        "employment-grade-max": "100",
        "employment-type": "5",
        "region": "2",
        "term": (
            "abschluss: mbi hsg business innovation\n"
            "position: \"junior\" oder \"entry level\" oder \"trainee\" "
            "oder \"graduate\" oder \"hochschulabsolvent\"\n"
            "suche: business development, digital crm, start-up & scale-up, "
            "technology solution architecture, digital transformation "
            "und supply chain management\n"
        ),
    }

    # -------------------------------------------------------------------------
    # Schlüsselwörter zur Erkennung der Anforderungs-Sektion im Inseratstext.
    # Die Reihenfolge bestimmt die Priorität (spezifischer zuerst).
    # -------------------------------------------------------------------------
    ANFORDERUNGS_KEYWORDS = [
        # --- Deutsch ---
        "ihr profil",
        "dein profil",
        "dein profil:",
        "anforderungen",
        "was sie mitbringen",
        "was du mitbringst",
        "deine qualitäten",
        "deine qualitäten und begabungen",
        "deine qualifikation",
        "qualifikationen",
        "was wir erwarten",
        "was wir von ihnen erwarten",
        "das bringst du mit",
        "das bringen sie mit",
        "das zeichnet dich aus:",
        "was dich auszeichnet",
        "das macht dich aus.",
        "ihre qualifikation",
        "voraussetzungen",
        "fachliche kompetenzen",
        "was sie idealerweise mitbringen",
        "was ist uns wichtig",
        "sie bringen",
        "wer du bist",
        "anforderungsprofil",
        "dieser job ist für dich, wenn",
        "damit machst du uns noch besser:",
        # --- Englisch ---
        "your background:",
        "your background",
        "profile",
        "your profile",
        "requirements",
        "what you bring",
        "what you'll bring",
        "what we expect",
        "qualifications",
        "your qualifications",
        "what you'll need",
        "what we're looking for",
        # --- Französisch ---
        "votre profil",
        "profil recherché",
        "profil souhaité",
        "votre parcours",
        "exigences",
        "qualifications requises",
        "ce que vous apportez",
    ]

    def start_requests(self):
        """
        Erstellt die erste Such-URL und startet den Crawl.
        dont_filter=True ist nötig, da jobs.ch die URL-Kodierung leicht
        ändert (z.B. '+' → '%20'), was Scrapy als Duplikat erkennen würde.
        """
        search_url = self._build_search_url(page=1)
        self.logger.info(f"Starte Suche: {search_url}")
        yield scrapy.Request(
            url=search_url,
            callback=self.parse_search_results,
            dont_filter=True,
        )

    def parse_search_results(self, response):
        """
        Verarbeitet eine Suchergebnisseite:
        1. Extrahiert Links zu Stelleninseraten.
        2. Folgt jedem Link zur Detailseite.
        3. Folgt dem "Nächste Seite"-Link für Pagination.
        """
        # --- Job-Detail-Links extrahieren ---
        # Links matchen das Muster /de/stellenangebote/detail/{UUID}/
        detail_links = response.css(
            'a[href*="/de/stellenangebote/detail/"]::attr(href)'
        ).getall()

        # Doppelte Links entfernen (Set), dann in absolute URLs umwandeln
        unique_links = set(detail_links)
        job_count = len(unique_links)
        self.logger.info(
            f"Seite geladen – {job_count} Inserate gefunden: {response.url}"
        )

        if job_count == 0:
            self.logger.warning("Keine Inserate auf dieser Seite gefunden!")
            return

        for link in unique_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_job_detail,
            )

        # --- Pagination: Nächste Seite ---
        # Der "Weiter"-Link hat das Attribut data-cy="paginator-next"
        next_page = response.css(
            'a[data-cy="paginator-next"]::attr(href)'
        ).get()

        if next_page:
            next_url = response.urljoin(next_page)
            self.logger.info(f"Navigiere zur nächsten Seite: {next_url}")
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_search_results,
            )
        else:
            self.logger.info("Letzte Seite erreicht – keine weitere Pagination.")

    def parse_job_detail(self, response):
        """
        Extrahiert die Anforderungen aus einer Stellendetailseite.

        STRATEGIE (abgestuft, vom zuverlässigsten zum Fallback):
        1. JSON-LD (schema.org/JobPosting): Enthält die vollständige
           Stellenbeschreibung als HTML im "description"-Feld.
        2. Fallback: Direkte HTML-Analyse der Seite.
        """
        item = JobItem()
        item["url"] = response.url

        # --- Schritt 1: JSON-LD extrahieren ---
        json_ld_data = self._extract_json_ld(response)

        if json_ld_data:
            # Metadaten aus JSON-LD
            item["titel"] = json_ld_data.get("title", "")
            item["veroeffentlicht_am"] = json_ld_data.get("datePosted", "")

            # Unternehmen
            hiring_org = json_ld_data.get("hiringOrganization", {})
            item["unternehmen"] = (
                hiring_org.get("name", "") if isinstance(hiring_org, dict) else ""
            )

            # Arbeitsort
            job_location = json_ld_data.get("jobLocation", {})
            if isinstance(job_location, dict):
                address = job_location.get("address", {})
                if isinstance(address, dict):
                    item["arbeitsort"] = address.get("addressLocality", "")
                else:
                    item["arbeitsort"] = ""
            else:
                item["arbeitsort"] = ""

            # --- Schritt 2: Anforderungen aus der HTML-Beschreibung parsen ---
            description_html = json_ld_data.get("description", "")
            sektion, anforderungen = self._extract_anforderungen_from_html(
                description_html
            )
            item["anforderungen_sektion"] = sektion
            item["anforderungen"] = anforderungen

        else:
            # Fallback: Kein JSON-LD vorhanden → aus dem HTML direkt lesen
            self.logger.warning(
                f"Kein JSON-LD gefunden für {response.url} – verwende Fallback"
            )
            item["titel"] = response.css("title::text").get("").split(" - ")[0].strip()
            item["unternehmen"] = ""
            item["arbeitsort"] = ""
            item["veroeffentlicht_am"] = ""
            item["anforderungen_sektion"] = ""
            item["anforderungen"] = ""

        # Nur Items mit extrahierten Anforderungen ausgeben
        if item.get("anforderungen"):
            yield item
        else:
            self.logger.warning(
                f"Keine Anforderungen gefunden für: {item.get('titel', 'Unbekannt')} "
                f"({response.url})"
            )
            # Trotzdem ausgeben, damit man sieht, welche Inserate keine
            # erkennbare Anforderungs-Sektion hatten
            item["anforderungen"] = "(keine Anforderungen erkannt)"
            item["anforderungen_sektion"] = "(nicht gefunden)"
            yield item

    # =========================================================================
    #  Hilfsmethoden
    # =========================================================================

    def _build_search_url(self, page=1):
        """
        Baut die vollständige Such-URL mit allen Parametern zusammen.
        Verwendet quote() statt urlencode(), da jobs.ch %20 statt + erwartet
        und sonst durch eine lange Redirect-Kette leitet.
        """
        params = dict(self.SEARCH_PARAMS)
        if page > 1:
            params["page"] = str(page)
        # urlencode mit quote_via=quote kodiert Leerzeichen als %20 statt +
        return f"{self.BASE_SEARCH_URL}?{urlencode(params, quote_via=quote)}"

    def _extract_json_ld(self, response):
        """
        Extrahiert das JSON-LD-Objekt vom Typ 'JobPosting' aus dem HTML.

        jobs.ch bettet die Stelleninformationen als <script type="application/ld+json">
        ein. Dieses enthält strukturierte Daten gemäss schema.org/JobPosting.
        """
        json_ld_scripts = response.css(
            'script[type="application/ld+json"]::text'
        ).getall()

        for script_text in json_ld_scripts:
            try:
                data = json.loads(script_text)
                # JSON-LD kann ein einzelnes Objekt oder eine Liste sein
                if isinstance(data, list):
                    for entry in data:
                        if entry.get("@type") == "JobPosting":
                            return entry
                elif isinstance(data, dict):
                    if data.get("@type") == "JobPosting":
                        return data
            except (json.JSONDecodeError, TypeError) as e:
                self.logger.debug(f"JSON-LD Parse-Fehler: {e}")
                continue

        return None

    def _extract_anforderungen_from_html(self, html_description):
        """
        Parst die HTML-Beschreibung aus dem JSON-LD und extrahiert die
        Anforderungs-Sektion.

        ANSATZ:
        - Sucht nach Überschriften, die eines der ANFORDERUNGS_KEYWORDS enthalten.
        - Sammelt die darauf folgende <ul>-Liste (Bulletpoints).
        - Falls keine passende Überschrift gefunden wird, wird die zweite <ul>
          im gesamten Text als Fallback verwendet (gemäss Aufgabenstellung).

        Returns:
            tuple: (sektions_name, anforderungen_text)
        """
        # Scrapy-Selektor aus dem HTML-Fragment erstellen
        selector = scrapy.Selector(text=html_description)

        # --- Strategie 1: Überschrift mit Keyword suchen ---
        # Alle Textblöcke durchsuchen, die ein Keyword enthalten
        for keyword in self.ANFORDERUNGS_KEYWORDS:
            # Suche in <strong>, <b>, <u>, <h1>-<h6>, <p> Tags nach dem Keyword
            # XPath: Suche case-insensitive nach dem Keyword in Textknoten
            # translate() wird für case-insensitive Vergleich verwendet
            xpath_expr = (
                f'//*[self::strong or self::b or self::u or self::h1 or '
                f'self::h2 or self::h3 or self::h4 or self::p]'
                f'[contains('
                f'translate(text(), '
                f'"ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÉÈÊËÀÂÇÎÏÔÙÛœ", '
                f'"abcdefghijklmnopqrstuvwxyzäöüéèêëàâçîïôùûœ"), '
                f'"{keyword}")]'
            )
            matches = selector.xpath(xpath_expr)

            for match in matches:
                sektion_name = match.css("::text").get("").strip()

                # Die nächste <ul>-Liste nach dieser Überschrift finden.
                # Wir navigieren zum Eltern-Element und suchen die folgende <ul>.
                following_uls = match.xpath(
                    'following::ul[1]//li/text()'
                ).getall()

                # Falls die <ul> innerhalb eines <p>-Eltern-Elements liegt,
                # auch im Parent suchen
                if not following_uls:
                    following_uls = match.xpath(
                        'ancestor::p/following-sibling::ul[1]//li/text()'
                    ).getall()

                if not following_uls:
                    following_uls = match.xpath(
                        'parent::*/following-sibling::ul[1]//li/text()'
                    ).getall()

                if following_uls:
                    # Bereinige die einzelnen Punkte und verbinde sie
                    cleaned = [punkt.strip() for punkt in following_uls if punkt.strip()]
                    anforderungen_text = " | ".join(cleaned)
                    return sektion_name, anforderungen_text

        # --- Strategie 2: Fallback – Zweite <ul> im Dokument verwenden ---
        # Gemäss Aufgabenstellung sind die Anforderungen meistens die zweite <ul>
        all_uls = selector.css("ul")
        if len(all_uls) >= 2:
            # Versuche, die Überschrift vor der zweiten <ul> zu finden
            second_ul = all_uls[1]
            li_texts = second_ul.css("li::text").getall()
            cleaned = [punkt.strip() for punkt in li_texts if punkt.strip()]

            # Überschrift: Suche den Text im vorherigen Geschwister-Element
            prev_heading = second_ul.xpath(
                'preceding-sibling::*[self::p or self::strong or self::h3][1]'
                '//text()'
            ).getall()
            sektion_name = " ".join(
                [t.strip() for t in prev_heading if t.strip()]
            ) or "(Fallback: 2. Aufzählung)"

            if cleaned:
                return sektion_name, " | ".join(cleaned)

        # --- Strategie 3: Letzer Fallback – Alle <ul>-Inhalte zusammen ---
        all_li_texts = selector.css("ul li::text").getall()
        if all_li_texts:
            cleaned = [punkt.strip() for punkt in all_li_texts if punkt.strip()]
            return "(alle Aufzählungen)", " | ".join(cleaned)

        return "", ""
