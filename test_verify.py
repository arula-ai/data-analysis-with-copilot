#!/usr/bin/env python3
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "scripts/verify_lab_contracts.py", "."],
    cwd=r"c:\Users\Asus\Inrhythm\data-analysis-with-copilot",
    capture_output=True,
    text=True
)

print("===== STDOUT =====")
print(result.stdout)
print("\n===== STDERR =====")
print(result.stderr)
print(f"\n===== EXIT CODE: {result.returncode} =====")
print(f"Verification PASSED: {result.returncode == 0}")
