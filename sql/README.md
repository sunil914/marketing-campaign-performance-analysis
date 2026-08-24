# SQLite analysis

Run `python3 scripts/build_database.py` to load the committed gzip CSV into `project.db`, validate all 41,188 records and create the analysis views.

- `v_project_kpis` reconciles campaign totals.
- `v_precontact_performance`, `v_monthly_performance`, `v_attempt_performance` and `v_previous_outcome` contain Tableau-ready aggregates.
- `v_duration_diagnostic` keeps post-call duration separate so it is not mistaken for a valid pre-contact targeting variable.

Expected reconciliation: **41,188 contacts**, **4,640 conversions**, **11.27% conversion**, **2.57 average attempts** and **258.29 seconds average call duration**. Open the generated database in DB Browser for SQLite to inspect or export any view.

