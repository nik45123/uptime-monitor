# app/core/scheduler.py
import asyncio
import time
from app.core.db import save_log
import httpx

# -------------------------------
# List of URLs to monitor
# -------------------------------
URLS = [
    "https://google.com",
    "https://github.com"
    # Add more URLs here
]

# -------------------------------
# Check a single URL
# -------------------------------
async def check_url(url: str) -> dict:
    """
    Check the status and latency of a URL.
    Returns a dict with url, status, latency, and timestamp.
    """
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url)
        status = "UP" if r.status_code == 200 else "DOWN"
    except Exception:
        status = "DOWN"
    latency = round(time.time() - start, 2)
    return {
        "url": url,
        "status": status,
        "latency": latency,
        "timestamp": time.time()
    }

# -------------------------------
# Scheduler to periodically check all URLs
# -------------------------------
async def schedule_checker():
    """
    Continuously checks all URLs every 10 seconds
    and saves results to the database.
    """
    while True:
        for url in URLS:
            result = await check_url(url)
            # Save log to SQLite in a thread to avoid blocking event loop
            await asyncio.to_thread(save_log, result)
        await asyncio.sleep(10)  # interval between checks
