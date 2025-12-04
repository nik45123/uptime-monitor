# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.core.db import get_logs, init_db
from app.core.scheduler import schedule_checker
import asyncio
import time

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(title="Uptime Monitor", version="0.2.0")

# -------------------------------
# Health response model
# -------------------------------
class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    timestamp: float

_start_time = time.time()

# -------------------------------
# CORS middleware (for frontend dev)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Health endpoint
# -------------------------------
@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health endpoint. Returns service status and uptime.
    """
    now = time.time()
    return HealthResponse(
        status="ok",
        uptime_seconds=now - _start_time,
        timestamp=now
    )

# -------------------------------
# Status logs endpoint
# -------------------------------
@app.get("/status")
async def status():
    """
    Returns last 50 logs from SQLite.
    """
    return get_logs(50)

# -------------------------------
# Startup event: initialize DB and start scheduler
# -------------------------------
@app.on_event("startup")
async def startup_event():
    # Initialize database
    init_db()
    # Start scheduler in background (multi-URL scheduler from scheduler.py)
    asyncio.create_task(schedule_checker())

# -------------------------------
# Mount frontend (after API routes!)
# -------------------------------
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
