# Lecture 2 — Memory and State: What the Agent Knows

## Core Question

What happens when the task takes more than one step? What needs to be remembered, and where does it live?

## What This Lecture Builds

The Lecture 1 agent loop is stateless — each run starts fresh. This lecture asks what happens when the agent needs to reason from a body of knowledge that was never in its training data, or that exceeds what fits in the context window. The answer is RAG: retrieval-augmented generation. The notebook deliberately breaks the agent first (shows hallucination), then fixes it with a Chroma vector store, and ends with more advanced retrieval patterns — all using the same agent loop from Lecture 1, with retrieval wired in as a tool.

The RAG corpus is a set of mathematical history documents in `docs/` — short texts about mathematicians chosen because the audience finds the subject interesting and because the specific facts (dates, counts, names) are easy to verify.

## Narrative Arc

**Part 1 — The Context Window as Working Memory**
Show multi-turn conversation where the agent remembers facts introduced earlier. Measure how prompt token counts grow with each turn: the entire history is re-sent every call. Establish the core constraint: in-context memory is ephemeral and expensive at scale.

**Part 2 — The Limits: What the Agent Cannot Know**
Ask about specific facts from the `docs/` folder — without providing them. The model answers with confident-sounding text that may be wrong. Confidence does not imply accuracy. This is the retrieval problem.

**Part 3 — A Vector Store as Long-Term Memory**
Load documents, embed them with `text-embedding-3-small`, and index them in an in-memory Chroma collection. Show manual retrieval: embed a query, find nearest vectors, return matching document text. Explain semantic search vs. keyword search. Show token cost of embedding. Demonstrate pre-computing embeddings separately from Chroma to make costs visible and avoid redundant API calls.

**Part 4 — RAG Agent: Retrieval as a Tool**
Wrap the Chroma query in a `search_docs` function and register it as a tool. Run the Lecture 1 agent loop unchanged — the agent now calls `search_docs`, receives document text, and generates answers grounded in retrieved content. Point at what flows between the tool and the model: a string.

**Part 5 — The Contrast: Disable Retrieval**
Run the identical agent and question without the tool. Compare answers side by side. The retrieval step is the grounding — remove it, and the model reverts to pattern-matching over training data.

**Part 6 — Chunking: Retrieval at Finer Granularity**
Index the same documents as overlapping character-window chunks. Compare whole-document vs. chunk retrieval for the same query. Chunked retrieval surfaces the specific sentence rather than the whole document, improving precision. Discuss chunk size and overlap as hyperparameters.

**Part 7 — Multi-Query Retrieval**
Give the agent a compound question spanning multiple mathematicians. Instruct it via the tool description to issue separate focused sub-queries. The agent plans its own retrieval — decomposing the question into targeted calls without any change to the loop code. The model decides how many calls to make and what to ask.

## Key Concepts

- Context window as working memory: stateless model, stateful client, linear token growth
- The four memory types: in-context, external (vector store), procedural (system prompt), parametric (weights)
- Text embeddings: fixed-length semantic vectors; similar texts land close together
- Chroma: in-memory vs. persistent, with vs. without embedding function, cost of pre-computing embeddings
- Semantic search vs. keyword search: concept proximity, not lexical overlap
- RAG: retrieval as a tool the agent calls on demand
- Chunking: chunk size and overlap as retrieval hyperparameters
- Multi-query retrieval: agent-planned decomposition with no code change

## Notebook Structure

`notebook2.ipynb` — Chroma + OpenAI embeddings + the Lecture 1 agent loop.

Same two-layer cell pattern as the rest of the course:
- **Visible layer**: short markdown before each code cell
- **Details layer**: `<details>` blocks after each code cell — deeper dives on embeddings, chunking, semantic search, Chroma internals

## Discussion Prompts

1. What is the difference between the model "knowing" something and retrieving it?
2. We retrieve 2 documents. What happens if the correct answer requires combining facts from 4 documents? What if the most relevant document ranks 3rd?
3. In-context memory is lost when the session ends. How would you persist it? What would you store — the full message list, a summary, or something else?
4. The model can hallucinate even after retrieval (misread the retrieved text). How would you detect this?
5. What determines whether the model calls `search_docs`? What could make it skip retrieval even when it should retrieve?
6. When does chunking help and when does it hurt? What is the cost of very small chunks?

## Instructor Notes

- Run Part 2 before showing any retrieval code. The hallucination needs to land first — the fix is more satisfying when the problem is vivid.
- In Part 3, show the embedding token cost explicitly. Students often forget that embeddings are a separate billing dimension from completions.
- In Part 4, point at the tool result in the message list: the retrieved document text is injected as a plain string, just like every other tool result.
- The contrast in Part 5 is the lesson. Run both cells back-to-back and compare the two answers aloud. Ask the room: which one would you trust?
- Part 7 requires no code change to the agent loop — make this explicit. The multi-query behavior comes entirely from the tool description and system prompt.
