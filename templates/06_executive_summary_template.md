# Executive Summary — Transaction Risk Analysis
**Stage:** 6 | **Agent Mode:** None (write yourself, use Copilot for drafting only) | **Time Budget:** 5 min
**Save to:** `outputs/06_executive_summary.md`

---

## Purpose
This document communicates the key findings from the Q4 2024 fraud alert analysis to a VP-level audience. No code, no jargon, no raw statistics without context. Every claim must be traceable to a specific finding in your Stage 3 exploratory insights.

---

## Context

> One paragraph: what data was analyzed, for what purpose, covering what time period, and by whom. Written for someone who has not seen any of the other lab outputs.

*Example: "This analysis examined 500 fraud alert cases from the Hartwell Financial Services Transaction Risk Alert System covering Q4 2024 (October–December). The dataset was profiled, cleaned, and analyzed to identify patterns in fraud confirmation rates across alert types, client segments, and geographic regions. Analysis was conducted by [name] using Python and GitHub Copilot on [date]."*

Your context paragraph:

---

## 3 Key Insights

> Exactly 3. No more, no less. Plain English. Each insight must be supported by a specific finding from Stage 3. Include one number or comparison to anchor each claim.

**Insight 1:**

> *(What the data shows — one clear, specific statement. Example: "Account Takeover alerts confirm as fraud at twice the rate of Velocity Check alerts — 41% vs. 20% — suggesting the alert engine's rule weighting may need recalibration.")*

**Insight 2:**

> *(What the data shows)*

**Insight 3:**

> *(What the data shows)*

---

## 2 Actionable Recommendations

> Exactly 2. Each recommendation must be tied directly to one of the insights above. Specific enough that a VP could assign it as an action item.

**Recommendation 1:**

> *(Specific action tied to Insight [N]. Example: "Prioritize Account Takeover alerts in analyst triage queues — a 20% increase in same-day review for this type could significantly improve confirmation timeliness given its elevated fraud rate.")*

**Recommendation 2:**

> *(Specific action tied to Insight [N])*

---

## 1 Risk Note

> One paragraph. What risk exists in these findings, the analysis methodology, or the data itself that the reader needs to be aware of before acting on them.

*Example: "This analysis is based on a single quarter of data and may not reflect full-year or multi-year fraud patterns. The Q4 period includes holiday-season transaction spikes that may inflate certain alert types. Recommendations should be validated against at least two additional quarters before being used to adjust staffing or rule thresholds."*

Your risk note:

---

## 1 Data Limitation Disclaimer

> One sentence. What this dataset and analysis explicitly cannot tell the reader.

*Example: "This dataset does not include resolved investigation outcomes beyond the binary fraud_confirmed flag, and therefore cannot distinguish between fraud types, loss amounts, or recovery rates."*

Your limitation:

---

## Methodology Note

> One sentence. What tools and methods were used.

*Example: "Analysis conducted using Python (pandas, matplotlib, seaborn) in VS Code with GitHub Copilot assistance; all generated code was reviewed and validated before execution."*
