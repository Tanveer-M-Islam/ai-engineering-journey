# Day 75 — LLM Evaluation Frameworks

## 1. Why LLM Evaluation Matters

Training an LLM does not guarantee that the resulting model is better.

A model can have:

- Lower training loss
- Better perplexity

while still producing:

- Incorrect answers
- Irrelevant answers
- Hallucinations
- Poorly grounded answers
- Unsafe responses

Therefore, LLM applications require dedicated evaluation.

---

## 2. Multiple Evaluation Dimensions

LLM quality has multiple dimensions.

Important dimensions include:

- Correctness
- Relevance
- Helpfulness
- Fluency
- Grounding
- Faithfulness
- Safety
- Latency
- Cost

No single metric captures all of these.

---

## 3. Traditional Metrics

Depending on the task, traditional metrics can include:

Classification:

- Accuracy
- Precision
- Recall
- F1

Text generation:

- BLEU
- ROUGE
- Perplexity

These metrics can be useful, but they do not fully measure open-ended
LLM response quality.

---

## 4. LLM-as-a-Judge

LLM-as-a-Judge uses one LLM to evaluate another model's response.

Conceptually:

Question
   +
Model Response
   ↓
Judge LLM
   ↓
Score / Explanation

Example:

Correctness: 4/5
Relevance: 5/5
Clarity: 4/5

The judge model itself can make mistakes, so judge-based evaluation
should be validated carefully.

---

## 5. RAG Evaluation

RAG systems require additional evaluation.

Important questions include:

### Retrieval Quality

Did the retriever find the correct information?

### Context Relevance

Is the retrieved context relevant to the question?

### Faithfulness / Grounding

Is the generated answer supported by the retrieved context?

### Answer Relevance

Does the answer actually answer the user's question?

### Correctness

Is the final answer factually correct?

---

## 6. Evaluation Frameworks

### Ragas

Ragas is designed especially for evaluating RAG and LLM applications.

It provides metrics related to:

- Faithfulness
- Answer relevance
- Context relevance
- Context recall

### DeepEval

DeepEval is an evaluation framework for LLM applications.

It can be used for:

- LLM-as-a-Judge evaluation
- RAG evaluation
- Custom metrics
- Testing

### LangSmith

LangSmith provides tooling for:

- LLM tracing
- Debugging
- Evaluation
- Monitoring

It is especially useful when working with LangChain/LangGraph
applications.

### Hugging Face Evaluate

Hugging Face Evaluate provides reusable evaluation metrics and
evaluation utilities.

---

## 7. Lexical vs Semantic Evaluation

Lexical similarity compares words.

Example:

Reference:
RAG retrieves information from documents.

Response:
RAG retrieves information from files.

A simple word-overlap metric may consider these different because
some words differ.

However, their meanings may be very similar.

Therefore:

Lexical similarity ≠ Semantic correctness

---

## 8. Production Evaluation

A production AI application should normally evaluate more than
response similarity.

Example:

Quality
+
Correctness
+
Grounding
+
Safety
+
Latency
+
Cost

The exact evaluation criteria depend on the application.

---

## 9. Evaluation Loop

Evaluation should be continuous.

Application
    ↓
Generate Responses
    ↓
Evaluate
    ↓
Find Failures
    ↓
Improve
    ↓
Evaluate Again

This creates an iterative evaluation loop.

---

## 10. Important Takeaway

LLM evaluation is not simply checking whether the generated text
looks similar to a reference answer.

A robust evaluation system measures the properties that actually
matter for the application.

For RAG, grounding and retrieval quality are particularly important.

For production systems, latency, cost, reliability, and safety are
also important.