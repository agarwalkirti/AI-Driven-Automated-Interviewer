import streamlit as st
import requests

st.title("RAG-based AI Interviewer")


# Session State
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "session_id" not in st.session_state:
    st.session_state.session_id = "demo-session"


# Ingestion
screen_text = st.text_area("Enter screen / code text (screenshare output in text)")
speech_text = st.text_area("Enter speech text (STT output in text)")

if st.button("Ingest Presentation"):
    if not screen_text.strip() and not speech_text.strip():
        st.error("Please paste project content before ingestion.")
    else:
        res = requests.post(
            "http://localhost:8000/ingest",
            json={
                "screen_text": screen_text,
                "speech_text": speech_text
            }
        )

        try:
            data = res.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.success("Context ingested successfully")
        except Exception:
            st.error("Backend error during ingestion")
            st.text(res.text)

 
# Interview Question
if st.button("Generate Interview Question"):
    res = requests.post("http://localhost:8000/interview")

    try:
        data = res.json()
        if "question" in data:
            st.session_state.current_question = data["question"]
            st.write("Interviewer:", data["question"])
        else:
            st.error(data.get("error", "Unknown backend error"))
    except Exception:
        st.error("Backend did not return JSON")
        st.text(res.text)

 
# Student Answer
answer = st.text_area("Student Answer")

 
# Evaluation
if st.button("Evaluate Answer"):
    res = requests.post(
        "http://localhost:8000/evaluate",
        json={"answer": answer}
    )
    st.write(res.text)

 
# Follow-up
st.session_state.session_id = st.text_input(
    "Session ID",
    value=st.session_state.session_id
)

if st.button("Get Follow-up Question"):
    res = requests.post(
        "http://localhost:8000/followup",
        json={
            "session_id": st.session_state.session_id,
            "question": st.session_state.current_question,
            "answer": answer
        }
    )

    try:
        data = res.json()
        followup = data["followup_question"]
        st.session_state.current_question = followup
        st.write("Follow-up:", followup)
    except Exception:
        st.error("Backend error during follow-up")
        st.text(res.text)
