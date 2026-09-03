from typing import TypedDict

from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph
from langgraph.graph import START, END


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
    question: str
    route: str
    answer: str


# ============================================================
# ROUTER LOGIC
# ============================================================

def decide_route(state: State) -> str:
    """
    Decide which branch should execute.
    """

    question = state["question"].lower()

    rag_keywords = [
        "course",
        "courses",
        "admission",
        "scholarship",
        "ielts",
        "university",
        "program",
        "programs",
        "tuition",
    ]

    for keyword in rag_keywords:
        if keyword in question:
            return "rag"

    return "chat"


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: State):
    """
    Router node records the selected route
    in the shared state.
    """

    route = decide_route(state)

    print("\n[Router Node]")
    print(f"Selected route: {route.upper()}")

    return {
        "route": route
    }


# ============================================================
# CHAT NODE
# ============================================================

def chat_node(state: State):

    print("\n[Chat Node]")
    print("Generating general response...")

    question = state["question"]

    response = llm.invoke(question)

    return {
        "answer": response.content
    }


# ============================================================
# RAG NODE
# ============================================================

def rag_node(state: State):

    print("\n[RAG Node]")
    print("University-related question detected.")

    question = state["question"]

    prompt = f"""
You are a university information assistant.

Answer the user's question clearly.

If you do not know the answer, say:
"I don't have enough information to answer that."

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# ============================================================
# BUILD GRAPH
# ============================================================

graph = StateGraph(State)


# Add nodes

graph.add_node("router", router_node)
graph.add_node("chat", chat_node)
graph.add_node("rag", rag_node)


# ============================================================
# START → ROUTER
# ============================================================

graph.add_edge(
    START,
    "router"
)


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

graph.add_conditional_edges(
    "router",
    decide_route,
    {
        "chat": "chat",
        "rag": "rag",
    }
)


# ============================================================
# BRANCHES → END
# ============================================================

graph.add_edge(
    "chat",
    END
)

graph.add_edge(
    "rag",
    END
)


# ============================================================
# COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# RUN APPLICATION
# ============================================================

print("=" * 60)
print("🤖 Day 52 - LangGraph Conditional Routing")
print("=" * 60)
print("Type 'exit' to quit.")


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    initial_state = {
        "question": question,
        "route": "",
        "answer": "",
    }

    result = app.invoke(initial_state)

    print("\nAI:")
    print(result["answer"])