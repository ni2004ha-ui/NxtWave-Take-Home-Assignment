# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

**Final status:** PASSED  |  **Drafts written:** 2  |  **Demo flaw injected:** yes

## Attempt 0 - REJECTED (11/16 checks passed)

What the writer did: First draft: used an open-book analogy and a school-notice example, defined each term before use, and used plain words with no idioms.  [DEMO: injected 'factual' flaw after writing]

- **L1_ACCURATE** (accurate & grounded, judged by llm)
  - Why it failed: This sentence is on the never-claim list because it says RAG retrains the model and changes it permanently, and it contradicts the fact sheet and the rest of the lesson.
  - Evidence: "Important: RAG works by retraining the AI model on your documents every time you ask a question, so the model's brain changes for good."
  - Fix requested: Delete this sentence, or replace it with: "Important: RAG does not retrain the model. It only adds extra text to the prompt for each question."
- **L2_NO_INVENTED_SPECIFICS** (accurate & grounded, judged by llm)
  - Why it failed: The product name "ChatGPT" does not appear in the fact sheet, so the fact sheet does not support it.
  - Evidence: "An **LLM** (large language model) is an AI program that reads and writes text. ChatGPT is one example."
  - Fix requested: Remove "ChatGPT is one example." or replace it with a generic description, such as "for example, a chat program that answers questions."
- **L5_PLAIN_ENGLISH** (beginner-friendly language, judged by llm)
  - Why it failed: "For good" is an idiom meaning "permanently", and a reader with limited English may not know it.
  - Evidence: "so the model's brain changes for good."
  - Fix requested: Remove the sentence, because it is also false. If any similar idea is kept, write "permanently" or "forever" instead of "for good".
- **L8_ORDER_NO_FORWARD_REFS** (coherent teaching flow, judged by llm)
  - Why it failed: This sentence relies on retraining and on the model's inner 'brain' (weights) before weights are explained in Part B, and it puts a confusing claim ahead of the step-by-step explanation.
  - Evidence: "Important: RAG works by retraining the AI model on your documents every time you ask a question, so the model's brain changes for good."
  - Fix requested: Remove the sentence so that Section 3 starts directly with "RAG has two parts."
- **L9_STANDALONE_AND_MISCONCEPTION** (coherent teaching flow, judged by llm)
  - Why it failed: The lesson states the misconception as fact and then contradicts it, so it does not clearly correct the "RAG retrains the model" misunderstanding.
  - Evidence: "Important: RAG works by retraining the AI model on your documents every time you ask a question" vs. "**RAG does not train the LLM again.**... RAG does not change the weights."
  - Fix requested: Delete the "Important: RAG works by retraining..." sentence so that the lesson says consistently that the model does not change.

## Attempt 1 - PASS (16/16 checks passed)

What the writer did: Deleted the false sentence saying RAG retrains the model, so Section 3 now starts with "RAG has two parts." Removed the "ChatGPT" example and used a generic description instead. Kept everything else the same.  (text similarity to previous draft: 98%)


## Memory update

None. This was a demo run with a deliberate flaw, so memory was not trained on it.
