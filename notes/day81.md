# Day 81 — FastAPI LLM Serving

## 1. LLM API

An LLM API exposes model functionality through HTTP endpoints.

Architecture:

Client
↓
FastAPI
↓
LLM Service
↓
Model

---

## 2. FastAPI

FastAPI is a Python web framework useful for building APIs.

Important features:

- Request validation
- Response models
- Automatic documentation
- Async support
- HTTP endpoints

---

## 3. Request Schema

Pydantic models define the expected request structure.

Example:

{
    "prompt": "Explain RAG",
    "temperature": 0.2
}

---

## 4. Response Schema

Response models define the structure returned by the API.

Example:

{
    "model": "llama3.2",
    "response": "...",
    "prompt_tokens": 10,
    "generated_tokens": 50
}

---

## 5. Model Loading vs Inference

Model loading means making the model/runtime available.

Inference means generating output from an input.

We should avoid repeatedly loading expensive models for every request.

---

## 6. Health Endpoint

/health

checks whether the service and its important dependency are available.

---

## 7. LLM Endpoint

/ generate

accepts a prompt and sends it to the model.

Architecture:

Client
↓
FastAPI
↓
Ollama
↓
LLM
↓
FastAPI
↓
Client

---

## 8. Validation

Validation prevents invalid requests from reaching the model.

Examples:

- Empty prompts
- Excessively long prompts
- Invalid temperature
- Invalid max_tokens

---

## 9. Swagger

FastAPI automatically provides API documentation at:

/docs

---

## 10. Main Lesson

FastAPI provides the application/API layer around the LLM.

Ollama provides local model execution.

The two can work together:

Client
↓
FastAPI
↓
Ollama
↓
LLM