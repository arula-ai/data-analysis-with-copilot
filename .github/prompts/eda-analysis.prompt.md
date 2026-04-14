---
mode: 'agent'
description: 'Run the Phase 2B treasury EDA — 4 analytical questions: concentration risk, temporal pattern, regional exposure, risk score validation — and write structured findings to outputs/A_eda_findings.md and outputs/A_eda_summary.txt.'
---

# Treasury EDA — Phase 2B

## Role
You are a Treasury Data Analyst building an evidence-based case for the Head of Treasury Operations. You run 4 analytical questions in sequence — each building on the previous. You do not summarize vaguely. Every finding cites exact numbers with numerator/denominator, n-count, and an operational implication.

## Input
- Cleaned treasury dataset: `outputs/treasury_payments_clean.csv`
- Reconciliation baseline: `outputs/A_reconciliation.txt` (use the final analysis-valid row count as your denominator)
- Attach using `#outputs/treasury_payments_clean.csv` when invoking this prompt.

## Task — Run all 4 analyses in sequence using pandas

### Analysis 1 — Concentration Risk: Where is the anomaly rate highest?
- Overall confirmed anomaly rate: count(anomaly_confirmed=1) / total valid rows — show as fraction AND % (e.g. "122/462 = 26.4%")
- Rate by payment_type: confirmed_count | total_count | rate_pct — ordered rate descending
- Rate by client_segment: same structure
- Cross-tab: anomaly rate per payment_type × client_segment — show only where confirmed_count >= 5, ordered rate descending, label highest cell with ***
- Consistency check: weighted average of per-category rates must equal overall rate

### Analysis 2 — Temporal Pattern: Is this getting worse or is it noise?
- Parse payment_date, group anomaly_confirmed=1 by ISO week
- Print: iso_week | week_start_date | confirmed_count | total_payments | weekly_rate_pct
- Calculate 3-week rolling average of confirmed_count
- State in plain English: (a) direction (b) volatility: max week − min week (c) pattern type: smooth trend / spike / random noise — and the operational implication of each

### Analysis 3 — Regional Exposure: Where should resources go?
- For confirmed anomalies only: region | confirmed_count | avg_payment_amount | total_exposure (count × avg)
- Sort by total_exposure descending
- Rank regions by confirmed_count AND by total_exposure — flag "PRIORITY" if top-2 in both
- State what % of total confirmed anomaly dollar exposure the top region accounts for
- Cross-check: sum of regional confirmed_counts must equal overall confirmed count from Analysis 1

### Analysis 4 — Risk Score Validation: Does the model actually work?
- Compare mean/std/min/max of risk_score for anomaly_confirmed=1 vs anomaly_confirmed=0
- Calculate separation ratio: mean(confirmed) / mean(non-confirmed)
  - >1.2: STRONG SIGNAL
  - 1.0–1.2: WEAK SIGNAL — flag for review
  - <1.0: INVERTED — confirmed anomalies score LOWER than non-anomalies — critical miscalibration
- Filter for the highest cross-tab cell from Analysis 1, print mean risk_score, compare to portfolio mean

## Output — Write 2 files

### File 1: `outputs/A_eda_findings.md`
Write the 4 structured findings in this format:
```
## EDA Findings — Treasury Anomaly Q4 2024

**Analysis denominator:** [n] confirmed-valid rows (500 raw − [count] anomaly_confirmed=2 excluded)
**Overall confirmed anomaly rate:** [n_confirmed]/[n_total] = [rate]%
**Key risk:** [one sentence citing the highest cross-tab cell]
**Model status:** [STRONG SIGNAL / WEAK SIGNAL / INVERTED]

### Finding 1 — Concentration Risk
Denominator: [n] confirmed-valid rows (anomaly_confirmed=2 excluded, n=[count])
Overall rate: [n_confirmed]/[n_total] = [rate]%
Highest payment_type: [type] — [rate]% (n=[count])
Highest client_segment: [segment] — [rate]% (n=[count])
Highest cross-tab cell: [type] × [segment] = [rate]% (n=[count]) ← headline risk
Sample size flag: [note if n<30]
Copilot confidence: [is the cross-tab result actionable? one sentence]

### Finding 2 — Temporal Pattern
Trend direction: [increasing / decreasing / stable]
Weekly range: min=[n] (week [ISO week]) to max=[n] (week [ISO week])
3-week rolling avg at end of Q4: [value]
Pattern type: [smooth trend / spike / random noise]
Operational implication: [one sentence]

### Finding 3 — Regional Exposure
Top region by total exposure: [region] — [count] anomalies, $[total_exposure] ([pct]% of all confirmed anomaly exposure)
PRIORITY region (top-2 in both count AND exposure): [region name, or "none identified"]
Verification: sum of regional counts = [n] (matches overall confirmed count from Finding 1: ✅ / ❌)
Resource recommendation: [one sentence]

### Finding 4 — Risk Score Validation
Mean risk_score (confirmed anomalies, n=[n]): [value]
Mean risk_score (non-anomalies, n=[n]): [value]
Separation ratio: [value]
Model verdict: [STRONG SIGNAL / WEAK SIGNAL / INVERTED]
Top cross-tab cell risk_score vs portfolio mean: [top cell mean] vs [overall mean] — [higher/lower/similar]
Recommendation: [one sentence — is this model reliable?]
```
If model verdict is INVERTED: prefix Finding 4 with ⚠️

### File 2: `outputs/A_eda_summary.txt`
Write a plain-text summary at the end containing:
- Analysis denominator (from A_reconciliation.txt)
- Overall confirmed anomaly rate (as fraction + %)
- Top cross-tab cell (type × segment, rate, n)
- Pattern type (trend/spike/noise)
- PRIORITY region (name + total exposure)
- Model verdict (STRONG SIGNAL / WEAK SIGNAL / INVERTED)
This file is used by Phase 3 to validate that chart values match EDA values.

### Technical script: `scripts/eda_treasury.py`
Write a standalone script that runs all 4 analyses in sequence with labeled section headers. Save it and run it immediately: `python scripts/eda_treasury.py`
Confirm both output files are written at the end.

## Constraints
- pandas only — no external libraries
- Exclude anomaly_confirmed = 2 from ALL calculations
- Do not print counterparty_masked in any output
- Every statistic must show numerator/denominator/rate — never just a percentage alone
- Do not claim causation — state correlations only
- Small samples (n<30): note "(interpret with caution)"

## Checks
- [ ] Analysis 1: weighted average of per-category rates equals overall rate
- [ ] Analysis 3: sum of regional confirmed_counts equals overall confirmed count from Analysis 1
- [ ] Analysis 4: separation ratio calculated correctly (confirmed mean ÷ non-confirmed mean)
- [ ] outputs/A_eda_findings.md written with all 4 findings
- [ ] outputs/A_eda_summary.txt written with all 6 key metrics
- [ ] scripts/eda_treasury.py runs standalone without errors
- [ ] counterparty_masked absent from all output
