import math
import os
import torch

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


# ============================================================
# ⚙️ CONFIGURATION
# ============================================================

MODEL_NAME = "distilgpt2"

TRAIN_FILE = "./train.jsonl"
VALIDATION_FILE = "./validation.jsonl"

OUTPUT_DIR = "./fine_tuned_model"

MAX_LENGTH = 128


# ============================================================
# 🖥️ DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("DAY 71 - LLM EVALUATION & PERPLEXITY")
print("=" * 60)

print(f"Device: {device}")
print(f"Base model: {MODEL_NAME}")


# ============================================================
# 🔤 LOAD TOKENIZER
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# 📚 LOAD DATASETS
# ============================================================

print("\nLoading datasets...")

train_dataset = load_dataset(
    "json",
    data_files=TRAIN_FILE,
)["train"]

validation_dataset = load_dataset(
    "json",
    data_files=VALIDATION_FILE,
)["train"]

print(f"Training examples: {len(train_dataset)}")
print(f"Validation examples: {len(validation_dataset)}")


# ============================================================
# 🔢 TOKENIZATION
# ============================================================

def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH,
    )


print("\nTokenizing datasets...")

tokenized_train = train_dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=train_dataset.column_names,
)

tokenized_validation = validation_dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=validation_dataset.column_names,
)


# ============================================================
# 🧩 DATA COLLATOR
# ============================================================

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)


# ============================================================
# 📊 EVALUATION FUNCTION
# ============================================================

def evaluate_model(model, model_name):
    print(f"\nEvaluating: {model_name}")

    model.to(device)

    evaluation_args = TrainingArguments(
        output_dir="./evaluation_output",

        per_device_eval_batch_size=1,

        report_to="none",

        fp16=False,
        bf16=False,
    )

    trainer = Trainer(
        model=model,
        args=evaluation_args,
        eval_dataset=tokenized_validation,
        processing_class=tokenizer,
        data_collator=data_collator,
    )

    metrics = trainer.evaluate()

    eval_loss = metrics["eval_loss"]

    perplexity = math.exp(eval_loss)

    print(f"Evaluation Loss: {eval_loss:.4f}")
    print(f"Perplexity: {perplexity:.4f}")

    return eval_loss, perplexity


# ============================================================
# 🔵 PRETRAINED MODEL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("PRETRAINED MODEL EVALUATION")
print("=" * 60)

base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

base_model.config.pad_token_id = tokenizer.pad_token_id

base_loss, base_perplexity = evaluate_model(
    base_model,
    "Pretrained distilgpt2"
)


# ============================================================
# 🏋️ FINE-TUNING
# ============================================================

print("\n" + "=" * 60)
print("FINE-TUNING MODEL")
print("=" * 60)

fine_tuned_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

fine_tuned_model.config.pad_token_id = tokenizer.pad_token_id

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    num_train_epochs=5,

    per_device_train_batch_size=2,

    learning_rate=2e-5,

    weight_decay=0.01,

    logging_strategy="steps",

    logging_steps=1,

    save_strategy="epoch",

    report_to="none",

    fp16=False,

    bf16=False,
)


trainer = Trainer(
    model=fine_tuned_model,
    args=training_args,

    train_dataset=tokenized_train,

    processing_class=tokenizer,

    data_collator=data_collator,
)


print("\nStarting fine-tuning...")

trainer.train()


# ============================================================
# 💾 SAVE FINE-TUNED MODEL
# ============================================================

print("\nSaving fine-tuned model...")

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Model saved to: {OUTPUT_DIR}")


# ============================================================
# 🟢 FINE-TUNED MODEL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("FINE-TUNED MODEL EVALUATION")
print("=" * 60)

fine_tuned_model = AutoModelForCausalLM.from_pretrained(
    OUTPUT_DIR
)

fine_tuned_model.config.pad_token_id = tokenizer.pad_token_id

fine_loss, fine_perplexity = evaluate_model(
    fine_tuned_model,
    "Fine-tuned distilgpt2"
)


# ============================================================
# 📈 FINAL COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("FINAL COMPARISON")
print("=" * 60)

print(
    f"{'Model':<25}"
    f"{'Loss':<15}"
    f"{'Perplexity':<15}"
)

print("-" * 55)

print(
    f"{'Pretrained':<25}"
    f"{base_loss:<15.4f}"
    f"{base_perplexity:<15.4f}"
)

print(
    f"{'Fine-tuned':<25}"
    f"{fine_loss:<15.4f}"
    f"{fine_perplexity:<15.4f}"
)

print("=" * 60)


# ============================================================
# 📉 IMPROVEMENT
# ============================================================

loss_improvement = base_loss - fine_loss

perplexity_improvement = base_perplexity - fine_perplexity

print("\nImprovement:")

print(f"Loss improvement: {loss_improvement:.4f}")

print(
    f"Perplexity improvement: "
    f"{perplexity_improvement:.4f}"
)

if base_loss > 0:
    loss_percentage = (
        loss_improvement / base_loss
    ) * 100

    print(
        f"Loss improvement percentage: "
        f"{loss_percentage:.2f}%"
    )

if base_perplexity > 0:
    perplexity_percentage = (
        perplexity_improvement / base_perplexity
    ) * 100

    print(
        f"Perplexity improvement percentage: "
        f"{perplexity_percentage:.2f}%"
    )


# ============================================================
# ✅ FINISHED
# ============================================================

print("\nDay 71 evaluation completed successfully.")