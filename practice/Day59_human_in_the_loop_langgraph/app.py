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
        "send_email",
        "delete_file",
        "respond"
    ]

    target: str = ""

    description: str = ""


structured_llm = llm.with_structured_output(
    AgentDecision
)


# ============================================================
# 3. Graph State
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

    prompt = f"""
You are an AI assistant that determines what action
should be performed.

Choose exactly one action:

search
    Use when information needs to be retrieved.

send_email
    Use when the user asks to send an email.

delete_file
    Use when the user asks to delete a file.

respond
    Use for normal conversation.

User request:

{question}
"""

    decision = structured_llm.invoke(prompt)

    print("\n--- AGENT DECISION ---")
    print("Action:", decision.action)
    print("Target:", decision.target)
    print("Description:", decision.description)

    return {
        "decision": decision.model_dump()
    }


# ============================================================
# 5. Safety Router
# ============================================================

def safety_router(state: AgentState):

    action = state["decision"]["action"]

    # Sensitive actions require human approval
    if action in [
        "send_email",
        "delete_file",
    ]:
        return "approval"

    return "execute"


# ============================================================
# 6. Human Approval Node
# ============================================================

def approval_node(state: AgentState):

    decision = state["decision"]

    approval_message = {
        "message": "Human approval required.",
        "action": decision["action"],
        "target": decision["target"],
        "description": decision["description"],
    }

    # Pause graph execution.
    #
    # The value supplied when the graph resumes
    # becomes the return value of interrupt().
    approved = interrupt(approval_message)

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
    target = decision["target"]

    if action == "search":

        result = (
            f"Search executed for: {target}"
        )

    elif action == "send_email":

        # Demonstration only.
        # No real email is sent.
        result = (
            f"Email action approved for: {target}"
        )

    elif action == "delete_file":

        # Demonstration only.
        # No real file is deleted.
        result = (
            f"Delete action approved for: {target}"
        )

    else:

        result = (
            "Normal response generated."
        )

    return {
        "result": result
    }


# ============================================================
# 9. Cancel Node
# ============================================================

def cancel_node(state: AgentState):

    action = state["decision"]["action"]

    return {
        "result": (
            f"Action '{action}' was rejected by the human. "
            "No action was executed."
        )
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
# 11. Graph Edges
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
# 12. Checkpointer
# ============================================================

memory = InMemorySaver()


app = builder.compile(
    checkpointer=memory
)


# ============================================================
# 13. Interactive Application
# ============================================================

config = {
    "configurable": {
        "thread_id": "day59_demo"
    }
}


print("=" * 60)
print("DAY 59 - HUMAN-IN-THE-LOOP AGENT")
print("=" * 60)

print("\nTry:")
print("  Search for admission requirements")
print("  Send an email to admin@example.com")
print("  Delete file report.pdf")
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
    # Check whether the graph is paused
    # --------------------------------------------------------

    state = app.get_state(config)

    if state.next:

        print("\n⚠️ HUMAN APPROVAL REQUIRED")

        decision = state.values["decision"]

        print(
            f"Action: {decision['action']}"
        )

        print(
            f"Target: {decision['target']}"
        )

        print(
            f"Description: {decision['description']}"
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
    print(result["result"])