DROP TABLE IF EXISTS campaign_contacts;

CREATE TABLE campaign_contacts (
    age INTEGER, job TEXT, marital TEXT, education TEXT, "default" TEXT,
    housing TEXT, loan TEXT, contact TEXT, month TEXT, day_of_week TEXT,
    duration INTEGER, campaign INTEGER, pdays INTEGER, previous INTEGER,
    poutcome TEXT, emp_var_rate REAL, cons_price_idx REAL, cons_conf_idx REAL,
    euribor3m REAL, nr_employed REAL, y TEXT, conversion_flag INTEGER,
    prior_contacted INTEGER, age_band TEXT, contact_attempt_band TEXT,
    month_number INTEGER
);

CREATE INDEX idx_campaign_month ON campaign_contacts (month_number);
CREATE INDEX idx_campaign_job ON campaign_contacts (job);
