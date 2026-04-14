# Copilot Commands and Workflow

## Core lab flow
1. Select the stage-specific agent in Copilot Chat.
2. Attach files using `#filename`.
3. Run the matching slash prompt.
4. Save outputs to required paths.

## Slash prompts used in lab
- `/data-profiling`
- `/data-cleaning`
- `/exploratory-analysis`
- `/eda-analysis` (Scenario A)
- `/rca-analysis` (Scenario B)
- `/data-visualization`
- `/data-risk-review` (optional)
- `/responsible-use-audit` (optional)

## File hand-off pattern
- Phase 1 output: `outputs/[X]_profile.md`
- Phase 2 outputs: `outputs/[scenario]_clean.csv`, `outputs/[X]_cleaning_decisions.md`
- Phase 3 output: `outputs/[X]_dashboard.html`
- Stage 4 optional output: `outputs/[X]_analysis_report.md`

## Useful shortcuts
- Open Copilot Chat: `Ctrl+Shift+I` (Windows)
- Open command palette: `Ctrl+Shift+P`
- Use `#` in chat to attach files from workspace
