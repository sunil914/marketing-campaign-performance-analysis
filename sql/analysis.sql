DROP VIEW IF EXISTS v_project_kpis;
DROP VIEW IF EXISTS v_precontact_performance;
DROP VIEW IF EXISTS v_monthly_performance;
DROP VIEW IF EXISTS v_attempt_performance;
DROP VIEW IF EXISTS v_previous_outcome;
DROP VIEW IF EXISTS v_duration_diagnostic;

CREATE VIEW v_project_kpis AS
SELECT
    COUNT(*) AS contacts,
    SUM(conversion_flag) AS conversions,
    ROUND(100.0 * SUM(conversion_flag) / COUNT(*), 2) AS conversion_rate_pct,
    ROUND(AVG(campaign), 2) AS average_attempts,
    ROUND(AVG(duration), 2) AS average_call_duration_seconds
FROM campaign_contacts;

CREATE VIEW v_precontact_performance AS
SELECT
    contact,
    job,
    age_band,
    COUNT(*) AS contacts,
    SUM(conversion_flag) AS conversions,
    ROUND(100.0 * SUM(conversion_flag) / COUNT(*), 2) AS conversion_rate_pct
FROM campaign_contacts
GROUP BY contact, job, age_band;

CREATE VIEW v_monthly_performance AS
SELECT
    month_number,
    month,
    COUNT(*) AS contacts,
    SUM(conversion_flag) AS conversions,
    ROUND(100.0 * SUM(conversion_flag) / COUNT(*), 2) AS conversion_rate_pct
FROM campaign_contacts
GROUP BY month_number, month;

CREATE VIEW v_attempt_performance AS
SELECT
    contact_attempt_band,
    COUNT(*) AS contacts,
    SUM(conversion_flag) AS conversions,
    ROUND(100.0 * SUM(conversion_flag) / COUNT(*), 2) AS conversion_rate_pct
FROM campaign_contacts
GROUP BY contact_attempt_band;

CREATE VIEW v_previous_outcome AS
SELECT
    poutcome,
    prior_contacted,
    COUNT(*) AS contacts,
    SUM(conversion_flag) AS conversions,
    ROUND(100.0 * SUM(conversion_flag) / COUNT(*), 2) AS conversion_rate_pct
FROM campaign_contacts
GROUP BY poutcome, prior_contacted;

-- Post-call duration is deliberately isolated: it explains completed calls but
-- is not valid input for deciding whom to contact before a call begins.
CREATE VIEW v_duration_diagnostic AS
SELECT
    y AS outcome,
    COUNT(*) AS contacts,
    ROUND(AVG(duration), 2) AS average_call_duration_seconds
FROM campaign_contacts
GROUP BY y;

