import os
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


# ============================================================
# CONFIGURATION
# ============================================================

BASE_MODEL = "distilgpt2"

# IMPORTANT:
# Change this to the folder that actually contains
# adapter_config.json and adapter_model.safetensors
ADAPTER_PATH = r"C:\MyFiles\AI Engineering 2026\projects\10-lora-finetuning\outputs\lora_ai_engineering_model"

OUTPUT_DIR = "./outputs/merged_model"


# ============================================================
# STEP 1: CHECK ADAPTER
# ============================================================

adapter_config = os.path.join(
    ADAPTER_PATH,
    "adapter_config.json"
)

adapter_weights = os.path.join(
    ADAPTER_PATH,
    "adapter_model.safetensors"
)

if not os.path.exists(ADAPTER_CONFIG := adapter_config):
    raise FileNotFoundError(
        f"adapter_config.json not found:\n{ADAPTER_CONFIG}\n\n"
        "Use the folder containing your actual LoRA adapter."
    )

if not os.path.exists(adapter_weights):
    raise FileNotFoundError(
        f"adapter_model.safetensors not found:\n{adapter_weights}\n\n"
        "Check the adapter checkpoint path."
    )


# ============================================================
# STEP 2: SELECT DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("MODEL MERGING & ADAPTER MANAGEMENT")
print("=" * 60)

print(f"Device: {device}")
print(f"Base model: {BASE_MODEL}")
print(f"Adapter: {ADAPTER_PATH}")


# ============================================================
# STEP 3: LOAD TOKENIZER
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# STEP 4: LOAD BASE MODEL
# ============================================================

print("\nLoading base model...")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL
)

base_model.to(device)


# ============================================================
# STEP 5: LOAD LORA ADAPTER
# ============================================================

print("\nLoading LoRA adapter...")

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH
)

model.to(device)

print("Adapter loaded successfully.")


# ============================================================
# STEP 6: SHOW TRAINABLE PARAMETERS
# ============================================================

print("\nAdapter information:")

model.print_trainable_parameters()


# ============================================================
# STEP 7: GENERATION BEFORE MERGING
# ============================================================

prompt = "Artificial intelligence is"

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}

print("\nGenerating with Base + Adapter...")

with torch.no_grad():

    output = model.generate(
        **inputs,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

adapter_text = tokenizer.decode(
    output[0],
    skip_special_tokens=True
)

print("\nGenerated text:")
print(adapter_text)


# ============================================================
# STEP 8: MERGE ADAPTER
# ============================================================

print("\nMerging adapter into base model...")

merged_model = model.merge_and_unload()

print("Adapter merged successfully.")


# ============================================================
# STEP 9: SAVE MERGED MODEL
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

print("\nSaving merged model...")

merged_model.save_pretrained(
    OUTPUT_DIR,
    safe_serialization=True
)

tokenizer.save_pretrained(
    OUTPUT_DIR
)

print(f"Merged model saved to: {OUTPUT_DIR}")


# ============================================================
# STEP 10: LOAD MERGED MODEL AGAIN
# ============================================================

print("\nReloading merged model for verification...")

del model
del base_model

merged_model = AutoModelForCausalLM.from_pretrained(
    OUTPUT_DIR
)

merged_model.to(device)

merged_model.eval()


# ============================================================
# STEP 11: GENERATE FROM MERGED MODEL
# ============================================================

print("\nGenerating with merged model...")

with torch.no_grad():

    output = merged_model.generate(
        **inputs,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

merged_text = tokenizer.decode(
    output[0],
    skip_special_tokens=True
)

print("\nMerged model output:")
print(merged_text)


# ============================================================
# STEP 12: FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("MODEL MERGING COMPLETED")
print("=" * 60)

print(f"Saved model: {OUTPUT_DIR}")
print("The merged model can now be loaded without the LoRA adapter.")