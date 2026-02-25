# Scripts

## run_pipeline.py

Run the full Workey job acquisition pipeline.

```bash
# Quick test with mock data (no API keys needed)
python scripts/run_pipeline.py --mock --no-llm

# Full run with real job sources
python scripts/run_pipeline.py --query "AI ML engineer"

# Save results to file
python scripts/run_pipeline.py --mock --output results.json
```

## seed.py

Seed the database with sample data for development.

```bash
python scripts/seed.py
```
