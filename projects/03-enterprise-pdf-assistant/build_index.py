import fitz
import faiss
import json
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


pdf_path = "sample.pdf"


doc = fitz.open(
    pdf_path
)


text = ""


for page in doc:

    text += page.get_text()


chunk_size = 500


chunks = []


for i in range(

    0,

    len(text),

    chunk_size
):

    chunk = text[
        i:i + chunk_size
    ]

    chunks.append(
        chunk
    )


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
    "Index built successfully."
)