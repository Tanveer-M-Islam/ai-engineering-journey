import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


# --------------------------------------------------
# 1. Model name
# --------------------------------------------------

MODEL_NAME = "distilgpt2"


# --------------------------------------------------
# 2. Select device
# --------------------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("Hugging Face Transformer Demo")
print("=" * 60)

print(f"Device: {device}")
print(f"Model: {MODEL_NAME}")


# --------------------------------------------------
# 3. Load tokenizer
# --------------------------------------------------

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Tokenizer loaded.")


# --------------------------------------------------
# 4. Load model
# --------------------------------------------------

print("\nLoading model...")

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

model = model.to(device)

model.eval()

print("Model loaded.")


# --------------------------------------------------
# 5. Input text
# --------------------------------------------------

prompt = "Artificial intelligence is changing the world because"

print("\nPrompt:")
print(prompt)


# --------------------------------------------------
# 6. Tokenize
# --------------------------------------------------

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

print("\nToken IDs:")

print(inputs["input_ids"])


# --------------------------------------------------
# 7. Move input to device
# --------------------------------------------------

inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}


# --------------------------------------------------
# 8. Generate text
# --------------------------------------------------

print("\nGenerating text...")

with torch.no_grad():

    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )


# --------------------------------------------------
# 9. Decode output
# --------------------------------------------------

generated_text = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)


# --------------------------------------------------
# 10. Display result
# --------------------------------------------------

print("\nGenerated Text:")
print("-" * 60)
print(generated_text)
print("-" * 60)