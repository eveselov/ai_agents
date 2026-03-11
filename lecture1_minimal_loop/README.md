# Lecture 1 — From LLM to Agent: The Simplest Possible Loop

## Core Question

What is the minimum structure that turns an LLM call into an agent?

## Narrative Arc

1. Bare OpenAI API call. Just a prompt, a response.
2. Ask: what's missing if we want this to *do* something in the world?
3. Add a tool. Show the JSON tool-calling contract. Point at the screen: *this string is the interface.*
4. Close the loop: model decides to call a tool → tool runs → result returns as text → model continues.
5. Name it: Observe → Think → Act. This is an agent. Everything else is elaboration.
6. Show the higher-level alternative: a `@tool` decorator that auto-generates JSON schemas from type hints and docstrings. Same loop, same API calls — pure developer-experience sugar. This is what LangChain and other frameworks do internally.

## Key Concepts

- LLM API call anatomy, completion token cost, list of user/system messages
- Tool/function calling (JSON schema) - called by LLM automatically or inferred from LLM structured repsonse
- The agent loop (ReAct conceptually)
- Language as interface (first appearance)

## Notebook

`notebook1.ipynb` — raw OpenAI API only, no frameworks.
Presents a list of cells demonstrating individual actions such as connection, API request, configuration for tools,
illustrations for results investigations and interpretations.
Total speaking time ~2 hours.

## Discussion Prompts

- What would happen if the tool returned structured data instead of a string?
- Where is the "decision" happening? Is the model really deciding?
- What could go wrong in this loop? When might it not terminate?
