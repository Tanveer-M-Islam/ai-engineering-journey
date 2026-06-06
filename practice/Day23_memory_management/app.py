import faiss
import json
import ollama
import numpy as np
import os

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

if os.path.exists(
    "chat_history.json"
):

    with open(
        "chat_history.json",
        "r",
        encoding="utf-8"
    ) as f:

        chat_history = json.load(f)

else:

    chat_history = []

if os.path.exists(
    "memory_summary.txt"
):

    with open(
        "memory_summary.txt",
        "r",
        encoding="utf-8"
    ) as f:

        memory_summary = f.read()

else:

    memory_summary = ""

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

    recent_history = chat_history[-6:]

    history_text = ""

    for msg in recent_history:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
Memory Summary:
{memory_summary}

Knowledge Context:
{context}

Recent Conversation:
{history_text}

Current Question:
{question}

Answer naturally.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role":"user",
                "content":prompt
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
            "role":"user",
            "content":question
        }
    )

    chat_history.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

    with open(
        "chat_history.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chat_history,
            f,
            indent=4
        )

    if len(chat_history) >= 6:

        summary_prompt = f"""
Summarize this conversation briefly.

{chat_history}
"""

        summary_response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role":"user",
                    "content":summary_prompt
                }
            ]
        )

        memory_summary = summary_response[
            "message"
        ][
            "content"
        ]

        with open(
            "memory_summary.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                memory_summary
            )

        chat_history = []