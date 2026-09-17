# Day 67 Notes — QLoRA Fine-Tuning

## Topic

QLoRA: Quantized Low-Rank Adaptation

QLoRA combines:

Quantization + LoRA + Fine-Tuning

---

## 1. Why QLoRA?

Full fine-tuning of large language models requires significant GPU memory.

For example, a 7-billion-parameter model requires approximately:

- FP32: 28 GB for weights
- FP16: 14 GB for weights
- INT8: 7 GB for weights
- INT4: 3.5 GB for weights

Training requires additional memory for gradients, optimizer states, and activations.

QLoRA reduces memory usage by loading the base model in 4-bit precision and training only small LoRA adapters.

---

## 2. Quantization

Quantization reduces the number of bits used to represent model weights.

Common formats:

- FP32 = 32 bits
- FP16 = 16 bits
- BF16 = 16 bits
- INT8 = 8 bits
- INT4 = 4 bits

Lower precision reduces model memory requirements.

---

## 3. What Is QLoRA?

QLoRA means Quantized Low-Rank Adaptation.

The process is:

1. Load the base model in 4-bit precision
2. Freeze the quantized base model
3. Prepare the model for k-bit training
4. Add LoRA adapters
5. Train only the LoRA parameters
6. Save the adapter

Concept:

4-bit Base Model + LoRA Adapter = QLoRA

---

## 4. QLoRA Architecture

```text
Pretrained Model
       ↓
4-bit Quantization
       ↓
Frozen Quantized Base Model
       ↓
LoRA Adapters
       ↓
Trainable Adapter Parameters