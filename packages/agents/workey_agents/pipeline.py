"""Main pipeline orchestrating all agents for the job acquisition workflow."""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
from .agent_a_job_scout import JobScoutAgent
from .agent_b_match_scorer import MatchScorerAgent
from .agent_c_resume_tailor import ResumeTailorAgent
from .agent_d_cover_letter import CoverLetterAgent
from .schemas import JobListing, JobScore, ResumeVariant, OutreachDraft


@dataclass
class ApplicationPackage:
    """Complete application package for a single job."""
    job: JobListing
    score: JobScore
    resume: ResumeVariant | None
    outreach: OutreachDraft | None


class WorkeyPipeline:
    """Orchestrates the full job acquisition pipeline."""
    
    def __init__(self, use_mock: bool = False, use_llm: bool = True):
        self.scout = JobScoutAgent(use_mock=use_mock)
        self.scorer = MatchScorerAgent(use_llm=use_llm)
        self.tailor = ResumeTailorAgent() if use_llm else None
        self.cover_agent = CoverLetterAgent() if use_llm else None
    
    async def run(
        self,
        query: str = "AI ML engineer agent",
        location: str = "remote",
        auto_tailor_threshold: int = 85,
        queue_review_threshold: int = 70,
    ) -> list[ApplicationPackage]:
        """Run the full pipeline: discover → score → tailor → draft."""
        print(f"\n[Pipeline] Starting job acquisition pipeline...")
        print(f"[Pipeline] Query: '{query}' | Location: {location}")
        
        # Phase 1: Discover
        print("\n[Pipeline] Phase 1: Job Discovery")
        jobs = await self.scout.discover(query=query, location=location)
        print(f"[Pipeline] Discovered {len(jobs)} jobs")
        
        # Phase 2: Score
        print("\n[Pipeline] Phase 2: Scoring")
        scored = await self.scorer.score_batch(jobs)
        
        # Phase 3: Classify and tailor high-scoring jobs
        packages = []
        auto_apply = [(j, s) for j, s in scored if s.total_score >= auto_tailor_threshold]
        queue_review = [(j, s) for j, s in scored if queue_review_threshold <= s.total_score < auto_tailor_threshold]
        archived = [(j, s) for j, s in scored if s.total_score < queue_review_threshold]
        
        print(f"\n[Pipeline] Results:")
        print(f"  Auto-apply (≥{auto_tailor_threshold}): {len(auto_apply)} jobs")
        print(f"  Queue review ({queue_review_threshold}-{auto_tailor_threshold-1}): {len(queue_review)} jobs")
        print(f"  Archived (<{queue_review_threshold}): {len(archived)} jobs")
        
        # Phase 4: Tailor top jobs
        print("\n[Pipeline] Phase 3: Tailoring top jobs")
        for job, score in auto_apply:
            print(f"  Tailoring: {job.title} @ {job.company} (score: {score.total_score})")
            resume = None
            outreach = None
            
            if self.tailor:
                try:
                    resume = await self.tailor.tailor(job)
                except Exception as e:
                    print(f"  [!] Resume tailor error: {e}")
            
            if self.cover_agent:
                try:
                    outreach = await self.cover_agent.draft(job, score)
                except Exception as e:
                    print(f"  [!] Cover letter error: {e}")
            
            packages.append(ApplicationPackage(job=job, score=score, resume=resume, outreach=outreach))
        
        # Add queue_review jobs without tailoring
        for job, score in queue_review:
            packages.append(ApplicationPackage(job=job, score=score, resume=None, outreach=None))
        
        print(f"\n[Pipeline] Pipeline complete. {len(packages)} application packages ready.")
        return packages
