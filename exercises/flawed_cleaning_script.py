"""
Flawed Cleaning Script — Exercise File
Hartwell Financial Services — Transaction Risk Alert Dataset

This script LOOKS like a reasonable data cleaning script but contains
exactly 6 labeled errors. Find and fix all 6 before Stage 2 proceeds.

CHALLENGE: After identifying each error, write a comment explaining:
  1. Why the original code is wrong
  2. What business rule or data risk it violates
  3. What the correct approach would be
"""

import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv('../data/transaction_alerts.csv')
print(f"Loaded {len(df)} rows")

# -------------------------------------------------------------------
# ERROR 1: Drops ALL rows with ANY null value across ALL columns
# This destroys a significant portion of the dataset.
# last_login_days_ago alone has 34 nulls; transaction_amount has 15.
# Many of these null-containing rows may still be valid for analysis.
# -------------------------------------------------------------------
df = df.dropna()
print(f"After dropping nulls: {len(df)} rows")


# -------------------------------------------------------------------
# ERROR 2: Silently replaces ALL negative transaction_amount values
# with 0 — no justification, no business rule, no logging, no flag.
# For a fraud dataset, a negative transaction amount could mean a
# reversal or refund — replacing with 0 destroys that signal.
# -------------------------------------------------------------------
df['transaction_amount'] = df['transaction_amount'].apply(
    lambda x: 0 if x is not None and x < 0 else x
)


# -------------------------------------------------------------------
# ERROR 3: Uses drop_duplicates() with NO subset parameter.
# This drops rows that share identical values in ANY column —
# not just duplicate alert_ids. Will incorrectly remove legitimate
# alerts that happen to share the same region, amount, or risk_score.
# -------------------------------------------------------------------
df = df.drop_duplicates()
print(f"After deduplication: {len(df)} rows")


# -------------------------------------------------------------------
# ERROR 4: Compares contract_review_date (a raw string) to a
# date string without first parsing either into datetime objects.
# This string comparison produces incorrect results — '01/15/2024'
# would sort before '2024-01-15' alphabetically, not chronologically.
# -------------------------------------------------------------------
df = df[df['escalation_date'] > '2024-01-01']
print(f"After date filter: {len(df)} rows")


# -------------------------------------------------------------------
# ERROR 5: Calculates the mean analyst_confidence to impute missing
# values WITHOUT first excluding the -1 sentinel values.
# The -1 values are NOT valid ratings — they mean "not rated."
# Including them in the mean pulls it significantly downward and
# produces a wrong imputation value.
# -------------------------------------------------------------------
mean_confidence = df['analyst_confidence'].mean()
df['analyst_confidence'] = df['analyst_confidence'].fillna(mean_confidence)
print(f"Mean analyst_confidence used for imputation: {mean_confidence:.2f}")


# -------------------------------------------------------------------
# ERROR 6: Prints the first 10 rows of the dataframe INCLUDING
# the account_masked column. In a real environment this exposes
# a PII-adjacent field in console logs, which may be captured
# in log files, CI/CD outputs, or shared terminal sessions.
# -------------------------------------------------------------------
print("\nSample cleaned data:")
print(df.head(10))


# Save output
df.to_csv('../data/transaction_alerts_clean.csv', index=False)
print(f"\nCleaned dataset saved: {len(df)} rows")


# -------------------------------------------------------------------
# CHALLENGE: Find and fix all 6 errors above.
# For each fix, write a comment explaining:
#   - Why the original code was wrong
#   - What business rule or data risk it violated
#   - What your corrected approach does instead
# -------------------------------------------------------------------
