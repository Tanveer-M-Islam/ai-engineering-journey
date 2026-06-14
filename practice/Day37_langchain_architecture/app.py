from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_ollama import (
    ChatOllama
)


model = ChatOllama(
    model="llama3.2"
)


prompt = ChatPromptTemplate.from_template(

    """
    Explain the following topic in simple words.

    Topic:
    {topic}
    """
)


parser = StrOutputParser()


chain = (

    prompt

    |

    model

    |

    parser
)


while True:

    topic = input(
        "\nTopic: "
    )

    if topic.lower() == "exit":

        break

    response = chain.invoke(

        {
            "topic": topic
        }
    )

    print(
        "\nAnswer:\n"
    )

    print(
        response
    )