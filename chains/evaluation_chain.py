from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Config


def build_evaluation_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    model = ChatGroq(
        model=Config.RAG_MODEL,
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template("""
Evaluate the student's answer using ONLY the context.

CONTEXT:
{context}

STUDENT ANSWER:
{answer}

Score from 0–5 on:
- Technical Depth
- Clarity
- Originality
- Understanding

Give short feedback.
""")

    def retrieve_context(answer: str):
        docs = retriever.invoke(answer)
        return "\n".join(d.page_content for d in docs)

    chain = (
        {
            "context": lambda x: retrieve_context(x["answer"]),
            "answer": lambda x: x["answer"]
        }
        | prompt
        | model
        | StrOutputParser()
    )

    return chain
