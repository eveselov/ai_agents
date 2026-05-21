# Lecture 5: Memory Without Words: How Neural Networks Remember

**«Память без слов: как нейронные сети запоминают»**

**Standalone mini-series of lectures (5abc) — independent of the AI Agents series (Lectures 1–4).**

Audience: mix of university students, software engineers with math interest, and intelligent non-technical professionals. All have seen RAG, embeddings, and how self-attention works.

Duration of each lecture: 2 hours.

Lectures Plan:

- a) What latent representation is?
- b) External latent memory: structure, content-based read/write, location-based addressing
- c) NTM: controller + memory head, trained end-to-end on copy/sort tasks
- d) Memorizing Transformers: extending context with a K/V cache bank
- e) ELM: experiential latent memory experiments

## notebook5b outline

1. **Single-matrix memory** (motivation) — naive design, why it conflates search and content
2. **Split K/V memory** — two parallel matrices, why keys and values live in different spaces
3. **Content-based read** — `r = softmax(q @ K.T / √D_K) @ V`, full visualization
4. **Write: erase-then-add** — differentiable update on V; additive update on K; soft addressing
5. **Location-based addressing** — shift convolution + sharpening scalar γ
6. **Full write→read cycle** — end-to-end demo on split K/V memory

Memory design choice: **split K/V matrices** throughout (not single matrix). Keys are compact search
descriptors; values carry richer content. This matches transformer attention notation and makes
read/write operations structurally transparent. notebook5c NTM will use the same structure.

Status:

| Notebook | Content | Status |
|----------|---------|--------|
| notebook5a | Latent representations | Completed |
| notebook5b | External K/V memory: read, write, addressing | In progress |
| notebook5c | NTM model | Drafted |
| notebook5d | Memorizing Transformers | Drafted |
| notebook5e | ELM | Not started |

To be continued...