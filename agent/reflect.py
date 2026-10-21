"""Self-evolution. After a REAL run, turn each failure into one short rule for the writer's prompt.
After human feedback, propose NEW rubric checks (saved as candidates; a human approves them)."""
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

EVOLVE_SYSTEM = ("You improve a lesson-quality rubric. Given human feedback, propose up to 3 NEW hard pass/fail checks "
                 "as YAML list items with keys: id, dimension, question, fail_when. Output only YAML.")


MERGE_SYSTEM = ("You maintain ONE short rule that stops a lesson-writing mistake. Given the existing rule (may be empty) "
                "and new failures, write ONE updated rule, max 45 words, imperative. Cover the whole CATEGORY of mistake, "
                "not only the latest example, and keep one or two short example words from the failures. Output only the rule.")


def learn_from_run(store, record, llm):
    if record["synthetic"]:
        return []  # injected flaws are a demo, not a real weakness of the writer
    by_id = {}
    for att in record["attempts"]:
        for f in att["failed"]:
            by_id.setdefault(f["id"], []).append(f)
    learned = []
    for cid, fails in by_id.items():
        entry = store["patches"].get(cid, {"fail_count": 0, "rule": ""})
        entry["fail_count"] += 1  # counted once per RUN, however many attempts failed it
        store["fail_counts"][cid] = store["fail_counts"].get(cid, 0) + 1
        details = "\n".join(f"- Reason: {f['reason']} | Evidence: {f['evidence']} | Fix: {f['fix']}" for f in fails)
        entry["rule"] = llm.complete(MERGE_SYSTEM,
                                     f"Check: {cid}\nExisting rule: {entry['rule'] or '(none)'}\nNew failures:\n{details}",
                                     role="reflect", max_tokens=200).strip()
        store["patches"][cid] = entry
        learned.append(cid)
    return learned


def evolve_rubric(store, llm):
    if not store["feedback"]:
        return "No human feedback stored yet. Add some with: python -m agent.cli feedback \"...\""
    notes = "\n".join(f"- {f['text']}" for f in store["feedback"])
    out = llm.complete(EVOLVE_SYSTEM, f"Human feedback on past lessons:\n{notes}", role="evolve", max_tokens=800)
    path = Path(os.getenv("CANDIDATES_PATH", ROOT / "memory" / "candidate_checks.yaml"))
    path.write_text(out.strip() + "\n")
    return f"Saved proposed checks to {path}. Review them, then copy good ones into rubric.yaml."
