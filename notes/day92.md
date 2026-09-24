# Day 92 — Responsible AI & Guardrails

## 1. Responsible AI

Responsible AI means building AI systems that are:

- safe
- fair
- transparent
- privacy-aware
- reliable
- accountable

---

## 2. Guardrails

Guardrails are controls placed around an AI application to reduce:

- unsafe behavior
- invalid output
- sensitive data leakage
- unauthorized actions
- policy violations

---

## 3. Input Guardrails

Input guardrails run before the LLM.

Examples:

- empty input checks
- prompt length limits
- prompt injection detection
- PII detection
- format validation

---

## 4. Output Guardrails

Output guardrails run after the LLM.

Examples:

- output schema validation
- PII leakage detection
- unsafe content detection
- unsupported value detection
- tool-call validation

---

## 5. Rule-Based Guardrails

Rule-based guardrails use:

- regex
- keywords
- allow lists
- block lists
- schemas
- type checks

Advantages:

- fast
- simple
- predictable

Limitations:

- easy to bypass
- limited semantic understanding

---

## 6. Model-Based Guardrails

A classifier model can classify input or output as:

- safe
- unsafe
- review

Advantages:

- better semantic understanding

Limitations:

- additional latency
- additional cost
- possible model errors

---

## 7. Hybrid Guardrails

Production systems often combine:

Rule-based checks
+
Model-based checks
+
Authorization
+
Output validation

---

## 8. PII

PII means Personally Identifiable Information.

Examples:

- email
- phone number
- national ID
- passport number
- credit card number
- home address

Sensitive data can be masked before sending it to the model.

Example:

tanveer@example.com

becomes:

[EMAIL_REDACTED]

---

## 9. Policy Guardrails

Policy guardrails define what an application is allowed to do.

Example:

Allowed:

- answer FAQ
- search documents
- create support tickets

Not allowed:

- delete users
- change admin permissions
- access unrestricted databases

---

## 10. Structured Output

Structured output makes validation easier.

Example:

{
  "category": "billing",
  "priority": "medium"
}

The application can validate the category and priority before using them.

---

## 11. Allow List

An allow list defines approved actions.

Example:

- search_documents
- create_ticket
- get_account_status

Anything outside the allow list is rejected.

---

## 12. Guardrail Pipeline

User
↓
Input Validation
↓
Prompt Injection Check
↓
PII Masking
↓
LLM
↓
Output Validation
↓
Final Response

---

## 13. RAG Guardrails

Retrieved documents should be treated as untrusted data.

Use:

User
↓
Input Guardrail
↓
Retriever
↓
Document Validation
↓
LLM
↓
Output Guardrail

---

## 14. Agent Guardrails

Tool-enabled agents should use:

LLM
↓
Tool Proposal
↓
Schema Validation
↓
Authorization
↓
Policy Check
↓
Human Approval if required
↓
Tool Execution

---

## 15. Human Review

Some requests should be classified as:

SAFE

REVIEW

BLOCKED

Uncertain high-risk requests can be escalated to a human.

---

## Key Takeaway

Guardrails should exist outside the LLM.

A production AI system should combine:

LLM
+
Input validation
+
Output validation
+
PII protection
+
Policy enforcement
+
Authorization
+
Monitoring
+
Human review