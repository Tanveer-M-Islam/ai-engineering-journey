#chunking document into smaller pieces
# from sentence_transformers import (
#     SentenceTransformer
# )

# from sklearn.metrics.pairwise import (
#     cosine_similarity
# )


# with open(
#     "sample.txt",
#     "r"
# ) as f:

#     text = f.read()


# chunks = text.split("\n\n")


# print(
#     "Chunks:"
# )

# for chunk in chunks:

#     print(chunk)

#modfied code to use sentence transformers for chunking
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
    "sample.txt",
    "r"
) as f:

    text = f.read()


chunks = text.split("\n\n")


chunk_embeddings = model.encode(
    chunks
)


query = input(
    "Search: "
)


query_embedding = model.encode(
    [query]
)


scores = cosine_similarity(

    query_embedding,

    chunk_embeddings
)


best_index = scores.argmax()


print(
    "\nBest Match:\n"
)

print(
    chunks[
        best_index
    ]
)