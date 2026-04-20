# 📊 DATENQUELLEN-ANALYSE: Aktuelle Europa VC-Daten (2015-2026)

**Datum:** 2. April 2026  
**Ziel:** 1000+ aktuelle Startup/VC Datenpunkte für Europa (letzte 10 Jahre)

---

## ✅ VERFÜGBARE DATENQUELLEN

### 🎯 **TIER 1: Empfohlene Quellen (Kostenlos + Aktuell)**

#### 1. **Crunchbase (via Kaggle) - Alternative Datasets**
- ❌ **Unser aktuelles Dataset**: Nur bis 2014
- ✅ **Alternative auf Kaggle suchen**:
  - `startups-2024` 
  - `european-startups`
  - `tech-startups-funding`
  
**Action:** Neue Kaggle Datasets durchsuchen

---

#### 2. **Y Combinator Companies** ⭐ BESTE OPTION
- **URL:** https://www.ycombinator.com/companies
- **Daten:** 5000+ Companies, viele 2015-2024
- **Europa-Anteil:** ~15-20% (ca. 750-1000 Companies)
- **Felder verfügbar:**
  - ✓ Startup Name
  - ✓ Industry (Tags)
  - ✓ Year (Batch → Jahr)
  - ✓ Country/Location
  - ✓ Stage (YC Batch = Seed/Early)
  - ✓ Website
- **Status:** Bereits implementiert in `3_yc_scraper.py`

**Action:** ✅ Scraper ausführen → Filter auf Europa

---

#### 3. **VCLense.ch** 🇨🇭 
- **URL:** https://dashboard.vclense.ch/
- **Fokus:** Schweizer Startup-Ökosystem
- **Daten:** 200-500 Swiss Startups
- **Zeitraum:** Meist 2015-2024
- **Felder:**
  - ✓ Startup Name
  - ✓ Funding Amount
  - ✓ Industry
  - ✓ Investor Name
  - ✓ Investment Stage
- **Status:** Bereits implementiert in `2_vclense_scraper.py`

**Action:** ✅ Scraper ausführen

---

#### 4. **Dealroom.co** (Limited Free Access)
- **URL:** https://dealroom.co
- **Fokus:** Europa Tech Ecosystem
- **Daten:** 10.000+ European Startups
- **Problem:** ⚠️ Benötigt Account, oft hinter Paywall
- **Alternative:** Public Company Lists durchsuchen

**Action:** ⚠️ Manuell prüfen, ob öffentliche Listen verfügbar

---

#### 5. **Tracxn** (via Public Reports)
- **URL:** https://tracxn.com
- **Reports:** Veröffentlicht öffentliche Sektor-Reports
- **Fokus:** Europa, Unicorns, Exits
- **Problem:** Meist nur Top-Companies (Unicorns)

**Action:** ⚠️ PDF Reports als Ergänzung

---

#### 6. **EU-Startups.com** 
- **URL:** https://www.eu-startups.com
- **Daten:** Funding Announcements, News
- **Zeitraum:** 2015-2024
- **Format:** News Articles → Muss geparst werden
- **Umfang:** 500-1000 Companies

**Action:** ⚙️ Optional: News-Artikel scrapen

---

#### 7. **PitchBook (via University Access)**
- **Status:** ⭐ Premium, aber oft via Uni-Zugang
- **Coverage:** Beste Europa-Abdeckung
- **HSG:** Evtl. Zugang über HSG Library?

**Action:** 🎓 Prüfen ob HSG Zugang hat

---

### 🎯 **TIER 2: Aggregierte Quellen (CSV/API)**

#### 8. **Kaggle - Alternative Datasets**
Suche nach:
- "european startups 2024"
- "vc funding europe"
- "tech startups funding rounds"
- "dealroom export"
- "crunchbase 2024"

**Action:** ✅ Durchsuchen mit besseren Keywords

---

#### 9. **GitHub - Open Startup Datasets**
- **Repos:** Viele sammeln öffentliche VC-Daten
- **Suche:** "startup funding dataset europe"

**Action:** ✅ GitHub durchsuchen

---

#### 10. **European Investment Fund (EIF) Data**
- **URL:** https://www.eif.org
- **Daten:** EU-geförderte Startups
- **Format:** Meist PDF/Excel Reports
- **Fokus:** Venture Debt, EIC Accelerator

**Action:** ⚙️ Reports runterladen + manuell parsen

---

## 🚀 **EMPFOHLENE STRATEGIE**

### **Phase 1: Schnell-Wins (Heute machbar)**

1. ✅ **Y Combinator scrapen** (3_yc_scraper.py)
   - Erwartung: 500-1000 Companies, davon 15-20% Europa
   - Zeitraum: Batches 2015-2024
   
2. ✅ **VCLense scrapen** (2_vclense_scraper.py)
   - Erwartung: 200-400 Swiss Companies
   - Zeitraum: 2015-2024

3. ✅ **Kaggle - Alternative Datasets suchen**
   - Bessere Keywords verwenden
   - Neuere Uploads finden

**Erwartetes Ergebnis:** 700-1400 aktuelle Europa-Datenpunkte

---

### **Phase 2: Ergänzungen (Optional, falls < 1000)**

4. ⚙️ **GitHub Datasets**
   - Fertige CSVs von anderen Projekten

5. ⚙️ **EU-Startups News scrapen**
   - Funding Announcements parsen

6. 🎓 **HSG Library - PitchBook Zugang prüfen**
   - Beste Quelle für Europa wenn verfügbar

---

## 📊 **ERWARTETE ABDECKUNG: EUROPA**

### Nach allen Scrapern (YC + VCLense + Kaggle-Alternative):

| Land | Erwartete Startups |
|------|-------------------|
| 🇬🇧 UK | 200-400 |
| 🇩🇪 Deutschland | 150-300 |
| 🇫🇷 Frankreich | 100-200 |
| 🇨🇭 Schweiz | 200-400 (VCLense!) |
| 🇳🇱 Niederlande | 50-150 |
| 🇸🇪 Schweden | 50-100 |
| 🇪🇸 Spanien | 50-100 |
| 🇮🇹 Italien | 30-80 |
| 🇵🇱 Polen | 20-50 |
| Andere EU | 50-150 |

**Total Europa:** 900-1900 Startups (2015-2024)

---

## 🎯 **NÄCHSTE SCHRITTE**

### Jetzt ausführen:

```bash
# 1. Y Combinator (global, filter Europa nachher)
python3 3_yc_scraper.py

# 2. VCLense (Schweiz-fokussiert)
python3 2_vclense_scraper.py

# 3. Alternative Kaggle Datasets suchen
# Manuell auf kaggle.com
```

### In Script 4 (Merge):
- Europa-Filter anwenden (Country = EU-Länder)
- Year-Filter: 2015-2026
- Kombinieren: Historische (Kaggle alt) + Aktuelle (YC/VCLense)

---

## ⚠️ **WICHTIG FÜR DEIN HSG PROJEKT**

### Im Report erwähnen:

**Datenquellen:**
1. Crunchbase (via Kaggle) - Historische Daten 2000-2014
2. Y Combinator - Aktuelle Daten 2015-2024
3. VCLense - Europa/CH Fokus 2015-2024

**Zeitraum-Split:**
- **Historisch:** 54.294 Startups (2000-2014) - Globale VC-Trends
- **Aktuell:** 1000+ Startups (2015-2024) - Europa-Fokus

**Methodologie:**
- Web Scraping (YC, VCLense)
- API Download (Kaggle/Crunchbase)
- Data Enrichment (Business Model Ableitung)

---

**READY TO START?** 🚀
