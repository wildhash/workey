# Workey Roadmap

## MVP (Week 1-2) — Working System

### ✅ Foundation
- [x] Monorepo scaffold (Turborepo)
- [x] Data source files (resume, achievements, projects, positioning)
- [x] Shared TypeScript types
- [x] Python agent package with Pydantic schemas

### ✅ Core Agents
- [x] Agent A: Job Scout (RemoteOK + Mock adapters)
- [x] Agent B: Match Scorer (LLM + keyword fallback)
- [x] Agent C: Resume Tailor
- [x] Agent D: Cover Letter + 7-message outreach suite
- [x] Agent G: Interview Prep Coach
- [x] Agent H: Portfolio Curator

### ✅ Backend API
- [x] FastAPI with async SQLAlchemy
- [x] Jobs CRUD + status tracking
- [x] Applications tracking
- [x] Agent run triggers
- [x] Portfolio sync endpoint

### ✅ Frontend
- [x] Portfolio homepage (Hero, Projects, Skills, Contact)
- [x] Dashboard (Command Center with pipeline Kanban)
- [x] Responsive design with dark theme

### ✅ Infrastructure
- [x] Docker Compose for local dev
- [x] Dockerfiles for each service
- [x] Environment configuration

## Phase 2 (Week 3-4) — Enhanced Features

### Job Sources
- [ ] Wellfound adapter (with Playwright auth)
- [ ] LinkedIn adapter (careful TOS compliance)
- [ ] Y Combinator jobs scraper
- [ ] Greenhouse/Lever API integrations

### Email Integration
- [ ] Gmail OAuth2 setup
- [ ] Agent F: Inbox Sentinel (classify emails)
- [ ] Recruiter thread detection
- [ ] Daily digest generation

### Application Runner
- [ ] Agent E: Playwright-assisted applications
- [ ] ATS field detection (Greenhouse, Lever, Ashby)
- [ ] Screenshot + receipt storage
- [ ] Human approval UI in dashboard

### Dashboard Enhancements
- [ ] Live data from API (replace static placeholders)
- [ ] Job cards in Kanban columns
- [ ] Score breakdown visualization
- [ ] Application timeline view

## Phase 3 (Month 2) — Scale & Polish

### Voice & Avatar
- [ ] LiveKit integration scaffold
- [ ] Voice interview practice mode
- [ ] Real-time avatar UI

### Portfolio Automation
- [ ] Auto-generate case study pages from READMEs
- [ ] Commit activity → portfolio updates
- [ ] "What I'm building now" feed

### Analytics
- [ ] Application funnel metrics
- [ ] Response rate tracking
- [ ] Score distribution charts
- [ ] A/B testing cover letter variants

### Productization
- [ ] Multi-user support
- [ ] SaaS billing integration
- [ ] White-label portfolio sites
- [ ] Team collaboration features

## 30/60/90 Day Plan

### Day 30 — Operational
- Full pipeline running daily
- 50+ jobs scored
- 10+ tailored applications sent
- Portfolio site live

### Day 60 — Optimized
- Gmail integration live
- Response rate measured and improving
- 3+ interviews from system-generated outreach
- Portfolio driving inbound

### Day 90 — Income
- First offer or contract from system
- System refined for efficiency
- Documented for potential SaaS pivot
- 2+ paying consulting clients from portfolio leads
