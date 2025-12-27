Challenge Statement:
Challenge 1: AI-Driven Automated Interviewer

Objective:
Build an AI system that listens to a student presenting a project (screen share + speech) and conducts an adaptive interview based on the presentation content and student responses.

Overview
RAG-Based AI Interviewer for Project Presentations. This project implements an AI-driven automated interviewer that evaluates students while they present technical projects.
The system listens to a student’s screen content (code, slides, diagrams) and speech explanation, understands the project context, and conducts a multi-round, adaptive technical interview.

The interviewer:
Generates context-aware technical questions
Asks intelligent follow-up questions
Evaluates answers across multiple dimensions
Maintains interview memory to ensure progressive difficulty
Produces structured scores and feedback

Functional Requirements:
Presentation Understanding
Extract content from screens using OCR
Transcribe student speech using STT
Analyze:
Code snippets
Slides
UI elements
Diagrams

Dynamic Interviewing
Generate context-aware interview questions

Ask adaptive follow-up questions based on:
Student responses
Previously covered topics

Interview memory
Evaluation & Feedback

Score students on:
Technical depth
Clarity of explanation
Originality
Understanding of implementation

Deliverable:
A live demo where: 
A student presents a project
The system interviews them in real time
The system generates:
Scores
Qualitative feedback
Progressive follow-up questions

High-Level Architecture:
Student Presentation
   ├── Screen (Image / Code / Slides)
   ├── Speech (Audio or Text)
   ↓
Content Extraction Layer
   ├── OCR (screen → text)
   ├── STT (audio → text)
   ↓
Understanding Layer
   ├── Content Chunking & Embeddings
   ├── Topic & Skill Detection
   ↓
Interview Engine (LLM + RAG)
   ├── Question Generation
   ├── Follow-up Logic
   ↓
Evaluation Engine
   ├── Technical Depth
   ├── Clarity
   ├── Originality
   ├── Understanding
   ↓
Score + Feedback Report

Tech Stack:
Component	   Technology
Backend	      Python + FastAPI
LLM	         Groq (LLaMA 3.1)
Embeddings	   HuggingFace (BGE)
Vector Store	FAISS
OCR	         pytesseract
STT	         OpenAI Whisper
UI	            Streamlit
Evaluation	   Prompt-based LLM scoring

Project Structure:
ai_interviewer/
│
├── app.py                     # FastAPI backend (API entry point)
│
├── ingestion/
│   ├── document_builder.py    # OCR + STT → LangChain Documents
│   ├── ocr.py                 # Screen → text
│   └── stt.py                 # Audio → text
│
├── vector_store/
│   └── faiss_store.py         # Embeddings + FAISS index
│
├── chains/
│   ├── interview_chain.py     # Initial RAG-based interview questions
│   ├── followup_chain.py      # Adaptive follow-up questions
│   ├── evaluation_chain.py    # RAG-based scoring & feedback
│   └── answer_classifier.py   # Shallow / Adequate / Strong
│
├── memory/
│   └── memory_store.py        # Multi-round interview memory
│
├── prompts/
│   └── prompts.py             # Centralized prompt templates
│
├── ui/
│   └── ui.py                  # Streamlit UI
│
├── config.py                  # Model names, API keys
├── requirements.txt
└── README.md

Folder Responsibilities:
ingestion-
Converts raw presentation artifacts into text
Combines OCR + STT output into unified documents

vector_store-
Embeds presentation content
Enables semantic similarity search using FAISS

chains-
Core reasoning logic:
Interview question generation
Follow-up logic
Evaluation & scoring
Answer quality classification

memory-
Maintains interview state:
Questions asked
Answers given
Difficulty progression
Follow-ups generated

prompts-
Centralized prompt definitions
Easy prompt tuning and explainability

ui-
Interactive Streamlit demo
Controls ingestion, interview flow, and follow-ups

End-to-End RAG Flow:
Presentation Content (OCR + STT)
        ↓
Chunking + Embeddings
        ↓
Vector Store (FAISS)
        ↓
Retriever
        ↓
Interview Question Generator (LLM)
        ↓
Follow-up + Evaluation (LLM + Retrieved Context)

Full Interview Loop:
Ingest presentation (OCR + STT)
Generate initial interview questions
Student answers

System:
Classifies answer quality
Retrieves relevant context
Generates adaptive follow-up
Repeat for 2–3 rounds
Produce final evaluation + feedback

Memory Design:
Each interview session stores:
Session ID
 ├── Presentation context
 ├── Asked questions
 ├── Student answers
 ├── Follow-up questions
 └── Answer quality history


Memory is used to:
Avoid repeated questions
Increase difficulty progressively
Enable human-like interview flow

How to Run the Project:
Start Backend (FastAPI):
uvicorn app:app --reload
Stop server:CTRL + C

Start UI (Streamlit):
streamlit run ui/ui.py

Demo Flow in UI:
Paste presentation text
Click Ingest Presentation
Click Generate Interview Question
Enter student answer
Click Get Follow-up Question

Final Notes:
This system is RAG-grounded, minimizing hallucinations
Fully modular and extensible

Suitable for:
AI learning platforms
Technical screenings
Project evaluations

One-Line Summary:
An AI-powered interviewer that understands project presentations and conducts adaptive, explainable technical interviews using Retrieval-Augmented Generation.
