import asyncio
from app.core.checker import ping_url 
from app.core.db import save_log

# In memory store for demonstration
LOGS = []

# List of URLS to monitor
URLS = ["https://www.google.com", "https://www.github.com", "https://www.npmjs.com"]


async def schedule_checker(url: str, interval: int=60):
    """
    Periodically ping all URL's every "interval" seconds and store results in LOGS
    """
    while True:
        for url in URLS:
            result = await ping_url(url)
            LOGS.append(result)
            await save_log(result) # persist in DB            
            if len(LOGS) > 100: # Keep last 100 logs
                LOGS.pop(0)
        await asyncio.sleep(interval)

    
 
