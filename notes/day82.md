# Day 82 — Streaming LLM Responses

## 1. Streaming

Streaming means sending generated output progressively instead of waiting for the complete response.

Non-streaming:

Request
↓
Generate everything
↓
Response

Streaming:

Request
↓
Token 1
↓
Token 2
↓
Token 3
↓
Token 4
...

---

## 2. Server-Sent Events

SSE allows a server to send events continuously over an HTTP connection.

Example:

data: {"type":"token","content":"Hello"}

data: {"type":"token","content":" world"}

---

## 3. FastAPI StreamingResponse

FastAPI provides StreamingResponse for streaming response data.

Example:

StreamingResponse(
    generator(),
    media_type="text/event-stream"
)

---

## 4. yield

Python generators can use yield to produce data progressively.

Instead of returning one complete response, the generator produces multiple pieces.

---

## 5. Ollama Streaming

Ollama can return generated output incrementally when:

"stream": true

is used.

---

## 6. Streaming Architecture

Client
↓
FastAPI
↓
Ollama
↓
LLM
↓
Token stream
↓
FastAPI
↓
SSE
↓
Client

---

## 7. Streaming vs Speed

Streaming does not necessarily make token generation faster.

It mainly reduces the time before the user sees the first generated output and improves perceived responsiveness.

---

## 8. SSE Use Cases

SSE can be used for:

- LLM token streaming
- Progress updates
- Notifications
- Live status

---

## 9. Main Lesson

A modern LLM API often needs both:

Non-streaming endpoint:
For complete responses.

Streaming endpoint:
For interactive real-time applications.