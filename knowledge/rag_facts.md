# Fact sheet: Retrieval-Augmented Generation (RAG)
This file is the "ground truth" the judge checks the lesson against.
Edit it by hand. Never let the generator edit it.

## What RAG is
- RAG = Retrieval-Augmented Generation. A method where a system first RETRIEVES relevant text
  from an external source, then AUGMENTS the model's prompt with that text, then the LLM GENERATES an answer.
- The term comes from a 2020 paper by Lewis et al. (Facebook AI Research, now Meta AI):
  "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".
- The LLM's weights are NOT changed by RAG. The extra text is only given in the prompt, per question.

## Why it matters
- LLMs only know what was in their training data, which stops at a cutoff date.
- LLMs have not seen private data (company files, school notices, personal notes).
- LLMs can hallucinate: produce fluent, confident, but false statements.
- RAG reduces (does NOT eliminate) hallucination by grounding answers in retrieved text.
- Updating knowledge = updating the document store. No retraining needed.
- Answers can point back to their source chunks, so people can verify them.

## How it works
- Indexing (done before questions): split documents into chunks -> convert each chunk to an embedding
  (a list of numbers capturing meaning) -> store in a vector database / vector index.
- Query time: embed the user's question -> find the top-k most similar chunks (similarity search)
  -> put the question + chunks into the prompt -> LLM writes the answer from that context.
- Similar meaning gives similar embeddings, so search works by meaning, not only exact keywords.

## Must-cover points (the lesson fails "coverage" if any is missing)
1. Definition of RAG and what the three words mean
2. At least two problems RAG solves (knowledge cutoff, private data, hallucination)
3. Chunks, embeddings, and a vector store/database
4. The three runtime steps: retrieve, augment, generate
5. A concrete worked example
6. RAG does not retrain the model

## Never-claim list (instant factual FAIL)
- That RAG retrains or fine-tunes the model, or changes its weights
- That RAG guarantees correct answers or removes all hallucination
- Invented statistics, dates, product claims, or citations not in this sheet
- That a vector database is the same thing as the LLM

## Honest limitations (good to mention briefly)
- Answer quality depends on document quality and on retrieval finding the right chunk.
- Fine-tuning is a different technique: it changes the model's weights, costs more, and suits style/skills better than fast-changing facts.
