# RIFCC-DA Prompt Pattern

Use this six-part pattern in every lab phase:

1. **Role** — who Copilot should act as (for example: Data Profiling Analyst).
2. **Input** — exact files attached with `#filename`.
3. **Format** — output shape (script path, markdown table, checklist).
4. **Constraints** — tooling and policy limits (pandas only, no PII-adjacent output, no external calls).
5. **Checks** — explicit validations before accepting output.
6. **Data-specific assumptions** — sentinel handling, null handling, and business caveats.

## Reusable skeleton

```text
Role: [analyst/engineer role]
Input: #[dataset], #[schema], #[prior artifact]
Format: Write [file path] and [expected sections]
Constraints: [libraries], [privacy restrictions], [do-not-do list]
Checks: [numeric checks], [completeness checks], [policy checks]
Data assumptions: [sentinel values], [null policy], [date handling]
```

## Phase mapping in this lab

- **Phase 1**: profile data and save `outputs/[X]_profile.md`
- **Phase 2**: clean data to `outputs/[scenario]_clean.csv` and capture decisions in `outputs/[X]_cleaning_decisions.md`
- **Phase 3**: build one dashboard `outputs/[X]_dashboard.html`
- **Stage 4 (optional)**: synthesize report `outputs/[X]_analysis_report.md`
