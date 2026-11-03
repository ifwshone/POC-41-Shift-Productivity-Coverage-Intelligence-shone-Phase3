"""Shared constants for the Phase 3 canonical data pipeline (POC-41)."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SOURCE_SAMPLE = DATA / "source-sample" / "source_sample.csv"
CANONICAL = DATA / "canonical" / "intelligence_data.csv"
PUBLISHED = DATA / "published" / "intelligence_data.json"
MANIFEST = DATA / "manifest.json"
SCHEMA = DATA / "schema.json"
PROFILE = DATA / "quality" / "data_profile.json"
VALIDATION = DATA / "quality" / "validation_report.json"
SAMPLING_REPORT = DATA / "quality" / "sampling_report.md"
STATS = DATA / "quality" / "pipeline_stats.json"

PAGE_TSX = ROOT / "frontend" / "app" / "page.tsx"
BACKEND_MAIN = ROOT / "backend" / "main.py"
BACKEND_MOCK = ROOT / "backend" / "mock_data.json"

PROJECT_ID = "POC-41"
PROJECT_TITLE = "Shift Productivity & Coverage Intelligence"
DATA_VERSION = "1.0.0"
RANDOM_SEED = 42
MAX_ROWS, MAX_COLS = 10_000, 50
MAX_DATA_MB, MAX_FILE_MB, MAX_TEXT = 10, 5, 500

SRC_FE = "Frontend mockDatabase (page.tsx)"
SRC_BE = "Backend synthetic shift generator (main.py, seed 42)"

SOURCE_COLUMNS = [
    "source_system", "source_row_id", "record_date", "facility", "team", "shift",
    "output_per_hour", "overtime_hours", "attendance_rate",
    "node_kpi_output_per_hour", "node_status", "node_issue_text", "coverage_status",
]

MANDATORY_COLUMNS = [
    "record_id", "record_type", "observed_at", "entity_id", "related_entity_id",
    "entity_name", "category", "subcategory", "status", "stage", "metric_name",
    "metric_value", "metric_unit", "text_value", "latitude", "longitude",
    "source_name", "source_record_id", "is_synthetic", "data_version",
]
RECORD_TYPES = ["entity", "event", "transaction", "measurement", "process",
                "scenario", "node", "edge", "document"]


def load_stats():
    return json.loads(STATS.read_text("utf-8")) if STATS.exists() else {}


def save_stats(update):
    s = load_stats()
    s.update(update)
    STATS.parent.mkdir(parents=True, exist_ok=True)
    STATS.write_text(json.dumps(s, indent=2, sort_keys=True) + "\n", "utf-8")


def mb(path):
    return round(Path(path).stat().st_size / 1024 / 1024, 6)
