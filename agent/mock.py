"""Offline stand-in for the models. Tests the pipeline wiring only; it says nothing about real lesson quality."""
import re
from pathlib import Path

GOOD = (Path(__file__).resolve().parent.parent / "tests" / "good_lesson.md").read_text()
BAD_LONG = ("Retrieval-augmented generation is, broadly speaking, a technique in which an information retrieval component "
            "fetches passages that are then concatenated with the original user query before being passed to the model, "
            "which then produces output conditioned on that extended context window.")


class MockLLM:
    def __init__(self):
        self.drafts = 0

    def complete(self, system, user, role="", max_tokens=0):
        if role == "generate":  # first draft is deliberately imperfect: one overly long sentence
            bad = GOOD.replace("## 2.", BAD_LONG + "\n\n## 2.", 1)
            return f"<lesson>{bad}</lesson><changes>First draft written.</changes>"
        if role == "regenerate":
            return f"<lesson>{GOOD}</lesson><changes>Split the very long sentence into short ones.</changes>"
        if role == "judge":
            ids = re.findall(r"\[(L\d_[A-Z_]+)\]", user)
            lesson = user.split("<lesson>")[-1]
            out = []
            for i in ids:
                bad = i == "L1_ACCURATE" and "retraining the AI model" in lesson
                out.append(f'{{"id":"{i}","evidence":"{"retraining the AI model" if bad else "ok"}",'
                           f'"verdict":"{"FAIL" if bad else "PASS"}",'
                           f'"reason":"{"Claims RAG retrains the model" if bad else ""}",'
                           f'"fix":"{"Say the model does not change" if bad else ""}"}}')
            return '{"checks":[' + ",".join(out) + "]}"
        if role == "reflect":
            return "Keep every sentence short; split any sentence with more than 20 words."
        return "- id: X1_MOCK\n  dimension: demo\n  question: Mock proposal.\n  fail_when: Never."
