"""SQLAlchemy ORM models."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    company: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255), default="Remote")
    remote_type: Mapped[str] = mapped_column(String(50), default="remote")
    source: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(Text)
    posted_at: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(10), default="USD")
    jd_text: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    ingest_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="new")
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    job_score: Mapped["JobScore | None"] = relationship(
        "JobScore", back_populates="job", uselist=False
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="job"
    )


class JobScore(Base):
    __tablename__ = "job_scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), unique=True)
    total_score: Mapped[int] = mapped_column(Integer)
    role_relevance: Mapped[int] = mapped_column(Integer, default=0)
    skills_overlap: Mapped[int] = mapped_column(Integer, default=0)
    seniority_fit: Mapped[int] = mapped_column(Integer, default=0)
    tech_stack_fit: Mapped[int] = mapped_column(Integer, default=0)
    geo_remote_fit: Mapped[int] = mapped_column(Integer, default=0)
    compensation_fit: Mapped[int] = mapped_column(Integer, default=0)
    mission_fit: Mapped[int] = mapped_column(Integer, default=0)
    why_fit: Mapped[str] = mapped_column(Text, default="")
    gaps: Mapped[list] = mapped_column(JSON, default=list)
    scored_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    job: Mapped["Job"] = relationship("Job", back_populates="job_score")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"))
    status: Mapped[str] = mapped_column(String(50), default="draft")
    cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)
    recruiter_email: Mapped[str | None] = mapped_column(Text, nullable=True)
    hiring_manager_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    linkedin_connect: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ats_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    applied_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    job: Mapped["Job"] = relationship("Job", back_populates="applications")


class ResumeVariant(Base):
    __tablename__ = "resume_variants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    job_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("jobs.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255))
    variant_type: Mapped[str] = mapped_column(String(50), default="ats")
    headline: Mapped[str] = mapped_column(String(255), default="")
    summary: Mapped[str] = mapped_column(Text, default="")
    skills: Mapped[list] = mapped_column(JSON, default=list)
    experience: Mapped[list] = mapped_column(JSON, default=list)
    highlighted_projects: Mapped[list] = mapped_column(JSON, default=list)
    model_used: Mapped[str] = mapped_column(String(100), default="")
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    input_refs: Mapped[dict] = mapped_column(JSON, default=dict)
    output_refs: Mapped[dict] = mapped_column(JSON, default=dict)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
