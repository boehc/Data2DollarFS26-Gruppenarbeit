# 🚀 Schnellstart-Anleitung

**Ziel:** In 5 Minuten die wichtigsten Ergebnisse verstehen

---

## ⚡ 30-Sekunden-Überblick

### Schritt 1: Diese Datei zuerst öffnen
```
results/INVESTMENT_RECOMMENDATIONS.csv
```
Zeigt **STRONG BUY / BUY / HOLD / AVOID** für jede Branche.

### Schritt 2: Validierung
```
results/SIMPLE_SUMMARY.csv
```
One-Pager mit allen Branchen auf einen Blick.

---

## 📊 Die wichtigsten Ergebnisse

### Wo gründen? (2026)

| Signal | Branchen | Warum? |
|--------|----------|--------|
| 🟢 **STRONG BUY** | GenAI, Robotics | Stärkstes Momentum (+168%, +109%) |
| 🟢 **BUY** | BioTech, MedTech | Grösste Märkte, stabile Führung |
| 🟡 **HOLD** | HealthTech, Ecommerce | Neutral, keine klare Richtung |
| 🔴 **AVOID** | ClimateTech, FinTech | Sinkende Marktanteile |
| 🔴 **SELL** | SpaceTech, EdTech | Kaum noch Aktivität |

---

## 📁 Welche Datei für welche Frage?

### "Welche Branche wächst am schnellsten?"
→ `D_momentum.csv` oder `MOMENTUM_LEADERS.csv`

### "Wie viele Deals pro Quartal?"
→ `F1_deal_count_quarterly.csv`

### "Wer hat die meisten Marktanteile?"
→ `A_market_share_pct.csv`

### "Komplette Branchen-Übersicht?"
→ `SIMPLE_SUMMARY.csv` (One-Pager)

### "Investment-Entscheidung?"
→ `INVESTMENT_RECOMMENDATIONS.csv`

---

## 🔢 Datengrundlage

| Metrik | Wert |
|--------|------|
| **Analysierte Deals** | 1'327 |
| **Zeitraum** | Q1/2023 – Q1/2026 |
| **Branchen** | 14 |
| **Datenquellen** | Startupticker.ch, Venture Kick |

---

## 📈 Vorgehensweise der Analyse

### Phase 1: Datensammlung
1. **Startupticker.ch** gescraped → 1'564 Artikel
2. **Venture Kick** gescraped → Zusätzliche VC-Daten
3. Weitere Quellen exploriert (Kaggle, YC, VCLense) → Nicht verwendet

### Phase 2: Datenverarbeitung
1. Daten zusammengeführt (`merge_and_clean.py`)
2. Duplikate entfernt
3. LLM-Klassifizierung mit GPT-4 (Branchen-Zuordnung)
4. Qualitätsprüfung

### Phase 3: Analyse
1. Marktanteile pro Branche berechnet
2. Momentum (Veränderung) analysiert
3. Rankings erstellt
4. Investment-Empfehlungen abgeleitet

### Phase 4: Output
16 CSV-Dateien in `results/` mit allen Ergebnissen

---

## ⚠️ Wichtige Hinweise

### Momentum-Definition
- **Momentum** = Veränderung des Marktanteils (nicht absolute Zahlen)
- Beispiel: FinTech hat -12% Momentum = sinkender Marktanteil, obwohl absolute Deals stabil

### GenAI-Kategorie
- "GenAI" = **AI-Native Startups** (Kernprodukt ist KI-basiert)
- Nicht: Startups die KI als Tool verwenden

### Datenstand
- Letztes vollständiges Quartal: Q1/2026
- Q2/2026 nur teilweise erfasst (5 Deals)

---

## 🔗 Weiterführende Dokumente

| Dokument | Zweck |
|----------|-------|
| `PROFESSOR_OVERVIEW.md` | Zusammenfassung für Bewertung (2-3 Min) |
| `EXECUTIVE_SUMMARY.md` | Detaillierte Kernaussagen |
| `CSV_FILES_INDEX.md` | Beschreibung aller CSV-Dateien |
| `../code/CODE_OVERVIEW.md` | Technische Pipeline-Details |

---

*Erstellt: April 2026*
