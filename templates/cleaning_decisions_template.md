# Cleaning Decisions Log
**Stage:** 2 | **Agent Mode:** Data Cleaning Engineer | **Time Budget:** 25 min
**Save to:** `outputs/[X]_cleaning_decisions.md` *(replace [X] with your scenario letter: A, B, or C)*

---

## Purpose
This document records every transformation applied to your scenario dataset. It is the audit trail for cleaning decisions — required for any analysis conducted on financial or operational data. Every row drop and imputation must have a written business justification.

---

## Row Counts

| Checkpoint | Row Count |
|---|---|
| **Pre-cleaning (raw)** | *(fill in before any transformation)* |
| After handling duplicates | |
| After handling invalid categorical values | |
| After handling null/invalid numeric values | |
| After handling sentinel values | |
| After handling date format inconsistencies | |
| *(add more checkpoints as needed)* | |
| **Post-cleaning (final)** | *(fill in after all transformations)* |
| **Rows removed total** | *(calculate: pre minus post)* |

> **If rows removed > 10% of total:** Document why this is analytically acceptable and what bias it might introduce.

---

## Transformations Applied

> Document every transformation. One row per issue addressed.

| Column | Issue Found | Action Taken | Business Justification | Rows Affected |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| *(add more as needed)* | | | | |

> **Action taken options:** Dropped row | Standardized value | Imputed with [method] | Flagged for review | Excluded from calculations | Reformatted

---

## Sentinel and Legacy Code Handling

> Document each sentinel or legacy code separately with explicit handling decision.

| Column | Value | Meaning | Handling Decision |
|---|---|---|---|
| | | | |

---

## Decisions NOT Taken

> List issues you identified but chose NOT to fix. Document why.

- *Example: "Did not impute null days_since_last_payment — business context unclear whether null means 'never transacted' or 'data missing'. Flagged for follow-up."*
- *[Add your own entries]*

---

## Cleaning Script Location

Script: `scripts/clean_[scenario].py`

Cleaned output saved to: `outputs/[dataset]_clean.csv`

Script reviewed line-by-line before execution: [ ] Yes | [ ] No

---

## EDA Findings — [Scenario Name] [Period]

> **Instructions:** Complete this section at the end of Phase 2B. Attach this file with `#outputs/A_eda_findings.md` in your Phase 3 visualization prompt.

**Denominator:** ___ confirmed-valid rows (after excluding anomaly_confirmed = 2 or equivalent sentinel, n=___)

### Finding 1 — Concentration Risk (from EDA Prompt 1)
[Category dimension 1] × [category dimension 2] shows the highest anomaly/issue rate: ___% (n=___)
Portfolio average: ___%
[Note if n<30: "(small sample — interpret with caution)"]

### Finding 2 — Temporal Pattern (from EDA Prompt 2)
Pattern type: [trend / spike / noise]
Range: min=___ ([period ___]) to max=___ ([period ___])
Operational implication: [one sentence — e.g. "spike in week 43 needs root cause" OR "escalating trend needs control tightening"]

### Finding 3 — Geographic / Segment Exposure (from EDA Prompt 3)
PRIORITY segment: [name] — [count] confirmed anomalies/issues, $[total_exposure] total exposure ([%] of portfolio)
[If no single PRIORITY segment (top-2 in both count and dollar): document which segment leads on each dimension separately]

### Finding 4 — Model / Score Validation (from EDA Prompt 4)
Model verdict: [STRONG SIGNAL / WEAK SIGNAL / INVERTED]
Separation ratio (confirmed vs non-confirmed): [___]
[If INVERTED: ⚠️ Flag as critical finding — risk model is miscalibrated. Escalate before briefing.]

---

## Cleaning Quality Checks

Run these assertions after cleaning to verify output is correct:

```python
# Verify no duplicates on primary key
assert df_clean.duplicated(subset=['id_col']).sum() == 0

# Verify no sentinel values remain in analysis columns
# (adapt to your scenario's sentinel values)

# Verify valid ranges on key numeric columns
# Example: assert (df_clean['score_col'] >= 0.0).all() and (df_clean['score_col'] <= 1.0).all()
```

Assertions passed: [ ] Yes | [ ] No — if No, describe what failed:
