from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


loader = PyPDFLoader(
    "sample.pdf"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(
    documents
)

embedding_model = HuggingFaceEmbeddings(
    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(
    chunks,
    embedding_model
)

vectorstore.save_local(
    "faiss_index"
)

print(
    "PDF indexed successfully."
)