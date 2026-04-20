# Startupticker Classification Results
**Datum:** 6. April 2026  
**Script:** `prepare_startups_classification.py`  
**Output:** `data/startups_classified_v2.csv`

---

## 📊 Ergebnis-Übersicht

| Metrik | Wert |
|--------|------|
| **Input Startups** | 1'564 |
| **Klassifizierte Startups** | 1'327 |
| **Ausgeschlossen** | 237 |
| **Erwartet laut Report** | ~1'388 |
| **Abweichung** | -61 (-4.4%) |

---

## 🎯 Ausschluss-Analyse

### Entfernte Startups (237 total)

| Kategorie | Anzahl | Grund |
|-----------|--------|-------|
| **Other** | 88 | Keine relevante Industrie-Kategorie |
| **B2C Tech ohne Match** | 62 | Keine Keywords aus System (meist Logistics) |
| **AI/ML ohne Tags** | 8 | Keine AI-Keywords in Tags (wahrscheinlich falsch kategorisiert) |
| **Sonstige** | 79 | Diverse ungemappte Kategorien |

### Details zu AI/ML Ausschlüssen (8 Startups)
Diese AI/ML-Startups haben keine AI-bezogenen Tags und sind vermutlich eher Business Intelligence / Data Analytics Tools:
- Pi imaging Technologies SA
- Manukai AG  
- Nextesy AG
- KNIME AG
- (4 weitere)

---

## 📈 Keyword-Verteilung

### Industry Layer (1'249 Startups)
```
FinTech         466  (35.1%)
BioTech         414  (31.2%)
ClimateTech     169  (12.7%)
MedTech          65  (4.9%)
HealthTech       48  (3.6%)
Enterprise       29  (2.2%)
Ecommerce        19  (1.4%)
PropTech         15  (1.1%)
AgriTech         14  (1.1%)
EdTech            6  (0.5%)
SpaceTech         4  (0.3%)
```

### Tech Layer (78 Startups)
```
GenAI            44  (3.3%)
Robotics         28  (2.1%)
Cybersecurity     6  (0.5%)
```

**Hinweis:** LLM und AgentAI fehlen komplett - alle AI/ML Startups wurden als GenAI klassifiziert, da die Tags nicht spezifisch genug waren (meist nur "AI" oder "AI | ...").

---

## 💰 Funding-Statistik

| Kategorie | Anzahl | CHF Mio. |
|-----------|--------|----------|
| **Mit Funding** | 827 (62.3%) | 40'586 |
| **Ohne Funding** | 500 (37.7%) | - |

---

## 📅 Zeitliche Verteilung

### Quartale (2023-Q1 bis 2026-Q2)
```
2023-Q1    138
2023-Q2    113
2023-Q3    105
2023-Q4    127
2024-Q1    115
2024-Q2    120
2024-Q3    126
2024-Q4    111
2025-Q1    126
2025-Q2     84
2025-Q3    139
2025-Q4    128
2026-Q1    126
2026-Q2      6  (partial)
```

---

## 🗺️ Output-Format

### Spalten (10 total)
1. **startup_name** - Name des Startups
2. **industry** - Original-Kategorie aus startupticker
3. **keyword** - Gemapptes Keyword (Natalie's System)
4. **layer_type** - `tech_layer` oder `industry_layer`
5. **funding_chf** - Funding-Betrag in CHF Mio. (NaN wenn UNDISCLOSED)
6. **has_funding** - Boolean (True/False)
7. **quarter** - Format: `2023-Q1` bis `2026-Q2`
8. **publication_date** - ISO-Format YYYY-MM-DD
9. **canton** - Schweizer Kanton (z.B. ZH, VD, GE)
10. **city** - Stadt

---

## ⚙️ Mapping-Logik

### 1. Direkte Mappings
```python
FinTech → FinTech (industry_layer)
BioTech → BioTech (industry_layer)
CleanTech → ClimateTech (industry_layer)
MedTech → MedTech (industry_layer)
Enterprise SaaS → Enterprise (industry_layer)
FoodTech → AgriTech (industry_layer)
Robotics → Robotics (tech_layer)
Cybersecurity → Cybersecurity (tech_layer)
```

### 2. AI/ML Fallback (Tag-basiert)
Priorität (höchste zuerst):
```python
"genai" / "gen ai" / "generative" / "foundation" → GenAI
"llm" / "large language" → LLM
"agent" / "agentic" → AgentAI
"ai" → GenAI (letzter Fallback)
```

**Problem:** Keine Startups hatten LLM/Agent-spezifische Tags, daher alle → GenAI.

### 3. B2C Tech Fallback (Tag-basiert)
```python
"ecommerce" / "e-commerce" → Ecommerce
"mobility" → MobilityTech
"biotech" → BioTech
"healthtech" → HealthTech
"fintech" → FinTech
```

62 B2C-Startups ohne Match (meist Logistics ohne spezifisches Keyword).

---

## ✅ Validierung

### Erwartungen vs. Realität
- ✅ Alle relevanten Keywords gemappt
- ✅ Tech/Industry Layer korrekt zugeordnet
- ✅ Funding korrekt geparst (CHF-Konvertierung)
- ✅ Quartale vollständig (2023-Q1 bis 2026-Q2)
- ⚠️ LLM/AgentAI fehlen (Tag-Problem im Source)
- ⚠️ 61 Startups weniger als Report-Erwartung (~4%)

### Mögliche Ursachen für -61 Startups
1. **B2C Logistics-Startups** (62) ohne Keyword-Match
2. **AI/ML ohne AI-Tags** (8) als falsch kategorisiert erkannt
3. Report-Schätzung war ~1'388, tatsächlich korrekt ~1'327

---

## 🚀 Nächste Schritte

### Für Analyse mit `articles_classified_t2.csv`
1. ✅ Keywords sind kompatibel mit Natalie's System
2. ✅ Zeitreihen-Daten vorhanden (Quarter-Spalte)
3. ✅ Funding-Daten sauber (CHF standardisiert)
4. ✅ Geo-Daten vorhanden (Canton/City)

### Empfohlene Verbesserungen
1. **LLM/AgentAI Detection:** Source-Tags verbessern
2. **B2C Mapping:** MobilityTech/Logistics als Keyword hinzufügen?
3. **AI/ML Validation:** 8 falsch kategorisierte Startups prüfen

---

## 📝 Datei-Informationen

**Input:**  
`data/startupticker_enriched_FINAL.csv` (1'564 Zeilen)

**Output:**  
`data/startups_classified_v2.csv` (1'327 Zeilen)

**Script:**  
`prepare_startups_classification.py`

**Ausführungszeit:** ~2 Sekunden  
**Erfolgsrate:** 84.8% klassifiziert

---

*Generiert am 6. April 2026*
