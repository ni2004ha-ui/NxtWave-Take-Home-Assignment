# Self-Evaluating Lesson Generator (RAG)

An agentic loop that writes a beginner lesson, grades it against a hard pass/fail rubric,
rewrites it using the judge's reasons, and only ships what passes. It remembers its failures across runs.

```
topic -> GENERATE -> EVALUATE (7 code checks + 9 judge checks) -> all pass? -> ship
                        ^                       | no (max 2 retries)
                        +---- feed reasons ----+        still failing? -> NEEDS_HUMAN_REVIEW (never silently shipped)
after every real run: failures -> one-line rules -> memory/store.json -> injected into the next run's writer prompt
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                   # then paste your ANTHROPIC_API_KEY into .env
```

## Run
```bash
python -m agent run                                    # real run, writes output/lesson.md + output/rejection_log.md
python -m agent run --inject-flaw factual              # DEMO: plants a false claim; watch the judge catch it
python -m agent run --inject-flaw jargon               # DEMO: plants unexplained jargon
python -m agent run --inject-flaw no_example           # DEMO: deletes the worked example
python -m agent run --judge-samples 1                  # cheaper: one judge pass per attempt (default 3, combined by vote)
python -m agent consistency examples/lesson.md --n 5   # measure judge reliability: judge the SAME file 5 times
python -m agent run --mock                             # no API key, tests the wiring only
python -m agent feedback "Analogy felt too long"       # store human feedback in memory
python -m agent evolve                                 # turn feedback into PROPOSED new rubric checks
python -m agent memory                                 # see what the system has learned
pytest -q                                              # ~60 tests, no API needed, never reads .env
```

## Files
- `rubric.yaml`  the 16 pass/fail checks (the thing you will defend in the video)
- `knowledge/rag_facts.md`  the ground truth the judge grades accuracy against
- `agent/checks.py`  deterministic checks   |  `agent/evaluator.py`  hybrid evaluator + judge prompt
- `agent/generator.py`  writer prompts   |  `agent/loop.py`  the control loop and rejection log
- `agent/memory.py`, `agent/reflect.py`  persistence and self-evolution
- `docs/DESIGN.md`  why it is built this way
