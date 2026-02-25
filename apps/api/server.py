"""Development server entrypoint."""
import asyncio
import sys
import os
from pathlib import Path

# Add api dir to path so imports work
api_dir = Path(__file__).parent
sys.path.insert(0, str(api_dir))

import uvicorn


async def init():
    from database import create_tables
    await create_tables()


if __name__ == "__main__":
    asyncio.run(init())
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("API_PORT", "8000")), reload=True, app_dir=str(api_dir))
