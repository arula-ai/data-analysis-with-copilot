---
mode: 'agent'
description: 'Run the Phase 2 RCA EDA — service failure rates, response time by log level, error code distribution — and write 2-3 briefing bullets to outputs/B_cleaning_decisions.md.'
---

# RCA Log Analysis

## Role
You are an Application Reliability Engineer preparing an incident briefing for the Engineering Operations lead. Your job is to surface 2–3 plain-English findings from the cleaned log dataset — findings that are specific, evidence-backed, and point to the likely root cause. You frame everything around the operations lead's actual question: *"Which service is failing, is it getting worse, and what is causing it?"*

## Input
- Cleaned log dataset: `outputs/rca_app_logs_clean.csv`
- Schema reference: `data/rca_schema.md`
- Attach both using `#outputs/rca_app_logs_clean.csv` and `#data/rca_schema.md` when invoking this prompt.

## Format
Run the following three analyses using pandas, printing each with a clear section header:

**Section 1 — Service Failure Rate and Environment Split**
- For each `service_name`: count ERROR + FATAL rows and total rows; calculate failure rate (%)
- Print as a table: `service_name | total | error_fatal_count | failure_rate (%)` — ordered by failure rate descending
- Then print the environment split: count ERROR + FATAL rows per `environment` (prod vs staging), total rows per environment, and failure rate per environment
- Print as: `environment | total | error_fatal_count | failure_rate (%)`
- End with one sentence: which service has the highest failure rate, and whether the failure is concentrated in one environment or spans both

**Section 2 — Response Time by Log Level (Hypothesis Test)**
- Filter to rows where `response_time_ms` is NOT null. Do NOT fill nulls with 0.
- Calculate mean `response_time_ms` per `log_level` (INFO, WARN, ERROR, FATAL)
- Count how many non-null rows exist per log_level (base-n for each mean)
- Print as a table: `log_level | non_null_count | avg_response_time_ms` — ordered by severity (INFO, WARN, ERROR, FATAL)
- Also calculate mean `response_time_ms` per `service_name` (excluding nulls)
- Print as a table: `service_name | non_null_count | avg_response_time_ms` — ordered by avg descending
- End with one sentence: do ERROR rows have significantly higher response times than INFO rows? State the difference in ms. Note whether the highest-failure service from Section 1 is also the slowest service here.

**Section 3 — Error Code Distribution (Hypothesis Closure)**
- Filter to ERROR + FATAL rows only
- Run `value_counts()` on `error_code`, counting NaN separately (label it "null — missing diagnostic")
- Print as a table: `error_code | count` — ordered by count descending
- For the top 2 error codes (excluding null): print a sub-table showing `service_name | count` for rows with that error code
- End with one sentence: do ERR_001 and ERR_DB_001 dominate the error distribution? Note which BUG in `app_service.py` each top code traces back to (ERR_001 → AuthService SESSION_TTL=30s; ERR_DB_001 → TransactionProcessor DB_POOL_SIZE=3).

**Final output — write to file**
After printing all three sections to the terminal, write the following to `outputs/B_cleaning_decisions.md` using Python's `open()`:
- 2–3 plain-English bullet points formatted as a briefing for the Engineering Operations lead
- Each bullet must cite an actual number from the analysis above
- Cover: which service has the highest failure rate (with the rate %), whether response time confirms resource exhaustion as a factor, and which error codes dominate and what BUG they map back to

## Constraints
- `pandas` only — no external libraries
- Do not include `user_id_masked` in any printed output, table, or written file
- Do not impute or fill missing values — exclude nulls from averages and document the exclusion
- Do not claim causation — state correlations only and flag hypotheses as hypotheses
- Every statistic in the briefing bullets must match the printed terminal output exactly

## Checks
- [ ] Section 1 failure rates per service are consistent with totals (error_fatal_count / total)
- [ ] Section 2 averages exclude null response_time_ms — not zero-filled
- [ ] Section 3 filters to ERROR + FATAL only before running value_counts
- [ ] Section 3 counts NaN as a separate category (not ignored)
- [ ] `user_id_masked` does not appear anywhere in terminal output or in `outputs/B_cleaning_decisions.md`
- [ ] `outputs/B_cleaning_decisions.md` contains exactly 2–3 bullet points with specific numbers
