# Lecture 3 — Structure and Control: Graphs, Chains, and Planning

## Core Question

How do you build something more complex than a single loop? How do you give an agent a structured process to follow?

## Narrative Arc

1. Introduce LangGraph. Show a minimal graph (2-3 nodes) in code and as a rendered diagram.
2. Point at the state object passing between nodes — it's a dict, and the meaningful part is strings. *This is the language flow.*
3. Show a linear graph first (search → write → end) and name it: this is just a chain. Ask: what makes a graph actually a graph?
4. Add a conditional edge — a `should_retry` branch that loops back if the search result is empty or too thin. Now the topology is doing real work.
5. Introduce the ReAct pattern formally (Reason + Act, interleaved). Reference Yao et al. 2022. Show it as a specific graph shape: think → act → observe → think…
6. Demo: research a topic and write a summary using Tavily web search + writing node, with the retry branch live.

## Key Concepts

- LangGraph: nodes, edges, conditional edges, state dict
- Chains vs. graphs — the distinction is branching, not size
- Conditional edges as the mechanism for control flow
- Planning and ReAct (Yao et al. 2022)
- Language flow made visible: the state dict is the data bus between nodes, and its values are strings

## Notebook

`notebook3.ipynb` — LangGraph workflow: user prompt → search (Tavily) → conditional retry branch → summarize with OpenAI.

## What Was Dropped and Why

- **RAG**: covered in Lecture 2. Re-introducing retrieval here would blur the lesson boundary. The Tavily search node already demonstrates "retrieval in a graph" without re-importing vector store mechanics.
- **Planning node**: tempting, but adds a third concept stack. The ReAct loop *is* a planning pattern — naming it is sufficient.

## Discussion Prompts

- What is the difference between a chain and a graph? When do you actually need a graph?
- What does "planning" mean for an LLM? Is it real planning?
- What happens when a node produces bad output? How do you handle errors in a graph?
- The retry branch loops on bad search results — what could go wrong with that design?
