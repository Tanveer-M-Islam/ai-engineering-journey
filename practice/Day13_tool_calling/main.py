
#Simple tool calling example without using ollama
# from datetime import datetime


# def get_time():

#     return datetime.now().strftime(
#         "%I:%M %p"
#     )


# def add_numbers(a, b):

#     return a + b

# question = input("You: ").lower()

# if "time" in question:

#     result = get_time()

#     print("AI:", result)


# elif "+" in question:

#     numbers = question.split("+")

#     a = int(numbers[0].strip())

#     b = int(numbers[1].strip())

#     result = add_numbers(a, b)

#     print("AI:", result)


#Tool calling example using ollama
import ollama
from datetime import datetime


def get_time():

    return datetime.now().strftime(
        "%I:%M %p"
    )

def multiply(a, b):

    return a * b



messages = [
    {
        "role": "system",
        "content": """
You are an AI agent.

Rules:

If user asks about time,
respond with:

CALL_TOOL:get_time

If multiplication is needed,
return:

CALL_TOOL:multiply:a,b

Otherwise answer normally.
"""
    }
]


while True:

    user_input = input("You: ")

    if user_input == "exit":
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

    if "call_tool:get_time" in command:

        tool_result = get_time()

        print("AI:", tool_result)

        messages.append(
            {
                "role": "assistant",
                "content": tool_result
            }
        )

    elif "call_tool:multiply" in command:

        numbers = command.split(":")[2].split(",")

        a = int(numbers[0].strip())

        b = int(numbers[1].strip())

        tool_result = multiply(a, b)

        print("AI:", tool_result)

        messages.append(
            {
                "role": "assistant",
                "content": tool_result
            }
        )

    else:

        print("AI:", ai_output)

        messages.append(
            {
                "role": "assistant",
                "content": ai_output
            }
        )