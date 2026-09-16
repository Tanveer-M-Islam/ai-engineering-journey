
---

## `README.md`

```markdown
# Day 66 — LoRA Fine-Tuning

This project demonstrates how to fine-tune a pretrained causal language model using LoRA (Low-Rank Adaptation).

LoRA is a parameter-efficient fine-tuning technique that trains only a small number of adapter parameters while keeping the original model frozen.

---

## Learning Goals

- Understand Parameter-Efficient Fine-Tuning
- Understand LoRA architecture
- Configure LoRA using PEFT
- Apply LoRA to DistilGPT2
- Train adapter parameters
- Compare evaluation before and after training
- Save a LoRA adapter
- Generate text using the adapted model

---

## Technologies

- Python
- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- Hugging Face PEFT
- Accelerate

---

## Project Structure

```text
10-lora-finetuning/
│
├── app.py
├── requirements.txt
├── README.md
├── notes.md
│
├── data/
│   ├── train.jsonl
│   └── validation.jsonl
│
└── outputs/