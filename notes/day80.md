# Day 80 — High-Performance LLM Serving

## 1. LLM Serving

LLM serving means deploying a language model so that applications and users can send requests to it.

Basic architecture:

User
↓
API
↓
Inference Server
↓
LLM
↓
GPU
↓
Response

---

## 2. Inference Server

An inference server manages:

- Model loading
- Request handling
- Scheduling
- Batching
- GPU execution
- KV cache
- Streaming
- Concurrency
- API responses
- Monitoring

---

## 3. Latency

Latency is the time required to process a request.

Example:

Request → 2 seconds → Response

Latency = 2 seconds.

---

## 4. Throughput

Throughput measures how much work the system can complete over time.

Examples:

- Requests/second
- Tokens/second

---

## 5. Concurrency

Concurrency means multiple requests are active during overlapping periods.

Example:

R1 ─────────
R2   ─────────
R3      ───────
R4          ───────

---

## 6. Batching

Batching groups multiple requests for processing.

Example:

R1
R2
R3

↓

Batch

↓

GPU

Batching can improve GPU utilization.

---

## 7. Static Batching

A fixed group of requests is processed together.

Example:

[R1 R2 R3]

↓

GPU

↓

Finish

↓

[R4 R5 R6]

---

## 8. Continuous Batching

Continuous batching dynamically changes the active batch.

When one request finishes, another request can enter while other requests continue generating.

This is particularly useful for autoregressive LLM serving.

---

## 9. KV Cache

The KV cache stores key/value information from previous tokens during autoregressive generation.

It avoids repeatedly recomputing information for previous tokens.

The KV cache can consume significant GPU memory.

---

## 10. PagedAttention

PagedAttention is a technique associated with vLLM for efficient KV-cache memory management.

It organizes KV-cache data into manageable blocks/pages.

Goal:

- Reduce memory waste
- Improve memory utilization
- Support more concurrent sequences
- Improve serving efficiency

---

## 11. vLLM

vLLM is a high-throughput LLM inference and serving engine.

Important concepts:

- Continuous batching
- Efficient KV-cache management
- GPU inference
- Concurrent request serving
- OpenAI-compatible APIs

---

## 12. TGI

TGI means Text Generation Inference.

It is a Hugging Face inference server for deploying and serving text-generation models.

It provides production-oriented inference features such as:

- HTTP APIs
- Streaming
- Batching
- GPU inference
- Metrics
- Quantization support

---

## 13. vLLM vs TGI

Both can be used for production LLM serving.

The appropriate choice depends on:

- Model
- Hardware
- Deployment environment
- API requirements
- Performance requirements
- Ecosystem

---

## 14. Serving Metrics

Important metrics include:

- Latency
- Throughput
- Requests/second
- Tokens/second
- Concurrency
- GPU utilization
- GPU memory usage

---

## 15. Production Architecture

A production architecture may look like:

Users
↓
Load Balancer
↓
Inference Servers
↓
vLLM / TGI
↓
GPU
↓
LLM

Multiple inference servers can be deployed for scalability.

---

## 16. Optimization

A basic optimization workflow:

1. Deploy model
2. Establish baseline
3. Test concurrency
4. Measure latency
5. Measure throughput
6. Measure GPU utilization
7. Measure memory
8. Tune batching
9. Tune context length
10. Benchmark again

---

## 17. Important Difference

Ollama:

Easy local model management and inference.

vLLM:

High-throughput LLM serving.

TGI:

Production-oriented text-generation inference server.

llama.cpp:

Efficient local LLM inference implementation.

---

## 18. Main Lesson

Running an LLM is different from serving an LLM.

Local inference:

User
↓
Model
↓
Response

Production serving:

Many Users
↓
API
↓
Scheduler
↓
Batching
↓
KV-cache management
↓
GPU
↓
LLM
↓
Responses

High-performance LLM engineering focuses on using available compute efficiently while maintaining acceptable latency, throughput, quality, cost, and reliability.