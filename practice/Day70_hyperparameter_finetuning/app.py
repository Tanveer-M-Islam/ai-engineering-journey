import os

import torch

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer,
)


MODEL_NAME = "distilgpt2"

TRAIN_FILE = "data/train.jsonl"
VALIDATION_FILE = "data/validation.jsonl"

OUTPUT_DIR = "outputs"


LEARNING_RATE = 5e-5
NUM_EPOCHS = 2
BATCH_SIZE = 1
GRADIENT_ACCUMULATION_STEPS = 4
WARMUP_RATIO = 0.1
WEIGHT_DECAY = 0.01
MAX_LENGTH = 128


def load_data():
    """
    Load train and validation JSONL datasets.
    """

    dataset = load_dataset(
        "json",
        data_files={
            "train": TRAIN_FILE,
            "validation": VALIDATION_FILE,
        }
    )

    return dataset


def prepare_text(example):
    """
    Combine instruction and response into one training text.
    """

    text = (
        "Instruction: "
        + example["instruction"]
        + "\nResponse: "
        + example["response"]
    )

    return {
        "text": text
    }


def tokenize_function(example, tokenizer):
    """
    Tokenize the prepared text.
    """

    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH,
    )


def build_model_and_tokenizer():
    """
    Load model and tokenizer.
    """

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    model.config.pad_token_id = tokenizer.pad_token_id

    return model, tokenizer


def train_model(dataset, model, tokenizer):
    """
    Train the model using selected hyperparameters.
    """

    tokenized_dataset = dataset.map(
        lambda examples: tokenize_function(
            examples,
            tokenizer
        ),
        batched=True,
        remove_columns=dataset["train"].column_names,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,

        num_train_epochs=NUM_EPOCHS,

        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,

        gradient_accumulation_steps=(
            GRADIENT_ACCUMULATION_STEPS
        ),

        learning_rate=LEARNING_RATE,

        warmup_ratio=WARMUP_RATIO,
        weight_decay=WEIGHT_DECAY,

        logging_steps=1,

        eval_strategy="epoch",
        save_strategy="epoch",

        save_total_limit=1,

        load_best_model_at_end=False,

        report_to="none",

        fp16=torch.cuda.is_available(),

        max_grad_norm=1.0,
    )

    trainer = Trainer(
        model=model,
        args=training_args,

        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],

        processing_class=tokenizer,

        data_collator=data_collator,
    )

    trainer.train()

    evaluation_result = trainer.evaluate()

    print("\n========== EVALUATION ==========")
    print(evaluation_result)

    trainer.save_model(
        os.path.join(OUTPUT_DIR, "final_model")
    )

    tokenizer.save_pretrained(
        os.path.join(OUTPUT_DIR, "final_model")
    )

    return trainer


def main():
    print("Starting hyperparameter experiment...")

    print("\nSelected Hyperparameters:")
    print(f"Learning rate: {LEARNING_RATE}")
    print(f"Epochs: {NUM_EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(
        "Gradient accumulation:",
        GRADIENT_ACCUMULATION_STEPS
    )
    print(f"Warmup ratio: {WARMUP_RATIO}")
    print(f"Weight decay: {WEIGHT_DECAY}")

    dataset = load_data()

    dataset = dataset.map(
        prepare_text
    )

    model, tokenizer = build_model_and_tokenizer()

    train_model(
        dataset,
        model,
        tokenizer
    )

    print("\nTraining completed.")


if __name__ == "__main__":
    main()