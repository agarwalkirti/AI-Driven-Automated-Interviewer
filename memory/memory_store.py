class InterviewMemory:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "questions": [],
                "answers": [],
                "qualities": [],
                "followups": []
            }
        return self.sessions[session_id]

    def add_round(
        self,
        session_id: str,
        question: str,
        answer: str,
        quality: str,
        followup: str = None
    ):
        session = self.get_session(session_id)
        session["questions"].append(question)
        session["answers"].append(answer)
        session["qualities"].append(quality)
        if followup:
            session["followups"].append(followup)
