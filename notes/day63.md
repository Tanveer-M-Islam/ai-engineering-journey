# Day 63 - Tokenization and Dataset Preparation

## Main Idea

A model cannot be fine-tuned directly from raw Python dictionaries.
The dataset must be formatted and tokenized first.

## Dataset Types

### Pretraining Dataset

Large collections of text used to learn general language patterns.

### Instruction Dataset

Contains instruction, input, and output fields.

### Chat Dataset

Contains messages with roles such as user and assistant.

## Dataset Pipeline

Raw Data
↓
Cleaning
↓
Formatting
↓
Tokenizer
↓
Input IDs
↓
Attention Mask
↓
Labels
↓
Training Dataset

## Important Fields

### input_ids

Numerical token representation of text.

### attention_mask

Indicates real tokens and padding tokens.

1 = real token
0 = padding

### labels

Target tokens used to calculate training loss.

For basic causal language modeling, labels are often copied
from input_ids.

## Padding

Padding makes sequences in a batch have compatible lengths.

## Truncation

Truncation cuts sequences longer than max_length.

## Maximum Sequence Length

Controls the maximum number of tokens in each example.

Longer sequences require more memory.

## Causal Language Modeling

The model predicts the next token using previous tokens.

Example:

I love machine -> learning

## Masked Language Modeling

The model predicts masked tokens.

Example:

I love [MASK] learning -> machine

## Dataset Quality Rules

- Correct answers
- Consistent formatting
- Relevant examples
- Diverse examples
- No duplicates
- No train/validation leakage
- No empty outputs
- No corrupted text

## Important Concept

Good data preparation is necessary for successful fine-tuning.

## Next Topics

Day 64:
LLM Fine-Tuning Fundamentals

Day 65:
First LLM Fine-Tuning Project