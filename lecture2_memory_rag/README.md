# Lecture 2 — Memory and State: What the Agent Knows

## Core Question

What happens when the task takes more than one step? What needs to be remembered, and where does it live?

## Narrative Arc

1. The Lecture 1 loop is stateless. Show what breaks when a task requires context from prior steps.
2. Introduce the four memory types: in-context, external (vector store), episodic (past runs), parametric (weights).
3. Don't just enumerate — show what *breaks* without each one.
4. Build a RAG setup with Chroma. Point at the retrieved chunk injected into the prompt: *this is memory — it's just text flowing into context.*
5. Deliberately remove retrieval to show hallucination. The contrast is the lesson.

## Key Concepts

- Context window as working memory
- Vector embeddings and similarity search
- RAG (Retrieval Augmented Generation)
- The four memory categories

## Notebook

`notebook2.ipynb` — Chroma + OpenAI. Show retrieval, prompt construction, answer. Then break it.

## Corpus

Source documents in `docs/` — corpus TBD (should be something the audience finds interesting).

## Discussion Prompts

- What is the difference between the model "knowing" something and retrieving it?
- When does RAG fail? What are its failure modes?
- How is a vector database different from a keyword search index?
