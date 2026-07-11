from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import (
    get_time,
    get_date,
    multiply,
    search_documents,
)

# -----------------------------------
# Load Model
# -----------------------------------

model = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# -----------------------------------
# Agent
# -----------------------------------

agent = create_agent(
    model=model,
    tools=[
        get_time,
        get_date,
        multiply,
    ],  # Notice: search_documents is NOT registered here
    system_prompt="""
You are a helpful AI assistant.

Rules:

- Use get_time only when the user asks for time.
- Use get_date only when the user asks for today's date.
- Use multiply only for multiplication.
- Otherwise answer normally.
""",
)

# -----------------------------------
# Conversation Memory
# -----------------------------------

messages = []

# -----------------------------------
# Keywords for RAG
# -----------------------------------

DOCUMENT_KEYWORDS = [
    "course",
    "courses",
    "admission",
    "scholarship",
    "program",
    "programs",
    "ielts",
    "deadline",
    "university",
]

print("=" * 60)
print("🤖 Agentic RAG Assistant")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # -----------------------------
    # ROUTER
    # -----------------------------

    lower_question = question.lower()

    if any(keyword in lower_question for keyword in DOCUMENT_KEYWORDS):

        print("\n🔍 Searching knowledge base...\n")

        context = search_documents.invoke(
            {
                "query": question
            }
        )

        prompt = f"""
Answer ONLY from the following context.

If the answer is not available,
say you don't know.

Context:

{context}

Question:

{question}
"""

        answer = model.invoke(prompt)

        print("AI:\n")
        print(answer.content)

        continue

    # -----------------------------
    # NORMAL AGENT
    # -----------------------------

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = agent.invoke(
        {
            "messages": messages
        }
    )

    assistant = response["messages"][-1]

    print("\nAI:\n")
    print(assistant.content)

    messages.append(
        {
            "role": "assistant",
            "content": assistant.content,
        }
    )