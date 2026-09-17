# 📅 Day 71 — LLM Evaluation & Perplexity

## 🎯 Main Concepts

LLM evaluation measures how well a model performs on unseen data.

For causal language models, evaluation loss and perplexity are common language-modeling metrics.

---

## 📉 Evaluation Loss

Evaluation loss measures how well the model predicts tokens from the validation dataset.

Lower evaluation loss generally means better next-token prediction on the same evaluation dataset.

---

## 🧮 Perplexity

Perplexity is calculated from evaluation loss.

Formula:

Perplexity = exp(Loss)

Example:

Loss = 2

Perplexity = exp(2)

Perplexity ≈ 7.39

Lower perplexity generally indicates lower uncertainty in next-token prediction.

---

## 📚 Dataset Roles

### Training Dataset

Used to update model parameters.

### Validation Dataset

Used to evaluate the model during development.

### Test Dataset

Used for final evaluation.

---

## 🔄 Evaluation Pipeline

Validation JSONL

↓

Tokenizer

↓

input_ids + attention_mask

↓

Data Collator

↓

labels

↓

Causal Language Model

↓

Evaluation Loss

↓

Perplexity

---

## 🔵 Pretrained Model

The original model before task-specific fine-tuning.

Its evaluation result provides a baseline.

---

## 🟢 Fine-Tuned Model

The pretrained model after additional training on a specialized dataset.

Its evaluation result can be compared against the pretrained baseline.

---

## 📊 Fair Model Comparison

When comparing two models:

- Use the same validation dataset.
- Use the same evaluation procedure.
- Keep preprocessing consistent.
- Compare evaluation loss and perplexity.

---

## ⚠️ Perplexity Limitation

Perplexity does not directly measure:

- Factual correctness
- Hallucination
- Reasoning
- Helpfulness
- Safety
- Instruction following

Therefore, generated responses should also be evaluated.

---

## 🧪 Qualitative Evaluation

Generated responses can be manually inspected for:

- Relevance
- Coherence
- Technical accuracy
- Repetition
- Completeness

---

## 🏁 Key Formula

Perplexity = exp(Evaluation Loss)

---

## 💡 Key Lesson

A lower perplexity indicates better token prediction on the evaluation data, but it does not automatically mean that the model produces better or more factually correct answers.