PDF Chatbot

Pipeline:

PDF
 ↓
Loader
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS
 ↓
Retriever
 ↓
LLM

Chunking:
Splits large documents into smaller pieces.

Chunk Overlap:
Preserves context between chunks.

Retriever:
Returns relevant chunks for a query.