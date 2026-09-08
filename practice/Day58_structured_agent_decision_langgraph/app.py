from typing import Literal
from typing_extensions import TypedDict

from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama

from langgraph.graph import (
    StateGraph,
    START,
    END,
)


# ============================================================
# 1. LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# 2. Structured Decision Schema
# ============================================================

class AgentDecision(BaseModel):

    action: Literal[
        "search",
        "calculate",
        "respond"
    ]

    query: str = ""

    confidence: float = Field(
        ge=0,
        le=1
    )


# ============================================================
# 3. State
# ============================================================

class AgentState(TypedDict):

    question: str

    decision: dict

    result: str


# ============================================================
# 4. Structured LLM
# ============================================================

structured_llm = llm.with_structured_output(
    AgentDecision
)


# ============================================================
# 5. Decision Node
# ============================================================

def decision_node(state: AgentState):

    question = state["question"]

    prompt = f"""
You are a routing system for an AI assistant.

Your job is to decide which action should handle the user's question.

IMPORTANT RULE:
If the question asks about admission, scholarship, courses,
university information, or any other information that may exist
in the knowledge base, ALWAYS choose "search".

Available actions:

1. search
Use this for:
- admission requirements
- scholarships
- courses
- university information
- knowledge-base questions

2. calculate
Use this only for mathematical calculations.

3. respond
Use this only for general conversation or questions that clearly
do not require the knowledge base.

User question:
{question}
"""

    decision = structured_llm.invoke(prompt)

    print("\n--- STRUCTURED DECISION ---")
    print("Action:", decision.action)
    print("Query:", decision.query)
    print("Confidence:", decision.confidence)

    return {
        "decision": decision.model_dump()
    }


# ============================================================
# 6. Router
# ============================================================

def route_decision(state: AgentState):

    action = state["decision"]["action"]

    if action == "search":
        return "search"

    elif action == "calculate":
        return "calculate"

    else:
        return "respond"


# ============================================================
# 7. Search Node
# ============================================================

def search_node(state: AgentState):

    query = state["decision"]["query"]

    # Simple demo knowledge base
    knowledge_base = {
        "admission": (
            "Admission generally requires academic certificates, "
            "application documents, and meeting the program requirements."
        ),
        "scholarship": (
            "Scholarships may depend on academic performance, "
            "eligibility requirements, and application deadlines."
        ),
        "courses": (
            "Courses depend on the selected program and academic semester."
        ),
    }

    answer = (
        "I could not find the requested information "
        "in the knowledge base."
    )

    query_lower = query.lower()

    for keyword, information in knowledge_base.items():

        if keyword in query_lower:

            answer = information
            break

    return {
        "result": answer
    }


# ============================================================
# 8. Calculate Node
# ============================================================

def calculate_node(state: AgentState):

    question = state["question"]

    # Simple demonstration calculator
    if "2 + 2" in question:

        result = "The answer is 4."

    elif "10 * 5" in question:

        result = "The answer is 50."

    elif "100 / 4" in question:

        result = "The answer is 25."

    else:

        result = (
            "This demo calculator only supports "
            "2 + 2, 10 * 5, and 100 / 4."
        )

    return {
        "result": result
    }


# ============================================================
# 9. Respond Node
# ============================================================

def respond_node(state: AgentState):

    question = state["question"]

    response = llm.invoke(
        f"""
Answer the following question clearly and concisely.

Question:
{question}
"""
    )

    return {
        "result": response.content
    }


# ============================================================
# 10. Build Graph
# ============================================================

builder = StateGraph(AgentState)


builder.add_node(
    "decision",
    decision_node
)

builder.add_node(
    "search",
    search_node
)

builder.add_node(
    "calculate",
    calculate_node
)

builder.add_node(
    "respond",
    respond_node
)


# ============================================================
# 11. Graph Edges
# ============================================================

builder.add_edge(
    START,
    "decision"
)


builder.add_conditional_edges(
    "decision",
    route_decision,
    {
        "search": "search",
        "calculate": "calculate",
        "respond": "respond",
    }
)


builder.add_edge(
    "search",
    END
)

builder.add_edge(
    "calculate",
    END
)

builder.add_edge(
    "respond",
    END
)


# ============================================================
# 12. Compile
# ============================================================

app = builder.compile()


# ============================================================
# 13. Interactive Application
# ============================================================

print("=" * 60)
print("STRUCTURED AGENT DECISION SYSTEM")
print("=" * 60)

print("\nType 'exit' to quit.")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    result = app.invoke(
        {
            "question": question,
            "decision": {},
            "result": "",
        }
    )

    print("\nAssistant:")
    print(result["result"])