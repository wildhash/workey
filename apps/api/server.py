"""Development server entrypoint."""
import asyncio
import os

import uvicorn

from workey_api.database import create_tables


async def init():
    await create_tables()


if __name__ == "__main__":
    asyncio.run(init())
    uvicorn.run(
        "workey_api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
        reload=True,
    )
