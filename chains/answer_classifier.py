from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Config


def classify_answer(answer: str) -> str:
    model = ChatGroq(
        model=Config.RAG_MODEL,
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
Classify the following answer as one of:
- shallow
- adequate
- strong

Answer:
{answer}

Return ONLY one word.
""")

    chain = prompt | model | StrOutputParser()
    return chain.invoke({"answer": answer}).strip().lower()
