"""
Erstellt eine zweite CSV mit aufgeschlüsselten MS365-Tools.
Behält alle Spalten aus jobs_kategorisiert.csv und fügt MS-Tool-Spalten hinzu.
"""
import pandas as pd
import re

df = pd.read_csv('jobs_combined.csv')

# Text zusammenbauen
def build_text(row):
    parts = []
    for col in ['requirements', 'anforderungen_sektion', 'full_description']:
        if pd.notna(row.get(col)):
            parts.append(str(row[col]))
    return ' '.join(parts).lower()

df['_text'] = df.apply(build_text, axis=1)

def match_any(text, patterns):
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return 1
    return 0

# Bestehende kategorisierte Datei laden (alle Spalten behalten)
df_kat = pd.read_csv('jobs_kategorisiert.csv')

# MS365-Tool-Aufschlüsselung
ms_tools = {
    'MS_Excel': [r'\bexcel\b'],
    'MS_Word': [r'\bword\b(?=.*(?:kenntn|office|microsoft|ms|dokument|document))'],
    'MS_PowerPoint': [r'\bpowerpoint\b', r'\bppt\b'],
    'MS_Outlook': [r'\boutlook\b'],
    'MS_SharePoint': [r'\bsharepoint\b'],
    'MS_Teams': [r'\bms\s*teams\b', r'\bmicrosoft\s*teams\b', r'(?:sharepoint|office|m365|365).*\bteams\b', r'\bteams\b.*(?:sharepoint|office|m365|365)'],
    'MS_Power_BI': [r'\bpower\s?bi\b'],
    'MS_Power_Automate': [r'\bpower\s?automate\b', r'\bpower\s?platform\b'],
    'MS_Power_Apps': [r'\bpower\s?apps?\b'],
    'MS_Dynamics': [r'\bdynamics\s?365\b', r'\bdynamics\s?crm\b', r'\bmicrosoft\s*dynamics\b', r'\bms\s*dynamics\b'],
    'MS_Visio': [r'\bvisio\b'],
    'MS_Project': [r'\bms\s?project\b', r'\bmicrosoft\s?project\b'],
    'MS_Intune': [r'\bintune\b'],
    'MS_Azure_AD_Entra': [r'\bazure\s?(?:ad|active\s?directory)\b', r'\bentra\b'],
    'MS_Exchange': [r'\bexchange\s*(?:server|online)\b', r'\bmicrosoft\s*exchange\b', r'\bms\s*exchange\b'],
    'MS_Copilot': [r'\b(?:microsoft|ms)\s*copilot\b', r'\bcopilot\b'],
    'MS_OneDrive': [r'\bonedrive\b'],
    'MS_Office_365_allg': [r'\bms\s*office\b', r'\bmicrosoft\s*office\b', r'\boffice\s*365\b', r'\bm365\b', r'\bmicrosoft\s*365\b'],
}

# MS-Tool-Spalten berechnen
for col_name, patterns in ms_tools.items():
    df_kat[col_name] = df['_text'].apply(lambda text: match_any(text, patterns))

# Zusammenfassung
ms_cols = list(ms_tools.keys())
df_kat['MS_Tools_Score'] = df_kat[ms_cols].sum(axis=1)

# Speichern
df_kat.to_csv('jobs_kategorisiert_ms_detail.csv', index=False, encoding='utf-8-sig')

print(f"Output: jobs_kategorisiert_ms_detail.csv ({len(df_kat)} Zeilen, {len(df_kat.columns)} Spalten)")
print(f"\n--- MS365-Tools Häufigkeiten ---")
for c in sorted(ms_cols, key=lambda x: -df_kat[x].sum()):
    count = df_kat[c].sum()
    if count > 0:
        print(f"  {c}: {count}")
print(f"\n  Inserate mit mind. 1 MS-Tool: {(df_kat['MS_Tools_Score'] > 0).sum()}")
