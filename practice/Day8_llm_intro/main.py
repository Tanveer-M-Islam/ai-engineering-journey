# import ollama

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful AI mentor."
#         },
#         {
#             "role": "user",
#             "content": "Explain AI engineering in simple words."
#         }
#     ]
# )

# print(
#     response["message"]["content"]
# )


import ollama


question = input("You: ")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": "You are an AI mentor."
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

print(
    "AI:",
    response["message"]["content"]
)