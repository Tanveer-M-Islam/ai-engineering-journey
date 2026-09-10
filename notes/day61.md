# Day 61 - Hugging Face Transformers

## Main Concepts

Hugging Face provides an ecosystem for machine learning models,
datasets, and AI development.

The Transformers library is widely used for working with
pretrained Transformer models.

## Important Components

### AutoTokenizer

Converts text into token IDs.

Text -> Token IDs

### AutoModelForCausalLM

Loads a pretrained causal language model.

Token IDs -> Model predictions

### from_pretrained()

Loads pretrained tokenizer/model files and weights.

## LLM Inference Flow

Text
↓
Tokenizer
↓
Token IDs
↓
Transformer Model
↓
Predicted Token IDs
↓
Decoder
↓
Generated Text

## Important Generation Parameters

max_new_tokens
Controls how many new tokens can be generated.

temperature
Controls randomness during sampling.

top_p
Controls nucleus sampling.

## Ollama vs Transformers

Ollama:
- Easy local model serving
- Good for applications
- Simple API
- Excellent for local LLM development

Transformers:
- Direct model access
- Tokenizer control
- Fine-tuning
- LoRA
- QLoRA
- PEFT
- Model experimentation

## Important Principle

Ollama helps us USE LLMs.

Transformers helps us UNDERSTAND, MODIFY, TRAIN, and USE LLMs.

## Today's Model

distilgpt2

It is intentionally small for learning Transformer inference.
It is not an instruction-tuned modern chat model.

## Next Topics

Day 62:
LLM Architecture Deep Dive

Day 63:
Tokenization and Dataset Preparation

Day 64:
LLM Fine-Tuning Fundamentals

Day 65:
First LLM Fine-Tuning Project