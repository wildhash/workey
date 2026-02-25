"""Agents router - trigger agent runs."""
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import AgentRun, Job, JobScore

router = APIRouter()


class ScoutRequest(BaseModel):
    query: str = "AI ML engineer agent"
    location: str = "remote"
    use_mock: bool = False


class ScoreRequest(BaseModel):
    job_id: str
    use_llm: bool = False


class TailorRequest(BaseModel):
    job_id: str


class OutreachRequest(BaseModel):
    job_id: str


@router.post("/scout")
async def run_job_scout(
    req: ScoutRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Trigger Job Scout agent to discover new listings."""
    run_id = str(uuid.uuid4())

    background_tasks.add_task(_run_scout_task, run_id, req.query, req.location, req.use_mock)

    return {
        "run_id": run_id,
        "status": "started",
        "message": "Job Scout running in background",
    }


async def _run_scout_task(run_id: str, query: str, location: str, use_mock: bool):
    """Background task for job scouting."""
    # Import here to avoid circular imports and optional dependency issues
    try:
        from workey_agents.agent_a_job_scout import JobScoutAgent

        scout = JobScoutAgent(use_mock=use_mock)
        jobs = await scout.discover(query=query, location=location)
        print(f"[Scout Task {run_id}] Found {len(jobs)} jobs")
    except ImportError as e:
        print(f"[Scout Task {run_id}] workey_agents not installed: {e}")
    except Exception as e:
        print(f"[Scout Task {run_id}] Error: {e}")


@router.post("/score/{job_id}")
async def score_job(job_id: str, use_llm: bool = False, db: AsyncSession = Depends(get_db)):
    """Score a specific job listing."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        from workey_agents.agent_b_match_scorer import MatchScorerAgent
        from workey_agents.schemas import JobListing

        job_listing = JobListing(
            company=job.company,
            title=job.title,
            location=job.location,
            remote_type=job.remote_type,
            source=job.source,
            url=job.url,
            jd_text=job.jd_text,
            tags=job.tags or [],
        )

        scorer = MatchScorerAgent(use_llm=use_llm)
        score = await scorer.score(job_listing)

        # Save score
        existing_score = await db.execute(select(JobScore).where(JobScore.job_id == job_id))
        job_score_rec = existing_score.scalar_one_or_none()

        if job_score_rec:
            job_score_rec.total_score = score.total_score
            job_score_rec.role_relevance = score.role_relevance
            job_score_rec.skills_overlap = score.skills_overlap
            job_score_rec.seniority_fit = score.seniority_fit
            job_score_rec.tech_stack_fit = score.tech_stack_fit
            job_score_rec.geo_remote_fit = score.geo_remote_fit
            job_score_rec.compensation_fit = score.compensation_fit
            job_score_rec.mission_fit = score.mission_fit
            job_score_rec.why_fit = score.why_fit
            job_score_rec.gaps = score.gaps
        else:
            job_score_rec = JobScore(
                id=str(uuid.uuid4()),
                job_id=job_id,
                total_score=score.total_score,
                role_relevance=score.role_relevance,
                skills_overlap=score.skills_overlap,
                seniority_fit=score.seniority_fit,
                tech_stack_fit=score.tech_stack_fit,
                geo_remote_fit=score.geo_remote_fit,
                compensation_fit=score.compensation_fit,
                mission_fit=score.mission_fit,
                why_fit=score.why_fit,
                gaps=score.gaps,
            )
            db.add(job_score_rec)

        job.score = score.total_score
        job.status = "scored"
        await db.commit()

        return {"job_id": job_id, "score": score.model_dump()}
    except ImportError as e:
        raise HTTPException(status_code=503, detail="Scoring agents unavailable") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/runs")
async def list_agent_runs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AgentRun).limit(50))
    runs = result.scalars().all()
    return [
        {
            "id": r.id,
            "agent_name": r.agent_name,
            "status": r.status,
            "started_at": r.started_at.isoformat(),
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
        }
        for r in runs
    ]
