import sys
from pathlib import Path
import pandas as pd

# Dynamically resolve absolute paths
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA_PATH = ROOT / "data" / "canonical" / "intelligence_data.csv"

# Add the hyphenated directory to sys.path
sys.path.append(str(HERE / "track-specific"))

from comparative_analysis import run_comparative_track
from export_intelligence_results import export_results

def main():
    # Load canonical data using absolute path
    df = pd.read_csv(DATA_PATH, dtype={"is_synthetic": str})
    
    # Execute Track A - Comparative
    pivot_records, baseline = run_comparative_track(df)
    
    # Export standard intelligence contract
    export_results(pivot_records, baseline)
    print("Analytical track executed and intelligence results exported successfully.")

if __name__ == "__main__":
    main()