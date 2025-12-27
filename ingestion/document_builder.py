from langchain_core.documents import Document

def build_documents(screen_text: str, speech_text: str):
    docs = []

    if screen_text.strip():
        docs.append(
            Document(
                page_content=screen_text,
                metadata={"source": "screen"}
            )
        )

    if speech_text.strip():
        docs.append(
            Document(
                page_content=speech_text,
                metadata={"source": "speech"}
            )
        )

    return docs
