# Tableau Validation Checklist

> **Status:** Pre-publication quality-assurance specification. The workbook, screenshots and Tableau Public link remain pending.

Run the validated preparation workflow before opening Tableau:

```bash
python3 scripts/prepare_tableau_data.py
```

Use `tableau/bank_marketing_tableau.csv` as the only Tableau data source. Keep SQLite views separate for reconciliation; joining aggregate views to contact rows would multiply counts.

## 1. Source and field checks

- [ ] The source contains exactly 41,188 contact rows and 26 columns.
- [ ] `conversion_flag` contains only 0 and 1.
- [ ] `prior_contacted` equals whether `previous` is greater than zero.
- [ ] Age Band, Contact Attempt Band and Month Number match the validated preparation rules.
- [ ] Month is sorted by Month Number rather than alphabetically.
- [ ] Call Duration is numeric and visibly classified as post-call information.
- [ ] Unknown categorical values remain visible rather than being silently removed.

## 2. Opening reconciliation

Clear every filter before recording the opening state.

| Check | Expected result | Pass condition |
|---|---:|---|
| Contacts | 41,188 | Exact row count |
| Conversions | 4,640 | Exact sum of Conversion Flag |
| Conversion rate | 11.27% | Equal after two-decimal display rounding |
| Average contact attempts | 2.57 | Equal after two-decimal display rounding |
| Average call duration | 258.29 seconds | Equal after two-decimal display rounding |

- [ ] Contacts equal `COUNT([Conversion Flag])`.
- [ ] Conversions equal `SUM([Conversion Flag])`.
- [ ] Conversion Rate equals `AVG([Conversion Flag])`.
- [ ] Clearing filters or using **Revert All** restores every opening value.
- [ ] SQLite KPI views reconcile independently without being joined to Tableau rows.

## 3. Filter and interaction tests

Test Age Band, Job, Education, Contact, Month, Day of Week, Previous Outcome, Prior Contacted and Contact Attempt Band:

- [ ] Every selected segment shows contact volume alongside conversion count and rate.
- [ ] Filtered conversion rate uses filtered contacts as its denominator.
- [ ] Zero-contact selections return null or an explanatory state, not an error or infinity.
- [ ] Month order remains chronological after filtering.
- [ ] Selecting a mark updates only the intended compatible worksheets.
- [ ] Clearing a mark restores the prior filter state.
- [ ] Multi-filter combinations do not duplicate or drop contact rows unexpectedly.
- [ ] Tooltips identify the filtered population and display unrounded values where useful.

## 4. Leakage boundary tests

- [ ] Duration is absent from every pre-contact filter, targeting recommendation and prioritisation view.
- [ ] Any Duration worksheet is placed in a separate post-call diagnostic area.
- [ ] Every Duration view states: **Post-call diagnostic only — not available for pre-contact targeting.**
- [ ] Dashboard actions from Duration do not drive pre-contact targeting views.
- [ ] Contact channel, month and attempt-band patterns are described as observed associations, not causal effects.
- [ ] The 65.11% prior-success rate is shown with its contact volume and not treated as guaranteed future performance.

## 5. Responsible interpretation

- [ ] Age, job, education and marital-status comparisons are aggregated and do not identify individuals.
- [ ] No demographic group is labelled as inherently valuable, risky or unsuitable.
- [ ] Unknown categories and small-volume segments are not hidden to improve the story.
- [ ] Recommendations call for consent, compliance and controlled testing.
- [ ] The dashboard states that this is observational campaign data and does not establish causality.
- [ ] Rate comparisons always include contact volume so small segments are not overstated.

## 6. Visual and accessibility checks

- [ ] KPIs, rates and counts have text labels and do not rely on colour alone.
- [ ] Positive and warning states remain distinguishable without red/green-only encoding.
- [ ] Text and marks have sufficient contrast.
- [ ] Keyboard and reading order follow title → KPIs → pre-contact views → post-call diagnostics → filters.
- [ ] Desktop layout has no clipped labels, overlapping marks or unnecessary scrolling.
- [ ] Phone layout keeps KPIs and primary campaign views first with touch-friendly controls.
- [ ] Worksheet titles identify the metric, population and whether the view is pre- or post-contact.

## 7. Publication gate

- [ ] All opening and representative filtered cases pass reconciliation.
- [ ] Leakage, responsible-use and accessibility checks pass.
- [ ] Desktop and phone screenshots match the final workbook.
- [ ] The Tableau Public URL opens successfully and shows the intended default state.
- [ ] The README and portfolio status change only after the workbook, screenshots and verified public link exist.

Do not mark the Tableau dashboard complete until every required reconciliation, interaction, leakage, accessibility and responsible-interpretation check passes.
