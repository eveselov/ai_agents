# CLAUDE.md — AI Agents Course

This file gives Claude context across multiple short threads. Update it as the course develops.

## Project Overview

A 4-lecture course on AI agents for a math-enthusiast friends club (~50 people). Mix of engineers and smart non-technical people. Goal: constructive understanding of how agents are built, not how to use them. Each lecture duration is 2 hours. 

Working directory: `c:/git/ai-agents/`

## Course Spine

Single progressive question: *What does it take to get an LLM to reliably accomplish a goal in the real world?*

Recurring theme (establish in L1, echo in each lecture):
> In classical software, interfaces are enforced by type systems. In agent systems, the interface between components is **natural language** — strings flowing between nodes.

Style: Raschka-style cell-by-cell notebooks, executed live in class. Prefer deliberate breakage to illustrate concepts.

## Folder Structure

```
ai-agents/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .env.example - a template
├── .env - a real secret keys - never submit to git
├── shared/
│   └── utils.py
├── lecture1_minimal_loop/
│   ├── README.md
│   └── notebook1.ipynb
├── lecture2_memory_rag/
│   ├── README.md
│   ├── notebook2.ipynb
│   └── docs/
├── lecture3_graphs_planning/
│   ├── README.md
│   └── notebook3.ipynb
└── lecture4_multi_agent/
    ├── README.md
    └── notebook4.ipynb
```

## Lecture Status

| Lecture | Topic | Status |
|---------|-------|--------|
| 1 | Minimal agent loop (raw OpenAI, no frameworks) | finished |
| 2 | Memory and RAG (Chroma) | scaffolded |
| 3 | Graphs and planning (LangGraph + Tavily) | scaffolded |
| 4 | Multi-agent systems (LangGraph orchestrator/worker) | scaffolded |

## Technical Stack

- Python, Jupyter notebooks
- OpenAI API (key in .env)
- Tavily API (key in .env)
- LangChain, LangGraph
- Chroma (vector store)
- SQLite (graph state persistence)

## Design Decisions

- One notebook per 2-hour lecture
- `shared/utils.py` for shared boilerplate (API client init, display helpers)
- Each lecture README has instructor notes and class discussion prompts
- Lecture 2 has a `docs/` folder for RAG corpus — corpus not yet chosen
- Notebooks must be self-contained and runnable start-to-finish
- In python code use explicit type specifications for all variables, parameters, return values
- In bigger Python cells use short comments before each logical to explain its intention

## Notebook Cell Structure

Each notebook follows a two-layer narrative pattern:

**Visible layer** (always shown): a short markdown cell before each code cell that states what the code does — one or two sentences, readable from across the room. This is what listeners see on the screen during live execution.

**Details layer** (instructor-controlled): a `<details>` / `<summary>` block in a markdown cell *after* the code cell. Contains deeper reflection: internals, design rationale, failure modes, connections to broader concepts. The instructor opens these selectively depending on time available and audience engagement.

Rules for `<details>` blocks:
- Title in `<summary>` should name the concept, not the code action (e.g. "What is a tool?" not "Tool schema defined")
- Content should deepen, not repeat — assume the listener just saw the code run
- Each block should be independently openable; avoid cross-references between blocks
- Prefer concrete examples and failure modes over abstract description
- Use lowercase `<summary>` tag (not `<Summary>`)

## Open Questions

- [ ] Single tool vs. multi-tool choice in Lecture 1 demo
- [ ] Choose RAG document corpus for Lecture 2 (something the audience finds interesting)
- [ ] Show LangGraph visual graph rendering in Lecture 3?
- [ ] Include CrewAI in Lecture 4 as contrast to raw LangGraph?
- [ ] Possible Lecture 5: evals, autonomous agents/safety, or specific application domain

## Per-Lecture Notes

### Lecture 1
- Bare OpenAI call → add tool → close the loop
- Notebook: raw OpenAI API only, no frameworks
- Key moment: point at the JSON tool-call string and say "this is the interface"

### Lecture 2
- Show context-window-as-working-memory breaking first, then fix with RAG
- Deliberately remove retrieval to show hallucination — contrast is the lesson
- Chroma + OpenAI embeddings

### Lecture 3
- Introduce LangGraph: nodes, edges, state dict
- Point at state dict: "the meaningful part is strings — this is the language flow"
- ReAct pattern formally (reference 2022 paper)
- Demo: research-and-summarize with Tavily + writing node

### Lecture 4
- Orchestrator generates tasks (natural language), worker executes
- "The interface between agents is a sentence" — course payoff moment
- End honestly: agents are powerful but fragile, abstractions still settling
