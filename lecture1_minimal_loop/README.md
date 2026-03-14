# Lecture 1 — From LLM to Agent: The Simplest Possible Loop

## Core Question

What is the minimum structure that turns an LLM call into an agent?

## Narrative Arc

The lecture builds toward a single answer in six steps, each one executable live in the notebook.

**Part 1 — A Bare API Call**
Send a message, get a reply. Examine the full response object: finish reason, token counts, the message list structure. Every API call is stateless — the model has no memory between calls. The client app is responsible for replaying the entire conversation history on every request.

**Part 2 — What's Missing?**
Ask the model what time it is. It can't answer. An LLM is a pure function: text in, text out. It has no clock, no network, no file system. To give it capabilities, we need tools.

**Part 3 — Adding a Tool**
Define a tool as a JSON schema: name, description, parameter types. Send it alongside the conversation. The model reads the English description and *infers* when to call the tool — there is no type system enforcing this. Point at the JSON string on the screen: *this is the interface.*

**Part 4 — Closing the Loop**
The model asked for a tool. Now execute the four steps: append the model's tool request to the conversation, run the Python function, append the result as a `tool` message, call the model again. This is one full turn.

**Part 5 — The Agent Loop**
Generalize to a loop: repeat until `finish_reason == "stop"`. Add a second tool (`calculate`). Give the model a two-part question requiring both tools. Watch it batch both tool calls in one turn. Name the pattern: **Observe → Think → Act**. This loop *is* the agent. Everything else is elaboration.

**Part 6 — Auto-Schema from Python Functions**
The JSON schema and dispatch table are pure boilerplate. Build a minimal `@tool` decorator that reads type hints and docstrings and generates the schema automatically. Run the same agent loop — identical API calls, identical wire protocol. This is exactly what LangChain's `@tool`, the OpenAI Agents SDK, and every major framework do internally.

## Key Concepts

- LLM API call anatomy: messages, roles, finish reason, token cost
- Statelessness: all memory lives in the client; the model re-reads history on every call
- Tool/function calling: JSON schema as natural-language interface
- The tool exchange pattern: request → execute → observe → continue
- The agent loop (ReAct pattern): Observe → Think → Act
- Language as interface — first appearance of the course's recurring theme
- `@tool` decorator: abstraction over boilerplate, not a change to the protocol

## Notebook Structure

`notebook1.ipynb` — raw OpenAI API only, no frameworks.

Each section follows the two-layer pattern used throughout the course:
- **Visible layer**: short markdown cell before the code — what it does, readable from across the room
- **Details layer**: `<details>` block after the code — internals, failure modes, design rationale; opened selectively depending on time and audience engagement

Appendix cells (optional, run if time permits):
- **A1. Prompt Injection** — demonstrate that the system prompt is not a security boundary
- **A2. Determinism vs. Stochasticity** — same prompt at temperature 0 vs. 1.2
- **A3. History** — brief timeline of pre-LLM agent paradigms

Total speaking time: ~2 hours.

## Discussion Prompts

1. What would happen if the tool returned structured data (a dict) instead of a string?
2. Where is the "decision" happening? Is the model really deciding?
3. What could go wrong in this loop? When might it not terminate?

## Instructor Notes

- The key moment is Part 3: point at the raw JSON tool-call string in the output and say *"this is the interface — a string, enforced by nothing but comprehension."*
- The broken tool cell in Part 5 (`KeyError`) is intentional — let it crash, then discuss silent failures vs. loud ones.
- Part 6 should land as a reveal: frameworks are not magic, they are this decorator applied at scale. The loop is the same.
- The appendix cells are independent; pick whichever fits the room's energy.
