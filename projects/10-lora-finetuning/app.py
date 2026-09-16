import os
import math
import torch

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)

from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "distilgpt2"

TRAIN_FILE = "data/train.jsonl"
VALIDATION_FILE = "data/validation.jsonl"

OUTPUT_DIR = "outputs/lora_ai_engineering_model"

MAX_LENGTH = 128


# ============================================================
# DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("DAY 66 - LoRA FINE-TUNING")
print("=" * 60)
print(f"Device: {device}")
print(f"Base model: {MODEL_NAME}")


# ============================================================
# LOAD DATASET
# ============================================================

dataset = load_dataset(
    "json",
    data_files={
        "train": TRAIN_FILE,
        "validation": VALIDATION_FILE,
    },
)

print("\nDataset:")
print(dataset)


# ============================================================
# LOAD TOKENIZER
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# TOKENIZATION
# ============================================================

def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )


tokenized_dataset = dataset.map(
    tokenize_function,
    batched=False,
    remove_columns=["text"],
)

print("\nTokenized dataset:")
print(tokenized_dataset)


# ============================================================
# LOAD BASE MODEL
# ============================================================

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

model.config.pad_token_id = tokenizer.pad_token_id


# ============================================================
# LORA CONFIGURATION
# ============================================================

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,

    inference_mode=False,

    r=8,

    lora_alpha=16,

    lora_dropout=0.05,

    target_modules=["c_attn"],
)


# ============================================================
# APPLY LORA
# ============================================================

model = get_peft_model(
    model,
    lora_config,
)


# ============================================================
# PRINT TRAINABLE PARAMETERS
# ============================================================

print("\nTrainable parameter summary:")

model.print_trainable_parameters()


# ============================================================
# DATA COLLATOR
# ============================================================

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)


# ============================================================
# TRAINING ARGUMENTS
# ============================================================

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    num_train_epochs=5,

    per_device_train_batch_size=1,

    per_device_eval_batch_size=1,

    gradient_accumulation_steps=1,

    learning_rate=5e-4,

    weight_decay=0.01,

    logging_steps=1,

    save_strategy="epoch",

    eval_strategy="epoch",

    report_to="none",

    fp16=False,

    save_total_limit=1,
)


# ============================================================
# TRAINER
# ============================================================

trainer = Trainer(
    model=model,

    args=training_args,

    train_dataset=tokenized_dataset["train"],

    eval_dataset=tokenized_dataset["validation"],

    processing_class=tokenizer,

    data_collator=data_collator,
)


# ============================================================
# BEFORE TRAINING EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("BEFORE LORA TRAINING")
print("=" * 60)

before_metrics = trainer.evaluate()

print(before_metrics)

if "eval_loss" in before_metrics:
    before_perplexity = math.exp(before_metrics["eval_loss"])
    print(f"Before-training perplexity: {before_perplexity:.2f}")


# ============================================================
# TRAINING
# ============================================================

print("\n" + "=" * 60)
print("STARTING LORA TRAINING")
print("=" * 60)

trainer.train()


# ============================================================
# AFTER TRAINING EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("AFTER LORA TRAINING")
print("=" * 60)

after_metrics = trainer.evaluate()

print(after_metrics)

if "eval_loss" in after_metrics:
    after_perplexity = math.exp(after_metrics["eval_loss"])
    print(f"After-training perplexity: {after_perplexity:.2f}")


# ============================================================
# SAVE LORA ADAPTER
# ============================================================

print("\nSaving LoRA adapter...")

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

print(f"LoRA adapter saved to: {OUTPUT_DIR}")


# ============================================================
# TEXT GENERATION
# ============================================================

def generate_text(prompt, max_new_tokens=60):
    model.eval()

    generation_device = next(model.parameters()).device

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    inputs = {
        key: value.to(generation_device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model.generate(
            **inputs,

            max_new_tokens=max_new_tokens,

            do_sample=True,

            temperature=0.7,

            top_p=0.9,

            pad_token_id=tokenizer.pad_token_id,
        )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )


# ============================================================
# GENERATION TESTS
# ============================================================

print("\n" + "=" * 60)
print("GENERATION TESTS")
print("=" * 60)

prompts = [
    "Artificial intelligence",
    "Machine learning is",
    "Large language models",
    "Retrieval augmented generation",
]

for prompt in prompts:
    print("\nPrompt:", prompt)

    result = generate_text(prompt)

    print("Generated:", result)


print("\n" + "=" * 60)
print("DAY 66 COMPLETED")
print("=" * 60)