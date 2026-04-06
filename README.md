# Veridion POC Challenge — Entity Resolution & Data Quality Assessment

## What is this

A POC simulation for Veridion's Deeptech Engineer Intern role. A manufacturing company's procurement team sent ~592 suppliers that needed to be matched against Veridion's company database and quality-checked.

## What's in this repo

- **`poc_analysis.ipynb`** — Main notebook with the full analysis: entity resolution process, data quality findings, and recommendations
- **`entity_resolution.py`** — Python script used for automated fuzzy matching with rapidfuzz (scoring algorithm that ranked candidates before manual review)
- **`presales_data_sample.xlsx`** — The dataset with both raw candidates and the working sheet with my match decisions and notes

## Quick summary

- Matched **498 out of 592** suppliers (84.1%)
- 94 left unmatched with documented reasons (mostly regional subsidiaries not in Veridion's DB)
- Found **14 duplicate suppliers** in the client's own database
- Identified data quality issues: phone numbers stored as floats, encoding artifacts, revenue outliers
- Sustainability data coverage is low (~17%) — client would need Veridion's ESG data layer

## Tools used

Excel,Python, pandas, matplotlib, rapidfuzz
