# Demo Script (Facilitator Opening)

Use this as your opening script for the first 5–7 minutes of the shared demo. Keep it aligned with `FACILITATOR_GUIDE.md` Sections 1–2.

## 1) Welcome and Session Contract (60–90 sec)

- "Welcome — today we will use GitHub Copilot in VS Code to profile, clean, and visualize data responsibly."
- "This is a 90-minute lab: 30-minute shared demo, 50-minute scenario sprint, 10-minute debrief."
- "You will complete one scenario end-to-end and produce three artifacts in `outputs/`."

## 2) Environment and Safety Check (2 min)

- "Open the repo in VS Code and confirm Copilot Chat is active."
- "Open `VERIFY_BEFORE_SEND.md` now — this checklist applies before every prompt."
- "If you are new to setup, use `QUICK_START.md`."
- "Confirm the enterprise install sequence has been run: `py -m ensurepip --upgrade`, `python -m pip install --upgrade pip`, then `python -m pip install pandas numpy plotly openpyxl --index-url https://artifactory.fmr.com/api/pypi/pypi-releases/simple`."

## 3) Agent + Prompt Discovery (90 sec)

- "Open Copilot Chat and verify agents appear in the Agent Selector."
- "Type `/` in chat to confirm prompt commands are available."
- "We will use scenario-specific file naming contracts for outputs:
  - A: `outputs/A_*.md|html`
  - B: `outputs/B_*.md|html`
  - C: `outputs/C_*.md|html`"

## 4) Prompting Standard (RIFCC-DA) (60–90 sec)

- "Use RIFCC-DA for every major prompt: Role, Inputs, Format, Constraints, Checks."
- "Always attach dataset + schema with `#filename`."
- "Do not accept first output blindly — run scripts, validate numbers, then iterate."

## 5) Transition to Shared Demo Flow (30 sec)

- "Next, I’ll model the first phase live (profiling), then you’ll choose Scenario A, B, or C for your sprint."
- "During your sprint, save all deliverables under `outputs/` with the correct scenario prefix."

> Facilitator note: Ground-truth issue counts, detailed coaching interventions, and timing adjustments remain in `FACILITATOR_GUIDE.md`. This file is the opening talk track only.
