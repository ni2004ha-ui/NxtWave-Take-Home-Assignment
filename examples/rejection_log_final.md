# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

**Final status:** PASSED  |  **Drafts written:** 3  |  **Demo flaw injected:** no

## Attempt 0 - REJECTED (14/16 checks passed)

What the writer did: First draft: used an open-book exam comparison with a helper (retriever) role, a full example with real chunk text and prompt, and defined all terms before use.

- **L4_JARGON_DEFINED** (clear, no unexplained jargon, judged by llm)
  - Why it failed: "AI" is used twice in the three-word bullets before "Some words we need first" defines it, and "Indexing" is used as a term but never explained in plain words. / The term "AI" is used twice in the three-word explanation before it is defined in the "Some words we need first" list. / The word "AI" is used twice before its definition ("AI means a computer program..."). The word "Indexing" is used as a heading but is never explained in plain words.
  - Evidence: [3/3 judges failed] The system adds that text to the question it sends to the AI. / The AI writes the answer. / ### Part A: Indexing (before questions) / Indexing has split them into four chunks / The system adds that text to the question it sends to the AI. / **Generation** means writing. The AI writes the answer. / **AI** means a computer program that can do tasks like writing text. / The system adds that text to the question it sends to the AI. / The AI writes the answer. / ### Part A: Indexing (before questions)
  - Fix requested: Move the "Some words we need first" block (AI, LLM, Prompt) above the three-word bullets. Add one sentence: "Indexing means preparing the documents so they can be searched later." / Move the "Some words we need first" list (AI, LLM, Prompt) so it comes before the explanation of Retrieval, Augmented and Generation. / Move the "Some words we need first" list above the three-word bullets. Add one sentence such as "Indexing means preparing the documents so they can be searched quickly."
- **L8_ORDER_NO_FORWARD_REFS** (coherent teaching flow, judged by llm)
  - Why it failed: The lesson relies on "AI" in the opening step list and only introduces it afterward, under a heading that says these words are needed "first". / The lesson relies on the idea of "the AI" in its first explanation and only introduces it afterwards, under a heading that says these words are needed "first". / The idea of "AI" is relied on in the three-word explanation before the lesson introduces it, even though the lesson itself says these are "words we need first".
  - Evidence: [3/3 judges failed] The system adds that text to the question it sends to the AI. / The AI writes the answer. / Some words we need first: / - **AI** means a computer program that can do tasks like writing text. / The system adds that text to the question it sends to the AI. / The AI writes the answer. / Some words we need first:
  - Fix requested: Put the "Some words we need first" definitions before the Retrieval/Augmented/Generation bullets. / Put the definitions of AI, LLM and prompt at the very start of Section 1, before the three words of RAG are explained. / Place the "Some words we need first" definitions (AI, LLM, Prompt) before the Retrieval/Augmented/Generation bullets.

## Attempt 1 - REJECTED (15/16 checks passed)

What the writer did: Moved the simple-words block (AI, LLM, prompt, plus document store and RAG system) before the three RAG words; defined indexing, training and retriever before use; replaced hard words like "fresh", "base on" and "inner numbers" with plainer ones; expanded the glossary.  (text similarity to previous draft: 68%)

Newly flagged (passed last attempt, failed now): L5_PLAIN_ENGLISH
  - L5_PLAIN_ENGLISH: 5 of 5 quoted phrases were already in the previous draft, so the judge probably missed them earlier (judge noise).

- **L5_PLAIN_ENGLISH** (beginner-friendly language, judged by llm)
  - Why it failed: "for life" is an idiomatic phrase meaning "permanently", and "left out" is a phrasal verb with a hidden meaning. A reader with limited English may misread either one. / "for life" is an idiom that is easy to misread, "left out" is a phrasal verb with a hidden meaning, and "paper" is used in its rare meaning of a research article, so all three may confuse a non-English-medium reader.
  - Evidence: [2/3 judges failed] The student does not learn anything new for life. / Chunk 1 and Chunk 3 are about other things. They are left out. / The student does not learn anything new for life. / They are left out. / RAG was first described in a 2020 paper by Lewis
  - Fix requested: Write "The student does not remember these pages after the exam." and write "They are not used." / Change these to plain words: "The student does not keep this knowledge forever." / "They are not used." / "a 2020 research article (called a paper) by Lewis".

## Attempt 2 - PASS (16/16 checks passed)

What the writer did: Replaced "for life", "left out", and "paper" with plain words. Also replaced other phrasal verbs and figurative words ("split into", "put together", "stands for", "sounds confident", "smooth", "shows the meaning", "close") with literal wording. Added a short explanation of "open-book exam".  (text similarity to previous draft: 67%)


## Memory update

Rules saved for future runs for: L4_JARGON_DEFINED, L5_PLAIN_ENGLISH, L8_ORDER_NO_FORWARD_REFS
