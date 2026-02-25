"""Agent H: Portfolio Curator - Syncs and curates GitHub projects for portfolio."""
from __future__ import annotations
import os
import httpx
import yaml
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"

GITHUB_API = "https://api.github.com"
CATEGORY_KEYWORDS = {
    "agentic_systems": ["agent", "langchain", "langgraph", "crewai", "autonomous", "llm", "multi-agent"],
    "trading_quant": ["trading", "bot", "quant", "algo", "defi", "alpha", "signal", "backtest"],
    "voice_ai": ["voice", "livekit", "elevenlabs", "tts", "stt", "speech", "audio"],
    "web3_defi": ["web3", "solidity", "ethereum", "defi", "nft", "smart-contract", "blockchain"],
    "dev_tools": ["cli", "tool", "utility", "generator", "parser", "formatter", "template"],
    "hackathon": ["hackathon", "hack", "submission", "demo"],
}


def categorize_repo(repo: dict) -> str:
    """Categorize a GitHub repo based on its name, description, and topics."""
    text = " ".join([
        repo.get("name", ""),
        repo.get("description", "") or "",
        " ".join(repo.get("topics", [])),
    ]).lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return category
    return "dev_tools"


class PortfolioCuratorAgent:
    """Syncs GitHub repos and curates portfolio content."""
    
    def __init__(self, username: str | None = None, token: str | None = None):
        self.username = username or os.getenv("GITHUB_USERNAME", "wildhash")
        self.token = token or os.getenv("GITHUB_TOKEN", "")
    
    def _headers(self) -> dict:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    async def sync_repos(self, limit: int = 100) -> list[dict]:
        """Fetch public repos from GitHub."""
        repos = []
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                page = 1
                while len(repos) < limit:
                    resp = await client.get(
                        f"{GITHUB_API}/users/{self.username}/repos",
                        headers=self._headers(),
                        params={"sort": "updated", "per_page": 100, "page": page, "type": "public"},
                    )
                    resp.raise_for_status()
                    batch = resp.json()
                    if not batch:
                        break
                    repos.extend(batch)
                    if len(batch) < 100:
                        break
                    page += 1
        except Exception as e:
            print(f"[PortfolioCurator] GitHub API error: {e}")
        
        return repos[:limit]
    
    def categorize_repos(self, repos: list[dict]) -> dict[str, list[dict]]:
        """Group repos by category."""
        categorized: dict[str, list[dict]] = {cat: [] for cat in CATEGORY_KEYWORDS}
        for repo in repos:
            category = categorize_repo(repo)
            categorized.setdefault(category, []).append(repo)
        return categorized
    
    def generate_project_card(self, repo: dict) -> dict:
        """Generate a project card from a GitHub repo."""
        return {
            "id": repo["name"],
            "name": repo["name"],
            "description": repo.get("description") or "",
            "url": repo["html_url"],
            "category": categorize_repo(repo),
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language"),
            "topics": repo.get("topics", []),
            "updated_at": repo.get("updated_at"),
        }
    
    async def build_portfolio_data(self) -> dict:
        """Build complete portfolio data from GitHub."""
        repos = await self.sync_repos()
        categorized = self.categorize_repos(repos)
        
        portfolio = {
            "total_repos": len(repos),
            "categories": {},
        }
        
        for category, cat_repos in categorized.items():
            portfolio["categories"][category] = {
                "count": len(cat_repos),
                "projects": [self.generate_project_card(r) for r in cat_repos],
            }
        
        return portfolio
