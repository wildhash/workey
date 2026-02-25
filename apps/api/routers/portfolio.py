"""Portfolio router - GitHub repo sync and portfolio data."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException

router = APIRouter()
logger = logging.getLogger(__name__)

try:
    from workey_agents.agent_h_portfolio import PortfolioCuratorAgent
except ImportError:  # pragma: no cover
    PortfolioCuratorAgent = None


def _resolve_data_dir() -> Path:
    env_dir = os.getenv("WORKEY_DATA_DIR")
    if env_dir:
        return Path(env_dir)

    file_path = Path(__file__).resolve()
    for parent in file_path.parents:
        candidate = parent / "data"
        if candidate.is_dir():
            return candidate

    return Path("/app/data")


DATA_DIR = _resolve_data_dir()
PROJECTS_YAML_PATH = DATA_DIR / "projects.yaml"


async def _read_yaml(path: Path) -> dict:
    def _load() -> dict:
        content = path.read_text(encoding="utf-8")
        return yaml.safe_load(content) or {}

    return await asyncio.to_thread(_load)


@router.get("")
async def get_portfolio():
    """Get portfolio data from GitHub."""
    if PortfolioCuratorAgent is None:
        raise HTTPException(status_code=503, detail="Portfolio agent not available")

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
    if not PROJECTS_YAML_PATH.is_file():
        raise HTTPException(status_code=404, detail="Projects data not found")

    try:
        data = await _read_yaml(PROJECTS_YAML_PATH)
        if not isinstance(data, dict):
            logger.error("Projects YAML root must be a mapping, got %s", type(data).__name__)
            raise HTTPException(status_code=500, detail="Projects data is invalid")

        projects = data.get("projects", [])
        if "projects" in data and not isinstance(projects, list):
            logger.error("Projects YAML 'projects' must be a list, got %s", type(projects).__name__)
            raise HTTPException(status_code=500, detail="Projects data is invalid")

        return projects
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Projects data not found")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Projects YAML read failed")
        raise HTTPException(status_code=500, detail="Projects read failed")
