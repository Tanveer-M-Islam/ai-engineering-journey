from typing import Annotated

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition


# ============================================================
# 1. LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# 2. TOOLS
# ============================================================

@tool
def calculator(
    a: float,
    b: float,
    operation: str,
) -> str:
    """
    Perform a basic mathematical operation.

    operation must be one of:
    add, subtract, multiply, divide
    """

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":

        if b == 0:
            return "Error: Cannot divide by zero."

        result = a / b

    else:
        return (
            "Error: operation must be "
            "add, subtract, multiply, or divide."
        )

    return str(result)


@tool
def get_weather(city: str) -> str:
    """
    Return demo weather information for a city.
    """

    weather_data = {
        "dhaka": "Dhaka is currently 31°C and partly cloudy.",
        "london": "London is currently 18°C and cloudy.",
        "new york": "New York is currently 24°C and sunny.",
        "tokyo": "Tokyo is currently 27°C and clear.",
    }

    city_key = city.lower().strip()

    if city_key in weather_data:
        return weather_data[city_key]

    return f"No weather data available for {city}."


# ============================================================
# 3. REGISTER TOOLS
# ============================================================

tools = [
    calculator,
    get_weather,
]


# ============================================================
# 4. BIND TOOLS TO THE LLM
# ============================================================

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 5. AGENT NODE
# ============================================================

def agent(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ============================================================
# 6. CREATE TOOL NODE
# ============================================================

tool_node = ToolNode(tools)


# ============================================================
# 7. BUILD GRAPH
# ============================================================

builder = StateGraph(MessagesState)


builder.add_node(
    "agent",
    agent,
)

builder.add_node(
    "tools",
    tool_node,
)


# ============================================================
# 8. GRAPH EDGES
# ============================================================

builder.add_edge(
    START,
    "agent",
)


builder.add_conditional_edges(
    "agent",
    tools_condition,
)


builder.add_edge(
    "tools",
    "agent",
)


# ============================================================
# 9. COMPILE GRAPH
# ============================================================

app = builder.compile()


# ============================================================
# 10. RUN APPLICATION
# ============================================================

print("=" * 70)
print("🤖 Day 54 - LangGraph Tool Calling Agent")
print("=" * 70)

print("\nAvailable tools:")
print("- calculator")
print("- get_weather")

print("\nExamples:")
print("- What is 25 multiplied by 8?")
print("- What is 100 divided by 4?")
print("- What is the weather in Dhaka?")
print("- What is the weather in London?")

print("\nType 'exit' to quit.")


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
    print(final_message.content)