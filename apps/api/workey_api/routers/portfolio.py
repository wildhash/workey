"""Portfolio router - GitHub repo sync and portfolio data."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import anyio
import yaml
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter()

try:
    from workey_agents.agent_h_portfolio import PortfolioCuratorAgent
except ImportError:  # pragma: no cover
    logger.exception("Failed to import PortfolioCuratorAgent; portfolio endpoint will be unavailable")
    PortfolioCuratorAgent = None  # type: ignore[assignment]


def _resolve_data_dir() -> Path:
    if env_dir := os.getenv("WORKEY_DATA_DIR"):
        return Path(env_dir).resolve()

    for parent in Path(__file__).resolve().parents:
        candidate = parent / "data"
        if (candidate / "projects.yaml").exists():
            return candidate.resolve()

    return (Path.cwd() / "data").resolve()


DATA_DIR = _resolve_data_dir()
PROJECTS_YAML_PATH = DATA_DIR / "projects.yaml"


async def _read_yaml(path: Path) -> dict:
    def _load() -> dict:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
        if not isinstance(data, dict):
            raise TypeError(f"YAML root must be a mapping, got {type(data).__name__}")
        return data

    return await anyio.to_thread.run_sync(_load)


@router.get("")
async def get_portfolio():
    """Get portfolio data from GitHub."""
    if PortfolioCuratorAgent is None:
        raise HTTPException(status_code=503, detail="Portfolio agent unavailable")
    try:
        agent = PortfolioCuratorAgent()
        return await agent.build_portfolio_data()
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
        projects = data.get("projects", [])
        if "projects" in data and not isinstance(projects, list):
            logger.error("Projects YAML 'projects' must be a list, got %s", type(projects).__name__)
            raise HTTPException(status_code=500, detail="Projects data is invalid")

        return projects
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Projects data not found")
    except ValueError:
        logger.exception("Projects YAML is invalid")
        raise HTTPException(status_code=500, detail="Projects data is invalid")
    except HTTPException:
        raise
    except TypeError:
        logger.exception("Projects YAML root must be a mapping")
        raise HTTPException(status_code=500, detail="Projects data is invalid")
    except Exception:
        logger.exception("Projects YAML read failed")
        raise HTTPException(status_code=500, detail="Projects read failed")
