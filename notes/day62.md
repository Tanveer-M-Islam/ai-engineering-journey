# Day 62 - LLM Architecture Deep Dive

## Decoder-Only LLM

Modern GPT-style LLMs commonly use decoder-only Transformer architectures.

## Main Architecture

Text
↓
Tokenizer
↓
Token IDs
↓
Token Embeddings
↓
Position Information
↓
Transformer Blocks
↓
LM Head
↓
Logits
↓
Next Token

## Transformer Block

A simplified Transformer block contains:

1. Normalization
2. Self-Attention
3. Residual Connection
4. Normalization
5. Feed-Forward Network
6. Residual Connection

## Self-Attention

Self-attention allows token representations to incorporate
information from other tokens.

Basic formula:

Attention(Q,K,V) =
softmax(QK^T / sqrt(d_k))V

Q = Query
K = Key
V = Value

## Causal Attention

Decoder-only LLMs use causal masking so that a token cannot
attend to future tokens during autoregressive prediction.

## Multi-Head Attention

Instead of one attention operation, multiple attention heads
perform attention using different learned projections.

The outputs are combined.

## Feed-Forward Network

The FFN applies learned nonlinear transformations to token
representations.

Simplified:

FFN(X) = W2 * activation(W1X + b1) + b2

Modern LLMs may use gated FFN variants.

## Residual Connections

Residual connections add the input to the transformed output.

Example:

Output = X + Attention(X)

They help information and gradients flow through deep networks.

## Layer Normalization

Normalization stabilizes activations during Transformer processing.

Modern architectures may use LayerNorm or RMSNorm.

## LM Head

The LM head maps final hidden states to vocabulary logits.

Logits represent scores for possible next tokens.

## Autoregressive Generation

LLM generation works conceptually as:

Prompt
↓
Predict next token
↓
Append token
↓
Predict next token
↓
Repeat

## Training

Training:

Input
↓
Prediction
↓
Loss
↓
Backpropagation
↓
Update parameters

## Inference

Inference:

Input
↓
Model
↓
Prediction

No parameter updates occur during normal inference.

## Important Future Connection

Understanding model parameters is necessary for:

- Full fine-tuning
- LoRA
- QLoRA
- PEFT

Day 63:
Tokenization and Dataset Preparation

Day 64:
LLM Fine-Tuning Fundamentals