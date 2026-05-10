# import ollama

# prompt = input("Prompt: ")

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )

# print(
#     response["message"]["content"]
# )







#Few-Shot Prompting

# import ollama

# prompt = """
# Translate English to Bangla.

# Example:
# Hello → হ্যালো
# Good morning → সুপ্রভাত

# Translate:
# How are you?
# """

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )

# print(
#     response["message"]["content"]
# )




#Build Prompt Lab v1

import ollama

mode = input(
    "Choose mode (zero/few/json): "
)

if mode == "zero":

    prompt = "Explain FastAPI."

elif mode == "few":

    prompt = """
English to Bangla:

Hello → হ্যালো
Thank you → ধন্যবাদ

Good night →
"""

else:

    prompt = """
Return JSON only.

{
  "topic":"",
  "summary":""
}

Explain Python.
"""

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": "You are an AI mentor."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(
    response["message"]["content"]
)