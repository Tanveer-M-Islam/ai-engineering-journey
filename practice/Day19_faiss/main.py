import faiss
import numpy as np
import ollama

from sentence_transformers import (
    SentenceTransformer
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


embeddings = model.encode(
    chunks
)


embeddings = np.array(
    embeddings,
    dtype="float32"
)


dimension = embeddings.shape[1]


index = faiss.IndexFlatL2(
    dimension
)


index.add(
    embeddings
)


question = input(
    "Question: "
)


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
    "\nRetrieved Chunks:\n"
)

for chunk in retrieved_chunks:

    print("-", chunk)


print(
    "\nAnswer:\n"
)

print(answer)