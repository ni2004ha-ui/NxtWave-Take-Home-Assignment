"""Writer agent: first draft, and targeted rewrites driven by the evaluator's reasons."""
import re

SYSTEM = """You write beginner lessons for a learner who finished 12th grade in India, studied in a
non-English-medium school, has a small English vocabulary, and has zero AI knowledge.

WRITING RULES
- Short sentences. Aim for 8-14 words. Never more than 25.
- Simple, common words. No idioms, no slang, no phrasal verbs with hidden meaning.
- Use LITERAL words only. Avoid figurative language: words used in a non-literal way (for example "capture the meaning",
  "point to", "meaning space", "only as good as", "under the hood"). Say the plain thing: "show", "depends on".
- If you use an abstract phrase (like "similar meaning"), explain it with a simple everyday example.
- Explain every technical term in plain words the first time it appears.
- Teach with an everyday analogy AND one concrete example that follows a real question through every step.
- Build in order. Never use an idea before you have taught it.
- Use only facts from the FACT SHEET. Do not invent numbers, dates, names or sources.

USE EXACTLY THESE SECTIONS (markdown, in this order):
# Introduction to RAG
## 1. What is RAG?
## 2. Why do we need RAG?
## 3. How RAG works, step by step
## 4. One full example
## 5. Common mistake to avoid
## 6. Key words (glossary)      <- 6 or more lines like: - **Term**: plain-words meaning
## 7. Quick check               <- 3 or 4 short questions, numbered

Output the lesson inside <lesson></lesson> tags. Then, inside <changes></changes>, write one short line
about what you did (first draft) or what you changed (rewrite)."""


def _system(facts, guidance):
    return SYSTEM + "\n\nFACT SHEET:\n" + facts + ("\n\n" + guidance if guidance else "")


def _parse(out):
    lesson = re.search(r"<lesson>(.*?)</lesson>", out, re.S)
    changes = re.search(r"<changes>(.*?)</changes>", out, re.S)
    return (lesson.group(1).strip() if lesson else out.strip(),
            changes.group(1).strip() if changes else "(writer gave no change note)")


def generate(topic, facts, guidance, llm):
    out = llm.complete(_system(facts, guidance), f"Write the lesson. Topic: {topic}", role="generate", max_tokens=4500)
    return _parse(out)


def regenerate(topic, previous, failures, facts, guidance, llm):
    problems = "\n".join(f"- [{r.id}] {r.reason}  Evidence: {r.evidence}  Fix: {r.fix}" for r in failures)
    prompt = (f"Topic: {topic}\n\nHere is your previous draft:\n<lesson>\n{previous}\n</lesson>\n\n"
              f"A strict reviewer REJECTED it. These checks failed:\n{problems}\n\n"
              "Rewrite the lesson to fix every failed check. The reviewer listed examples, but there may be OTHER places with "
              "the same kind of problem: scan the WHOLE lesson and fix all of them. Keep everything that was already good. "
              "Do not break anything that passed. Return the full lesson.")
    out = llm.complete(_system(facts, guidance), prompt, role="regenerate", max_tokens=4500)
    return _parse(out)
