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
    BitsAndBytesConfig,
)

from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

TRAIN_FILE = "data/train.jsonl"
VALIDATION_FILE = "data/validation.jsonl"

OUTPUT_DIR = "outputs/qlora_tinyllama"

MAX_LENGTH = 256


# ============================================================
# DEVICE CHECK
# ============================================================

print("=" * 70)
print("DAY 67 - QLoRA FINE-TUNING")
print("=" * 70)

if not torch.cuda.is_available():
    raise RuntimeError(
        "QLoRA requires a compatible CUDA-enabled NVIDIA GPU. "
        "Run this project on Kaggle or Google Colab GPU."
    )

device = "cuda"

print(f"Device: {device}")
print(f"GPU: {torch.cuda.get_device_name(0)}")


# ============================================================
# 4-BIT QUANTIZATION CONFIGURATION
# ============================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,

    bnb_4bit_quant_type="nf4",

    bnb_4bit_use_double_quant=True,

    bnb_4bit_compute_dtype=torch.float16,
)


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

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
)

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
# LOAD 4-BIT MODEL
# ============================================================

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,

    quantization_config=bnb_config,

    device_map="auto",

    torch_dtype=torch.float16,
)

model.config.pad_token_id = tokenizer.pad_token_id


# ============================================================
# PREPARE MODEL FOR K-BIT TRAINING
# ============================================================

model = prepare_model_for_kbit_training(model)


# ============================================================
# LORA CONFIGURATION
# ============================================================

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,

    inference_mode=False,

    r=8,

    lora_alpha=16,

    lora_dropout=0.05,

    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
)


# ============================================================
# APPLY LORA
# ============================================================

model = get_peft_model(
    model,
    lora_config,
)


# ============================================================
# TRAINABLE PARAMETERS
# ============================================================

print("\nTrainable parameters:")

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

    num_train_epochs=3,

    per_device_train_batch_size=1,

    per_device_eval_batch_size=1,

    gradient_accumulation_steps=4,

    learning_rate=2e-4,

    logging_steps=1,

    save_strategy="epoch",

    eval_strategy="epoch",

    report_to="none",

    fp16=True,

    gradient_checkpointing=True,

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
# BEFORE TRAINING
# ============================================================

print("\n" + "=" * 70)
print("BEFORE TRAINING")
print("=" * 70)

before_metrics = trainer.evaluate()

print(before_metrics)

if "eval_loss" in before_metrics:
    print(
        "Before-training perplexity:",
        math.exp(before_metrics["eval_loss"]),
    )


# ============================================================
# TRAINING
# ============================================================

print("\n" + "=" * 70)
print("STARTING QLoRA TRAINING")
print("=" * 70)

trainer.train()


# ============================================================
# AFTER TRAINING
# ============================================================

print("\n" + "=" * 70)
print("AFTER TRAINING")
print("=" * 70)

after_metrics = trainer.evaluate()

print(after_metrics)

if "eval_loss" in after_metrics:
    print(
        "After-training perplexity:",
        math.exp(after_metrics["eval_loss"]),
    )


# ============================================================
# SAVE ADAPTER
# ============================================================

print("\nSaving QLoRA adapter...")

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Adapter saved to: {OUTPUT_DIR}")


print("\n" + "=" * 70)
print("DAY 67 COMPLETED")
print("=" * 70)