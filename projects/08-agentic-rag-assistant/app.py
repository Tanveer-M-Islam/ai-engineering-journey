from typing import TypedDict

from langchain_ollama import ChatOllama, OllamaEmbeddings

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
)

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)


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

def load_documents():

    documents = []

    file_names = [
        "admission.txt",
        "scholarship.txt",
        "courses.txt",
    ]

    for file_name in file_names:

        path = f"data/{file_name}"

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            content = file.read()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_name
                },
            )
        )

    return documents


documents = load_documents()


print(
    f"Loaded {len(documents)} documents."
)


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


print(
    f"Created {len(chunks)} chunks."
)


# ============================================================
# 5. CREATE VECTOR STORE
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
# 7. RAG TOOL
# ============================================================

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the university knowledge base.

    Use this tool when the user asks about university
    admission, scholarships, courses, departments,
    or other information that may be contained in
    the university documents.
    """

    results = retriever.invoke(query)

    if not results:

        return (
            "No relevant information was found "
            "in the knowledge base."
        )

    output = []

    for index, document in enumerate(
        results,
        start=1,
    ):

        source = document.metadata.get(
            "source",
            "unknown",
        )

        output.append(
            f"Document {index}\n"
            f"Source: {source}\n"
            f"{document.page_content}"
        )

    return "\n\n".join(output)


# ============================================================
# 8. CALCULATOR TOOL
# ============================================================

@tool
def calculator(
    a: float,
    b: float,
    operation: str,
) -> str:
    """
    Perform a mathematical calculation.

    Supported operations:
    add
    subtract
    multiply
    divide
    """

    if operation == "add":

        result = a + b

    elif operation == "subtract":

        result = a - b

    elif operation == "multiply":

        result = a * b

    elif operation == "divide":

        if b == 0:

            return (
                "Error: division by zero "
                "is not allowed."
            )

        result = a / b

    else:

        return (
            "Invalid operation. Use add, "
            "subtract, multiply, or divide."
        )

    return str(result)


# ============================================================
# 9. REGISTER TOOLS
# ============================================================

tools = [
    search_knowledge_base,
    calculator,
]


# ============================================================
# 10. BIND TOOLS TO LLM
# ============================================================

llm_with_tools = llm.bind_tools(
    tools
)


# ============================================================
# 11. AGENT NODE
# ============================================================

def agent(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ============================================================
# 12. TOOL NODE
# ============================================================

tool_node = ToolNode(
    tools
)


# ============================================================
# 13. BUILD GRAPH
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
# 14. GRAPH ROUTING
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
# 15. MEMORY / CHECKPOINTING
# ============================================================

memory = InMemorySaver()


app = builder.compile(
    checkpointer=memory
)


# ============================================================
# 16. CONVERSATION CONFIG
# ============================================================

config = {
    "configurable": {
        "thread_id": "user_conversation_1"
    }
}


# ============================================================
# 17. APPLICATION
# ============================================================

print("\n" + "=" * 70)

print(
    "🤖 Day 56 - Agentic RAG Assistant"
)

print("=" * 70)

print("\nAvailable capabilities:")

print("1. Knowledge Base Search")
print("2. Calculator")
print("3. General Conversation")
print("4. Conversation Memory")

print("\nExamples:")

print(
    "- What documents are required for admission?"
)

print(
    "- How can students get a scholarship?"
)

print(
    "- What courses are available in Computer Science?"
)

print(
    "- What is 125 multiplied by 24?"
)

print(
    "- What is LangGraph?"
)

print("\nCommands:")
print("- new  → start a new conversation")
print("- exit → quit")


# ============================================================
# 18. CHAT LOOP
# ============================================================

while True:

    question = input("\nYou: ")

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if question.lower().strip() == "exit":

        print("\nGoodbye!")

        break


    # --------------------------------------------------------
    # NEW CONVERSATION
    # --------------------------------------------------------

    if question.lower().strip() == "new":

        config = {
            "configurable": {
                "thread_id": "user_conversation_2"
            }
        }

        print(
            "\nStarted a new conversation."
        )

        continue


    # --------------------------------------------------------
    # INVOKE GRAPH
    # --------------------------------------------------------

    result = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=question
                )
            ]
        },
        config=config,
    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    final_message = result["messages"][-1]

    print("\nAI:")

    print(
        final_message.content
    )