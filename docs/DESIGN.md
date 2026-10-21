# Design decisions and trade-offs

**Why plain Python, not LangGraph or n8n.** The workflow is one loop with one branch. A graph framework
adds a dependency and hides the control flow without adding capability. In `loop.py` the termination
guarantee is visible: a `for` loop over `max_retries + 1`. If the workflow grew parallel branches or
human-approval pauses, LangGraph would earn its place. Choosing the simpler tool is a decision, not a gap.

**Why a hybrid evaluator.** Some quality properties are countable (sentence length, section presence,
word count). Counting is cheap, identical on every run, and cannot be talked into a pass. Others need
meaning (is the analogy misleading? is a term used before it is explained?). Only a model can judge
those. So 7 checks are code and 9 are judged. Putting everything on the LLM would make the cheap checks
noisy; putting everything in code would make the meaningful checks impossible.

**Why the judge is a different, stronger model than the writer.** A model grading its own writing tends
to approve it (self-preference bias). A separate model with a separate prompt and the adversarial job
"find problems" gives a more independent signal.

**Why evidence before verdict.** The judge must quote the lesson text, then say PASS or FAIL. Quoting
first forces it to look at the actual text, which reduces rubber-stamping, and it makes every verdict
auditable in the rejection log.

**Why hard pass/fail and fail-closed.** No scores means no argument about whether 7/10 is good enough.
Malformed or missing judge output counts as FAIL, so a broken judge can never approve content.

**Why the fact sheet.** "Accurate" cannot be judged by a model from its own memory alone, since that is
the same memory that causes hallucination. The judge compares the lesson to a human-written, versioned
fact sheet with a never-claim list. Limitation: the judge can only catch errors the fact sheet knows about.

**Why max 2 retries and an escalation path.** Retries are bounded so cost and time are bounded. If the
lesson still fails, status is NEEDS_HUMAN_REVIEW and the output carries a banner. The system never
ships what it could not verify.

**Why the rewrite sees the old draft plus reasons.** Regenerating from scratch discards what was good.
The writer gets its previous draft and the exact failures, and is told not to break passing parts.
The loop records regressions (a check that passed before and fails now) so this risk is visible.

**Why the judge votes (found from a real failure).** In a real run the same sentences passed the plain-English
check in one attempt and failed it in the next, so the loop kept chasing "new" failures that were already in
the draft. The log now measures this: for every check that newly fails, it counts how many quoted phrases were
already in the previous draft. The fix is self-consistency: three independent judge passes per attempt.
Subjective checks (wording, flow, analogy) fail only if MORE THAN HALF of the passes object; safety-critical
checks (facts, invented specifics, coverage, the example, the misconception) fail if ANY pass objects, because
a true error should never be voted away. Trade-off: about 3x judge cost. `consistency` measures how flaky the
judge is on a fixed lesson, so the claim "the judge is noisy" is a number, not an impression.

**Self-evolution, and its guardrails.** After a real run, each failure becomes a one-line rule stored in
memory and injected into the next writer prompt; chronic failures are flagged. Two guardrails: runs with
a deliberately injected flaw never update memory (they would teach it false lessons), and the system only
PROPOSES new rubric checks from human feedback. A human approves them. Letting the system rewrite its own
rubric would let it lower its own bar.

**Known limitations (say these in the video).** The judge can be wrong in both directions. Code checks are
proxies: short sentences do not guarantee clarity. A fact sheet covers one topic. Real validation needs a
human reading the lesson and, ideally, a real learner trying it. Memory is a JSON file, fine for one
topic, not for hundreds.
