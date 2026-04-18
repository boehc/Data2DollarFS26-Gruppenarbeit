# Industry Trends Analysis — README

## 📋 Übersicht

Dieser Analyse-Workflow beantwortet die Kernfrage:  
**"Welche Industrien gewinnen oder verlieren 2023–2026 an Bedeutung?"**

Nicht absolute Wachstumszahlen sind entscheidend, sondern **relative Verschiebungen** —  
welche Industrie bekommt MEHR Aufmerksamkeit und Funding als zuvor?

---

## 🚀 Quick Start

```bash
# 1. Stelle sicher, dass startups_classified_v2.csv existiert
ls data/startups_classified_v2.csv

# 2. Führe die Analyse aus
python3 step2_industry_trends.py

# 3. Ergebnisse anschauen
ls -lh output/industry_trends/
cat output/industry_trends/ANALYSIS_SUMMARY.md
```

**Laufzeit:** ~2 Sekunden  
**Input:** `data/startups_classified_v2.csv` (1'327 Startups)  
**Output:** 7 CSV-Dateien + 1 Summary

---

## 📊 Die 6 Analysen

### A. Market Share Shift
**Frage:** Welche Industrie gewinnt/verliert Marktanteile?

- Zeigt Anteil jeder Industrie an allen Deals pro Jahr (in %)
- Jede Spalte summiert auf ~100%
- `share_change_pct`: Veränderung 2023 → 2025
- `direction`: '+' (wächst), '-' (schrumpft), '=' (stabil)

**Beispiel:**  
GenAI: 1.8% → 4.1% = +2.3pp → **Winner**  
ClimateTech: 16.9% → 9.8% = -7.1pp → **Loser**

---

### B. Rankings
**Frage:** Wer war #1 in 2023 — ist er es noch in 2026?

- Rank 1 = meiste Deals
- `rank_change`: positiv = aufgestiegen
- `trend`: '↑' aufgestiegen, '↓' abgestiegen, '→' stabil

**Top Aufsteiger:**  
- Robotics: #10 → #5 (+5 Plätze)
- GenAI: #7 → #5 (+2 Plätze)

**Top Absteiger:**  
- Enterprise: #6 → #11 (-5 Plätze)
- SpaceTech: #11 → #14 (-3 Plätze)

---

### C. Funding-Volumen Shift
**Frage:** Welche Industrie bekommt MEHR Geld (auch wenn Deal-Count gleich bleibt)?

- Anteil am Total-Funding pro Jahr
- `funding_change_pp`: Veränderung 2023 → 2025
- `signal`: 
  - 'Grosse Deals ↑' → Funding wächst schneller als Deal-Count
  - 'Viele Deals ↑' → Deal-Count wächst schneller als Funding
  - 'Gleichmässig' → beide wachsen ähnlich

**Wichtige Erkenntnis:**  
- BioTech: 52% → 58% Funding-Anteil (+6pp) — **Grosse Deals!**
- HealthTech: Deal-Share stabil, aber Funding +6pp — **Quality over Quantity**
- ClimateTech: 18.6% → 3.4% Funding (-15.2pp) — **dramatischer Einbruch**

---

### D. Momentum Score
**Frage:** Welche Industrie beschleunigt JETZT gerade?

- Vergleicht frühe 4 Quartale (2023-Q1 bis Q4) vs. späte 4 Quartale (2025-Q3 bis 2026-Q2)
- `momentum_pct`: (recent_avg - earlier_avg) / (earlier_avg + 0.1) × 100
- Klassifikation:
  - `> 50%` → Accelerating 🚀
  - `> 10%` → Growing ↑
  - `-10% bis +10%` → Stable →
  - `< -10%` → Slowing/Declining 📉

**Beispiel:**  
- GenAI: +168% Momentum — **explosive Beschleunigung!**
- Robotics: +109% — **verdoppelt sich gerade**
- SpaceTech: -89% — **quasi tot**

---

### E. Finale Klassifikation
**Frage:** Wo lohnt es sich 2026 zu gründen?

Kombiniert Market Share + Momentum:

| Kategorie | Kriterien | Keywords |
|-----------|-----------|----------|
| **Emerging 🌱** | share_change > +1.5pp UND momentum > 30% | GenAI, Robotics |
| **Growing ↑** | share_change > +0.5pp UND momentum > 10% | MedTech, BioTech |
| **Stable →** | abs(share_change) <= 0.5pp | HealthTech, Ecommerce, PropTech, AgriTech, Cybersecurity |
| **Slowing ↓** | share_change < -0.5pp UND momentum < 10% | FinTech, Enterprise, ClimateTech, EdTech, SpaceTech |

**Direktes Investment-Signal:**  
✅ Gründen in: **Emerging + Growing**  
⚠️ Vorsicht bei: **Slowing**  
❌ Vermeiden: **Declining** (EdTech, SpaceTech)

---

### F. Quartals-Detail
**Frage:** Wie entwickelt sich jede Industrie quartalsweise?

- **F1:** Absolute Deal-Zahlen pro Quartal
- **F2:** Relative Anteile pro Quartal (in %)

Nützlich für:
- Saisonalität erkennen
- Trendbrüche identifizieren
- Detaillierte Visualisierungen

---

## 📂 Output-Struktur

```
output/industry_trends/
├── A_market_share_pct.csv         # Marktanteile % pro Jahr
├── B_rankings_by_year.csv          # Ranking 2023–2026
├── C_funding_share_pct.csv         # Funding-Volumen %
├── D_momentum.csv                  # Momentum-Score
├── E_industry_classification.csv   # Finale Kategorisierung ⭐
├── F1_deal_count_quarterly.csv     # Quartals-Count
├── F2_deal_share_quarterly.csv     # Quartals-Share %
└── ANALYSIS_SUMMARY.md             # Zusammenfassung
```

**Wichtigste Datei:** `E_industry_classification.csv`  
→ Direkte Antwort auf: "Wo gründen 2026?"

---

## 🔍 Wichtigste Erkenntnisse (TL;DR)

### 🚀 Gründer-Empfehlungen 2026

**STRONG BUY:**
1. **GenAI** — +168% Momentum, +2.3pp Market Share
2. **Robotics** — +109% Momentum, größter Ranking-Aufstieg (#10 → #5)

**BUY:**
3. **MedTech** — Wachsend, steigendes Ranking
4. **BioTech** — Größter Markt (30.9%), große Funding-Runden (58% des Volumens)

**AVOID:**
- **ClimateTech** — -7.1pp Market Share, -47% Momentum, -15pp Funding-Anteil
- **SpaceTech** — -89% Momentum, keine neuen Deals 2026

---

## 🛠 Technische Details

### Voraussetzungen
```bash
pip install pandas numpy
```

### Eingabedaten
- **Datei:** `data/startups_classified_v2.csv`
- **Spalten erwartet:**
  - `quarter` (z.B. "2024-Q3")
  - `keyword` (Industrie-Klassifikation)
  - `funding_chf` (optional, für Analyse C)
  - `has_funding` (Boolean, für Analyse C)

### Zeitraum
- **Vollständige Jahre:** 2023, 2024, 2025 (für Jahres-Vergleiche)
- **Alle Jahre:** 2023, 2024, 2025, 2026 (inkl. 2026 für Momentum)
- **Quartale:** 2023-Q1 bis 2026-Q2 (14 Quartale)

### Laufzeit
~2 Sekunden für 1'327 Startups auf einem MacBook

---

## 📈 Next Steps

1. **Visualisierung:** Charts in Tableau oder Python (matplotlib/seaborn)
   - Line Charts für Quartals-Trends
   - Bubble Charts für Market Share vs. Momentum
   - Heatmaps für Quartals-Entwicklung

2. **Deep Dives:**
   - Warum schrumpft ClimateTech so massiv?
   - Welche konkreten GenAI-Startups treiben das Wachstum?
   - BioTech: Welche Sub-Kategorien sind besonders stark?

3. **Geo-Analyse:**
   - Verhalten sich die Trends in der Schweiz anders als in Europa?
   - Unterschiede zwischen Städten (Zürich vs. Lausanne)?

4. **Funding-Stage-Analyse:**
   - Ist GenAI eher Seed oder Series A?
   - BioTech: Early-Stage oder späte Runden?

---

## 📞 Support

Bei Fragen oder Problemen:
1. Logs prüfen (Script gibt detaillierte Ausgaben)
2. CSV-Dateien öffnen und direkt anschauen
3. `ANALYSIS_SUMMARY.md` lesen für interpretierte Ergebnisse

**Happy Analyzing! 🚀**
