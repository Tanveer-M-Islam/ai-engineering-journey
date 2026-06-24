from datetime import datetime

from langchain_core.tools import tool


@tool
def get_time():

    """
    Get the current time.
    """

    return datetime.now().strftime(
        "%I:%M %p"
    )


@tool
def get_date():

    """
    Get today's date.
    """

    return datetime.now().strftime(
        "%d-%m-%Y"
    )


@tool
def multiply(
    a: int,
    b: int
):

    """
    Multiply two numbers.
    """

    return a * b