> **NOT APPROVED.** This draft still failed checks after all retries. A human must review it.

# Introduction to RAG

## 1. What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It is a way to help an AI answer questions better.

First, some basic words:
- **AI** (artificial intelligence) means a computer program that does tasks that normally need human thinking.
- **LLM** (large language model) is an AI program that reads and writes text. Many chat programs that answer questions use an LLM.
- **Prompt** is the text you give to an LLM. It is your question and any extra information.

The three words in RAG mean:
- **Retrieval** means finding. The system finds useful text from a collection of documents.
- **Augmented** means made bigger. The system adds the found text to the prompt.
- **Generation** means writing. The LLM writes the answer.

**An everyday comparison: an open-book exam with a helper.** Think of a student who must answer a question. If the student writes only from memory, the student may forget or guess. Now imagine a library helper sits next to the student. The helper finds the right pages in the books. The helper gives only those pages to the student. The student then writes the answer using those pages.

In RAG, the books are the collection of documents. The helper is the search part of the system. The student is the LLM. The helper finds the text. The LLM does not search.

The name RAG comes from a 2020 research paper by Lewis and others, from Facebook AI Research (now Meta AI).

## 2. Why do we need RAG?

An LLM has limits. RAG helps with three of them.

1. **Knowledge cutoff.** An LLM learns from text during *training*. Training is the time when the model learns from a very large amount of text. That text stops at a certain date, called the cutoff date. The LLM does not know newer things.
2. **Private data.** The LLM has not seen your private files. Examples are company files, school notices, or your own notes.
3. **Hallucination.** Sometimes an LLM writes an answer that sounds very sure and is well written, but the answer is false. This is called hallucination.

RAG gives the LLM the right text at the time of the question. The answer is then based on that text. This makes hallucination **smaller**. It does **not** remove it completely.

There are two more good points:
- To update knowledge, you update the documents. You do not need to train the model again.
- The answer can show which text it used. People can then check it.

## 3. How RAG works, step by step

RAG has two parts. The first part is done before anyone asks a question. The second part is done for every question.

### Part A: Preparing the documents (called indexing)

Indexing means preparing documents so the system can search them quickly.

1. **Split into chunks.** A chunk is a small piece of a document, such as a few sentences. Small pieces are easier to search than a whole book.
2. **Make an embedding for each chunk.** An embedding is a list of numbers that stands for the meaning of a text. A computer program makes it.
3. **Store them.** The chunks and their embeddings are saved in a **vector database**. A vector is a list of numbers. A database is a place that keeps data in an ordered way. So a vector database is a special store that can search these lists of numbers quickly.

A vector database is **not** the LLM. It only stores and finds text. The LLM writes the answer.

### Part B: Answering a question

4. **Retrieve.** The system makes an embedding of the question. Then it does a *similarity search*. This means it finds the chunks whose embeddings are most like the question's embedding. It takes the best matches. The number of chunks it takes is called **top-k**. The letter k is a number you choose. If k is 2, the system takes 2 chunks.
5. **Augment.** The system joins the question and the found chunks into one prompt.
6. **Generate.** The LLM reads the prompt and writes the answer using the chunks.

**What does "similar meaning" mean?** Look at these two questions:
- "What is the last date to pay the fee?"
- "By when must I submit the fee money?"

The words are different, but the meaning is the same. So their embeddings will be almost the same list of numbers. The search works by meaning, not only by exact words.

**RAG does not train the LLM.** The model does not change. The extra text is given only in the prompt, for that one question.

## 4. One full example

Imagine a school has saved its notices in a RAG system. All the notices and answers below are made up. They only show the steps.

**Before any question (indexing):**

The notices are split into four chunks:
- Chunk 1: "The library is open from 9 AM to 4 PM."
- Chunk 2: "Exam fee notice: The exam fee must be paid by 10 March. Pay at the school office."
- Chunk 3: "Sports day is on 20 March. Wear the sports dress."
- Chunk 4: "Fee notice: A student who misses the fee date must meet the class teacher."

Each chunk gets an embedding. All four are stored in the vector database.

**The question:** A student asks, "By when must I pay the exam fee?"

**Step 1: Retrieve.**
- The system makes an embedding of the question.
- It compares this embedding with the four stored embeddings.
- Chunk 2 is the best match, because it is about the exam fee.
- Chunk 4 is the next best match, because it is also about the fee date.
- Here k is 2. So the system takes Chunk 2 and Chunk 4.
- Chunk 1 and Chunk 3 are not about fees. The system does not use them.

**Step 2: Augment.** The system builds this prompt:

> Answer the question using only the notices below.
> Question: By when must I pay the exam fee?
> Notice 1: Exam fee notice: The exam fee must be paid by 10 March. Pay at the school office.
> Notice 2: Fee notice: A student who misses the fee date must meet the class teacher.

**Step 3: Generate.** The LLM reads the prompt and writes this answer:

> You must pay the exam fee by 10 March. Pay at the school office. (Source: exam fee notice)

The LLM had never seen this private notice in training. RAG gave it the notice at the time of the question. The LLM itself did not change.

## 5. Common mistake to avoid

Many beginners think: "RAG teaches the model new facts, and RAG is always right." Both parts are wrong.

- RAG does **not** retrain the model or change it. It only adds text to the prompt.
- RAG does **not** make sure the answer is correct. The answer depends on two things:
  - how good the documents are, and
  - whether the search finds the right chunk.

If the documents are wrong or old, the answer can be wrong. If the search finds the wrong chunk, the answer can also be wrong.

RAG is also different from **fine-tuning**. Fine-tuning means training the model more, so the model itself changes. It costs more. It is better for learning a style or a skill than for facts that change fast.

## 6. Key words (glossary)

- **RAG**: A method where the system finds text, adds it to the prompt, and then the LLM writes the answer.
- **LLM**: An AI program that reads and writes text.
- **Prompt**: The text you give to an LLM, such as a question and extra information.
- **Hallucination**: An answer from an LLM that sounds very sure but is false.
- **Knowledge cutoff**: The date after which the LLM has seen no new text.
- **Indexing**: Preparing documents before any question, so the system can search them quickly.
- **Chunk**: A small piece of a document, such as a few sentences.
- **Embedding**: A list of numbers that stands for the meaning of a text.
- **Vector database**: A store that keeps embeddings and can search them quickly. It is not the LLM.
- **Similarity search**: Finding the chunks whose embeddings are most like the question's embedding.
- **Top-k**: The number of best-matching chunks the system takes. You choose k.
- **Fine-tuning**: Training a model more, so the model itself changes. RAG does not do this.

## 7. Quick check

1. What do the three words *Retrieval*, *Augmented* and *Generation* mean in RAG?
2. Name two problems that RAG helps to solve.
3. What is the job of a vector database? Is it the same as the LLM?
4. Does RAG change the LLM? Does RAG make sure the answer is correct? Give a reason.
