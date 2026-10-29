from fastapi import FastAPI, File, HTTPException, UploadFile
import pandas as pd
from ml_engine import cluster_data, forecast_data

app = FastAPI(title="AeroScope ML API", version="1.0.0")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AeroScope ML"}

@app.post("/api/cluster")
async def cluster(file: UploadFile = File(...), clusters: int = 3):
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")
    try:
        df = pd.read_csv(file.file)
        return cluster_data(df, clusters)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not analyze CSV: {exc}") from exc

@app.post("/api/forecast")
async def forecast(file: UploadFile = File(...), target: str = "PM2.5", periods: int = 7):
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")
    try:
        df = pd.read_csv(file.file)
        return forecast_data(df, target, periods)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not forecast CSV: {exc}") from exc