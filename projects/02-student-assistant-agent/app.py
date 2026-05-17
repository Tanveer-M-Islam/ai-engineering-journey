import json
import ollama

from prompts import SYSTEM_PROMPT
from tools import (
    get_time,
    get_date,
    multiply,
    calculate_gpa,
    start_timer
)


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def save_chat(messages):

    with open(
        "chat_history.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            messages,
            f,
            indent=4,
            ensure_ascii=False
        )


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        save_chat(messages)
        break

    # ✅ ADD USER ONLY ONCE
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    lower_input = user_input.lower()

    final_answer = None

    # -------------------
    # TOOL ROUTING
    # -------------------

    if "time" in lower_input:

        final_answer = get_time()

    elif "date" in lower_input:

        final_answer = get_date()

    elif "multiply" in lower_input or "*" in lower_input:

        numbers = []

        for word in lower_input.replace("*", " ").split():

            if word.isdigit():
                numbers.append(int(word))

        if len(numbers) >= 2:

            final_answer = multiply(
                numbers[0],
                numbers[1]
            )

    elif "gpa" in lower_input:

        numbers = []

        for word in lower_input.split():

            if word.isdigit():
                numbers.append(int(word))

        if len(numbers) >= 2:

            final_answer = calculate_gpa(
                numbers[0],
                numbers[1]
            )

    elif "timer" in lower_input:

        numbers = []

        for word in lower_input.split():

            if word.isdigit():
                numbers.append(int(word))

        if len(numbers) >= 1:

            final_answer = start_timer(
                numbers[0]
            )

    # -------------------
    # NORMAL CHAT
    # -------------------

    if final_answer is None:

        response = ollama.chat(
            model="llama3.2",
            messages=messages,
            stream=False
        )

        final_answer = response[
            "message"
        ][
            "content"
        ]

    print("AI:", final_answer)

    # ✅ ADD ASSISTANT ONLY ONCE
    messages.append(
        {
            "role": "assistant",
            "content": str(final_answer)
        }
    )

    save_chat(messages)