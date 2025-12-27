from fastapi import FastAPI
from pydantic import BaseModel

from ingestion.document_builder import build_documents
from vector_store.faiss_store import create_vector_store
from chains.interview_chain import build_interview_chain
from chains.evaluation_chain import build_evaluation_chain
from chains.followup_chain import build_followup_chain
from chains.answer_classifier import classify_answer
from memory.memory_store import InterviewMemory

app = FastAPI()

memory_store = InterviewMemory()

vectorstore = None
interview_chain = None
evaluation_chain = None
followup_chain = None


# Request Models
class IngestRequest(BaseModel):
    screen_text: str = ""
    speech_text: str = ""

class AnswerRequest(BaseModel):
    answer: str

class FollowupRequest(BaseModel):
    session_id: str
    question: str
    answer: str


# Endpoints
@app.post("/ingest")
def ingest(payload: IngestRequest):
    global vectorstore, interview_chain, evaluation_chain, followup_chain

    docs = build_documents(payload.screen_text, payload.speech_text)

    if not docs:
        return {"error": "No content provided. Please paste project text before ingestion."}

    vectorstore = create_vector_store(docs)

    interview_chain = build_interview_chain(vectorstore)
    evaluation_chain = build_evaluation_chain(vectorstore)
    followup_chain = build_followup_chain(vectorstore)

    print(f"Ingested {len(docs)} documents")
    return {"status": "Context ingested"}


@app.post("/interview")
def interview():
    if interview_chain is None:
        return {"error": "Context not ingested yet"}

    question = interview_chain.invoke({})
    return {"question": str(question)}


@app.post("/evaluate")
def evaluate(payload: AnswerRequest):
    return evaluation_chain.invoke({"answer": payload.answer})


@app.post("/followup")
def followup(payload: FollowupRequest):
    session_memory = memory_store.get_session(payload.session_id)

    quality = classify_answer(payload.answer)

    followup_question = followup_chain.invoke({
        "answer": payload.answer,
        "quality": quality,
        "memory": session_memory
    })

    memory_store.add_round(
        session_id=payload.session_id,
        question=payload.question,
        answer=payload.answer,
        quality=quality,
        followup=followup_question
    )

    return {
        "answer_quality": quality,
        "followup_question": followup_question,
        "rounds_completed": len(session_memory["questions"])
    }
