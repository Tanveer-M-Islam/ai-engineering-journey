# Day 57 - Agent Loops

## Main Concept

An agent can repeatedly execute:

Agent → Tool → Agent → Tool → Agent

until it determines that no more tools are required.

## Architecture

START
 ↓
Agent
 ↓
Tool call?
 ├── NO → END
 │
 └── YES
       ↓
     ToolNode
       ↓
      Agent
       ↓
Tool call?
 ├── NO → END
 │
 └── YES
       ↓
     ToolNode
       ↓
      Agent

## Important Concept

The graph contains a cycle:

Agent → Tools → Agent

This allows repeated tool execution.

## Single-Step Agent

User
 ↓
Agent
 ↓
Tool
 ↓
Agent
 ↓
Answer

## Multi-Step Agent

User
 ↓
Agent
 ↓
Tool 1
 ↓
Agent
 ↓
Tool 2
 ↓
Agent
 ↓
Tool 3
 ↓
Agent
 ↓
Answer

## Important APIs

StateGraph
MessagesState
ToolNode
tools_condition
bind_tools()

## Main Risk

Agents can potentially continue looping if the stopping
condition is not properly designed.

Production systems therefore need limits and safeguards.