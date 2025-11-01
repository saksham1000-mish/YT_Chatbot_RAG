from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()


embedding_model = HuggingFaceEmbeddings(
        model_name=os.getenv("HF_EMBEDDING_MODEL")
    )

def get_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en'], preserve_formatting=True)
        return " ".join(snippet.text for snippet in transcript_list)
    except TranscriptsDisabled:
        return "Transcript is disabled for this video."



def create_vector_store(transcript: str):
    
    # 2. Split the transcript into chunks (from your text_splitter)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.create_documents([transcript])
    
    if not chunks:
        return None
    
    print(f"Creating vector store with {len(chunks)} chunks...")
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )
    print("Vector store created successfully.")
    return vectorstore