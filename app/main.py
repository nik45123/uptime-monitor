from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.scheduler import schedule_checker, LOGS
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import time

app = FastAPI(title="Uptime Monitor", version="0.2.0")

class HealthResponse(BaseModel):
    status: str 
    uptime_seconds: float 
    timestamp: float 

_start_time = time.time()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/status")
async def status():
    return JSONResponse(content=LOGS)


@app.on_event("startup")
async def startup_event():
    # start the background checker
    asyncio.create_task(schedule_checker("https://www.google.com", interval=5))


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
