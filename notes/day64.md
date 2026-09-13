# Day 64 - LLM Fine-Tuning Fundamentals

## What is Fine-Tuning?

Fine-tuning is the process of training a pretrained model
further on a smaller, specialized dataset.

## Pretraining

Pretraining learns general language patterns from massive
datasets.

## Fine-Tuning

Fine-tuning adapts an existing pretrained model to a specific
domain, task, style, or behavior.

## Fine-Tuning Pipeline

Pretrained Model
↓
Prepared Dataset
↓
Tokenization
↓
Forward Pass
↓
Loss Calculation
↓
Backpropagation
↓
Gradient Update
↓
Fine-Tuned Model

## Forward Pass

The model receives input tokens and produces predictions.

## Loss

Loss measures how different the model prediction is from
the expected target.

Causal language models commonly use cross-entropy loss.

## Backpropagation

Backpropagation calculates gradients of the loss with respect
to model parameters.

## Gradient Descent

Parameters are updated to reduce loss.

theta_new = theta_old - learning_rate * gradient

## Important Training Terms

Epoch:
One complete pass through the dataset.

Batch:
A group of examples processed together.

Learning rate:
Controls the size of parameter updates.

Validation:
Measures generalization on unseen examples.

## Full Fine-Tuning

All or almost all model parameters are updated.

Advantages:
- Maximum adaptation flexibility

Disadvantages:
- High memory and compute cost
- Large storage requirements
- Risk of catastrophic forgetting

## Parameter-Efficient Fine-Tuning

Only a small number of parameters are trained.

Examples:
- LoRA
- QLoRA
- Adapters
- Prefix tuning
- Prompt tuning

## Catastrophic Forgetting

A model may lose previously learned capabilities when
fine-tuned too aggressively on a narrow dataset.

## Overfitting

The model memorizes the training data and performs poorly
on validation data.

Typical warning:

Training loss decreases while validation loss increases.

## Trainer

Hugging Face Trainer manages the standard training loop,
evaluation, logging, checkpointing, and optimization.

## Important Principle

Fine-tuning does not create a model from zero.
It adapts an already pretrained model.

## Next Topics

Day 65:
First LLM Fine-Tuning Project

Day 66:
LoRA

Day 67:
QLoRA