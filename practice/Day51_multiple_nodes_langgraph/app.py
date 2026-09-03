from typing import TypedDict

from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph
from langgraph.graph import START, END


# ============================================================
# 1. Load LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# 2. Define Graph State
# ============================================================

class State(TypedDict):
    question: str
    answer: str


# ============================================================
# 3. First Node
# ============================================================

def question_node(state: State):
    """
    Reads the user's question and stores it in the state.
    """

    question = state["question"]

    print("\n[Question Node]")
    print("Received:", question)

    return {
        "question": question
    }


# ============================================================
# 4. Second Node
# ============================================================

def answer_node(state: State):
    """
    Reads the question from the state
    and generates an answer using the LLM.
    """

    question = state["question"]

    print("\n[Answer Node]")
    print("Generating answer...")

    response = llm.invoke(question)

    return {
        "answer": response.content
    }


# ============================================================
# 5. Create Graph
# ============================================================

graph = StateGraph(State)


# ============================================================
# 6. Add Nodes
# ============================================================

graph.add_node(
    "question_node",
    question_node
)

graph.add_node(
    "answer_node",
    answer_node
)


# ============================================================
# 7. Connect Nodes
# ============================================================

graph.add_edge(
    START,
    "question_node"
)

graph.add_edge(
    "question_node",
    "answer_node"
)

graph.add_edge(
    "answer_node",
    END
)


# ============================================================
# 8. Compile Graph
# ============================================================

app = graph.compile()


# ============================================================
# 9. Application
# ============================================================

print("=" * 60)
print("🤖 Day 51 - Multiple Node LangGraph")
print("=" * 60)
print("Type 'exit' to quit.")


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # --------------------------------------------------------
    # Initial State
    # --------------------------------------------------------

    initial_state = {
        "question": question,
        "answer": ""
    }

    # --------------------------------------------------------
    # Run Graph
    # --------------------------------------------------------

    result = app.invoke(initial_state)

    # --------------------------------------------------------
    # Final Answer
    # --------------------------------------------------------

    print("\nAI:")
    print(result["answer"])