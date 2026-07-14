from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from router import detect_intent
from rag import answer_from_documents
from memory import ConversationMemory
from prompts import CHAT_PROMPT

from tools import (
    get_time,
    get_date,
    multiply,
)

# ----------------------------------------------------
# Load LLM
# ----------------------------------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# ----------------------------------------------------
# Conversation Memory
# ----------------------------------------------------

memory = ConversationMemory()

# ----------------------------------------------------
# Create Tool Agent
# ----------------------------------------------------

agent = create_agent(
    model=llm,
    tools=[
        get_time,
        get_date,
        multiply,
    ],
    system_prompt=CHAT_PROMPT,
)

# ----------------------------------------------------
# Banner
# ----------------------------------------------------

print("=" * 60)
print("🎓 Campus AI Copilot")
print("=" * 60)
print("Type 'exit' to quit.")

# ----------------------------------------------------
# Main Loop
# ----------------------------------------------------

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # Detect intent
    intent = detect_intent(question)

    print(f"\n[Intent: {intent}]")

    # ====================================================
    # RAG
    # ====================================================

    if intent == "rag":

        answer = answer_from_documents(question)

        print("\nAI:\n")
        print(answer)

        continue

    # ====================================================
    # TOOL AGENT
    # ====================================================

    elif intent == "tool":

        memory.add_user_message(question)

        response = agent.invoke(
            {
                "messages": memory.get_messages()
            }
        )

        assistant = response["messages"][-1].content

        print("\nAI:\n")
        print(assistant)

        memory.add_ai_message(assistant)

    # ====================================================
    # GENERAL CHAT
    # ====================================================

    else:

        memory.add_user_message(question)

        response = llm.invoke(
            memory.get_messages()
        )

        assistant = response.content

        print("\nAI:\n")
        print(assistant)

        memory.add_ai_message(assistant)