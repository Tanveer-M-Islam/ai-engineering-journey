from typing import TypedDict

from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END


# ---------------------------------------
# LLM
# ---------------------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ---------------------------------------
# Graph State
# ---------------------------------------

class State(TypedDict):
    question: str
    answer: str


# ---------------------------------------
# Node
# ---------------------------------------

def chatbot(state: State):

    response = llm.invoke(state["question"])

    return {
        "answer": response.content
    }


# ---------------------------------------
# Graph
# ---------------------------------------

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")

graph.add_edge("chatbot", END)

app = graph.compile()


# ---------------------------------------
# Chat Loop
# ---------------------------------------

print("=" * 60)
print("🤖 LangGraph Chatbot")
print("=" * 60)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    result = app.invoke(
        {
            "question": question
        }
    )

    print("\nAI:\n")

    print(result["answer"])