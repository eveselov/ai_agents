# AI Agents Course

A 4-lecture hands-on course on how AI agents are built — not how to use them.

Designed for a math-enthusiast audience: engineers and curious non-technical people.

## Central Question

> *What does it take to get an LLM to reliably accomplish a goal in the real world?*

Each lecture answers one layer of that question through running notebook code.

## Lectures

| # | Topic | Key Concept |
|---|-------|-------------|
| 1 | [Minimal Agent Loop](lecture1_minimal_loop/) | Tool calling, Observe→Think→Act |
| 2 | [Memory and RAG](lecture2_memory_rag/) | Context window, vector search, retrieval |
| 3 | [Graphs and Planning](lecture3_graphs_planning/) | LangGraph, ReAct pattern |
| 4 | [Multi-Agent Systems](lecture4_multi_agent/) | Orchestrator/worker, language as API |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Fill in your API keys in .env - use .env.example as a template
```

## Recurring Theme

In classical software, component interfaces are enforced by type systems and compilers.
In agent systems, the interface between components is **natural language** — strings flowing between nodes.
This is the fundamental architectural novelty of agents.
