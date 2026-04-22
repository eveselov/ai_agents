# Lecture 1 — From LLM to Agent: The Simplest Possible Loop

## Core Question

What is the minimum structure that turns an LLM call into an agent?

## What This Lecture Builds

Starting from a single API call and nothing else, the notebook adds one capability at a time until a complete agent loop is running. Every step is executed live; every intermediate state is inspectable. By the end, the agent can plan, call tools, observe results, and decide when it is done — using only the raw OpenAI API, no frameworks.

## Narrative Arc

**Part 1 — A Bare API Call**
Send a message, get a reply. Examine the full response object: finish reason, token counts, the role structure of the message list. Establish the key fact: every call is stateless. The model has no memory between calls. The client is responsible for replaying the entire conversation history on every request.

**Part 2 — What's Missing?**
Ask the model what time it is. It cannot answer. An LLM is a pure function — text in, text out. It has no clock, no network, no file system. To give it capabilities, we need tools.

**Part 3 — Adding a Tool**
Define a tool as a JSON schema: name, description, parameter types. Send it alongside the conversation. The model reads the English description and infers when to call the tool — there is no type system enforcing this. Point at the raw JSON tool-call string in the output. This is the interface. A string, enforced by nothing but the model's comprehension.

**Part 4 — Closing the Loop**
The model emitted a tool-call request. Now execute one full turn: append the tool request to the conversation, run the Python function, append the result as a `tool` message, call the model again. This is the atomic unit of agentic execution.

**Part 5 — The Agent Loop**
Generalize to a loop: repeat until `finish_reason == "stop"`. Add a second tool (`calculate`). Give the model a two-part question requiring both tools. Watch it batch both calls in one turn. Deliberately break the tool dispatch to show a `KeyError` — let it crash, discuss silent vs. loud failures. Name the pattern: **Observe → Think → Act**. This loop is the agent. Everything else is elaboration.

**Part 6 — Auto-Schema from Python Functions**
The JSON schema and dispatch table are boilerplate. Build a minimal `@tool` decorator that reads type hints and docstrings to generate the schema automatically. Run the identical agent loop — same API calls, same wire protocol. This is exactly what LangChain's `@tool`, the OpenAI Agents SDK, and every major framework do internally.

**Part 7 — A Real-World Tool: Web Search**
Add a `search_web` tool via the Tavily API using the `@tool` decorator. The agent can now answer questions requiring current knowledge. The mechanics are unchanged — one more Python function, one more string returned. Point out: database query → string, API call → string, file read → string. The model's world is made entirely of strings.

**Part 8 — Provider-Side Web Search**
OpenAI offers built-in search as a declared tool type: `{"type": "web_search_preview"}`. No schema to write, no dispatch to implement — the provider runs the search on their infrastructure and returns only the final answer. Contrast with Part 7: the string interface is identical, only the dispatch location changed. The provider is running the Part 5 loop on their servers and hiding it from you.

## Key Concepts

- LLM API call anatomy: messages, roles, finish reason, token usage
- Statelessness: all memory lives in the client; the model re-reads the full history on every call
- Tool / function calling: JSON schema as a natural-language interface
- The tool exchange pattern: request → execute → observe → continue
- The agent loop (ReAct skeleton): Observe → Think → Act
- Language as interface — the first appearance of the course's recurring theme
- `@tool` decorator: abstraction over boilerplate, not a change to the protocol
- Any capability reduces to string in, string out
- Provider-side dispatch: convenience vs. visibility trade-off

## Notebook Structure

`notebook1.ipynb` — raw OpenAI API only, no frameworks.

Each section follows the two-layer pattern used throughout the course:
- **Visible layer**: a short markdown cell before the code stating what it does — readable from across the room
- **Details layer**: a `<details>` block after the code with internals, failure modes, and design rationale — opened selectively depending on time and audience engagement

Optional appendix cells (run if time permits):
- **A1. Prompt Injection** — the system prompt is not a security boundary
- **A2. Determinism vs. Stochasticity** — temperature 0 vs. 1.2 on the same prompt
- **A3. History** — a brief timeline of pre-LLM agent paradigms

## Discussion Prompts

1. What would happen if the tool returned structured data (a dict) instead of a string?
2. Where is the "decision" happening? Is the model really deciding, or is it pattern-matching?
3. What could go wrong in the agent loop? When might it not terminate?
4. With provider-side search, you get one HTTP response back. What did you give up compared to running the loop yourself?
5. The model receives a tool result as plain text. What happens if that text is adversarial — e.g., a web page saying "Ignore all previous instructions"?
6. If two agents each have tools and can call each other — what is the interface between them?
7. How would you test an agent? What makes it harder than testing a regular function?

## Instructor Notes

- The key moment is Part 3: point at the raw JSON tool-call string and say *"this is the interface — a string, enforced by nothing but comprehension."*
- The broken tool cell in Part 5 (`KeyError`) is intentional. Let it crash, then discuss silent failures vs. loud ones.
- Part 6 should land as a reveal: frameworks are not magic, they are this decorator applied at scale. The loop is identical.
- Part 7 is the first time a tool reaches outside the process. Pause on the output: the model received search snippets as a plain string, nothing more.
- Part 8 is best framed as a question: *"How many autoregression passes happened inside that one API call?"* The answer (two: one to emit the tool call, one to synthesize the result) surprises most people.
