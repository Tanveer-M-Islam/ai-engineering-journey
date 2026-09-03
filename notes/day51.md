# Day 51 - Multiple Nodes & State Updates

## Main Concept

LangGraph allows multiple nodes to work together
through a shared State.

## Today's Graph

START
↓
Question Node
↓
Answer Node
↓
END

## State

The State stores information shared between nodes.

Example:

question
answer

## Node

A node is a Python function that performs a task.

## State Update

A node can return new values that are added to
the graph state.

## Important Idea

Nodes do not directly call each other.

LangGraph controls the execution flow through edges.

## Example

Question Node
↓
reads question
↓
updates state
↓
Answer Node
↓
reads question
↓
generates answer
↓
updates answeradd