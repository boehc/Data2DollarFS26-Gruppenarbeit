# Pfad A: Gründen - VC/Startup Investment Data Pipeline

Daten-Pipeline für MBI HSG Gruppenprojekt zur Sammlung von VC/Startup-Investitionsdaten.

## Setup

### 1. Kaggle API Key einrichten

1. Gehe zu [kaggle.com](https://www.kaggle.com)
2. Login → Account → API → "Create New API Token"
3. Download `kaggle.json` Datei
4. **Option A**: Platziere `kaggle.json` in `~/.kaggle/kaggle.json` (Linux/Mac) oder `C:\Users\<Windows-Username>\.kaggle\kaggle.json` (Windows)
5. **Option B**: Erstelle `.env` Datei im Projektordner:
   ```
   KAGGLE_USERNAME=dein_username
   KAGGLE_KEY=dein_api_key
   ```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Scripts ausführen (in dieser Reihenfolge)

```bash
# Schritt 1: Kaggle Dataset herunterladen
python 1_kaggle_downloader.py

# Schritt 2: VCLense.ch scrapen
python 2_vclense_scraper.py

# Schritt 3: Y Combinator scrapen
python 3_yc_scraper.py

# Schritt 4: Daten mergen und bereinigen
python 4_merge_and_clean.py
```

## Output

Final dataset: `data/final_dataset.csv` mit 1000+ Datenpunkten

### Felder im finalen Dataset:
- Startup_Name
- Industry
- Sub_Industry
- Business_Model_Type
- Tech_Keywords
- Year
- Funding_Amount
- Funding_Round
- Investor_Type
- Investor_Name
- Country
- Founding_Year
- Investment_Stage
- Valuation
- Exit_Type
- Startup_Stage

## Hinweise

- Alle Scripts können einzeln ausgeführt werden
- Progress wird auf der Konsole angezeigt
- Fehlerbehandlung ist implementiert
- Respektvolle Scraping-Delays sind eingebaut
