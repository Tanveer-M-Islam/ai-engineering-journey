# Day 65 Notes — First LLM Fine-Tuning Project

## Main Concepts

- JSONL dataset
- Domain-specific dataset
- Train/validation split
- Tokenization
- Causal language modeling
- Hugging Face Trainer
- Evaluation before training
- Evaluation after training
- Perplexity
- Model saving
- Text generation

## Key Principle

A fine-tuning project should separate:

- Dataset
- Training code
- Model outputs
- Evaluation
- Inference

## Important Limitation

DistilGPT2 is a base causal language model, not an instruction-following chatbot.

## GitHub Rule

Do not push model checkpoints or model.safetensors to GitHub.

Push only:

- app.py
- requirements.txt
- README.md
- notes.md
- Small dataset files

Ignore:

- outputs/
- checkpoint-*/
- model.safetensors
- optimizer.pt