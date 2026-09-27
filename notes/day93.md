# Day 93 — LLM Evaluation & Observability

## 1. LLM Evaluation

LLM evaluation measures the quality and behavior of an LLM system.

Important dimensions include:

- correctness
- relevance
- faithfulness
- safety
- latency
- token usage
- error rate

---

## 2. Quality vs System Metrics

Quality metrics:

- correctness
- relevance
- faithfulness
- completeness
- safety

System metrics:

- latency
- TTFT
- tokens/sec
- token usage
- error rate
- availability

Production systems need both.

---

## 3. Offline Evaluation

Offline evaluation uses a predefined evaluation dataset.

Evaluation Dataset
↓
LLM
↓
Generated Answers
↓
Metrics

Useful for comparing:

- models
- prompts
- RAG configurations
- fine-tuned models
- system versions

---

## 4. Online Evaluation

Online evaluation monitors the deployed application.

Examples:

- user feedback
- errors
- latency
- token usage
- safety violations

---

## 5. Evaluation Dataset

An evaluation dataset contains representative test cases.

It should contain:

- normal cases
- difficult cases
- edge cases
- known failures
- domain-specific cases

---

## 6. Exact Match

Exact match checks whether:

prediction == expected

Useful for structured tasks but limited for open-ended LLM answers.

---

## 7. Semantic Evaluation

Semantic evaluation compares meaning instead of exact wording.

Embeddings can be used to calculate semantic similarity.

Similarity does not automatically guarantee factual correctness.

---

## 8. LLM-as-a-Judge

Another LLM evaluates the generated answer.

Input:

- question
- expected answer/context
- generated answer

Output:

- score
- pass/fail
- evaluation

The judge can also make mistakes.

---

## 9. Correctness

Correctness asks:

Is the answer actually correct?

---

## 10. Faithfulness

Faithfulness asks:

Is the answer supported by the provided context?

Important for RAG systems.

---

## 11. Observability

Observability helps engineers understand what is happening inside
an AI application.

Three pillars:

- logs
- metrics
- traces

---

## 12. LLM Observability Metrics

Useful metrics include:

- latency
- TTFT
- input tokens
- output tokens
- tokens/sec
- error rate
- model name
- prompt version
- retrieval latency
- guardrail results

---

## 13. Request IDs

Every request can receive a unique ID.

This allows engineers to trace a specific request through:

API
↓
Retriever
↓
LLM
↓
Tools
↓
Response

---

## 14. Structured Logging

JSON/JSONL logs make machine processing easier.

Example:

{
    "request_id": "abc123",
    "latency": 2.1,
    "status": "success"
}

---

## 15. Error Rate

Error Rate:

failed requests / total requests

A reliable production system needs both good answer quality and low
system failure rates.

---

## 16. Evaluation in CI/CD

Evaluation can run before deployment.

Code Change
↓
Evaluation
↓
Quality Check
↓
Deploy or Stop

This helps detect regressions.

---

## 17. Task-Specific Evaluation

Classification:

- accuracy
- precision
- recall
- F1

RAG:

- correctness
- faithfulness
- context relevance
- retrieval quality

Agents:

- task completion
- tool correctness
- number of steps
- safety

Production:

- latency
- TTFT
- throughput
- errors
- token usage

---

## 18. Continuous Evaluation Loop

Build
↓
Evaluate
↓
Deploy
↓
Observe
↓
Find Failures
↓
Add Failures to Evaluation Dataset
↓
Improve
↓
Evaluate Again

---

## Key Takeaway

Evaluation tells us whether the AI is performing well.

Observability tells us what the AI system is doing in production.

Strong AI engineering requires both:

Evaluation
+
Logging
+
Metrics
+
Tracing
+
User Feedback
+
Continuous Improvement