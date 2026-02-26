#!/usr/bin/env python3
"""Run the full Workey pipeline - discover, score, tailor, draft."""
import asyncio
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "agents"))

from dotenv import load_dotenv
load_dotenv()


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run Workey Pipeline")
    parser.add_argument("--query", default="AI ML engineer agent", help="Job search query")
    parser.add_argument("--location", default="remote", help="Location filter")
    parser.add_argument("--mock", action="store_true", help="Use mock job data")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM calls (keyword scoring only)")
    parser.add_argument("--output", help="Save results to JSON file")
    args = parser.parse_args()
    
    use_llm = not args.no_llm and bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    
    if not use_llm:
        print("[Pipeline] No LLM API key found - using keyword scoring only")
        print("[Pipeline] Set OPENAI_API_KEY in .env for full LLM-powered scoring\n")
    
    from workey_agents.pipeline import WorkeyPipeline
    
    pipeline = WorkeyPipeline(use_mock=args.mock, use_llm=use_llm)
    packages = await pipeline.run(query=args.query, location=args.location)
    
    print(f"\n{'='*60}")
    print("PIPELINE RESULTS")
    print('='*60)
    
    for pkg in packages:
        print(f"\n📋 {pkg.job.title} @ {pkg.job.company}")
        print(f"   Score: {pkg.score.total_score}/100 | Action: {pkg.score.action}")
        print(f"   Why: {pkg.score.why_fit[:100]}...")
        if pkg.score.gaps:
            print(f"   Gaps: {', '.join(pkg.score.gaps[:3])}")
        if pkg.resume:
            print(f"   ✅ Resume tailored: '{pkg.resume.headline}'")
        if pkg.outreach:
            print(f"   ✅ Outreach drafted ({len(pkg.outreach.cover_letter)} chars)")
    
    if args.output:
        output_data = [
            {
                "job": pkg.job.model_dump(),
                "score": pkg.score.model_dump(),
                "resume": pkg.resume.model_dump() if pkg.resume else None,
                "outreach": pkg.outreach.model_dump() if pkg.outreach else None,
            }
            for pkg in packages
        ]
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\n[Pipeline] Results saved to {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
