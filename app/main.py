from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="Uptime Monitor", version="0.1.0")

class HealthResponse(BaseModel):
    status: str 
    uptime_seconds: float 
    timestamp: float 

_start_time = time.time()

@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health endpoint. Returns service status and uptime.
    """

    now = time.time()
    return HealthResponse(
        status="ok",
        uptime_seconds = now - _start_time,
        timestamp = now,
    )