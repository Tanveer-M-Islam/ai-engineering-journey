# Day 70 — Fine-Tuning Hyperparameters

## What Are Hyperparameters?

Hyperparameters are training settings selected before or during model
training.

Examples:

- Learning rate
- Batch size
- Number of epochs
- Gradient accumulation
- Warmup ratio
- Weight decay
- Maximum gradient norm

They control how the model learns.

---

## Learning Rate

Learning rate controls the size of each model-weight update.

Example:

```python
learning_rate=2e-4