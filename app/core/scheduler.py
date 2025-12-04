import asyncio
from app.core.checker import ping_url 

# In memory store for demonstration
LOGS = []

async def schedule_checker(url: str, interval: int=60):
    """
    Periodically ping URL every "interval" seconds and store results in LOGS
    """
    while True:
        result = await ping_url(url)
        LOGS.append(result)
        # Keep only last 20 pages 
        if len(LOGS) > 20:
            LOGS.pop(0)
        await asyncio.sleep(interval)

    
 
