# Day 54 - LangGraph Tool Nodes & Agent Tool Execution

## Main Concepts

### Tool
A Python function that an LLM can call.

### bind_tools()
Connects tools to the LLM so the model can generate tool calls.

### ToolNode
LangGraph node responsible for executing tool calls.

### tools_condition
Routes the graph to the ToolNode when the latest AI message contains
tool calls.

## Architecture

START
    ↓
Agent
    ↓
Tool call?
   / \
 YES  NO
  ↓    ↓
Tools END
  ↓
Agent
  ↓
 END

## Important Messages

HumanMessage
    ↓
AIMessage
    ↓
ToolMessage
    ↓
AIMessage

## Important Difference

The LLM does not directly execute Python tools.

The LLM generates a tool call.

LangGraph's ToolNode executes the actual tool.

## Key APIs

llm.bind_tools(tools)

ToolNode(tools)

tools_condition

StateGraph(MessagesState)