# Day 94 — Advanced LLM Cost & Performance Optimization

## 1. Main Goal

Optimize an LLM application while maintaining acceptable quality.

Important dimensions:

- quality
- cost
- latency
- throughput
- memory

---

## 2. Latency

Latency measures how long a request takes.

Example:

Request -> Model -> Response

Measured using wall-clock time.

---

## 3. TTFT

TTFT means Time to First Token.

It measures how long a streaming application takes to return its
first generated token.

Low TTFT makes chat applications feel responsive.

---

## 4. Throughput

Throughput measures how much work a system processes over time.

Examples:

- requests/second
- tokens/second

Latency and throughput are different metrics.

---

## 5. Token Optimization

LLM applications should avoid unnecessary:

- system prompt tokens
- conversation history
- retrieved context
- output tokens

Reducing tokens can reduce cost and latency.

---

## 6. Context Optimization

Do not automatically send every available document to the model.

For RAG:

Question
↓
Retrieve
↓
Select relevant chunks
↓
Optional reranking
↓
Compact context
↓
LLM

---

## 7. Output Control

Set output limits appropriate to the task.

Classification -> small output

Extraction -> small output

Chat -> medium output

Long-form generation -> larger output

---

## 8. Model Routing

Different requests can use different models.

Simple request -> smaller model

Complex request -> more capable model

Routing can reduce cost and latency.

---

## 9. Semantic Caching

Semantic caching can reuse responses for meaningfully similar
requests.

Prompt
↓
Embedding
↓
Similarity Search
↓
Cache Hit?
↓
Return cached response or call LLM

Use carefully for personalized or changing information.

---

## 10. Batching

Batching processes multiple requests efficiently together.

It can improve:

- GPU utilization
- throughput
- serving efficiency

---

## 11. Quantization

Quantization reduces numerical precision.

Examples:

FP16
INT8
INT4

Benefits may include:

- lower model memory
- easier local deployment
- potentially faster inference

There can be quality and hardware-dependent performance trade-offs.

---

## 12. KV Cache

The KV cache stores transformer key/value states from previous
tokens during autoregressive generation.

Benefits:

- reduces repeated computation
- improves generation efficiency

Cost:

- consumes memory
- grows with context and generation length

---

## 13. Caching Types

Common caching strategies:

- exact response cache
- semantic cache
- embedding cache
- retrieval cache
- prompt/prefix cache

---

## 14. Cold vs Warm Inference

Cold inference may include model-loading overhead.

Warm inference uses an already-loaded model.

Benchmarks should distinguish between them.

---

## 15. RAG Optimization

Possible RAG optimizations:

- reduce irrelevant chunks
- tune top-k
- rerank candidates
- reduce chunk duplication
- cache embeddings
- cache retrieval results
- compress context

Always measure retrieval and answer quality.

---

## 16. Benchmark Metrics

Useful metrics:

- latency
- TTFT
- input tokens
- output tokens
- tokens/sec
- throughput
- memory usage
- cost
- answer quality
- error rate

---

## 17. Production Principle

Never optimize only for cost.

Measure:

Quality
+
Cost
+
Latency
+
Reliability

The best configuration depends on application requirements.

---

## Key Takeaway

Production LLM optimization is a system-level problem.

Important techniques include:

Prompt Optimization
+
Context Optimization
+
Output Limits
+
Model Routing
+
Caching
+
Batching
+
Quantization
+
KV Cache Management
+
RAG Optimization
+
Continuous Benchmarking