import faiss
import json
import ollama
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "vector_index.faiss"
)

with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

chat_history = []

while True:

    question = input(
        "\nYou: "
    )

    if question.lower() == "exit":
        break

    question_embedding = model.encode(
        [question]
    )

    question_embedding = np.array(
        question_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        question_embedding,
        3
    )

    retrieved_chunks = []

    for idx in indices[0]:

        retrieved_chunks.append(
            chunks[idx]
        )

    context = "\n".join(
        retrieved_chunks
    )

    history_text = ""

    for message in chat_history:

        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are an AI Study Assistant.

Knowledge Context:
{context}

Conversation History:
{history_text}

Current Question:
{question}

Answer based on the context and history.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response[
        "message"
    ][
        "content"
    ]

    print(
        "\nAI:",
        answer
    )

    chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )