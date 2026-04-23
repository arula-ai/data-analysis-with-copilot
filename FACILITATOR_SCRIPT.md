# Facilitator Script — Data Analysis with GitHub Copilot
## Full Session · 90 Minutes · All Three Scenarios Intro + Sub-Lab A Walkthrough

> **How to use this script**
> Text under **SAY** is what you speak — adapt freely, keep the substance.
> Text under **SHOW** is what you put on screen.
> Text under **NOTE** is background context for you only — do not read aloud.
> `[CHECK-IN]` marks points where you pause and verify the room before moving on.
> Timing is shown at the start of each block — adjust based on group pace.

---

## BLOCK 1 — OPENING & CONTEXT · 0:00–0:10

### Welcome · 0:00

**SAY:**
Good morning everyone. Welcome to *Data Analysis with GitHub Copilot*.

What we are doing today is not a demo — it is a hands-on working session. You are going to load real-looking financial data, find what is wrong with it, clean it, analyse it, and build an interactive dashboard — all inside VS Code, with GitHub Copilot as your co-analyst.

By the end of this session you will have done something that trips most people up the first time they use Copilot for analysis work: you will have caught it making a mistake, understood why it made it, and corrected it before it turned into a wrong business decision.

That is the core skill. Everything else today is in service of that.

---

### What This Lab Is · 0:02

**SAY:**
The lab is structured around three fictional financial services companies, each with a different analytical problem. All three problems are ones you would encounter in the real world — anomaly investigation, root cause analysis, and modernisation prioritisation.

The three scenarios are:

- **Sub-Lab A — Treasury Anomaly Detection** — You are a Treasury Data Analyst at Meridian Asset Management. Your dataset is 500 Q4 2024 payment records. Your job is to find which payment types and regions have elevated anomaly rates, whether the pattern is worsening, and whether the company's own risk scoring model actually predicts what it is supposed to predict.

- **Sub-Lab B — Root Cause Analysis** — You are a Platform Reliability Analyst at Orion Payments Inc. A microservices payment platform has been degrading — transactions are failing intermittently and response times are spiking. Your dataset is 300 application log entries from the last 24 hours plus the application's source code. Your job is to find the root cause service and back it with log evidence.

- **Sub-Lab C — Product Modernisation** — You are a Product Data Analyst at Centrix Financial Systems. Engineering leadership needs to know which legacy mainframe features to modernise first — limited budget, can't do everything at once. Your dataset is 400 rows of feature usage metrics plus the legacy source code. Your job is to produce a data-backed prioritisation.

All three scenarios follow exactly the same four-phase workflow. The Copilot skills you build in one scenario transfer directly to the other two. You will choose one scenario to work through end to end. If you are more data-analysis oriented — Sub-Lab A. If you are more engineering oriented — Sub-Lab B. If you work in product or platform planning — Sub-Lab C.

---

### The Four Learning Objectives · 0:05

**SAY:**
Four things you will be able to do when you leave today.

One — use Copilot in VS Code to profile, clean, and analyse a dataset and translate it into findings that a business audience can act on. Not just code — conclusions.

Two — generate and validate policy-compliant visualisations from cleaned data. A self-contained interactive HTML dashboard your stakeholders can open in any browser.

Three — critically evaluate Copilot-generated code and output before you use it. Copilot is not always right. It can miss sentinel values, fill nulls with zeros silently, calculate a rate using the wrong denominator, and claim correlation is causation. You will catch all of those today.

Four — apply responsible-use practices before sharing any output. You will handle PII-adjacent fields, run a privacy preflight checklist, and know exactly what classification governs the data you are working with.

---

## BLOCK 2 — THE THREE DATASETS · 0:10–0:20

**SAY:**
Before we touch any tool, let me give you proper context on each dataset. Understanding the data is half the analysis — if you go in blind, Copilot goes in blind with you.

---

### Sub-Lab A Dataset — treasury_payments.xlsx · 0:10

**SHOW:** `data/treasury_payments.xlsx` and `data/treasury_schema.md` in VS Code Explorer.

**SAY:**
Sub-Lab A's input is `data/treasury_payments.xlsx` — an Excel file with 500 rows and 14 columns covering Q4 2024 treasury payment activity for a fictional asset management firm.

Here is what the columns represent:

| Column | What it is |
|---|---|
| `payment_id` | Unique transaction identifier — should be unique per row |
| `payment_date` | Date the payment was processed — has mixed format issues (MM/DD/YYYY vs YYYY-MM-DD) |
| `payment_type` | Category of payment instrument — Wire, ACH Batch, Check, EFT |
| `payment_amount` | Dollar value of the transaction — some rows have negative values (an intentional quality issue) |
| `region` | Geographic region — Northeast, Southeast, Midwest, West |
| `client_segment` | Type of client — Institutional, Sovereign Wealth, Endowment, Family Office |
| `counterparty_masked` | A masked identifier for the counterparty — **PII-adjacent. Never include in any output, chart, or print statement.** |
| `analyst_confidence` | Analyst's confidence score for their review — sentinel value **-1** means "not rated." Not a real score. |
| `prior_alerts_90d` | Number of prior alerts in the 90-day window — sentinel value **999** is a placeholder. Not a real count. |
| `risk_score` | Model-generated risk score (0 to 1) — used to validate whether the scoring model actually predicts anomalies |
| `anomaly_confirmed` | Binary flag — 0 = not an anomaly, 1 = confirmed anomaly, **2 = invalid flag value** |
| `review_status` | Status of the analyst review — some rows are blank |
| `payment_date_parsed` | A second date column — sometimes populated, sometimes not |

The dataset has **11 documented data quality issues** listed in `data/treasury_schema.md`. Phase 1 is about finding them all. Three are especially important because they affect analysis numbers directly:

- `anomaly_confirmed = 2` — these rows are real transactions with an invalid flag. They are **excluded from anomaly rate calculations** but retained in the clean dataset. They are not simply dropped.
- `prior_alerts_90d = 999` — placeholder. Replace with NaN. Do not average this.
- `analyst_confidence = -1` — not rated. Replace with NaN. Do not average this.

If any of these get through to analysis, the numbers are wrong. The reconciliation report at the end of Phase 2A is how we prove they did not.

**NOTE:**
The analytical question in Sub-Lab A is: *which payment type × client segment combination has the highest confirmed anomaly rate, is it trending over Q4, and does the risk_score model actually predict it?* The last question — model validation — often produces the most surprising finding. The separation ratio (mean risk score for confirmed anomalies vs non-confirmed) can reveal that the scoring model is inverted — confirmed anomalies actually score lower than non-anomalies. That is a critical finding that completely changes the recommendation.

---

### Sub-Lab B Dataset — rca_app_logs.csv + app_service.py · 0:13

**SHOW:** `data/rca_app_logs.csv` and `data/app_service.py` in VS Code Explorer.

**SAY:**
Sub-Lab B has two input files — not one. This is intentional. Root cause analysis requires code evidence AND log evidence together.

**File 1 — `data/app_service.py`**
This is the source code of a Python microservices platform that processes real-time payment transactions. It has five service classes:
- `TransactionProcessor` — handles payment transactions
- `AuthService` — manages session authentication
- `NotificationService` — sends alerts and notifications
- `PaymentGateway` — the external payment interface
- `DatabaseManager` — the database connection layer

Each service has intentional defects. Some are marked with `# BUG` comments — those are obvious. Some are structural defects with no annotation — those are harder to spot, and catching them is part of the skill. You read the code **before** you look at the logs, so you go into the log analysis with a hypothesis, not a blank slate.

**File 2 — `data/rca_app_logs.csv`**
300 log entries from the past 24 hours across all five services, with 9 columns:

| Column | What it is |
|---|---|
| `timestamp` | When the log entry was recorded — mixed format issues |
| `service_name` | Which service generated the entry |
| `log_level` | INFO, WARN, ERROR, FATAL |
| `request_id` | Unique ID for the transaction request — 8 duplicate IDs present |
| `response_time_ms` | How long the service took to respond in milliseconds — null on all FATAL rows (service crashed), and also null on some ERROR rows |
| `error_code` | Specific error code — null on 12 ERROR/FATAL rows |
| `environment` | prod or staging |
| `user_id_masked` | Masked user identifier — **PII-adjacent. Never include in any output, chart, or axis.** |
| `message` | Free-text log message |

The key data quality issue to watch: **FATAL rows have null `response_time_ms` because the service crashed** — that is expected and meaningful. If your cleaning script fills those nulls with zero, it drags the average response time down and makes the service look faster than it is. That is a real analytical error that the pre-written flawed analysis in Sub-Lab B makes. You will catch it.

---

### Sub-Lab C Dataset — mainframe_usage.xlsx + legacy_mainframe.py · 0:16

**SHOW:** `data/mainframe_usage.xlsx` and `data/legacy_mainframe.py` in VS Code Explorer.

**SAY:**
Sub-Lab C also has two input files — source code and data.

**File 1 — `data/legacy_mainframe.py`**
A legacy Python module representing a mainframe system with six functions — each corresponding to a business capability: payment processing, account reconciliation, fraud detection, reporting, user authentication, and batch processing. Each function has technical debt and intentional bugs. Your job is to assess migration complexity — which functions are highest risk to migrate — before looking at the usage data.

**File 2 — `data/mainframe_usage.xlsx`**
400 rows of feature usage metrics across the six legacy functions, with columns for:
- Monthly Active Users — how many users rely on each feature
- Error Rate — how often the feature fails in production
- Migration Effort Score — estimated complexity to migrate (note: sentinel value **9999** means the estimate was never captured)
- Business Criticality — classification of how important the feature is to operations
- Last Modified — when the feature was last changed (proxy for how much technical debt has accumulated)

The analytical output of Sub-Lab C is a prioritised list of 3–5 modernisation candidates with supporting evidence on both business impact and migration risk. A feature that is high impact AND high risk needs a different migration strategy than one that is high impact and low risk.

---

## BLOCK 3 — HOW COPILOT AGENTS WORK · 0:20–0:26

**SHOW:** VS Code Copilot Chat panel. Click the Agent Selector Dropdown.

**SAY:**
Now let me explain the two tools that make this lab work — agents and slash command prompts. These are the core mechanism. Once you understand them, the entire workflow makes sense.

---

### Agents — Specialist Personas · 0:20

**SAY:**
An agent in GitHub Copilot is a custom AI persona with a specific role, a specific set of tools it can use, and specific rules about what it must and must not do. You select an agent from the dropdown in Copilot Chat — it looks like a name selector, not a traditional settings panel.

Think of it this way: without an agent selected, Copilot is a generalist. It will try to help, but it has no specialisation. When you select the **Data Profiling Analyst** agent, you are loading a system prompt that tells Copilot: *"You are a Data Profiling Analyst working in VS Code with pandas. Never modify the source dataset. Always report null counts for every column. Always flag sentinel values separately from legitimate nulls. Write the output to a file — do not just show it in chat."*

You have seven agents in this lab. Each maps to a specific phase:

| Agent | When You Use It | What It Specialises In |
|---|---|---|
| **Data Profiling Analyst** | Phase 1 | Surfaces data quality issues — nulls, outliers, sentinels, format inconsistencies |
| **Data Cleaning Engineer** | Phase 2A | Generates cleaning scripts with inline business justification on every transformation |
| **Exploratory Data Analyst** | Phase 2B | Translates statistical patterns into plain-English business findings |
| **Visualization Architect** | Phase 3 | Builds labeled interactive Plotly charts in a self-contained HTML dashboard |
| **Report Writer** | Stage 4 | Synthesises all prior outputs into a structured written deliverable |
| **Data Risk Reviewer** | Optional | Reviews outputs for data quality and analytical risk before sharing |
| **Responsible Use Auditor** | Optional | Governance check — PII exposure, classification, prompt safety |

**SHOW:** Click through each agent in the dropdown slowly.

**SAY:**
You select the agent from this dropdown, **then** type your prompt. The order matters. If you type `/` first and browse the list, built-in VS Code commands like `/tests` appear in the same menu — selecting one by mistake produces an error that stops your session. Always select the agent first. Then type.

---

### What Is Inside an Agent · 0:23

**SHOW:** Open `.github/agents/data-profiling-analyst.agent.md` in VS Code.

**SAY:**
If you want to see exactly what an agent does — open the `.github/agents/` folder. Each agent is a markdown file. The top section is a YAML header that declares which VS Code tools the agent can use: run scripts in the terminal, write files to disk, read files, search the codebase. Below that is the actual instruction set in plain English.

The **Data Profiling Analyst** agent, for example, has these hard rules:
- Use pandas only — no external profiling libraries
- Treat profiling as read-only — never mutate the original dataframe
- Print all counts as both raw numbers and percentages
- Document every anomaly — do not summarise away edge cases
- Never report "no issues found" without showing the actual distributions that support that conclusion

These rules are what makes Copilot behave like a disciplined analyst rather than a code generator that happens to output some statistics. The agent is not magic — it is a well-written instruction set. You can read it, critique it, and understand exactly why Copilot responds the way it does.

---

### Slash Command Prompts · 0:25

**SHOW:** In Copilot Chat (with Data Profiling Analyst selected), type `/data-profiling`. Show it appearing.

**SAY:**
The second tool is slash command prompts. These live in `.github/prompts/` — each one is a pre-written, structured prompt template for a specific phase.

When you type `/data-profiling` after selecting the Data Profiling Analyst agent, you are not just typing a shortcut — you are loading a prompt file that contains:
- The exact role to play
- Which input files to expect (and what to do with each)
- The exact output format — what sections to write, what calculations to show
- Constraints — no PII in output, pandas only, no external calls
- Specific checks — what to validate before accepting the output

Think of slash command prompts as the structured brief you give to a consultant before they start work. A well-written brief produces a well-scoped deliverable. A vague one produces something you cannot use.

For each phase you have two options in the guide: use the slash command for a single structured shot, or use the individual prompts written out in the guide for a step-by-step approach. If this is your first time — use the individual prompts. You will learn more by reading each output before moving to the next one.

---

## BLOCK 4 — THE RIFCC-DA FRAMEWORK · 0:26–0:30

**SHOW:** `reference/PROMPT_PATTERN.md`

**SAY:**
Before we write a single prompt — one framework. This is the most important slide in the session and it is not a slide, it is a file: `reference/PROMPT_PATTERN.md`.

RIFCC-DA stands for: **Role, Inputs, Format, Constraints, Checks, Data-specific assumptions.**

Every analytical prompt you write today — and every analytical prompt you write after today — should hit all six elements. Let me show you the difference it makes.

**SHOW:** Type in Copilot Chat (no agent):

```
Analyze this data
```

**SAY:**
Generic request. Generic output — a describe() at best, maybe some value counts. No business context. No constraints. No PII check. Now the same intent written with RIFCC-DA:

**SHOW:** Type in Copilot Chat (Data Profiling Analyst selected):

```
Role: Data Profiling Analyst.
Inputs: #data/treasury_payments.xlsx and #data/treasury_schema.md.
Format: Python pandas script — print row count, null count per column as count and %, sentinel flag counts, value_counts for all categoricals.
Constraints: pandas only. Do not print counterparty_masked values. Never modify the source dataframe.
Checks: Flag any column with null % > 5%. Flag values outside schema-defined valid ranges. Flag sentinel 999 and -1 separately from nulls.
Data assumptions: Treat 999 in prior_alerts_90d as a sentinel — not a real count. Treat -1 in analyst_confidence as "not rated" — not a real score. Treat anomaly_confirmed = 2 as an invalid flag — not a valid binary value.
```

**SAY:**
Same intent. Completely different output quality. **Role** scopes the persona so Copilot knows what lens to apply. **Inputs** tells it exactly which files with the `#filename` reference syntax. **Format** specifies what to print and how. **Constraints** prevents PII from appearing in output and locks the tooling to pandas. **Checks** adds validation so Copilot self-reviews before responding. **Data assumptions** handles the critical edge cases that would otherwise slip through silently.

`reference/PROMPT_PATTERN.md` is your cheat sheet. Keep it open in a VS Code tab throughout the session.

---

## BLOCK 5 — RESPONSIBLE USE · 0:30–0:33

**SHOW:** `VERIFY_BEFORE_SEND.md`

**SAY:**
One non-negotiable before anyone touches data.

This file — `VERIFY_BEFORE_SEND.md` — is a three-question preflight checklist. Run it before attaching any file to Copilot Chat.

**Question 1 — Data classification:** Does this file contain Confidential or Restricted data? If yes — attach the schema only, not the raw data rows.

**Question 2 — PII and PII-adjacent fields:** Does the file contain personal or masked identifiers? In Sub-Lab A, `counterparty_masked` is PII-adjacent. In Sub-Lab B, `user_id_masked` is PII-adjacent. Neither field should appear in a printed DataFrame output, a chart label, a chart hover tooltip, an axis value, or an exported file. If it appears anywhere in your output — that is a governance failure, and the correct response is to stop, fix the prompt, and regenerate.

**Question 3 — Where is this going?** If the output is being shared externally — with a client, in an email, on a shared drive — run the full checklist before sharing.

The datasets today are synthetic. There is no real customer data here. But the behaviour you practice today is the behaviour you take back to production environments where the data is real. Treat `counterparty_masked` and `user_id_masked` as if they contained real names and real account numbers. Because in production, they will.

`[CHECK-IN]` Quick question — without opening anything — who can tell me what `counterparty_masked` is, and why it cannot appear in chart output?

> **Expected answer:** PII-adjacent masked identifier, Confidential classification tier. Acceptable to attach the schema file. Never the values. Take 1–2 answers.

---

## BLOCK 6 — ENVIRONMENT CHECK · 0:33–0:37

**SAY:**
Let's confirm everyone is ready before we split into scenario tracks. Open VS Code now and work through this checklist.

**SHOW:** Walk through the checklist on screen while participants check their own machines.

```
[ ] VS Code open with the repo root as the workspace folder
    (not a subfolder — the .github/ folder must be visible in Explorer)
[ ] Copilot Chat opens with Ctrl+Shift+I on Windows / Cmd+Shift+I on Mac
[ ] Agent Selector Dropdown shows at least 7 agents
[ ] Type / in Copilot Chat — lab slash commands appear
    (not only built-in commands like /tests or /explain)
[ ] data/, outputs/, and scripts/ folders visible in Explorer
[ ] Run in terminal: python scripts/verify_setup.py — all checks green
```

**NOTE:**
Most common setup failure: participant opened a subfolder as the workspace root. The `.github/` folder is not found and agents/slash commands do not appear. Fix: **File → Open Folder → navigate to repo root**. This accounts for ~80% of agent dropdown issues.

Second most common: pip dependencies missing. Run `pip install -r requirements.txt` from the repo root. If on the corporate network — use the `--index` flag with the Artifactory URL.

`[CHECK-IN]` Raise of hands — who sees 7 agents in the dropdown? If any hands are not up — fix those before proceeding. Do not move on with missing agents.

---

## BLOCK 7 — SCENARIO SELECTION · 0:37–0:40

**SAY:**
Three tracks from here. Take 30 seconds, pick your scenario, and open the corresponding SCENARIO_BRIEF.md.

**Sub-Lab A — Treasury Anomaly Detection:** More data-analysis focused. Heavy on pandas aggregation, rate calculations, and model validation. Best fit if you work with operational data or financial reporting.

**Sub-Lab B — Root Cause Analysis:** More engineering focused. Involves reading Python source code before touching the data, forming a hypothesis, then testing it against log evidence. Best fit if you work in SRE, platform reliability, or backend engineering.

**Sub-Lab C — Product Modernisation:** Prioritisation-focused. Combines code complexity assessment with usage data to produce a ranked recommendation. Best fit if you work in product, architecture, or technology planning.

**SHOW:**
```
scenarios/sub-lab-A-treasury/SCENARIO_BRIEF.md
scenarios/sub-lab-B-rca/SCENARIO_BRIEF.md
scenarios/sub-lab-C-modernization/SCENARIO_BRIEF.md
```

`[CHECK-IN]` Raise of hands — Sub-Lab A? Sub-Lab B? Sub-Lab C? Note the count. From here on, use the SUB_LAB_GUIDE.md for your chosen scenario as your primary guide. I will walk through Sub-Lab A on the shared screen — if you are on B or C, follow your own guide and flag me if you are stuck.

---

---

# SUB-LAB A — TREASURY ANOMALY DETECTION
## Full Phase Walkthrough

**Role:** Treasury Data Analyst — Operations Risk Team
**Company:** Meridian Asset Management (fictional)
**Dataset:** `data/treasury_payments.xlsx` — 500 Q4 2024 payment records
**Goal:** Identify elevated anomaly rate patterns by payment type, client segment, and region — and validate whether the risk scoring model predicts them
**Duration:** 50 minutes (0:40–1:30)

---

## STAGE 0 — SETUP & ORIENTATION · 0:40–0:45

**SAY:**
Open `scenarios/sub-lab-A-treasury/SUB_LAB_GUIDE.md`. This is your primary reference for the next 50 minutes.

Before you open any data file — open `data/treasury_schema.md` and read the Known Issues section. I want everyone to take 90 seconds and read it now.

**SHOW:** `data/treasury_schema.md` — scroll to the Known Issues section.

**SAY:**
The Known Issues section documents 11 specific data quality problems in this dataset. Three of them are critical to your analysis — write these down:

**One — `anomaly_confirmed = 2`.** The column should be a binary flag: 0 or 1. Some rows have a value of 2, which is invalid. These are real transactions with a bad flag. You do not drop them from the clean dataset — you exclude them from rate calculations. This distinction matters: the denominator for anomaly rate calculations is 500 minus duplicates minus negatives minus these invalid-flag rows.

**Two — `prior_alerts_90d = 999`.** This is a sentinel placeholder meaning "data not available." It is not a real count of 999 prior alerts. If it gets included in any average or sum, it inflates alert count statistics dramatically.

**Three — `analyst_confidence = -1`.** This means "not rated." The analyst reviewed this payment but did not assign a confidence score. It is not a real score of negative one. If it gets averaged in with real scores, it drags the mean down artificially.

If any of these three get through to your EDA phase without being handled — your numbers are wrong. Your denominator is wrong. Your rates are wrong. Your findings are wrong. Phase 2A's reconciliation report is how you prove they did not slip through.

---

## PHASE 1 — DATA PROFILING · 0:45–0:55

**What you are building:** `scripts/profile_treasury.py` + `outputs/A_profile.md`

**Why this phase exists:** You cannot write a good cleaning prompt without knowing exactly what is wrong. Phase 1 is intelligence gathering. Nothing gets modified. The source file is never touched.

**SAY:**
Let's go. In Copilot Chat — select **Data Profiling Analyst** from the agent dropdown. Then type `/data-profiling` and use the `#` reference syntax to attach two files: `#data/treasury_payments.xlsx` and `#data/treasury_schema.md`. Both files. Copilot uses the schema to know what values are valid — without it, it cannot flag `anomaly_confirmed = 2` as invalid because it does not know the column is supposed to be binary.

**SHOW:** Select Data Profiling Analyst → type `/data-profiling` → attach both files.

**SAY:**
When Copilot responds, it will generate a Python script in the chat panel. **Do not copy-paste it manually.** Hover over the code block — you will see an **Insert into New File** button appear. Click it. VS Code will open the code in a new tab. Save it as `scripts/profile_treasury.py`. Then run it from the VS Code terminal:

```
python scripts/profile_treasury.py
```

**SHOW:** Hover over code block → Insert into New File → Save As → `scripts/profile_treasury.py` → run in terminal.

**SAY:**
Before you accept the output — read the script before you run it. Four things to check:

1. Does it call `pd.read_excel('data/treasury_payments.xlsx')` — not read from a different path?
2. Does it print `counterparty_masked` column statistics but **not** actual `counterparty_masked` values?
3. Does it flag `anomaly_confirmed = 2` explicitly — not just report value counts where 2 appears?
4. Does it flag `prior_alerts_90d = 999` and `analyst_confidence = -1` as sentinels — separately from null analysis?

If any of these are wrong — that is the script review step. Fix the prompt. Add the missing element. Regenerate.

`[CHECK-IN]` At 0:52 — has everyone run `profile_treasury.py` and seen terminal output? Check this list:

```
[ ] Row count = 500 printed
[ ] Duplicate payment_id count reported (should be > 0)
[ ] Sentinel 999 in prior_alerts_90d flagged separately from nulls
[ ] Sentinel -1 in analyst_confidence flagged as "not rated"
[ ] anomaly_confirmed = 2 flagged as invalid binary value
[ ] Negative payment_amount values reported
[ ] Mixed date formats in payment_date flagged
[ ] Blank review_status values counted
[ ] counterparty_masked noted as PII-adjacent — no actual values printed
[ ] outputs/A_profile.md saved
```

**NOTE:**
The most common Phase 1 failure: the script prints `counterparty_masked` values in a `.head()` or `value_counts()` call. This is a Constraints failure in the prompt — the RIFCC-DA Constraints element was either missing or incomplete. Use it as a teaching moment: *"Where in the prompt did this slip through? What one line would have prevented it?"*

`outputs/A_profile.md` is the handoff to Phase 2. Every Phase 2 prompt attaches it. If it is missing or empty, Phase 2 output quality drops significantly.

---

## PHASE 2A — DATA CLEANING · 0:55–1:05

**What you are building:** `scripts/clean_treasury.py` + `outputs/treasury_payments_clean.csv` + `outputs/A_reconciliation.txt`

**Why this phase exists:** Every transformation decision needs a business justification — not just code that works but code that documents why it does what it does. This is your audit trail.

**SAY:**
Switch to **Data Cleaning Engineer** in the agent dropdown. Use `/data-cleaning` and attach `#data/treasury_payments.xlsx` and `#outputs/A_profile.md`. The profile is your handoff — Copilot uses it to understand what it needs to fix.

**SHOW:** Select Data Cleaning Engineer → `/data-cleaning` → attach both files.

**SAY:**
The guide walks you through six steps in Phase 2A. I want to call out two of them explicitly because they are where the most errors happen.

**Step 3 — The assertion block.** After cleaning, the script must include assertions that verify the cleaning actually worked. One assertion in particular is commonly written wrong. You might see:

```python
assert df['anomaly_confirmed'].isin([0, 1, float('nan')]).all()
```

This looks correct. It is not. In pandas, `.isin()` never matches `NaN` values — they are excluded from the check silently. The correct form is:

```python
assert (df['anomaly_confirmed'].isin([0, 1]) | df['anomaly_confirmed'].isna()).all()
```

If the script Copilot generates uses the first form — reject it. Show Copilot the correct form and ask it to update. This is a real bug that produces a false pass — your assertions say clean when the data is not.

**Step 4 — The reconciliation report.** This is the denominator anchor for everything downstream. The script must print — and save to `outputs/A_reconciliation.txt` — a report that looks like this:

```
=== RECONCILIATION REPORT ===
Starting rows:                     500
Duplicate payment_id removed:      [n]   → Running total: [n]
Negative payment_amount removed:   [n]   → Running total: [n]
anomaly_confirmed = 2 (excluded):  [n]   → Excluded from analysis (rows kept in df_clean)
prior_alerts_90d = 999 → NaN:      [n]   → Rows kept, value replaced
analyst_confidence = -1 → NaN:     [n]   → Rows kept, value replaced
─────────────────────────────────────────────
Final analysis-valid row count:    [n]
Analysis denominator for all Phase 2B calculations: [n]
=============================
```

The "Final analysis-valid row count" in this report is your denominator. Write it down. Every rate calculation in Phase 2B and every chart label in Phase 3 must use this number. If Phase 3 uses a different denominator than Phase 2A's reconciliation — your dashboard numbers are wrong and not defensible.

`[CHECK-IN]` At 1:03 — before running the script, review these:

```
[ ] anomaly_confirmed = 2 handled with explicit justification comment — not silently dropped
[ ] prior_alerts_90d = 999 replaced with NaN — not averaged
[ ] analyst_confidence = -1 replaced with NaN — not averaged
[ ] Assertion uses (isin([0, 1]) | isna()) — NOT isin([0, 1, float('nan')])
[ ] counterparty_masked never printed or included in CSV output
[ ] Row count printed before AND after each cleaning step
[ ] outputs/treasury_payments_clean.csv created in outputs/ — not in data/
[ ] outputs/A_reconciliation.txt saved and contains Final analysis-valid row count
```

**SAY:**
Do not proceed to Phase 2B until you have `outputs/A_reconciliation.txt` and you know the final analysis-valid row count. That number is the anchor. Everything downstream must match it.

---

## PHASE 2B — EXPLORATORY ANALYSIS · 1:05–1:15

**What you are building:** `outputs/A_eda_findings.md` + `scripts/eda_treasury.py` + `outputs/A_eda_summary.txt`

**Why this phase exists:** You are not generating output — you are building a case. Four analytical questions, in order, each building on the previous. The goal is one finding strong enough to change what the Head of Treasury Operations does tomorrow morning.

**SAY:**
Switch to **Exploratory Data Analyst**. Attach `#outputs/treasury_payments_clean.csv` and `#outputs/A_reconciliation.txt` — the reconciliation file is attached so Copilot validates its denominator against your Phase 2A anchor before it runs any calculation.

You have two options: use `/eda-analysis` for a single structured run, or use the four focused prompts in your guide one at a time. I strongly recommend the four individual prompts your first time through — read each output before moving on. You are more likely to catch errors and more likely to understand what the data is telling you.

**SHOW:** Select Exploratory Data Analyst → attach both files.

**SAY:**
The four analytical questions:

**Prompt 1 — "Where is the anomaly rate highest, and is it concentrated?"**
This calculates anomaly rate by `payment_type` and by `client_segment`, then drills to the cross-tab — each `payment_type × client_segment` combination. The cross-tab reveals your highest-concentration risk cell. Look for the cell marked `***` — but also look at its sample size. A 46% anomaly rate based on 7 transactions is very different from 46% based on 70. Check the `n=` count before drawing conclusions.

After the output — **capture the finding in plain English.** Write it to `outputs/A_eda_findings.md` in the format the guide specifies. Do not move to Prompt 2 until you have recorded Finding 1.

**Prompt 2 — "Is this getting worse or is it noise?"**
This groups confirmed anomalies by ISO week across Q4 and adds a 3-week rolling average. Look at two things: the direction (increasing, decreasing, stable) AND the range (highest week count vs. lowest week count). A declining trend with a range of 13 (week high=13, week low=0) is a very different operational signal than a declining trend with a range of 2.

After the output — write Finding 2. Capture both the direction and the range. One sentence on what operations should do differently based on this pattern.

**Prompt 3 — "Where should we focus resources?"**
This calculates regional confirmed counts AND average payment amounts. You need both because a region with 5 anomalies averaging $10M is a different risk than a region with 37 anomalies averaging $2M. The guide flags any region that is top-2 in BOTH frequency AND dollar value as PRIORITY. That region is where investigation resources go first.

After the output — write Finding 3. Note the verification check: the sum of regional confirmed counts must equal the overall confirmed count from Prompt 1. If they do not match, there is a filtering error in the script.

**Prompt 4 — "Does our risk score actually work?"**
This is model validation — the most analytically important question. It compares mean `risk_score` for confirmed anomalies (anomaly_confirmed = 1) against non-anomalies (anomaly_confirmed = 0) and calculates the separation ratio.

- Ratio **> 1.2**: model shows reasonable signal
- Ratio **1.0–1.2**: model signal is weak — flag for review  
- Ratio **< 1.0**: model is **INVERTED** — confirmed anomalies actually score lower than non-anomalies. This is a critical finding.

If the verdict is INVERTED — write it with a ⚠️ in your findings document. This changes the recommendation completely: the risk model cannot be trusted for prioritising investigations until it is recalibrated.

**NOTE:**
This is the finding most participants miss because they do not expect it. The separation ratio < 1.0 means the model is actively misleading — it rates anomalies as lower risk than legitimate transactions. Operationally, that means investigations based on model scores are starting from the wrong end of the queue.

`[CHECK-IN]` At 1:13 — check the findings document:

```
[ ] outputs/A_eda_findings.md contains all 4 findings with exact numbers
[ ] Finding 1: overall rate as fraction (not just %) + top payment_type + top cross-tab cell with n=
[ ] Finding 2: trend direction stated + weekly range (high and low weeks) + pattern type
[ ] Finding 3: regional table with count AND avg amount + PRIORITY region identified + verification check passes
[ ] Finding 4: separation ratio calculated + model verdict stated (STRONG / WEAK / INVERTED)
[ ] scripts/eda_treasury.py generated and runs standalone
[ ] outputs/A_eda_summary.txt saved by the EDA script
[ ] counterparty_masked absent from all findings
```

---

## PHASE 3 — VISUALIZATION · 1:15–1:27

**What you are building:** `scripts/visualize_treasury.py` + `outputs/A_dashboard.html`

**Why this phase exists:** The dashboard is the stakeholder artifact. It must stand completely alone — no server, no dependencies, no installation required. A non-technical executive should be able to open it in any browser and immediately see the finding.

**SAY:**
Switch to **Visualization Architect**. Use `/data-visualization` and attach `#outputs/treasury_payments_clean.csv` and `#outputs/A_eda_findings.md`. Both files — the cleaned data for the charts, and the findings document so the dashboard summary header matches your EDA conclusions.

**SHOW:** Select Visualization Architect → `/data-visualization` → attach both files.

**SAY:**
Three charts. Let me describe what each one must look like — read these against what Copilot generates before you accept:

**Chart 1 — Confirmed Anomaly Rate by Payment Type (Bar chart)**
- Bars sorted by rate descending
- Each bar labelled with BOTH the rate percentage AND the base-n that produced it — for example: `34.0%  n=36/106`. If a bar only shows the percentage, you cannot assess whether it is based on 5 transactions or 500. Reject it.
- A horizontal dashed reference line at the portfolio-wide average rate
- Y-axis starting at zero

**Chart 2 — Weekly Confirmed Anomaly Count (Line chart)**
- Main line: weekly confirmed anomaly count with data point markers
- Overlay: 3-week rolling average as a dotted line, visually distinct from the main line
- Annotation on the peak week and the trough week — what the counts were, not just where they were
- X-axis: week start dates at 45° angle — not ISO week numbers like "2024-W44" (unreadable to a stakeholder)
- Y-axis starting at zero

**Chart 3 — Regional Confirmed Count vs. Avg Payment Amount (Dual Y-axis grouped bar)**
- Left Y-axis (bars in one colour): confirmed count per region
- Right Y-axis (bars in a different colour): average payment amount per region
- Regions sorted by confirmed count descending
- Both Y-axes starting at zero
- This chart is the visual test of your Finding 3 — does the region that leads on count also lead on average amount, or are they different?

**SAY:**
Critical instruction before running: save the generated script first.

Hover over the code block in chat → click **Insert into New File** → save as `scripts/visualize_treasury.py`. If you run unsaved code from the chat panel, you cannot re-run it, cannot modify it, and cannot commit it. Always save before running.

Then open the dashboard:
```
start outputs\A_dashboard.html        ← Windows
open outputs/A_dashboard.html         ← Mac
```

**SAY:**
When the dashboard opens — before you call it done, verify each chart against your EDA findings:

Does the overall anomaly rate in the summary header match exactly what `outputs/A_eda_summary.txt` says? If Copilot used a different denominator than your reconciliation report, the header number is wrong.

Does the Model Status in the header reflect your actual Finding 4 verdict? If the verdict is INVERTED, the header should say INVERTED with a ⚠️ — not WEAK SIGNAL, not STRONG SIGNAL.

Is `counterparty_masked` visible anywhere — in a bar label, an axis value, a hover tooltip? Right-click any chart element → Inspect → search the HTML source for `counterparty_masked`. If it appears — the column was not dropped on load. Fix: add `df = df.drop(columns=['counterparty_masked'])` immediately after `pd.read_csv`.

`[CHECK-IN]` At 1:25 — verify the dashboard:

```
[ ] Dashboard opens in browser — all 3 charts visible with summary header
[ ] Summary header: row count (500 raw + analysis-valid n), date range, overall anomaly rate as fraction
[ ] Model Status reflects actual Finding 4 verdict (not defaulted to WEAK SIGNAL)
[ ] Chart 1: bars sorted descending, each labelled "XX.X%  n=x/y", portfolio average reference line visible
[ ] Chart 2: rolling average overlay distinct from main line, peak and trough annotated, x-axis shows dates not ISO week codes
[ ] Chart 3: dual Y-axes clearly labelled, two bar colours, regions sorted by confirmed count
[ ] All Y-axes start at 0
[ ] counterparty_masked not visible in any label, axis, or hover tooltip
[ ] anomaly_confirmed = 2 excluded — denominator in header matches A_reconciliation.txt
[ ] Data lineage line present ("Source: outputs/treasury_payments_clean.csv")
```

**NOTE:**
If the script crashes with a RuntimeError about rate mismatch — the EDA summary file and the reconciliation file have different denominators. This means the EDA script was run with different filtering than the cleaning script. Resolution: re-run `eda_treasury.py` after confirming `clean_treasury.py` ran cleanly and `A_reconciliation.txt` has the correct Final analysis-valid row count.

---

## STAGE 4 — FINAL ANALYSIS REPORT · 1:27–1:38 (Optional Extension)

**What you are building:** `outputs/A_analysis_report.md`

**Why this phase exists:** A dashboard is evidence — a report is an argument. Section 5 must tell the Head of Treasury Operations exactly what to do, citing exactly what the data showed.

**SAY:**
Stage 4 is optional — it is a post-lab extension. If you have time, open Copilot Chat, make sure you are on the **Report Writer** agent (use `Ctrl+Shift+I` / `Cmd+Shift+I` to open Chat if it closed), and attach three files: `#outputs/A_eda_findings.md`, `#outputs/A_eda_summary.txt`, and `#outputs/A_dashboard.html`.

Use the custom Stage 4 prompt from your guide. When Copilot generates the report — read Section 3 immediately. Every number in Section 3 must match exactly what your EDA scripts printed in the terminal. If Copilot estimated or rounded differently — reject that section and re-prompt:

*"Section 3 numbers do not match my EDA output. Use these exact figures: [paste your terminal numbers]."*

Section 5 — Recommended Action — must name a specific action, a specific metric, and a data citation. *"Investigate anomalies"* is not acceptable. *"Increase manual review coverage for ACH Batch payments in the Northeast region, which showed a 34.0% confirmed anomaly rate (36/106 transactions) and the highest risk-weighted dollar exposure in Q4 2024"* is acceptable.

```
[ ] outputs/A_analysis_report.md saved
[ ] Section 3 numbers match EDA terminal output — no estimates or rounding differences
[ ] Section 5 names a specific action with a specific metric and a data citation
[ ] Section 6 references specific row exclusion counts from A_reconciliation.txt
[ ] counterparty_masked absent from the entire document
```

---

## BLOCK 8 — GROUP DEBRIEF · 1:38–1:45

**SAY:**
Pens down. Let's close together. Three things from each person — 30 seconds each:

**One — your primary finding.** State it as you would to a VP walking by your desk. No field names. No code. Plain English. One number. One implication.

**Two — one risk you caught.** A data quality issue or Copilot error that would have affected the analysis if you missed it. What was it, and what told you it was wrong?

**Three — one Copilot correction.** Something the generated code or output did that you had to fix. What did you change, and why?

**SAY (after share-out):**
Three things to take back to your own analytical work.

**First — the RIFCC-DA pattern.** Role, Inputs, Format, Constraints, Checks, Data assumptions. Six elements. Every analytical Copilot prompt. This is the difference between a script that runs and a script that is correct.

**Second — question-led EDA.** One question per prompt. Read the output before you generate the next one. Copilot produces better analysis when it is answering a specific question than when it is asked to "do the analysis."

**Third — the review-before-run habit.** Generated code is a draft. Domain expertise is the final check. The scripts in this lab are built to be read — every transformation has an inline comment, every assumption is documented. That is the standard. Apply it to every Copilot-generated script you run in production.

The reference folder in this repo has everything you used today — the RIFCC-DA framework, the responsible use policy, the glossary, the quick reference card. It stays in your VS Code workspace. Use it.

Thank you. Questions?

---

---

## APPENDIX — SCENARIO B & C QUICK REFERENCE

> For facilitators running Sub-Lab B or Sub-Lab C in parallel.
> The phase structure is identical to Sub-Lab A — the differences are below.

---

### Sub-Lab B Differences

**Pre-Step (5 min before Phase 1):**
Read `data/app_service.py` — find `# BUG` annotations AND structural defects with no annotation. Write a one-sentence hypothesis: which service will have the most ERROR/FATAL entries, and is it resource exhaustion or logic failure? Do this before Phase 1. The hypothesis is tested in Phase 2B.

**Phase 1 — Different sentinels to flag:**
- Duplicate `request_id` values (8 present)
- Null `response_time_ms` on FATAL rows — expected (service crashed), NOT a cleaning error
- Null `response_time_ms` on some ERROR rows — unexpected data gap, treat separately
- Null `error_code` on 12 ERROR/FATAL rows

**Phase 2A — Critique first, clean second:**
Before generating `clean_logs.py`, critique `scenarios/sub-lab-B-rca/exercises/flawed_rca_analysis.md`. Five embedded flaws — causation stated as correlation, row count that contradicts the cleaning steps, FATAL nulls filled with 0ms, ERROR nulls treated the same as FATAL nulls (they are not), error code completeness overclaimed. Find them before generating new code.

**Phase 2B — Use `/rca-analysis` not `/eda-analysis`**
The three questions: Which service has the highest ERROR/FATAL rate? Does the service with the highest failure rate also have the highest average ERROR response time (resource exhaustion) or is it a different service (logic failure)? Do error code distributions match the defect signatures from the Pre-Step code review?

**Phase 3 — Chart 3 is a timeline, not an hour-of-day aggregation:**
Chart 3 must show confirmed failures grouped by actual datetime hour (chronological) — not grouped by hour-of-day (0–23). Copilot frequently extracts the integer hour, which loses the chronological ordering. If Chart 3 x-axis shows 0–23, the prompt failed. Fix: use `pd.Grouper(freq='H')`.

---

### Sub-Lab C Differences

**Pre-Step (5 min before Phase 1):**
Read `data/legacy_mainframe.py` — assess migration complexity for each of the 6 functions before looking at usage data. Note which functions have the most technical debt, which have no error handling, which appear to do nothing (dead code). Write a hypothesis: which 2–3 functions are highest migration risk?

**Phase 1 — Key sentinel to flag:**
- `migration_effort_score = 9999` — estimate was never captured. Not a real effort score. Exclude from all averaging.

**Phase 2B — Output is a prioritised list, not a rate table:**
The EDA output for Sub-Lab C is a ranked list of 3–5 modernisation candidates, scored on two dimensions: business impact (usage data) and migration risk (code assessment). Participants should explicitly cross-reference their Pre-Step code assessment against the usage data to confirm or contradict their hypothesis.

**Phase 3 — Three charts:**
Chart 1: Monthly Active Users by feature (bar, sorted descending — shows business impact).
Chart 2: Error rate by feature (bar, sorted descending — shows current production instability).
Chart 3: Scatter or grouped bar showing migration effort score vs. monthly active users — this is the prioritisation chart. High users + low effort = quick wins. High users + high effort = strategic initiatives.

---

*End of Facilitator Script*
*© 2026 InRhythm™ · Internal Use Only · Powered by ARULA.AI*
