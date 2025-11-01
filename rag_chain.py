import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from youtube_utils import get_youtube_transcript

load_dotenv()


embedding_model = HuggingFaceEmbeddings(
    model_name = os.getenv("HF_EMBEDDING_MODEL")
)

llm = ChatGoogleGenerativeAI(
        model = os.getenv("GOOGLE_MODEL"),
        temperature = 0.4
    )


def text_splitter(transcript):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
        )
    chunks = splitter.create_documents([transcript])
    return chunks

def vector_store(chunks):

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )
    return vectorstore


transcript = get_youtube_transcript("dQw4w9WgXcQ")
chunks = text_splitter(transcript)
vectorstore = vector_store(chunks)
print(vectorstore.index_to_docstore_id)


    

