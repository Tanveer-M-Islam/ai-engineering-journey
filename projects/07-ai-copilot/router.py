from langchain_ollama import ChatOllama

from prompts import ROUTER_PROMPT


router_llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


def detect_intent(question: str) -> str:
    """
    Detect the user's intent.

    Returns:
        chat
        tool
        rag
    """

    prompt = f"""
{ROUTER_PROMPT}

User Question:

{question}
"""

    response = router_llm.invoke(prompt)

    intent = response.content.strip().lower()

    if intent not in ["chat", "tool", "rag"]:
        return "chat"

    return intent