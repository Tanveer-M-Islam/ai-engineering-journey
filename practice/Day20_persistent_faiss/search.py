import faiss
import json
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


print(
    "\nRetrieved Chunks:\n"
)


for i in indices[0]:

    print(
        "-",
        chunks[i]
    )