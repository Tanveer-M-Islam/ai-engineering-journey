# Day 56 - Agentic RAG Assistant

## Project

Build an agent that can decide whether it needs:

1. Knowledge base search
2. Calculator
3. Direct LLM response

## Architecture

User
 ↓
Agent
 ↓
tools_condition
 ├── END
 │
 └── ToolNode
       ↓
      Agent
       ↓
      END

## Tools

### search_knowledge_base

Uses:

- Ollama Embeddings
- FAISS
- Retriever

### calculator

Performs:

- Addition
- Subtraction
- Multiplication
- Division

## Agent

The LLM decides whether a tool is necessary.

## Memory

InMemorySaver stores graph checkpoints.

Each thread_id represents a separate conversation.

## Important APIs

@tool
bind_tools()
ToolNode
tools_condition
MessagesState
StateGraph
InMemorySaver
FAISS

## Core Idea

RAG is treated as a tool rather than being
forced into every question.

This makes the system agentic.