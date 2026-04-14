# Responsible Use (Lab Policy)

This lab uses synthetic training data, but the same governance rules apply as production work.

## Allowed in prompts
- Schema files (`data/*_schema.md`)
- Cleaned, scenario-scoped datasets used in the exercises
- Aggregated counts and percentages needed for analysis

## Not allowed in outputs
- PII-adjacent field values (`counterparty_masked`, `user_id_masked`)
- Credentials, secrets, tokens, or internal connection details
- Claims that imply causation when only correlation is shown

## Required controls
1. Run `VERIFY_BEFORE_SEND.md` before attaching or sharing files.
2. Review generated scripts before execution.
3. Record row counts before/after cleaning.
4. Document sentinel and null handling decisions.
5. Verify every chart/report number against computed outputs.

## Scenario-specific reminders
- **Treasury (A):** exclude invalid `anomaly_confirmed = 2` from rates.
- **RCA (B):** do not surface `user_id_masked`; treat null response times as missing.
- **Modernization (C):** sentinel `9999` means “effort not assessed”; exclude from effort analysis.
