# Tableau Dashboard Build Guide

> **Project status:** Build specification only. The Tableau dashboard is not yet complete or published.

This guide converts the documented bank-marketing analysis into a reproducible, leakage-aware Tableau dashboard. It separates valid pre-contact planning information from fields that are available only after a call.

## 1. Dashboard objective

Build a campaign-performance dashboard that answers:

1. How many contacts and conversions occurred, and what was the conversion rate?
2. How did contact volume and conversion vary by month and weekday?
3. How did channel, occupation, age band and contact frequency perform?
4. What does previous campaign history suggest?
5. Which findings are descriptive only and must not be used for pre-contact targeting?

**Primary audience:** marketing operations and campaign analysts  
**Source:** [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank%2Bmarketing)  
**Licence:** CC BY 4.0

## 2. Analysis boundary

The dashboard must distinguish two analytical contexts.

### Pre-contact planning

These fields may support compliant segment-level planning because they are known before or at contact initiation:

- Age Band
- Job / occupation
- Education
- Contact channel
- Month
- Weekday
- Previous campaign outcome
- Prior Contacted
- Contact Attempt Band
- Available macroeconomic indicators

### Post-campaign explanation only

**Call duration is known only after a call ends.** It can describe completed campaign outcomes, but it must not be used to select people before contact or presented as an actionable targeting variable.

Any worksheet containing duration must include the label:

> Post-call diagnostic only — not available for pre-contact targeting.

## 3. Required fields

Confirm the prepared data contains these fields before building worksheets:

| Field | Purpose |
|---|---|
| Conversion Flag | Binary campaign outcome |
| Contact | Contact channel |
| Month | Campaign month |
| Month Number | Chronological month sort |
| Day of Week | Weekday comparison |
| Job | Occupation comparison |
| Age Band | Aggregate age analysis |
| Contact Attempt Band | Contact-frequency analysis |
| Campaign | Number of contacts in the current campaign |
| Previous Outcome | Previous campaign comparison |
| Prior Contacted | Previous-contact grouping |
| Duration | Post-call diagnostic only |

Use the prepared categorical fields rather than recreating bands independently inside Tableau. This keeps the workbook consistent with the documented cleaning process.

## 4. KPI validation gate

With all dashboard filters cleared, reproduce these documented values:

| KPI | Expected display |
|---|---:|
| Contacts | 41,188 |
| Conversions | 4,640 |
| Conversion Rate | 11.27% |
| Average Contact Attempts | 2.57 |
| Average Call Duration | 258 seconds |

These are rounded display values. Keep full precision in the data source and apply rounding through Tableau formatting.

Before continuing, confirm:

- Each row represents one campaign contact.
- `Conversion Flag` contains only 0 and 1.
- `SUM([Conversion Flag]) = 4,640`.
- `COUNT([Conversion Flag]) = 41,188`.
- Segment totals reconcile to the full contact population.
- No default filter changes the opening KPI values.

## 5. Calculated fields

### Conversions

```tableau
SUM([Conversion Flag])
```

### Conversion Rate

Because the prepared table contains one row per contact:

```tableau
AVG([Conversion Flag])
```

Format as a percentage with two decimal places.

### Contact Efficiency

```tableau
IF SUM([Campaign]) = 0 THEN
    NULL
ELSE
    SUM([Conversion Flag]) / SUM([Campaign])
END
```

Use this only as a campaign-effort indicator. It does not measure cost, profitability or incremental causal impact.

### Month Sort

Use `Month Number` to sort the displayed `Month` field in chronological order. Do not sort month names alphabetically.

### Volume-aware comparison

Every conversion-rate view should also display:

```tableau
COUNT([Conversion Flag])
```

A high rate from a small segment should not be presented as equivalent to a high rate from a large segment.

## 6. Worksheet specifications

Use consistent worksheet names to make the workbook auditable.

### KPI — Contacts

- Marks: Text
- Measure: `COUNT([Conversion Flag])`
- Number format: Whole number with thousands separator
- Expected value: **41,188**

Create equivalent KPI sheets for:

- `KPI — Conversions`
- `KPI — Conversion Rate`
- `KPI — Average Contact Attempts`

Keep average duration outside the primary pre-contact KPI row. If shown, place it in a clearly labelled post-call diagnostic area.

### Trend — Monthly Contact Volume

- Columns: `Month`, sorted by `Month Number`
- Rows: `COUNT([Conversion Flag])`
- Marks: Bar
- Tooltip: Month, Contacts, Conversions and Conversion Rate

### Trend — Monthly Conversion Rate

Build as a separate aligned panel under the volume chart:

- Columns: `Month`, sorted by `Month Number`
- Rows: `AVG([Conversion Flag])`
- Marks: Line with points
- Label only the highest and lowest observed months.
- Tooltip must include contact volume.

Separate aligned charts keep rate and volume visible without a potentially confusing dual axis.

### Performance — Contact Channel

- Rows: `Contact`
- Columns: `AVG([Conversion Flag])`
- Marks: Horizontal bar
- Label: Conversion Rate
- Tooltip: Channel, Contacts, Conversions, Conversion Rate and Average Attempts
- Sort: Descending by conversion rate

Do not describe the result as causal channel lift. Channel groups may differ in other ways.

### Performance — Occupation

- Rows: `Job`
- Columns: `AVG([Conversion Flag])`
- Marks: Horizontal bar
- Label: Conversion Rate
- Tooltip: Job, Contacts, Conversions and Conversion Rate
- Sort: Descending by conversion rate
- Always show contact volume in the tooltip.

### Performance — Contact Attempts

- Rows: `Contact Attempt Band`
- Columns: `AVG([Conversion Flag])`
- Marks: Bar
- Label: Conversion Rate
- Tooltip: Attempt Band, Contacts, Conversions, Conversion Rate and Average Attempts
- Sort using the logical band order, not alphabetically.

This worksheet supports investigation of diminishing returns. It does not prove that additional attempts caused lower conversion.

### History — Previous Outcome

- Rows: `Previous Outcome`
- Columns: `AVG([Conversion Flag])`
- Marks: Bar
- Label: Conversion Rate
- Tooltip: Previous Outcome, Contacts, Conversions, Conversion Rate and Prior Contacted
- Add contact volume beside the rate.

The documented analysis found a **65.11% observed conversion rate** for a previously successful outcome. Reconcile this value before publishing.

### Profile — Age Band

- Rows: `Age Band`
- Columns: `AVG([Conversion Flag])`
- Marks: Bar
- Tooltip: Age Band, Contacts, Conversions and Conversion Rate
- Display for descriptive monitoring only.
- Do not recommend discriminatory exclusion or targeting based on age.

### Timing — Weekday

- Columns: `Day of Week`
- Rows: `AVG([Conversion Flag])`
- Marks: Bar
- Tooltip: Weekday, Contacts, Conversions and Conversion Rate
- Use chronological weekday ordering.

### Diagnostic — Duration

Optional post-campaign worksheet:

- Columns: Duration Band
- Rows: `AVG([Conversion Flag])`
- Marks: Line or bar
- Add the post-call diagnostic warning directly in the title and caption.
- Do not connect this sheet to pre-contact recommendation text.

## 7. Dashboard layout

Recommended fixed layout:

1. **Header:** Campaign Performance & Contact Efficiency
2. **Primary KPI row:** Contacts, Conversions, Conversion Rate, Average Attempts
3. **Top-left:** Monthly contact volume
4. **Middle-left:** Monthly conversion rate
5. **Top-right:** Channel and occupation comparisons
6. **Bottom-left:** Contact-attempt and previous-outcome views
7. **Bottom-right:** Age-band and weekday views
8. **Optional separate tab:** Post-call duration diagnostic
9. **Filter rail:** Age Band, Job, Education, Channel, Month, Weekday and Previous Outcome

Keep the pre-contact dashboard and post-call diagnostic visually separated.

## 8. Filters and actions

Apply filters only to relevant worksheets using the same prepared data source.

Recommended filters:

- Age Band
- Job
- Education
- Contact channel
- Month
- Weekday
- Previous Outcome
- Prior Contacted
- Contact Attempt Band

Recommended actions:

- Selecting a month filters channel and occupation views.
- Selecting a channel filters timing and attempt-band views.
- Selecting a previous outcome filters the supporting segment views.
- Clearing selections restores the complete 41,188-contact baseline.

After configuring actions, reset all filters and rerun the KPI validation gate.

## 9. Formatting and accessibility

- Use a neutral primary colour and one highlight colour for selected marks.
- Do not use red/green alone to encode conversion performance.
- Show percentage labels to two decimal places.
- Use whole-number formatting for contacts and conversions.
- Keep body text at least 11–12 px.
- Use explicit titles such as “Observed Conversion Rate by Channel”.
- Include contact counts in every rate-based tooltip.
- Avoid truncated occupation and previous-outcome labels.
- Ensure keyboard focus and colour contrast remain visible after publication.

## 10. Interpretation rules

Use careful language:

- Say **observed association**, not cause or uplift.
- Compare conversion rate with segment size and campaign effort.
- Treat previous success as a testable planning signal, not a guarantee.
- Do not use demographic results to justify unfair exclusion.
- Validate channel and timing recommendations through compliant experiments.
- Keep call duration out of pre-contact targeting recommendations.

## 11. Publishing checklist

Before publishing to Tableau Public:

- [ ] Contacts reconcile to 41,188
- [ ] Conversions reconcile to 4,640
- [ ] Conversion Rate displays 11.27%
- [ ] Average Contact Attempts displays 2.57
- [ ] Previously successful outcome reconciles to 65.11%
- [ ] Month and weekday fields use chronological sorting
- [ ] Every rate view also exposes segment volume
- [ ] Duration is isolated and labelled post-call only
- [ ] Filters and actions restore correctly when cleared
- [ ] Titles use descriptive, non-causal language
- [ ] Dashboard does not recommend discriminatory targeting
- [ ] Tableau Public link is added to the README
- [ ] Final screenshot is added under `images/`

## 12. Next repository assets

The next implementation phase should add:

```text
data/bank_marketing_clean.csv
sql/analysis.sql
analysis/kpis.json
tableau/conversion_by_channel.csv
tableau/conversion_by_month.csv
tableau/conversion_by_job.csv
tableau/conversion_by_age_band.csv
tableau/conversion_by_attempt_band.csv
tableau/conversion_by_previous_outcome.csv
images/dashboard.png
```

Do not mark the dashboard complete until the workbook is published, the live link works and every validation check passes.
