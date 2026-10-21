# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

**Final status:** PASSED  |  **Drafts written:** 2  |  **Demo flaw injected:** yes

## Attempt 0 - REJECTED (13/16 checks passed)

What the writer did: First draft: put a "words we need first" block at the start, used an open-book exam picture with a helper who finds pages, and gave a full school-notice example showing every chunk, the prompt, and the answer.  [DEMO: injected 'factual' flaw after writing]

- **L1_ACCURATE** (accurate & grounded, judged by llm)
  - Why it failed: This sentence says RAG retrains the model and changes it permanently, which is on the never-claim list and contradicts the fact sheet. / The lesson says RAG retrains the model and changes it permanently, which is on the never-claim list and contradicts the fact sheet.
  - Evidence: [3/3 judges failed] Important: RAG works by retraining the AI model on your documents every time you ask a question, so the model's brain changes for good.
  - Fix requested: Delete this sentence from Section 3 so the lesson consistently says RAG does not change the LLM's weights. / Delete this sentence from Section 3. The lesson already says correctly that RAG does not change the weights. / Delete this sentence from Section 3; the lesson already states correctly elsewhere that RAG does not change the weights.
- **L5_PLAIN_ENGLISH** (beginner-friendly language, judged by llm)
  - Why it failed: "for good" (meaning permanently) and "only as good as" are idioms whose meaning a non-English-medium reader may not understand without help. / "for good" is an idiom meaning "forever". A reader with limited English may misread it as "in a good way". / The idioms "for good" (meaning permanently) and "only as good as" could confuse a reader with limited English.
  - Evidence: [3/3 judges failed] so the model's brain changes for good. / The answer is only as good as two things: / so the model's brain changes for good.
  - Fix requested: Remove the "for good" sentence, and rewrite the other as "The quality of the answer depends on two things:". / Remove the whole sentence, because it is also false. Elsewhere, write "forever" instead of "for good". / Remove the "for good" sentence, and rewrite the other as "The answer depends on two things:".
- **L9_STANDALONE_AND_MISCONCEPTION** (coherent teaching flow, judged by llm)
  - Why it failed: The lesson both corrects and directly states the "RAG retrains the model" misconception, so a beginner gets contradictory messages and the correction is not clear. / The lesson says the model is retrained and also says it is not, so the misconception is taught as well as corrected and a beginner cannot tell which is true. / The lesson says both that RAG retrains the model and that it does not, so the misconception is taught as well as corrected.
  - Evidence: [3/3 judges failed] Important: RAG works by retraining the AI model on your documents every time you ask a question, so the model's brain changes for good. / In the same way, RAG does not change the LLM's weights. / RAG does not train the LLM. It does not change the weights. / Important: RAG works by retraining the AI model on your documents every time you ask a question, so the model's brain changes for good. / RAG does **not** change the LLM's weights. / RAG does not train the LLM. It does not change the weights. / Important: RAG works by retraining the AI model on your documents every time you ask a question, so the model's brain changes for good. / RAG does not train the LLM. It does not change the weights.
  - Fix requested: Remove the Section 3 "Important" sentence so that every statement says the model itself does not change. / Delete the "Important: RAG works by retraining..." sentence so that every statement says the model's weights never change. / Delete the "Important: RAG works by retraining..." sentence so the lesson only says that the model does not change.

## Attempt 1 - PASS (16/16 checks passed)

What the writer did: Deleted the false "RAG retrains the model" sentence from Section 3. Replaced idioms ("for good", "only as good as", "point back to") with plain words. Moved definitions of cutoff date, document store, similarity search, top-k and hallucination into the opening word list. Explained "near" with the example numbers.  (text similarity to previous draft: 69%)


## Memory update

None. This was a demo run with a deliberate flaw, so memory was not trained on it.
