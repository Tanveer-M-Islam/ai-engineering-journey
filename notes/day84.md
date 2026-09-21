# Day 84 — LLM API Observability

## 1. What is Observability?

Observability is the ability to understand the internal behavior of a system using information produced by that system.

For LLM applications, observability includes:

- Request information
- Errors
- Latency
- Token usage
- Model information
- Generation speed
- Retrieval information
- Resource usage

---

## 2. Three Pillars

The traditional three pillars are:

1. Logs
2. Metrics
3. Traces

---

## 3. Logs

Logs record events.

Examples:

request_started
request_completed
request_failed

Logs answer:

"What happened?"

---

## 4. Metrics

Metrics are numerical measurements.

Examples:

- Request count
- Error count
- Error rate
- Average latency
- Token count
- Tokens per second

Metrics answer:

"How much, how often, or how fast?"

---

## 5. Traces

A trace follows a request across multiple components.

Example:

Request
↓
Authentication
↓
Prompt processing
↓
Retriever
↓
LLM
↓
Response

Traces answer:

"Where did the time go?"

---

## 6. LLM-Specific Observability

LLM systems need additional metrics beyond traditional APIs.

Important metrics:

- Input tokens
- Output tokens
- Total tokens
- Model
- Latency
- Tokens per second
- Time to First Token
- Retrieval latency
- Context size

---

## 7. Request ID

Every request should have a unique identifier.

Example:

request_id = uuid.uuid4()

This allows logs and traces belonging to one request to be correlated.

---

## 8. Latency

Latency measures how long a request takes.

Example:

Request
↓
LLM generation
↓
Response

If the total time is 3 seconds:

Latency = 3 seconds

---

## 9. Time To First Token

TTFT is the time from the request until the first generated token arrives.

It is especially important for streaming LLM applications.

Example:

Request
↓
450 ms
↓
First token

TTFT = 450 ms

---

## 10. Tokens Per Second

A simple generation-speed metric:

tokens_per_second =
output_tokens / generation_time

Example:

100 tokens / 5 seconds = 20 tokens/sec

---

## 11. Input and Output Tokens

Input tokens represent the prompt/context sent to the model.

Output tokens represent generated tokens.

Tracking them helps with:

- Cost estimation
- Performance analysis
- Capacity planning
- Debugging
- Usage monitoring

---

## 12. Structured Logging

Instead of plain text:

"Model completed"

structured logging stores machine-readable data.

Example:

{
    "event": "llm_completed",
    "request_id": "abc123",
    "model": "llama3.2",
    "latency_ms": 1800,
    "output_tokens": 120
}

---

## 13. JSONL

JSONL means JSON Lines.

Each line contains one JSON object.

Example:

{"event":"request_started"}
{"event":"request_completed"}
{"event":"request_started"}
{"event":"request_completed"}

JSONL is useful for log processing and ingestion.

---

## 14. Error Rate

Error rate:

error rate =
failed requests / total requests × 100

Example:

20 failed requests
1000 total requests

Error rate = 2%

---

## 15. LLM Observability Architecture

Client
↓
API
↓
Retriever / Tools
↓
LLM
↓
Response

Telemetry:

Logs
Metrics
Traces

↓

Monitoring system

---

## 16. Production Tools

Common observability technologies include:

- Prometheus
- Grafana
- OpenTelemetry
- Jaeger
- ELK
- OpenSearch
- Datadog

---

## 17. What to Monitor

### Reliability

- Requests
- Errors
- Error rate
- Timeouts

### Performance

- Latency
- TTFT
- Tokens/sec
- Throughput

### LLM

- Input tokens
- Output tokens
- Model
- Context size

### Infrastructure

- CPU
- RAM
- GPU utilization
- GPU memory

### RAG

- Retrieval latency
- Retrieved chunks
- Retrieval scores
- Context size

---

## 18. Main Takeaway

An LLM application should not be treated as a black box.

Production systems should provide visibility into:

What happened?
How long did it take?
How many tokens were used?
Which model was used?
Did it fail?
Where did the time go?

Observability makes these questions measurable.