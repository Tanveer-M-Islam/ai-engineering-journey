#fixed chunking

# with open(
#     "knowledge.txt",
#     "r",
#     encoding="utf-8"
# ) as f:

#     text = f.read()

# chunk_size = 50

# chunks = []

# for i in range(
#     0,
#     len(text),
#     chunk_size
# ):

#     chunk = text[
#         i:i+chunk_size
#     ]

#     chunks.append(
#         chunk
#     )

# print(
#     "\nFixed Chunks:\n"
# )

# for i, chunk in enumerate(
#     chunks,
#     start=1
# ):

#     print(
#         f"Chunk {i}:"
#     )

#     print(
#         chunk
#     )

#     print(
#         "-"*40
#     )



#recursive chunking
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

with open(
    "knowledge.txt",
    "r",
    encoding="utf-8"
) as f:

    text = f.read()

splitter = (
    RecursiveCharacterTextSplitter(
        chunk_size=50,
        chunk_overlap=20
    )
)

chunks = splitter.split_text(
    text
)

print(
    "\nRecursive Chunks:\n"
)

for i, chunk in enumerate(
    chunks,
    start=1
):

    print(
        f"Chunk {i}:"
    )

    print(
        chunk
    )

    print(
        "-"*40
    )