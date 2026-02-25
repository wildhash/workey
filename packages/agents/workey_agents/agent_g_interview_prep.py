"""Agent G: Interview Prep Coach - Generates interview prep packs."""
from __future__ import annotations
from langchain_core.prompts import ChatPromptTemplate
from .schemas import JobListing, InterviewPrepPack
from .llm import get_llm

INTERVIEW_PREP_PROMPT = """\
You are preparing Will Oak Wild for a job interview.

## Will's Background
- AI/ML Engineer and technical founder
- Ships multi-agent systems (LangGraph, LangChain, CrewAI)
- Voice AI: LiveKit, ElevenLabs
- Algorithmic trading: BotSpot.trade, AlphaShield, AlphaGenesis
- 60+ open-source projects
- Full-stack: Python, TypeScript, FastAPI, Next.js, PostgreSQL

## Target Role
Company: {company}
Title: {title}
JD:
{jd_text}

## Generate Interview Prep Pack
Respond with JSON:
{{
  "company_brief": "2-3 paragraphs: what company does, product, tech stack, recent signals/news",
  "role_brief": "What this role actually cares about, key success metrics, day-to-day focus",
  "why_you": "Will's specific positioning for THIS role - 3-4 talking points",
  "likely_questions": [
    "Question 1",
    "Question 2",
    "... 10 questions total (mix behavioral + technical)"
  ],
  "star_stories": [
    {{
      "question_type": "Tell me about a complex system you built",
      "story": "STAR-format answer using Will's real work"
    }},
    {{
      "question_type": "How do you handle ambiguity?",
      "story": "STAR-format answer"
    }}
  ],
  "technical_talking_points": [
    "LangGraph multi-agent architecture: ...",
    "Real-time systems with WebSockets: ...",
    "... (5-7 points)"
  ],
  "questions_to_ask": [
    "Question 1 to ask interviewer",
    "... 5 questions total"
  ],
  "compensation_talking_points": "How to handle comp discussion - anchor, range, equity considerations",
  "red_flags": ["Potential concern 1", "Potential concern 2"]
}}
"""


class InterviewPrepAgent:
    """Generates interview preparation packs."""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.3)
        self.prompt = ChatPromptTemplate.from_template(INTERVIEW_PREP_PROMPT)
    
    async def prepare(self, job: JobListing) -> InterviewPrepPack:
        """Generate an interview prep pack for a job."""
        chain = self.prompt | self.llm
        
        result = await chain.ainvoke({
            "company": job.company,
            "title": job.title,
            "jd_text": job.jd_text[:4000],
        })
        
        import json
        content = result.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        data = json.loads(content)
        
        return InterviewPrepPack(
            company_brief=data.get("company_brief", ""),
            role_brief=data.get("role_brief", ""),
            why_you=data.get("why_you", ""),
            likely_questions=data.get("likely_questions", []),
            star_stories=data.get("star_stories", []),
            technical_talking_points=data.get("technical_talking_points", []),
            questions_to_ask=data.get("questions_to_ask", []),
            compensation_talking_points=data.get("compensation_talking_points", ""),
            red_flags=data.get("red_flags", []),
        )
