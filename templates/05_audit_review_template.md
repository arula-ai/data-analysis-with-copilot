# Responsible Use Audit Review
**Stage:** 5 | **Agent Mode:** Responsible Use Auditor | **Time Budget:** 10 min
**Save to:** `outputs/05_audit_review.md`

---

## Purpose
This document is the formal compliance review of all generated code and analytical outputs produced during this lab. It is required before this lab is considered complete. Every finding must be rated with a specific severity, and every file must be explicitly reviewed — not assumed clean.

---

## Files Reviewed

> Check off each file as you review it. Do not check a file you only skimmed.

- [ ] `scripts/clean_alerts.py`
- [ ] `notebooks/starter_analysis.ipynb` (or your working notebook)
- [ ] `outputs/01_data_profile.md`
- [ ] `outputs/02_cleaning_decisions.md`
- [ ] `outputs/03_exploratory_insights.md`
- [ ] `outputs/04_visualizations.ipynb`

*Other files reviewed (add here):*

---

## Risk Findings

> Document every finding. If a category has no findings, state "No findings in this category" with a brief note showing evidence of review.

**Severity Scale:** Low (informational) | Medium (should fix) | High (must fix before use) | Critical (stop — do not use)

| Finding # | File | Line / Location | Description | Severity | Recommendation |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| *(add rows as needed)* | | | | | |

**No findings in External Calls category:** *(evidence of review — e.g., "Searched clean_alerts.py for urllib, requests, http — none found")*

**No findings in Sensitive Data Exposure category:** *(evidence — e.g., "Searched all output files for 'account_masked' — not present in any chart label or print output")*

---

## Policy Compliance Assessment

> Answer each question with Yes / No and provide the supporting evidence.

| Question | Answer | Evidence |
|---|---|---|
| Does any generated code make external network calls? | | |
| Does any output file or chart contain `account_masked` values? | | |
| Are all transformations in `clean_alerts.py` accompanied by written justifications? | | |

---

## Required Corrective Actions

> List actions that must be completed before this lab is final. If none, state explicitly.

1. *[Corrective action or "None identified"]*

**Completion target:** *(date or "before lab close")*

---

## Auditor Sign-off

| Field | Value |
|---|---|
| Reviewer Name | |
| Review Date | |
| Files Reviewed | *(count)* |
| Findings Identified | *(count)* |
| Overall Assessment | *Pass / Pass with conditions / Fail* |
| Conditions (if applicable) | |
