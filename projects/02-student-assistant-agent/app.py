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


TOOLS = {

    "get_time": get_time,

    "get_date": get_date,

    "multiply": multiply,

    "calculate_gpa": calculate_gpa,

    "start_timer": start_timer
}


messages = [

    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:

    user_input = input(
        "You: "
    )

    if user_input.lower() == "exit":
        break

    messages.append(

        {
            "role": "user",
            "content": user_input
        }
    )

    response_stream = ollama.chat(

        model="llama3.2",

        messages=messages,

        stream=True
    )

    full_output = ""

    print(
        "AI: ",
        end=""
    )

    for chunk in response_stream:

        text = chunk[
            "message"
        ][
            "content"
        ]

        full_output += text

        print(
            text,
            end="",
            flush=True
        )

    print()

    try:

        tool_request = json.loads(
            full_output
        )

        tool_name = tool_request[
            "tool"
        ]

        arguments = tool_request[
            "arguments"
        ]

        if tool_name in TOOLS:

            result = TOOLS[
                tool_name
            ](
                **arguments
            )

            print(
                "TOOL:",
                result
            )

            messages.append(

                {
                    "role": "assistant",
                    "content": str(result)
                }
            )

        else:

            print(
                "Unknown tool."
            )

    except json.JSONDecodeError:

        messages.append(

            {
                "role": "assistant",
                "content": full_output
            }
        )

    with open(
        "chat_history.json",
        "w"
    ) as f:

        json.dump(
            messages,
            f,
            indent=4
        )