import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ["MEMORY_PATH"] = os.path.join(tempfile.mkdtemp(), "store.json")

from agent import checks, flaws, loop, memory
from agent.evaluator import load_rubric
from agent.mock import MockLLM, GOOD

RUBRIC = load_rubric()


def code_results(text):
    return {r.id: r.passed for r in checks.run_code_checks(text, RUBRIC)}


def test_good_lesson_passes_all_code_checks():
    assert all(code_results(GOOD).values()), code_results(GOOD)


def test_missing_example_is_caught():
    assert code_results(flaws.inject(GOOD, "no_example"))["D6_EXAMPLE_DEPTH"] is False


def test_long_sentence_is_caught():
    from agent.mock import BAD_LONG
    assert code_results(GOOD.replace("## 2.", BAD_LONG + "\n\n## 2.", 1))["D3_SENTENCE_LENGTH"] is False


def test_loop_retries_then_passes():
    m = MockLLM()
    rec = loop.run("Introduction to RAG", m, m, max_retries=2, log=lambda *_: None)
    assert rec["status"] == "PASSED" and rec["attempts_used"] == 2
    assert "D3_SENTENCE_LENGTH" in rec["attempts"][0]["failed_ids"]


def test_injected_factual_error_is_caught_and_memory_untouched():
    m = MockLLM()
    before = memory.load()["patches"].copy()
    rec = loop.run("Introduction to RAG", m, m, max_retries=2, inject="factual", log=lambda *_: None)
    assert "L1_ACCURATE" in rec["attempts"][0]["failed_ids"] and rec["status"] == "PASSED"
    assert rec["synthetic"] and memory.load()["patches"] == before


def test_loop_always_terminates_and_escalates():
    class AlwaysBad(MockLLM):
        def complete(self, system, user, role="", max_tokens=0):
            if role == "regenerate":
                role = "generate"
            return super().complete(system, user, role, max_tokens)
    m = AlwaysBad()
    rec = loop.run("x", m, m, max_retries=2, log=lambda *_: None)
    assert rec["attempts_used"] == 3 and rec["status"] == "NEEDS_HUMAN_REVIEW"
