from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Config


def build_followup_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    model = ChatGroq(
        model=Config.RAG_MODEL,
        temperature=0.4
    )

    prompt = ChatPromptTemplate.from_template("""
You are an AI interviewer conducting a multi-round interview.

PAST QUESTIONS:
{past_questions}

PAST ANSWERS:
{past_answers}

RETRIEVED CONTEXT:
{context}

LATEST STUDENT ANSWER:
{answer}

ANSWER QUALITY: {quality}

Rules:
- Do NOT repeat previous questions
- If shallow → ask "why/how"
- If adequate → ask implementation detail
- If strong → ask optimization or scaling
- Ask ONLY ONE concise follow-up question
""")

    def retrieve_context(answer: str):
        docs = retriever.invoke(answer)
        return "\n".join(d.page_content for d in docs)

    chain = (
        {
            "context": lambda x: retrieve_context(x["answer"]),
            "answer": lambda x: x["answer"],
            "quality": lambda x: x["quality"],
            "past_questions": lambda x: "\n".join(x["memory"]["questions"]),
            "past_answers": lambda x: "\n".join(x["memory"]["answers"]),
        }
        | prompt
        | model
        | StrOutputParser()
    )

    return chain
