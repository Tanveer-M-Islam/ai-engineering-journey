import faiss
import json
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

with open(
    "knowledge.txt",
    "r",
    encoding="utf-8"
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

index = faiss.IndexFlatL2(
    embeddings.shape[1]
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
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        indent=4
    )

print(
    "Index created."
)