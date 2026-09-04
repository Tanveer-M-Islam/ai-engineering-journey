from typing import TypedDict

from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================
# LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# STATE
# ============================================================

class State(TypedDict):
    messages: list[dict]


# ============================================================
# CHATBOT NODE
# ============================================================

def chatbot(state: State):
    """
    Read the conversation history from state,
    send it to the LLM, and add the AI response.
    """

    print("\n[Chatbot Node]")

    messages = state["messages"]

    # Convert our dictionaries into a simple
    # conversation prompt.
    conversation = ""

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            conversation += f"User: {content}\n"

        elif role == "assistant":
            conversation += f"Assistant: {content}\n"

    conversation += "Assistant:"

    response = llm.invoke(conversation)

    return {
        "messages": messages + [
            {
                "role": "assistant",
                "content": response.content,
            }
        ]
    }


# ============================================================
# BUILD GRAPH
# ============================================================

graph = StateGraph(State)

graph.add_node(
    "chatbot",
    chatbot,
)

graph.add_edge(
    START,
    "chatbot",
)

graph.add_edge(
    "chatbot",
    END,
)


# ============================================================
# CHECKPOINT MEMORY
# ============================================================

memory = InMemorySaver()


# ============================================================
# COMPILE GRAPH WITH CHECKPOINTER
# ============================================================

app = graph.compile(
    checkpointer=memory
)


# ============================================================
# THREAD CONFIGURATION
# ============================================================

config = {
    "configurable": {
        "thread_id": "conversation_1"
    }
}


# ============================================================
# APPLICATION
# ============================================================

print("=" * 60)
print("🤖 Day 53 - LangGraph Memory")
print("=" * 60)

print("Memory-enabled chatbot")
print("Type 'exit' to quit.")
print("Type 'new' to start a new conversation.")


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # Create a new conversation
    if question.lower() == "new":

        config = {
            "configurable": {
                "thread_id": "conversation_2"
            }
        }

        print("\nStarted a new conversation.")

        continue

    # Get previous conversation state
    current_state = app.get_state(config)

    previous_messages = current_state.values.get(
        "messages",
        []
    )

    # Add new user message
    new_messages = previous_messages + [
        {
            "role": "user",
            "content": question,
        }
    ]

    # Invoke graph
    result = app.invoke(
        {
            "messages": new_messages
        },
        config=config,
    )

    # Get latest assistant response
    assistant_message = result["messages"][-1]["content"]

    print("\nAI:")
    print(assistant_message)