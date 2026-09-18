import os
import math
import json
import torch

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer,
)

from peft import PeftModel


# ============================================================
# CONFIGURATION
# ============================================================

BASE_MODEL_NAME = "distilgpt2"

ADAPTER_PATH = "../../projects/10-lora-finetuning/outputs/lora_ai_engineering_model/checkpoint-150"

VALIDATION_FILE = "../../projects/10-lora-finetuning/data/validation.jsonl"

RESULTS_DIR = "results"

MAX_LENGTH = 128


# ============================================================
# CREATE RESULTS DIRECTORY
# ============================================================

os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("ADAPTER EVALUATION")
print("=" * 60)
print(f"Device: {device}")


# ============================================================
# LOAD TOKENIZER
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# LOAD VALIDATION DATASET
# ============================================================

print("Loading validation dataset...")

dataset = load_dataset(
    "json",
    data_files=VALIDATION_FILE,
)

validation_dataset = dataset["train"]


# ============================================================
# FORMAT DATASET
# ============================================================

# ============================================================
# INSPECT DATASET
# ============================================================

print("\nDataset columns:", validation_dataset.column_names)
print("First example:", validation_dataset[0])


# ============================================================
# FORMAT DATASET
# ============================================================

def format_example(example):
    if "instruction" in example and "response" in example:
        instruction = example["instruction"]
        response = example["response"]

        text = (
            f"### Instruction:\n"
            f"{instruction}\n\n"
            f"### Response:\n"
            f"{response}"
        )

    elif "text" in example:
        text = example["text"]

    else:
        raise KeyError(
            "Dataset must contain either "
            "instruction/response columns or a text column."
        )

    return {
        "text": text
    }


formatted_dataset = validation_dataset.map(format_example)


# ============================================================
# TOKENIZATION
# ============================================================

def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH,
    )


tokenized_dataset = formatted_dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=formatted_dataset.column_names,
)


# ============================================================
# DATA COLLATOR
# ============================================================

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate_model(model, model_name):
    print(f"\nEvaluating: {model_name}")

    model = model.to(device)

    training_args = TrainingArguments(
        output_dir=f"./temp_{model_name}",
        per_device_eval_batch_size=1,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        eval_dataset=tokenized_dataset,
        processing_class=tokenizer,
        data_collator=data_collator,
    )

    metrics = trainer.evaluate()

    eval_loss = metrics["eval_loss"]

    try:
        perplexity = math.exp(eval_loss)
    except OverflowError:
        perplexity = float("inf")

    print(f"Evaluation Loss: {eval_loss:.4f}")
    print(f"Perplexity: {perplexity:.4f}")

    return {
        "model": model_name,
        "evaluation_loss": round(eval_loss, 4),
        "perplexity": round(perplexity, 4),
    }


# ============================================================
# LOAD BASE MODEL
# ============================================================

print("\nLoading base model...")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME
)

base_model.config.pad_token_id = tokenizer.pad_token_id


# ============================================================
# EVALUATE BASE MODEL
# ============================================================

base_results = evaluate_model(
    base_model,
    "base_model"
)


# ============================================================
# RELEASE BASE MODEL MEMORY
# ============================================================

del base_model

if torch.cuda.is_available():
    torch.cuda.empty_cache()


# ============================================================
# LOAD BASE MODEL AGAIN
# ============================================================

print("\nReloading base model for adapter...")

adapter_base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME
)

adapter_base_model.config.pad_token_id = tokenizer.pad_token_id


# ============================================================
# CHECK ADAPTER PATH
# ============================================================

if not os.path.exists(ADAPTER_PATH):
    raise FileNotFoundError(
        f"Adapter path does not exist: {ADAPTER_PATH}"
    )


# ============================================================
# LOAD LORA ADAPTER
# ============================================================

print("Loading LoRA adapter...")

fine_tuned_model = PeftModel.from_pretrained(
    adapter_base_model,
    ADAPTER_PATH
)


# ============================================================
# EVALUATE FINE-TUNED MODEL
# ============================================================

fine_tuned_results = evaluate_model(
    fine_tuned_model,
    "fine_tuned_model"
)


# ============================================================
# COMPARE RESULTS
# ============================================================

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(
    f"Base Model Loss:       "
    f"{base_results['evaluation_loss']}"
)

print(
    f"Fine-Tuned Model Loss:  "
    f"{fine_tuned_results['evaluation_loss']}"
)

print(
    f"Base Model Perplexity:  "
    f"{base_results['perplexity']}"
)

print(
    f"Fine-Tuned Perplexity:  "
    f"{fine_tuned_results['perplexity']}"
)


loss_difference = (
    base_results["evaluation_loss"]
    - fine_tuned_results["evaluation_loss"]
)

perplexity_difference = (
    base_results["perplexity"]
    - fine_tuned_results["perplexity"]
)

print(f"\nLoss Difference: {loss_difference:.4f}")
print(f"Perplexity Difference: {perplexity_difference:.4f}")


# ============================================================
# SAVE METRICS
# ============================================================

comparison_results = {
    "base_model": base_results,
    "fine_tuned_model": fine_tuned_results,
    "loss_difference": round(loss_difference, 4),
    "perplexity_difference": round(perplexity_difference, 4),
}

results_file = os.path.join(
    RESULTS_DIR,
    "evaluation_results.json"
)

with open(results_file, "w", encoding="utf-8") as file:
    json.dump(
        comparison_results,
        file,
        indent=4
    )

print(f"\nResults saved to: {results_file}")


# ============================================================
# GENERATION FUNCTION
# ============================================================

def generate_response(model, prompt):
    model.eval()

    formatted_prompt = (
        f"### Instruction:\n"
        f"{prompt}\n\n"
        f"### Response:\n"
    )

    inputs = tokenizer(
        formatted_prompt,
        return_tensors="pt"
    )

    generation_device = next(model.parameters()).device

    inputs = {
        key: value.to(generation_device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )


# ============================================================
# GENERATION TEST
# ============================================================

print("\n" + "=" * 60)
print("GENERATION COMPARISON")
print("=" * 60)

test_prompts = [
    "What is machine learning?",
    "What is Python?",
    "What is artificial intelligence?",
]


for prompt in test_prompts:
    print("\n" + "-" * 60)
    print(f"Prompt: {prompt}")

    print("\nFine-tuned model response:")

    response = generate_response(
        fine_tuned_model,
        prompt
    )

    print(response)


print("\nEvaluation completed successfully.")