import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from backend.api.assistant import router as assistant_router

import sys

# Dynamically add parent directory and current directory to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
for path in [CURRENT_DIR, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Fallback-safe import
try:
    from backend.api.assistant import router as assistant_router
except ModuleNotFoundError:
    from api.assistant import router as assistant_router
# Security Guardrail: Never hardcode credentials
load_dotenv()

app = FastAPI(title="Shift Productivity & Coverage Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the Grounded Data Assistant Router
app.include_router(assistant_router, prefix="/api/assistant", tags=["assistant"])

def generate_synthetic_shift_data():
    # Fallback to mock data if synthetic generation fails
    try:
        np.random.seed(42)
        dates = pd.date_range(start="2026-10-24", periods=7, freq="D")
        shifts = ["Morning", "Evening", "Night"]
        
        data = []
        for d in dates:
            for s in shifts:
                data.append({
                    "date": d.strftime("%Y-%m-%d"),
                    "shift": s,
                    "attendance_rate": round(np.random.uniform(0.85, 0.99), 2),
                    "output_per_hour": round(np.random.uniform(110, 150), 1),
                    "overtime_hours": round(np.random.uniform(5, 40), 1),
                    "coverage_status": np.random.choice(["Optimal", "Strained", "Critical"], p=[0.7, 0.2, 0.1])
                })
        return pd.DataFrame(data).to_dict(orient="records")
    except Exception as e:
        with open("mock_data.json", "r") as f:
            return json.load(f)

@app.get("/api/v1/intelligence/coverage")
async def get_coverage_intelligence():
    data = generate_synthetic_shift_data()
    # Transform raw data into insights
    df = pd.DataFrame(data)
    avg_output = df["output_per_hour"].mean()
    
    insights = {
        "status": "success",
        "kpi": {
            "title": "Avg Output / Hour",
            "value": f"{avg_output:.1f} Units",
            "context": f"{((avg_output - 120) / 120 * 100):.1f}% above regional baseline"
        },
        "dataset": data
    }
    return insights