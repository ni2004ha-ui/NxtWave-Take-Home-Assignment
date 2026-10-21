"""Deterministic rubric checks. Pure Python: same input, same verdict, every time."""
import re
from dataclasses import dataclass


@dataclass
class Result:
    id: str
    dimension: str
    passed: bool
    evidence: str
    reason: str = ""
    fix: str = ""
    source: str = "code"


REQUIRED = [  # (regex on the section title, human-readable name)
    (r"what is rag", "What is RAG?"),
    (r"why", "Why do we need RAG?"),
    (r"how rag works|how it works", "How RAG works, step by step"),
    (r"example", "One full example"),
    (r"mistake", "Common mistake to avoid"),
    (r"key words|glossary", "Key words (glossary)"),
    (r"quick check", "Quick check"),
]


def sections(text: str):
    parts = re.split(r"(?m)^##\s+", text)
    out = []
    for p in parts[1:]:
        title, _, body = p.partition("\n")
        out.append((title.strip(), body))
    return out


def words(text: str):
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text)


def sentences(text: str):
    sents = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^(?:[-*]\s+|\d+[.)]\s+)", "", line).replace("**", "")
        for s in re.split(r"(?<=[.!?])\s+", line):
            if words(s):
                sents.append(s)
    return sents


def d1_structure(text):
    titles = [t.lower() for t, _ in sections(text)]
    pos, missing = 0, []
    for pattern, name in REQUIRED:
        found = next((i for i in range(pos, len(titles)) if re.search(pattern, titles[i])), None)
        if found is None:
            missing.append(name)
        else:
            pos = found + 1
    return (not missing, f"sections found: {len(titles)}; missing or out of order: {missing or 'none'}",
            "Add or reorder the missing sections: " + ", ".join(missing) if missing else "")


def d2_length(text):
    n = len(words(text))
    ok = 550 <= n <= 1500
    fix = "" if ok else ("Add detail where a beginner would be confused." if n < 550 else "Cut repetition and side-topics.")
    return ok, f"{n} words (allowed 550-1500)", fix


def d3_sentence_length(text):
    sents = sentences(text)
    lens = [len(words(s)) for s in sents]
    avg = sum(lens) / max(len(lens), 1)
    longest = max(sents, key=lambda s: len(words(s))) if sents else ""
    ok = avg <= 16 and max(lens or [0]) <= 28
    fix = "" if ok else f"Split long sentences. Longest ({max(lens)} words): \"{longest[:120]}...\""
    return ok, f"average {avg:.1f} words, longest {max(lens or [0])} words (limits 16 / 28)", fix


def d4_long_words(text):
    toks = [t for w in words(text) for t in w.split("-")]
    long_ = [t for t in toks if len(t) >= 13]
    share = len(long_) / max(len(toks), 1)
    ok = share <= 0.02
    fix = "" if ok else "Replace long words with short ones: " + ", ".join(sorted(set(long_))[:8])
    return ok, f"{share:.1%} of words have 13+ letters (limit 2%)", fix


def _section(text, pattern):
    for t, body in sections(text):
        if re.search(pattern, t.lower()):
            return body
    return ""


def d5_glossary(text):
    body = _section(text, r"key words|glossary")
    n = len(re.findall(r"(?m)^\s*(?:[-*]|\d+[.)])\s+\*\*[^*]+\*\*", body))
    ok = n >= 6
    return ok, f"{n} glossary terms (need 6+)", "" if ok else "Define more terms in the glossary, as '- **Term**: plain-words meaning'."


def d6_example_depth(text):
    n = len(words(_section(text, r"example")))
    ok = n >= 80
    return ok, f"example section has {n} words (need 80+)", "" if ok else "Write the full worked example: one real question, followed through every step."


def d7_quick_check(text):
    body = _section(text, r"quick check")
    n = sum(1 for l in body.splitlines() if "?" in l)
    ok = n >= 3
    return ok, f"{n} questions in Quick check (need 3+)", "" if ok else "Add at least 3 short questions."


CODE_CHECKS = {
    "D1_STRUCTURE": d1_structure,
    "D2_LENGTH": d2_length,
    "D3_SENTENCE_LENGTH": d3_sentence_length,
    "D4_LONG_WORDS": d4_long_words,
    "D5_GLOSSARY": d5_glossary,
    "D6_EXAMPLE_DEPTH": d6_example_depth,
    "D7_QUICK_CHECK": d7_quick_check,
}


def run_code_checks(text, rubric_checks):
    results = []
    for c in rubric_checks:
        if c["type"] != "code":
            continue
        ok, evidence, fix = CODE_CHECKS[c["id"]](text)
        results.append(Result(c["id"], c["dimension"], ok, evidence,
                              reason="" if ok else f"{c['question']} Measured: {evidence}", fix=fix, source="code"))
    return results
