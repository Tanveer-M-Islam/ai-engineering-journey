import ollama
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


with open(
    "knowledge.txt",
    "r"
) as f:

    text = f.read()


chunks = text.split("\n\n")


chunk_embeddings = model.encode(
    chunks
)


question = input(
    "Question: "
)


question_embedding = model.encode(
    [question]
)


scores = cosine_similarity(

    question_embedding,

    chunk_embeddings
)[0]


top_k = 3


top_indices = np.argsort(
    scores
)[-top_k:][::-1]


retrieved_chunks = []


for index in top_indices:

    retrieved_chunks.append(
        chunks[index]
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
    "\nRetrieved Chunks:\n"
)

for chunk in retrieved_chunks:

    print(
        "-",
        chunk
    )


print(
    "\nAnswer:\n"
)

print(
    answer
)