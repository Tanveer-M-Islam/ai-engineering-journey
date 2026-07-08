# Day 46 Notes

## Modern LangChain Agent

Today I learned how to build an AI agent using LangChain's `create_agent()` API.

### Components

- ChatOllama
- @tool
- create_agent()

### Agent Workflow

User
↓
Model
↓
Tool Selection
↓
Tool Execution
↓
Final Response

### Benefits

- Automatic tool selection
- Automatic reasoning loop
- Less boilerplate code
- Easier to extend with new tools