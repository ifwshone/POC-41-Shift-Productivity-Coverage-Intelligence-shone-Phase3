"""Run the full pipeline: extract -> sample -> standardize -> publish -> profile -> validate."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for step in ["extract_data", "sample_data", "standardize_data", "publish_data", "profile_data", "validate_data"]:
    print(f"== {step}")
    subprocess.run([sys.executable, str(HERE / f"{step}.py")], check=True)
