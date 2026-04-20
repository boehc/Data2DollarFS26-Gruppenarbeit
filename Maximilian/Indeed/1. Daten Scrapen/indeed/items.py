# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedItem(scrapy.Item):
    """Datenmodell für eine Indeed-Stellenanzeige."""
    job_title = scrapy.Field()         # Titel der Stelle
    company = scrapy.Field()           # Firmenname
    location = scrapy.Field()          # Arbeitsort
    requirements = scrapy.Field()      # Extrahierte Requirements
    full_description = scrapy.Field()  # Vollständige Jobbeschreibung
    job_url = scrapy.Field()           # Link zur Stellenanzeige
