# Day 58 — Structured Agent Decisions

## 1. What is a Structured Agent Decision?

A structured agent decision is an LLM decision that follows a predefined schema instead of returning unrestricted natural language.

Example:

{
    "action": "search",
    "query": "admission requirements",
    "confidence": 0.95
}

This makes the LLM output easier for Python and LangGraph to process.

---

## 2. Why Structured Output?

Normal LLM output:

The user is asking about admission, so I think we should search the knowledge base.

Problem:

- Difficult to parse reliably
- Different wording can be generated
- Harder to route programmatically

Structured output:

{
    "action": "search",
    "query": "admission requirements",
    "confidence": 0.95
}

Advantages:

- Machine-readable
- Predictable format
- Easier validation
- Easier routing
- Easier debugging

---

## 3. Pydantic Decision Schema

We use Pydantic to define the expected decision structure.

Example:

class AgentDecision(BaseModel):

    action: Literal[
        "search",
        "calculate",
        "respond"
    ]

    query: str = ""

    confidence: float = Field(
        ge=0,
        le=1
    )

### Fields

action:
    Determines which operation should be executed.

query:
    Contains the relevant query or input.

confidence:
    Represents the confidence value from 0 to 1.

---

## 4. with_structured_output()

LangChain provides:

structured_llm = llm.with_structured_output(
    AgentDecision
)

This tells the LLM integration that the response should follow
the AgentDecision schema.

Example:

decision = structured_llm.invoke(prompt)

The result can contain:

decision.action
decision.query
decision.confidence

---

## 5. Structured Decision Architecture

The Day 58 architecture is:

START
  |
  v
Decision Node
  |
  v
Structured Decision
  |
  v
Python Router
  |
  +---- search ------> Search Node
  |
  +---- calculate ---> Calculate Node
  |
  +---- respond -----> Respond Node
                           |
                           v
                          END

---

## 6. LangGraph Conditional Routing

The graph uses:

builder.add_conditional_edges(
    "decision",
    route_decision,
    {
        "search": "search",
        "calculate": "calculate",
        "respond": "respond",
    }
)

The router reads the decision from the graph state.

Example:

action = state["decision"]["action"]

If action is "search":

    route to search node

If action is "calculate":

    route to calculate node

If action is "respond":

    route to respond node

---

## 7. Important Difference

Structured output guarantees the FORMAT of the result.

It does NOT guarantee that the LLM chooses the correct action.

For example, the LLM may incorrectly return:

{
    "action": "respond",
    "query": "admission requirements",
    "confidence": 1.0
}

even though the correct action should be:

{
    "action": "search",
    "query": "admission requirements",
    "confidence": 1.0
}

Therefore:

Structured Output != Correct Decision

---

## 8. Why This Happened With llama3.2

The local llama3.2 model may decide that it already knows the answer
to a question such as:

"What are the admission requirements?"

Therefore, it can select:

action = "respond"

instead of:

action = "search"

The structured output mechanism can still correctly format that
incorrect decision.

---

## 9. Better Production Pattern

A stronger architecture combines deterministic rules with LLM
decision-making.

Example:

User Question
     |
     v
Deterministic Rules
     |
     +---- Known KB topic ----> Search
     |
     +---- Mathematical -----> Calculate
     |
     +---- Unknown ----------> LLM Structured Decision
                                      |
                                      v
                                  Python Router

This prevents the LLM from making decisions that Python can make
more reliably.

---

## 10. Deterministic Routing Example

Example:

search_keywords = [
    "admission",
    "admissions",
    "scholarship",
    "scholarships",
    "course",
    "courses",
    "university",
    "program",
    "programs",
]

If the question contains one of these terms, route directly to
the knowledge base.

Example:

"What are the admission requirements?"

contains:

"admission"

Therefore:

action = "search"

---

## 11. LLM vs Python Responsibilities

LLM:

- Understand natural language
- Interpret ambiguous questions
- Generate structured decisions
- Handle flexible language

Python:

- Validate decisions
- Apply deterministic rules
- Control workflow
- Execute business logic
- Control tool/API access

Good AI engineering systems often combine both.

---

## 12. Day 57 vs Day 58

### Day 57 — Agent Loops

Architecture:

Agent
  |
  v
Tool?
  |
  +---- YES ---> ToolNode
  |                |
  |                v
  |              Agent
  |
  +---- NO ----> END

The agent can repeatedly call tools.

### Day 58 — Structured Decisions

Architecture:

Decision
  |
  v
Structured Output
  |
  v
Python Router
  |
  +---- Search
  |
  +---- Calculate
  |
  +---- Respond

The main focus is controlled decision-making.

---

## 13. Key Concepts

### Structured Output

LLM response follows a predefined schema.

### Pydantic

Used to define and validate structured data.

### Literal

Restricts a field to predefined values.

Example:

Literal["search", "calculate", "respond"]

### Field

Allows validation rules.

Example:

Field(ge=0, le=1)

means the value must be between 0 and 1.

### Conditional Edge

LangGraph uses conditional edges to select the next node based
on the current state.

---

## 14. Important Engineering Principle

Do not give the LLM control over everything.

Prefer:

LLM
 |
 v
Structured Decision
 |
 v
Validation
 |
 v
Deterministic Application Logic
 |
 v
Tool / API / Database

instead of:

LLM
 |
 v
Unrestricted Action

This improves:

- Reliability
- Debugging
- Testing
- Safety
- Maintainability

---

## 15. Day 58 Summary

Today we learned:

1. Structured agent decisions
2. Pydantic schemas
3. with_structured_output()
4. LangGraph conditional routing
5. Deterministic routing
6. LLM decision limitations
7. LLM + Python hybrid architecture

Most important takeaway:

"Structured output makes an LLM response predictable in format,
but it does not guarantee that the decision itself is correct."

---

## 16. Interview Questions

### Q1. What is structured output?

Structured output forces an LLM response to follow a predefined
schema so that applications can reliably process it.

### Q2. Why use Pydantic with LLMs?

Pydantic defines and validates the structure and types of the
LLM's output.

### Q3. Why combine LLM decisions with deterministic routing?

LLMs are flexible but can make inconsistent decisions. Deterministic
Python logic provides reliable control over important workflows.