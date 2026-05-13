
#streaming response from ollama
# import ollama

# question = input("You: ")

# stream = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are an AI mentor."
#         },
#         {
#             "role": "user",
#             "content": question
#         }
#     ],
#     stream=True
# )

# print("AI: ", end="")

# for chunk in stream:

#     content = chunk["message"]["content"]

#     print(
#         content,
#         end="",
#         flush=True
#     )

# print()


#Streaming response with conversation history
import ollama

messages = [
    {
        "role": "system",
        "content": "You are an AI engineering mentor."
    }
]

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

    stream = ollama.chat(
        model="llama3.2",
        messages=messages,
        stream=True
    )

    print("AI: ", end="")

    full_response = ""

    for chunk in stream:

        text = chunk["message"]["content"]

        full_response += text

        print(
            text,
            end="",
            flush=True
        )

    print()

    messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    import json

with open(
    "chat_history.json",
    "w"
) as f:

    json.dump(
        messages,
        f,
        indent=4
    )