---
mode: 'agent'
description: 'Read all stage outputs and write a structured analyst report to the scenario-mapped output file (A/B/C) — executive summary, data quality table, EDA findings, dashboard insights, one recommendation, and two limitations.'
---

## Role
You are a Senior Data Analyst writing the final report for this scenario. Synthesize all outputs from previous stages into a structured, business-ready report. Every number must come from the provided outputs — do not estimate or fabricate.

## Input
Attach the following files for your selected scenario:

- **Scenario A (Treasury)**
  - `#outputs/A_profile.md` — profiling findings from Phase 1
  - `#outputs/A_eda_findings.md` — EDA findings with actual numbers from Phase 2B
  - `#scripts/clean_treasury.py` — sentinel handling decisions
- **Scenario B (RCA)**
  - `#outputs/B_profile.md` — profiling findings from Phase 1
  - `#outputs/B_cleaning_decisions.md` — EDA findings with actual numbers from Phase 2B
  - `#scripts/clean_logs.py` — sentinel handling decisions
- **Scenario C (Modernization)**
  - `#outputs/C_profile.md` — profiling findings from Phase 1
  - `#outputs/C_cleaning_decisions.md` — EDA findings with actual numbers from Phase 2B
  - `#scripts/clean_mainframe.py` — sentinel handling decisions

## Format
Write the report to the matching scenario output file with these six sections:
- Scenario A: `outputs/A_analysis_report.md`
- Scenario B: `outputs/B_analysis_report.md`
- Scenario C: `outputs/C_analysis_report.md`

**1. Executive Summary** — 2–3 sentences for a non-technical business leader. State what was analyzed, the key finding (with a number), and the recommended action. No field names, no code references.

**2. Data Quality Issues Found** — Table: Issue | Field | Sentinel or Flag Value | How Handled | Business Justification. Sourced from the profile and cleaning script.

**3. EDA Findings** — Table: Business Question | Methodology | Finding (with actual numbers from the cleaning decisions file) | Implication. Three rows — one per business question answered in Phase 2B.

**4. Visualization Insights** — Table: Chart | What It Shows | Key Pattern | Business Implication. Three rows — one per chart in the dashboard.

**5. Recommended Action** — One specific, measurable action. Name the action, the metric it targets, and the evidence that justifies it.

**6. Limitations** — Two specific limitations. Reference which rows were excluded during cleaning, how many, and what conclusions that prevents.

## Constraints
- No PII-adjacent fields (counterparty_masked, user_id_masked) anywhere in the report
- No fabricated numbers — use "data not available from current outputs" if a number is missing
- Executive Summary must be readable by a non-technical business leader
- Recommendation must be a direct action statement — not "consider reviewing"
- Save to the matching scenario file (`outputs/A_analysis_report.md`, `outputs/B_analysis_report.md`, or `outputs/C_analysis_report.md`) — do not output the full text in chat

## Checks
- [ ] Executive Summary is ≤ 3 sentences and free of field names and technical jargon?
- [ ] Section 3 Finding column contains actual numbers from the EDA outputs?
- [ ] Recommendation names a specific action, metric, and evidence?
- [ ] Limitations cite specific exclusion counts and their impact on conclusions?
- [ ] No PII-adjacent fields in any section?
- [ ] Report saved to the matching scenario file (`outputs/A_analysis_report.md`, `outputs/B_analysis_report.md`, or `outputs/C_analysis_report.md`)?
