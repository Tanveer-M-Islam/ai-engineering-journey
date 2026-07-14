# Campus AI Copilot

A production-style AI assistant built using LangChain, Ollama and FAISS.

---

## Features

- General Chat
- Tool Calling
- Retrieval-Augmented Generation (RAG)
- Conversation Memory
- Intent Routing

---

## Technologies

- Python
- LangChain
- Ollama
- FAISS
- HuggingFace Embeddings

---

## Project Structure

Day49_ai_copilot/

app.py

router.py

tools.py

rag.py

memory.py

vector_store.py

build_index.py

prompts.py

requirements.txt

documents/

faiss_index/

---

## Installation

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Build FAISS Index

```bash
python build_index.py
```

---

## Run

```bash
python app.py
```

---

## Example Questions

General Chat

Hello

Who are you?

Explain Artificial Intelligence.

---

Tool Calling

What time is it?

What is today's date?

Multiply 15 by 9.

---

Knowledge Base

What courses are offered?

Tell me about scholarships.

What IELTS score is required?

---

## Learning Outcomes

After completing this project you will understand:

- Tool Calling
- Retrieval-Augmented Generation
- Embeddings
- Vector Databases
- Intent Routing
- AI Application Architecture

---

## Author

AI Engineering 2026 Learning Roadmap