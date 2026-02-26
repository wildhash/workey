"""Workey Worker - Background task runner for job scraping and monitoring."""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add packages/agents to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "agents"))

API_URL = os.getenv("INTERNAL_API_URL", "http://localhost:8000")


async def run_scout(query: str = "AI ML engineer agent", use_mock: bool = False):
    """Run the job scout pipeline."""
    import httpx
    
    print(f"[Worker] Starting job scout: '{query}'")
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            resp = await client.post(
                f"{API_URL}/api/agents/scout",
                json={"query": query, "location": "remote", "use_mock": use_mock},
            )
            resp.raise_for_status()
            print(f"[Worker] Scout triggered: {resp.json()}")
        except Exception as e:
            print(f"[Worker] Scout error (API may not be running): {e}")
            # Run locally if API is not available
            await run_scout_local(query, use_mock)


async def run_scout_local(query: str = "AI ML engineer agent", use_mock: bool = False):
    """Run scout locally without API."""
    from workey_agents.agent_a_job_scout import JobScoutAgent
    from workey_agents.agent_b_match_scorer import MatchScorerAgent

    scout = JobScoutAgent(use_mock=use_mock)
    scorer = MatchScorerAgent(use_llm=False)  # keyword scoring for speed
    
    jobs = await scout.discover(query=query, location="remote")
    print(f"[Worker] Discovered {len(jobs)} jobs")
    
    scored = await scorer.score_batch(jobs)
    
    auto_apply = [(j, s) for j, s in scored if s.total_score >= 85]
    queue_review = [(j, s) for j, s in scored if 70 <= s.total_score < 85]
    archived = [(j, s) for j, s in scored if s.total_score < 70]
    
    print(f"\n[Worker] Results:")
    print(f"  Auto-apply (≥85): {len(auto_apply)}")
    for job, score in auto_apply:
        print(f"    ✅ {score.total_score}/100 - {job.title} @ {job.company}")
    
    print(f"  Queue review (70-84): {len(queue_review)}")
    for job, score in queue_review:
        print(f"    📋 {score.total_score}/100 - {job.title} @ {job.company}")
    
    print(f"  Archived (<70): {len(archived)}")
    
    return {"auto_apply": len(auto_apply), "queue_review": len(queue_review), "archived": len(archived)}


async def run_portfolio_sync():
    """Sync GitHub repos for portfolio."""
    from workey_agents.agent_h_portfolio import PortfolioCuratorAgent
    
    print("[Worker] Syncing GitHub portfolio...")
    agent = PortfolioCuratorAgent()
    portfolio = await agent.build_portfolio_data()
    print(f"[Worker] Portfolio sync complete: {portfolio['total_repos']} repos")
    return portfolio


async def scheduled_run():
    """Main scheduled task loop."""
    print("[Worker] Workey scheduled worker started")
    print("[Worker] Running initial job scout...")
    
    await run_scout_local(use_mock=True)  # Use mock for initial run
    
    print("\n[Worker] Portfolio sync...")
    try:
        await run_portfolio_sync()
    except Exception as e:
        print(f"[Worker] Portfolio sync error: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Workey Worker")
    parser.add_argument("--task", choices=["scout", "portfolio", "all"], default="all")
    parser.add_argument("--query", default="AI ML engineer agent")
    parser.add_argument("--mock", action="store_true", help="Use mock data")
    args = parser.parse_args()
    
    if args.task == "scout":
        asyncio.run(run_scout_local(args.query, args.mock))
    elif args.task == "portfolio":
        asyncio.run(run_portfolio_sync())
    else:
        asyncio.run(scheduled_run())
