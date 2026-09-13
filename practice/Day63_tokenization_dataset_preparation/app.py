from datasets import Dataset

from transformers import AutoTokenizer


# ============================================================
# 1. Model/tokenizer name
# ============================================================

MODEL_NAME = "distilgpt2"


# ============================================================
# 2. Create a small instruction dataset
# ============================================================

raw_data = [
    {
        "instruction": "Explain Python in one sentence.",
        "input": "",
        "output": "Python is a high-level programming language known for its simplicity."
    },
    {
        "instruction": "What is machine learning?",
        "input": "",
        "output": "Machine learning is a method where computers learn patterns from data."
    },
    {
        "instruction": "What is an API?",
        "input": "",
        "output": "An API allows different software systems to communicate with each other."
    },
    {
        "instruction": "What is a neural network?",
        "input": "",
        "output": "A neural network is a computational model inspired by the human brain."
    },
    {
        "instruction": "Explain overfitting briefly.",
        "input": "",
        "output": "Overfitting happens when a model memorizes training data and performs poorly on new data."
    }
]


# ============================================================
# 3. Convert Python list into Hugging Face Dataset
# ============================================================

dataset = Dataset.from_list(raw_data)

print("=" * 70)
print("RAW DATASET")
print("=" * 70)

print(dataset)

print("\nFirst example:")
print(dataset[0])


# ============================================================
# 4. Train-validation split
# ============================================================

split_dataset = dataset.train_test_split(
    test_size=0.2,
    seed=42
)

train_dataset = split_dataset["train"]
validation_dataset = split_dataset["test"]

print("\n" + "=" * 70)
print("DATASET SPLIT")
print("=" * 70)

print(f"Training examples: {len(train_dataset)}")
print(f"Validation examples: {len(validation_dataset)}")


# ============================================================
# 5. Format instruction examples
# ============================================================

def format_example(example):

    formatted_text = (
        "### Instruction:\n"
        + example["instruction"]
        + "\n\n"
        "### Input:\n"
        + example["input"]
        + "\n\n"
        "### Response:\n"
        + example["output"]
    )

    return {
        "text": formatted_text
    }


formatted_train_dataset = train_dataset.map(
    format_example
)

formatted_validation_dataset = validation_dataset.map(
    format_example
)

print("\n" + "=" * 70)
print("FORMATTED EXAMPLE")
print("=" * 70)

print(formatted_train_dataset[0]["text"])


# ============================================================
# 6. Load tokenizer
# ============================================================

print("\n" + "=" * 70)
print("LOADING TOKENIZER")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# distilgpt2 does not define a padding token by default.
# We reuse the EOS token as the padding token for this demo.

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")


# ============================================================
# 7. Tokenization function
# ============================================================

def tokenize_example(example):

    tokenized = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

    # For causal language modeling, labels are usually
    # copied from input_ids.

    tokenized["labels"] = tokenized["input_ids"].copy()

    return tokenized


# ============================================================
# 8. Tokenize datasets
# ============================================================

tokenized_train_dataset = formatted_train_dataset.map(
    tokenize_example,
    remove_columns=formatted_train_dataset.column_names
)

tokenized_validation_dataset = formatted_validation_dataset.map(
    tokenize_example,
    remove_columns=formatted_validation_dataset.column_names
)


# ============================================================
# 9. Display tokenized dataset
# ============================================================

print("\n" + "=" * 70)
print("TOKENIZED DATASET")
print("=" * 70)

print(tokenized_train_dataset)

first_tokenized_example = tokenized_train_dataset[0]

print("\nInput IDs:")
print(first_tokenized_example["input_ids"])

print("\nAttention Mask:")
print(first_tokenized_example["attention_mask"])

print("\nLabels:")
print(first_tokenized_example["labels"])


# ============================================================
# 10. Decode input IDs
# ============================================================

decoded_text = tokenizer.decode(
    first_tokenized_example["input_ids"],
    skip_special_tokens=True
)

print("\n" + "=" * 70)
print("DECODED TOKENS")
print("=" * 70)

print(decoded_text)


# ============================================================
# 11. Show token count
# ============================================================

non_padding_tokens = sum(
    first_tokenized_example["attention_mask"]
)

print("\n" + "=" * 70)
print("TOKEN STATISTICS")
print("=" * 70)

print(f"Maximum sequence length: 128")
print(f"Actual non-padding tokens: {non_padding_tokens}")
print(
    f"Padding tokens: "
    f"{128 - non_padding_tokens}"
)


# ============================================================
# 12. Final summary
# ============================================================

print("\n" + "=" * 70)
print("PIPELINE COMPLETE")
print("=" * 70)

print("""
Raw Instruction Dataset
        ↓
Hugging Face Dataset
        ↓
Train/Validation Split
        ↓
Instruction Formatting
        ↓
Tokenizer
        ↓
Input IDs
        ↓
Attention Mask
        ↓
Labels
        ↓
Fine-Tuning Ready Dataset
""")