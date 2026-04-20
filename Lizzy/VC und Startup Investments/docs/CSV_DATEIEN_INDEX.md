# 📊 CSV-Dateien Index

**Ordner:** `results/`  
**Anzahl:** 16 CSV-Dateien  
**Stand:** April 2026

---

## 🎯 Schnellnavigation

### Für schnelle Entscheidungen (hier starten!)
| Datei | Beschreibung |
|-------|--------------|
| ⭐ `INVESTMENT_RECOMMENDATIONS.csv` | Buy/Hold/Avoid für jede Branche |
| ⭐ `TOP_WINNERS_LOSERS.csv` | Gewinner und Verlierer auf einen Blick |
| ⭐ `SIMPLE_SUMMARY.csv` | One-Pager aller Branchen |

### Für tiefere Analyse
| Datei | Beschreibung |
|-------|--------------|
| `E_industry_classification.csv` | Komplette Klassifizierung mit allen Metriken |
| `YEARLY_COMPARISON.csv` | Jahr-zu-Jahr Vergleich |
| `MOMENTUM_LEADERS.csv` | Branchen nach Momentum sortiert |

---

## 📁 Vollständige Datei-Beschreibungen

### A — Marktanteile

**`A_market_share_pct.csv`**
- **Inhalt:** Marktanteile pro Branche in Prozent
- **Zeitraum:** 2023, 2024, 2025, 2026
- **Spalten:** `keyword`, `2023`, `2024`, `2025`, `2026`, `change_pct`
- **Verwendung:** Wer dominiert den Markt?

**Beispiel:**
| keyword | 2023 | 2024 | 2025 | change_pct |
|---------|------|------|------|------------|
| FinTech | 36.8% | 35.2% | 36.1% | -0.7pp |
| BioTech | 27.7% | 32.0% | 30.9% | +3.2pp |

---

### B — Rankings

**`B_rankings_by_year.csv`**
- **Inhalt:** Ranking-Position jeder Branche pro Jahr
- **Spalten:** `keyword`, `rank_2023`, `rank_2024`, `rank_2025`, `rank_change`
- **Verwendung:** Wer steigt auf, wer fällt ab?

---

### C — Funding-Anteile

**`C_funding_share_pct.csv`**
- **Inhalt:** Anteil am Gesamtfunding pro Branche
- **Spalten:** `keyword`, `funding_share_2023`, `funding_share_2024`, `funding_share_2025`
- **Verwendung:** Wo fliesst das Geld hin?

---

### D — Momentum

**`D_momentum.csv`**
- **Inhalt:** Veränderung des Marktanteils (Beschleunigung/Verlangsamung)
- **Spalten:** `keyword`, `momentum_pct`, `direction`, `classification`
- **Verwendung:** Wer beschleunigt, wer bremst?

**Wichtig:** Momentum ≠ absolute Grösse
- GenAI: +168% Momentum (klein aber schnell wachsend)
- FinTech: -12% Momentum (gross aber schrumpfend)

---

### E — Klassifizierung

**`E_industry_classification.csv`**
- **Inhalt:** Komplette Branchen-Klassifizierung
- **Spalten:** `keyword`, `classification`, `deals_total`, `market_share`, `momentum`, `signal`
- **Verwendung:** Master-Datei für alle Metriken

**Klassifizierungen:**
- `Emerging 🌱` — Stark wachsend (GenAI, Robotics)
- `Growing ↑` — Wachsend (BioTech, MedTech)
- `Stable →` — Stabil (HealthTech, Ecommerce)
- `Slowing ↓` — Rückläufig (ClimateTech, FinTech)

---

### F1/F2 — Quartals-Daten

**`F1_deal_count_quarterly.csv`**
- **Inhalt:** Anzahl Deals pro Branche pro Quartal
- **Spalten:** `keyword`, `2023-Q1`, `2023-Q2`, ..., `2026-Q1`
- **Verwendung:** Saisonale Muster, Zeitverlauf

**`F2_deal_share_quarterly.csv`**
- **Inhalt:** Prozentanteil pro Quartal (statt absolute Zahlen)
- **Verwendung:** Relative Entwicklung

---

### Zusammenfassungen

**`SIMPLE_SUMMARY.csv`**
- **Inhalt:** One-Pager aller Branchen
- **Spalten:** `keyword`, `total_deals`, `deals_2023`, `deals_2025`, `growth`, `classification`, `momentum`
- **Verwendung:** ⭐ Schnellster Überblick

**`INVESTMENT_RECOMMENDATIONS.csv`**
- **Inhalt:** Finale Investment-Signale
- **Spalten:** `keyword`, `signal`, `reasoning`, `risk_level`
- **Signale:** STRONG BUY, BUY, HOLD, AVOID, SELL
- **Verwendung:** ⭐ Entscheidungsgrundlage

**`TOP_WINNERS_LOSERS.csv`**
- **Inhalt:** Gewinner und Verlierer
- **Spalten:** `keyword`, `category`, `change`, `reason`
- **Verwendung:** Schnelle Identifikation von Trends

---

### Weitere Dateien

**`FUNDING_ANALYSIS.csv`**
- Detaillierte Funding-Analyse pro Branche

**`MOMENTUM_LEADERS.csv`**
- Top-Branchen nach Momentum sortiert

**`RECENT_QUARTERS_TREND.csv`**
- Fokus auf die letzten 4 Quartale

**`TOP5_PER_YEAR.csv`**
- Top 5 Branchen pro Jahr

**`YEARLY_COMPARISON.csv`**
- Direkter Jahr-zu-Jahr Vergleich

**`_FILE_GUIDE.csv`**
- Maschinenlesbare Datei-Übersicht (Meta)

---

## 🔢 Datenqualität

| Metrik | Wert |
|--------|------|
| **Total Deals** | 1'327 |
| **Vollständigkeit** | 100% für Branchen, Deals |
| **Zeitabdeckung** | Q1/2023 – Q1/2026 (13 Quartale) |
| **Branchen** | 14 klassifiziert |

---

## 💡 Tipps zur Analyse

### In Excel/Google Sheets
1. `SIMPLE_SUMMARY.csv` öffnen
2. Nach `momentum` sortieren (absteigend)
3. Top 3 = Empfohlene Branchen

### Für Visualisierung
- `F1_deal_count_quarterly.csv` → Liniendiagramm über Zeit
- `A_market_share_pct.csv` → Kreisdiagramm Marktanteile
- `D_momentum.csv` → Balkendiagramm Momentum

### Für Präsentationen
- `INVESTMENT_RECOMMENDATIONS.csv` → Entscheidungsmatrix
- `TOP_WINNERS_LOSERS.csv` → Gewinner/Verlierer Folie

---

*Erstellt: April 2026*
