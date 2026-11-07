"""Apply the Post #6 / presentation patch to the repo root:  python patch/apply_patch.py
Idempotent string edits for existing files; new/rewritten files are copied from patch/."""
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = Path(__file__).resolve().parent


def sub(rel, pairs):
    f = ROOT / rel
    t = f.read_text("utf-8")
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new)
        elif new not in t:
            sys.exit(f"pattern not found in {rel}: {old[:60]!r}")
    f.write_text(t, "utf-8")
    print("edited", rel)


# 1. copy rewritten files
for rel in ["assistant/core/output_validator.py", "frontend/app/intelligence/page.tsx"]:
    shutil.copy(P / rel, ROOT / rel); print("replaced", rel)

# 2. B2: backend image must build from repo root (Dockerfile already copies the whole context)
sub("docker-compose.yml", [("context: ./backend\n      dockerfile: Dockerfile", "context: .\n      dockerfile: backend/Dockerfile")])

# 3. assistant entity bug: explicit entity must not be overridden by text scan
sub("backend/api/assistant.py", [
    ('entity = intent_params.get("entity_id", "facility_a_night_watch")\n                if not entity or "facility_b" in question.lower():\n                    entity = "facility_b_night_watch"',
     'entity = intent_params.get("entity_id") or "facility_a_night_watch"')])

# 4. AssistantPanel: auto-ask the selected-finding question
sub("frontend/components/data-assistant/AssistantPanel.tsx", [
    ("interface AssistantPanelProps {\n  onClose: () => void;\n}", "interface AssistantPanelProps {\n  onClose: () => void;\n  initialQuestion?: string;\n}"),
    ("export function AssistantPanel({ onClose }: AssistantPanelProps) {", "export function AssistantPanel({ onClose, initialQuestion }: AssistantPanelProps) {"),
    ("  const showInitialPrompt =", "  useEffect(() => {\n    if (initialQuestion) handleAsk(initialQuestion);\n    // eslint-disable-next-line react-hooks/exhaustive-deps\n  }, [initialQuestion]);\n\n  const showInitialPrompt ="),
])

# 5. Operations page wording + KPI strip (map untouched)
sub("frontend/app/page.tsx", [
    ("Real-Time Operational Intelligence", "Synthetic Operations Demonstration"),
    (">Live Exceptions<", ">Demonstration Insight<"),
    ("CRITICAL ALERT:", "OBSERVED CRITICAL:"),
    ("SYSTEM WARNING:", "OBSERVED WARNING:"),
    ("{ value: 'Last 30 Days', label: 'Last 30 Days' }", "{ value: 'Last 30 Days', label: 'Last 30 Days (simulated)' }"),
    ("{ value: 'YTD', label: 'Year to Date' }", "{ value: 'YTD', label: 'Year to Date (simulated)' }"),
    ('<div className="pointer-events-auto flex w-fit items-center gap-4 rounded-full',
     '<div className="pointer-events-auto grid max-w-2xl grid-cols-2 gap-2 sm:grid-cols-4">\n            {[["Facilities","2"],["Shift groups","6"],["Baseline","119.4 u/hr"],["Priority review","A / Night −25.8"]].map(([l,v]) => (\n              <div key={l} className="rounded-lg border border-line bg-surface px-3 py-2"><div className="eyebrow !text-[9px]">{l}</div><div className="font-display text-sm font-bold text-mist">{v}</div></div>\n            ))}\n          </div>\n          <div className="pointer-events-auto flex w-fit items-center gap-4 rounded-full'),
])

# 6. publish canonical observations next to intelligence JSON
sub("scripts/copy_intelligence.py", [
    ("if __name__", "def copy_canonical():\n    root = Path(__file__).resolve().parents[1]\n    dest = root / 'frontend' / 'public' / 'data' / 'intelligence'\n    dest.mkdir(parents=True, exist_ok=True)\n    shutil.copy(root / 'data' / 'published' / 'intelligence_data.json', dest / 'canonical_observations.json')\n    print('Copied canonical observations.')\n\n\nif __name__"),
    ("    main()", "    main()\n    copy_canonical()"),
])
print("done. Now: python scripts/copy_intelligence.py && cd frontend && npm run build")
