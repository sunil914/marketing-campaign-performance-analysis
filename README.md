# Marketing Campaign Performance Analysis

> **Status:** Validated data and executable SQLite analysis complete · Tableau dashboard in progress

## Overview

This project analyses a bank direct-marketing campaign to measure term-deposit conversion, understand contact efficiency and identify patterns that can support better testing and planning.

**Dataset:** [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank%2Bmarketing) · CC BY 4.0

## Key KPIs

| Metric | Result |
|---|---:|
| Contacts | 41,188 |
| Conversions | 4,640 |
| Conversion rate | 11.27% |
| Average contact attempts | 2.57 |
| Average call duration | 258 seconds |

## Analysis completed

- Standardised categorical values and validated missing-value markers.
- Created Conversion Flag, Prior Contacted, Age Band, Contact Attempt Band and Month Number.
- Reconciled every segment summary to the full 41,188-contact population.
- Compared channel, month, occupation, age band, contact attempts, weekday and prior outcome.
- Separated descriptive post-call information from valid pre-contact variables.

## Repository contents

- [`data/`](data/) — cleaned dataset, preview sample, source and validation notes
- [`sql/`](sql/) — executable SQLite schema, leakage-aware analysis views and run guide
- [`scripts/build_database.py`](scripts/build_database.py) — standard-library loader that rebuilds and validates `project.db`
- [`tableau/`](tableau/) — build guide; workbook and screenshots are still pending

## Tableau dashboard — in progress

Planned views:

- Conversion rate and contact volume by month
- Channel and occupation comparisons
- Conversion by contact-attempt band
- Previous campaign outcome comparison
- Age-band and weekday performance
- Interactive campaign filters

## Key insights

- The campaign achieved an **11.27% conversion rate**.
- March had the highest observed monthly conversion rate.
- Cellular contacts converted more strongly than telephone contacts.
- A previously successful campaign outcome corresponded to a **65.11% conversion rate**.

## Repository roadmap

- [x] Business problem and KPI definition
- [x] Cleaning and feature-engineering approach
- [x] SQL analysis documented
- [x] Leakage-aware recommendations documented
- [x] Add cleaned data with source and validation notes
- [x] Add reproducible SQLite database loader
- [ ] Add reproducible preparation code
- [x] Add complete SQL schema and analysis views
- [ ] Build and publish Tableau dashboard
- [ ] Add dashboard screenshots and Tableau Public link

## Analytical limitation

Call duration is known only after a call finishes. It may explain completed outcomes but must not be used to decide whom to contact beforehand. Observed associations should be validated through compliant experiments.
