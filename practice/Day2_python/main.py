# Dictionary in Python

student = {
    "name": "Tanveer",
    "goal": "AI Engineer",
    "skills": ["Python", "ML", "Research"]
}

print(student)
print(student["name"])
print(student["skills"])

#list in Python

messages = [
    "Hello",
    "Summarize this",
    "Translate this"
]

print(messages[0])

#Real example of List & Dictionary

chat_history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi"}
]
print(chat_history[0]["content"])



#function in Python
def summarize(text):
    return text[:50]

result = summarize("AI Engineering is one of the hottest careers.")
print(result)


#json in Python
import json

user_data = {
    "name": "Tanveer",
    "goal": "AI Engineer"
}

with open("data.json", "w") as f:
    json.dump(user_data, f, indent=4)

with open("data.json", "r") as f:
    data = json.load(f)

print(data)

#dotenv in Python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print(api_key)



#mini practice

user_profile = {
    "name": "Tanveer",
    "country": "Bangladesh",
    "career_goal": "Generative AI Engineer",
    "learning_day": 2
}

with open("data.json", "w") as f:
    json.dump(user_profile, f, indent=4)

with open("data.json", "r") as f:
    data = json.load(f)
print(f"Welcome {data['name']} from {data['country']}")