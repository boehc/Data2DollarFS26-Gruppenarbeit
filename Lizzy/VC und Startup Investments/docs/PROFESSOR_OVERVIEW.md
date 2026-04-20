# 🎓 Übersicht für Professor — Chiara's Beitrag

**Projekt:** Data2Dollar – MBI Gruppenarbeit FS26  
**Autor:** Chiara Boehme  
**Datum:** April 2026

---

## 📋 Zusammenfassung

Dieses Projekt analysiert das **Schweizer Startup-Ökosystem von 2023–2026** mit dem Ziel, MBI-Studierenden datenbasierte Gründungsempfehlungen zu geben.

### Mein Beitrag umfasst:
1. **Datensammlung** — Web Scraper für Schweizer Startup-Daten
2. **Datenverarbeitung** — Bereinigung, Klassifizierung, LLM-Extraktion
3. **Analyse** — Industry Trends, Momentum-Berechnung, Rankings
4. **Visualisierung** — Interaktive Webseite "Lizzys"

---

## 📊 Datengrundlage

| Metrik | Wert |
|--------|------|
| **Gesamt-Deals** | 1'327 Startup-Finanzierungsrunden |
| **Zeitraum** | Q1/2023 – Q1/2026 (13 Quartale) |
| **Branchen** | 14 klassifiziert |
| **Funding-Volumen** | CHF 38.5 Mrd. Total |
| **Datenquellen** | Startupticker.ch, Venture Kick |

---

## 🛠️ Technische Pipeline

### Phase 1: Datensammlung (`code/1_data_collection/`)
```
Startupticker Scraper → 1'564 Artikel gescraped
Venture Kick Scraper  → Zusätzliche VC-Daten
Kaggle/YC/VCLense     → Exploriert, nicht verwendet (siehe README)
```

### Phase 2: Verarbeitung (`code/2_data_processing/`)
```
Merge & Clean         → Duplikate entfernt, Formate vereinheitlicht
LLM-Extraktion        → GPT-4 für Branchen-Klassifizierung
Quality Analysis      → Datenqualität validiert
```

### Phase 3: Analyse (`code/3_analysis/`)
```
Industry Trends       → Marktanteile, Momentum, Rankings
Funding Analysis      → Volumen pro Branche/Quartal
```

---

## 📁 Datei-Übersicht

### Wichtigste Result-Dateien (`results/`)

| Priorität | Datei | Beschreibung |
|-----------|-------|--------------|
| ⭐⭐⭐ | `INVESTMENT_RECOMMENDATIONS.csv` | Buy/Hold/Avoid pro Branche |
| ⭐⭐⭐ | `SIMPLE_SUMMARY.csv` | One-Pager aller Branchen |
| ⭐⭐ | `D_momentum.csv` | Momentum-Berechnungen |
| ⭐⭐ | `F1_deal_count_quarterly.csv` | Quartals-Daten (Webseite) |
| ⭐ | `TOP_WINNERS_LOSERS.csv` | Gewinner vs. Verlierer |

### Dokumentation (`docs/`)

| Datei | Inhalt |
|-------|--------|
| `EXECUTIVE_SUMMARY.md` | Kernaussagen für Entscheidungsträger |
| `QUICK_START.md` | Anleitung für CSV-Analyse |
| `CSV_FILES_INDEX.md` | Detaillierte Beschreibung aller Dateien |
| `PROJECT_ORGANIZATION.md` | Komplette Ordnerstruktur |

---

## 🔑 Kernaussagen der Analyse

### Empfehlung 2026: Wo gründen?

| Kategorie | Branchen | Begründung |
|-----------|----------|------------|
| 🟢 **STRONG BUY** | GenAI, Robotics | +168% / +109% Momentum, stark wachsend |
| 🟢 **BUY** | BioTech, MedTech | Grösste Märkte, stabile Dominanz |
| 🟡 **HOLD** | HealthTech, Ecommerce | Neutral, weder stark wachsend noch sinkend |
| 🔴 **AVOID** | ClimateTech, FinTech | Sinkende Marktanteile, Dynamik lässt nach |
| 🔴 **SELL** | SpaceTech, EdTech | Praktisch keine Deals mehr |

### Wichtigste Erkenntnisse
1. **BioTech** dominiert mit 31% Marktanteil und 58% des Funding-Volumens
2. **GenAI** hat sich von 1.8% auf 4.1% Marktanteil verdoppelt
3. **ClimateTech** hat -7.1pp Marktanteil verloren (grösster Verlierer)
4. **FinTech** ist der grösste Markt (36%), aber mit sinkender Dynamik

### ⚠️ Methodische Anmerkung zu "GenAI"

> **Disclaimer:** Die Kategorie "GenAI" (bzw. "AI/ML" in den Rohdaten) bezeichnet hier **AI-Native Startups** – also Unternehmen, deren Kernprodukt auf Künstlicher Intelligenz basiert.
>
> Technisch betrachtet ist GenAI eine **Querschnittstechnologie**, die in vielen Branchen angewendet wird (z.B. HealthTech+AI, FinTech+AI, etc.). In den Originaldaten von Startupticker wurden 44 Startups als "AI/ML" klassifiziert, da deren Hauptprodukt AI-basiert ist und sich nicht primär einer anderen Branche zuordnen lässt.
>
> Diese Einordnung folgt der Praxis von Startupticker.ch und spiegelt den Markttrend wider, dass AI zunehmend als eigenständiger Geschäftsbereich wahrgenommen wird.

---

## 🌐 Webseite "Lizzys"

Die interaktive Webseite (`Webseite Gründerin/`) visualisiert die Analyse:

| Seite | Inhalt |
|-------|--------|
| **Home** | Projektübersicht, Navigation |
| **Trends** | Globale Tech-Trends (News-Analyse) |
| **Investments** | Schweizer VC-Deals & Funding |
| **Opportunity** | Branchen-Ranking, Gründungsempfehlungen |
| **MBI-Kurse** | Self-Assessment & Kursempfehlungen |

**Live-Demo:** `python3 -m http.server 8080` im Ordner `Webseite Gründerin/`

---

## ✅ Qualitätssicherung

### Daten-Validierung
- [x] Total Deals in Results = Total Deals in Rohdaten (1'327)
- [x] Branchen-Summen stimmen überein
- [x] Quartals-Daten vollständig (bis Q1/2026)
- [x] Funding-Werte aus classified_v2.csv validiert

### Dokumentation
- [x] README.md mit Projektübersicht
- [x] Alle Scraper dokumentiert
- [x] Nicht verwendete Scraper begründet
- [x] Rohdaten-Pfade dokumentiert

---

## 📚 Weiterführende Ressourcen

- **Rohdaten:** `rohdaten/startupticker_enriched_FINAL.csv`
- **Klassifiziert:** `rohdaten/startups_classified_v2.csv`
- **Webseite:** `Webseite Gründerin/`
- **Archiv:** `archive/` (alle alten Versionen)

---

*Erstellt: 20. April 2026*
