# Lecture 4 — Multi-Agent Systems: Division of Labor

## Core Question

When does one agent become multiple agents, and why?

## Narrative Arc

1. Show what a single agent struggles with: long tasks, conflicting roles, parallelism.
2. Introduce decomposition: orchestrator + worker.
3. The interface between them is a natural language task description — a sentence. *This is the payoff of the whole course.*
4. Discuss what this buys (flexibility, specialization) and costs (reliability, debugging, prompt brittleness).
5. End honestly: agents are powerful but fragile, the field is rapidly evolving, abstractions are still settling.

## Key Concepts

- Orchestrator / worker pattern
- Agent-to-agent communication (language as API)
- Task decomposition
- Current limitations and failure modes

## Notebook

`notebook4.ipynb` — Two-agent LangGraph system. Orchestrator generates tasks, worker executes, results flow back.

## Discussion Prompts

- How is agent-to-agent communication different from function calls in classical software?
- What can go wrong when agents communicate in natural language?
- Where is the "intelligence" in a multi-agent system — in the orchestrator, the workers, or both?
- What would you need to trust this system with something important?
