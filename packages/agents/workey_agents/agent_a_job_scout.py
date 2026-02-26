"""Agent A: Job Scout - Discovers job listings from multiple sources."""
from __future__ import annotations
import hashlib
import httpx
from typing import AsyncGenerator
from bs4 import BeautifulSoup
from .schemas import JobListing


def _make_hash(company: str, title: str, url: str) -> str:
    """Create a deduplication hash for a job listing."""
    raw = f"{company.lower()}|{title.lower()}|{url.lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class JobScoutAdapter:
    """Base adapter interface for job source scrapers."""
    
    source_name: str = "unknown"
    
    async def scrape(self, query: str, location: str = "remote") -> list[JobListing]:
        raise NotImplementedError


class RemoteOKAdapter(JobScoutAdapter):
    """Adapter for RemoteOK job board (public JSON API)."""
    
    source_name = "remoteok"
    BASE_URL = "https://remoteok.com/api"
    
    async def scrape(self, query: str, location: str = "remote") -> list[JobListing]:
        """Scrape RemoteOK for AI/ML/engineering jobs."""
        jobs = []
        try:
            async with httpx.AsyncClient(timeout=30, headers={"User-Agent": "WorkeyBot/1.0"}) as client:
                resp = await client.get(self.BASE_URL)
                resp.raise_for_status()
                data = resp.json()
                # First item is metadata, skip it
                listings = [item for item in data if isinstance(item, dict) and "company" in item]
                
                query_terms = query.lower().split()
                for item in listings[:100]:
                    # Filter by query relevance
                    text = f"{item.get('position', '')} {item.get('tags', [])}".lower()
                    if not any(term in text for term in query_terms):
                        continue
                    
                    company = item.get("company", "Unknown")
                    title = item.get("position", "")
                    url = item.get("url", "")
                    if not url:
                        url = f"https://remoteok.com/l/{item.get('id', '')}"
                    
                    tags = item.get("tags", [])
                    if isinstance(tags, str):
                        tags = [t.strip() for t in tags.split(",")]
                    
                    salary_min = item.get("salary_min")
                    salary_max = item.get("salary_max")
                    
                    jd_parts = [item.get("position", ""), item.get("description", "")]
                    jd_text = "\n".join(p for p in jd_parts if p)
                    
                    jobs.append(JobListing(
                        company=company,
                        title=title,
                        location="Remote",
                        remote_type="remote",
                        source=self.source_name,
                        url=url,
                        posted_at=item.get("date"),
                        salary_min=int(salary_min) if salary_min else None,
                        salary_max=int(salary_max) if salary_max else None,
                        salary_currency="USD",
                        jd_text=jd_text,
                        tags=tags,
                        ingest_hash=_make_hash(company, title, url),
                    ))
        except Exception as e:
            print(f"[RemoteOK] Error: {e}")
        return jobs


class WellfoundAdapter(JobScoutAdapter):
    """Adapter for Wellfound (AngelList) - uses public search."""
    
    source_name = "wellfound"
    
    async def scrape(self, query: str, location: str = "remote") -> list[JobListing]:
        """Scrape Wellfound for startup AI/ML roles."""
        # Wellfound requires auth for full API; return empty for now
        # TODO: Implement with Playwright or authenticated session
        print("[Wellfound] Adapter not yet implemented - requires auth session")
        return []


class MockJobAdapter(JobScoutAdapter):
    """Mock adapter for testing - returns sample AI/ML jobs."""
    
    source_name = "mock"
    
    async def scrape(self, query: str, location: str = "remote") -> list[JobListing]:
        """Return sample job listings for development/testing."""
        return [
            JobListing(
                company="Acme AI",
                title="Senior AI Engineer",
                location="Remote",
                remote_type="remote",
                source="mock",
                url="https://example.com/jobs/ai-engineer-1",
                jd_text="""We are looking for a Senior AI Engineer to build production LLM systems.
                Requirements: Python, LangChain/LangGraph, multi-agent systems, FastAPI, PostgreSQL.
                Nice to have: LangGraph, voice AI, LiveKit, ElevenLabs.
                Salary: $150k-$200k. Remote-first, global team.""",
                tags=["python", "langchain", "langgraph", "multi-agent", "fastapi", "llm"],
                salary_min=150000,
                salary_max=200000,
                ingest_hash=_make_hash("Acme AI", "Senior AI Engineer", "https://example.com/jobs/ai-engineer-1"),
            ),
            JobListing(
                company="QuantBot Labs",
                title="Quantitative AI Engineer",
                location="Remote / Singapore",
                remote_type="hybrid",
                source="mock",
                url="https://example.com/jobs/quant-ai-2",
                jd_text="""QuantBot Labs is hiring an AI Engineer with quantitative/trading background.
                Stack: Python, FastAPI, WebSockets, PostgreSQL, AWS.
                Must have: algorithmic trading, signal generation, real-time systems.
                Salary: $120k-$180k. Remote-friendly, SE Asia preferred.""",
                tags=["python", "trading", "quant", "fastapi", "websocket", "aws"],
                salary_min=120000,
                salary_max=180000,
                ingest_hash=_make_hash("QuantBot Labs", "Quantitative AI Engineer", "https://example.com/jobs/quant-ai-2"),
            ),
        ]


class JobScoutAgent:
    """Orchestrates multiple job source adapters."""
    
    def __init__(self, use_mock: bool = False):
        self.adapters: list[JobScoutAdapter] = []
        if use_mock:
            self.adapters.append(MockJobAdapter())
        else:
            self.adapters.append(RemoteOKAdapter())
            self.adapters.append(WellfoundAdapter())
    
    async def discover(
        self,
        query: str = "AI ML engineer agent",
        location: str = "remote",
        limit_per_source: int = 50,
    ) -> list[JobListing]:
        """Discover jobs from all configured sources."""
        all_jobs: list[JobListing] = []
        seen_hashes: set[str] = set()
        
        for adapter in self.adapters:
            print(f"[JobScout] Scraping {adapter.source_name}...")
            jobs = await adapter.scrape(query, location)
            for job in jobs[:limit_per_source]:
                if job.ingest_hash not in seen_hashes:
                    seen_hashes.add(job.ingest_hash)
                    all_jobs.append(job)
        
        print(f"[JobScout] Found {len(all_jobs)} unique listings")
        return all_jobs
