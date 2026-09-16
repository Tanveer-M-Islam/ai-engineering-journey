# Day 66 Notes — LoRA Fine-Tuning

## Topic

Parameter-Efficient Fine-Tuning using LoRA.

---

## 1. Full Fine-Tuning

Full fine-tuning updates all or most parameters of a pretrained model.

Advantages:

- Maximum adaptation capacity
- Can significantly adapt the model to a new domain

Disadvantages:

- Requires high GPU memory
- Training is expensive
- Produces a large model checkpoint
- Difficult to maintain multiple task-specific versions

---

## 2. Parameter-Efficient Fine-Tuning

PEFT updates only a small number of parameters while keeping the original model frozen.

Examples:

- LoRA
- Prefix Tuning
- Prompt Tuning
- Adapters
- IA3

---

## 3. LoRA

LoRA means Low-Rank Adaptation.

Instead of directly updating the original weight matrix:

W

LoRA learns a low-rank update:

ΔW = BA

The updated weight becomes:

W' = W + BA

Where:

- W = frozen pretrained weight
- A = trainable low-rank matrix
- B = trainable low-rank matrix

---

## 4. LoRA Rank

The rank is controlled using:

r=8

Lower rank:

- Fewer trainable parameters
- Lower memory usage
- Lower adaptation capacity

Higher rank:

- More trainable parameters
- Higher memory usage
- Higher adaptation capacity

Common values:

- 4
- 8
- 16
- 32
- 64

---

## 5. LoRA Alpha

Example:

lora_alpha=16

LoRA alpha controls the scaling of the LoRA update.

A common relationship is:

scaling = lora_alpha / r

For this project:

lora_alpha / r = 16 / 8 = 2

---

## 6. LoRA Dropout

Example:

lora_dropout=0.05

Dropout helps reduce overfitting in the adapter layers.

---

## 7. Target Modules

LoRA must be applied to suitable layers in the model.

For DistilGPT2:

target_modules=["c_attn"]

Different model architectures use different names.

Examples:

GPT-2:

- c_attn

LLaMA/Mistral:

- q_proj
- k_proj
- v_proj
- o_proj

BERT:

- query
- value

---

## 8. Important PEFT Functions

### LoraConfig

Defines the LoRA configuration.

```python
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["c_attn"],
)