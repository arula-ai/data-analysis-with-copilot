"""
Flawed Visualization Script — Exercise File
Hartwell Financial Services — Transaction Risk Alert Dataset

This script generates charts for the transaction_alerts.csv dataset
but contains exactly 4 visualization errors. Find and fix all 4.

CHALLENGE: After identifying each error, write a comment explaining:
  1. Why the original chart code is wrong
  2. What visualization principle it violates
  3. What your corrected version does instead
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

df = pd.read_csv('../data/transaction_alerts.csv')

# Clean minimally for visualization purposes
df_clean = df[df['fraud_confirmed'].isin([0, 1])].copy()
df_clean = df_clean[df_clean['risk_score'] <= 1.0].copy()


# -------------------------------------------------------------------
# VIZ ERROR 1: Y-axis is set to start at 0.6 instead of 0.
# This exaggerates the visual difference between alert types.
# A bar that is 10% taller looks 5x taller when the baseline is 0.6.
# This is a data visualization integrity violation.
# -------------------------------------------------------------------
fraud_by_type = df_clean.groupby('alert_type')['fraud_confirmed'].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(fraud_by_type.index, fraud_by_type.values, color='steelblue')
ax.set_ylim(0.6, 1.0)   # VIZ ERROR 1: Y-axis starts at 0.6, not 0
ax.set_title("Fraud Confirmation Rate by Alert Type")
ax.set_xlabel("Alert Type")
ax.set_ylabel("Fraud Rate")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('../outputs/viz_error1_truncated_yaxis.png')
plt.close()


# -------------------------------------------------------------------
# VIZ ERROR 2: Uses account_masked as bar chart labels.
# account_masked is a PII-adjacent field that must never appear in
# any visualization, export, or shared output. Displaying it in a
# chart — even if masked — creates a compliance risk if the chart
# is shared externally or captured in a report.
# -------------------------------------------------------------------
top_accounts = df_clean.groupby('account_masked')['transaction_amount'].sum().nlargest(10)

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(top_accounts.index, top_accounts.values, color='salmon')
ax.set_title("Top 10 Accounts by Total Transaction Amount")
ax.set_xlabel("Account")   # VIZ ERROR 2: account_masked shown on axis
ax.set_ylabel("Total Transaction Amount ($)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('../outputs/viz_error2_pii_in_labels.png')
plt.close()


# -------------------------------------------------------------------
# VIZ ERROR 3: Chart has no title, no x-axis label, and no y-axis
# label. Without these, the chart is uninterpretable to any reader
# who was not present when it was created. A chart without a title
# and axis labels is not a complete analytical artifact.
# -------------------------------------------------------------------
risk_by_segment = df_clean.groupby('client_segment')['risk_score'].mean()

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(risk_by_segment.index, risk_by_segment.values, color='mediumpurple')
# VIZ ERROR 3: No title, no axis labels
plt.tight_layout()
plt.savefig('../outputs/viz_error3_no_labels.png')
plt.close()


# -------------------------------------------------------------------
# VIZ ERROR 4: Uses a 3D pie chart.
# 3D pie charts distort proportions — slices at the front appear
# larger than slices at the back even if they represent equal values.
# This makes accurate comparison impossible and can mislead readers
# about the relative sizes of categories.
# -------------------------------------------------------------------
segment_counts = df_clean['client_segment'].value_counts()
explode = [0.05] * len(segment_counts)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')   # VIZ ERROR 4: 3D projection

# Simulate 3D pie effect using bar3d
xpos = np.arange(len(segment_counts))
ax.bar3d(xpos, np.zeros(len(segment_counts)), np.zeros(len(segment_counts)),
         0.8, 0.8, segment_counts.values, shade=True)
ax.set_xticks(xpos + 0.4)
ax.set_xticklabels(segment_counts.index, rotation=30)
ax.set_title("Alert Distribution by Client Segment (3D)")
plt.tight_layout()
plt.savefig('../outputs/viz_error4_3d_chart.png')
plt.close()

print("Charts generated (with errors). Review each one.")


# -------------------------------------------------------------------
# CHALLENGE: Fix all 4 visualization errors above.
# For each fix, write a comment explaining:
#   - Why the original approach was wrong
#   - What visualization principle it violated
#   - What your corrected version does to address it
# -------------------------------------------------------------------
