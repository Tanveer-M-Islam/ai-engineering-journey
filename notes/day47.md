# Day 47 Notes

## Conversation Memory

The LLM itself does not remember previous interactions.

Memory is achieved by sending the conversation history with every request.

Workflow:

User Message
↓

Append to History
↓

Agent
↓

Assistant Response
↓

Append to History

Benefits

- Multi-turn conversations
- Follow-up questions
- More natural interaction
- Foundation for long-term memory systems