"""HackerNews Who's Hiring adapter - scrapes monthly hiring threads."""
from __future__ import annotations
import re
import httpx
from .agent_a_job_scout import JobScoutAdapter, _make_hash
from .schemas import JobListing

HN_API = "https://hacker-news.firebaseio.com/v0"


class HackerNewsAdapter(JobScoutAdapter):
    """Scrapes HN 'Who is hiring?' monthly threads."""

    source_name = "hackernews"

    async def _get_latest_hiring_thread(self, client: httpx.AsyncClient) -> int | None:
        """Find the latest 'Who is hiring?' thread by whoishiring user."""
        resp = await client.get(f"{HN_API}/user/whoishiring.json")
        resp.raise_for_status()
        user = resp.json()
        for story_id in user.get("submitted", [])[:5]:
            resp2 = await client.get(f"{HN_API}/item/{story_id}.json")
            resp2.raise_for_status()
            item = resp2.json()
            title = (item.get("title") or "").lower()
            if "who is hiring" in title:
                return story_id
        return None

    def _parse_hn_comment(self, comment: dict) -> JobListing | None:
        """Parse an HN comment into a JobListing."""
        text = comment.get("text", "")
        if not text or len(text) < 50:
            return None

        # HN format: "Company | Role | Location | ..."
        lines = text.replace("<p>", "\n").split("\n")
        first_line = re.sub(r"<[^>]+>", "", lines[0]).strip()
        parts = [p.strip() for p in first_line.split("|")]

        company = parts[0] if len(parts) > 0 else "Unknown"
        title = parts[1] if len(parts) > 1 else first_line[:80]
        location = parts[2] if len(parts) > 2 else "Unknown"

        # Clean HTML
        clean_text = re.sub(r"<[^>]+>", " ", text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        # Detect remote
        loc_lower = location.lower()
        remote_type = "remote" if "remote" in loc_lower else "onsite"

        url = f"https://news.ycombinator.com/item?id={comment.get('id', '')}"

        # Extract tags from text
        tag_keywords = ["python", "typescript", "javascript", "react", "fastapi",
                        "langchain", "llm", "ai", "ml", "agent", "trading",
                        "rust", "go", "kubernetes", "docker", "aws", "gcp"]
        tags = [t for t in tag_keywords if t in clean_text.lower()]

        return JobListing(
            company=company[:100],
            title=title[:200],
            location=location[:100],
            remote_type=remote_type,
            source=self.source_name,
            url=url,
            jd_text=clean_text[:5000],
            tags=tags,
            ingest_hash=_make_hash(company, title, url),
        )

    async def scrape(self, query: str, location: str = "remote") -> list[JobListing]:
        """Scrape the latest HN Who is hiring thread."""
        jobs = []
        query_terms = query.lower().split()
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                thread_id = await self._get_latest_hiring_thread(client)
                if not thread_id:
                    print("[HackerNews] Could not find hiring thread")
                    return []

                resp = await client.get(f"{HN_API}/item/{thread_id}.json")
                resp.raise_for_status()
                thread = resp.json()
                kid_ids = thread.get("kids", [])[:80]

                print(f"[HackerNews] Found thread, scanning {len(kid_ids)} top comments")

                import asyncio
                sem = asyncio.Semaphore(10)

                async def fetch_comment(kid_id):
                    async with sem:
                        try:
                            r = await client.get(f"{HN_API}/item/{kid_id}.json", timeout=5)
                            r.raise_for_status()
                            return r.json()
                        except Exception:
                            return None

                comments = await asyncio.gather(*(fetch_comment(kid) for kid in kid_ids))

                for comment in comments:
                    if not comment or comment.get("deleted") or comment.get("dead"):
                        continue
                    text_lower = (comment.get("text") or "").lower()
                    if not any(term in text_lower for term in query_terms):
                        continue
                    if location.lower() == "remote" and "remote" not in text_lower:
                        continue
                    listing = self._parse_hn_comment(comment)
                    if listing:
                        jobs.append(listing)

        except Exception as e:
            print(f"[HackerNews] Error: {e}")
        return jobs
