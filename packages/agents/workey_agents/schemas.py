"""Shared schemas / Pydantic models for agent I/O."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobListing(BaseModel):
    """A job listing discovered by Job Scout."""
    company: str
    title: str
    location: str
    remote_type: str = Field(default="remote", description="remote|hybrid|onsite")
    source: str
    url: str
    posted_at: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    jd_text: str
    tags: list[str] = Field(default_factory=list)
    ingest_hash: str = ""


class JobScore(BaseModel):
    """Score output from Match Scorer agent."""
    total_score: int = Field(ge=0, le=100)
    role_relevance: int = Field(ge=0, le=20)
    skills_overlap: int = Field(ge=0, le=20)
    seniority_fit: int = Field(ge=0, le=15)
    tech_stack_fit: int = Field(ge=0, le=15)
    geo_remote_fit: int = Field(ge=0, le=10)
    compensation_fit: int = Field(ge=0, le=10)
    mission_fit: int = Field(ge=0, le=10)
    why_fit: str
    gaps: list[str] = Field(default_factory=list)
    action: str = Field(description="auto_apply|queue_review|archive")


class ResumeVariant(BaseModel):
    """A tailored resume variant."""
    headline: str
    summary: str
    skills: list[str]
    experience: list[dict]
    highlighted_projects: list[str]
    variant_type: str = "ats"
    model_used: str = ""


class OutreachDraft(BaseModel):
    """Outreach messages drafted for a job application."""
    cover_letter: str
    recruiter_email: str
    hiring_manager_note: str
    linkedin_connect: str
    follow_up_3day: str
    follow_up_7day: str
    follow_up_14day: str


class InterviewPrepPack(BaseModel):
    """Interview preparation pack for a specific role."""
    company_brief: str
    role_brief: str
    why_you: str
    likely_questions: list[str]
    star_stories: list[dict]
    technical_talking_points: list[str]
    questions_to_ask: list[str]
    compensation_talking_points: str
    red_flags: list[str]
