"""EverMemOS - YAML-based persistent memory for Workey agents.

Stores job history, application state, agent learnings, and self-improvement
logs in structured YAML files. Designed for full auditability and human
readability.
"""
from __future__ import annotations
import os
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MEMORY_DIR = Path(os.getenv("WORKEY_MEMORY_DIR", str(
    Path(__file__).parent.parent.parent.parent / "memory"
)))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load_yaml(path: Path) -> dict:
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def _save_yaml(path: Path, data: dict) -> None:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


class EverMemOS:
    """Persistent YAML memory store for Workey's autonomous loop.

    Directory layout:
        memory/
            jobs/              # One YAML per discovered job (keyed by hash)
            applications/      # Application state per job
            learnings/         # Agent self-improvement notes
            runs/              # Pipeline run logs
            scam_intel/        # Scam reports and patterns
            config.yaml        # Runtime config + thresholds
    """

    def __init__(self, root: Path | None = None):
        self.root = root or MEMORY_DIR
        _ensure_dir(self.root)
        self._dirs = {
            "jobs": self.root / "jobs",
            "applications": self.root / "applications",
            "learnings": self.root / "learnings",
            "runs": self.root / "runs",
            "scam_intel": self.root / "scam_intel",
        }
        for d in self._dirs.values():
            _ensure_dir(d)

    # ── Job memory ──
    def remember_job(self, job_hash: str, job_data: dict) -> None:
        path = self._dirs["jobs"] / f"{job_hash}.yaml"
        existing = _load_yaml(path)
        if existing:
            existing.setdefault("seen_count", 0)
            existing["seen_count"] += 1
            existing["last_seen"] = _now()
            _save_yaml(path, existing)
        else:
            job_data["first_seen"] = _now()
            job_data["last_seen"] = _now()
            job_data["seen_count"] = 1
            _save_yaml(path, job_data)

    def was_seen(self, job_hash: str) -> bool:
        return (self._dirs["jobs"] / f"{job_hash}.yaml").exists()

    def get_job(self, job_hash: str) -> dict:
        return _load_yaml(self._dirs["jobs"] / f"{job_hash}.yaml")

    # ── Application state ──
    def save_application(self, job_hash: str, app_data: dict) -> None:
        app_data["updated_at"] = _now()
        app_data.setdefault("created_at", _now())
        _save_yaml(self._dirs["applications"] / f"{job_hash}.yaml", app_data)

    def get_application(self, job_hash: str) -> dict:
        return _load_yaml(self._dirs["applications"] / f"{job_hash}.yaml")

    def list_applications(self, status: str | None = None) -> list[dict]:
        apps = []
        for f in sorted(self._dirs["applications"].glob("*.yaml")):
            data = _load_yaml(f)
            if status is None or data.get("status") == status:
                data["_hash"] = f.stem
                apps.append(data)
        return apps

    # ── Scam intel ──
    def report_scam(self, job_hash: str, report: dict) -> None:
        report["reported_at"] = _now()
        _save_yaml(self._dirs["scam_intel"] / f"{job_hash}.yaml", report)

    def known_scam_hashes(self) -> set[str]:
        return {f.stem for f in self._dirs["scam_intel"].glob("*.yaml")}

    # ── Agent learnings (self-improvement) ──
    def add_learning(self, agent_name: str, learning: dict) -> None:
        path = self._dirs["learnings"] / f"{agent_name}.yaml"
        data = _load_yaml(path)
        data.setdefault("learnings", [])
        learning["timestamp"] = _now()
        data["learnings"].append(learning)
        _save_yaml(path, data)

    def get_learnings(self, agent_name: str) -> list[dict]:
        data = _load_yaml(self._dirs["learnings"] / f"{agent_name}.yaml")
        return data.get("learnings", [])

    # ── Run logs ──
    def log_run(self, run_data: dict) -> str:
        run_id = _now().replace(":", "-").replace("+", "Z")
        run_data["run_id"] = run_id
        run_data["timestamp"] = _now()
        _save_yaml(self._dirs["runs"] / f"{run_id}.yaml", run_data)
        return run_id

    def get_run(self, run_id: str) -> dict:
        return _load_yaml(self._dirs["runs"] / f"{run_id}.yaml")

    def list_runs(self, limit: int = 10) -> list[dict]:
        files = sorted(self._dirs["runs"].glob("*.yaml"), reverse=True)
        return [_load_yaml(f) for f in files[:limit]]

    # ── Stats ──
    def stats(self) -> dict:
        return {
            "total_jobs_seen": len(list(self._dirs["jobs"].glob("*.yaml"))),
            "total_applications": len(list(self._dirs["applications"].glob("*.yaml"))),
            "total_scams_flagged": len(list(self._dirs["scam_intel"].glob("*.yaml"))),
            "total_runs": len(list(self._dirs["runs"].glob("*.yaml"))),
            "memory_dir": str(self.root),
        }
