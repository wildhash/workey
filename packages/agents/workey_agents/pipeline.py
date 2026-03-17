"""Main pipeline orchestrating all agents for the job acquisition workflow."""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
from .agent_a_job_scout import JobScoutAgent
from .agent_b_match_scorer import MatchScorerAgent
from .agent_c_resume_tailor import ResumeTailorAgent
from .agent_d_cover_letter import CoverLetterAgent
from .agent_e_scam_shield import ScamShieldAgent
from .memory import EverMemOS
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
        self.scam_shield = ScamShieldAgent()
        self.scorer = MatchScorerAgent(use_llm=use_llm)
        self.tailor = ResumeTailorAgent() if use_llm else None
        self.cover_agent = CoverLetterAgent() if use_llm else None
        self.memory = EverMemOS()
    
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
        
        # Phase 1.5: Scam filter
        print("\n[Pipeline] Phase 1.5: Scam Shield")
        jobs, scam_reports = self.scam_shield.filter_batch(jobs)
        for report in scam_reports:
            self.memory.report_scam(report.get("company", "unknown"), report)
        print(f"[Pipeline] {len(jobs)} jobs passed scam filter")

        # Phase 1.6: Deduplicate against memory
        new_jobs = []
        for job in jobs:
            self.memory.remember_job(job.ingest_hash, job.model_dump())
            existing_app = self.memory.get_application(job.ingest_hash)
            if existing_app.get("status") in ("applied", "interviewing", "rejected"):
                print(f"  [Memory] Skipping already-applied: {job.title} @ {job.company}")
            else:
                new_jobs.append(job)
        jobs = new_jobs
        print(f"[Pipeline] {len(jobs)} new jobs after memory dedup")

        # Phase 2: Score
        print("\n[Pipeline] Phase 2: Scoring")
        scored = await self.scorer.score_batch(jobs)
        
        # Phase 3: Classify jobs by score
        packages = []
        auto_apply = [(j, s) for j, s in scored if s.total_score >= auto_tailor_threshold]
        queue_review = [(j, s) for j, s in scored if queue_review_threshold <= s.total_score < auto_tailor_threshold]
        archived = [(j, s) for j, s in scored if s.total_score < queue_review_threshold]
        
        print(f"\n[Pipeline] Results:")
        print(f"  Auto-apply (>={auto_tailor_threshold}): {len(auto_apply)} jobs")
        print(f"  Queue review ({queue_review_threshold}-{auto_tailor_threshold-1}): {len(queue_review)} jobs")
        print(f"  Archived (<{queue_review_threshold}): {len(archived)} jobs")
        
        # Phase 4: Tailor top jobs
        print("\n[Pipeline] Phase 4: Tailoring top jobs")
        sem = asyncio.Semaphore(3)

        async def build_package(job: JobListing, score: JobScore) -> ApplicationPackage:
            async with sem:
                try:
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

                    return ApplicationPackage(job=job, score=score, resume=resume, outreach=outreach)
                except Exception as e:
                    print(f"  [!] Unexpected packaging error for {job.title} @ {job.company}: {e}")
                    return ApplicationPackage(job=job, score=score, resume=None, outreach=None)

        packages.extend(await asyncio.gather(*(build_package(job, score) for job, score in auto_apply)))
        
        # Add queue_review jobs without tailoring
        for job, score in queue_review:
            packages.append(ApplicationPackage(job=job, score=score, resume=None, outreach=None))
        
        # Phase 5: Save to memory and log run
        for pkg in packages:
            self.memory.save_application(pkg.job.ingest_hash, {
                "status": "ready" if pkg.resume else "scored",
                "company": pkg.job.company,
                "title": pkg.job.title,
                "score": pkg.score.total_score,
                "action": pkg.score.action,
                "has_resume": pkg.resume is not None,
                "has_outreach": pkg.outreach is not None,
            })

        run_id = self.memory.log_run({
            "query": query,
            "location": location,
            "discovered": len(jobs) + len(scam_reports),
            "scams_blocked": len(scam_reports),
            "scored": len(scored),
            "auto_apply": len(auto_apply),
            "queue_review": len(queue_review),
            "archived": len(archived),
            "packages_ready": len(packages),
        })

        stats = self.memory.stats()
        print(f"\n[Pipeline] Pipeline complete. {len(packages)} application packages ready.")
        print(f"[Memory] Run logged: {run_id}")
        print(f"[Memory] Total jobs seen: {stats['total_jobs_seen']} | Applications: {stats['total_applications']} | Scams flagged: {stats['total_scams_flagged']}")
        return packages
