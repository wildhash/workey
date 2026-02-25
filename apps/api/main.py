"""Workey API - Main FastAPI application."""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Support running as script from apps/api dir OR as module from project root
_api_dir = Path(__file__).parent
if str(_api_dir) not in sys.path:
    sys.path.insert(0, str(_api_dir))

from routers import jobs, applications, agents, portfolio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Workey API] Starting up...")
    yield
    print("[Workey API] Shutting down...")


app = FastAPI(
    title="Workey API",
    description="Autonomous job-acquisition operating system API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "workey-api"}
