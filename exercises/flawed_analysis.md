# Q4 2024 Fraud Alert Analysis — Findings Summary

**Analyst:** J. Mercer, Risk Analytics Team
**Dataset:** Hartwell Financial Services — Transaction Risk Alerts
**Scope:** Q4 2024 alert queue, all regions

---

## Executive Overview

This report summarizes the key findings from the Q4 2024 analysis of the Transaction Risk Alert dataset. The analysis was conducted using the cleaned dataset (500 records) and covers fraud confirmation rates, regional performance, risk signal effectiveness, and analyst confidence patterns.

---

## Finding 1: Regional Fraud Confirmation Rates

Fraud confirmation rates vary considerably by region. The Northeast (24.8%), Midwest (22.1%), and Southeast (20.3%) showed rates broadly consistent with historical baselines. International alerts had the lowest rate at 18.9%, consistent with lower alert volume.

<!-- FLAW 1: Impossible statistic — a rate cannot exceed 100%. This is a data or calculation error that should have been caught before publication. -->

The Western region was a clear outlier in this period, with a confirmed fraud rate of **112%** — significantly above all other regions and above the theoretical maximum for a binary confirmation rate.

---

## Finding 2: Risk Score as a Predictor of Fraud

The analysis examined the relationship between `risk_score` and `fraud_confirmed` across all alert types. Higher risk scores were consistently associated with higher fraud confirmation rates, with alerts scoring above 0.80 confirming at a rate more than three times that of alerts scoring below 0.40.

<!-- FLAW 2: Causal claim without evidence — correlation from observational data does not establish causation. The correct framing is "correlates with" or "is associated with," not "causes." -->

These results confirm that **high risk scores directly cause fraud confirmation**, and the alert engine's scoring model should therefore be treated as a reliable causal predictor when prioritizing analyst workloads.

---

## Finding 3: Dataset Completeness After Cleaning

Prior to analysis, the dataset was cleaned to remove rows containing invalid values, sentinel codes, and null entries. Standard cleaning protocols were applied across all 15 columns.

<!-- FLAW 3: Logical contradiction — if rows were removed during cleaning, the dataset cannot still contain 500 records. The statement below is arithmetically impossible given the cleaning described. -->

After removing missing values and invalid entries, **the dataset remains complete with all 500 alert records intact**. No data was lost during the cleaning process.

---

## Finding 4: Analyst Confidence Distribution

Analyst confidence ratings provide insight into the quality of fraud determinations made during Q4. High-confidence ratings (9–10) accounted for 31.2% of all rated alerts, while moderate-confidence ratings (5–8) represented 47.4%.

<!-- FLAW 4: The -1 sentinel values (19 rows coded as "not rated") were not excluded before calculating the mean. Including -1 in the mean calculation pulls the average down significantly, producing a misleading figure. -->

NPS scores were analyzed across all 500 alerts included in the dataset. The average analyst confidence score across the full alert queue was **7.2 out of 10**, indicating strong overall analyst conviction in their fraud determinations.

---

## Finding 5: Product Usage Score Outlier Analysis

All risk signals were examined for out-of-range values before analysis began. Null values were documented and handled per the cleaning protocol.

<!-- FLAW 5: False claim — 11 rows in the dataset have risk_score values above 1.0, which is outside the valid 0.0–1.0 range defined in the schema. These represent data entry errors that should have been detected and addressed in Stage 1. -->

The `risk_score` distribution was examined and found to be within expected bounds. **No outliers were detected in the risk_score column**, and all values fell within the documented valid range of 0.0 to 1.0.

---

## Methodology

Analysis was conducted using Python 3.11, pandas 2.1, and matplotlib 3.8. All figures reference the cleaned dataset. Statistical summaries were generated using pandas `describe()` and `value_counts()` functions.

---

> **Exercise:** Identify all 5 analytical flaws embedded in this document.
>
> For each flaw, state:
> 1. What the claim is
> 2. Why it is wrong (logical, statistical, or factual error)
> 3. What the correct approach or correct statement would be
>
> Use `data/schema.md` as your reference for valid data ranges and business rules.
