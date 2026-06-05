import faiss
import numpy as np
import json

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


faiss.write_index(
    index,
    "vector_index.faiss"
)


with open(
    "chunks.json",
    "w"
) as f:

    json.dump(
        chunks,
        f,
        indent=4
    )


print(
    "Index saved successfully."
)