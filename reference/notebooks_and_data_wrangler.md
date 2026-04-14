# Notebooks and Data Wrangler

Use Data Wrangler as an exploration aid, not a replacement for governed scripts.

## Recommended pattern
1. Explore shape, nulls, and outliers in notebook/Data Wrangler.
2. Export or translate transformations into `scripts/clean_[scenario].py`.
3. Re-run script from workspace root.
4. Confirm outputs land in required `outputs/` paths.

## Guardrails
- Do not keep final business logic only in notebook cells.
- Keep sentinel handling explicit in scripts.
- Verify that notebook experiments and script results match row counts.
