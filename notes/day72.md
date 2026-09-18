# Day 72 — Fine-Tuning Evaluation and Adapter Inference

## Main Goal

Evaluate an already-trained LoRA adapter and compare it with the original base model.

## Why Evaluation Matters

Successful training does not automatically mean that the model improved.

We must compare:

- Base model loss
- Fine-tuned model loss
- Base model perplexity
- Fine-tuned model perplexity
- Generated responses

## Workflow

1. Load tokenizer
2. Load validation dataset
3. Format validation examples
4. Tokenize dataset
5. Load base model
6. Evaluate base model
7. Load base model again
8. Attach LoRA adapter
9. Evaluate fine-tuned model
10. Compare metrics
11. Generate responses
12. Save evaluation results

## PeftModel

PeftModel allows an already-trained adapter to be loaded on top of a compatible base model.

Example:

```python
fine_tuned_model = PeftModel.from_pretrained(
    base_model,
    adapter_path
)