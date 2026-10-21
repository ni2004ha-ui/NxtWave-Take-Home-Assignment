import argparse
import os
import sys

from . import memory, reflect
from .flaws import KINDS
from .llm import get_models
from .loop import run, write_outputs

if not os.getenv("AGENT_NO_DOTENV"):  # tests set this so a real .env can never leak a key into them
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass


def _run_checked(a, gen, judge):
    return run(a.topic, gen, judge, max_retries=max(0, min(a.max_retries, 2)),
               inject=a.inject_flaw, persist=not a.mock,
               judge_samples=max(1, min(a.judge_samples, 5)))


def _friendly(e):
    name = type(e).__name__
    msg = str(e)
    if name == "AuthenticationError":
        return "API key rejected. Check ANTHROPIC_API_KEY in your .env file (no quotes, no spaces)."
    if name == "NotFoundError":
        return ("Model not found. Your account may not have access to that model. Set GEN_MODEL and JUDGE_MODEL "
                "in .env to models you can use (see console.anthropic.com).\nDetails: " + msg[:200])
    if name == "PermissionDeniedError":
        return "Permission denied for that model or key. Details: " + msg[:200]
    if name == "RateLimitError":
        return "Rate limited. Wait a minute and run again."
    if name in ("APIConnectionError", "APITimeoutError"):
        return "Could not reach the API. Check your internet connection and try again."
    if "credit balance" in msg.lower():
        return "Your Anthropic credit balance is too low. Add credit at console.anthropic.com (Billing)."
    return f"Run failed: {name}: {msg[:300]}"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agent")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="generate, evaluate, regenerate, and write the outputs")
    r.add_argument("--topic", default="Introduction to RAG (Retrieval-Augmented Generation)")
    r.add_argument("--max-retries", type=int, default=2, help="1 or 2 recommended; the loop always stops")
    r.add_argument("--inject-flaw", choices=KINDS, default="none", help="demo: plant a deliberate error")
    r.add_argument("--judge-samples", type=int, default=int(os.getenv("JUDGE_SAMPLES", "3")),
                   help="independent judge passes per attempt, combined by vote (1 = cheapest, 3 = steadier)")
    r.add_argument("--mock", action="store_true", help="no API calls; tests the pipeline only")
    r.add_argument("--out", default=None)

    f = sub.add_parser("feedback", help="store a human reviewer's note in memory")
    f.add_argument("text")

    c = sub.add_parser("consistency", help="measure judge reliability: judge the SAME lesson file N times")
    c.add_argument("file")
    c.add_argument("--n", type=int, default=5)

    sub.add_parser("evolve", help="turn stored human feedback into proposed new rubric checks")
    sub.add_parser("memory", help="show what memory has learned")

    a = ap.parse_args(argv)

    if a.cmd == "run":
        if not a.mock and not os.getenv("ANTHROPIC_API_KEY"):
            sys.exit("Set ANTHROPIC_API_KEY (see .env.example), or use --mock to test without it.")
        gen, judge = get_models(a.mock)
        try:
            rec = _run_checked(a, gen, judge)
        except Exception as e:
            sys.exit(_friendly(e))
        write_outputs(rec, a.out)
        print(f"\nStatus: {rec['status']}  |  drafts: {rec['attempts_used']}  |  files in output/")
        return
    elif a.cmd == "consistency":
        if not os.getenv("ANTHROPIC_API_KEY"):
            sys.exit("consistency needs a real judge. Set ANTHROPIC_API_KEY first.")
        from concurrent.futures import ThreadPoolExecutor
        from .evaluator import evaluate, load_facts, load_rubric
        _, judge = get_models(False)
        text, rub, facts = open(a.file).read(), load_rubric(), load_facts()
        n = max(2, min(a.n, 10))
        with ThreadPoolExecutor(max_workers=n) as ex:
            runs = [f.result() for f in [ex.submit(evaluate, text, judge, rub, facts, 1) for _ in range(n)]]
        print(f"Same lesson judged {n} times by one judge. A reliable check passes {n}/{n} or fails {n}/{n}.\n")
        for r0 in runs[0]:
            if r0.source != "llm":
                continue
            ps = sum(1 for run in runs for r in run if r.id == r0.id and r.passed)
            flag = "" if ps in (0, n) else "   <-- INCONSISTENT"
            print(f"  {r0.id:34s} passed {ps}/{n}{flag}")
    elif a.cmd == "feedback":
        s = memory.load(); memory.add_feedback(s, a.text); memory.save(s); print("Saved.")
    elif a.cmd == "evolve":
        if not os.getenv("ANTHROPIC_API_KEY"):
            sys.exit("evolve needs a real model. Set ANTHROPIC_API_KEY first.")
        gen, _ = get_models(mock=False)
        print(reflect.evolve_rubric(memory.load(), gen))
    elif a.cmd == "memory":
        s = memory.load()
        print("Learned rules:")
        for k, v in s["patches"].items():
            print(f"  {k} (failed {v['fail_count']}x): {v['rule']}")
        print(f"Runs logged: {len(s['runs'])}  |  Human feedback notes: {len(s['feedback'])}")


if __name__ == "__main__":
    main()
