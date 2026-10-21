"""Deliberate error injection for the demo video: proves the evaluator catches real problems."""
import re

FALSE_SENTENCE = ("Important: RAG works by retraining the AI model on your documents every time "
                  "you ask a question, so the model's brain changes for good.")
JARGON_SENTENCE = ("Under the hood, the system uses cosine similarity over HNSW-indexed dense embeddings "
                   "with a cross-encoder reranker.")


def _after_heading(text, heading_regex, insert):
    return re.sub(rf"(?m)^(##\s+{heading_regex}.*\n)", lambda m: m.group(1) + insert + "\n\n", text, count=1)


def inject(lesson: str, kind: str) -> str:
    if kind == "factual":
        return _after_heading(lesson, r"3\.", FALSE_SENTENCE)
    if kind == "jargon":
        return _after_heading(lesson, r"3\.", JARGON_SENTENCE)
    if kind == "no_example":
        return re.sub(r"(?ms)(^##\s+4\..*?\n).*?(?=^##\s+5\.)", r"\1\n", lesson, count=1)
    return lesson


KINDS = ["none", "factual", "jargon", "no_example"]
