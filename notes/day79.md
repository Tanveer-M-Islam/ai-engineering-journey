# Day 79 — GGUF, GPTQ, AWQ & Local LLM Inference Optimization

## 1. GGUF

GGUF is a model file format used extensively by the llama.cpp ecosystem.

It can contain:

- Model tensors
- Metadata
- Quantization information
- Model configuration
- Tokenizer-related information

GGUF is widely used for local LLM inference.

---

## 2. GGUF Quantization

Common names include:

- Q4_0
- Q4_1
- Q4_K_S
- Q4_K_M
- Q5_K_S
- Q5_K_M
- Q6_K
- Q8_0

The Q number broadly indicates the quantization level.

Example:

Q4 → approximately 4-bit quantization.

However, modern quantization schemes use block structures and additional metadata, so Q4 should not be interpreted as every individual value being stored in exactly four bits without overhead.

---

## 3. GPTQ

GPTQ is a post-training quantization method for large language models.

Basic pipeline:

FP16 Model
↓
GPTQ
↓
Quantized Model
↓
Inference

GPTQ is commonly encountered in GPU-oriented quantized inference workflows.

---

## 4. AWQ

AWQ means:

Activation-aware Weight Quantization.

The method uses activation information to identify important weights and tries to preserve their contribution while quantizing the model.

Basic idea:

Weights
+
Activation information
↓
Identify important weights
↓
Quantize
↓
Efficient inference

---

## 5. GGUF vs GPTQ vs AWQ

Important distinction:

GGUF:
A model file format/ecosystem.

GPTQ:
A post-training quantization method.

AWQ:
An activation-aware post-training quantization method.

They are therefore not simply three names for the same type of technology.

---

## 6. Ollama

Ollama provides a convenient interface for running LLMs locally.

Common commands:

ollama list

ollama run llama3.2

ollama pull llama3.2

ollama rm llama3.2

ollama --version

---

## 7. llama.cpp

llama.cpp is an efficient C/C++ implementation for local LLM inference.

It supports:

- CPU inference
- GPU acceleration
- Quantized models
- GGUF
- Local deployment

---

## 8. CPU vs GPU

CPU:

- Easier hardware requirements
- Generally slower for large LLMs

GPU:

- Better parallel computation
- Usually faster inference
- Requires sufficient VRAM

---

## 9. Context Length

Context length is the amount of token context available to the model.

Examples:

4K
8K
16K
32K

Increasing context length can increase memory requirements.

---

## 10. KV Cache

During autoregressive generation, transformers maintain a Key-Value cache.

Conceptually:

Prompt
↓
Transformer
↓
KV Cache
↓
Next token
↓
Updated KV Cache

The KV cache can consume substantial memory for long contexts.

---

## 11. Model Memory

Total inference memory is not only model weights.

It can include:

- Model weights
- KV cache
- Activations
- Runtime buffers
- Framework overhead

Quantization primarily reduces model-weight memory.

---

## 12. Tokens Per Second

A useful inference metric is:

tokens_per_second =
generated_tokens / elapsed_time

Example:

100 tokens / 5 seconds = 20 tokens/second

---

## 13. Benchmarking

A useful benchmark should control:

- Model
- Quantization
- Prompt
- Output length
- Hardware
- Context
- Runtime
- Batch size

Do not compare tokens/second from unrelated configurations.

---

## 14. Local Inference Optimization

Basic optimization workflow:

1. Establish baseline
2. Measure latency
3. Measure tokens/second
4. Measure memory
5. Apply quantization
6. Measure again
7. Check output quality
8. Adjust context
9. Repeat

Important metrics:

- Quality
- Memory
- Latency
- Throughput

---

## 15. Important Takeaway

A simplified local LLM ecosystem looks like:

Model
↓
Quantization
↓
GGUF / GPTQ / AWQ or another representation
↓
Inference runtime
↓
CPU/GPU
↓
Generated output

GGUF is particularly important in the llama.cpp/Ollama ecosystem.

GPTQ and AWQ are quantization methods.

Ollama makes local model management and inference easier.

llama.cpp provides an efficient inference implementation.

---

## 16. Day 79 Main Lesson

Quantization makes models smaller.

Model formats and quantization methods make those models practical to deploy.

Inference optimization then focuses on:

Memory
+
Latency
+
Throughput
+
Quality