import pandas as pd

# Dateien einlesen
indeed = pd.read_csv("indeed_jobs_bereinigt.csv")
jobs = pd.read_csv("jobs_anforderungen_clean (kopie).csv")

# Spalten umbenennen auf gemeinsames Schema
indeed_renamed = indeed.rename(columns={
    "job_url": "url"
})
indeed_renamed["anforderungen_sektion"] = None
indeed_renamed["veroeffentlicht_am"] = None
indeed_renamed["quelle"] = "indeed"

jobs_renamed = jobs.rename(columns={
    "titel": "job_title",
    "unternehmen": "company",
    "arbeitsort": "location",
    "anforderungen": "requirements",
})
jobs_renamed["job_profil"] = None
jobs_renamed["full_description"] = None
jobs_renamed["quelle"] = "jobs.ch"

# Gemeinsame Spaltenreihenfolge
cols = [
    "job_profil", "job_title", "company", "location",
    "anforderungen_sektion", "requirements", "full_description",
    "veroeffentlicht_am", "url", "quelle"
]

combined = pd.concat([indeed_renamed[cols], jobs_renamed[cols]], ignore_index=True)

# Duplikate entfernen basierend auf job_title + company + location
vor = len(combined)
combined = combined.drop_duplicates(subset=["job_title", "company", "location"], keep="first")
nach = len(combined)

print(f"Indeed: {len(indeed)} Zeilen")
print(f"Jobs.ch: {len(jobs)} Zeilen")
print(f"Kombiniert: {vor} Zeilen")
print(f"Duplikate entfernt: {vor - nach}")
print(f"Final: {nach} Zeilen")

combined.to_csv("jobs_combined.csv", index=False)
print("Gespeichert als: jobs_combined.csv")
