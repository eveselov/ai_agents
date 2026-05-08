# CLAUDE.md — LLM & AI Agents Lecture Series

This file gives Claude context across multiple short threads. Update it as the series develops.

## Project Overview

An ongoing lecture series for a math-enthusiast friends club (~50 people). Mix of engineers and smart non-technical people. Each lecture is 2 hours, standalone, and built around a working Jupyter notebook executed live in class.

Working directory: `c:/git/ai-agents/`

**The series has two distinct parts — keep them separate in your mind:**

**Part 1 — AI Agents (Lectures 1–4, finished):** A progressive course on building LLM-powered agents from scratch. Has a shared spine and each lecture builds on the previous one.

**Part 2 — LLM Internals & ML Topics (Lectures 5+, ongoing):** Independent standalone lectures on specific ML/LLM topics. These do NOT continue the agents narrative. Each is self-contained. New lectures may be added on any topic (evals, training, architectures, memory mechanisms, etc.).

## Part 1 Spine (Agents)

Single progressive question: *What does it take to get an LLM to reliably accomplish a goal in the real world?*

Recurring theme:
> In classical software, interfaces are enforced by type systems. In agent systems, the interface between components is **natural language** — strings flowing between nodes.

## Folder Structure

```
ai-agents/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .env.example
├── .env  (never commit)
├── shared/
│   └── utils.py
├── lecture1_minimal_loop/
├── lecture2_memory_rag/
├── lecture3_graphs_planning/
├── lecture4_multi_agent/
└── lecture5_latent_memory/   ← Part 2 begins here; independent of lectures 1–4
```

## Lecture Status

| # | Topic | Part | Status |
|---|-------|------|--------|
| 1 | Minimal agent loop (raw OpenAI, no frameworks) | Agents | finished |
| 2 | Memory and RAG (Chroma) | Agents | finished |
| 3 | Graphs and planning (LangGraph + Tavily) | Agents | finished |
| 4 | Multi-agent systems (LangGraph orchestrator/worker) | Agents | finished |
| 5 | Latent Memory Mechanisms in LLM (NTM, Memorizing Transformers) | Internals | in progress |

## Technical Stack

- Python, Jupyter notebooks
- PyTorch, matplotlib, numpy (Part 2 lectures)
- OpenAI API (key in .env) — Part 1 only
- Tavily API (key in .env) — Part 1 only
- LangChain, LangGraph — Part 1 only
- Chroma (vector store) — Part 1 only
- SQLite (graph state persistence) — Part 1 only

## Lecture Style

Raschka-style cell-by-cell notebooks, executed live in class. Prefer deliberate breakage to illustrate concepts.

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

**Part 1 (Agents):**
- [ ] Single tool vs. multi-tool choice in Lecture 1 demo
- [ ] Choose RAG document corpus for Lecture 2
- [ ] Show LangGraph visual graph rendering in Lecture 3?
- [ ] Include CrewAI in Lecture 4 as contrast to raw LangGraph?

**Part 2 (Internals):**
- [ ] Lecture 6 topic candidates: Titans/Mamba deep dive, evals, training internals, RLHF

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
