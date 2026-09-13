from datasets import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)


# ============================================================
# 1. Configuration
# ============================================================

MODEL_NAME = "distilgpt2"

OUTPUT_DIR = "./Day64_finetuning_fundamentals"

MAX_LENGTH = 128


# ============================================================
# 2. Small training dataset
# ============================================================

raw_data = [
    {
        "text": "Python is a high-level programming language used for software development."
    },
    {
        "text": "Machine learning allows computers to learn patterns from data."
    },
    {
        "text": "Artificial intelligence enables machines to perform tasks that usually require human intelligence."
    },
    {
        "text": "A REST API allows software applications to communicate over HTTP."
    },
    {
        "text": "FastAPI is a modern Python framework for building APIs."
    },
    {
        "text": "A neural network is composed of interconnected computational layers."
    },
    {
        "text": "Embeddings represent text as numerical vectors."
    },
    {
        "text": "Retrieval augmented generation combines retrieval with language generation."
    },
    {
        "text": "Fine-tuning adapts a pretrained model to a specialized dataset."
    },
    {
        "text": "Transformers use attention mechanisms to process relationships between tokens."
    }
]


# ============================================================
# 3. Create Hugging Face Dataset
# ============================================================

dataset = Dataset.from_list(raw_data)

split_dataset = dataset.train_test_split(
    test_size=0.2,
    seed=42
)

train_dataset = split_dataset["train"]
validation_dataset = split_dataset["test"]

print("=" * 70)
print("DATASET")
print("=" * 70)

print(f"Training examples: {len(train_dataset)}")
print(f"Validation examples: {len(validation_dataset)}")


# ============================================================
# 4. Load tokenizer
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# GPT-2-family models do not define a padding token
# by default, so we use the EOS token as padding.

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")


# ============================================================
# 5. Tokenization function
# ============================================================

def tokenize_function(example):

    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )


# ============================================================
# 6. Tokenize datasets
# ============================================================

tokenized_train_dataset = train_dataset.map(
    tokenize_function,
    batched=False,
    remove_columns=["text"]
)

tokenized_validation_dataset = validation_dataset.map(
    tokenize_function,
    batched=False,
    remove_columns=["text"]
)

print("\nTokenization completed.")

print(
    f"Tokenized training examples: {len(tokenized_train_dataset)}"
)

print(
    f"Tokenized validation examples: {len(tokenized_validation_dataset)}"
)


# ============================================================
# 7. Load pretrained model
# ============================================================

print("\nLoading pretrained model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

model.config.pad_token_id = tokenizer.pad_token_id

print("Model loaded.")


# ============================================================
# 8. Data collator
# ============================================================

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)


# ============================================================
# 9. Training arguments
# ============================================================

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    num_train_epochs=3,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    learning_rate=2e-5,
    weight_decay=0.01,

    logging_strategy="steps",
    logging_steps=10,

    save_strategy="epoch",

    eval_strategy="epoch",

    load_best_model_at_end=True,

    metric_for_best_model="eval_loss",

    greater_is_better=False,

    report_to="none",

    fp16=False,
    bf16=False
)


# ============================================================
# 10. Trainer
# ============================================================

trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=tokenized_train_dataset,

    eval_dataset=tokenized_validation_dataset,

    processing_class=tokenizer,

    data_collator=data_collator
)


# ============================================================
# 11. Evaluate before training
# ============================================================

print("\n" + "=" * 70)
print("EVALUATION BEFORE FINE-TUNING")
print("=" * 70)

before_metrics = trainer.evaluate()

print("\nBefore fine-tuning:")
print(before_metrics)


# ============================================================
# 12. Fine-tune
# ============================================================

print("\n" + "=" * 70)
print("STARTING FINE-TUNING")
print("=" * 70)

trainer.train()


# ============================================================
# 13. Evaluate after training
# ============================================================

print("\n" + "=" * 70)
print("EVALUATION AFTER FINE-TUNING")
print("=" * 70)

after_metrics = trainer.evaluate()

print("\nAfter fine-tuning:")
print(after_metrics)


# ============================================================
# 14. Save model
# ============================================================

print("\nSaving fine-tuned model...")

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Model saved to: {OUTPUT_DIR}")


# ============================================================
# 15. Generate sample output
# ============================================================

print("\n" + "=" * 70)
print("TESTING FINE-TUNED MODEL")
print("=" * 70)

prompt = "Machine learning"

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

outputs = model.generate(
    **inputs,
    max_new_tokens=40,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    pad_token_id=tokenizer.eos_token_id
)

generated_text = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("\nPrompt:")
print(prompt)

print("\nGenerated text:")
print(generated_text)

print("\nFine-tuning completed successfully.")