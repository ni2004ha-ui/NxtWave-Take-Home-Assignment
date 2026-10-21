"""Persistent memory across runs. A plain JSON file: easy to read, diff, and explain in a video.
 - patches:   one short rule per rubric check, learned from past failures, injected into the writer's prompt
 - fail_counts: how often each check has failed across REAL runs (chronic failures get top priority)
 - feedback:  notes from a human reviewer, turned into candidate rubric checks by `python -m agent.cli evolve`
 - runs:      short history of every run
Runs with a deliberately injected flaw are logged but never taught to memory (they would poison it)."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = Path(os.getenv("MEMORY_PATH", ROOT / "memory" / "store.json"))
EMPTY = {"patches": {}, "fail_counts": {}, "feedback": [], "runs": []}


def load():
    if PATH.exists():
        return {**EMPTY, **json.loads(PATH.read_text())}
    return json.loads(json.dumps(EMPTY))


def save(store):
    PATH.parent.mkdir(parents=True, exist_ok=True)
    PATH.write_text(json.dumps(store, indent=2, ensure_ascii=False))


def guidance(store, limit=8):
    """Rules for the writer prompt, most-failed first."""
    items = sorted(store["patches"].items(), key=lambda kv: -kv[1].get("fail_count", 0))[:limit]
    if not items:
        return ""
    out = ["LESSONS LEARNED FROM PAST RUNS (follow these):"]
    for cid, p in items:
        tag = " [CHRONIC - failed 3+ times]" if p.get("fail_count", 0) >= 3 else ""
        out.append(f"- {p['rule']}{tag}")
    for f in store["feedback"][-3:]:
        out.append(f"- Human reviewer said: {f['text']}")
    return "\n".join(out)


def add_feedback(store, text):
    store["feedback"].append({"text": text, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})


def record_run(store, record):
    store["runs"].append({k: record[k] for k in ("topic", "status", "attempts_used", "synthetic", "finished_at")}
                         | {"first_try_failures": record["attempts"][0]["failed_ids"]})
    store["runs"] = store["runs"][-50:]
