# Day 95 — AI System Architecture

## 1. AI System Architecture

AI system architecture describes how the components of an AI
application interact.

A production AI system contains more than an LLM.

Typical components:

- client
- API
- authentication
- authorization
- guardrails
- orchestrator
- RAG
- agents
- tools
- model gateway
- databases
- cache
- queues
- workers
- observability
- evaluation

---

## 2. Architecture Layers

Common layers:

1. Presentation
2. API
3. Security
4. AI orchestration
5. Model
6. Data
7. Infrastructure
8. Observability

---

## 3. API Layer

The API connects clients with backend services.

Responsibilities can include:

- validation
- authentication
- rate limiting
- request IDs
- error handling
- routing

---

## 4. Authentication vs Authorization

Authentication:

Who are you?

Authorization:

What are you allowed to do?

---

## 5. AI Orchestrator

The orchestrator coordinates AI workflows.

It may decide whether to use:

- LLM
- RAG
- tool
- agent
- cache
- human review

---

## 6. Model Gateway

A model gateway provides a common interface to models.

It can handle:

- model routing
- retries
- fallbacks
- timeouts
- logging
- cost tracking

---

## 7. RAG Architecture

Indexing:

Documents
↓
Cleaning
↓
Chunking
↓
Embeddings
↓
Vector Database

Querying:

Question
↓
Query Embedding
↓
Retrieval
↓
Reranking
↓
Context
↓
LLM
↓
Answer

---

## 8. SQL vs Vector Database

SQL database:

Stores structured application data.

Examples:

- users
- accounts
- messages
- permissions

Vector database:

Stores embeddings for semantic retrieval.

Many AI applications use both.

---

## 9. Agent Architecture

User
↓
Agent
↓
Tool Selection
↓
Permission Check
↓
Tool
↓
Observation
↓
Answer

LLMs should not have unrestricted access to sensitive tools.

---

## 10. Guardrails

Input guardrails run before AI processing.

Output guardrails run before responses/actions leave the AI layer.

Guardrails can check:

- prompt injection
- PII
- policy
- schema
- unsafe actions

---

## 11. Caching

Caching avoids repeated computation.

Examples:

- response cache
- semantic cache
- embedding cache
- retrieval cache
- prefix cache

---

## 12. Background Processing

Slow operations can use queues and workers.

Examples:

- document indexing
- transcription
- embedding generation
- batch inference
- report generation

---

## 13. Stateless Services

Application state should not unnecessarily depend on one server's
memory.

External stores allow multiple application instances to access
shared state.

This makes horizontal scaling easier.

---

## 14. Horizontal Scaling

Horizontal scaling adds more server instances.

Users
↓
Load Balancer
↓
Multiple Servers

---

## 15. Failure Handling

Production systems should prepare for failures.

Common mechanisms:

- timeouts
- retries
- fallbacks
- circuit breakers
- graceful errors
- logging

---

## 16. Observability

Three pillars:

- logs
- metrics
- traces

AI-specific information may include:

- model
- latency
- tokens
- retrieval time
- guardrail result
- tool calls
- errors

---

## 17. Evaluation

Observability asks:

What happened?

Evaluation asks:

Was the result good?

Production failures can be added to evaluation datasets.

---

## 18. Monolith vs Microservices

Monolith:

Simpler deployment and development.

Microservices:

Independent components and scaling but greater operational
complexity.

Start with the simplest architecture that meets the requirements.

---

## 19. Complete Architecture

User
↓
Client
↓
API
↓
Authentication
↓
Input Guardrail
↓
AI Orchestrator
↓
RAG / Agent / Tools / Model Router
↓
Model Gateway
↓
LLM
↓
Output Guardrail
↓
Cache
↓
Response

Supporting systems:

- SQL database
- vector database
- cache
- object storage
- queues
- workers
- secret management

Surrounding systems:

- security
- logs
- metrics
- traces
- evaluation
- cost monitoring

---

## Key Takeaway

AI engineering is not only about calling an LLM.

A production AI system combines:

Software Engineering
+
LLMs
+
RAG
+
Agents
+
Data Infrastructure
+
Security
+
Guardrails
+
Observability
+
Evaluation
+
Deployment
+
Scaling