# Day 55 - LangGraph + RAG

## Main Idea

RAG can be exposed as a tool.

The agent decides whether it needs retrieval.

## Architecture

START
    ↓
Agent
    ↓
tools_condition
    ↓
RAG Tool
    ↓
ToolNode
    ↓
Agent
    ↓
END

## Normal RAG

Question
    ↓
Retriever
    ↓
Documents
    ↓
LLM
    ↓
Answer

## Agentic RAG

Question
    ↓
Agent
    ↓
Should retrieval be used?
    ↓
RAG Tool
    ↓
Documents
    ↓
Agent
    ↓
Answer

## Important APIs

@tool
llm.bind_tools()
ToolNode
tools_condition
FAISS
Retriever

## Key Concept

The retriever is no longer directly forced into
the main workflow.

Instead, retrieval becomes a capability that
the agent can invoke.