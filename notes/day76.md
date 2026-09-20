# Day 76 — Hallucination Detection & Evaluation

## What Is Hallucination?

LLM hallucination occurs when a model produces information that is incorrect,
fabricated, or unsupported by the available evidence.

## Common Types

### Factual Hallucination

The model generates an incorrect fact.

### Fabrication

The model invents information that does not exist.

### Contextual Hallucination

The answer contradicts the provided context.

### RAG Hallucination

The model generates information that is not supported by retrieved documents.

## Why Hallucinations Happen

Common causes include:

- Incomplete knowledge
- Poor-quality training data
- Missing context
- Weak retrieval
- Ambiguous prompts
- Long/noisy context
- Generation randomness
- Model limitations

## Faithfulness

Faithfulness asks:

"Is the answer supported by the provided context?"

## Correctness

Correctness asks:

"Is the answer actually true?"

These are different concepts.

An answer can be faithful to an incorrect document.

## LLM-as-a-Judge

An LLM can evaluate another model's output.

Typical inputs:

- Question
- Context
- Answer

The evaluator produces a judgment.

Example:

SUPPORTED
UNSUPPORTED

## Evaluation Pipeline

Question
↓
Context
↓
Answer
↓
LLM Judge
↓
Evaluation

## Temperature

Temperature controls generation randomness.

For evaluation:

temperature = 0

can provide more consistent results.

## Important Limitation

LLM judges can also make mistakes.

Therefore, production evaluation should combine:

- Ground-truth evaluation
- Rule-based evaluation
- Retrieval-based evaluation
- LLM-as-a-Judge
- Human evaluation

## RAG Connection

Hallucination detection is especially important in RAG.

The evaluator can check whether generated claims are supported by retrieved documents.

## Key Takeaway

A good LLM system should not only generate answers.

It should also evaluate whether those answers are supported and reliable.