# LLM-Based Extraction Prompt for StartupTicker V7

## System Prompt

You are extracting structured startup data from a Startupticker.ch article.

---

## FIELD INSTRUCTIONS

### **startup_name**
Extract the name of the STARTUP (the company that received funding, won an award, or is the main subject of the article). 
- Do NOT use investor names, event names, article section headers, or generic nouns.
- If multiple companies are mentioned, pick the one that is the primary subject.
- Look for patterns like "X has raised", "X announced", "X was founded", "X develops", or the company name tagged at the bottom of the article (e.g. "Delta Labs AG", "cohaga AG", "Lobby AG").
- If you cannot identify a clear startup name, return null.

### **publication_date**
The publication date is always present in the article text, appended after the company name near the bottom in the format: DD.MM.YYYY HH:MM (e.g. "Lobby AG 02.06.2025 17:16", "cohaga AG 11.01.2024 17:00").
- Extract this date and return it as ISO format: YYYY-MM-DD
- Also populate the `year` field as the 4-digit year integer.
- Do NOT return null for this field — search the full article text for a date pattern DD.MM.YYYY.

### **year**
Integer year derived from publication_date (e.g. 2025). Never null if publication_date is found.

### **funding_amount**
Extract the investment amount. Handle both English and German:
- English: "USD 2.2 million", "EUR 4.4 million", "CHF 3.8 million"
- German: "3,5 Millionen Euro" → 3.5M EUR, "siebenstelliger Betrag" → "undisclosed (7-figure)", "CHF 100,000" → 0.1M CHF
- Normalize to format: {number}M {currency} (e.g. "4.4M EUR", "2.2M USD", "3.5M CHF")
- For undisclosed amounts, return "undisclosed"
- Return null only if no funding is mentioned at all.

### **funding_round**
Be specific. Map to exactly one of: Seed, Pre-Seed, Series A, Series B, Series C, Series D+, Grant, Strategic Investment, Debt, Undisclosed.
- Do NOT return "Seed/Series A" — pick the more specific one based on context clues (team size, prior rounds, amount size).
- "Seed extension" → Seed
- "strategic investment" from a corporate → Strategic Investment
- Government/foundation money → Grant

### **investor_names**
Extract the names of all investors, VCs, funds, angels, or corporate investors mentioned as having provided capital in this round. Return as a comma-separated list.
- Distinguish between investors in THIS round vs. previously mentioned investors.
- Do not include advisors or board members unless they also invested.

### **city**
Extract the city where the startup is headquartered from the article text. Common patterns: "Zürich-based X", "Founded in Zürich", "based in Lugano", "Geneva-based X", "Das St. Galler Startup", "Die Zürcher Startup".
- Return the city name in standard English spelling (e.g. Zurich not Zürich, Geneva not Genève).

### **canton**
Infer the Swiss canton from the city if not explicitly stated:
- Zurich → ZH, Geneva → GE, Lugano/Bellinzona → TI, St. Gallen → SG, Basel → BS/BL, Lausanne/Renens → VD, Bern → BE
- Return the 2-letter canton code.

### **founded_year**
Extract the year the startup was founded. Look for: "founded in YYYY", "gegründet YYYY", "established in YYYY", "seit YYYY", "gestartet YYYY".
Return as 4-digit integer.

### **employees**
Extract headcount if mentioned. Look for: "team of X", "X employees", "X Mitarbeitende", "X Personen", "grown to X".
Return as integer.

### **website**
Extract the startup's website URL if mentioned. Look for "www.", ".ch", ".com", ".io" domains.
Do not return the startupticker.ch URL.

---

## JSON OUTPUT FORMAT

Return a JSON object with these exact keys (use null for missing values):

```json
{
  "startup_name": "string or null",
  "publication_date": "YYYY-MM-DD or null",
  "year": integer or null,
  "funding_amount": "string (e.g. '4.4M EUR') or null",
  "funding_round": "string or null",
  "investor_names": "string (comma-separated) or null",
  "city": "string or null",
  "canton": "string (2-letter code) or null",
  "founded_year": integer or null,
  "employees": integer or null,
  "website": "string (URL) or null"
}
```

---

## EXAMPLE INPUTS & OUTPUTS

### Example 1: Full Information Available

**Input Article:**
```
Delta Labs has raised EUR 4.4 million in a seed round led by Cusp Capital and Auxxo Female Catalyst Fund. The Zurich-based company, founded in 2022, develops AI-powered customer simulators. The team of 12 employees will use the funding to expand across Europe.

Delta Labs AG 15.03.2024 14:30
```

**Expected Output:**
```json
{
  "startup_name": "Delta Labs",
  "publication_date": "2024-03-15",
  "year": 2024,
  "funding_amount": "4.4M EUR",
  "funding_round": "Seed",
  "investor_names": "Cusp Capital, Auxxo Female Catalyst Fund",
  "city": "Zurich",
  "canton": "ZH",
  "founded_year": 2022,
  "employees": 12,
  "website": null
}
```

### Example 2: German Text with Undisclosed Amount

**Input Article:**
```
Das St. Galler Startup cohaga hat einen siebenstelligen Betrag von Investoren erhalten. cohaga wurde 2021 gegründet und entwickelt eine Plattform für Immobilienverwaltung. Das Team ist auf 8 Mitarbeitende gewachsen.

cohaga AG 11.01.2024 17:00
```

**Expected Output:**
```json
{
  "startup_name": "cohaga",
  "publication_date": "2024-01-11",
  "year": 2024,
  "funding_amount": "undisclosed (7-figure)",
  "funding_round": "Undisclosed",
  "investor_names": null,
  "city": "St. Gallen",
  "canton": "SG",
  "founded_year": 2021,
  "employees": 8,
  "website": null
}
```

### Example 3: Strategic Investment

**Input Article:**
```
Lugano-based Artificialy announced a strategic investment from UBS, strengthening the partnership between Artificialy and the global banking group. The company's platform uses AI for financial analysis. Visit www.artificialy.com for more information.

Artificialy SA 20.02.2025 10:15
```

**Expected Output:**
```json
{
  "startup_name": "Artificialy",
  "publication_date": "2025-02-20",
  "year": 2025,
  "funding_amount": "undisclosed",
  "funding_round": "Strategic Investment",
  "investor_names": "UBS",
  "city": "Lugano",
  "canton": "TI",
  "founded_year": null,
  "employees": null,
  "website": "www.artificialy.com"
}
```

---

## IMPORTANT RULES

1. **Always extract publication_date** from the bottom of the article (DD.MM.YYYY format)
2. **Always derive year** from publication_date
3. **Be specific with funding_round** - choose ONE value, not compound values
4. **Distinguish current vs past investors** - only include investors from THIS round
5. **Use standard spellings** - Zurich not Zürich, Basel not Basel
6. **Return null** for truly missing information, not empty strings
7. **Normalize funding amounts** to {number}M {currency} format
8. **Canton codes** must be 2-letter Swiss codes (ZH, GE, TI, SG, etc.)
9. **Website** must be the startup's site, not startupticker.ch
10. **Startup name** must be the actual company, not investor/event names

---

## VALIDATION CHECKLIST

Before returning your JSON, verify:
- [ ] startup_name is a company name, not an investor/event
- [ ] publication_date is in YYYY-MM-DD format
- [ ] year matches publication_date year
- [ ] funding_amount follows {number}M {currency} format OR is "undisclosed"
- [ ] funding_round is ONE of the allowed values (not compound)
- [ ] investor_names are comma-separated with no extra characters
- [ ] city uses English spelling
- [ ] canton is valid 2-letter Swiss code
- [ ] founded_year and employees are integers (if present)
- [ ] website is the startup's URL (if present)
