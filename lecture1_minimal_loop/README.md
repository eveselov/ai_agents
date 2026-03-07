# Lecture 1 — From LLM to Agent: The Simplest Possible Loop

## Core Question

What is the minimum structure that turns an LLM call into an agent?

## Narrative Arc

1. Bare OpenAI API call. Just a prompt, a response.
2. Ask: what's missing if we want this to *do* something in the world?
3. Add a tool. Show the JSON tool-calling contract. Point at the screen: *this string is the interface.*
4. Close the loop: model decides to call a tool → tool runs → result returns as text → model continues.
5. Name it: Observe → Think → Act. This is an agent. Everything else is elaboration.

## Key Concepts

- LLM API call anatomy
- Tool/function calling (JSON schema)
- The agent loop (ReAct conceptually)
- Language as interface (first appearance)

## Notebook

`notebook.ipynb` — ~50-80 lines, raw OpenAI API only, no frameworks.

## Discussion Prompts

- What would happen if the tool returned structured data instead of a string?
- Where is the "decision" happening? Is the model really deciding?
- What could go wrong in this loop? When might it not terminate?
