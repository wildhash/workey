"""Portfolio router - GitHub repo sync and portfolio data."""

from __future__ import annotations

import logging
from pathlib import Path

import anyio
import yaml
from fastapi import APIRouter, HTTPException

router = APIRouter()

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data"
PROJECTS_YAML_PATH = DATA_DIR / "projects.yaml"
AGENTS_DIR = REPO_ROOT / "packages" / "agents"


def _import_portfolio_agent():
    try:
        from workey_agents.agent_h_portfolio import PortfolioCuratorAgent

        return PortfolioCuratorAgent
    except ModuleNotFoundError:
        pass

    try:
        import sys

        if AGENTS_DIR.exists() and str(AGENTS_DIR) not in sys.path:
            sys.path.insert(0, str(AGENTS_DIR))

        from workey_agents.agent_h_portfolio import PortfolioCuratorAgent

        return PortfolioCuratorAgent
    except Exception:
        logger.exception("Failed to import PortfolioCuratorAgent")
        return None


PortfolioCuratorAgent = _import_portfolio_agent()


async def _read_yaml(path: Path) -> dict:
    content = await anyio.to_thread.run_sync(path.read_text, encoding="utf-8")
    return yaml.safe_load(content) or {}


@router.get("")
async def get_portfolio():
    """Get portfolio data from GitHub."""
    if PortfolioCuratorAgent is None:
        raise HTTPException(status_code=503, detail="Portfolio agent unavailable")

    try:
        agent = PortfolioCuratorAgent()
        portfolio = await agent.build_portfolio_data()
        return portfolio
    except HTTPException:
        raise
    except Exception:
        logger.exception("Portfolio sync failed")
        raise HTTPException(status_code=500, detail="Portfolio sync failed")


@router.get("/projects")
async def list_projects():
    """List projects from data/projects.yaml."""
    try:
        data = await _read_yaml(PROJECTS_YAML_PATH)
        return data.get("projects", [])
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Projects data not found")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Projects YAML read failed")
        raise HTTPException(status_code=500, detail="Projects read failed")
