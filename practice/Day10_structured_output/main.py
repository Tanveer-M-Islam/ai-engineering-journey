# #JSON Prompt

# import ollama

# prompt = """
# Return only valid JSON.

# {
#   "topic":"",
#   "difficulty":"",
#   "summary":""
# }

# Explain FastAPI.
# """

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a precise AI assistant."
#         },
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )

# print(
#     response["message"]["content"]
# )

#parse the JSON response
# import json
# import ollama

# prompt = """
# Analyze this text and return ONLY valid JSON.

# Required format:

# {
#     "topic": "string",
#     "summary": "string",
#     "keywords": ["string"]
# }

# Do not explain.
# Do not add markdown.
# Do not add extra text.

# Text:
# FastAPI is a modern Python web framework...
# """

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a precise AI assistant."
#         },
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )

# result = response["message"]["content"]

# print(result)

# try:

#     data = json.loads(result)

#     print(data)

# except json.JSONDecodeError:

#     print("Invalid JSON from model")
# data = json.loads(result)

# print(data)


import json
import ollama

prompt = """
Analyze this question and return ONLY valid JSON.

Required format:

{
  "skills": ["skill1", "skill2", "skill3"],
  "career_path": "string",
  "difficulty": "Beginner | Intermediate | Advanced"
}

Fill every field with meaningful values.
Do not leave fields empty.
Do not explain.
Do not add markdown.

Question:
What skills are needed to become an AI engineer?
"""

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": "You are a precise AI assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

result = response["message"]["content"]

print(result)

try:

    data = json.loads(result)

    print(data["skills"])
    print(data)

except json.JSONDecodeError:

    print("Invalid JSON from model")