# Facilitator Guide — GitHub Copilot for Data Analysis Lab

**Instructor Reference Only — Not for Participants**

---

## 1. Session Overview

| Property | Value |
|---|---|
| Duration | 90 minutes |
| Recommended group size | 8–20 participants |
| Format | Individual work with brief group check-ins at 25, 50, and 75 minutes |
| Room setup | Individual workstations, VS Code installed, Python environment ready |
| Pre-session checks | Verify all participants have Copilot Chat enabled and `pip install pandas matplotlib seaborn numpy jupyter` completed |
| Dataset | `data/transaction_alerts.csv` — 500 rows, synthetic fraud alerts for fictional Hartwell Financial Services |

**Pre-session reminder for facilitators:** The dataset contains intentional data quality issues. Do not fix them. Do not hint that they exist until the debrief. Participants are expected to discover them through profiling.

---

## 2. Expected Outputs Per Stage (Ground Truth)

### Stage 0 — Data Risk Review
**Strong output:** All 15 columns classified with appropriate tiers. `account_masked` flagged as Confidential/PII-adjacent with "exclude from all outputs" documented. At least 3 specific handling recommendations. Policy referenced.
**Minimum acceptable:** 10+ columns classified, `account_masked` flagged, at least 1 handling restriction documented.
**Red flag:** Participant marks all columns as "Public" or "Low risk" without reading schema. Prompt: *"What makes `account_masked` different from `alert_id`? Read the schema note for that column."*

### Stage 1 — Data Profiling
**Strong output:** All 11 issues identified and documented with exact counts. Code was executed. Copilot assumptions listed separately. Sentinel values (999, -1) correctly identified as distinct from normal outliers.
**Minimum acceptable:** At least 8 issues found, code executed, null counts documented per column.
**Red flag:** Participant saves profiling output without running the code. Prompt: *"Show me the actual output from running this script. What did the terminal print?"*

### Stage 2 — Data Cleaning
**Strong output:** `clean_alerts.py` with one justification comment per transformation. Row counts printed at start, after each major step, and at end. Negative `transaction_amount` handled with a written business reasoning. Date format inconsistency resolved.
**Minimum acceptable:** Script runs without errors, row counts before/after documented, no silent drops.
**Red flag:** Cleaning script drops all nulls in one line with `df.dropna()`. Prompt: *"How many rows did that remove? Which business decision justifies removing all of them?"*

### Stage 3 — Exploratory Analysis
**Strong output:** 2+ specific business questions answered with plain-English narrative. Assumptions listed. Limitations listed. No causal claims.
**Minimum acceptable:** 1 business question answered, findings in plain English, one assumption documented.
**Red flag:** Participant produces charts instead of narrative. Prompt: *"What would you tell the VP of Fraud Operations if you had 2 minutes and a whiteboard?"*

### Stage 4 — Visualization
**Strong output:** 4 charts, all with titles, labeled axes with units, Y-axis starting at 0, no 3D, no `account_masked`, each with interpretation cell.
**Minimum acceptable:** 4 charts with titles and axis labels, no `account_masked` visible.
**Red flag:** Charts have no labels or titles. Prompt: *"If someone printed this chart with no context, what would they know from looking at it?"*

### Stage 5 — Audit
**Strong output:** All generated files reviewed, findings table with specific severity ratings, evidence shown for "no issues" categories, corrective actions documented.
**Minimum acceptable:** `clean_alerts.py` reviewed, at least one finding documented, `account_masked` confirmed absent from outputs.
**Red flag:** Participant gives clean bill of health without showing review evidence. Prompt: *"Show me where in the code you checked for external network calls."*

### Stage 6 — Executive Summary
**Strong output:** Exactly 3 insights, 2 recommendations, 1 risk, 1 limitation, written in plain English with no code references or jargon. Each insight traceable to Stage 3 findings.
**Minimum acceptable:** 3 insights and 2 recommendations present, no code or pandas references in text.
**Red flag:** Summary is a bullet list of data operations performed rather than business findings. Prompt: *"Read the first paragraph to me out loud. Would a VP understand what the data shows from hearing that?"*

---

## 3. All 11 Intentional Data Quality Issues

| Issue # | Column | Description | Count | Expected Discovery Method | Stage |
|---|---|---|---|---|---|
| 1 | `alert_id` | 12 duplicate IDs — same alert_id in multiple rows | 12 | `df.duplicated(subset=['alert_id']).sum()` | 1 |
| 2 | `alert_type` | Value "VEL" instead of "Velocity Check" — encoding inconsistency | 23 | `df['alert_type'].value_counts()` | 1 |
| 3 | `transaction_amount` | Negative values — invalid for a transaction amount | 8 | `df[df['transaction_amount'] < 0]` | 1 |
| 4 | `transaction_amount` | Null/missing values | 15 | `df.isnull().sum()` | 1 |
| 5 | `prior_alerts_90d` | Sentinel value 999 — system error or uncoded missing | 6 | `df['prior_alerts_90d'].describe()` or `df[df['prior_alerts_90d'] > 20]` | 1 |
| 6 | `days_since_last_txn` | Null/missing values | 34 | `df.isnull().sum()` | 1 |
| 7 | `risk_score` | Values > 1.0 — outside valid normalized range (data entry error) | 11 | `df[df['risk_score'] > 1.0]` | 1 |
| 8 | `analyst_confidence` | Value -1 — legacy code for "not rated," invalid on 0–10 scale | 19 | `df['analyst_confidence'].value_counts()` | 1 |
| 9 | `fraud_confirmed` | Value 2 — invalid for binary flag | 4 | `df['fraud_confirmed'].value_counts()` | 1 |
| 10 | `investigation_complete` | Null/blank values — originally blank entries, appears as NaN in pandas | 7 | `df['investigation_complete'].isnull().sum()` | 1 |
| 11 | `escalation_date` | 5 rows in MM/DD/YYYY format instead of YYYY-MM-DD | 5 | Visual inspection or `pd.to_datetime()` parse errors | 2 |

---

## 4. Common Failure Patterns and Coaching Interventions

| Stage | Common Failure | Root Cause | Coaching Intervention |
|---|---|---|---|
| 0 | Marks all columns as "Internal — no restrictions" | Did not read schema.md or responsible_use.md | "Open schema.md and find the note about account_masked. What does it say about including it in outputs?" |
| 0 | Skips policy doc entirely and jumps straight to Copilot | Treats Stage 0 as optional overhead | "Stage 0 is the governance checkpoint. In a real engagement, skipping this creates legal exposure. Read it first." |
| 1 | Accepts Copilot's profiling output without running the code | Trusts AI output over verified execution | "What does your terminal actually show? Run the script and show me line 3 of the output." |
| 1 | Finds only 3–4 issues, not the expected 8+ | Didn't use value_counts() on categoricals or check schema ranges | "What does df['analyst_confidence'].value_counts() show? Is -1 a valid value?" |
| 2 | Cleaning script uses dropna() with no parameters | Copilot generated it; participant didn't read it | "How many rows does that remove? Run df.dropna().shape and compare to df.shape." |
| 2 | Imputes without stating assumption | Copied Copilot output, didn't add justification comment | "What business rule justifies using the median here? Write that as a comment in the script." |
| 3 | Produces a list of stats instead of business findings | EDA mindset vs. analyst mindset | "Translate this into one sentence a fraud operations manager would put in a status update." |
| 3 | Makes causal claims — "X causes Y" | Didn't apply the constraint | "What would you need to show causation here? This dataset can't establish that — change to 'is associated with.'" |
| 4 | Y-axis starts at 0.6, making a 5% difference look huge | Copilot's default, participant didn't check | "Open exercises/flawed_visualization.py — VIZ ERROR 1 is exactly this. What does the fix look like?" |
| 4 | Produces charts without interpretation cells | Focused on code, not analysis | "If someone saw this chart with no context, what would they know? Write that as a markdown cell." |
| 5 | Gives "looks fine" audit without showing evidence of review | Audit feels like bureaucracy, not analysis | "Show me where in clean_alerts.py you confirmed there are no calls to urllib or requests." |
| 5 | Rates all findings as "Low" to minimize attention | Conflict avoidance or incomplete review | "If a script prints account_masked to the console in a shared CI/CD environment, is that Low severity?" |
| 6 | Executive summary reads like a technical changelog | Wrote for analyst audience, not VP | "Read the first sentence aloud. Does a VP need to know what dropna() does?" |
| 6 | Writes more than 3 insights | More is not better here | "Pick the 3 most actionable. If you had one slide, which 3 findings matter most to the fraud ops team?" |

---

## 5. Timing Guidance

| Check-in | Time | Typical State | Action if Behind |
|---|---|---|---|
| First check | 25 min | Should be finishing Stage 1 | Stage 0 is lightweight — anyone still there needs coaching; skip the second profiling check and go straight to issue log |
| Second check | 50 min | Should be finishing Stage 2 | Stage 2 is the most time-consuming; if stuck on cleaning script, have participant use exercises/flawed_cleaning_script.py as a reference for what to fix |
| Third check | 75 min | Should be finishing Stage 4 | Stage 5 and 6 are often rushed; if behind, combine: generate audit and summary together, focus on quality of 3 insights over completeness of audit |

**Where participants typically fall behind:**
- Stage 2 is the most time-consuming — allow 20–25 minutes; reduce Stage 3 to 10 if needed
- Stage 6 is often rushed — reinforce at 75-minute mark that 5 minutes is sufficient if Stage 3 findings are solid
- Stage 1 tends to be underestimated — running the code takes time; allow 15 minutes

---

## 6. Debrief Discussion Questions

**Stage 0:**
- "What would have happened if you had started analysis without reviewing the sensitivity of `account_masked`? Where could it have ended up?"
- "Under Hartwell's policy, what approval would you need to analyze Restricted-tier data with Copilot?"

**Stage 1:**
- "How many of the 11 data quality issues did you find? Which one was hardest to detect? Why?"
- "If you had run an analysis on the raw data without profiling first — which issue would have caused the most damage to your findings?"

**Stage 2:**
- "What business decision did you make about the 8 negative transaction_amount values? What assumption does that decision make?"
- "If a colleague asked 'why did you drop those 4 rows?' — would your clean_alerts.py answer that question?"

**Stage 3:**
- "What's the difference between what you found in Stage 3 and what you would have found if you'd analyzed the raw uncleaned data?"
- "You listed assumptions and limitations. Which limitation most constrains how much we can act on these findings?"

**Stage 4:**
- "What would a misleading version of chart 1 look like? How would you detect it in someone else's report?"
- "If a colleague sent you the visualization notebook — what's the first thing you'd check before forwarding it to leadership?"

**Stage 5:**
- "What does a clean audit mean? Is it possible to generate 'no findings' on AI-generated code in a regulated environment?"
- "If you found a High-severity issue in Stage 5 — what would you do before submitting Stage 6?"

**Stage 6:**
- "Read your three insights to the group. Could a VP make a decision from these? What's missing?"
- "What would you change about this analysis if you had access to 12 months of data instead of one quarter?"

---

## 7. Technical Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| Copilot Chat not responding | Extension not authenticated or rate limited | Check extension status bar; sign out and back into GitHub account |
| Copilot doesn't see the file | `#filename` not typed — pasted text instead | Retype `#` in chat input and use the file picker dropdown |
| Jupyter kernel not starting | Python path not configured or virtual env not active | `Ctrl+Shift+P` → "Python: Select Interpreter" → choose the correct Python 3.10+ path |
| `import pandas` fails | Pandas not installed | Run `pip install pandas matplotlib seaborn numpy jupyter` in the terminal |
| CSV not loading in notebook | Relative path issue | Verify notebook uses `'../data/transaction_alerts.csv'` not an absolute path |
| Custom prompt files not showing in dropdown | `.github/agents/` folder not in the workspace root | Verify folder is at workspace root, not inside a subfolder |
| Chart saves but doesn't display in notebook | Output not inline | Add `%matplotlib inline` at the top of the notebook or use `plt.show()` |
| `pd.to_datetime()` fails on escalation_date | Mixed date formats (5 rows in MM/DD/YYYY) | Use `pd.to_datetime(df['escalation_date'], infer_datetime_format=True, errors='coerce')` |
