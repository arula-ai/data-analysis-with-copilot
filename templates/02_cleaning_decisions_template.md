# Cleaning Decisions Log
**Stage:** 2 | **Agent Mode:** Data Cleaning Engineer | **Time Budget:** 20 min
**Save to:** `outputs/02_cleaning_decisions.md`

---

## Purpose
This document records every transformation applied to `transaction_alerts.csv`. It is the audit trail for cleaning decisions — required for any analysis conducted on financial data. Every row drop and imputation must have a written business justification.

---

## Row Counts

| Checkpoint | Row Count |
|---|---|
| **Pre-cleaning (raw)** | *(fill in before any transformation)* |
| After handling duplicate alert_ids | |
| After handling invalid alert_type values | |
| After handling null/negative transaction_amount | |
| After handling invalid fraud_confirmed values | |
| After handling date format inconsistencies | |
| **Post-cleaning (final)** | *(fill in after all transformations)* |
| **Rows removed total** | *(calculate: pre minus post)* |

> **If rows removed > 10% of total:** Document why this is analytically acceptable and what bias it might introduce.

---

## Transformations Applied

> Document every transformation. One row per issue addressed.

| Column | Issue Found | Action Taken | Business Justification | Rows Affected |
|---|---|---|---|---|
| alert_id | 12 duplicate IDs | | | 12 |
| alert_type | 23 "VEL" values | | | 23 |
| transaction_amount | 8 negative values | | | 8 |
| transaction_amount | 15 null values | | | 15 |
| prior_alerts_90d | 6 sentinel values (999) | | | 6 |
| days_since_last_txn | 34 null values | | | 34 |
| risk_score | 11 values > 1.0 | | | 11 |
| analyst_confidence | 19 values of -1 | | | 19 |
| fraud_confirmed | 4 values of 2 | | | 4 |
| investigation_complete | 7 empty strings | | | 7 |
| escalation_date | 5 MM/DD/YYYY rows | | | 5 |

> **Action taken options:** Dropped row | Standardized value | Imputed with [method] | Flagged for review | Excluded from calculations | Reformatted

---

## Decisions NOT Taken

> List issues you identified but chose NOT to fix. Document why.

- *Example: "Did not impute null days_since_last_txn — business context unclear whether null means 'never transacted' or 'data missing'. Flagged for follow-up."*
- *[Add your own entries]*

---

## Cleaning Script Location

Script: `scripts/clean_alerts.py`

Cleaned output saved to: `data/transaction_alerts_clean.csv`

Script reviewed line-by-line before execution: [ ] Yes | [ ] No

---

## Cleaning Quality Checks

Run these assertions after cleaning to verify output is correct:

```python
# Verify no duplicates
assert df_clean.duplicated(subset=['alert_id']).sum() == 0

# Verify valid fraud_confirmed
assert df_clean['fraud_confirmed'].isin([0, 1]).all()

# Verify valid risk_score range
assert (df_clean['risk_score'] >= 0.0).all() and (df_clean['risk_score'] <= 1.0).all()

# Verify no negative transaction amounts
assert (df_clean['transaction_amount'].dropna() >= 0).all()
```

Assertions passed: [ ] Yes | [ ] No — if No, describe what failed:
