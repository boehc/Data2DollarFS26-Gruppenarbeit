# 🎯 ACTION PLAN: Pfad A Data Pipeline

**Projekt:** VC/Startup Investment Data Collection  
**Ziel:** 1000+ Datenpunkte für MBI HSG Gruppenprojekt (Europa-Fokus 2020-2026)  
**Status:** ✅ Data Collection Complete - Ready for Merge & Analysis  
**Letzte Aktualisierung:** 02.04.2026

---

## 📊 AKTUELLE DATENLAGE

### ✅ Gesammelte Datenquellen:

| Quelle | Anzahl | Zeitraum | Status | Vollständigkeit |
|--------|--------|----------|--------|-----------------|
| **Kaggle Crunchbase** | 54,294 | 2000-2014 | ✅ Complete | 91% Name, 84% Industry |
| **Y Combinator Europa** | 353 | 2015-2026 | ✅ Complete | 100% Name, 99% Country |
| **Startupticker.ch** | 399 | 2025-2026 | ✅ Complete | 100% Name, 100% Industry, 40% Investors |
| **TOTAL** | **55,046** | 2000-2026 | ✅ Ready | Alle 16 Felder vorhanden |

### 🎯 Ziele erreicht:
- ✅ **1000+ Datenpunkte:** 55,046 Startups (5500% Übererfüllung!)
- ✅ **Europa-Fokus:** 752 aktuelle europäische Startups (2015-2026)
- ✅ **Schweiz-Daten:** 399 Schweizer Startups mit Investor-Details
- ✅ **Alle 16 Felder:** Vollständig implementiert in allen Quellen

---

## 📋 PHASE 1: SETUP & VORBEREITUNG ✅ ABGESCHLOSSEN

### ✅ 1.1 Python Environment Setup
### ✅ 1.1 Python Environment Setup
- ✅ Python 3.9.6 verfügbar
- ✅ Workspace-Ordner erstellt
- ✅ Terminal-Zugriff konfiguriert

---

### ✅ 1.2 Dependencies Installiert
- ✅ selenium==4.36.0 (Web Scraping)
- ✅ webdriver-manager==4.0.2 (Chrome Driver)
- ✅ pandas==2.3.3 (Datenverarbeitung)
- ✅ kaggle (API Client)
- ✅ beautifulsoup4, requests, lxml

---

### ✅ 1.3 Kaggle API Key Eingerichtet
- ✅ Account: boehccc
- ✅ Token: KGAT_629fe78ca3fc5b842bf4dabdfb1b9af6
- ✅ Authentication erfolgreich
- ✅ Dataset-Download funktioniert

---

## 📊 PHASE 2: DATEN SAMMELN ✅ ABGESCHLOSSEN

### ✅ 2.1 Kaggle Crunchbase Dataset

**Script:** `1_kaggle_downloader.py`

**Ergebnis:**
- ✅ 54,294 Startups heruntergeladen
- ✅ Zeitraum: 2000-2014 (Peak: 2012 mit 5,211 Startups)
- ✅ Alle 16 Felder gemappt und validiert
- ✅ Output: `data/kaggle_crunchbase.csv`

**Datenqualität:**
- Startup_Name: 91.1%
- Industry: 83.8%
- Funding_Amount: 91.1%
- Country: 81.3%
- Year: 70.9%

**Limitierung:** Nur historische Daten bis 2014

---

### ✅ 2.2 Y Combinator Europa Scraper

**Script:** `3_yc_scraper_europa.py`

**Strategie:**
- ✅ URL-Filter: `?regions=Europe` für Europa-Startups
- ✅ Aggressives Scrolling (40 Scrolls) für Lazy Loading
- ✅ Parsing: Name+Location, Batch→Year, Industry, Sub-Industry
- ✅ Filter: Year >= 2015 für aktuelle Daten

**Ergebnis:**
- ✅ 353 europäische Startups gescraped
- ✅ Zeitraum: 2015-2026 (Peak: 2021 mit 90 Startups)
- ✅ Output: `data/yc_companies.csv`

**Datenqualität:**
- Startup_Name: 100%
- Country: 99.4%
- Industry: 93.5%
- Investor_Name: 100% (Y Combinator)

**Top Länder:**
- UK: 134 Startups
- France: 53 Startups
- Germany: 41 Startups
- Switzerland: 10 Startups

---

### ✅ 2.3 Startupticker.ch Schweizer Startups

**Script:** `5_startupticker_scraper_v2.py`

**Features:**
- ✅ Pagination: 50 Seiten News durchsucht
- ✅ Detail-Scraping: 400 Artikel mit Investor-Extraktion
- ✅ Industry-Mapping: Aus Tags + Titel-Keywords
- ✅ Investment_Stage: Dynamisch aus Funding-Amount
- ✅ Investor-Extraktion: Regex-Patterns ("led by X", "from Y")
- ✅ Filter: 2020-2026

**Ergebnis:**
- ✅ 399 Schweizer Startups
- ✅ Zeitraum: 2025-2026 (primär 2026)
- ✅ Output: `data/startupticker_startups.csv`

**Datenqualität:**
- Startup_Name: 100%
- Industry: 100% (B2B: 278, Healthcare: 81, Fintech: 24)
- Investment_Stage: 100% (Early Stage: 236, Series C+: 66, Series A: 36)
- Investor_Name: 40.4% (161 Investors extrahiert!)
- Funding_Amount: 41.1%

**Innovation:** Einzige Quelle mit echten Investor-Namen aus News-Artikeln!

---

## � PHASE 3: MERGE & CLEAN (NÄCHSTER SCHRITT)

### ⚙️ 3.1 Datensätze Zusammenführen

**Script:** `4_merge_and_clean.py` (bereits vorbereitet)

**Aufgaben:**
```bash
python3 4_merge_and_clean.py
```

**Was das Script macht:**
1. Lädt alle 3 CSV-Dateien:
   - `kaggle_crunchbase.csv` (54,294 Zeilen)
   - `yc_companies.csv` (353 Zeilen)
   - `startupticker_startups.csv` (399 Zeilen)

2. Kombiniert alle Daten (Total: ~55,046 Zeilen)

3. Ableitung fehlender Felder:
   - `Business_Model_Type` aus Industry/Keywords (B2B/B2C/B2B2C/Marketplace)
   - `Investor_Type` aus Stage/Funding (VC Fund/Angel/Corporate VC/etc.)

4. Deduplizierung:
   - Entfernt Duplikate basierend auf Startup_Name + Year
   - Priorisiert neueste/vollständigste Einträge

5. Data Cleaning:
   - Normalisiert Country-Namen (USA/United States → USA)
   - Standardisiert Funding-Amounts (alle in Millionen)
   - Vereinheitlicht Investment_Stages

6. Output: `data/final_dataset.csv`

**Erwartetes Ergebnis:**
- ~53,000-55,000 finale Datenpunkte (nach Deduplizierung)
- Alle 16 Felder befüllt (wo möglich)
- Europa-Anteil: ~1-2% (aber mit aktuellen 2015-2026 Daten!)

---

### ⚙️ 3.2 Optionale Filter-Varianten erstellen

**Mögliche Analysen:**
```bash
# Nur Europa 2015-2026 (für aktuelle Analyse)
python3 -c "import pandas as pd; df = pd.read_csv('data/final_dataset.csv'); eu_df = df[(df['Year'] >= 2015) & (df['Country'].isin(['UK', 'France', 'Germany', 'Switzerland', 'Spain', 'Netherlands', 'Denmark', 'Sweden', 'Norway', 'Italy']))]; eu_df.to_csv('data/europa_2015_2026.csv', index=False); print(f'✓ {len(eu_df)} Europa-Startups (2015-2026) gespeichert')"

# Nur Schweiz
python3 -c "import pandas as pd; df = pd.read_csv('data/final_dataset.csv'); ch_df = df[df['Country'] == 'Switzerland']; ch_df.to_csv('data/switzerland_only.csv', index=False); print(f'✓ {len(ch_df)} Schweizer Startups gespeichert')"

# High-Value Deals (>10M USD)
python3 -c "import pandas as pd; df = pd.read_csv('data/final_dataset.csv'); df['Amount_Numeric'] = df['Funding_Amount'].str.extract('(\d+\.?\d*)').astype(float); high_df = df[df['Amount_Numeric'] > 10]; high_df.to_csv('data/high_value_deals.csv', index=False); print(f'✓ {len(high_df)} High-Value Deals gespeichert')"
```

---

## ✅ PHASE 4: QUALITY CONTROL

### ⚙️ 4.1 Datenqualität Validieren

**Checks durchführen:**
```bash
python3 -c "
import pandas as pd

df = pd.read_csv('data/final_dataset.csv')

print('='*60)
print('DATENQUALITÄT FINAL DATASET')
print('='*60)

print(f'\n📊 Gesamtanzahl: {len(df):,} Zeilen')

print(f'\n📅 Zeitraum:')
print(f'  Ältestes Jahr: {df[\"Year\"].min():.0f}')
print(f'  Neuestes Jahr: {df[\"Year\"].max():.0f}')

print(f'\n🌍 Top 10 Länder:')
print(df['Country'].value_counts().head(10))

print(f'\n💰 Investment Stages:')
print(df['Investment_Stage'].value_counts())

print(f'\n🏭 Top 10 Industries:')
print(df['Industry'].value_counts().head(10))

print(f'\n✅ Vollständigkeit (% nicht-NULL):')
for col in df.columns:
    pct = (df[col].notna().sum() / len(df) * 100)
    print(f'  {col}: {pct:.1f}%')

# Europa-Statistik
eu_countries = ['UK', 'France', 'Germany', 'Switzerland', 'Spain', 'Netherlands', 
                'Denmark', 'Sweden', 'Norway', 'Italy', 'Belgium', 'Austria']
eu_df = df[df['Country'].isin(eu_countries)]
eu_recent = eu_df[eu_df['Year'] >= 2015]

print(f'\n🇪🇺 Europa-Daten:')
print(f'  Gesamt: {len(eu_df):,} Startups')
print(f'  2015-2026: {len(eu_recent):,} Startups')
print(f'  Anteil am Dataset: {len(eu_df)/len(df)*100:.1f}%')
"
```

**Erwartete Werte:**
- ✓ Gesamtanzahl: 53,000-55,000
- ✓ Zeitraum: 2000-2026
- ✓ Vollständigkeit Startup_Name: >90%
- ✓ Vollständigkeit Year: >70%
- ✓ Europa 2015-2026: 700-800 Startups

---

### ⚙️ 4.2 Sample-Daten Prüfen

**Erste 10 Zeilen anschauen:**
```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/final_dataset.csv'); print(df.head(10).to_string())"
```

**Zufällige 10 Zeilen:**
```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/final_dataset.csv'); print(df.sample(10).to_string())"
```

**Europa-Sample:**
```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/final_dataset.csv'); eu = df[df['Country'].isin(['UK', 'France', 'Germany', 'Switzerland'])]; print(eu.sample(min(10, len(eu))).to_string())"
```

---

## 📝 PHASE 5: DOKUMENTATION

### ⚙️ 5.1 README.md vervollständigen

**Ergänze im README.md:**
- [x] Finale Daten-Statistiken
- [x] Verwendete Datenquellen mit Links
- [x] Datenqualität pro Quelle
- [x] Bekannte Limitierungen
- [x] Verwendungshinweise

---

### ⚙️ 5.2 Data Dictionary erstellen

**Erstelle `DATA_DICTIONARY.md`:**
```markdown
# Data Dictionary - VC/Startup Investment Dataset

## Datei: final_dataset.csv

### Felder (16 total):

1. **Startup_Name** (String)
   - Name des Startups
   - Quelle: Alle Quellen
   - Vollständigkeit: ~95%

2. **Industry** (String)
   - Haupt-Industrie (z.B. FINTECH, HEALTHCARE, B2B)
   - Quelle: Alle Quellen, teilweise abgeleitet
   - Vollständigkeit: ~85%

[... fortsetzung für alle 16 Felder ...]
```

---

## 🎓 PHASE 6: ANALYSE-VORBEREITUNG

### ⚙️ 6.1 Jupyter Notebook Setup (Optional)

**Für interaktive Analyse:**
```bash
pip3 install jupyter matplotlib seaborn

jupyter notebook
```

**Erstelle `analysis.ipynb` mit:**
- Daten laden und explorieren
- Zeitreihen-Analysen (Funding-Trends über Jahre)
- Geographische Verteilung (Europa vs Rest)
- Industry-Trends
- Investor-Analyse

---

### ⚙️ 6.2 Beispiel-Analysen

**Funding-Trend über Zeit:**
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/final_dataset.csv')

# Anzahl Deals pro Jahr
yearly = df.groupby('Year').size()
yearly.plot(kind='bar', figsize=(15,6))
plt.title('Startup Funding Deals pro Jahr')
plt.xlabel('Jahr')
plt.ylabel('Anzahl Deals')
plt.savefig('output/deals_per_year.png')
plt.show()
```

**Europa vs USA:**
```python
# Top Länder
top_countries = df['Country'].value_counts().head(10)
top_countries.plot(kind='barh', figsize=(10,6))
plt.title('Top 10 Länder nach Startup-Anzahl')
plt.xlabel('Anzahl Startups')
plt.savefig('output/top_countries.png')
plt.show()
```

**Investment Stages:**
```python
# Stage Distribution
stages = df['Investment_Stage'].value_counts()
stages.plot(kind='pie', autopct='%1.1f%%', figsize=(10,10))
plt.title('Verteilung Investment Stages')
plt.savefig('output/investment_stages.png')
plt.show()
```

---

## 🚀 NÄCHSTE SCHRITTE

### Sofort ausführen:
1. ⚙️ **Merge & Clean:** `python3 4_merge_and_clean.py`
2. ⚙️ **Quality Check:** Validierungs-Scripts ausführen
3. ⚙️ **Sample prüfen:** Erste Zeilen anschauen

### Für die Projektarbeit:
1. 📊 **Analyse-Fragen definieren** (Was wollt ihr herausfinden?)
2. 📈 **Visualisierungen erstellen** (Charts, Grafiken)
3. 📝 **Insights dokumentieren** (Key Findings)
4. 🎯 **Präsentation vorbereiten** (Für MBI HSG)

---

## 🆘 TROUBLESHOOTING

### Problem: Kaggle Dataset nicht verfügbar
**Lösung:** Alternative Datasets:
- `startup-investments` von anderen Autoren
- `crunchbase-data` (verschiedene Versionen)
- Notfalls: YC + VCLense reichen für >1000 Datenpunkte

### Problem: VCLense scraped keine Daten
**Lösung:** Normal! Website ist dynamisch. Nutze Kaggle + YC.

### Problem: ChromeDriver startet nicht
**Lösung:**
```bash
# Mac
brew install chromedriver

# Linux
sudo apt-get install chromium-chromedriver

# Manual Download
# https://chromedriver.chromium.org/downloads
```

### Problem: "Module not found" Fehler
**Lösung:**
```bash
pip3 install <module_name>
# oder
pip3 install -r requirements.txt
```

### Problem: Merge Script Fehler
**Lösung:** Prüfe ob alle CSVs existieren:
```bash
ls -lh data/*.csv
```

Fehlende CSVs? Führe entsprechende Scraper nochmal aus.

---

## 📊 ERWARTETE OUTPUTS

### Dateien im `data/` Ordner:
  - Year: 93.5%

Top Länder (Europa):
  🇬🇧 United Kingdom: 134 Startups
  🇫🇷 France: 53
  🇩🇪 Germany: 41
  🇪🇸 Spain: 16
  🇩🇰 Denmark: 14
  🇳🇱 Netherlands: 10
  🇨🇭 Switzerland: 10
  🇸🇪 Sweden: 9
  🇮🇪 Ireland: 8

Jahresverteilung (neueste zuerst):
  2025: 7 Startups
  2024: 24 Startups
  2023: 37 Startups
  2022: 61 Startups
  2021: 90 Startups (Peak!)
  2020: 33 Startups
  2015-2019: 68 Startups
```

**Verbesserungen:**
- ✅ Europa-Filter direkt auf YC-Website genutzt (`?regions=Europe`)
- ✅ Aggressives Scrolling (40 Scrolls) um ALLE Companies zu laden
- ✅ Automatische Filterung nach Jahr (ab 2015)
- ✅ 353 statt 11 europäische Startups! (32x mehr Daten)
- ✅ Perfekt für "Pfad A: Gründen" - aktuellste europäische Startup-Daten

---

## 🔄 PHASE 3: DATEN ZUSAMMENFÜHREN & BEREINIGEN

### ☐ 3.1 Merge, Clean & Enrich
```bash
python3 4_merge_and_clean.py
```

**Was du tun musst:**
- [ ] Befehl ausführen
- [ ] Verarbeitungs-Steps beobachten
- [ ] Summary studieren
- [ ] Prüfen: `data/final_dataset.csv` existiert

**Erwartete Ausgabe:**
```
============================================================
MERGE, CLEAN & ENRICH
============================================================
Lade Datasets...
  ✓ Kaggle/Crunchbase: XXXX Zeilen
  ✓ VCLense: XX Zeilen
  ✓ Y Combinator: XXX Zeilen

Normalisiere Spalten...
  ✓ Kaggle: XXXX Zeilen normalisiert
  ✓ VCLense: XX Zeilen normalisiert
  ✓ YC: XXX Zeilen normalisiert

Führe Datasets zusammen...
  ✓ Kombiniert: XXXX Zeilen

Reichere Daten an...
  ✓ Investor_Type: XXX Werte abgeleitet
  ✓ Business_Model_Type: XXX Werte abgeleitet
  ✓ Year: XX Werte aus Founding_Year abgeleitet

Entferne Duplikate...
  ✓ XX Duplikate entfernt (XXXX → XXXX Zeilen)


| Datei | Größe | Zeilen | Beschreibung |
|-------|-------|--------|--------------|
| `kaggle_crunchbase.csv` | ~15 MB | 54,294 | Historische Crunchbase-Daten (2000-2014) |
| `yc_companies.csv` | ~100 KB | 353 | Europäische YC Startups (2015-2026) |
| `startupticker_startups.csv` | ~150 KB | 399 | Schweizer Startups mit Investor-Details (2025-2026) |
| `final_dataset.csv` | ~15 MB | ~54,000 | **Finales Merged Dataset** (nach Deduplizierung) |

---

## ✅ ERFOLGS-KRITERIEN

### Hauptziele:
- ✅ **1000+ Datenpunkte:** 55,046 Startups gesammelt (5500% Übererfüllung)
- ✅ **16 Datenfelder:** Alle implementiert und validiert
- ✅ **Europa-Fokus:** 752 aktuelle europäische Startups (2015-2026)
- ✅ **Schweiz-Daten:** 399 CH-Startups mit 40% Investor-Coverage
- ✅ **Aktuelle Daten:** 2020-2026 Timeframe abgedeckt

### Datenqualität-Benchmarks:
- ✅ Startup_Name: >90% Vollständigkeit (erreicht: 91-100%)
- ✅ Industry: >80% Vollständigkeit (erreicht: 84-100%)
- ✅ Year: >70% Vollständigkeit (erreicht: 71-100%)
- ✅ Country: >80% Vollständigkeit (erreicht: 81-100%)
- ✅ Funding_Amount: >40% Vollständigkeit (erreicht: 41-91%)

---

## 🎯 VERWENDUNG FÜR PROJEKTARBEIT

### Empfohlene Analysen:

**1. Europa-Fokussierte Analyse (2020-2026):**
```python
# Filtere auf Europa + aktuelle Jahre
eu_countries = ['UK', 'France', 'Germany', 'Switzerland', 'Spain', 
                'Netherlands', 'Denmark', 'Sweden', 'Norway', 'Italy']
eu_recent = df[(df['Year'] >= 2020) & (df['Country'].isin(eu_countries))]

# Analysiere:
# - Funding-Trends pro Jahr
# - Top Industries in Europa
# - Investment Stages Distribution
# - Schweiz vs andere EU-Länder
```

**2. Investor-Landscape (Schweiz):**
```python
# Nutze Startupticker-Daten (einzige Quelle mit Investor-Namen!)
ch_df = df[df['Country'] == 'Switzerland']

# Analysiere:
# - Top Investors in der Schweiz
# - Average Funding Amount pro Stage
# - Co-Investment Patterns
```

**3. Industry-Trends:**
```python
# Vergleiche historisch (2000-2014) vs aktuell (2015-2026)
historical = df[df['Year'] < 2015]
current = df[df['Year'] >= 2015]

# Analysiere:
# - Welche Industries wachsen?
# - Neue Industries (AI, Climate Tech)?
# - Geografische Shifts (Europa gaining ground?)
```

---

## 📞 SUPPORT & RESSOURCEN

### Bei Fragen:
- 📖 **README.md:** Projekt-Übersicht und Quick Start
- 📊 **DATENQUELLEN_ANALYSE.md:** Details zu allen Datenquellen
- 🐛 **Troubleshooting:** Siehe Abschnitt oben

### Nützliche Links:
- Kaggle API Docs: https://www.kaggle.com/docs/api
- Selenium Docs: https://selenium-python.readthedocs.io/
- Pandas Cheat Sheet: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf

---

**Erstellt:** 01.04.2026  
**Letzte Aktualisierung:** 02.04.2026  
**Status:** ✅ Data Collection Complete - Ready for Analysis

- [ ] Startup_Name Spalte gefüllt (keine leeren Felder)?
- [ ] Business_Model_Type kategorisiert (SaaS, Marketplace, Fintech, etc.)?
- [ ] Investor_Type klassifiziert (VC Fund, Angel, Accelerator, etc.)?

---

### ☐ 4.3 Quick Data Analysis (Optional)

**Python Console:**
```python
import pandas as pd
df = pd.read_csv('data/final_dataset.csv')

print(f"Total Rows: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nBusiness Models:\n{df['Business_Model_Type'].value_counts()}")
print(f"\nTop 10 Countries:\n{df['Country'].value_counts().head(10)}")
print(f"\nInvestor Types:\n{df['Investor_Type'].value_counts()}")
```

- [ ] Befehl ausführen
- [ ] Verteilung analysieren

---

## 🎓 PHASE 5: DOKUMENTATION & ABGABE

### ☐ 5.1 Datenqualität Dokumentieren

**Erstelle:** `DATA_QUALITY_REPORT.md`

Inhalt:
```markdown
# Data Quality Report - Pfad A: Gründen

**Datum:** 2. April 2026
**Team:** [Euer Team]

## Übersicht
- **Total Datenpunkte:** XXXX
- **Quellen:** Kaggle (Crunchbase), VCLense.ch, Y Combinator
- **Zeitraum:** [ältestes Jahr] - [neuestes Jahr]

## Vollständigkeit
- Startup_Name: 100%
- Industry: XX%
- Funding_Amount: XX%
- Country: XX%
...

## Datenverteilung
- Top Business Models: SaaS (XX%), Marketplace (XX%), ...
- Top Countries: USA (XX%), UK (XX%), Switzerland (XX%), ...
- Top Investor Types: VC Fund (XX%), Angel (XX%), ...

## Herausforderungen
- VCLense Scraping: [funktioniert/hat nicht funktioniert wegen...]
- YC Scraping: [Anzahl Companies extrahiert]
- Duplikate entfernt: XX

## Fazit
✅ Ziel von 1000+ Datenpunkten erreicht
```

- [ ] Report erstellt
- [ ] Zahlen eingefügt

---

### ☐ 5.2 Git Commit & Push (Optional)

```bash
git add pfad_a_scraper/
git commit -m "Add Pfad A: VC/Startup Investment Data Pipeline - 1000+ datapoints"
git push origin main
```

- [ ] Changes commited
- [ ] Zu GitHub gepusht

---

### ☐ 5.3 Final Checklist

**Deliverables:**
- [ ] `data/final_dataset.csv` mit 1000+ Zeilen
- [ ] Alle 16 Spalten korrekt befüllt
- [ ] README.md mit Setup-Anleitung
- [ ] Alle 4 Python Scripts funktionsfähig
- [ ] Data Quality Report (optional)

**Code Quality:**
- [ ] Scripts laufen ohne Fehler
- [ ] Error Handling funktioniert
- [ ] Progress-Ausgaben vorhanden
- [ ] Docstrings in allen Funktionen

---

## 🚨 TROUBLESHOOTING

### Problem: Kaggle Dataset nicht gefunden
**Lösung:**
1. Alternativ-Dataset verwenden: `thomaskonstantin/top-270-companies-evolution`
2. In `1_kaggle_downloader.py` Zeile 56 ändern zu:
   ```python
   dataset_name = 'thomaskonstantin/top-270-companies-evolution'
   ```

### Problem: VCLense/YC liefern keine Daten
**Lösung:**
- Das ist OK! Kaggle alleine liefert 1000+ Datenpunkte
- Leere CSVs werden trotzdem erstellt (korrekte Struktur)
- Script 4 merged alle verfügbaren Daten

### Problem: ChromeDriver Error
**Lösung Mac:**
```bash
brew install chromedriver
```

**Lösung Ubuntu/Linux:**
```bash
sudo apt-get install chromium-chromedriver
```

### Problem: pip install schlägt fehl
**Lösung:**
```bash
pip3 install --upgrade pip
pip3 install --user -r requirements.txt
```

### Problem: "Module not found" beim Ausführen
**Lösung:**
```bash
# Prüfe Python Version
python3 --version

# Prüfe installierte Pakete
pip3 list | grep pandas

# Reinstall
pip3 install --force-reinstall pandas
```

---

## 📞 HILFE BENÖTIGT?

**Bei technischen Problemen:**
1. Fehlermeldung komplett kopieren
2. GitHub Copilot fragen: "Ich habe folgenden Fehler: [paste error]"
3. Stack Overflow durchsuchen

**Bei Daten-Problemen:**
1. Prüfe `data/` Ordner-Inhalte
2. Öffne CSV in Excel zur Inspektion
3. Laufe Script 4 nochmal (merged alle verfügbaren Daten)

---

## ✨ SUCCESS CRITERIA

✅ **Minimum Goal:** 1000+ Datenpunkte in `final_dataset.csv`  
✅ **Alle 16 Spalten** vorhanden und teilweise befüllt  
✅ **Scripts laufen** ohne kritische Fehler  
✅ **Dokumentation** ist verständlich  

**Bonus:**
- 🌟 > 2000 Datenpunkte
- 🌟 Alle 3 Datenquellen erfolgreich
- 🌟 > 80% Vollständigkeit in Key-Spalten (Startup_Name, Industry, Country)

---

**🎯 LOS GEHT'S! Starte mit Phase 1.1** ☝️
