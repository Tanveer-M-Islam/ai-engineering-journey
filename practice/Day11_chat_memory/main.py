import ollama

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI mentor."
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

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    ai_message = response["message"]["content"]

    print("AI:", ai_message)

    messages.append(
        {
            "role": "assistant",
            "content": ai_message
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