# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

**Final status:** PASSED  |  **Drafts written:** 3  |  **Demo flaw injected:** no

## Attempt 0 - REJECTED (14/16 checks passed)

What the writer did: First draft: used the open-book exam analogy and a school library example that follows one question through retrieve, augment and generate, and covered all must-cover points and the limitations.

- **L4_JARGON_DEFINED** (clear, no unexplained jargon, judged by llm)
  - Why it failed: Several technical terms are used without a plain explanation: the word "vector" is never explained, "runtime" is never explained, "indexing" is only labelled "(before questions)", and "AI" is never defined.
  - Evidence: "We keep all embeddings in a **vector database**." / "Now the three runtime steps happen." / "### Part A: Indexing (before questions)" / "It is the 'brain' behind AI chat tools."
  - Fix requested: Add short definitions: "A vector is a list of numbers, like an embedding", "Runtime means the time when the system is answering a question", "Indexing means preparing and storing the documents so they can be searched later", and "AI (Artificial Intelligence) means computer programs that do tasks that usually need human thinking".
- **L5_PLAIN_ENGLISH** (beginner-friendly language, judged by llm)
  - Why it failed: "Capture the meaning" is a figurative phrase, and "meaning space" is an unexplained abstract phrase that a reader with limited English may not understand.
  - Evidence: "The numbers capture the meaning of the text." / "two texts with similar meaning are near each other in 'meaning space'."
  - Fix requested: Rewrite as "The numbers show the meaning of the text" and either explain "meaning space" as "an imaginary map where texts with similar meaning are placed close together" or remove the phrase.

## Attempt 1 - REJECTED (15/16 checks passed)

What the writer did: Added plain definitions for AI, vector, indexing and runtime. Replaced "capture the meaning" with "show the meaning". Replaced "meaning space" with a simple map-of-ideas explanation. Added "grounding" to the glossary. Kept everything else the same.  (text similarity to previous draft: 89%)

- **L5_PLAIN_ENGLISH** (beginner-friendly language, judged by llm)
  - Why it failed: The idiom "only as good as" and the phrase "point to" (meaning "show which") carry hidden meanings that a reader with limited English may misread.
  - Evidence: "The answer is only as good as two things:" / "The answer can point to the pieces of text it used."
  - Fix requested: Replace them with "The quality of the answer depends on two things:" and "The system can show the pieces of text it used."

## Attempt 2 - PASS (16/16 checks passed)

What the writer did: Replaced "point to" with "show" and "only as good as" with "depends on"; also changed "look at the three words" to "learn" and "puts together" to "joins" to remove other hidden-meaning phrases.  (text similarity to previous draft: 99%)


## Memory update

Rules saved for future runs for: L4_JARGON_DEFINED, L5_PLAIN_ENGLISH
