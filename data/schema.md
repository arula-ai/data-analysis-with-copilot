# Hartwell Financial Services — Transaction Risk Alert Dataset Schema

**Version:** 1.0 | **Effective:** Q4 2024 | **Owner:** Data & Analytics Governance

---

## Business Context

Hartwell Financial Services is a fictional financial institution providing retail, business, and institutional banking services. The Transaction Risk Alert System generates automated alerts when transaction behavior deviates from established risk thresholds. Fraud is defined as a confirmed unauthorized transaction flagged within the alert triage workflow and verified by a licensed analyst within 30 days of the alert creation date.

This dataset contains one row per fraud alert case and covers the Q4 2024 alert queue (October–December 2024). It is used for analyzing alert quality, analyst performance, fraud confirmation rates, and risk signal effectiveness across regions and client segments.

---

## Column Reference

| Column Name | Data Type | Valid Range / Values | Nullable | Business Description |
|---|---|---|---|---|
| `alert_id` | string | ALT-XXXXXXXX (8-digit suffix) | No | Unique identifier for each fraud alert case |
| `account_masked` | string | Pattern: `x***@xx***.tld` | No | Masked account identifier. Not directly identifiable but must be treated as PII-adjacent. Do not include in any output or visualization. |
| `region` | string | Northeast, Southeast, Midwest, West, International | No | Geographic region where the flagged transaction originated |
| `alert_type` | string | Velocity Check, Large Transaction, Geographic Anomaly, Account Takeover, Pattern Match | No | Classification of the fraud signal that triggered the alert |
| `transaction_amount` | float | $0.01–$500,000.00 | Yes | Dollar value of the flagged transaction |
| `prior_alerts_90d` | integer | 0–20 | No | Count of prior alerts for the same account in the 90 days preceding this alert |
| `account_age_days` | integer | 1–3,650 | No | Number of days since the account was opened at the time of the alert |
| `days_since_last_txn` | integer | 1–365 | Yes | Days since the account's last completed transaction before this alert |
| `risk_score` | float | 0.0–1.0 | No | Normalized risk signal score from the alert engine (0.0 = no risk, 1.0 = maximum risk) |
| `analyst_confidence` | integer | 0–10 | No | Analyst's self-rated confidence that the alert represents genuine fraud (0 = no confidence, 10 = certain). -1 is an invalid legacy code meaning "not rated". |
| `fraud_confirmed` | integer | 0 or 1 | No | Final disposition: 0 = not confirmed fraud, 1 = confirmed fraud |
| `analyst_id` | string | ANL-XXX (3-digit suffix) | No | Identifier of the analyst who reviewed and closed the alert |
| `investigation_complete` | string | Yes, No, Pending | No | Whether the investigation workflow was completed before closing |
| `escalation_date` | string | YYYY-MM-DD | No | Date the alert was escalated to a senior analyst or compliance officer |
| `client_segment` | string | Retail, Business, Premier, Institutional | No | Client segment classification at the time of the alert |

---

## Known Data Quality Issues (Facilitator Reference)

> **Note:** The following issues are intentional and embedded in the dataset for training purposes. Participants are expected to discover and document these during Stage 1 (Data Profiling) and address them during Stage 2 (Data Cleaning).

| Issue # | Column | Description | Count | Expected Discovery Method |
|---|---|---|---|---|
| 1 | `alert_id` | Duplicate IDs — same alert_id appears more than once | 12 | `df.duplicated(subset=['alert_id'])` |
| 2 | `alert_type` | Value "VEL" used instead of "Velocity Check" — encoding inconsistency | 23 | `df['alert_type'].value_counts()` |
| 3 | `transaction_amount` | Negative values — invalid for a transaction amount | 8 | `df[df['transaction_amount'] < 0]` |
| 4 | `transaction_amount` | Null/missing values | 15 | `df.isnull().sum()` |
| 5 | `prior_alerts_90d` | Sentinel value 999 — likely indicates a system error or missing data coded as integer | 6 | `df['prior_alerts_90d'].describe()` or `df[df['prior_alerts_90d'] > 20]` |
| 6 | `days_since_last_txn` | Null/missing values | 34 | `df.isnull().sum()` |
| 7 | `risk_score` | Values > 1.0 — outside valid normalized range | 11 | `df[df['risk_score'] > 1.0]` |
| 8 | `analyst_confidence` | Value -1 — legacy code for "not rated"; not valid on the 0–10 scale | 19 | `df['analyst_confidence'].value_counts()` |
| 9 | `fraud_confirmed` | Value 2 — invalid for a binary flag | 4 | `df['fraud_confirmed'].value_counts()` |
| 10 | `investigation_complete` | Null/blank values — appears as NaN in pandas (originally blank entries) | 7 | `df['investigation_complete'].isnull().sum()` |
| 11 | `escalation_date` | Five rows use MM/DD/YYYY format instead of YYYY-MM-DD | 5 | Visual inspection or `pd.to_datetime()` parse errors |

---

## Privacy and Handling Notes

- **`account_masked`** is a masked representation of a customer account identifier. It is not directly identifiable, but it must be treated with caution as it is PII-adjacent.
- **Do not include `account_masked` in any visualization, chart, or exported output.**
- **Do not paste rows containing `account_masked` into any AI prompt interface.**
- This is fully synthetic data generated for training purposes only. It does not represent real customers, accounts, or transactions at Hartwell Financial Services or any other institution.
- Treat this dataset as Internal tier under Hartwell's data classification policy.

---

## Business Rules

| Rule | Definition |
|---|---|
| `fraud_confirmed` | 0 = not confirmed fraud, 1 = confirmed fraud. No other values are valid. |
| `analyst_confidence` | Scale 0–10. 9–10 = high confidence of fraud, 5–8 = moderate, 0–4 = low. -1 is an invalid legacy code and must be excluded from all calculations. |
| `risk_score` | 0.0 = no detectable risk signal, 1.0 = maximum risk signal from alert engine. Values above 1.0 are data entry errors. |
| `prior_alerts_90d` | Valid range is 0–20. Values of 999 are sentinel errors and must not be included in statistical summaries. |
| `transaction_amount` | Must be > 0. Negative values indicate a data entry or system error. |
| `investigation_complete` | Valid values are Yes, No, Pending only. Empty strings are invalid and must be imputed or removed with justification. |
