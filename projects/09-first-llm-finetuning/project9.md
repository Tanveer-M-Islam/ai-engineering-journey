# First LLM Fine-Tuning Project

This project demonstrates domain-specific fine-tuning of a pretrained causal language model using Hugging Face Transformers.

## Base Model

distilgpt2

## Domain

AI Engineering and Generative AI concepts

## Workflow

1. Load JSONL dataset
2. Tokenize text
3. Load pretrained model
4. Configure Trainer
5. Evaluate before training
6. Fine-tune model
7. Evaluate after training
8. Save model
9. Generate domain-specific text

## Technologies

- Python
- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- Accelerate

## Important Note

This is an educational fine-tuning project. The model is a small causal language model and is not an instruction-tuned chatbot.