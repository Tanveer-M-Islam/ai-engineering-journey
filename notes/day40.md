LangChain Memory Architecture

Components:

1. ChatPromptTemplate
2. MessagesPlaceholder
3. RunnableWithMessageHistory

MessagesPlaceholder:
Injects conversation history.

RunnableWithMessageHistory:
Automatically stores and retrieves chat history.

Benefits:

- Multi-user support
- Cleaner architecture
- Production ready