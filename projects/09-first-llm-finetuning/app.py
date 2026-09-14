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


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "distilgpt2"

TRAIN_FILE = "data/train.jsonl"
VALIDATION_FILE = "data/validation.jsonl"

OUTPUT_DIR = "outputs/ai_engineering_model"

MAX_LENGTH = 128


# ============================================================
# DEVICE INFORMATION
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 70)
print("FIRST LLM FINE-TUNING PROJECT")
print("=" * 70)

print(f"Base model: {MODEL_NAME}")
print(f"Device: {device}")
print(f"Output directory: {OUTPUT_DIR}")


# ============================================================
# STEP 1: LOAD DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 1: LOADING DATASET")
print("=" * 70)

dataset = load_dataset(
    "json",
    data_files={
        "train": TRAIN_FILE,
        "validation": VALIDATION_FILE,
    },
)

print(dataset)

print(f"Training examples: {len(dataset['train'])}")
print(f"Validation examples: {len(dataset['validation'])}")

print("\nSample training example:")
print(dataset["train"][0])


# ============================================================
# STEP 2: LOAD TOKENIZER
# ============================================================

print("\n" + "=" * 70)
print("STEP 2: LOADING TOKENIZER")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# GPT-2 does not have a default padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f"Vocabulary size: {len(tokenizer)}")
print(f"Padding token: {tokenizer.pad_token}")


# ============================================================
# STEP 3: TOKENIZATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 3: TOKENIZING DATASET")
print("=" * 70)


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

print(tokenized_dataset)

print("\nTokenized sample:")
print(tokenized_dataset["train"][0])


# ============================================================
# STEP 4: LOAD BASE MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 4: LOADING BASE MODEL")
print("=" * 70)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

model.config.pad_token_id = tokenizer.pad_token_id

model.to(device)

print("Base model loaded successfully.")
print(f"Number of parameters: {model.num_parameters():,}")


# ============================================================
# STEP 5: DATA COLLATOR
# ============================================================

print("\n" + "=" * 70)
print("STEP 5: CREATING DATA COLLATOR")
print("=" * 70)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

print("Causal language modeling collator created.")


# ============================================================
# STEP 6: TRAINING ARGUMENTS
# ============================================================

print("\n" + "=" * 70)
print("STEP 6: CONFIGURING TRAINING")
print("=" * 70)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
   

    num_train_epochs=5,

    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,

    gradient_accumulation_steps=1,

    learning_rate=5e-5,
    weight_decay=0.01,

    logging_steps=1,

    save_strategy="epoch",
    eval_strategy="epoch",

    load_best_model_at_end=False,

    report_to="none",

    fp16=False,

    save_total_limit=1,
)

print("Training configuration created.")


# ============================================================
# STEP 7: CREATE TRAINER
# ============================================================

print("\n" + "=" * 70)
print("STEP 7: CREATING TRAINER")
print("=" * 70)

trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],

    processing_class=tokenizer,
    data_collator=data_collator,
)

print("Trainer created successfully.")


# ============================================================
# STEP 8: EVALUATE BEFORE TRAINING
# ============================================================

print("\n" + "=" * 70)
print("STEP 8: EVALUATION BEFORE FINE-TUNING")
print("=" * 70)

before_metrics = trainer.evaluate()

print("Before-training metrics:")
print(before_metrics)

if "eval_loss" in before_metrics:
    before_perplexity = math.exp(before_metrics["eval_loss"])
    print(f"Before-training perplexity: {before_perplexity:.2f}")


# ============================================================
# STEP 9: FINE-TUNE MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 9: STARTING FINE-TUNING")
print("=" * 70)

trainer.train()

print("Fine-tuning completed successfully.")


# ============================================================
# STEP 10: EVALUATE AFTER TRAINING
# ============================================================

print("\n" + "=" * 70)
print("STEP 10: EVALUATION AFTER FINE-TUNING")
print("=" * 70)

after_metrics = trainer.evaluate()

print("After-training metrics:")
print(after_metrics)

if "eval_loss" in after_metrics:
    after_perplexity = math.exp(after_metrics["eval_loss"])
    print(f"After-training perplexity: {after_perplexity:.2f}")


# ============================================================
# STEP 11: SAVE MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 11: SAVING FINE-TUNED MODEL")
print("=" * 70)

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Fine-tuned model saved to: {OUTPUT_DIR}")


# ============================================================
# STEP 12: GENERATION FUNCTION
# ============================================================

def generate_text(prompt, max_new_tokens=50):
    print("\n" + "-" * 70)
    print(f"Prompt: {prompt}")

    model.eval()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    print("Generated text:")
    print(generated_text)

    return generated_text


# ============================================================
# STEP 13: TEST FINE-TUNED MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 13: TESTING FINE-TUNED MODEL")
print("=" * 70)

test_prompts = [
    "Machine learning",
    "Artificial intelligence",
    "Transformers",
    "Retrieval augmented generation",
    "Fine-tuning",
]

for prompt in test_prompts:
    generate_text(prompt)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED")
print("=" * 70)

print(f"Model saved at: {OUTPUT_DIR}")
print("You successfully completed a domain-specific LLM fine-tuning pipeline.")