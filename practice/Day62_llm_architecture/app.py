import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


# ============================================================
# 1. Model
# ============================================================

MODEL_NAME = "distilgpt2"


# ============================================================
# 2. Load tokenizer
# ============================================================

print("=" * 70)
print("LLM Architecture Inspection")
print("=" * 70)

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Tokenizer loaded.")


# ============================================================
# 3. Load model
# ============================================================

print("\nLoading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

print("Model loaded.")


# ============================================================
# 4. Display model architecture
# ============================================================

print("\n" + "=" * 70)
print("MODEL ARCHITECTURE")
print("=" * 70)

print(model)


# ============================================================
# 5. Model configuration
# ============================================================

print("\n" + "=" * 70)
print("MODEL CONFIGURATION")
print("=" * 70)

config = model.config

print(f"Model type: {config.model_type}")
print(f"Vocabulary size: {config.vocab_size}")
print(f"Hidden size: {config.n_embd}")
print(f"Number of layers: {config.n_layer}")
print(f"Number of attention heads: {config.n_head}")
print(f"Maximum position embeddings: {config.n_positions}")


# ============================================================
# 6. Tokenization example
# ============================================================

text = "Artificial intelligence is powerful."

print("\n" + "=" * 70)
print("TOKENIZATION")
print("=" * 70)

print(f"\nOriginal text:\n{text}")

tokens = tokenizer.tokenize(text)

print("\nTokens:")
print(tokens)

token_ids = tokenizer.encode(text)

print("\nToken IDs:")
print(token_ids)


# ============================================================
# 7. Tensor representation
# ============================================================

inputs = tokenizer(
    text,
    return_tensors="pt"
)

print("\nInput tensor:")
print(inputs["input_ids"])

print("\nTensor shape:")
print(inputs["input_ids"].shape)


# ============================================================
# 8. Parameter count
# ============================================================

total_parameters = sum(
    parameter.numel()
    for parameter in model.parameters()
)

trainable_parameters = sum(
    parameter.numel()
    for parameter in model.parameters()
    if parameter.requires_grad
)

print("\n" + "=" * 70)
print("PARAMETERS")
print("=" * 70)

print(
    f"Total parameters: "
    f"{total_parameters:,}"
)

print(
    f"Trainable parameters: "
    f"{trainable_parameters:,}"
)


# ============================================================
# 9. Model data type
# ============================================================

first_parameter = next(
    model.parameters()
)

print("\n" + "=" * 70)
print("MODEL DATA TYPE")
print("=" * 70)

print(
    f"Model dtype: "
    f"{first_parameter.dtype}"
)


# ============================================================
# 10. Summary
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
Text
 ↓
Tokenizer
 ↓
Token IDs
 ↓
Embedding
 ↓
Transformer Blocks
 ↓
LM Head
 ↓
Logits
 ↓
Next Token
""")