"""
Items für den jobs.ch Scraper.
Definiert die Datenstruktur für jedes gescrapte Stelleninserat.
"""

import scrapy


class JobItem(scrapy.Item):
    """
    Repräsentiert ein einzelnes Stelleninserat von jobs.ch.
    Enthält die wichtigsten Metadaten sowie die extrahierten Anforderungen.
    """
    # Jobtitel (z.B. "Junior Business Development Manager")
    titel = scrapy.Field()

    # Name des Unternehmens
    unternehmen = scrapy.Field()

    # Arbeitsort (z.B. "Zürich")
    arbeitsort = scrapy.Field()

    # Direkt-Link zur Stellenanzeige
    url = scrapy.Field()

    # Veröffentlichungsdatum des Inserats
    veroeffentlicht_am = scrapy.Field()

    # Extrahierte Anforderungen / Profil-Punkte als kommaseparierter Text
    anforderungen = scrapy.Field()

    # Überschrift der Anforderungs-Sektion (z.B. "Ihr Profil", "Anforderungen")
    anforderungen_sektion = scrapy.Field()
