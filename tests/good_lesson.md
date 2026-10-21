# Introduction to RAG

## 1. What is RAG?
RAG stands for Retrieval-Augmented Generation. It is a way to help an AI chatbot give better answers. First, the system looks for useful information. Then the chatbot uses that information to write its answer.

Think about an open-book exam. In a closed-book exam, you must answer only from memory. In an open-book exam, you can look at your book first. Then you write your answer. RAG gives the AI an open book.

The chatbot is powered by a Large Language Model, or LLM. An LLM is a computer program that learned to read and write by studying a huge amount of text. It can answer questions. But it only knows what it saw while it was studying.

## 2. Why do we need RAG?
An LLM has three problems.

First, its knowledge has an end date. It does not know anything that happened after its study time ended.

Second, it does not know your private information. It has never seen your school notices, your company files, or your own notes.

Third, it can make mistakes and sound very sure. This is called a hallucination. A hallucination is an answer that sounds correct but is false.

RAG helps with all three problems. The system finds the right text from a trusted source. It gives that text to the AI. The AI then answers from that text. You can update the source at any time, so the answer stays fresh. You can also check the source, so you can trust the answer more. RAG does not remove every mistake. But it makes mistakes less likely.

## 3. How RAG works, step by step
First, we prepare the documents. This happens before any question comes.

We split each document into small pieces. Each piece is called a chunk. A chunk is usually a few sentences or one short paragraph. Next, we turn each chunk into a list of numbers. This list is called an embedding. An embedding is a list of numbers that shows the meaning of a text. Texts with similar meaning get similar numbers. We save all the embeddings in a special database. It is called a vector database.

Now a user asks a question. Three steps happen.

Step 1 is Retrieve. "Retrieve" means to find and bring back. The system turns the question into an embedding too. It compares this embedding with the saved ones. Then it picks the few chunks with the closest meaning.

Step 2 is Augment. "Augment" means to add more. The system builds a new message for the AI. It puts the question and the chosen chunks together. This message is called a prompt. A prompt is the text we send to the AI.

Step 3 is Generate. "Generate" means to create. The LLM reads the prompt and writes the answer. It uses the chunks as its source.

So the name follows the steps in order: Retrieve, Augment, Generate. Notice one more thing. The LLM does not change at any point. It does not learn or get retrained. It only reads extra text for that one question.

## 4. One full example
A college builds a help chatbot for its students. A student asks: "What is the last date to pay the exam fee?"

Without RAG, the LLM has never seen the college notices. It may guess a date. The guess can be wrong.

With RAG, the work goes like this. In the preparation step, the college loads its notice files. The system cuts them into chunks, makes embeddings, and saves them in the vector database.

Now the student asks the question. In the Retrieve step, the system turns the question into an embedding. It finds the chunk that says the exam fee must be paid by 15 March. It also finds one chunk about late fees.

In the Augment step, the system writes a prompt. The prompt says: "Answer using only this text," and then it shows the two chunks and the student's question.

In the Generate step, the LLM replies: "The last date to pay the exam fee is 15 March. After that date, a late fee applies."

The student gets the right answer from the real notice. The college can also show which notice the answer came from.

## 5. Common mistake to avoid
Many beginners think RAG teaches the AI new things. It does not. The AI does not change. RAG only gives the AI the right pages to read at the right time. In the open-book exam, the student does not learn the book. The student just reads the right page.

Training an AI again is a different method. It is called fine-tuning. It costs more and takes more time. It is also not a good choice for facts that change often.

Remember that RAG is only as good as its documents. If the notice is old or wrong, the answer will be wrong too. If the search step brings back the wrong chunk, the answer will also be poor.

## 6. Key words (glossary)
- **RAG**: A method where the system finds useful text first, then the AI uses it to answer.
- **LLM**: A computer program that reads and writes text after studying a huge amount of text.
- **Hallucination**: An answer that sounds right but is false.
- **Chunk**: A small piece of a document, such as a short paragraph.
- **Embedding**: A list of numbers that shows the meaning of a text.
- **Vector database**: A place that stores embeddings so we can search them by meaning.
- **Prompt**: The text we send to the AI.
- **Fine-tuning**: Training an AI model again so that the model itself changes.

## 7. Quick check
1. What do the three words in RAG stand for?
2. Why can an LLM not answer questions about your private files?
3. Which step puts the question and the chunks together in one prompt?
4. Does RAG change the LLM? Explain in one sentence.
