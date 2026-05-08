# Lecture 5 — Latent Memory in Neural Networks
## A Conceptual Reading Guide for Non-Technical Attendees

---

## Section 0: The Memory Paradox — Where Does the Past Live?

Every language model has a window. It reads the text you give it, produces a response, and then — in a fundamental sense — forgets. The next conversation starts fresh. This is not an engineering oversight; it is a deliberate design choice with deep consequences.

So where does the past live? There are three possible answers, and they are not equivalent.

The first is in the **frozen weights** — the billions of parameters that were adjusted during training and have not changed since. The model 'knows' that Paris is the capital of France not because it looked it up, but because that relationship is encoded, distributed across millions of numbers, in the weights themselves. This is permanent but static: the weights cannot be updated during a conversation.

The second is in the **context window** — the tokens currently being processed. This is fully faithful and immediately accessible, but strictly bounded. Tokens that fall outside the window simply cease to exist for the model.

The third — and this is what this lecture is about — is in an **external latent memory**: a structure that lives outside the weights but speaks the same mathematical language as the model's internal representations. Not text. Vectors. Floating-point numbers that the model can write to, read from, and be trained to use effectively.

The question this lecture pursues: what does it mean to store a *vector* rather than a *word*? And why does that difference matter?

---

## Section 1: What Attention Actually Does — And What It Cannot Do

You have probably heard that transformers use 'attention' to relate different parts of a sequence to each other. Here is a more precise way to think about it: attention is already a form of memory retrieval.

When a token asks a question (the query), attention compares that question to all other tokens in the context (the keys) and returns a weighted blend of their content (the values). This is exactly how a library works: you describe what you are looking for, the system finds the closest matches, and returns a combination of the most relevant material.

The difference from a library card catalog is that the match is *soft*. Instead of returning the single most relevant item, attention returns a blend — a little from many sources, weighted by relevance. This is not imprecision; it is a feature. The soft blend is what makes the whole system trainable.

The fundamental limitation is this: attention can only read from what is already in the context window. It cannot write anything new. Every piece of information it can retrieve had to be placed in the context explicitly, before the model started processing. If a fact is not in the window, attention cannot find it — no matter how relevant it is.

This is the question that motivates the rest of the lecture: can we give the model a place to write as well as read, without requiring that everything be in the context first?

---

## Section 2: The Neural Turing Machine — Teaching a Model to Remember

The Neural Turing Machine (NTM), introduced by Graves et al. in 2014, answers that question with a radical proposal: attach a differentiable external memory to a neural network, and train the whole system — the network *and* its memory usage — end to end.

The memory is a matrix: a grid of rows, where each row is a vector. Think of it as a small spreadsheet where each cell contains a floating-point number rather than text. The model can read from any row, or write to any row, during the course of processing a sequence.

**The key insight is how it decides which row to read or write.** Not with an index. Not with a key string. With *similarity*. The model produces a query vector and compares it to every row in memory using cosine similarity — the same geometric measure of closeness used in attention. The result is a probability distribution over rows: 'this row is 60% likely to be the right one, that row is 25% likely, the others contribute a little.' Then the model reads a *blend* of rows, weighted by that distribution.

This soft addressing is the invention that makes everything work. If the model used a hard index — 'read row 4' — the system would not be trainable, because there is no gradient through a discrete choice. The soft blend is differentiable from end to end. Gradients flow backward through the read and write operations, all the way back to the part of the model that decided *what to query* and *where to write*. Over training, the model learns not just what to remember, but *how* to remember it.

A biological analogy: the hippocampus in the brain acts as an index — it does not store memories directly, but it records where memories are distributed across the cortex, and retrieves them by pattern completion. The NTM's content-based addressing is a computational version of this indexing idea. You describe a memory, and the system finds the closest match, even if your description is approximate.

---

## Section 3: Why NTM Memory Is Not a Dictionary

A Python dictionary is exact or broken. You either know the key precisely — down to the last character — or you get an error. There is no in-between.

NTM memory has no such cliff. When you query with a slightly noisy or imperfect cue, the address distribution broadens but does not collapse. You still get something back — a blend that is closest to the correct answer, degraded gracefully by the distance between your query and the stored key.

This is the property called **graceful degradation**, and it matters more than it might seem. Real environments are noisy. Tool outputs are imperfectly formatted. User questions are ambiguous. A memory system that returns something plausible — rather than failing loudly — is strictly more useful in these settings.

There is also a deeper question here. The NTM returns a vector, not a word. It does not say 'Paris'. It returns a high-dimensional floating-point object that represents, geometrically, something close to the correct answer. We can measure how close by computing cosine similarity between the retrieved vector and the stored value. A similarity of 1.0 means perfect recall. A similarity of 0.5 means partial recall — something was retrieved, but degraded.

Is that remembering? The answer you give to that question says something about what you think memory is.

---

## Section 4: Memorizing Transformers — The Elegance of Same-Language Memory

The Neural Turing Machine introduced a seam: the main reasoning network and the external memory system used different mechanisms, different representations, different addressing schemes. The model had to 'switch modes' to access memory.

Memorizing Transformers (Wu et al., 2022) remove the seam. The insight is disarmingly simple: a transformer already knows how to retrieve information from a set of key-value pairs — that is exactly what attention does. So instead of building a new memory access mechanism, just extend the existing one.

When processing a sequence, the model maintains a bank of past key-value pairs from earlier in the document (or from earlier documents). When computing attention, it concatenates these past pairs with the current context's pairs and runs the same attention operation across the full set. The model does not need to know that some keys came from the past and some from the present — it simply finds the most relevant keys, wherever they happen to live.

The architectural elegance is that there is no seam at all. The model's internal language — the geometry of its key and query spaces — is the same for local context and for retrieved memory. There is no translation step, no mode switch. Remembering and reasoning use the same vocabulary. The boundary between 'what I am currently reading' and 'what I am recalling' is a line drawn for our convenience, not for the model's.

---

## Section 5a: Titans — Learning While Thinking

Memorizing Transformers extend the *reach* of attention. Titans (Behrouz et al., 2024, Google Research) change its *nature*.

In every standard transformer, inference is stateless. The weights are frozen after training. Processing a document does not change the model. It reads, it computes, it outputs — and it is the same model at the end as it was at the beginning.

Titans breaks this. The long-term memory module in Titans is not a matrix of vectors. It is a small neural network — a few layers, with its own weights. And those weights are updated via gradient descent *during the forward pass*. The model is literally learning from the sequence it is currently processing.

The mechanism that controls how much to update is the surprise signal. When the model encounters a token that it did not predict well from recent context — an unexpected word, an unusual fact, a shift in topic — the prediction error is large. A large error triggers a larger weight update. Routine, predictable tokens cause smaller updates. The memory module pays more attention to surprising events.

This is not unlike how human memory works. We remember surprising, emotionally significant, or unexpected events more vividly than routine ones. The Titans surprise signal is a computational analog: the model's 'highlighter' is its prediction error.

The deeper implication: the boundary between training and inference, which has been sharp in machine learning for decades, is beginning to blur. A model that updates its weights during inference is learning while thinking. What that means for alignment, for consistency, for safety — these are open questions.

---

## Section 5b: Mamba — Compression Without Addressability

Mamba (Gu & Dao, 2023) does not try to extend attention or add an external memory. It takes a fundamentally different path: replace attention entirely with a recurrent computation that compresses all past history into a fixed-size hidden state.

The idea is similar to the hidden state in a classical recurrent neural network: at each step, the model reads the current token and updates a compact summary of everything it has seen so far. The summary is fixed-size regardless of how long the sequence is. No growing memory bank. No quadratic attention computation. Linear time, constant memory.

The tradeoff is stark and unavoidable. To retrieve a specific past event from NTM or Memorizing Transformer memory, you address it by content — you describe what you are looking for and find the matching slot. With Mamba, there are no slots. Everything is compressed together into a single vector. You cannot 'look up' something from the past; you can only ask what the compressed summary suggests.

A useful analogy: NTM is a filing cabinet with labeled folders. You can find any document by searching the labels. Mamba is a single sheet of paper on which you keep rewriting a summary of everything you have read. The summary gets better and richer, but individual documents are no longer separately accessible. Efficient and lossy, rather than expensive and precise.

Neither is better in absolute terms. Real-time systems processing continuous streams — audio, sensor data, financial ticks — often need constant-memory efficiency. Tasks requiring precise recall of specific past events need addressable memory. The choice is architectural, not moral.

---

## Section 5c: The Spectrum — Where Is Research Going?

If we place all of these mechanisms on two axes — how much they cost to run versus how precisely they can retrieve specific past information — a spectrum emerges.

Mamba sits at the low-cost, low-addressability end. It is fast and memory-efficient, but history is compressed and cannot be directly retrieved. NTM and DNC sit at the high-cost, high-addressability end: full content-based retrieval, but expensive. Memorizing Transformers and Titans sit in the upper-middle: high addressability achieved by extending the existing attention mechanism, at moderate cost.

Standard transformers with their KV cache — which is what most production LLMs use today — sit in the middle of this space. They can retrieve from context, but only from what fits in the window.

The current research direction is *hybrids*. Jamba interleaves Mamba layers with attention layers, trying to capture the efficiency of recurrent compression for long-range structure while preserving attention's precision for local context. Titans combines a fast attention window with a slow memory module that learns during inference — echoing, loosely, dual-process theories of cognition.

The unifying question: can we get the precision of addressable retrieval at the cost of linear computation? Current evidence says no, but the gap is narrowing. Every point on the spectrum is a live research program, and the field has not converged.

What is clear is that the question this lecture began with — where does the past live? — has no single answer. It lives, partly and imperfectly, in all of these places at once. The art of architecture is choosing which combination of imperfections you can live with.
