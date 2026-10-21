# Introduction to RAG

## 1. What is RAG?

**AI** means Artificial Intelligence. These are computer programs that do tasks that usually need human thinking.

An **LLM** is one kind of AI program. It reads and writes text. LLM means Large Language Model. AI chat tools use an LLM to write their answers.

RAG means **Retrieval-Augmented Generation**. Let us learn the three words.

- **Retrieval** means finding. The system finds useful text from a collection of documents.
- **Augmented** means made bigger or better. The system adds that text to your question.
- **Generation** means writing. The LLM writes an answer.

So RAG is a method with three steps. First, find useful text. Second, add it to the question. Third, let the LLM write the answer.

The name comes from a 2020 research paper by Lewis and others at Facebook AI Research.

**An everyday analogy: the open-book exam.**
Think of a student in an exam. In a closed-book exam, the student uses only memory. In an open-book exam, the student looks at the right page and then writes the answer.

An LLM without RAG is like the closed-book student. An LLM with RAG is like the open-book student. The student does not become smarter. The student only reads the right page at the right time.

## 2. Why do we need RAG?

An LLM learns from text. This text is called its **training data**. RAG helps with three problems.

**Problem 1: The knowledge cutoff.**
Training data stops at one date. This date is called the **cutoff date**. The LLM does not know anything that happened after it.

**Problem 2: Private data.**
The LLM has not seen your private files. These can be company files, school notices, or your own notes. It cannot answer questions about them.

**Problem 3: Hallucination.**
Sometimes an LLM writes a false answer. It still sounds confident and correct. This is called **hallucination**.

RAG gives the LLM real text to read before it answers. This is called **grounding**. Grounding means basing the answer on real text. It reduces hallucination. But it does not remove it completely.

RAG has two more benefits:

- To update knowledge, you only update your documents. You do not need to train the LLM again.
- The system can show the pieces of text it used. People can then check the source.

## 3. How RAG works, step by step

RAG has two parts. The first part is done before anyone asks a question. The second part is done every time someone asks.

### Part A: Indexing (preparing the documents)

**Indexing** means preparing the documents and storing them. We do this so we can search them later. It has three steps.

**Step 1: Split into chunks.**
A **chunk** is a small piece of a document. A long document is cut into many chunks. Each chunk is short and has one main idea.

**Step 2: Make an embedding for each chunk.**
A **vector** is a list of numbers. An **embedding** is a vector that shows the meaning of a text. Texts with similar meaning get similar numbers.

Think of a map of ideas. Two shops close together on a city map are near each other. In the same way, texts with similar meaning are placed close together on this imaginary map. Texts with different meaning are placed far apart.

**Step 3: Store the embeddings.**
We keep all embeddings in a **vector database**. This is a special store. It is built to find similar embeddings quickly. It is *not* the LLM. It only stores and searches. It does not write answers.

### Part B: Question time (runtime)

**Runtime** means the time when the system is answering a question. A **query** is the user's question. At runtime, three steps happen.

**Step 4: Retrieve.**
The system makes an embedding of the question. It compares this with the stored chunk embeddings. This is called **similarity search**. It picks the **top-k** chunks. This means the best few matches. Here *k* is just a number, such as "the best three".

The search uses meaning. So it does not need exactly the same words. A question can use different words from the document and still find the right chunk.

**Step 5: Augment.**
A **prompt** is the text we send to the LLM. The system joins the question and the chosen chunks in one prompt.

**Step 6: Generate.**
The LLM reads the prompt. It writes an answer using the chunks as its source.

**Important:** RAG does not change the LLM. It does not retrain it. The extra text goes only into the prompt, for that one question.

## 4. One full example

This is an imaginary example. A school puts its notices into a RAG system.

**Before questions (indexing):**

1. The school has a long notice about the library. The system splits it into chunks.
2. One chunk says: "The library is open on weekdays and Saturday morning. It is closed on Sunday."
3. Another chunk says: "Students can borrow books for two weeks." *(This chunk is about borrowing, not about days.)*
4. The system makes an embedding for each chunk. It stores them in the vector database.

**A student asks:** "Can I go to the library on Sunday?"

1. **Retrieve:** The system makes an embedding of the question. It searches the vector database. The chunk about library days is closest in meaning. It is chosen as a top match.
2. **Augment:** The system builds a prompt. It has the student's question and the chosen chunk.
3. **Generate:** The LLM reads the prompt. It writes: "No. The library is closed on Sunday. It is open on weekdays and Saturday morning."

The LLM never saw this notice during its training. It still answered correctly. This is because RAG gave it the right text at the right time. The system can also show the chunk it used. The student can then check it.

## 5. Common mistake to avoid

**Mistake 1: "RAG teaches the model new things."**
This is wrong. RAG does not retrain the model. It does not change the model at all. It only adds text to the prompt for each question.

Fine-tuning is a different method. It *does* change the model. It costs more. It is better for style and skills than for facts that change often.

**Mistake 2: "RAG always gives correct answers."**
This is also wrong. RAG reduces hallucination. It does not remove it. The quality of the answer depends on two things:

- The quality of your documents. Wrong documents give wrong answers.
- The retrieval step. If it finds the wrong chunk, the answer can be wrong.

## 6. Key words (glossary)

- **AI**: Artificial Intelligence. Computer programs that do tasks that usually need human thinking.
- **LLM**: A kind of AI program that reads and writes text. The name means Large Language Model.
- **RAG**: A method that finds useful text, adds it to the prompt, and then lets the LLM write an answer.
- **Training data**: The text the LLM learned from. It stops at a cutoff date.
- **Hallucination**: A false answer that sounds confident and correct.
- **Grounding**: Basing the answer on real text that was found.
- **Indexing**: Preparing documents and storing them, so they can be searched later.
- **Chunk**: A small piece of a longer document.
- **Vector**: A list of numbers.
- **Embedding**: A vector that shows the meaning of a text.
- **Vector database**: A special store that keeps embeddings and finds similar ones. It is not the LLM.
- **Similarity search**: Finding the stored embeddings that are closest in meaning to the question.
- **Top-k**: The best few matching chunks. The number k tells how many.
- **Prompt**: The text we send to the LLM. It includes the question and the chosen chunks.
- **Runtime**: The time when the system is answering a question.

## 7. Quick check

1. What do the three words in Retrieval-Augmented Generation mean?
2. Name two problems that RAG helps to solve.
3. What is the difference between a chunk and an embedding?
4. Does RAG change or retrain the LLM? Explain in one sentence.
