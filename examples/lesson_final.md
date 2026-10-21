# Introduction to RAG

## 1. What is RAG?

First, some simple words we need.

- **AI** means a computer program that can do tasks like writing text.
- **LLM** means "large language model". It is an AI program that reads and writes text. Many chat programs use an LLM. In this lesson, "the LLM" always means this text-writing program.
- **Prompt** means the text we send to the LLM. It has our question and any extra text.
- **Document store** means a place where we keep many documents. Examples are notices, books, or notes.
- **RAG system** means the whole computer program that does the RAG steps. It works with the LLM.

RAG is short for **Retrieval-Augmented Generation**. The name has three words. Each word is one step.

- **Retrieval** means finding. The RAG system finds useful text in the document store.
- **Augmented** means made larger by adding something. The RAG system adds that text to the prompt.
- **Generation** means writing. The LLM writes the answer.

RAG was first described in a 2020 research article by Lewis and other researchers at Facebook AI Research (now Meta AI).

**An everyday comparison: an open-book exam.** In an open-book exam, students may read books while they write answers.

- The student is the LLM.
- The books and notes are the document store.
- A helper finds the right pages in the books. This helper is called the "retriever". It is the part of the RAG system that finds text.
- The helper gives those pages to the student together with the question.
- The student reads the question and the pages, then writes the answer.

The student does not keep this knowledge after the exam. The student only reads the pages for this one question. RAG works in the same way. RAG does **not** change the LLM. The extra text is only in the prompt, for each question.

## 2. Why do we need RAG?

An LLM learns from a very large amount of text. This learning is called **training**. The text it learns from is called **training data**. This causes three problems.

1. **Knowledge cutoff.** Training data stops at one date, called the cutoff date. The LLM does not know about things after that date.
2. **Private data.** The LLM has not seen private files. Examples are company files, school notices, or your personal notes.
3. **Hallucination.** Sometimes an LLM writes an answer that is well written and sounds sure, but the answer is false. This is called a hallucination.

RAG helps to solve all three problems.

- It gives the LLM new text, so the cutoff date is less of a problem.
- It gives the LLM your private text.
- It gives the LLM real text to use for the answer. This **reduces** hallucination. It does **not** remove it.

There are two more benefits.

- To change what the system knows, you change the document store. You do not need to train the LLM again.
- The answer can show which pieces of text it used. A person can then check the answer.

## 3. How RAG works, step by step

RAG has two parts. The first part is done before anyone asks a question. The second part is done for every question.

### Part A: Indexing (before questions)

**Indexing** means preparing the documents so the system can search them later. It has three steps.

1. **Cut the documents into chunks.** A **chunk** is a small piece of a document, such as a few sentences.
2. **Make an embedding for each chunk.** An **embedding** is a list of numbers that stands for the meaning of a text. Texts with similar meaning get similar numbers. For example, "exam fee" and "cost of the exam" use different words, but they mean almost the same thing. So their numbers will be almost the same.
3. **Store them.** We keep the chunks and their embeddings in a **vector database**. A vector is a list of numbers. So a vector database is a place that stores lists of numbers and can search them fast. A vector database is **not** the LLM. It only stores and finds text.

### Part B: When a question arrives

1. **Retrieve.**
   - Make an embedding of the question.
   - Compare it with the chunk embeddings. This is called a **similarity search**.
   - Choose the **top-k** chunks. This means the k chunks that are most similar to the question. We pick the number k. For example, k = 2 means the best 2 chunks.
2. **Augment.** Join the question and the chosen chunks in one prompt.
3. **Generate.** The LLM reads the prompt and writes the answer from that text.

The search uses meaning. So it can find a chunk even if its words are different from the words in the question.

## 4. One full example

A school adds its notices to a RAG system. These are made-up notices. Indexing has cut them into four chunks:

- Chunk 1: "The school library is open from 9 AM to 4 PM."
- Chunk 2: "The exam fee must be paid by 10 March."
- Chunk 3: "Sports day will be held on 5 February."
- Chunk 4: "The exam fee can be paid at the school office or online."

Each chunk has an embedding in the vector database.

**The student asks:** "When must I pay the exam fee?"

**Step 1: Retrieve.**
- The system makes an embedding of the question.
- It compares that embedding with all four chunks.
- Chunk 2 and Chunk 4 talk about the exam fee. Their meaning is most similar to the question.
- With k = 2, the system chooses Chunk 2 and Chunk 4.
- Chunk 1 and Chunk 3 are about other things. They are not used.

**Step 2: Augment.** The system makes this prompt:

```
Answer the question using only the text below.

Text:
- The exam fee must be paid by 10 March.
- The exam fee can be paid at the school office or online.

Question: When must I pay the exam fee?
```

**Step 3: Generate.** The LLM reads the prompt and writes:

"You must pay the exam fee by 10 March. You can pay at the school office or online."

The system can also show that the answer used Chunk 2 and Chunk 4. The student can read those chunks and check the answer. The LLM was never changed.

## 5. Common mistake to avoid

Many beginners think RAG trains the LLM. Some also think RAG makes every answer correct. Both ideas are wrong.

- RAG does not train the LLM. It does not change the **weights** of the LLM. Weights are the numbers inside the LLM that come from its training. RAG only adds text to the prompt.
- RAG does not remove all mistakes. The answer depends on two things:
  - The documents must be good. Wrong or old documents give wrong answers.
  - The search must find the right chunk. If it finds the wrong chunk, the answer can be wrong.

**Fine-tuning** is a different method. It trains the LLM more, so its weights change. It costs more. It is better for teaching style or skills. For facts that change often, changing the document store is easier.

## 6. Key words (glossary)

- **AI**: A computer program that can do tasks like writing text.
- **LLM**: An AI program that reads and writes text.
- **Prompt**: The text we send to the LLM, with our question and any extra text.
- **Document store**: A place where we keep many documents.
- **RAG**: A method where the system finds useful text, adds it to the prompt, and then the LLM writes the answer.
- **Retriever**: The part of the RAG system that finds useful text.
- **Hallucination**: An answer that is well written and sounds sure, but is false.
- **Indexing**: Preparing the documents before questions, so they can be searched later.
- **Chunk**: A small piece of a document, such as a few sentences.
- **Embedding**: A list of numbers that stands for the meaning of a text. Similar meaning gives similar numbers.
- **Vector database**: A place that stores embeddings and chunks and can search them fast. It is not the LLM.
- **Top-k**: The k chunks that are most similar to the question.
- **Weights**: The numbers inside the LLM that come from its training. RAG does not change them.

## 7. Quick check

1. What do the three words in "Retrieval-Augmented Generation" mean?
2. Name two problems that RAG helps to solve.
3. In the example, why were Chunk 1 and Chunk 3 not used?
4. Does RAG change the LLM's weights? Does it make every answer correct? Explain.
