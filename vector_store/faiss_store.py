from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config


def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL
    )
    return FAISS.from_documents(docs, embeddings)
