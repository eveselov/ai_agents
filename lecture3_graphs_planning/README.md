# Lecture 3 — Structure and Control: Graphs, Chains, and Planning

## Core Question

How do you build something more complex than a single loop? How do you give an agent a structured process to follow?

## What This Lecture Builds

Lectures 1 and 2 built capable agents using raw Python loops. This lecture asks what happens when the logic grows: multiple paths, retry conditions, quality checks, adaptive behavior. The answer is a graph — and the library that makes graphs first-class objects is LangGraph. The notebook starts with the smallest possible graph (two nodes, no branching) and builds up to a full ReAct agent, demonstrating streaming and SQLite-backed checkpointing along the way. No LangChain abstractions are used — LangGraph is wired directly to the same raw OpenAI and Tavily clients from earlier lectures.

The analogy made explicit in the notebook: Lectures 1–2 were assembly language. LangGraph is C — more structure, same underlying mechanism, still visible at the right level of abstraction.

## Narrative Arc

**Part 1 — A Graph Is Just Nodes and Edges**
Build the smallest possible LangGraph: two nodes (`node_a`, `node_b`), one fixed edge, a `TypedDict` state. Run it. Render the diagram with `draw_mermaid_png()`. Establish the vocabulary: nodes are computation, edges are control flow, state is communication.

**Part 2 — This Is a Chain, Not a Graph**
A → B → END is a chain — every run takes the same path. Introduce `add_conditional_edges` with a routing function that loops back when a counter is too low. Now the graph is a graph: the path taken depends on runtime state. Name the distinction: branching is what separates a chain from a graph.

**Part 3 — The State Dict Is the Language Flow**
Introduce `ResearchState` with string fields: `topic`, `search_results`, `summary`. Point at the type annotations: everything meaningful is a string. The interface between nodes is natural language flowing through a dict.

**Part 4 — Building the Research Graph**
Three nodes: `search` (Tavily), `check_results` (routing function — no LLM), `write` (OpenAI) and `give_up` (fallback). The routing function is pure Python: it inspects result length and attempt count; it never calls a model. Explain the `MAX_ATTEMPTS` guard — every cycle needs a budget.

**Part 5 — Run the Graph**
Invoke the research graph on a topic. Inspect `final_state` after completion: all intermediate state is visible — raw search results, attempt count, final summary. Full observability without separate logging.

**Part 6 — The ReAct Pattern**
Introduce the formal ReAct pattern (Yao et al. 2022): Reason + Act, interleaved. Build a `think → act → (continue?) → think → ...` graph. The `think` node asks the model what to do next; the `act` node executes it; the routing function checks for a final answer or step budget exhaustion. The model drives the loop; the graph provides the execution harness and the termination guard.

**Part 7 — Streaming**
Switch from `.invoke()` to `.stream()`. Show `stream_mode="values"` (full state after each node) and `stream_mode="updates"` (only changed keys, wrapped by node name). The graph becomes observable in real time — during live demos the audience sees the agent thinking step by step.

**Part 8 — Checkpointing and Persistence**
Compile the graph with a `SqliteSaver` checkpointer. Run with a `thread_id` in config. Retrieve the saved state afterward with `get_state()` — no re-running, just reading from SQLite. Explain the human-in-the-loop pattern: `interrupt_before` freezes the graph mid-run; the same `thread_id` resumes it after human review.

## Key Concepts

- LangGraph: nodes (computation), edges (control flow), state dict (communication)
- Chains vs. graphs: the distinction is branching, not size
- `TypedDict` state: plain dict at runtime, typed at development time, JSON-serializable for checkpointing
- Conditional edges and routing functions: pure Python decisions, not LLM calls
- Step budgets: every cycle in a graph needs a hard termination condition
- Language flow: string values in the state dict are the agent's interface between nodes
- ReAct pattern: model-driven Reason + Act interleaved with graph-enforced structure
- `stream_mode="values"` vs. `"updates"`: full state vs. delta per node
- Checkpointing: SQLite-backed state snapshots, thread IDs, resume after crash, human-in-the-loop

## Notebook Structure

`notebook3.ipynb` — LangGraph wired directly to raw OpenAI and Tavily clients.

Same two-layer cell pattern:
- **Visible layer**: short markdown before each code cell
- **Details layer**: `<details>` blocks covering LangGraph's functional state model, routing function constraints, why routing functions must not call LLMs, the framework landscape, and when to use a graph vs. a plain loop

## Discussion Prompts

1. What is the difference between a chain and a graph? When do you actually need a graph?
2. A routing function must not call an LLM — why? What would break if it did?
3. The `MAX_ATTEMPTS` guard is a hard limit. What are other ways to budget a loop? What are the trade-offs?
4. In the ReAct graph, the model decides what action to take next. In the research graph, the Python routing function decides. What determines which approach to use?
5. What does checkpointing enable beyond crash recovery? What would you need to implement a "pause for human approval" step?
6. The state dict contains everything the graph knows. What happens when a node needs information that was not anticipated as a state field?

## Instructor Notes

- Open Part 1 by saying explicitly: "We are moving from assembly language to C — the loop is the same, the structure becomes visible."
- In Part 2, run the chain first, then show the conditional edge. The moment the diagram gains a cycle is the moment a graph becomes a graph.
- In Part 4, pause on the routing function: point out that it is pure Python, has no LLM call, runs inside the engine's control-flow loop. This is why it must be fast and deterministic.
- The ReAct diagram in Part 6 is worth dwelling on: compare it to the research graph. Ask the room where the "intelligence" sits in each — in the graph structure, or in the model?
- Streaming in Part 7 is primarily a live-demo tool. Run it during the lecture so the audience sees node-by-node output appearing in real time.
- Part 8 can be shortened if time is short — the `get_state()` call is the key moment: state persisted to SQLite and retrieved without re-running.
