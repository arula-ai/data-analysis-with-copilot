---
mode: 'agent'
description: 'Run the Phase 2B RCA EDA — 4 analytical questions: failure rate concentration, temporal pattern, service impact prioritization, response time model validation — and write structured findings to outputs/B_cleaning_decisions.md and outputs/B_eda_summary.txt.'
---

# RCA Log Analysis — Phase 2B

## Role
You are a Platform Reliability Analyst building an evidence-based incident brief for the Engineering Operations Lead. You run 4 analytical questions in sequence — each building on the previous. Every finding cites exact numbers with numerator/denominator, n-count, and one operational implication. Your goal: answer "Which service is failing, is it getting worse, and where should we focus the fix?"

## Input
- Cleaned log dataset: `outputs/rca_app_logs_clean.csv`
- Reconciliation baseline: `outputs/B_reconciliation.txt` — read the **final analysis-valid row count** as your denominator before starting
- Attach using `#outputs/rca_app_logs_clean.csv` when invoking this prompt.

## Task — Run all 4 analyses in sequence using pandas

### Analysis 1 — Failure Rate Concentration: Which service and environment are failing most?
- ERROR + FATAL rows = failure events. Flagged rate = count(log_level ∈ {'ERROR','FATAL'}) / total valid rows — show as fraction AND % (e.g. "87/274 = 31.8%")
- Rate by service_name: error_fatal_count | total_count | failure_rate_pct — ordered rate descending
- Rate by environment: same structure (prod vs staging)
- Cross-tab: failure rate per service_name × environment — show only where error_fatal_count >= 3, ordered rate descending, label highest cell with ***
- Consistency check: weighted average of per-service rates must equal overall failure rate

### Analysis 2 — Temporal Pattern: Is the failure rate escalating or stable?
- Parse timestamp (pd.to_datetime, errors='coerce'), group ERROR+FATAL events by hour or day (use whichever gives 8–15 meaningful time buckets)
- Print: [period] | [period_start] | failure_count | total_log_entries | failure_rate_pct
- Calculate 3-period rolling average of failure_count
- State in plain English:
  - (a) Direction: increasing, decreasing, or stable?
  - (b) Volatility: max period − min period count
  - (c) Pattern type: smooth trend / spike / random noise
  - (d) Operational implication: one sentence (trend → control tightening; spike → incident root cause; noise → more data needed)

### Analysis 3 — Service Impact Prioritization: Where should the fix go first?
- For ERROR + FATAL rows only, group by service_name
- Calculate: service_name | failure_count | avg_response_time_ms (non-null rows only) | impact_score (failure_count × avg_response_time_ms)
- Sort by impact_score descending
- Rank two ways: by failure_count AND by impact_score — flag "PRIORITY" if top-2 in both
- State what % of total failure impact the top service accounts for
- Cross-check: sum of service failure_counts must equal overall failure count from Analysis 1

### Analysis 4 — Response Time Model Validation: Does response time predict failures?
- Compare mean/std/min/max of response_time_ms for: log_level=ERROR or FATAL vs log_level=INFO or WARN
- Exclude null response_time_ms values from all calculations — do NOT fill nulls with 0
- Calculate separation ratio: mean(ERROR+FATAL response_time) / mean(INFO+WARN response_time)
  - > 1.2: STRONG SIGNAL — response time reliably indicates failure severity
  - 1.0–1.2: WEAK SIGNAL — response time is a weak predictor — flag for review
  - < 1.0: INVERTED — failures have LOWER response time than successes — investigate data collection
- Filter for the highest cross-tab cell from Analysis 1, print mean response_time_ms, compare to dataset mean
- Also print the top 3 error_codes by count for ERROR+FATAL rows (label NaN as "null — missing diagnostic")

## Output — Write 2 files

### File 1: `outputs/B_cleaning_decisions.md`
Write the 4 structured findings:
```
## EDA Findings — RCA Log Analysis

**Analysis denominator:** [n] analysis-valid rows ([raw_count] raw − [excluded_count] invalid entries excluded)
**Overall failure rate:** [n_failures]/[n_valid] = [rate]%
**Key failure:** [one sentence citing the highest service × environment cross-tab cell]
**Response time signal:** [STRONG SIGNAL / WEAK SIGNAL / INVERTED]

### Finding 1 — Failure Rate Concentration
Denominator: [n] analysis-valid rows
Overall failure rate: [n_failures]/[n_valid] = [rate]%
Highest service: [name] — [rate]% (n=[count])
Highest environment: [env] — [rate]% (n=[count])
Highest cross-tab cell: [service] × [environment] = [rate]% (n=[count]) ← headline failure
Sample size flag: [note if n<3]
Confidence note: [is this finding actionable? one sentence]

### Finding 2 — Temporal Pattern
Trend direction: [increasing / decreasing / stable]
Period range: min=[n] ([period]) to max=[n] ([period])
3-period rolling avg at end of dataset: [value]
Pattern type: [smooth trend / spike / random noise]
Operational implication: [one sentence]

### Finding 3 — Service Impact Prioritization
Top service by impact score: [service] — [failure_count] failures, avg [response_time]ms, impact score=[score] ([pct]% of total failure impact)
PRIORITY service (top-2 in both count AND impact): [service name, or "none identified"]
Verification: sum of service failure_counts = [n] (matches overall failure count from Finding 1: ✅ / ❌)
Fix recommendation: [one sentence — which service to prioritize and why]

### Finding 4 — Response Time Signal
Mean response_time_ms (ERROR+FATAL, n=[n]): [value]ms
Mean response_time_ms (INFO+WARN, n=[n]): [value]ms
Separation ratio: [value]
Signal verdict: [STRONG SIGNAL / WEAK SIGNAL / INVERTED]
Top cross-tab cell response_time vs dataset mean: [top cell mean]ms vs [overall mean]ms — [higher/lower/similar]
Top error codes: [code1] (n=[n]), [code2] (n=[n]), null (n=[n])
Recommendation: [one sentence — does response time reliably guide investigation priority?]
```
If signal verdict is INVERTED: prefix Finding 4 with ⚠️

### File 2: `outputs/B_eda_summary.txt`
Write a plain-text summary containing exactly these 6 lines:
```
Denominator: [n] analysis-valid rows
Overall failure rate: [n_failures]/[n_valid] = [rate]%
Top cross-tab cell: [service] × [environment] = [rate]% (n=[count])
Pattern type: [smooth trend / spike / random noise]
Priority service: [service name] — impact score=[score] ([pct]% of total)
Signal verdict: [STRONG SIGNAL / WEAK SIGNAL / INVERTED]
```

### Technical script: `scripts/analyze_logs.py`
Write a standalone script running all 4 analyses in sequence with labeled section headers. Run it immediately: `python scripts/analyze_logs.py`. Confirm both output files are written.

## Constraints
- pandas only — no external libraries
- Do not include `user_id_masked` in any printed output, table, or written file
- Exclude null response_time_ms from all averages — do NOT fill with 0
- Every statistic must show numerator/denominator/rate — never just a percentage alone
- Do not claim causation — state correlations and flag hypotheses explicitly
- Flag small-sample findings (n<3 for cross-tab) with "(interpret with caution)"
- Validate denominator against `outputs/B_reconciliation.txt` before starting

## Checks
- [ ] Denominator validated against `outputs/B_reconciliation.txt` before analysis
- [ ] Analysis 1: weighted average of per-service failure rates equals overall rate
- [ ] Analysis 3: sum of service failure_counts equals overall failure count from Analysis 1
- [ ] Analysis 4: null response_time_ms excluded — not zero-filled
- [ ] `outputs/B_cleaning_decisions.md` written with all 4 structured findings
- [ ] `outputs/B_eda_summary.txt` written with exactly 6 lines
- [ ] `scripts/analyze_logs.py` runs standalone without errors
- [ ] `user_id_masked` absent from all output
- [ ] All statistics show fraction + % + n-count
