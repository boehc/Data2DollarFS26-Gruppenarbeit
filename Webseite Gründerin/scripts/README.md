# Python-Skripte für Datentransformation

Dieser Ordner enthält Python-Skripte, die CSV-Dateien in JSON-Dateien für die Website transformieren.

## Zu erstellende Skripte:

1. **`create_tech_trends.py`**
   - Input: `Lizzy/Trends/Trends_Data/keyword_monthly_normalized.csv`
   - Output: `data/tech_trends.json`
   - Funktion: Tech-Keywords (GenAI, LLM, AgentAI, ...) nach Quartalen aggregieren

2. **`create_industry_trends.py`**
   - Input: `Lizzy/Trends/Trends_Data/keyword_monthly_normalized.csv`
   - Output: `data/industry_trends.json`
   - Funktion: Industry-Keywords (FinTech, HealthTech, ...) nach Quartalen aggregieren

3. **`create_deal_count.py`**
   - Input: `chiara/results/F1_deal_count_quarterly.csv`
   - Output: `data/deal_count.json`
   - Funktion: Deal-Anzahl pro Quartal & Kategorie

4. **`create_funding_share.py`**
   - Input: `chiara/results/C_funding_share_pct.csv`
   - Output: `data/funding_share.json`
   - Funktion: Funding-Volumen (CHF) pro Kategorie

5. **`create_momentum_matrix.py`**
   - Input: `chiara/results/D_momentum.csv`
   - Output: `data/momentum_matrix.json`
   - Funktion: Bubble Chart (Delta Media vs. VC)

6. **`create_co_occurrence.py`**
   - Input: `Lizzy/Trends/Trends_Data/articles_classified_t2.csv`
   - Output: `data/co_occurrence.json`
   - Funktion: Tech × Industry Co-Occurrence Matrix (normalisiert)

7. **`create_mbi_courses.py`**
   - Input: `Curriculum MBI/0_mbi_curriculum_final.csv`
   - Output: `data/mbi_courses.json`
   - Funktion: Kurse mit ECTS, Keywords, Sektoren

8. **`create_ec_domains.py`**
   - Input: Manuell (EntreComp Framework)
   - Output: `data/ec_domains.json`
   - Funktion: 12 EC-Domains mit MBI-Abdeckung

---

## Workflow:

```bash
# 1. Skripte erstellen
python scripts/create_tech_trends.py
python scripts/create_industry_trends.py
python scripts/create_deal_count.py
python scripts/create_funding_share.py
python scripts/create_momentum_matrix.py
python scripts/create_co_occurrence.py
python scripts/create_mbi_courses.py
python scripts/create_ec_domains.py

# 2. Prüfen
ls -lh data/
```

---

## Dependencies:

```bash
pip install pandas numpy
```
