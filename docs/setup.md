# Setup Guide

## Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 14+ (or use Docker Compose)
- Git

## Quick Start (Development)

### 1. Clone and configure

```bash
git clone https://github.com/wildhash/workey.git
cd workey
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies (agents)
cd packages/agents
pip install -e ".[dev]"
cd ../..

# Install API dependencies
cd apps/api
pip install -e ".[dev]"
cd ../..
```

### 3. Start database

```bash
# Option A: Docker
docker compose -f infra/docker-compose.yml up db -d

# Option B: Local PostgreSQL
createdb workey
```

### 4. Start API server

```bash
cd apps/api
python server.py
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 5. Start frontend

```bash
cd apps/web
npm run dev
# Frontend running at http://localhost:3000
```

### 6. Run first job scout

```bash
# Option A: Via worker CLI
cd apps/worker
python main.py --task scout --mock  # Use mock data for testing

# Option B: Via API
curl -X POST http://localhost:8000/api/agents/scout \
  -H "Content-Type: application/json" \
  -d '{"query": "AI ML engineer", "use_mock": true}'
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `OPENAI_API_KEY` | Yes* | OpenAI API key (*or Anthropic) |
| `ANTHROPIC_API_KEY` | No | Anthropic Claude API key |
| `GITHUB_TOKEN` | No | GitHub API token for portfolio sync |
| `GITHUB_USERNAME` | No | GitHub username (default: wildhash) |
| `LLM_PROVIDER` | No | `openai` or `anthropic` (default: openai) |
| `LLM_MODEL` | No | Model name (default: gpt-4o-mini) |

## Docker Compose (Full Stack)

```bash
# Copy and configure env
cp .env.example .env
# Edit .env

# Start all services
docker compose -f infra/docker-compose.yml up -d

# View logs
docker compose -f infra/docker-compose.yml logs -f
```

Services:
- `http://localhost:3000` — Portfolio + Dashboard
- `http://localhost:8000` — API
- `http://localhost:8000/docs` — API docs

## Using Without LLM APIs

The system works without API keys in degraded mode:

1. **Job Scout** — RemoteOK adapter works without API keys
2. **Match Scorer** — Falls back to keyword scoring (no LLM needed)
3. **Resume Tailor** — Requires LLM API key
4. **Cover Letter** — Requires LLM API key

Use `--mock` flag for job scout to test with sample data:
```bash
python apps/worker/main.py --task scout --mock
```
