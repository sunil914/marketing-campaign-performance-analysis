# Data

## File

`bank_marketing_clean.csv.gz` contains 41,188 campaign contacts and 26 columns. `bank_marketing_sample.csv` provides the first 500 rows for browser preview. Decompress the full file with `gzip -dk bank_marketing_clean.csv.gz`.

## Source

- Dataset: UCI Bank Marketing (`bank-additional-full.csv`)
- URL: https://archive.ics.uci.edu/dataset/222/bank+marketing
- DOI: https://doi.org/10.24432/C5K306
- Creators: S. Moro, P. Rita and P. Cortez
- License: CC BY 4.0

## Preparation

The original semicolon-delimited file was converted to standard CSV. Five analysis fields were added: `conversion_flag`, `prior_contacted`, `age_band`, `contact_attempt_band` and `month_number`. Original source columns remain unchanged.

## Validation

| Check | Result |
|---|---:|
| Contacts | 41,188 |
| Conversions | 4,640 |
| Conversion rate | 11.27% |
| Average contact attempts | 2.57 |
| Average call duration | 258.29 seconds |

Uncompressed CSV SHA-256: `a5c3bf2ab19f3dfa656655a827ba22f7b0ab05b884edfe588f2b0746b440c579`

Compressed file SHA-256: `25ba75f76b29b0e2f90865bf5fc43378179af5925a0bc60f4ca2670529acfd2c`
