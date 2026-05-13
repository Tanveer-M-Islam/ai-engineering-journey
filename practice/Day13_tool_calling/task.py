import ollama
from datetime import datetime
import time


# ======================
# Tools
# ======================

def get_current_time():

    return datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )


def calculate_gpa(grades):

    total = sum(grades)

    gpa = total / len(grades)

    return round(gpa, 2)


def start_timer(minutes):

    seconds = minutes * 60

    print(f"Timer started for {minutes} minutes")

    time.sleep(seconds)

    return "Study session completed!"


# ======================
# Memory
# ======================

messages = [
    {
        "role": "system",
        "content": """
You are a student assistant.

Available tools:

1. Current time:
CALL_TOOL:get_time

2. GPA:
CALL_TOOL:gpa:3.5,3.7,4.0

3. Study timer:
CALL_TOOL:timer:1

Use tools when needed.
"""
    }
]


# ======================
# Agent loop
# ======================

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    ai_output = response["message"]["content"]

    command = ai_output.strip().lower()


    # -------------------
    # Time Tool
    # -------------------
    if "call_tool:get_time" in command:

        tool_result = get_current_time()


    # -------------------
    # GPA Tool
    # -------------------
    elif "call_tool:gpa" in command:

        parts = command.split(":")

        grades = parts[2].split(",")

        grades = [
            float(g.strip())
            for g in grades
        ]

        tool_result = calculate_gpa(
            grades
        )


    # -------------------
    # Timer Tool
    # -------------------
    elif "call_tool:timer" in command:

        parts = command.split(":")

        minutes = int(
            parts[2]
        )

        tool_result = start_timer(
            minutes
        )


    # -------------------
    # Normal chat
    # -------------------
    else:

        tool_result = ai_output


    print("AI:", tool_result)


    messages.append(
        {
            "role": "assistant",
            "content": str(
                tool_result
            )
        }
    )