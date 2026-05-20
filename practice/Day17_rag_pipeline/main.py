import ollama

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
)


best_index = scores.argmax()


retrieved_chunk = chunks[
    best_index
]


prompt = f"""
Answer the question using ONLY the context below.

Context:
{retrieved_chunk}

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
    "\nRetrieved Context:\n"
)

print(
    retrieved_chunk
)

print(
    "\nAnswer:\n"
)

print(
    answer
)