"""Agent B: Match Scorer - Scores jobs against Will's profile."""
from __future__ import annotations
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .schemas import JobListing, JobScore
from .llm import get_llm

# Will's core skills for keyword matching
WILL_SKILLS = {
    "python", "typescript", "javascript", "fastapi", "next.js", "react",
    "langchain", "langgraph", "crewai", "openai", "anthropic", "llm",
    "multi-agent", "agents", "autonomous", "livekit", "elevenlabs", "voice",
    "websocket", "postgresql", "redis", "docker", "trading", "quant", "defi",
    "solidity", "web3", "rag", "embeddings", "vector", "fine-tuning",
}

TARGET_ROLES = {
    "ai engineer", "ml engineer", "machine learning", "artificial intelligence",
    "agentic", "agent systems", "applied ai", "solutions engineer",
    "forward deployed", "full-stack ai", "quant", "automation engineer",
}

TARGET_GEOS = {"remote", "vietnam", "thailand", "singapore", "malaysia", "sea"}

SCORING_PROMPT = """\
You are a career coach scoring a job listing against a candidate profile.

## Candidate: Will Oak Wild
- AI/ML Engineer and technical founder
- Skills: Python, TypeScript, FastAPI, Next.js, LangGraph, LangChain, CrewAI, OpenAI, Anthropic, 
  multi-agent systems, voice AI (LiveKit, ElevenLabs), algorithmic trading, DeFi, WebSockets, PostgreSQL
- 60+ shipped open-source projects
- Target roles: AI Engineer, ML Engineer, Agentic Systems Engineer, Applied AI, Solutions Engineer
- Target: Remote-first, SE Asia, US Remote
- Seniority: Mid-Senior / Lead level

## Job Listing
Company: {company}
Title: {title}
Location: {location}
JD:
{jd_text}

## Scoring Criteria (score each 0-max):
- role_relevance (0-20): How well does the role match AI/ML/agentic/full-stack focus?
- skills_overlap (0-20): Overlap between required skills and Will's skills?
- seniority_fit (0-15): Is the level right (not junior, not too senior for solo founder)?
- tech_stack_fit (0-15): Does the tech stack match Will's expertise?
- geo_remote_fit (0-10): Is it remote-first or in Will's target geos?
- compensation_fit (0-10): Based on any salary signals, does it fit?
- mission_fit (0-10): Does the company mission align (AI tools, trading, voice, dev tools)?

{format_instructions}

Be honest. Flag real gaps. Give a clear action recommendation.
"""


class MatchScorerAgent:
    """Scores job listings against Will's profile."""
    
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.parser = PydanticOutputParser(pydantic_object=JobScore)
        if use_llm:
            self.llm = get_llm(temperature=0.1)
            self.prompt = ChatPromptTemplate.from_template(SCORING_PROMPT)
            self.chain = self.prompt | self.llm | self.parser
    
    def _keyword_score(self, job: JobListing) -> JobScore:
        """Fast keyword-based scoring without LLM (fallback)."""
        jd_lower = job.jd_text.lower()
        title_lower = job.title.lower()
        
        # Role relevance
        role_relevance = 0
        for role in TARGET_ROLES:
            if role in title_lower or role in jd_lower:
                role_relevance += 4
        role_relevance = min(20, role_relevance)
        
        # Skills overlap
        jd_skills = set(jd_lower.split())
        tag_skills = {t.lower() for t in job.tags}
        overlap = WILL_SKILLS.intersection(jd_skills | tag_skills)
        skills_overlap = min(20, len(overlap) * 2)
        
        # Seniority
        seniority_fit = 10
        if "junior" in jd_lower or "entry" in jd_lower:
            seniority_fit = 3
        elif "senior" in title_lower or "lead" in title_lower or "staff" in title_lower:
            seniority_fit = 15
        
        # Tech stack
        tech_stack_fit = min(15, len(overlap) * 1)
        
        # Geo fit
        geo_text = job.location.lower() + " " + job.remote_type.lower()
        geo_remote_fit = 0
        if "remote" in geo_text:
            geo_remote_fit = 10
        elif any(geo in geo_text for geo in TARGET_GEOS):
            geo_remote_fit = 7
        
        # Compensation
        compensation_fit = 5
        if job.salary_min and job.salary_min >= 80000:
            compensation_fit = 10
        elif job.salary_max and job.salary_max < 60000:
            compensation_fit = 0
        
        # Mission
        mission_fit = 5
        mission_keywords = {"ai", "ml", "agent", "trading", "fintech", "voice", "automation", "developer"}
        if any(kw in jd_lower for kw in mission_keywords):
            mission_fit = 10
        
        total = role_relevance + skills_overlap + seniority_fit + tech_stack_fit + geo_remote_fit + compensation_fit + mission_fit
        
        if total >= 85:
            action = "auto_apply"
        elif total >= 70:
            action = "queue_review"
        else:
            action = "archive"
        
        return JobScore(
            total_score=total,
            role_relevance=role_relevance,
            skills_overlap=skills_overlap,
            seniority_fit=seniority_fit,
            tech_stack_fit=tech_stack_fit,
            geo_remote_fit=geo_remote_fit,
            compensation_fit=compensation_fit,
            mission_fit=mission_fit,
            why_fit=f"Keyword match: {len(overlap)} skills overlap ({', '.join(list(overlap)[:5])})",
            gaps=[],
            action=action,
        )
    
    async def score(self, job: JobListing) -> JobScore:
        """Score a job listing. Uses LLM if enabled, otherwise keyword scoring."""
        if not self.use_llm:
            return self._keyword_score(job)
        
        try:
            result = await self.chain.ainvoke({
                "company": job.company,
                "title": job.title,
                "location": job.location,
                "jd_text": job.jd_text[:3000],
                "format_instructions": self.parser.get_format_instructions(),
            })
            return result
        except Exception as e:
            print(f"[MatchScorer] LLM error, falling back to keyword: {e}")
            return self._keyword_score(job)
    
    async def score_batch(self, jobs: list[JobListing]) -> list[tuple[JobListing, JobScore]]:
        """Score multiple jobs."""
        results = []
        for job in jobs:
            score = await self.score(job)
            results.append((job, score))
        return results
