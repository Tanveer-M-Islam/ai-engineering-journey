from typing import List

from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition


# ============================================================
# 1. LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# 2. EMBEDDING MODEL
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)


# ============================================================
# 3. LOAD DOCUMENTS
# ============================================================

documents = [
    Document(
        page_content=open(
            "data/admission.txt",
            encoding="utf-8",
        ).read(),
        metadata={
            "source": "admission.txt"
        },
    ),
    Document(
        page_content=open(
            "data/scholarship.txt",
            encoding="utf-8",
        ).read(),
        metadata={
            "source": "scholarship.txt"
        },
    ),
    Document(
        page_content=open(
            "data/courses.txt",
            encoding="utf-8",
        ).read(),
        metadata={
            "source": "courses.txt"
        },
    ),
]


# ============================================================
# 4. CHUNK DOCUMENTS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = text_splitter.split_documents(
    documents
)


print(f"Loaded {len(documents)} documents.")
print(f"Created {len(chunks)} chunks.")


# ============================================================
# 5. CREATE FAISS VECTOR STORE
# ============================================================

vectorstore = FAISS.from_documents(
    chunks,
    embeddings,
)


# ============================================================
# 6. CREATE RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)


# ============================================================
# 7. CREATE RAG TOOL
# ============================================================

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the university knowledge base for factual
    information about admission, scholarships, courses,
    departments, and university policies.

    Use this tool whenever the user's question requires
    information from the university documents.
    """

    results = retriever.invoke(query)

    if not results:
        return "No relevant information was found."

    formatted_results = []

    for i, document in enumerate(results, start=1):

        formatted_results.append(
            f"Document {i}\n"
            f"Source: {document.metadata.get('source')}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n".join(formatted_results)


# ============================================================
# 8. REGISTER TOOLS
# ============================================================

tools = [
    search_knowledge_base,
]


# ============================================================
# 9. BIND TOOLS TO LLM
# ============================================================

llm_with_tools = llm.bind_tools(
    tools
)


# ============================================================
# 10. AGENT NODE
# ============================================================

def agent(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ============================================================
# 11. TOOL NODE
# ============================================================

tool_node = ToolNode(
    tools
)


# ============================================================
# 12. BUILD GRAPH
# ============================================================

builder = StateGraph(
    MessagesState
)


builder.add_node(
    "agent",
    agent,
)


builder.add_node(
    "tools",
    tool_node,
)


# ============================================================
# 13. EDGES
# ============================================================

builder.add_edge(
    START,
    "agent",
)


builder.add_conditional_edges(
    "agent",
    tools_condition,
)


builder.add_edge(
    "tools",
    "agent",
)


# ============================================================
# 14. COMPILE
# ============================================================

app = builder.compile()


# ============================================================
# 15. CHAT LOOP
# ============================================================

print("\n" + "=" * 70)
print("🤖 Day 55 - LangGraph + RAG Agent")
print("=" * 70)

print("\nThe agent can search:")
print("- Admission information")
print("- Scholarship information")
print("- Computer Science courses")

print("\nType 'exit' to quit.")


while True:

    question = input("\nYou: ")

    if question.lower().strip() == "exit":
        print("\nGoodbye!")
        break

    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        }
    )

    final_message = result["messages"][-1]

    print("\nAI:")
    print(final_message.content)