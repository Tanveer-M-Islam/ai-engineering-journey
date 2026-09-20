# Day 78 — LLM Quantization

## 1. What is Quantization?

LLM quantization reduces the numerical precision used to represent model parameters.

Typical progression:

FP32
↓
FP16 / BF16
↓
INT8
↓
INT4

Lower precision generally reduces memory requirements.

---

## 2. Precision

| Format | Bits | Approx. Bytes/Parameter |
|---|---:|---:|
| FP32 | 32 | 4 |
| FP16 | 16 | 2 |
| BF16 | 16 | 2 |
| INT8 | 8 | 1 |
| INT4 | 4 | 0.5 |

---

## 3. Approximate Model Weight Memory

For a 7B parameter model:

FP32 ≈ 26.08 GB
FP16 ≈ 13.04 GB
BF16 ≈ 13.04 GB
INT8 ≈ 6.52 GB
INT4 ≈ 3.26 GB

These are theoretical weight-memory estimates.

Actual runtime memory is higher because of:

- Activations
- KV cache
- CUDA/framework overhead
- Temporary tensors
- Quantization metadata

---

## 4. Weight Quantization

Weight quantization converts model weights from a higher-precision representation into a lower-precision representation.

Example:

FP16 weights
↓
INT8 or INT4

This reduces model memory.

---

## 5. Activation Quantization

Activation quantization reduces the precision of intermediate neural-network activations.

Example:

Input
↓
Layer
↓
Quantized activation
↓
Next layer

---

## 6. Post-Training Quantization

PTQ applies quantization after the model has already been trained.

Pipeline:

Pretrained Model
↓
Quantization
↓
Quantized Model

No complete retraining is required.

---

## 7. Quantization-Aware Training

QAT incorporates quantization effects during training.

Pipeline:

Training
↓
Simulated quantization
↓
Model learns to tolerate quantization
↓
Quantized model

---

## 8. Quantization Error

Quantization maps continuous numerical values to a smaller set of representable values.

Therefore some numerical information is lost.

Example:

Original:
0.7234

Quantized:
0.72

The difference is quantization error.

---

## 9. Scale

A scale controls the mapping between floating-point values and quantized values.

Simplified example:

q = round(x / scale)

Reconstruction:

x ≈ q × scale

---

## 10. BitsAndBytes

Hugging Face Transformers can use BitsAndBytesConfig for 8-bit and 4-bit model loading.

Example:

from transformers import BitsAndBytesConfig

8-bit:

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True
)

---

## 11. 4-bit Configuration

A common 4-bit configuration:

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

---

## 12. NF4

NF4 means NormalFloat4.

It is designed for efficient 4-bit representation of neural-network weights.

It is especially associated with QLoRA.

---

## 13. Double Quantization

Double quantization reduces the memory overhead associated with quantization parameters.

Conceptually:

Weights
↓
Quantize weights
↓
Quantize quantization constants

---

## 14. Compute Dtype

A quantized model may store weights in 4-bit format while using a higher precision format for computation.

Example:

Storage:
INT4

Computation:
FP16

Therefore storage precision and computation precision are not necessarily the same.

---

## 15. Weight vs Activation Quantization

Weight quantization:

Weights → lower precision

Activation quantization:

Intermediate activations → lower precision

Weight quantization is particularly important for reducing LLM model memory.

---

## 16. Quantization Trade-Off

Advantages:

- Lower memory usage
- Easier local deployment
- Lower hardware requirements
- Potentially faster inference
- Lower deployment cost

Potential disadvantages:

- Quantization error
- Possible quality degradation
- Hardware-specific behavior
- Different methods produce different results

---

## 17. Important Methods

Important LLM quantization technologies:

- BitsAndBytes
- GPTQ
- AWQ
- GGUF

Day 79 will cover GGUF, GPTQ and AWQ in more detail.

---

## 18. Main Takeaway

Quantization reduces the number of bits used to represent model weights.

The basic idea:

FP32
↓
FP16
↓
INT8
↓
INT4

Lower precision generally means lower memory requirements, but the best precision depends on the model, task, hardware and quantization method.