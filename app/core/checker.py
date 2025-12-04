import httpx 
import time
from typing import Dict 

async def ping_url(url: str) -> Dict:
    """
    ping the given URL and return a result dict with status and latency
    """

    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            response = await client.get(url)
        status = "UP" if response.status_code == 200 else "DOWN"
    except Exception:
        status = "DOWn"

    latency = time.time() - start_time
    return {
        "url": url, 
        "status": status, 
        "latency": round(latency, 3),
        "timestamp": time.time()
    }

