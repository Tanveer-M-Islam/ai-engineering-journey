from langchain_ollama import ChatOllama

from prompts import RAG_PROMPT
from tools import search_documents


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


def answer_from_documents(question: str) -> str:
    """
    Search the knowledge base and answer
    using only the retrieved context.
    """

    context = search_documents.invoke(
        {
            "query": question
        }
    )

    prompt = f"""
{RAG_PROMPT}

Context:

{context}

Question:

{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content