from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Config


def build_interview_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    model = ChatGroq(
        model=Config.RAG_MODEL,
        temperature=0.4
    )

    prompt = ChatPromptTemplate.from_template("""
You are an AI interviewer.

Use ONLY the following retrieved project context to ask questions.

CONTEXT:
{context}

Ask:
1. One core technical question
2. One implementation-level question
3. One design trade-off question
""")

    def retrieve_context(_):
        docs = retriever.invoke("project presentation")
        return "\n".join(d.page_content for d in docs)

    chain = (
        {
            "context": retrieve_context
        }
        | prompt
        | model
        | StrOutputParser()
    )

    return chain
