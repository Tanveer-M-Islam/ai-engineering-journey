import json
import ollama

from prompts import SYSTEM_PROMPT

from tools import (
    get_time,
    get_date,
    get_tomorrow_date,
    multiply
)

TOOLS = {

    "get_time": get_time,

    "get_date": get_date,

    "get_tomorrow_date": get_tomorrow_date,

    "multiply": multiply
}

messages = [

    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

while True:

    user_input = input(
        "\nYou: "
    )

    if user_input.lower() == "exit":

        break

    messages.append(

        {
            "role": "user",
            "content": user_input
        }
    )

    while True:

        response = ollama.chat(

            model="llama3.2",

            messages=messages
        )

        output = response[
            "message"
        ][
            "content"
        ]

        try:

            tool_request = json.loads(
                output
            )

            tool_name = tool_request[
                "tool"
            ]

            arguments = tool_request[
                "arguments"
            ]

            result = TOOLS[
                tool_name
            ](
                **arguments
            )

            print(
                f"\nTOOL [{tool_name}] =>",
                result
            )

            messages.append(

                {
                    "role": "assistant",
                    "content": output
                }
            )

            messages.append(

                {
                    "role": "user",
                    "content":
                    f"Tool Result: {result}"
                }
            )

        except:

            print(
                "\nAI:",
                output
            )

            messages.append(

                {
                    "role": "assistant",
                    "content": output
                }
            )

            break