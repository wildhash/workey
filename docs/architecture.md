# Workey Architecture

## Overview

Workey is an autonomous job-acquisition and personal-brand operating system built as a modular multi-agent workflow. It is designed for solo founders and engineers who want to systematize and accelerate their job search.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        WORKEY SYSTEM                            │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  apps/web   │    │  apps/api   │    │    apps/worker      │ │
│  │  (Next.js)  │◄──►│  (FastAPI)  │◄──►│  (Background tasks) │ │
│  └─────────────┘    └──────┬──────┘    └─────────────────────┘ │
│                            │                                    │
│                    ┌───────┴───────┐                            │
│                    │  PostgreSQL   │                            │
│                    └───────────────┘                            │
│                            │                                    │
│              ┌─────────────▼─────────────┐                     │
│              │      packages/agents      │                     │
│              │  ┌──────────────────────┐ │                     │
│              │  │ A: Job Scout         │ │                     │
│              │  │ B: Match Scorer      │ │                     │
│              │  │ C: Resume Tailor     │ │                     │
│              │  │ D: Cover Letter      │ │                     │
│              │  │ E: App Runner        │ │                     │
│              │  │ F: Inbox Sentinel    │ │                     │
│              │  │ G: Interview Prep    │ │                     │
│              │  │ H: Portfolio Curator │ │                     │
│              │  └──────────────────────┘ │                     │
│              └───────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Job Acquisition Pipeline
```
1. Job Scout (A) → discovers listings from RemoteOK, Wellfound, etc.
2. Match Scorer (B) → scores each listing 0-100 across 7 dimensions
3. Decision:
   ├── Score ≥85 → Auto-tailor + draft outreach
   ├── Score 70-84 → Queue for human review
   └── Score <70 → Archive
4. Resume Tailor (C) → generates role-specific resume variant
5. Cover Letter Agent (D) → drafts full outreach suite (7 messages)
6. Application Runner (E) → prepares application with human approval gate
7. Inbox Sentinel (F) → monitors email for responses
8. Interview Prep (G) → generates prep pack when interview scheduled
```

## Tech Stack Decision

**Why FastAPI (Python) for API:**
- Agents are Python-native (LangGraph, LangChain, Pydantic)
- Async-first with excellent WebSocket support
- Pydantic models shared between API and agents
- Performance adequate for MVP load

**Why Next.js for Frontend:**
- App Router + React Server Components for SEO and performance
- TypeScript for type safety across the monorepo
- Vercel deployment is trivial
- Ecosystem supports shadcn/ui, Framer Motion for premium UI

**Why LangGraph for Agents:**
- Durable stateful workflows (critical for long-running pipelines)
- Built-in checkpointing and human-in-the-loop support
- First-class streaming support
- Active development from LangChain team

## Agent Specifications

### Agent A: Job Scout
- **Input:** query string, location, source list
- **Output:** List[JobListing] with dedup hash
- **Sources:** RemoteOK (live), Wellfound (stub), Mock (dev)
- **Pattern:** Adapter pattern for pluggable sources

### Agent B: Match Scorer
- **Input:** JobListing, candidate profile
- **Output:** JobScore (7 dimensions + action recommendation)
- **Modes:** LLM scoring (accurate) / keyword scoring (fast fallback)
- **Thresholds:** ≥85 auto-apply, 70-84 queue, <70 archive

### Agent C: Resume Tailor
- **Input:** JobListing + resume_master.yaml + achievements.yaml
- **Output:** ResumeVariant (tailored bullets, re-ranked sections)
- **Integrity:** No fabrication rule enforced in prompt
- **Variants:** ATS-optimized + polished versions

### Agent D: Cover Letter + Outreach
- **Input:** JobListing + JobScore
- **Output:** OutreachDraft (7 messages: cover letter, recruiter email, HM note, LinkedIn, 3 follow-ups)
- **Style:** Sharp, technical, high-agency founder tone

### Agent G: Interview Prep Coach
- **Input:** JobListing
- **Output:** InterviewPrepPack (company brief, likely questions, STAR stories, talking points)

### Agent H: Portfolio Curator
- **Input:** GitHub username + token
- **Output:** Categorized project cards with recruiter-friendly descriptions
- **Categories:** Agentic Systems, Trading/Quant, Voice AI, Web3/DeFi, Dev Tools, Hackathon

## Database Schema

### Core Tables
- `jobs` — discovered job listings
- `job_scores` — scoring results per job
- `applications` — application tracking
- `resume_variants` — tailored resume versions
- `agent_runs` — audit log of all agent executions

## Security Model
- All secrets via `.env` (never hardcoded)
- Human approval gate before any application submission
- Rate limiting on scraping (respect TOS)
- No hallucinated resume content (hard rule in all prompts)
- Audit trail for every agent action
