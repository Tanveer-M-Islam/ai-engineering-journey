from datetime import datetime
from langchain_core.tools import tool

from vector_store import retriever


# -------------------------------------------------
# TIME
# -------------------------------------------------

@tool
def get_time() -> str:
    """
    Returns the current local time.

    Use ONLY when the user explicitly asks
    for the current time.
    """

    return datetime.now().strftime("%I:%M %p")


# -------------------------------------------------
# DATE
# -------------------------------------------------

@tool
def get_date() -> str:
    """
    Returns today's date.

    Use ONLY when the user explicitly asks
    for today's date.
    """

    return datetime.now().strftime("%d %B %Y")


# -------------------------------------------------
# MULTIPLY
# -------------------------------------------------

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.
    """

    return a * b


# -------------------------------------------------
# SEARCH DOCUMENTS
# -------------------------------------------------

@tool
def search_documents(query: str) -> str:
    """
    Search the university knowledge base.

    Use when answering questions related to:
    - courses
    - admission
    - scholarship
    - IELTS
    - university information
    """

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    context = []

    for doc in docs:

        source = doc.metadata.get("source", "Unknown")

        context.append(
            f"[Source: {source}]\n{doc.page_content}"
        )

    return "\n\n".join(context)