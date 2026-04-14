---
mode: 'agent'
description: 'Write a Plotly visualization script for Scenario A/B/C, run it, and produce the matching A_dashboard.html, B_dashboard.html, or C_dashboard.html file with a summary header and 3 policy-compliant charts.'
---

## Role
You are a Data Visualization Architect. Generate 3 labeled, honest interactive charts for the attached cleaned dataset by generating a production Python script using Plotly. Each chart must answer a specific business question from the scenario. All 3 charts are combined into a single self-contained HTML dashboard file.

## Input
- The cleaned dataset file (e.g., `#outputs/treasury_payments_clean.csv`).

## Format
- Determine scenario first, then use this exact mapping:
  - Scenario A (Treasury): `scripts/visualize_treasury.py` -> `outputs/A_dashboard.html`
  - Scenario B (RCA): `scripts/visualize_logs.py` -> `outputs/B_dashboard.html`
  - Scenario C (Modernization): `scripts/visualize_mainframe.py` -> `outputs/C_dashboard.html`
  Write the complete Python script to the mapped script file and run it immediately after writing.
- Build each chart using plotly.express, then combine them into one dashboard file:
  ```python
  chart1_html = fig1.to_html(include_plotlyjs=True,  full_html=False)
  chart2_html = fig2.to_html(include_plotlyjs=False, full_html=False)
  chart3_html = fig3.to_html(include_plotlyjs=False, full_html=False)

  summary = f"""
  <h2>[Scenario] Analysis Dashboard</h2>
  <p><strong>Dataset:</strong> 500 raw &nbsp;|&nbsp; {n_valid} analysis-valid (after excluding invalid flag values) &nbsp;|&nbsp; <strong>Period:</strong> [first_date] to [last_date]</p>
  <p><strong>Overall confirmed anomaly rate:</strong> {n_confirmed}/{n_valid} = {rate_pct:.1f}%</p>
  <p><strong>Key Risk:</strong> [highest cross-tab cell from EDA: type × segment = rate% (n=count)]</p>
  <p><strong>Model Status:</strong> [STRONG SIGNAL / WEAK SIGNAL / INVERTED — from EDA Finding 4]</p>
  <p style='font-size:0.85em;color:#666;'>Source: [cleaned_csv_path] &nbsp;|&nbsp; EDA: [eda_script_path]</p>
  <hr/>
  """

  html = f"<html><head><meta charset='utf-8'></head><body>{summary}{chart1_html}{chart2_html}{chart3_html}</body></html>"
  with open('<scenario-mapped dashboard path>', 'w', encoding='utf-8') as f:
        f.write(html)
  ```
  `include_plotlyjs=True` on the first chart embeds Plotly.js once — fully self-contained, no CDN, no external network call.
- Include a block comment after each chart section explaining what the chart shows, the key pattern, and one sentence about the business implication.

## Constraints
- plotly.express only — no matplotlib, no seaborn, no 3D charts
- PII-adjacent fields (counterparty_masked, user_id_masked) must not appear as a chart label, axis value, hover field, or legend entry — remove them from the dataframe before passing to Plotly
- Sentinel values (9999, 999, -1) must be excluded before plotting — confirm exclusion in the code
- The dashboard is a single self-contained `.html` file — no server required to open it, no external CDN
- Populate the summary header with real computed values — row count from the cleaned dataframe, period/date range from the data, one-sentence key finding from EDA
- A descriptive title stating what the chart shows on every chart
- Labeled x-axis and y-axis with units where applicable
- Y-axis starting at 0 for all bar and line charts (`fig.update_yaxes(rangemode='tozero')`)
- A legend where multiple series or categories are shown
- Do not call `fig.show()` or `fig.write_html()` per individual chart — use `to_html()` and combine into the single dashboard
- For Scenario A: load outputs/A_eda_summary.txt and verify that the overall anomaly rate in the dashboard summary header matches exactly — if they differ, stop and fix before generating charts
- The data lineage line in the summary header must reference both the source CSV and the EDA script
- n_valid (analysis-valid row count) must be read from outputs/[X]_reconciliation.txt — do not recalculate it independently

## Checks
- [ ] Does every chart have a title and fully labeled axes with units?
- [ ] Does the Y-axis start at zero for bar and line charts?
- [ ] Are all PII-adjacent fields absent from chart elements?
- [ ] Is the summary header populated with real values (row count, period, key finding)?
- [ ] Is the single scenario-mapped dashboard file (`outputs/A_dashboard.html`, `outputs/B_dashboard.html`, or `outputs/C_dashboard.html`) present in `outputs/` after running?
- [ ] Does the dashboard open correctly in a browser and show all 3 charts?
- [ ] Is each chart section followed by a block comment with the chart's key pattern and business implication?
- [ ] Does the summary header show both raw row count AND analysis-valid row count?
- [ ] Does the overall anomaly rate in the header match outputs/A_eda_summary.txt exactly (Scenario A)?
- [ ] Is the data lineage line present referencing the source CSV and EDA script?
