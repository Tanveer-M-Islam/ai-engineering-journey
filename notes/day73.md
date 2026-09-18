# Day 73 — Post-Training Alignment Overview

## 1. What is Post-Training?

Post-training is the training performed after the initial pretraining
of a language model.

A simplified LLM lifecycle is:

Pretraining
    ↓
Base LLM
    ↓
Post-training
    ↓
Instruction-following / aligned LLM

Pretraining mainly teaches the model language patterns and general
knowledge.

Post-training improves how the model behaves when interacting with
users.

---

## 2. Why is Post-Training Needed?

A pretrained language model is not automatically a good assistant.

It may:

- Continue text instead of answering a question
- Give unnecessarily complicated answers
- Fail to follow instructions
- Produce an undesirable response style
- Behave inconsistently

Post-training helps make the model more useful for practical
applications.

---

## 3. Supervised Fine-Tuning (SFT)

SFT means Supervised Fine-Tuning.

The model learns from examples of desired behavior.

Example:

User:
What is RAG?

Assistant:
RAG retrieves relevant information from documents and provides
that information to an LLM as context before generating an answer.

The model learns the relationship:

Instruction → Desired Response

---

## 4. Preference Learning

Preference learning uses multiple candidate responses.

Example:

Prompt:
Explain RAG simply.

Response A:
RAG is a retrieval-augmented conditional generation architecture.

Response B:
RAG retrieves useful information from documents before an LLM
generates an answer.

If humans prefer B:

Chosen   → Response B
Rejected → Response A

This creates a preference pair.

---

## 5. Preference Dataset

A common conceptual structure is:

{
    "prompt": "...",
    "chosen": "...",
    "rejected": "..."
}

The chosen response is the preferred response.

The rejected response is the less-preferred response.

---

## 6. Reward Model

A reward model learns to assign a score to a response.

Conceptually:

Prompt + Response
       ↓
Reward Model
       ↓
Reward Score

For example:

Response A → 0.30
Response B → 0.85

The higher score indicates that the reward model predicts stronger
preference for that response.

---

## 7. RLHF

RLHF means:

Reinforcement Learning from Human Feedback

A simplified traditional RLHF pipeline is:

Base LLM
   ↓
SFT
   ↓
Preference Data
   ↓
Reward Model
   ↓
Reinforcement Learning
   ↓
Aligned LLM

---

## 8. DPO

DPO means:

Direct Preference Optimization

DPO directly uses preference pairs to optimize the language model.

Conceptually:

Prompt
 ├── Chosen Response
 └── Rejected Response
          ↓
         DPO
          ↓
    Updated LLM

DPO does not require the traditional separate reward-model-plus-RL
pipeline.

---

## 9. LoRA vs Alignment Methods

LoRA and DPO are different concepts.

LoRA:
A parameter-efficient method for updating a model.

SFT:
A supervised training approach.

DPO:
A preference optimization approach.

RLHF:
A preference-based reinforcement learning approach.

Therefore:

LoRA = HOW parameters can be efficiently updated

SFT / DPO / RLHF = WHAT training approach or objective is being used

LoRA can be used during SFT or preference optimization.

---

## 10. Preference Does Not Mean Truth

A preferred answer is not automatically factually correct.

For example, humans may prefer:

- concise answers
- confident answers
- simple answers

But a concise or confident answer can still be incorrect.

Therefore:

Preference ≠ Truth

This is one reason LLM evaluation is important.

---

## 11. Important Takeaway

Post-training changes a model from a general pretrained language model
toward a model that is more useful for specific user-facing behavior.

The major concepts are:

Pretraining
SFT
Preference Data
Reward Models
RLHF
DPO
Alignment