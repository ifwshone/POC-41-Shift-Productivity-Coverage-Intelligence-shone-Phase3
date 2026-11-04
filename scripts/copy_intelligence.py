# /scripts/copy_intelligence.py
import shutil
from pathlib import Path

def main():
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "data-science" / "outputs"
    dest_dir = root / "frontend" / "public" / "data" / "intelligence"
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    for filename in ["intelligence_results.json", "intelligence_summary.json", "validation_metrics.json"]:
        src_file = src_dir / filename
        if src_file.exists():
            shutil.copy(src_file, dest_dir / filename)
            print(f"Copied {filename} to public directory.")
        else:
            print(f"Warning: {filename} not found in outputs.")

if __name__ == "__main__":
    main()
    