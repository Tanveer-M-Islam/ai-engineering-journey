# from sentence_transformers import SentenceTransformer


# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# sentences = [

#     "Cats drink milk.",

#     "Dogs are loyal animals.",

#     "Neural networks learn patterns.",

#     "Python is a programming language."
# ]


# embeddings = model.encode(
#     sentences
# )


# print(
#     embeddings.shape
# )




#Search by meaning
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

    "Cats drink milk.",

    "Dogs are loyal animals.",

    "Neural networks learn patterns.",

    "Python is a programming language."
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
