# Lecture 5: Memory Without Words: How Neural Networks Remember

**«Память без слов: как нейронные сети запоминают»**

**Standalone lecture — independent of the AI Agents series (Lectures 1–4).**

Audience: mix of university students, software engineers with math interest, and intelligent non-technical professionals. All have seen RAG, embeddings, and how self-attention works.

Duration: 2 hours.

---

## Central Question

RAG stores text outside the model. NTM stores *vectors* outside the reasoning substrate. Why does that feel different?

The inside/outside distinction in memory is not about location — it is about representation type. A memory can be architecturally external to the weights but still feel deeply "internal" because it is stored and accessed in continuous, distributed (latent) form.

---

## Conceptual Ladder

| Level | Mechanism | Key idea |
|-------|-----------|----------|
| 0 | Frozen weights | The model "knows" things before any conversation begins |
| 1 | Attention / KV cache | Exact lossless working memory — but read-only during inference |
| 2 | NTM | External latent matrix; soft differentiable addressing; the model *learns how to remember* |
| 3 | Memorizing Transformers | Same QKV math as attention, pointed at a bank of past context |
| 4 | Titans | Memory weights updated by gradient descent *during* the forward pass |
| 5 | Mamba / SSMs | History compressed into a fixed hidden state — linear cost, no addressability |

Titans and Mamba are covered conceptually in this lecture; full implementations are candidates for a follow-up lecture.

---

## Files

| File | Purpose |
|------|---------|
| `notebook5.ipynb` | Main lecture notebook — runnable top to bottom |
| `lecture_outline_conceptual.md` | Pure prose version — no code; handout for non-technical attendees |

---

## What the Notebook Builds

- **Section 0** — The memory enigma (framing diagram)
- **Section 1** — Attention as associative memory (deepening + Hopfield connection)
- **Section 2** — NTM from scratch: memory matrix, content-based addressing, read, write, graceful degradation demo
- **Section 3** — Dictionary vs. NTM contrast ("Is that remembering? You decide.")
- **Section 4** — Memorizing Transformers: local + external KV, split attention heatmap
- **Section 5** — Titans (surprise signal visualization), Mamba (markdown), spectrum scatter plot

Dependencies: `torch`, `matplotlib`, `numpy`. No external NTM library. No API keys required.

---

## Possible Follow-up Lectures

- Titans deep dive: implement the surprise-gated memory update
- Mamba / SSM deep dive: build a minimal S4/Mamba cell, needle-in-haystack comparison
- Training internals: how NTM learns to remember (backprop through the memory matrix)
