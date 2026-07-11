from vector_store import retriever

docs = retriever.invoke("courses")

for doc in docs:
    print(doc.metadata)
    print(doc.page_content)