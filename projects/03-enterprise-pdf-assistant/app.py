import faiss
import json
import ollama
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


index = faiss.read_index(
    "vector_index.faiss"
)


with open(
    "chunks.json",
    "r"
) as f:

    chunks = json.load(f)


while True:

    question = input(
        "\nQuestion: "
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


    top_k = 3


    distances, indices = index.search(

        question_embedding,

        top_k
    )


    retrieved_chunks = []


    for i in indices[0]:

        retrieved_chunks.append(
            chunks[i]
        )


    context = "\n\n".join(
        retrieved_chunks
    )


    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {question}
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
        "\nAnswer:\n"
    )

    print(
        answer
    )