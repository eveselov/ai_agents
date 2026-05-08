# Latent Memories in LLM

## My Vision of the Lecture

My courses of lectures about LLM and AI agents successfully finished. Now I am considering giving a few lectures on various topics around LLM, ML, AI agents.

The first of those is about latent memory mechanisms. Since I am working on ANIMA ELM (experiential latent memory) and recently learned quite a lot about this, I think I could give an interesting lecture. I am planning to build it around discussing the mechanism suggested by NTM. Comparing it with Memorizing Transformers, maybe other similar mechanisms. I have only 2 hours in my lecture, and the material might be pretty hard to comprehend, so the challenge is how present it at a high conceptual level, that would be interesting to my audience. The audience includes three categories: few young university students, several seasoned software developers with the interest in math, their friends who are neither math nor software specialists - doctors, accountants, business people. All very intelligent and curious.

They already heard of RAG, vector storage, embeddings, cosine similarity. Now I am shifting the focus from LLM wrappers and agentic wrappers into LLM internals. I want to tell the a story that excites and attracts me the most - how memory can work deeply inside the neural networks. They already know how self-attention works in transformers (which is the first level of memorization - within episode). NTM is the next step: also within-episode memory, but a step of storing the information outside the weights, though in latent form. The latent form - is what makes it feel so "internal" even though the memory is actually "external" (it is not outside of the brain, it is outside of its reasoning substrate). Memorizing Transformers use the same effect (with an interesting twist of how QKVs used for tying the local context with "external" one).

Maybe you can suggest other similar angles, ideas and known sources existing in public research and industry.

## Claude Pro Suggestion for this Request: Build a Jupyter Notebook for a Lecture on Latent Memory Mechanisms in Neural Networks

### Context and Goal

I am preparing a two-hour lecture on **latent memory mechanisms inside neural networks**, aimed at a mixed audience: a few university students, several seasoned software developers with mathematical interest, and non-technical professionals (doctors, accountants, business people) — all intelligent and curious. The audience has already attended lectures on LLMs and AI agents. They are familiar with: RAG, vector storage, embeddings, cosine similarity, and how self-attention works in transformers.

This lecture shifts focus from LLM wrappers and agentic patterns **into LLM internals** — specifically, how memory can work *deeply inside* neural networks, at a level more fundamental than retrieval-augmented generation.

The notebook should follow the style of Sebastian Raschka's *"Build a Large Language Model From Scratch"* — meaning: every concept is demonstrated with working Python code, visualizations, and runnable experiments. The philosophy is: **one cell = one conceptual claim**. Code is not there to show machinery — it is there to answer a question the audience is already asking. This constructive approach is intentional: it grounds philosophical discussions in something concrete and visible.

---

### The Conceptual Spine of the Lecture

The central tension is this: **the inside/outside distinction in memory is not about location — it is about representation type.** A memory can be architecturally external to the weights but still feel deeply "internal" because it is stored and accessed in latent (continuous, distributed) form — not as symbolic tokens or raw text. This is what distinguishes the mechanisms in this lecture from RAG, which the audience already knows.

The lecture climbs a conceptual ladder:

**Level 0 — Weights as frozen memory**
The model already "knows" things before any episode begins. This knowledge is baked into billions of parameters at training time and never changes during inference. Analogy: procedural long-term memory in humans — riding a bike. It is not retrieved; it is enacted.

**Level 1 — Attention as working memory (recap and deepen)**
The KV cache lets the model attend to everything said so far in a conversation. It is exact, lossless, and grows with context. But it does not compress, it does not forget, it does not abstract. It is more like reading your own chat history than truly *remembering* a conversation. The audience already understands this level, but the notebook should deepen it slightly — especially the idea that the KV matrix is already an associative memory, just one that cannot be written to.

**Level 2 — Neural Turing Machines (NTM): the first latent external memory**
This is the core of the lecture. NTM separates a *controller* (a neural network doing reasoning) from a *memory matrix* (an external differentiable tape). The memory matrix is written to and read from using soft, differentiable addressing — content-based (cosine similarity over latent vectors) and potentially location-based. Because addressing is differentiable, the whole system trains end-to-end: **the model learns how to remember**. The memory slots hold latent vectors, not tokens — this is what makes it feel "internal" even though it is outside the weights. The Differentiable Neural Computer (DNC, Graves et al. 2016) is a natural follow-on worth mentioning — it adds dynamic allocation and temporal linking.

**Level 3 — Memorizing Transformers: the KV twist**
Instead of inventing a new memory format, Memorizing Transformers reuse the same QKV language the transformer already speaks. An external cache of past (K, V) pairs is retrieved using the same attention mechanism used for local context. The philosophical point: memory access and reasoning use the *same mathematical vocabulary*. The boundary between local context and retrieved memory is architectural, not representational.

**Level 4 — Titans: memory that learns to remember during inference**
Titans (Behrouz et al., 2024, Google Research) introduces a neural long-term memory module whose weights are updated via gradient descent *during the forward pass* — not during training. The key concept is the **surprise metric**: the gradient of the loss with respect to the input measures information novelty. Surprising tokens get written into long-term memory more strongly — just as humans remember unexpected events more vividly. This blurs the boundary between training and inference in a philosophically important way: the model is *learning while it thinks*.

**Level 5 — SSMs / Mamba: memory as compressed hidden state**
A fundamentally different philosophy. Instead of an external addressable memory, Mamba compresses all history into a fixed-size hidden state vector that evolves recurrently. The tradeoff: you gain linear-time efficiency, but you lose addressability — you cannot "look up" a specific past event the way you can query a KV cache. This is the contrast that closes the spectrum: from NTM (expressive, addressable, relatively expensive) → Memorizing Transformers (reuses existing structure) → Mamba (compressed, fast, lossy).

---

### What to Build in the Notebook

The notebook should be divided into clearly labeled sections matching the conceptual ladder above. Here is what each section should contain:

**Section 0: Framing — The Inside/Outside Paradox**
A single markdown cell with a diagram (can be a matplotlib figure or ASCII art embedded in markdown) showing three layers: frozen weights / episodic memory matrix / attention window. This is the only "pure concept" section — everything else is constructive. Optionally: a brief code cell that loads no model but prints the three-way distinction as a structured illustration.

**Section 1: Attention as Associative Memory (Deepening)**
Show a small Q, K, V matrix. Demonstrate that the attention operation is already a soft lookup: a query retrieves a weighted combination of values based on key similarity. Visualize the attention weight heatmap. Then pose the question that motivates Level 2: "What if we could *write* to this matrix during inference, not just read from it?"

**Section 2: NTM Memory — Read and Write from Scratch**
This is the centerpiece. Implement from scratch (no external NTM library):
- A memory matrix M of shape (N_slots × vector_dim), initialized to small random values or zeros
- Content-based addressing: cosine similarity between a query vector and each memory slot → softmax → weight vector over slots
- A memory read operation: weighted sum of memory slots using the address weights
- A memory write operation: erase vector + add vector applied to memory slots, weighted by address

Keep this to roughly 30–50 lines of clean PyTorch. Then run a demonstration:
- Write 4–5 key-value pairs (as latent vectors) into memory sequentially
- Query with exact keys → show perfect retrieval (visualize weights as heatmap: should show sharp peak at correct slot)
- Query with noisy/partial keys → show graceful degradation (weights spread slightly but still peak at correct slot)
- Query with an orthogonal key → show it retrieves something but confidence is diffuse

Visualize the memory matrix state (as a heatmap) before and after writes. Visualize the address weight vector for each query. This is the image that justifies the whole section.

**Section 3: The Associative Memory Contrast**
Side-by-side comparison: exact Python dictionary lookup vs. NTM memory read with a noisy key. The dictionary raises a KeyError. The NTM returns something reasonable. Pose the question: "Is that remembering? You decide." This is the moment where the philosophical question becomes precise and the audience can answer it themselves.

**Section 4: Memorizing Transformers — The KV Cache Extended**
Do not implement a full Memorizing Transformer. Instead:
- Show a minimal self-attention block operating on a short local window
- Concatenate an external memory bank of (K, V) pairs from "past context" to the local KV matrices
- Run attention and visualize which past KV pairs get high attention weight for a given query
- Highlight: the mechanism is identical to local attention — only the *source* of the keys and values differs

The key visualization: an attention heatmap split into "local context" attention weights vs. "external memory" attention weights. Show that for a query that references something from long ago, the external memory weights dominate.

**Section 5: The Surprise Signal (Titans Concept)**
Do not implement a full Titans architecture. Instead, demonstrate the core idea:
- Run a small language model (or a minimal next-token predictor) on a stream of tokens
- For each token, compute the gradient of the loss with respect to the input embedding
- Plot the gradient magnitude across the token stream
- Show that it spikes at semantically surprising or unexpected tokens (you can construct a synthetic sequence where the surprise is predictable and visible)

Label this "the model's highlighter." Connect it to the Titans idea: these are the tokens that would get written into long-term memory most strongly.

**Section 6: Mamba — Memory as Compression**
Use an existing minimal Mamba implementation (or a simplified SSM). Run it on a sequence. Visualize the hidden state vector evolving over time — show it changing with each new token. Then run a needle-in-haystack retrieval test: plant a specific token early in a long sequence, ask the model to retrieve it later. Compare retrieval accuracy against a transformer with a full KV cache. The contrast is the point: the transformer retrieves exactly because it stores exactly; Mamba approximates because it compresses.

**Section 7: The Spectrum Summary**
A final visualization (matplotlib or a rendered table) showing the five mechanisms on two axes: **memory capacity / expressiveness** vs. **computational cost / efficiency**. Optionally add a third axis: **addressability** (can you look up a specific past event?). Place NTM, DNC, Memorizing Transformers, Titans, and Mamba on this spectrum. This is the closing image of the lecture.

---

### Implementation Notes

- Use **PyTorch** throughout. Keep imports minimal: torch, torch.nn.functional, matplotlib, numpy. Avoid heavy dependencies.
- Every visualization should be self-contained in its cell — no state shared across cells for visualization purposes.
- Use **descriptive cell comments** oriented toward the audience question being answered, not toward the implementation mechanics.
- Where an existing reference implementation is used (Mamba, Memorizing Transformers), add a clearly labeled cell at the top of that section that installs or imports it, with a comment explaining that we are borrowing rather than building.
- Memory matrix visualizations should use `imshow` with a diverging colormap (e.g., `RdBu`) so that near-zero values are visually neutral and written values are visible.
- Attention weight heatmaps should use a sequential colormap (e.g., `Blues`) with slot labels on the axes.

---

### A Note on Perspective: What Not to Do Without Code

Before or alongside building the notebook, it is worth preserving a "pure conceptual" version of the lecture outline — the version that lives entirely in markdown cells, without code. This serves as a reference for the higher-level narrative and ensures that if any code section runs long or requires debugging, the conceptual thread can be recovered without losing the room. Consider a companion file `lecture_outline_conceptual.md` that mirrors the notebook structure but contains only the questions, analogies, and claims — no implementation. This is the safety net, and also the document you hand to the non-technical attendees as a reading guide.

---

### Desired Output

A working Jupyter notebook file `latent_memory_lecture.ipynb` with all sections above implemented, runnable top to bottom in a standard Python environment with PyTorch and matplotlib installed. Section headers in markdown. Conceptual framing in markdown before each code block. All visualizations inline. The companion conceptual outline saved as `lecture_outline_conceptual.md`.
