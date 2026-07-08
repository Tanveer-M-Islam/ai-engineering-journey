from datetime import datetime

from langchain_core.tools import tool


@tool
def get_time() -> str:
    """Return the current local time."""

    return datetime.now().strftime("%I:%M %p")


@tool
def get_date() -> str:
    """Return today's date."""

    return datetime.now().strftime("%d-%m-%Y")


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""

    return a * b