from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)


# ============================================================
# 1. LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# 2. KNOWLEDGE BASE TOOL
# ============================================================

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search a small university knowledge base.

    Use this tool when the user asks about courses,
    admission, scholarships, or university information.
    """

    knowledge = {
        "courses": """
        Computer Science courses:

        1. Python Programming
        2. Data Structures
        3. Algorithms
        4. Database Systems
        5. Artificial Intelligence
        6. Machine Learning
        7. Computer Networks
        8. Software Engineering
        9. Natural Language Processing
        """,

        "scholarship": """
        The university offers merit-based scholarships
        to academically strong students.

        Students must maintain the required academic
        performance to continue receiving scholarships.
        """,

        "admission": """
        Undergraduate applicants must submit academic
        certificates, transcripts, identification
        information, and a recent photograph.
        """,
    }

    query_lower = query.lower()

    if "course" in query_lower:
        return knowledge["courses"]

    if "scholarship" in query_lower:
        return knowledge["scholarship"]

    if "admission" in query_lower:
        return knowledge["admission"]

    return "No relevant information found."


# ============================================================
# 3. CALCULATOR TOOL
# ============================================================

@tool
def calculator(
    a: float,
    b: float,
    operation: str,
) -> str:
    """
    Perform basic mathematical calculations.

    Supported operations:
    add
    subtract
    multiply
    divide
    """

    if operation == "add":

        result = a + b

    elif operation == "subtract":

        result = a - b

    elif operation == "multiply":

        result = a * b

    elif operation == "divide":

        if b == 0:
            return "Cannot divide by zero."

        result = a / b

    else:

        return (
            "Invalid operation. "
            "Use add, subtract, multiply, or divide."
        )

    return str(result)


# ============================================================
# 4. TOOLS
# ============================================================

tools = [
    search_knowledge_base,
    calculator,
]


# ============================================================
# 5. BIND TOOLS
# ============================================================

llm_with_tools = llm.bind_tools(
    tools
)


# ============================================================
# 6. AGENT NODE
# ============================================================

def agent(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ============================================================
# 7. TOOL NODE
# ============================================================

tool_node = ToolNode(
    tools
)


# ============================================================
# 8. BUILD GRAPH
# ============================================================

builder = StateGraph(
    MessagesState
)


builder.add_node(
    "agent",
    agent,
)

builder.add_node(
    "tools",
    tool_node,
)


# ============================================================
# 9. START
# ============================================================

builder.add_edge(
    START,
    "agent",
)


# ============================================================
# 10. AGENT → TOOL OR END
# ============================================================

builder.add_conditional_edges(
    "agent",
    tools_condition,
)


# ============================================================
# 11. TOOL → AGENT
# ============================================================

builder.add_edge(
    "tools",
    "agent",
)


# ============================================================
# 12. COMPILE
# ============================================================

app = builder.compile()


# ============================================================
# 13. APPLICATION
# ============================================================

print("=" * 70)
print("🤖 Day 57 - Agent Loops")
print("=" * 70)

print("\nAvailable tools:")
print("- search_knowledge_base")
print("- calculator")

print("\nTry:")
print(
    "What courses are offered and how many courses are there?"
)

print(
    "What are the admission requirements?"
)

print(
    "What is 25 multiplied by 8?"
)

print("\nType 'exit' to quit.")


# ============================================================
# 14. CHAT LOOP
# ============================================================

while True:

    question = input("\nYou: ")

    if question.lower().strip() == "exit":

        print("\nGoodbye!")

        break


    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        }
    )


    final_message = result["messages"][-1]


    print("\nAI:")

    print(
        final_message.content
    )