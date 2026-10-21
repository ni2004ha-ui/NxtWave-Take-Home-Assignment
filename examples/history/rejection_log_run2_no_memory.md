# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

**Final status:** PASSED  |  **Drafts written:** 3  |  **Demo flaw injected:** no

## Attempt 0 - REJECTED (14/16 checks passed)

What the writer did: First draft: wrote all seven sections with short, literal sentences, an open-book analogy, and one school-library example followed through every step.

- **L2_NO_INVENTED_SPECIFICS** (accurate & grounded, judged by llm)
  - Why it failed: The fact sheet does not support the product name 'ChatGPT', and the lesson brings it in as a real-world claim, not as invented example data.
  - Evidence: ChatGPT is one example.
  - Fix requested: Remove 'ChatGPT is one example.' or replace it with a generic description such as 'Chatbots that answer questions are one example.'
- **L4_JARGON_DEFINED** (clear, no unexplained jargon, judged by llm)
  - Why it failed: The heading uses 'Indexing' and only says when it happens, never what the word means in plain words, and the word 'vector' in 'vector database' is never explained.
  - Evidence: ### Part A: Indexing (before questions) / They go into a **vector database**. This is a special store that can search embeddings quickly.
  - Fix requested: Add 'Indexing means preparing the documents so they can be searched quickly later.' and 'A vector is simply a list of numbers, like an embedding.' before or at first use.

## Attempt 1 - REJECTED (14/16 checks passed)

What the writer did: Removed the "ChatGPT" mention. Defined "indexing", "vector", "query time" and "document store" at first use. Replaced "close" embeddings with "almost the same numbers". Changed "computer model" to "computer program" and "at the moment of the question" to "when you ask". Added the new terms to the glossary.  (text similarity to previous draft: 92%)

Regressions (passed before, failed now): L8_ORDER_NO_FORWARD_REFS

- **L4_JARGON_DEFINED** (clear, no unexplained jargon, judged by llm)
  - Why it failed: The AI term "trained" appears in Section 1 with no explanation. The idea that an LLM learns from text only appears in Section 2, and "chatbot" is used without a definition.
  - Evidence: The model is not trained again. / Chatbots that answer questions use LLMs.
  - Fix requested: Before first using "trained", add one sentence such as "Training means the LLM learns by reading a very large amount of text before anyone uses it." Also define chatbot as "a program you can chat with by typing".
- **L8_ORDER_NO_FORWARD_REFS** (coherent teaching flow, judged by llm)
  - Why it failed: Section 1 relies on the idea of training a model before the lesson has said that an LLM learns from text. That idea only comes in Section 2.
  - Evidence: RAG does **not** change the LLM. The model is not trained again. / An LLM learns from text collected up to one date.
  - Fix requested: Move a short explanation of how an LLM learns from text (training) into Section 1, before the sentence "The model is not trained again."

## Attempt 2 - PASS (16/16 checks passed)

What the writer did: Defined "chatbot" and "training" in Section 1 before first use. Linked the cutoff idea in Section 2 to training. Renamed the Part B heading so "query time" is not used before it is explained. Added Chatbot, Training and RAG to the glossary, and explained fine-tuning as extra training.  (text similarity to previous draft: 80%)


## Memory update

Rules saved for future runs for: L2_NO_INVENTED_SPECIFICS, L4_JARGON_DEFINED, L8_ORDER_NO_FORWARD_REFS
