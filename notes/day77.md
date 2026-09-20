# Day 77 — Model Merging & Adapter Management

## 1. What is a Model Adapter?

A model adapter is a small set of trainable parameters added to a pretrained model.

Instead of updating the complete model, PEFT methods such as LoRA train only a small number of additional parameters.

Basic idea:

W' = W + ΔW

For LoRA:

ΔW = BA

Where:

- W = original model weights
- ΔW = learned update
- B and A = low-rank matrices

---

## 2. Base Model vs Adapter

Base model:

Contains the original pretrained parameters.

Adapter:

Contains task-specific learned parameters.

Together:

Base Model + Adapter = Fine-tuned Model

---

## 3. Why Use Adapters?

Adapters provide:

- Lower storage requirements
- Lower training memory requirements
- Faster experimentation
- Easy task switching
- Multiple task-specific models using one base model

Example:

Base Model
├── Coding Adapter
├── Medical Adapter
└── Customer Support Adapter

---

## 4. Loading an Adapter

PEFT provides:

PeftModel.from_pretrained()

Example:

model = PeftModel.from_pretrained(
    base_model,
    adapter_path
)

This loads the adapter on top of the base model.

---

## 5. Adapter Merging

A LoRA adapter can be merged into the base model.

API:

merged_model = model.merge_and_unload()

Before:

Base Model + LoRA Adapter

After:

Merged Model

The resulting model no longer needs the LoRA adapter separately.

---

## 6. Separate Adapter vs Merged Model

Separate adapter:

Advantages:

- Small adapter files
- Easy to switch adapters
- Multiple adapters can share one base model
- Useful during experimentation

Disadvantages:

- Requires base model
- Requires adapter
- Deployment can be slightly more complicated

Merged model:

Advantages:

- Standalone model
- Simpler deployment
- No PEFT adapter required during inference

Disadvantages:

- Larger storage requirement
- Cannot easily switch the original adapter
- Multiple merged models require multiple copies

---

## 7. Adapter Management Workflow

Typical workflow:

1. Load base model
2. Load adapter
3. Evaluate adapter
4. Compare outputs
5. Merge adapter if required
6. Save merged model
7. Reload merged model
8. Verify inference

---

## 8. Important PEFT APIs

Load adapter:

PeftModel.from_pretrained()

Inspect parameters:

model.print_trainable_parameters()

Merge:

model.merge_and_unload()

Save:

model.save_pretrained()

---

## 9. Adapter Checkpoint

A LoRA checkpoint commonly contains:

adapter_config.json
adapter_model.safetensors

The folder containing these files should be passed to:

PeftModel.from_pretrained()

Do not assume the parent output directory is the adapter directory.

---

## 10. Adapter Switching Concept

One base model can theoretically be used with multiple adapters.

Example:

Base Model
    |
    +-- Adapter A
    |
    +-- Adapter B
    |
    +-- Adapter C

This is useful when different applications require different task-specific behaviors.

---

## 11. When to Merge

Merge when:

- Fine-tuning is complete
- Evaluation is complete
- The adapter is finalized
- A standalone model is desired
- Deployment simplicity is important

Keep separate when:

- Experimenting
- Comparing adapters
- Frequently switching tasks
- Storage efficiency matters
- Multiple adapters share one base model

---

## 12. Important Command

Find LoRA adapter checkpoints:

Get-ChildItem -Recurse -Filter adapter_config.json

---

## 13. Key Takeaway

LoRA allows task-specific knowledge to be stored as a small adapter.

PEFT allows the adapter to be loaded separately.

merge_and_unload() combines the adapter with the base model to produce a standalone model.

Pipeline:

Base Model
    ↓
Load Adapter
    ↓
Evaluate
    ↓
Merge
    ↓
Save
    ↓
Standalone Model