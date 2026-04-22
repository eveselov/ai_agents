# Lecture 4 — Multi-Agent Systems: Division of Labor

## Core Question

When does one agent become multiple agents, and why?

## What This Lecture Builds

Lectures 1–3 built progressively smarter single agents: a bare loop, a memory-augmented loop, a graph-structured planner. All the intelligence lived in one process, one prompt, one loop. This lecture asks what happens when a task is too large, too varied, or too conflicted for one agent to handle well. The answer is decomposition: an orchestrator agent that plans and assigns work, and worker agents that execute isolated tasks in parallel. Workers are launched via LangGraph's `Send` primitive — a true dynamic fan-out where the number of parallel branches is determined at runtime by the orchestrator's output. The interface between orchestrator and workers is a plain English sentence. This is the payoff of the whole course.

## Narrative Arc

**Part 1 — Why One Agent Is Not Always Enough**
Demonstrate role conflict live: prompt a single model to argue both sides of a question and produce a policy recommendation. It hedges. Name the three failure modes that motivate multi-agent systems: role conflict, context window exhaustion, and serial bottleneck (no parallelism).

**Part 2 — The Orchestrator / Worker Pattern**
Introduce the architecture with an ASCII diagram: orchestrator fans out to three workers in parallel, workers fan back in to a synthesizer. Define two state schemas: `MultiAgentState` (shared across the whole graph) and `WorkerState` (private to each worker instance). Introduce the `Annotated[list[str], operator.add]` reducer that makes concurrent writes to `results` safe.

**Part 3 — The Orchestrator Node**
The orchestrator calls the model with a system prompt that says "decompose into THREE independent tasks" and a user message containing the research goal. It returns a JSON array of task strings and stores them in shared state. A separate `dispatch_workers` routing function converts the task list into a list of `Send` objects — one per task — each carrying its own private `WorkerState`. Explain how `Send` differs from a plain string edge: it is a call request (not just a destination) that carries its own argument (not the shared state).

**Part 4 — The Worker Node**
Each worker receives exactly one `WorkerState` — it cannot read `goal`, `tasks`, or other workers' results. It searches Tavily for its task, summarizes the findings, and returns `{"results": [one_string]}`. The reducer appends this single entry to the shared list. Demonstrate testability: call `worker_node` directly with a hand-constructed `WorkerState` dict — no graph, no orchestrator required.

**Part 5 — The Synthesizer Node**
The synthesizer is the only node that sees both the original goal and all worker results. It formats the results as a numbered prose list (not a Python list — the model reads text, not data structures), asks the model to synthesize them into a 4–6 sentence answer, and returns the result. Two Details blocks: one on why a numbered string is the right format (the model's "type system" is reading comprehension), one on why a separate synthesizer is better than having the orchestrator do everything.

**Part 6 — Assemble and Run**
Wire the three nodes into a graph using `add_conditional_edges("orchestrator", dispatch_workers, ["worker"])`. The diagram shows the fan-out shape. Three Details blocks cover: reading the diagram (fan-out and fan-in, dynamic parallelism, the automatic barrier before synthesizer), and three honest questions about the architecture — whether the synthesizer could work incrementally (reflection pattern), what happens when a worker fails, and why the diagram does not show parallel branches (static definition vs. runtime shape).

**Part 7 — The Interface Between Agents Is a Sentence**
Print the task strings from `final_state["tasks"]`. Show their Python type (`str`). Name the observation: this string is the entire contract between orchestrator and worker — no schema, no type enforcement, no compiler check. Two Details blocks: one unpacking where the three genuinely different findings came from (the task strings, not temperature), one on the deeper mechanics of how the language model merges two orthogonal perspectives (the decomposition instruction and the user's topic) into coherent subtasks — without any explicit merge logic.

A third Details block examines three levels of perspective merge visible in a single run: (1) planning — "THREE" meets "gradient descent" produces three subtasks; (2) search — each task string meets raw web results produces a focused paragraph; (3) synthesis — "Synthesize" meets three findings produces a coherent answer. Each level is illustrated with an ASCII diagram. The closing observation: each prompt parameter is an independent dial; the language model is the mixer.

**Part 8 — Specialized Workers**
Build a second graph with two genuinely different worker types sharing no code: a `researcher` (searches Tavily, neutral summary) and a `critic` (no search, adversarial challenge). Both call the same `gpt-4o-mini` model — specialization is entirely in the system prompt. A `verdict` node synthesizes both. Run on a contested scientific claim about neural scaling laws.

**Part 9 — Honest Limitations**
Deliberately run the orchestrator with an ambiguous goal ("make it better"). It produces plausible-sounding tasks anyway — no error raised, silent failure. Name five limitations to know before deploying: silent failures, error propagation through the pipeline, no shared memory between workers, cost and latency multiplication, and prompt brittleness compounding across agents.

## Key Concepts

- Three single-agent failure modes: role conflict, context exhaustion, serial bottleneck
- Orchestrator / worker / synthesizer pattern
- `Send` for dynamic fan-out: call request with private state, not just a routing destination
- Two state schemas: shared `MultiAgentState` vs. isolated `WorkerState`
- `Annotated[list[str], operator.add]` reducer for concurrent writes
- Language as the agent API: `str` is the only type crossing agent boundaries
- Specialization through prompting: role is defined by the system prompt, not the model
- Perspective merge: how a language model fuses independent sources of meaning without explicit merge logic
- Silent failure: confident output despite meaningless input
- Five production limitations: silent failures, error propagation, no inter-worker memory, cost multiplication, prompt brittleness

## Notebook Structure

`notebook4.ipynb` — LangGraph orchestrator/worker system wired to raw OpenAI and Tavily clients.

Same two-layer cell pattern:
- **Visible layer**: short markdown before each code cell
- **Details layer**: `<details>` blocks covering `Send` mechanics, worker isolation, reducer semantics, the linguistic nature of data serialization, why the diagram is static, three fan-out questions, where output diversity comes from, perspective merge at three levels, and specialization through prompting

## Discussion Prompts

1. How is agent-to-agent communication different from function calls in classical software? What does the absence of a type system cost you in practice?
2. The orchestrator decomposed "gradient descent" into three subtasks without any domain knowledge in its code. Where did the domain structure come from?
3. A worker cannot see what other workers are finding. When is this a problem? How would you redesign the architecture to allow workers to coordinate?
4. The synthesizer prompt says "Synthesize." What would change if you replaced that word with "Critique" or "Rank by confidence"? Where in the code would you make that change?
5. Silent failure is the most dangerous failure mode demonstrated. What would a minimal safety net look like — what would you check, and when?
6. Where is the "intelligence" in this system — in the orchestrator, the workers, the synthesizer, or the prompts? What would break first if you removed each one?
7. What would you need to trust this system with something important?

## Instructor Notes

- Part 1's role-conflict demo sets up the entire motivation. Run it without comment first, then ask the room what felt wrong about the output.
- In Part 3, the key moment is showing `dispatch_workers` alongside the orchestrator. Contrast: the orchestrator returns a `dict` (state update); the routing function returns a `list[Send]` (execution requests). Different return types, different semantics.
- Part 4's direct call to `worker_node` is worth pausing on: the worker is just a Python function. The graph machinery is not required to run or test it. This is what isolation buys.
- Part 7 is the course payoff. Read the task strings aloud. Ask: where is the contract written? Answer: inside those strings, in natural language, nowhere else.
- The three Details blocks in Part 7 (miracle, perspectives merge, three levels) are the densest conceptual content in the notebook. Open them selectively — the "three levels" diagram is the most rewarding for audiences who have followed the whole course.
- Part 9's deliberate failure is important to run. The system should not feel magical at the end of the lecture. It is powerful and fragile simultaneously.
