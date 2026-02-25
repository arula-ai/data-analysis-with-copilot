# Data Risk Review
**Stage:** 0 | **Agent Mode:** Data Risk & Policy Reviewer | **Time Budget:** 10 min
**Save to:** `outputs/00_data_risk_review.md`

---

## Purpose
This document records the sensitivity classification for every column in the dataset before analysis begins. It is the governance record for this lab session and determines what can and cannot appear in downstream outputs.

---

## Data Classification Assessment

> Fill in the table below for all 15 columns. Reference `data/schema.md` for column descriptions and `reference/responsible_use.md` for classification tier definitions.

| Column Name | Data Type | Sensitivity Tier | Risk Notes | Recommended Handling |
|---|---|---|---|---|
| alert_id | | | | |
| account_masked | | | *Pre-flagged: PII-adjacent — see schema.md* | *Must not appear in any output* |
| region | | | | |
| alert_type | | | | |
| transaction_amount | | | | |
| prior_alerts_90d | | | | |
| account_age_days | | | | |
| days_since_last_txn | | | | |
| risk_score | | | | |
| analyst_confidence | | | | |
| fraud_confirmed | | | | |
| analyst_id | | | | |
| investigation_complete | | | | |
| escalation_date | | | | |
| client_segment | | | | |

**Sensitivity Tiers:** Public | Internal | Confidential | Restricted

---

## Columns Requiring Special Handling

> List any columns that require extra care before analysis, visualization, or sharing. Explain what specific handling is required.

1. `account_masked` — *Excluded from all visualizations, printed DataFrames, and exported files. PII-adjacent even when masked.*
2. *[Add additional columns here with specific handling instructions]*

---

## What Must NOT Appear in Any Output

> Check all that apply based on your classification review above.

- [x] `account_masked` — must not appear in charts, exports, print statements, or executive summaries
- [ ] *[Add any additional columns you identified as requiring exclusion]*

**Justification:** *Write one sentence explaining why each flagged column must be excluded.*

---

## Pre-Analysis Checklist

Confirm the following before proceeding to Stage 1:

- [ ] All 15 columns classified with a sensitivity tier
- [ ] `account_masked` explicitly flagged and handling documented
- [ ] `reference/responsible_use.md` has been read and understood
- [ ] The dataset is confirmed as Internal (Synthetic) tier — no real customer data
- [ ] You understand what approval would be required if this were Confidential or Restricted data

---

## Analyst Confirmation

| Field | Value |
|---|---|
| Analyst Name | |
| Date | |
| Dataset Reviewed | `data/transaction_alerts.csv` |
| Schema Reference | `data/schema.md` |
| Policy Reference | `reference/responsible_use.md` |
| Sign-off | *I confirm I have read the responsible use policy and completed this review before beginning analysis.* |
