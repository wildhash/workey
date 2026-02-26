"""Agent D: Cover Letter + Outreach - Drafts cover letters and outreach messages."""
from __future__ import annotations
import os
from langchain_core.prompts import ChatPromptTemplate
from .schemas import JobListing, JobScore, OutreachDraft
from .llm import get_llm

OUTREACH_PROMPT = """\
You are writing outreach messages for Will Oak Wild, an AI/ML Engineer and technical founder.

## Will's Positioning
- Builder of autonomous systems
- Shipped 60+ projects spanning AI agents, trading, voice AI, DeFi
- Deep LangGraph/LangChain expertise with production deployments
- Voice AI with LiveKit and ElevenLabs
- Algorithmic trading and DeFi automation (BotSpot.trade)
- Solo founder execution speed
- Tone: elite but grounded, technical but clear, strong ownership energy

## Target Role
Company: {company}
Title: {title}
Score: {score}/100
Why fit: {why_fit}
Gaps: {gaps}

JD excerpt:
{jd_excerpt}

## Generate all outreach messages
Respond with a JSON object:
{{
  "cover_letter": "Full cover letter (3-4 paragraphs, max 400 words). Strong opening, specific alignment, clear CTA.",
  "recruiter_email": "Short recruiter outreach email (max 150 words). Subject line included as first line starting with 'Subject: '",
  "hiring_manager_note": "Direct note to hiring manager (max 120 words). More technical, shows research.",
  "linkedin_connect": "LinkedIn connection request (max 300 chars). Specific, not generic.",
  "follow_up_3day": "3-day follow-up email (max 100 words).",
  "follow_up_7day": "7-day follow-up email (max 100 words). Slightly different angle.",
  "follow_up_14day": "14-day final follow-up (max 80 words). Graceful, leaves door open."
}}

Style rules:
- Sharp, technical, human - NOT desperate
- High-agency founder/engineer tone  
- Emphasize shipped systems, speed, ownership
- Reference specific company/role details
- No fluff or corporate speak
"""


class CoverLetterAgent:
    """Drafts cover letters and outreach messages for job applications."""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.5)
        self.prompt = ChatPromptTemplate.from_template(OUTREACH_PROMPT)
    
    async def draft(self, job: JobListing, score: JobScore) -> OutreachDraft:
        """Draft all outreach messages for a job application."""
        chain = self.prompt | self.llm
        
        result = await chain.ainvoke({
            "company": job.company,
            "title": job.title,
            "score": score.total_score,
            "why_fit": score.why_fit,
            "gaps": ", ".join(score.gaps) if score.gaps else "None identified",
            "jd_excerpt": job.jd_text[:2000],
        })
        
        import json
        content = result.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        data = json.loads(content)
        
        return OutreachDraft(
            cover_letter=data.get("cover_letter", ""),
            recruiter_email=data.get("recruiter_email", ""),
            hiring_manager_note=data.get("hiring_manager_note", ""),
            linkedin_connect=data.get("linkedin_connect", ""),
            follow_up_3day=data.get("follow_up_3day", ""),
            follow_up_7day=data.get("follow_up_7day", ""),
            follow_up_14day=data.get("follow_up_14day", ""),
        )
