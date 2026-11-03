# RealRails Shift Productivity Dashboard

An enterprise-grade, high-performance telemetry dashboard designed to visualize operational shift metrics, output trends, and workforce coverage. 

An operational map view of shift output and coverage across facilities, with a contextual intelligence panel. All data shown is synthetic.

## Current Application Behaviour

The page is an interactive operational map: six markers (2 facilities x 3 teams) show output-per-hour and a status colour (Optimal / Warning / Critical). Location, Team and Time Horizon selectors drive an Intelligence side panel with an output trend, an overtime chart and an insight text, and a CSV export of the selected view.

* The frontend reads a hard-coded **synthetic** `mockDatabase` in `frontend/app/page.tsx`; it does not call the backend or any external API.
* "Last 30 Days" and "Year to Date" views are interpolated in the browser from the 5 base data points (display only, not source data).
* The backend (`backend/main.py`) serves a **synthetic**, seeded (42) shift-level dataset at `/api/v1/intelligence/coverage`.
* Frontend data is facility/team-level; backend data is shift-level with no facility. They are different synthetic scopes and must **not** be treated as one comparable operational series in later analytics.

## Phase 3 Canonical Data Package

All data is synthetic (no personal or restricted data). The single source of truth is `data/canonical/intelligence_data.csv` (129 records, 20 columns, version 1.0.0), generated from a 51-record source sample (full population retained, no sampling needed). See `data/README.md` and `docs/`. Regenerate and validate with `python scripts/data_pipeline/run_pipeline.py`.

## 🛠️ Tech Stack

* **Framework:** React / Next.js (App Router)
* **Styling:** Tailwind CSS
* **Charts:** Recharts
* **Backend:** FastAPI (synthetic data generator)
* **Data pipeline:** Python (pandas, numpy)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ifwshone/POC-41-Shift-Productivity-Coverage-Intelligence-shone-Phase2.git
   cd POC-41-Shift-Productivity-Coverage-Intelligence-shone-Phase2/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open the application:**
   Navigate to [http://localhost:3000](http://localhost:3000) in your browser.

## 🏗️ Architecture

* `frontend/app/page.tsx`: the page, its state logic, the synthetic `mockDatabase` and the intelligence panel.
* `backend/main.py`: synthetic shift-level API (not consumed by the UI yet).
* `data/` and `scripts/data_pipeline/`: Phase 3 canonical data package and its reproducible pipeline (not read by the app at runtime).

## 🧪 Testing (UAT)

A rigorous User Acceptance Testing (UAT) protocol is established for this project. See `UAT_CHECKLIST.md` (note: written for an earlier layout; re-verify against the current map UI):
* Interactive handshake events between the 70% stage and 30% sidebar.
* Temporal, risk, and ownership filter logic.
* Dynamic intelligence rendering based on active data nodes.

---
*Built for the RealRails Telemetry Initiative.*