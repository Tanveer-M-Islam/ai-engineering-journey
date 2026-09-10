from typing import Literal
from typing_extensions import TypedDict

from pydantic import BaseModel

from langchain_ollama import ChatOllama

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.types import (
    Command,
    interrupt,
)


# ============================================================
# 1. LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# 2. Structured Decision
# ============================================================

class AgentDecision(BaseModel):

    action: Literal[
        "search",
        "calculate",
        "send_email",
        "respond",
    ]

    query: str = ""


structured_llm = llm.with_structured_output(
    AgentDecision
)


# ============================================================
# 3. State
# ============================================================

class AgentState(TypedDict):

    question: str

    decision: dict

    result: str

    approved: bool


# ============================================================
# 4. Decision Node
# ============================================================

def decision_node(state: AgentState):

    question = state["question"]

    question_lower = question.lower()

    # --------------------------------------------------------
    # Deterministic routing for known operations
    # --------------------------------------------------------

    if any(
        word in question_lower
        for word in [
            "admission",
            "scholarship",
            "course",
            "university",
        ]
    ):

        decision = AgentDecision(
            action="search",
            query=question,
        )

    elif any(
        symbol in question_lower
        for symbol in [
            "+",
            "-",
            "*",
            "/",
        ]
    ):

        decision = AgentDecision(
            action="calculate",
            query=question,
        )

    elif "send email" in question_lower:

        decision = AgentDecision(
            action="send_email",
            query=question,
        )

    else:

        # ----------------------------------------------------
        # LLM handles ambiguous/general requests
        # ----------------------------------------------------

        prompt = f"""
You are an AI assistant router.

Choose exactly one action:

search
calculate
send_email
respond

Question:

{question}
"""

        decision = structured_llm.invoke(prompt)

    print("\n--- DECISION ---")
    print("Action:", decision.action)
    print("Query:", decision.query)

    return {
        "decision": decision.model_dump()
    }


# ============================================================
# 5. Safety Router
# ============================================================

def safety_router(state: AgentState):

    action = state["decision"]["action"]

    # Sensitive operation
    if action == "send_email":

        return "approval"

    return "execute"


# ============================================================
# 6. Human Approval
# ============================================================

def approval_node(state: AgentState):

    decision = state["decision"]

    approval_request = {
        "message": "Human approval required.",
        "action": decision["action"],
        "query": decision["query"],
    }

    approved = interrupt(
        approval_request
    )

    return {
        "approved": bool(approved)
    }


# ============================================================
# 7. Approval Router
# ============================================================

def approval_router(state: AgentState):

    if state["approved"]:

        return "execute"

    return "cancel"


# ============================================================
# 8. Execute Node
# ============================================================

def execute_node(state: AgentState):

    decision = state["decision"]

    action = decision["action"]
    query = decision["query"]

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    if action == "search":

        result = (
            f"RAG/search operation executed for: {query}"
        )

    # --------------------------------------------------------
    # Calculate
    # --------------------------------------------------------

    elif action == "calculate":

        result = (
            f"Calculator operation requested for: {query}"
        )

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    elif action == "send_email":

        # Demo only.
        # No real email is sent.

        result = (
            f"Email operation approved for: {query}"
        )

    # --------------------------------------------------------
    # Normal response
    # --------------------------------------------------------

    else:

        response = llm.invoke(
            f"""
Answer the following question clearly:

{query}
"""
        )

        result = response.content

    return {
        "result": result
    }


# ============================================================
# 9. Cancel Node
# ============================================================

def cancel_node(state: AgentState):

    return {
        "result": (
            "The requested action was rejected. "
            "No sensitive operation was performed."
        )
    }


# ============================================================
# 10. Build Graph
# ============================================================

builder = StateGraph(
    AgentState
)


builder.add_node(
    "decision",
    decision_node
)

builder.add_node(
    "approval",
    approval_node
)

builder.add_node(
    "execute",
    execute_node
)

builder.add_node(
    "cancel",
    cancel_node
)


# ============================================================
# 11. Graph Connections
# ============================================================

builder.add_edge(
    START,
    "decision"
)


builder.add_conditional_edges(
    "decision",
    safety_router,
    {
        "approval": "approval",
        "execute": "execute",
    }
)


builder.add_conditional_edges(
    "approval",
    approval_router,
    {
        "execute": "execute",
        "cancel": "cancel",
    }
)


builder.add_edge(
    "execute",
    END
)

builder.add_edge(
    "cancel",
    END
)


# ============================================================
# 12. Checkpointing
# ============================================================

memory = InMemorySaver()

app = builder.compile(
    checkpointer=memory
)


# ============================================================
# 13. Configuration
# ============================================================

config = {
    "configurable": {
        "thread_id": "day60_demo"
    }
}


# ============================================================
# 14. Application
# ============================================================

print("=" * 60)
print("DAY 60 - PRODUCTION STYLE AGENT ARCHITECTURE")
print("=" * 60)

print("\nTry:")
print("1. What are the admission requirements?")
print("2. What is 10 + 20?")
print("3. Send email to the administrator")
print("4. What is artificial intelligence?")

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
            "approved": False,
        },
        config=config,
    )

    # --------------------------------------------------------
    # Detect paused graph
    # --------------------------------------------------------

    state = app.get_state(config)

    if state.next:

        decision = state.values["decision"]

        print("\n⚠️ HUMAN APPROVAL REQUIRED")

        print(
            "Action:",
            decision["action"]
        )

        print(
            "Request:",
            decision["query"]
        )

        while True:

            answer = input(
                "\nApprove? (yes/no): "
            ).strip().lower()

            if answer in ["yes", "y"]:

                result = app.invoke(
                    Command(resume=True),
                    config=config,
                )

                break

            elif answer in ["no", "n"]:

                result = app.invoke(
                    Command(resume=False),
                    config=config,
                )

                break

            else:

                print(
                    "Please enter yes or no."
                )

    print("\nAssistant:")

    print(
        result["result"]
    )