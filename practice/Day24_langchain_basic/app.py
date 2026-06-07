#basic langchain app

# from langchain_ollama import ChatOllama

# llm = ChatOllama(
#     model="llama3.2"
# )

# response = llm.invoke(
#     "What is Artificial Intelligence?"
# )

# print(
#     response.content
# )

from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    ChatPromptTemplate
)

llm = ChatOllama(
    model="llama3.2",
    streaming=True
)

prompt = ChatPromptTemplate.from_template(
    """
You are an AI Engineering Mentor.

Explain:

{topic}

In beginner friendly language.
"""
)

while True:

    topic = input(
        "\nTopic: "
    )

    if topic.lower() == "exit":
        break

    chain = prompt | llm

    response = chain.invoke(
        {
            "topic": topic
        }
    )

    print(
        "\nAI:"
    )

    print(
        response.content
    )