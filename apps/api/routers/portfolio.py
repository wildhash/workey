"""Portfolio router - GitHub repo sync and portfolio data."""
import sys
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("")
async def get_portfolio():
    """Get portfolio data from GitHub."""
    try:
        sys.path.insert(0, "/home/runner/work/workey/workey/packages/agents")
        from workey_agents.agent_h_portfolio import PortfolioCuratorAgent
        
        agent = PortfolioCuratorAgent()
        portfolio = await agent.build_portfolio_data()
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects")
async def list_projects():
    """List projects from data/projects.yaml."""
    import yaml
    from pathlib import Path
    
    projects_path = Path("/home/runner/work/workey/workey/data/projects.yaml")
    with open(projects_path) as f:
        data = yaml.safe_load(f)
    return data.get("projects", [])
