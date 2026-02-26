"""Applications router."""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Application

router = APIRouter()


class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    status: str
    cover_letter: Optional[str]
    notes: Optional[str]
    applied_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    job_id: str
    status: str = "draft"
    cover_letter: Optional[str] = None
    recruiter_email: Optional[str] = None
    hiring_manager_note: Optional[str] = None
    linkedin_connect: Optional[str] = None
    notes: Optional[str] = None


@router.get("", response_model=list[ApplicationResponse])
async def list_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).order_by(desc(Application.created_at)))
    apps = result.scalars().all()
    return [
        ApplicationResponse(
            id=a.id,
            job_id=a.job_id,
            status=a.status,
            cover_letter=a.cover_letter,
            notes=a.notes,
            applied_at=a.applied_at.isoformat() if a.applied_at else None,
            created_at=a.created_at.isoformat(),
        )
        for a in apps
    ]


@router.post("", response_model=ApplicationResponse, status_code=201)
async def create_application(payload: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    app = Application(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return ApplicationResponse(
        id=app.id,
        job_id=app.job_id,
        status=app.status,
        cover_letter=app.cover_letter,
        notes=app.notes,
        applied_at=app.applied_at.isoformat() if app.applied_at else None,
        created_at=app.created_at.isoformat(),
    )


@router.patch("/{app_id}/status")
async def update_application_status(app_id: str, status: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).where(Application.id == app_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = status
    await db.commit()
    return {"id": app_id, "status": status}
