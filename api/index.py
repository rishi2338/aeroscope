from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

from python_ml_engine import cluster_data, forecast_data

app = FastAPI(title="AeroScope API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_csv_upload(file: UploadFile) -> pd.DataFrame:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")
    try:
        return pd.read_csv(io.BytesIO(file.file.read()))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}") from exc


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AeroScope ML"}


@app.post("/api/cluster")
def cluster(file: UploadFile = File(...), clusters: int = Query(default=3, ge=2, le=10)):
    try:
        return cluster_data(read_csv_upload(file), clusters)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not analyze CSV: {exc}") from exc


@app.post("/api/forecast")
def forecast(
    file: UploadFile = File(...),
    target: str = Query(default="PM2.5"),
    periods: int = Query(default=7, ge=1, le=90),
):
    try:
        return forecast_data(read_csv_upload(file), target, periods)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not forecast CSV: {exc}") from exc
