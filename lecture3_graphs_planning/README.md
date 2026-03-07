# Lecture 3 — Structure and Control: Graphs, Chains, and Planning

## Core Question

How do you build something more complex than a single loop? How do you give an agent a structured process to follow?

## Narrative Arc

1. Introduce LangGraph. Show a graph with 2-3 nodes.
2. Point at the state object passing between nodes — it's a dict, and the meaningful part is strings. *This is the language flow.*
3. Build toward planning: an agent that generates a sequence of steps before executing them.
4. Introduce the ReAct pattern formally (Reason + Act, interleaved). Reference the 2022 paper.
5. Demo: research a topic and write a summary using Tavily web search + writing node.

## Key Concepts

- LangGraph: nodes, edges, state
- Chains vs. graphs
- Planning and ReAct (Yao et al. 2022)
- Language flow made visible (state dict as the data bus)

## Notebook

`notebook.ipynb` — LangGraph workflow: Tavily search → summarize with OpenAI.

## Discussion Prompts

- What is the difference between a chain and a graph? When do you need a graph?
- What does "planning" mean for an LLM? Is it real planning?
- What happens when a node produces bad output? How do you handle errors in a graph?
