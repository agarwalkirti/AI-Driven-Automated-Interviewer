INTERVIEW_PROMPT = """
You are an AI interviewer.

Based on the following project content:
{context}

Ask:
1. One core technical question
2. One implementation-level question
3. One design trade-off question
"""

EVALUATION_PROMPT = """
Evaluate the student's answer.

Context:
{context}

Answer:
{answer}

Score from 0–5 on:
- Technical Depth
- Clarity
- Originality
- Understanding

Give short feedback.
"""
