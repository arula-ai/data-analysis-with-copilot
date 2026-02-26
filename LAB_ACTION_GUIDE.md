# GitHub Copilot for Data Analysis — Lab Action Guide

**90-Minute Hands-On Lab**
**Workflow:** Risk Review → Data Profiling → Cleaning → Exploratory Analysis → Visualization → Audit → Executive Summary

---

## Quick Reference

| Stage | Agent (select from dropdown) | Input | Core Artifacts |
|-------|------------------------------|-------|----------------|
| 0 | Data Risk Reviewer | `transaction_alerts.csv` + `schema.md` | `outputs/00_data_risk_review.md` |
| 1 | Data Profiling Analyst | `transaction_alerts.csv` | `outputs/01_data_profile.md` |
| 2 | Data Cleaning Engineer | `transaction_alerts.csv` + `01_data_profile.md` | `scripts/clean_alerts.py` + `outputs/02_cleaning_decisions.md` |
| 3 | Exploratory Data Analyst | cleaned dataset | `outputs/03_exploratory_insights.md` |
| 4 | Visualization Architect | cleaned dataset | `outputs/04_visualizations.ipynb` |
| 5 | Responsible Use Auditor | all scripts + all outputs | `outputs/05_audit_review.md` |
| 6 | — | all outputs | `outputs/06_executive_summary.md` |

**Total Duration:** 90 minutes

---

## How to Use Agents

Agents are selected using the **Agent Selector Dropdown** in Copilot Chat (not by typing `@`).

1. Open Copilot Chat (`Ctrl+Shift+I` / `Cmd+Shift+I`)
2. Click the **Agent Selector Dropdown** (top of chat panel)
3. Select the appropriate agent for your stage
4. Type your prompt and press Enter

The agent constrains how Copilot responds — it acts as a specialist for that stage's task.

---

## Before You Begin

- [ ] VS Code is open with Copilot Chat enabled — test with `Ctrl+Shift+I`
- [ ] `data/transaction_alerts.csv` is visible in the file explorer
- [ ] You have read `VERIFY_BEFORE_SEND.md` — do this now if you haven't
- [ ] `data/schema.md` is your ground truth for all column definitions and valid ranges
- [ ] All outputs go in the `/outputs/` folder — use the templates in `/templates/` to structure them
- [ ] Click the Agent Selector Dropdown to verify all 6 custom agents appear

---

## Stage 0 — Data Risk & Policy Review (10 min)

**Agent:** Data Risk Reviewer (select from dropdown)

**Objective:** Classify every column in the dataset by sensitivity and document what must not appear in any output.

### Actions

1. **Open input files:**

   ```
   data/transaction_alerts.csv
   data/schema.md
   reference/responsible_use.md
   ```

   Read `reference/responsible_use.md` first — understand what "Internal" classification means before activating Copilot.

2. **Select agent:** Click Agent Selector Dropdown → **Data Risk Reviewer**

3. **Enter prompt:**

   ```
   Using #schema.md and #transaction_alerts.csv, classify each of the 15 columns
   by sensitivity tier (Public / Internal / Confidential / Restricted).
   For each column: note the risk and recommend specific handling.
   Flag account_masked explicitly. List all columns that must not appear in any output.
   ```

4. **Review output for:**
   - All 15 columns assessed with a sensitivity tier
   - `account_masked` flagged as requiring caution — not just "low risk"
   - At least 3 specific handling recommendations documented
   - A clear list of columns that must NOT appear in any output or visualization

5. **Save to:** `outputs/00_data_risk_review.md`
   *(Use template: `templates/00_data_risk_review_template.md`)*
   Record your name and date in the analyst sign-off section.

**Hand-Off:** Paste into Copilot Chat:
> *"Summarize what I found in Stage 0 in 3 bullet points."*
> Save as `outputs/00_handoff.md`

---

## Stage 1 — Data Profiling (15 min)

**Agent:** Data Profiling Analyst (select from dropdown)

**Objective:** Generate profiling code to document data quality issues, null counts, and anomalies across all 15 columns.

### Actions

1. **Open input file:**

   ```
   data/transaction_alerts.csv
   ```

2. **Select agent:** Click Agent Selector Dropdown → **Data Profiling Analyst**

3. **Enter prompt:**

   ```
   Generate a pandas profiling script for #transaction_alerts.csv.
   Print: row count, null count per column (as count and %), value_counts for
   all categorical columns, describe() for all numeric columns.
   Flag values outside the valid ranges defined in #schema.md.
   Do not modify the dataframe.
   ```

4. **Run the generated code.** Do not trust Copilot's output without executing it — check the actual numbers.

5. **Enter follow-up prompt** (paste your actual script output):

   ```
   I ran the profiling script and found these results: [paste output].
   Which issues need to be fixed before analysis, and which might be meaningful fraud signals?
   ```

6. **Review output for:**
   - Row count documented (must be 500)
   - Null counts documented for all 15 columns
   - At least 8 data quality issues identified with column name, description, and count
   - `prior_alerts_90d` sentinel value 999 flagged separately — including it would skew fraud rate calculations
   - Results reflect actual data, not Copilot's assumptions

7. **Save to:** `outputs/01_data_profile.md`
   *(Use template: `templates/01_data_profile_template.md`)*

**Hand-Off:** Paste into Copilot Chat:
> *"Summarize what I found in Stage 1 in 3 bullet points."*
> Save as `outputs/01_handoff.md`

---

## Stage 2 — Data Cleaning (20 min)

**Agent:** Data Cleaning Engineer (select from dropdown)

**Objective:** Generate a safe, reversible cleaning script with a written justification for every transformation.

### Actions

1. **Open input files:**

   ```
   data/transaction_alerts.csv
   outputs/01_data_profile.md
   exercises/flawed_cleaning_script.py
   ```

   Identify all 6 labeled errors in `flawed_cleaning_script.py` before writing your own — this primes you to recognize the same mistakes in Copilot-generated code.

2. **Select agent:** Click Agent Selector Dropdown → **Data Cleaning Engineer**

3. **Enter prompt:**

   ```
   Using the issues found in #01_data_profile.md, generate scripts/clean_alerts.py
   to clean #transaction_alerts.csv.
   Every transformation must have an inline comment explaining the business justification.
   Print row count before cleaning, after each major step, and at the end.
   Save the cleaned data to data/transaction_alerts_clean.csv — do not overwrite the original.
   ```

4. **Review the code line by line** before running it. Verify each transformation has a justification comment.

5. **Enter follow-up prompt:**

   ```
   For the negative transaction_amount values: what are the business-valid options
   for handling them in a fraud alert dataset? What assumption does each option make?
   ```

6. **Review output for:**
   - Every row drop or imputation has a written justification in both the code and the decisions doc
   - Row count documented before AND after cleaning
   - `account_masked` never printed, exported, or referenced in cleaning logic unnecessarily
   - Negative `transaction_amount` values handled with explicit business justification
   - Date format inconsistencies in `escalation_date` resolved
   - `analyst_confidence = -1` excluded from any mean/average calculation

7. **Save to:** `scripts/clean_alerts.py` + `outputs/02_cleaning_decisions.md`
   *(Use template: `templates/02_cleaning_decisions_template.md`)*

**Hand-Off:** Paste into Copilot Chat:
> *"Summarize what I found in Stage 2 in 3 bullet points."*
> Save as `outputs/02_handoff.md`

---

## Stage 3 — Exploratory Analysis (15 min)

**Agent:** Exploratory Data Analyst (select from dropdown)

**Objective:** Answer business questions about fraud patterns using the cleaned dataset and translate findings into plain-English insights.

### Actions

1. **Open input file:**

   ```
   data/transaction_alerts_clean.csv
   ```

2. **Select agent:** Click Agent Selector Dropdown → **Exploratory Data Analyst**

3. **Enter prompt:**

   ```
   Using data/transaction_alerts_clean.csv and #schema.md:
   What alert types have the highest confirmed fraud rates by region?
   Show the code, then explain the finding in plain English for a fraud operations manager.
   State all assumptions. Do not claim causation from correlation.
   ```

4. **Enter second prompt:**

   ```
   Which client segment (Retail, Business, Premier, Institutional) has the highest
   fraud confirmation rate? Is this meaningful given the sample sizes? State your assumptions.
   ```

5. **Review output for:**
   - At least 3 specific business questions answered in plain English
   - All percentages cross-checked against raw counts
   - No causal claims — "correlates with" not "causes"
   - Assumptions explicitly listed (e.g., "this excludes rows with null transaction_amount")
   - Limitations explicitly listed (e.g., "this covers only Q4 2024")

6. **Save to:** `outputs/03_exploratory_insights.md`
   *(Use template: `templates/03_exploratory_insights_template.md`)*

**Hand-Off:** Paste into Copilot Chat:
> *"Summarize what I found in Stage 3 in 3 bullet points."*
> Save as `outputs/03_handoff.md`

---

## Stage 4 — Visualization (15 min)

**Agent:** Visualization Architect (select from dropdown)

**Objective:** Generate at least 4 labeled, honest charts from the cleaned dataset.

### Actions

1. **Open input files:**

   ```
   data/transaction_alerts_clean.csv
   exercises/flawed_visualization.py
   notebooks/starter_analysis.ipynb
   ```

   Identify all 4 labeled errors in `flawed_visualization.py` — know what a bad chart looks like before building a good one.

2. **Select agent:** Click Agent Selector Dropdown → **Visualization Architect**

3. **Enter prompt:**

   ```
   Using data/transaction_alerts_clean.csv and #schema.md, generate 4 charts
   as Jupyter notebook cells:
   1. risk_score distribution by fraud_confirmed status
   2. Confirmed fraud rate by alert_type (bar chart)
   3. transaction_amount distribution by client_segment (box plot)
   4. prior_alerts_90d vs confirmed fraud rate (bar chart)
   Rules: Y-axis starts at 0. No 3D charts. No account_masked in any chart.
   All axes labeled with units. All charts titled.
   Follow each chart cell with a 2–3 sentence markdown interpretation.
   ```

4. **Review each chart** before saving:
   - All 4 charts have titles
   - All axes labeled with units (e.g., "Transaction Amount ($)", "Fraud Confirmation Rate (%)")
   - Y-axis starts at 0 — no truncated scales
   - No 3D charts
   - `account_masked` not visible in any chart
   - Each chart followed by a 2–3 sentence interpretation cell

5. **Save to:** `outputs/04_visualizations.ipynb`

**Hand-Off:** Paste into Copilot Chat:
> *"Summarize what I found in Stage 4 in 3 bullet points."*
> Save as `outputs/04_handoff.md`

---

## Stage 5 — Responsible Use Audit (10 min)

**Agent:** Responsible Use Auditor (select from dropdown)

**Objective:** Review all generated code and outputs for security risks, privacy violations, and policy compliance issues.

### Actions

1. **Open input files:**

   ```
   scripts/clean_alerts.py
   outputs/04_visualizations.ipynb
   ```

2. **Select agent:** Click Agent Selector Dropdown → **Responsible Use Auditor**

3. **Enter prompt:**

   ```
   Review #clean_alerts.py for: external network calls, hardcoded sensitive values,
   operations that modify the source file, and any logic that could expose account_masked.
   Rate each finding: Low / Medium / High / Critical.
   ```

4. **Enter second prompt:**

   ```
   Review #04_visualizations.ipynb for: account_masked in chart labels,
   unmasked data in output cells, and chart integrity issues.
   ```

5. **Review output for:**
   - `clean_alerts.py` reviewed line by line — not just summarized
   - Any external library calls identified and flagged
   - `account_masked` confirmed absent from all chart outputs and print statements
   - At least one finding documented (even "no issues" must show evidence of review)
   - Required corrective actions listed or explicitly stated as "none required"

6. **Save to:** `outputs/05_audit_review.md`
   *(Use template: `templates/05_audit_review_template.md`)*

**Hand-Off:** Paste into Copilot Chat:
> *"Summarize what I found in Stage 5 in 3 bullet points."*
> Save as `outputs/05_handoff.md`

---

## Stage 6 — Executive Summary (5 min)

**Agent:** None — write this yourself, use Copilot only for drafting assistance.

**Objective:** Write a 1-page summary for a VP of Fraud Operations — 3 insights, 2 recommendations, 1 risk, 1 limitation.

### Actions

1. **Open input file:**

   ```
   templates/06_executive_summary_template.md
   ```

2. Fill in the Context paragraph yourself — do not delegate this to Copilot.

3. Draft your 3 key insights in plain English. No code, no jargon, no percentages without context.

4. **Enter prompt** (Copilot Chat, no agent selected):

   ```
   Draft an executive summary for a VP of Fraud Operations based on these findings:
   [paste your 3 key findings from Stage 3].
   Format: 3 numbered insights, 2 actionable recommendations, 1 risk note, 1 data limitation.
   Plain English. No jargon. No code. Maximum 400 words.
   ```

5. Verify every claim is traceable to a Stage 3 finding before saving.

6. **Review output for:**
   - Exactly 3 key insights — no more, no less
   - Exactly 2 actionable recommendations tied to the insights
   - At least 1 explicit risk note
   - At least 1 data limitation
   - Written for a non-technical executive — no code, no SQL, no pandas references
   - No `account_masked` or identifiable information anywhere in the document

7. **Save to:** `outputs/06_executive_summary.md`
   *(Use template: `templates/06_executive_summary_template.md`)*

---

## Completion Checklist

- [ ] `outputs/00_data_risk_review.md` — sensitivity ratings and handling recommendations
- [ ] `outputs/01_data_profile.md` — at least 8 data quality issues documented
- [ ] `scripts/clean_alerts.py` — commented cleaning script with row counts before/after
- [ ] `outputs/02_cleaning_decisions.md` — justification for every transformation
- [ ] `outputs/03_exploratory_insights.md` — fraud pattern insights in plain English
- [ ] `outputs/04_visualizations.ipynb` — at least 4 labeled charts with interpretations
- [ ] `outputs/05_audit_review.md` — code and output compliance review
- [ ] `outputs/06_executive_summary.md` — 3 insights, 2 recommendations, 1 risk, 1 limitation

**No artifact = incomplete lab. No exceptions.**

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Agent not in dropdown | Verify `.github/agents/` folder exists with `.agent.md` files |
| Copilot Chat not opening | Check extension status bar — sign out and back into GitHub |
| Jupyter kernel not starting | `Ctrl+Shift+P` → "Python: Select Interpreter" → choose Python 3.10+ |
| `import pandas` fails | Run `pip install pandas matplotlib seaborn numpy jupyter` in terminal |
| CSV not loading in notebook | Verify notebook uses `'../data/transaction_alerts.csv'` (relative path) |
| Output too generic | Reference files with `#transaction_alerts.csv` — use the `#` file picker |
| `pd.to_datetime()` error on dates | Use `errors='coerce'` — 5 rows have MM/DD/YYYY format (intentional issue) |
