from rank_bm25 import BM25Okapi

from sentence_transformers import (
    SentenceTransformer
)

import faiss
import numpy as np


# ==========================
# Load Knowledge Base
# ==========================

with open(
    "knowledge.txt",
    "r",
    encoding="utf-8"
) as f:

    text = f.read()


documents = [

    chunk.strip()

    for chunk in text.split("\n\n")

    if chunk.strip()
]


# ==========================
# BM25 Setup
# ==========================

tokenized_docs = [

    doc.lower().split()

    for doc in documents
]

bm25 = BM25Okapi(
    tokenized_docs
)


# ==========================
# Embedding Model
# ==========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================
# Create Embeddings
# ==========================

embeddings = model.encode(
    documents
)


# ==========================
# FAISS Index
# ==========================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    np.array(
        embeddings
    )
)


# ==========================
# Hybrid Search Function
# ==========================

def hybrid_search(
    query
):

    tokenized_query = (
        query.lower().split()
    )

    bm25_scores = bm25.get_scores(
        tokenized_query
    )

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(

        np.array(
            query_embedding
        ),

        len(documents)
    )

    combined_scores = {}

    for i in range(
        len(documents)
    ):

        combined_scores[i] = 0

    # BM25 Scores

    for i, score in enumerate(
        bm25_scores
    ):

        combined_scores[i] += score

    # Semantic Scores

    for rank, idx in enumerate(
        indices[0]
    ):

        semantic_score = (

            len(documents)

            - rank
        )

        combined_scores[idx] += (
            semantic_score
        )

    results = sorted(

        combined_scores.items(),

        key=lambda x: x[1],

        reverse=True
    )

    return results


# ==========================
# Chat Loop
# ==========================

while True:

    query = input(
        "\nQuestion: "
    )

    if query.lower() == "exit":

        break

    results = hybrid_search(
        query
    )

    print(
        "\nTop Results:\n"
    )

    for idx, score in results[:3]:

        print(
            f"Score: {score:.2f}"
        )

        print(
            documents[idx]
        )

        print(
            "-" * 50
        )