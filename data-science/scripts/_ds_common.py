"""Shared helpers for Post #2. Reads ONLY data/canonical/intelligence_data.csv (and manifest/schema/source sample for checks)."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "canonical" / "intelligence_data.csv"
MANIFEST = ROOT / "data" / "manifest.json"
SCHEMA = ROOT / "data" / "schema.json"
SOURCE_SAMPLE = ROOT / "data" / "source-sample" / "source_sample.csv"
OUT = ROOT / "data-science" / "outputs"


def load():
    return pd.read_csv(CANONICAL, dtype={"is_synthetic": str})


def dump(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=2, sort_keys=False, default=str) + "\n", "utf-8")
    print(f"wrote data-science/outputs/{name}")


def read_out(name):
    return json.loads((OUT / name).read_text("utf-8"))
