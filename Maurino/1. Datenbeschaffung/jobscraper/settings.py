# =============================================================================
# Scrapy Settings für den jobs.ch Scraper
# =============================================================================
#
# Dokumentation: https://docs.scrapy.org/en/latest/topics/settings.html

BOT_NAME = "jobscraper"
SPIDER_MODULES = ["jobscraper.spiders"]
NEWSPIDER_MODULE = "jobscraper.spiders"

# ---------------------------------------------------------------------------
# User-Agent: Realistische Browser-Kennung setzen, damit die Anfragen
# nicht sofort als Bot erkannt werden.
# ---------------------------------------------------------------------------
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# robots.txt: Gemäss Aufgabenstellung wird die robots.txt nicht beachtet.
# HINWEIS: In der Praxis sollte man die robots.txt respektieren und die
# Nutzungsbedingungen der Webseite prüfen, bevor man scrapt.
# ---------------------------------------------------------------------------
ROBOTSTXT_OBEY = False

# ---------------------------------------------------------------------------
# Höfliches Scraping: Download-Verzögerung und Concurrent Requests begrenzen,
# damit der Server nicht überlastet wird.
# ---------------------------------------------------------------------------
DOWNLOAD_DELAY = 1.5            # 1.5 Sekunden Pause zwischen Requests
RANDOMIZE_DOWNLOAD_DELAY = True  # Variiert die Pause leicht (0.5x bis 1.5x)
CONCURRENT_REQUESTS = 4          # Maximal 4 gleichzeitige Requests
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# ---------------------------------------------------------------------------
# HTTP-Headers: Realistische Browser-Headers senden.
# ---------------------------------------------------------------------------
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-CH,de;q=0.9,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}

# ---------------------------------------------------------------------------
# AutoThrottle: Passt die Download-Geschwindigkeit automatisch an die
# Server-Antwortzeit an. Verhindert Überlastung.
# ---------------------------------------------------------------------------
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.5
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# ---------------------------------------------------------------------------
# Item Pipeline: Aktiviert die Datenbereinigung.
# ---------------------------------------------------------------------------
ITEM_PIPELINES = {
    "jobscraper.pipelines.CleanTextPipeline": 300,
}

# ---------------------------------------------------------------------------
# Retry-Einstellungen: Bei temporären Fehlern automatisch wiederholen.
# ---------------------------------------------------------------------------
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# ---------------------------------------------------------------------------
# Download-Timeout: Nach 30 Sekunden abbrechen.
# ---------------------------------------------------------------------------
DOWNLOAD_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Logging: INFO-Level für übersichtliche Konsolenausgabe.
# ---------------------------------------------------------------------------
LOG_LEVEL = "INFO"

# ---------------------------------------------------------------------------
# CSV-Export: Standard-Ausgabeformat und Feld-Reihenfolge.
# ---------------------------------------------------------------------------
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "jobs_anforderungen.csv": {
        "format": "csv",
        "encoding": "utf-8",
        "fields": [
            "titel",
            "unternehmen",
            "arbeitsort",
            "anforderungen_sektion",
            "anforderungen",
            "veroeffentlicht_am",
            "url",
        ],
        "overwrite": True,
    },
}

# ---------------------------------------------------------------------------
# Zukunftssichere Einstellungen (standardmässig von Scrapy generiert).
# ---------------------------------------------------------------------------
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
