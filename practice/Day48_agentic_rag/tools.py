from datetime import datetime

from langchain_core.tools import tool

from vector_store import retriever


@tool
def get_time() -> str:
    """Return current time."""

    return datetime.now().strftime("%I:%M %p")


@tool
def get_date() -> str:
    """Return today's date."""

    return datetime.now().strftime("%d-%m-%Y")


@tool
def multiply(
    a: int,
    b: int
) -> int:
    """Multiply two integers."""

    return a * b


@tool
def search_documents(
    query: str
) -> str:
    """
    Search the knowledge base and return relevant information.
    """

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    context = ""

    for doc in docs:

        context += doc.page_content + "\n\n"

    return context