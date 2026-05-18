from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


documents = [

    "Operating systems manage hardware.",

    "Databases store structured data.",

    "Machine learning learns from data.",

    "FastAPI builds APIs."
]


doc_vectors = model.encode(
    documents
)


query = input(
    "Search: "
)


query_vector = model.encode(
    [query]
)


scores = cosine_similarity(

    query_vector,

    doc_vectors
)


best_index = scores.argmax()


print(
    "Best Match:"
)

print(
    documents[
        best_index
    ]
)