"""Agent E: Scam Shield - Filters out scam/referral-farming job listings."""
from __future__ import annotations
import re
from .schemas import JobListing, JobScore


# Known scam/referral-farming domains and patterns
SCAM_DOMAINS = {
    "pyjamahr.com", "zohorecruit.com",
}

SCAM_COMPANIES = {
    "yo hr consultancy", "micro1", "pesto tech", "crossover",
}

GHOST_RECRUITER_PLATFORMS = {
    "mercor", "micro1", "pesto",
}

SCAM_TITLE_PATTERNS = [
    r"ai\s*trainer",
    r"ai\s*response\s*evaluator",
    r"data\s*annotation\s*specialist",
    r"ai\s*rater",
    r"search\s*quality\s*rater",
]

SCAM_JD_SIGNALS = [
    "complete a short ai interview",
    "15 minute ai interview",
    "referral partner",
    "complete this assessment",
    "pyjamahr",
    "take a quick ai test",
    "automated screening interview",
]

RED_FLAG_PATTERNS = [
    "pay upfront", "training fee", "equipment deposit",
    "wire transfer", "western union", "crypto payment required",
    "guaranteed placement", "100% placement",
    "no experience needed.*high salary",
]


class ScamShieldAgent:
    """Filters scam, ghost-recruiter, and referral-farming listings."""

    def __init__(self):
        self.scam_title_re = [re.compile(p, re.IGNORECASE) for p in SCAM_TITLE_PATTERNS]
        self.red_flag_re = [re.compile(p, re.IGNORECASE) for p in RED_FLAG_PATTERNS]

    def scan(self, job: JobListing) -> dict:
        """Scan a job listing for scam signals. Returns verdict dict."""
        flags: list[str] = []
        severity = 0  # 0=clean, 1-3=suspicious, 4+=scam

        # Check company name
        company_lower = job.company.lower().strip()
        if company_lower in SCAM_COMPANIES:
            flags.append(f"Known scam/ghost company: {job.company}")
            severity += 5

        # Check source domain
        url_lower = job.url.lower()
        for domain in SCAM_DOMAINS:
            if domain in url_lower:
                flags.append(f"Scam platform domain: {domain}")
                severity += 4

        # Check ghost recruiter platforms
        for ghost in GHOST_RECRUITER_PLATFORMS:
            if ghost in company_lower or ghost in url_lower:
                flags.append(f"Ghost recruiter platform: {ghost}")
                severity += 3

        # Check title patterns
        for pattern in self.scam_title_re:
            if pattern.search(job.title):
                flags.append(f"Scam title pattern: {job.title}")
                severity += 3
                break

        # Check JD for scam signals
        jd_lower = job.jd_text.lower()
        for signal in SCAM_JD_SIGNALS:
            if signal in jd_lower:
                flags.append(f"Scam JD signal: '{signal}'")
                severity += 2

        # Check red flags
        for pattern in self.red_flag_re:
            if pattern.search(jd_lower):
                flags.append(f"Red flag: {pattern.pattern}")
                severity += 4

        # Verdict
        if severity >= 4:
            verdict = "scam"
        elif severity >= 2:
            verdict = "suspicious"
        else:
            verdict = "clean"

        return {
            "verdict": verdict,
            "severity": severity,
            "flags": flags,
            "company": job.company,
            "title": job.title,
        }

    def filter_batch(
        self, jobs: list[JobListing]
    ) -> tuple[list[JobListing], list[dict]]:
        """Filter a batch of jobs. Returns (clean_jobs, flagged_reports)."""
        clean = []
        flagged = []
        for job in jobs:
            result = self.scan(job)
            if result["verdict"] == "scam":
                print(f"  [ScamShield] BLOCKED: {job.title} @ {job.company} — {result['flags'][0]}")
                flagged.append(result)
            elif result["verdict"] == "suspicious":
                print(f"  [ScamShield] ⚠ SUSPICIOUS: {job.title} @ {job.company}")
                clean.append(job)  # pass through but warn
                flagged.append(result)
            else:
                clean.append(job)
        print(f"  [ScamShield] {len(clean)} clean, {len(flagged)} flagged")
        return clean, flagged
