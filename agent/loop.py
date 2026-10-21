"""The control loop: generate -> evaluate -> (fail? feed reasons back, regenerate) -> ship or escalate.
Plain Python on purpose: the whole state machine is ~40 lines and always terminates."""
import difflib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from . import flaws, memory, reflect
from .evaluator import evaluate, load_facts, load_rubric, passed
from .generator import generate, regenerate

ROOT = Path(__file__).resolve().parent.parent


def _quotes(evidence):
    ev = re.sub(r"^\[[^\]]*\]\s*", "", evidence)
    return [q for q in (x.strip().strip('"\u201c\u201d').replace("**", "") for x in ev.split(" / ")) if len(q) > 8]


def _diagnose(r, prev_lesson):
    """Was the flagged text already in the previous draft? If so the judge probably missed it earlier (noise),
    rather than the rewrite creating the problem."""
    qs = _quotes(r.evidence)
    prev = prev_lesson.replace("**", "")
    present = sum(1 for q in qs if q in prev)
    return dict(id=r.id, quotes=len(qs), already_in_previous_draft=present)


def _summ(results):
    return [dict(id=r.id, dimension=r.dimension, passed=r.passed, evidence=r.evidence,
                 reason=r.reason, fix=r.fix, source=r.source) for r in results]


def run(topic, gen_llm, judge_llm, max_retries=2, inject=None, log=print, persist=True, judge_samples=1):
    store = memory.load()
    facts, rubric = load_facts(), load_rubric()
    guide = memory.guidance(store)
    attempts, draft, prev_failed = [], "", set()

    for n in range(max_retries + 1):  # attempt 0 is the first draft; max 1 + max_retries drafts total
        if n == 0:
            draft, changes = generate(topic, facts, guide, gen_llm)
            if inject and inject != "none":
                draft = flaws.inject(draft, inject)
                changes += f"  [DEMO: injected '{inject}' flaw after writing]"
        else:
            failures = [r for r in results if not r.passed]
            old = draft
            draft, changes = regenerate(topic, old, failures, facts, guide, gen_llm)
            ratio = difflib.SequenceMatcher(None, old, draft).ratio()
            changes += f"  (text similarity to previous draft: {ratio:.0%})"

        results = evaluate(draft, judge_llm, rubric, facts, samples=judge_samples)
        failed = [r for r in results if not r.passed]
        regress = sorted(r.id for r in failed if r.id not in prev_failed and attempts)
        newly = [_diagnose(r, attempts[-1]["lesson"]) for r in failed if r.id in regress and r.source == "llm"]
        attempts.append(dict(attempt=n, changes=changes, passed=passed(results), results=_summ(results),
                             failed=_summ(failed), failed_ids=[r.id for r in failed],
                             regressions=regress, newly_flagged=newly, lesson=draft))
        log(f"attempt {n}: {len(results) - len(failed)}/{len(results)} checks passed"
            + (f"  FAILED: {', '.join(r.id for r in failed)}" if failed else "  -> PASS"))
        prev_failed = {r.id for r in failed}
        if not failed:
            break

    status = "PASSED" if attempts[-1]["passed"] else "NEEDS_HUMAN_REVIEW"
    record = dict(topic=topic, status=status, attempts_used=len(attempts), synthetic=bool(inject and inject != "none"),
                  finished_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                  final_lesson=draft, attempts=attempts)

    learned = []
    if persist:  # mock runs pass persist=False so fake failures never enter memory
        learned = reflect.learn_from_run(store, record, gen_llm)
        memory.record_run(store, record)
        memory.save(store)
    record["learned"] = learned
    return record


def write_outputs(record, out_dir=None):
    out = Path(out_dir or ROOT / "output")
    out.mkdir(parents=True, exist_ok=True)
    banner = "" if record["status"] == "PASSED" else (
        "> **NOT APPROVED.** This draft still failed checks after all retries. A human must review it.\n\n")
    (out / "lesson.md").write_text(banner + record["final_lesson"] + "\n")
    (out / "rejection_log.md").write_text(render_log(record))
    slim = json.loads(json.dumps(record))
    (out / "run.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False))


def render_log(record):
    L = [f"# Rejection log: {record['topic']}", "",
         f"**Final status:** {record['status']}  |  **Drafts written:** {record['attempts_used']}  |  "
         f"**Demo flaw injected:** {'yes' if record['synthetic'] else 'no'}", ""]
    for a in record["attempts"]:
        total = len(a["results"])
        L += [f"## Attempt {a['attempt']} - {'PASS' if a['passed'] else 'REJECTED'} "
              f"({total - len(a['failed'])}/{total} checks passed)", "",
              f"What the writer did: {a['changes']}", ""]
        if a["regressions"]:
            L += [f"Newly flagged (passed last attempt, failed now): {', '.join(a['regressions'])}"]
            for d in a.get("newly_flagged", []):
                if d["quotes"]:
                    L.append(f"  - {d['id']}: {d['already_in_previous_draft']} of {d['quotes']} quoted phrases were already in the "
                             "previous draft, so " + ("the judge probably missed them earlier (judge noise)."
                             if d["already_in_previous_draft"] * 2 >= d["quotes"] else "the rewrite likely introduced them."))
            L.append("")
        for f in a["failed"]:
            L += [f"- **{f['id']}** ({f['dimension']}, judged by {f['source']})",
                  f"  - Why it failed: {f['reason']}",
                  f"  - Evidence: {f['evidence']}",
                  f"  - Fix requested: {f['fix']}"]
        L.append("")
    if record.get("learned"):
        L += ["## Memory update", "", "Rules saved for future runs for: " + ", ".join(sorted(set(record["learned"]))), ""]
    elif record["synthetic"]:
        L += ["## Memory update", "", "None. This was a demo run with a deliberate flaw, so memory was not trained on it.", ""]
    else:
        L += ["## Memory update", "", "None. Memory was not updated (mock run, or nothing failed).", ""]
    return "\n".join(L)
