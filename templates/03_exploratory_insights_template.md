# Exploratory Analysis Insights
**Stage:** 3 | **Agent Mode:** Exploratory Data Analyst | **Time Budget:** 15 min
**Save to:** `outputs/03_exploratory_insights.md`

---

## Purpose
This document translates the EDA code output into business-readable findings. Every insight here must be supported by actual numbers from the cleaned dataset, and every conclusion must be accompanied by the assumptions and limitations that bound it.

---

## Business Question

> State the primary business question this analysis is answering. Be specific.

*Example: "Which alert types and client segments have the highest confirmed fraud rates in Q4 2024, and what risk signal patterns are most associated with fraud confirmation?"*

Your question:

---

## Methodology

> 2–3 sentences: what analysis you ran, on what data subset, using what approach.

*Example: "Calculated fraud confirmation rates (fraud_confirmed = 1 / total valid alerts) grouped by alert_type and client_segment using the cleaned dataset (N = [X] rows). Excluded rows where fraud_confirmed was not 0 or 1, and excluded analyst_confidence = -1 from any confidence-related calculations. Used pandas groupby and value_counts for aggregation."*

Your methodology:

---

## Key Findings

> State 3–5 numbered findings in plain English — no code, no jargon. Write for a fraud operations manager who will use this to make staffing and process decisions.

1. *[Finding in plain English — include a number or percentage to anchor the claim]*
2. *[Finding in plain English]*
3. *[Finding in plain English]*
4. *(optional) [Finding in plain English]*
5. *(optional) [Finding in plain English]*

---

## Supporting Evidence

> For each finding above, show the actual numbers that support it.

**Finding 1:** *(paste the relevant output — a count, rate, table, or summary statistic)*

**Finding 2:**

**Finding 3:**

---

## Assumptions

> List every assumption that underlies this analysis. Be specific.

- *Example: "Excluded 4 rows where fraud_confirmed = 2 — treated as invalid per schema.md."*
- *Example: "Excluded analyst_confidence = -1 from all confidence analysis — treated as missing, not a low rating."*
- *Example: "Null transaction_amounts were excluded from transaction amount analysis but included in fraud rate calculation."*
- *[Add your own assumptions]*

---

## Limitations

> List what this dataset and this analysis cannot tell you. Be honest.

- *Example: "This dataset covers Q4 2024 only — seasonal patterns cannot be assessed."*
- *Example: "We cannot distinguish between fraud types (card fraud vs. account takeover) beyond the alert_type categories."*
- *Example: "Analyst confidence ratings are self-reported and may reflect individual bias rather than actual fraud signal quality."*
- *[Add your own limitations]*

---

## Copilot's Output vs. Your Interpretation

> Note any cases where Copilot's framing of a finding differed from your interpretation — and what you changed.

- *Example: "Copilot stated 'high risk scores cause fraud confirmation' — corrected to 'correlate with' to avoid an unsupported causal claim."*
- *[Add your own corrections]*
