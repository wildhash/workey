#!/usr/bin/env python3
"""Seed script - populates the database with sample data for development."""

from __future__ import annotations

import argparse
import asyncio
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the Workey database with sample data")
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL"),
        help="Database URL. Defaults to $DATABASE_URL if set, otherwise SQLite at repo root.",
    )
    return parser.parse_args()


async def seed():
    """Seed sample jobs and initial data."""
    from workey_api.database import create_tables, AsyncSessionLocal
    from workey_api.models import Job
    
    print("[Seed] Creating tables...")
    await create_tables()
    
    sample_jobs = [
        {
            "id": str(uuid.uuid4()),
            "company": "Acme AI Labs",
            "title": "Senior AI Engineer",
            "location": "Remote",
            "remote_type": "remote",
            "source": "seed",
            "url": "https://example.com/jobs/ai-engineer",
            "salary_min": 150000,
            "salary_max": 200000,
            "salary_currency": "USD",
            "jd_text": "We need a Senior AI Engineer to build production LLM systems with LangGraph and multi-agent architectures. Required: Python, LangChain/LangGraph, FastAPI, PostgreSQL. Nice to have: Voice AI, LiveKit.",
            "tags": ["python", "langchain", "langgraph", "fastapi", "multi-agent"],
            "ingest_hash": "seed_001",
            "status": "new",
            "score": None,
        },
        {
            "id": str(uuid.uuid4()),
            "company": "QuantBot Labs",
            "title": "Quantitative AI Engineer",
            "location": "Remote / Singapore",
            "remote_type": "hybrid",
            "source": "seed",
            "url": "https://example.com/jobs/quant-ai",
            "salary_min": 120000,
            "salary_max": 180000,
            "salary_currency": "USD",
            "jd_text": "Building AI-powered quant trading systems. Stack: Python, FastAPI, WebSockets. Must have: algorithmic trading experience, signal generation, real-time systems.",
            "tags": ["python", "trading", "quant", "fastapi", "websocket"],
            "ingest_hash": "seed_002",
            "status": "scored",
            "score": 87,
        },
        {
            "id": str(uuid.uuid4()),
            "company": "VoiceFirst AI",
            "title": "Voice AI Engineer",
            "location": "Remote",
            "remote_type": "remote",
            "source": "seed",
            "url": "https://example.com/jobs/voice-ai",
            "salary_min": 130000,
            "salary_max": 170000,
            "salary_currency": "USD",
            "jd_text": "Join our team building real-time voice AI products with LiveKit and ElevenLabs. Python, WebRTC, streaming LLMs. SE Asia timezone preferred.",
            "tags": ["python", "livekit", "elevenlabs", "voice", "webrtc"],
            "ingest_hash": "seed_003",
            "status": "tailored",
            "score": 92,
        },
    ]
    
    async with AsyncSessionLocal() as session:
        for job_data in sample_jobs:
            job = Job(**job_data)
            session.add(job)
        await session.commit()
        print(f"[Seed] Added {len(sample_jobs)} sample jobs")
    
    print("[Seed] Complete! Start the API with: cd apps/api && python server.py")


if __name__ == "__main__":
    args = _parse_args()

    database_url = args.database_url
    if not database_url:
        db_path = REPO_ROOT / "workey.db"
        print(f"[Seed] No DATABASE_URL provided; using SQLite at {db_path}")
        database_url = f"sqlite+aiosqlite:///{db_path}"

    os.environ["DATABASE_URL"] = database_url

    try:
        asyncio.run(seed())
    except ImportError as e:
        missing_name = getattr(e, "name", None) or ""
        if missing_name.split(".")[0] == "workey_api":
            raise SystemExit(
                "workey-api is not installed. Run: python -m pip install -e apps/api"
            ) from e
        raise
