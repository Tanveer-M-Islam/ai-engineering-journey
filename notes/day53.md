# Day 53 - LangGraph Memory & Checkpointing

## Main Concept

LangGraph can preserve graph state between
multiple invocations using checkpointing.

## State

State contains information that flows through
the graph.

Example:

messages

## Memory

Memory allows previous state to be available
during future interactions.

## Checkpoint

A checkpoint stores a snapshot of graph state.

## InMemorySaver

InMemorySaver provides in-memory checkpointing.

It is useful for:

- learning
- prototypes
- local experiments

It is not suitable for persistent production memory.

## Thread ID

A thread ID identifies a conversation.

Example:

thread_id = "conversation_1"

Different thread IDs can represent different
conversations.

## Flow

User
↓
Invoke Graph
↓
Load Checkpoint
↓
Execute Graph
↓
Update State
↓
Save Checkpoint

## Important Distinction

Short-term memory:
Conversation state

Long-term memory:
Persistent user information

RAG:
External knowledge retrieval

Memory and RAG are different concepts.

## Key API

InMemorySaver()

graph.compile(checkpointer=memory)

app.invoke(..., config=config)

configurable:
    thread_id