from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import (
    get_time,
    get_date,
    multiply,
)

# Load the model
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

# Create the agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=(
        "You are a helpful AI assistant. "
        "Use tools whenever they help answer the user's question accurately."
    ),
)

print("=" * 50)
print("Modern LangChain Agent")
print("Type 'exit' to quit.")
print("=" * 50)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    assistant_messages = [
        msg for msg in response["messages"]
        if getattr(msg, "type", "") == "ai"
    ]

    if assistant_messages:
        print("\nAI:", assistant_messages[-1].content)