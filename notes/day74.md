# Day 74 — RLHF, DPO & Preference Optimization

## 1. Preference Optimization

Preference optimization teaches a model which responses are preferred.

Basic data:

Prompt
 ├── Chosen Response
 └── Rejected Response

The training process attempts to increase the likelihood of preferred
behavior and reduce the likelihood of less-preferred behavior.

---

## 2. RLHF

RLHF means:

Reinforcement Learning from Human Feedback

Traditional conceptual pipeline:

Base LLM
    ↓
SFT
    ↓
Candidate responses
    ↓
Human preferences
    ↓
Reward Model
    ↓
Reinforcement Learning
    ↓
Aligned LLM

---

## 3. Reward Model

A reward model predicts how desirable a response is.

Input:

Prompt + Response

Output:

Reward score

Example:

Response A → 0.25
Response B → 0.82

The reward model predicts that B is preferred.

---

## 4. PPO

PPO means:

Proximal Policy Optimization

It is a reinforcement learning algorithm that can be used to update
the language model using reward signals.

Conceptually:

LLM
 ↓
Generate response
 ↓
Reward Model
 ↓
Reward
 ↓
PPO
 ↓
Updated LLM

As an AI engineer, it is more important to understand where PPO fits
than to implement PPO from scratch.

---

## 5. DPO

DPO means:

Direct Preference Optimization

DPO directly works with preference pairs.

Input:

Prompt
Chosen Response
Rejected Response

Training:

Preference Data
      ↓
     DPO
      ↓
Updated LLM

---

## 6. RLHF vs DPO

Traditional RLHF:

Preference Data
      ↓
Reward Model
      ↓
PPO / RL
      ↓
LLM

DPO:

Preference Data
      ↓
DPO
      ↓
LLM

DPO removes the need for the traditional separate reward-model and
PPO pipeline.

---

## 7. Preference Margin

A simple conceptual preference margin is:

Chosen Score - Rejected Score

Example:

Chosen = 0.90
Rejected = 0.40

Margin = 0.50

A positive margin means the chosen response receives a higher score.

---

## 8. Important Limitation

Our Day 74 Python evaluator is a toy demonstration.

It is NOT:

- A real reward model
- A real RLHF system
- A real DPO implementation
- A production-quality evaluator

Its purpose is to demonstrate the idea of comparing preferred and
rejected responses.

---

## 9. Real-World Example

Coding assistant:

Prompt:
Fix this Python function.

Response A:
Provides a long explanation but does not actually fix the code.

Response B:
Fixes the code and briefly explains the bug.

Human preference:

Chosen   → B
Rejected → A

Preference optimization attempts to make the model more likely to
produce behavior similar to the preferred response.

---

## 10. LoRA + DPO

LoRA can be used to make DPO training more memory-efficient.

Conceptually:

Base LLM
   ↓
DPO + LoRA
   ↓
Preference-aligned adapter

Therefore:

LoRA = parameter-efficient update technique

DPO = preference optimization method

---

## 11. Key Takeaway

RLHF uses preference feedback through a reward-based reinforcement
learning pipeline.

DPO directly optimizes from preference pairs.

Both aim to improve model behavior according to a preference signal.