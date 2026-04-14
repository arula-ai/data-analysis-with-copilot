# Notebooks and Jupyter in This Lab

This lab is script-first for reproducibility. Use notebooks only when they improve iteration speed.

## Use scripts when
- You need deterministic reruns
- You are producing required lab artifacts
- You are handing work to another analyst

## Use notebooks when
- You are exploring hypotheses quickly
- You want inline visual checks before script finalization

## Minimal setup
```bash
py -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install pandas numpy plotly openpyxl --index-url https://artifactory.fmr.com/api/pypi/pypi-releases/simple
```
Then in VS Code, open a `.ipynb` and select your Python interpreter.

## Rule
If you prototype in a notebook, port final logic to `scripts/*.py` and keep required outputs in `outputs/`.
