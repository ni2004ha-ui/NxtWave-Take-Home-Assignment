# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

**Final status:** NEEDS_HUMAN_REVIEW  |  **Drafts written:** 3  |  **Demo flaw injected:** no

## Attempt 0 - REJECTED (13/16 checks passed)

What the writer did: First draft: used an open-book exam analogy, a school-notice example followed through all steps, and plain defined terms.

- **L2_NO_INVENTED_SPECIFICS** (accurate & grounded, judged by llm)
  - Why it failed: The product name 'ChatGPT' is a specific name that the fact sheet does not support.
  - Evidence: ChatGPT is one example.
  - Fix requested: Remove the ChatGPT sentence, or replace it with a general description such as 'Many chat programs on phones and websites use an LLM.'
- **L6_RUNNING_EXAMPLE** (teaches by example, judged by llm)
  - Why it failed: The example stays abstract: it never shows the real text of any chunk, which second chunk is taken, the actual prompt, or the actual final answer, so the reader never sees a real answer come out.
  - Evidence: Chunk 2 is about the exam fee. / Say k is 2. Then the system also takes the next closest chunk. / It finds the fee rule in Chunk 2. / It writes an answer using that rule.
  - Fix requested: Give made-up chunk text (for example, Chunk 2: 'Exam fee must be paid by 10 March'), name the second chunk retrieved, show the full prompt, and show the final answer, such as 'You must pay the exam fee by 10 March (source: exam fee notice).'
- **L7_ANALOGY_SOUND** (teaches by example, judged by llm)
  - Why it failed: Because the LLM is the student who finds the pages, the analogy suggests the LLM does the search, but in RAG the retrieval system finds the chunks and only then hands them to the LLM.
  - Evidence: In an open-book exam, the student first finds the right pages in the book. Then the student writes the answer using those pages. RAG works the same way. The LLM is the student.
  - Fix requested: Change the analogy so a helper (the search system) finds the right pages and gives them to the student (the LLM), who then writes the answer using only those pages.

## Attempt 1 - REJECTED (15/16 checks passed)

What the writer did: Removed the ChatGPT name; changed the analogy so a helper finds the pages and the LLM only writes; made the example real with chunk text, the second chunk, the full prompt and the final answer; replaced "smooth" and "close" with plainer words; defined database and fine-tuning.  (text similarity to previous draft: 78%)

Regressions (passed before, failed now): L5_PLAIN_ENGLISH

- **L5_PLAIN_ENGLISH** (beginner-friendly language, judged by llm)
  - Why it failed: The words 'analogy' and 'guarantee', and 'suits' used as a verb, are not explained and may be unknown to a student with limited English vocabulary.
  - Evidence: **Analogy: an open-book exam with a helper.** / RAG does **not** guarantee a correct answer. / Does RAG guarantee a correct answer? Explain. / It suits learning a style or a skill better than facts that change fast.
  - Fix requested: Replace 'Analogy' with 'An everyday comparison', replace 'guarantee' with 'promise' or 'make sure of', and replace 'It suits learning a style' with 'It is better for learning a style'.

## Attempt 2 - REJECTED (15/16 checks passed)

What the writer did: Replaced "analogy", "guarantee" and "suits" with simpler words, and simplified other hard words and phrasal verbs (reduces, organized, left out, put together, quality, explain).  (text similarity to previous draft: 89%)

Regressions (passed before, failed now): L4_JARGON_DEFINED

- **L4_JARGON_DEFINED** (clear, no unexplained jargon, judged by llm)
  - Why it failed: "AI" is used in the first sentence before it is defined, and the word "model" is never directly explained as meaning the LLM, even though later sentences rely on it.
  - Evidence: It is a way to help an AI answer questions better. / **LLM** (large language model) is an AI program that reads and writes text. / Training is the time when the model learns from a very large amount of text. / You do not need to train the model again.
  - Fix requested: Put the AI definition before the sentence "It is a way to help an AI...", and add one line such as: "In this lesson, 'the model' means the LLM."

## Memory update

Rules saved for future runs for: L2_NO_INVENTED_SPECIFICS, L4_JARGON_DEFINED, L5_PLAIN_ENGLISH, L6_RUNNING_EXAMPLE, L7_ANALOGY_SOUND
