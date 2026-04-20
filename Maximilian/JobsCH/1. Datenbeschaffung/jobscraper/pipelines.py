"""
Item Pipelines für den jobs.ch Scraper.
Bereinigt und normalisiert die gescrapten Daten vor dem Export.
"""

import re
from itemadapter import ItemAdapter


class CleanTextPipeline:
    """
    Pipeline zur Textbereinigung:
    - Entfernt überflüssige Leerzeichen und Zeilenumbrüche
    - Normalisiert Unicode-Sonderzeichen (z.B. &nbsp;)
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                # Mehrfache Leerzeichen/Zeilenumbrüche zu einem Leerzeichen zusammenfassen
                value = re.sub(r'\s+', ' ', value).strip()
                adapter[field_name] = value
        return item
