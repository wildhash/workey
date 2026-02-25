"""Jobs router."""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from database import get_db, create_tables
from models import Job, JobScore

router = APIRouter()


class JobResponse(BaseModel):
    id: str
    company: str
    title: str
    location: str
    remote_type: str
    source: str
    url: str
    posted_at: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    jd_text: str
    tags: list
    status: str
    score: Optional[int]
    created_at: str

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    company: str
    title: str
    location: str = "Remote"
    remote_type: str = "remote"
    source: str = "manual"
    url: str
    posted_at: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    jd_text: str = ""
    tags: list[str] = []


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    status: Optional[str] = Query(None),
    min_score: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List all jobs with optional filters."""
    query = select(Job).order_by(desc(Job.created_at)).limit(limit)
    if status:
        query = query.where(Job.status == status)
    if min_score is not None:
        query = query.where(Job.score >= min_score)
    result = await db.execute(query)
    jobs = result.scalars().all()
    return [
        JobResponse(
            id=j.id,
            company=j.company,
            title=j.title,
            location=j.location,
            remote_type=j.remote_type,
            source=j.source,
            url=j.url,
            posted_at=j.posted_at,
            salary_min=j.salary_min,
            salary_max=j.salary_max,
            jd_text=j.jd_text,
            tags=j.tags or [],
            status=j.status,
            score=j.score,
            created_at=j.created_at.isoformat(),
        )
        for j in jobs
    ]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(
        id=job.id,
        company=job.company,
        title=job.title,
        location=job.location,
        remote_type=job.remote_type,
        source=job.source,
        url=job.url,
        posted_at=job.posted_at,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        jd_text=job.jd_text,
        tags=job.tags or [],
        status=job.status,
        score=job.score,
        created_at=job.created_at.isoformat(),
    )


@router.post("", response_model=JobResponse, status_code=201)
async def create_job(payload: JobCreate, db: AsyncSession = Depends(get_db)):
    """Manually add a job listing."""
    import hashlib
    ingest_hash = hashlib.sha256(f"{payload.company}|{payload.title}|{payload.url}".lower().encode()).hexdigest()[:16]
    
    job = Job(
        id=str(uuid.uuid4()),
        ingest_hash=ingest_hash,
        **payload.model_dump(),
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return JobResponse(
        id=job.id,
        company=job.company,
        title=job.title,
        location=job.location,
        remote_type=job.remote_type,
        source=job.source,
        url=job.url,
        posted_at=job.posted_at,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        jd_text=job.jd_text,
        tags=job.tags or [],
        status=job.status,
        score=job.score,
        created_at=job.created_at.isoformat(),
    )


@router.patch("/{job_id}/status")
async def update_job_status(job_id: str, status: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = status
    await db.commit()
    return {"id": job_id, "status": status}
