---
mode: 'agent'
description: 'Run the Phase 2B EDA — 4 analytical questions: rate/concentration, temporal pattern, segment prioritization, model/score validation — and write structured findings to outputs/[X]_cleaning_decisions.md and outputs/[X]_eda_summary.txt.'
---

# Exploratory Analysis — Phase 2B

## Role
You are a Senior Data Analyst building an evidence-based case for a business or technical operations lead. You run 4 analytical questions in sequence — each building on the previous. Every finding cites exact numbers with numerator/denominator, n-count, and one operational implication. You do not summarize vaguely.

## Input
- Cleaned dataset: attach with `#outputs/[scenario_clean_csv]` (e.g., `#outputs/treasury_payments_clean.csv`, `#outputs/rca_app_logs_clean.csv`, `#outputs/mainframe_usage_clean.csv`)
- Reconciliation baseline: `outputs/[X]_reconciliation.txt` — read the **final analysis-valid row count** as your denominator before starting any analysis
- Schema reference: attach `#data/[scenario_schema.md]` for column definitions and valid value ranges

## Task — Run all 4 analyses in sequence using pandas

### Analysis 1 — Rate / Concentration: Where is the problem rate highest?
- Identify the primary **flag column** (e.g., `anomaly_confirmed`, `log_level`, `feature_status`) and the valid **flagged value** (e.g., `1`, `ERROR`/`FATAL`, `deprecated`)
- Overall flagged rate: count([flag_column]==[flagged_value]) / total valid rows — show as fraction AND % (e.g. "122/462 = 26.4%")
- Rate by **primary dimension** (e.g., `payment_type`, `service_name`, `module_name`): flagged_count | total_count | rate_pct — ordered rate descending
- Rate by **secondary dimension** (e.g., `client_segment`, `environment`, `complexity_tier`): same structure
- Cross-tab: rate per [primary dimension] × [secondary dimension] — show only where flagged_count >= 5, order rate descending, label highest cell with ***
- Consistency check: weighted average of per-category rates must equal overall rate

### Analysis 2 — Temporal Pattern: Is this getting worse or is it noise?
- Identify the **date/time column** (e.g., `payment_date`, `timestamp`, `last_accessed_date`)
- Group flagged events by time period (ISO week for daily data, hour or day for high-frequency data)
- Print: [period] | [period_start] | flagged_count | total_records | rate_pct
- Calculate 3-period rolling average of flagged_count
- State in plain English:
  - (a) Direction: increasing, decreasing, or stable?
  - (b) Volatility: max period − min period count
  - (c) Pattern type: smooth trend / spike / random noise
  - (d) Operational implication: one sentence on what this pattern requires (action / investigation / more data)

### Analysis 3 — Segment Prioritization: Where should resources go?
- For flagged records only, group by the **geographic or organizational dimension** (e.g., `region`, `environment`, `team_owner`)
- Calculate: [dimension] | flagged_count | [impact_metric] (e.g., avg_payment_amount, avg_response_time_ms, avg_migration_effort) | total_impact (flagged_count × impact_metric)
- Sort by total_impact descending
- Rank two ways: by flagged_count AND by total_impact — flag "PRIORITY" if top-2 in both
- State what % of total flagged impact the top segment accounts for
- Cross-check: sum of segment flagged_counts must equal overall flagged count from Analysis 1

### Analysis 4 — Model / Score Validation: Does the scoring model actually work?
- Identify the **score column** (e.g., `risk_score`, `response_time_ms`, `complexity_score`, `estimated_migration_effort_days`)
- Compare mean/std/min/max of [score_column] for the flagged group vs the non-flagged group
- Calculate separation ratio: mean(flagged) / mean(non-flagged)
  - > 1.2: STRONG SIGNAL — model differentiates well
  - 1.0–1.2: WEAK SIGNAL — flag for review
  - < 1.0: INVERTED — flagged records score LOWER than non-flagged — critical miscalibration
- Filter for the highest cross-tab cell from Analysis 1 and print mean [score_column], compare to portfolio mean
- If sentinel values exist in [score_column] (e.g., 9999, -1, 999): exclude them before calculating means

## Output — Write 2 files

### File 1: `outputs/[X]_cleaning_decisions.md`
Write the 4 structured findings using this format:

```
## EDA Findings — [Scenario Title] [Period]

**Analysis denominator:** [n] analysis-valid rows ([raw_count] raw − [excluded_count] invalid flag values excluded)
**Overall flagged rate:** [n_flagged]/[n_valid] = [rate]%
**Key risk:** [one sentence citing the highest cross-tab cell]
**Model status:** [STRONG SIGNAL / WEAK SIGNAL / INVERTED]

### Finding 1 — Concentration Risk
Denominator: [n] analysis-valid rows (invalid flag values excluded, n=[count])
Overall rate: [n_flagged]/[n_valid] = [rate]%
Highest [primary dimension]: [value] — [rate]% (n=[count])
Highest [secondary dimension]: [value] — [rate]% (n=[count])
Highest cross-tab cell: [primary] × [secondary] = [rate]% (n=[count]) ← headline risk
Sample size flag: [note "(interpret with caution)" if n<30, else "sample size adequate"]
Confidence note: [is the cross-tab result actionable? one sentence]

### Finding 2 — Temporal Pattern
Trend direction: [increasing / decreasing / stable]
Period range: min=[n] ([period label]) to max=[n] ([period label])
3-period rolling avg at end of dataset: [value]
Pattern type: [smooth trend / spike / random noise]
Operational implication: [one sentence]

### Finding 3 — Segment Prioritization
Top segment by total impact: [segment] — [count] flagged records, [impact_total] total impact ([pct]% of all flagged impact)
PRIORITY segment (top-2 in both count AND impact): [segment name, or "none identified"]
Verification: sum of segment counts = [n] (matches overall flagged count from Finding 1: ✅ / ❌)
Resource recommendation: [one sentence]

### Finding 4 — Model / Score Validation
Mean [score_column] (flagged group, n=[n]): [value]
Mean [score_column] (non-flagged group, n=[n]): [value]
Separation ratio: [value] (flagged mean ÷ non-flagged mean)
Model verdict: [STRONG SIGNAL / WEAK SIGNAL / INVERTED]
Top cross-tab cell score vs portfolio mean: [top cell mean] vs [overall mean] — [higher/lower/similar]
Recommendation: [one sentence — is this score reliable for prioritizing investigations?]
```
If model verdict is INVERTED: prefix Finding 4 with ⚠️

### File 2: `outputs/[X]_eda_summary.txt`
Write a plain-text summary containing exactly these 6 lines:
```
Denominator: [n] analysis-valid rows
Overall flagged rate: [n_flagged]/[n_valid] = [rate]%
Top cross-tab cell: [primary] × [secondary] = [rate]% (n=[count])
Pattern type: [smooth trend / spike / random noise]
Priority segment: [segment name] — [impact_total] total impact ([pct]%)
Model verdict: [STRONG SIGNAL / WEAK SIGNAL / INVERTED]
```
This file is the cross-validation anchor for Phase 3 — the dashboard summary header must match these values exactly.

### Technical script: `scripts/eda_[scenario].py` or `scripts/analyze_[scenario].py`
Write a standalone script that runs all 4 analyses in sequence with labeled section headers. Run it immediately: `python scripts/eda_[scenario].py`. Confirm both output files are written at the end.

## Constraints
- pandas only — no external libraries
- Exclude invalid flag values from ALL calculations (check schema for which values are invalid)
- Exclude sentinel values from score column before calculating means (check schema for sentinels: 9999, 999, -1, etc.)
- Do not print any PII-adjacent fields (counterparty_masked, user_id_masked, or any masked identifier)
- Every statistic must show numerator/denominator/rate — never just a percentage alone
- Do not claim causation — state correlations only
- Flag small-sample findings (n<30) with "(interpret with caution)"
- Validate denominator against `outputs/[X]_reconciliation.txt` before starting — stop if different

## Checks
- [ ] Denominator validated against `outputs/[X]_reconciliation.txt` before any analysis
- [ ] Analysis 1: weighted average of per-category rates equals overall rate
- [ ] Analysis 3: sum of segment flagged_counts equals overall flagged count from Analysis 1
- [ ] Analysis 4: separation ratio = flagged mean ÷ non-flagged mean (sentinel values excluded from score)
- [ ] `outputs/[X]_cleaning_decisions.md` written with all 4 structured findings
- [ ] `outputs/[X]_eda_summary.txt` written with exactly 6 lines
- [ ] EDA script runs standalone without errors
- [ ] No PII-adjacent fields in any output
- [ ] All statistics show fraction + % + n-count (never percentage alone)
