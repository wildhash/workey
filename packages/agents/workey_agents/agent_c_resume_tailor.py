"""Agent C: Resume Tailor - Generates role-specific resume variants."""
from __future__ import annotations
import os
import yaml
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from .schemas import JobListing, ResumeVariant
from .llm import get_llm

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"

TAILORING_PROMPT = """\
You are an expert resume writer. Your job is to tailor a master resume to a specific job listing.

IMPORTANT RULES:
- DO NOT fabricate claims, dates, titles, or employers
- DO NOT invent skills or experiences the candidate doesn't have
- Flag missing requirements as gaps instead of inventing them
- Preserve factual accuracy while optimizing for relevance
- Write in concise STAR/CAR bullet style (Action → Impact)
- Use ATS-friendly language

## Master Resume
{master_resume}

## Target Job
Company: {company}
Title: {title}
JD:
{jd_text}

## Your Task
Generate a tailored resume variant. Respond with a JSON object matching this structure:
{{
  "headline": "Role-specific professional headline (max 10 words)",
  "summary": "3-4 sentence summary aligned to this specific role",
  "skills": ["list", "of", "most_relevant", "skills", "max_15"],
  "experience": [
    {{
      "company": "Company name",
      "title": "Job title",
      "period": "Date range",
      "bullets": ["Rewritten bullet 1", "Rewritten bullet 2", "Rewritten bullet 3"]
    }}
  ],
  "highlighted_projects": ["project_id_1", "project_id_2", "project_id_3"],
  "variant_type": "ats",
  "gaps": ["Missing skill 1", "Missing requirement 2"]
}}

Prioritize relevance. Reorder bullets to lead with the most relevant achievements.
"""


class ResumeTailorAgent:
    """Tailors master resume to specific job listings."""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.2)
        self.prompt = ChatPromptTemplate.from_template(TAILORING_PROMPT)
        self._master_resume: dict | None = None
    
    def _load_master_resume(self) -> dict:
        """Load master resume YAML."""
        if self._master_resume is None:
            resume_path = DATA_DIR / "resume_master.yaml"
            with open(resume_path) as f:
                self._master_resume = yaml.safe_load(f)
        return self._master_resume
    
    async def tailor(self, job: JobListing) -> ResumeVariant:
        """Generate a tailored resume variant for a specific job."""
        master = self._load_master_resume()
        master_text = yaml.dump(master, default_flow_style=False)
        
        chain = self.prompt | self.llm
        result = await chain.ainvoke({
            "master_resume": master_text[:4000],
            "company": job.company,
            "title": job.title,
            "jd_text": job.jd_text[:3000],
        })
        
        import json
        content = result.content
        # Extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        data = json.loads(content)
        
        return ResumeVariant(
            headline=data.get("headline", ""),
            summary=data.get("summary", ""),
            skills=data.get("skills", []),
            experience=data.get("experience", []),
            highlighted_projects=data.get("highlighted_projects", []),
            variant_type=data.get("variant_type", "ats"),
            model_used=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        )
