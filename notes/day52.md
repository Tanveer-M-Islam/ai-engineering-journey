# Day 52 - Conditional Routing in LangGraph

## Main Concept

Conditional routing allows a LangGraph workflow
to choose different execution paths.

## Graph

START
↓
Router
↓
├── Chat
│
└── RAG
↓
END

## Router

The router decides which branch should execute.

## Conditional Edges

LangGraph uses:

add_conditional_edges()

to connect a node to different destinations.

## Example

graph.add_conditional_edges(
    "router",
    decide_route,
    {
        "chat": "chat",
        "rag": "rag",
    }
)

## Important Idea

The routing function returns a value.

That value determines the next node.

Example:

"chat" → Chat Node

"rag" → RAG Node

## Engineering Lesson

For predictable routing, deterministic Python
logic can be more reliable than asking a small
LLM to classify every request.

## Today's Architecture

START
↓
Router
↓
Chat / RAG
↓
END