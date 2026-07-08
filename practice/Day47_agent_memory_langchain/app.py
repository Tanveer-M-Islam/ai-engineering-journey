from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import (
    get_time,
    get_date,
    multiply,
)

# Load model
model = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# Register tools
tools = [
    get_time,
    get_date,
    multiply,
]

# Create Agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=(
        "You are a helpful AI assistant."
        "Use tools whenever necessary."
    ),
)

# Conversation memory
messages = []

print("=" * 50)
print("Modern LangChain Agent with Memory")
print("Type 'exit' to quit.")
print("=" * 50)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # Save user message
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Invoke agent with full conversation
    response = agent.invoke(
        {
            "messages": messages
        }
    )

    # Get assistant reply
    assistant_message = response["messages"][-1]

    print("\nAI:", assistant_message.content)

    # Save assistant reply
    messages.append(
        {
            "role": "assistant",
            "content": assistant_message.content
        }
    )