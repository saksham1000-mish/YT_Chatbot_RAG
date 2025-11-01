import os
import re
import streamlit as st
from dotenv import load_dotenv
from youtube_utils import get_youtube_transcript, create_vector_store
from rag_chain import get_rag_chain

load_dotenv()

def get_video_id(url: str) -> str:
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

st.set_page_config(page_title="Chat with YouTube Video", page_icon="▶️")
st.title("▶️ Chat with any YouTube Video")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Video Processing")
    youtube_url = st.text_input("Enter YouTube Video URL:", key="youtube_url")
    
    if st.button("Process Video", key="process_button"):
        if not youtube_url:
            st.warning("Please enter a YouTube URL.")
        else:
            video_id = get_video_id(youtube_url)
            
            if not video_id:
                st.error("Invalid YouTube URL. Please try again.")
            else:
                with st.spinner("Processing video... This may take a moment."):
                    try:
                        # 1. Get Transcript
                        transcript = get_youtube_transcript(video_id)
                        if not transcript:
                            st.error("Could not fetch transcript. The video might not have one.")
                            st.stop()
                        
                        # 2. Create Vector Store
                        st.session_state.vector_store = create_vector_store(transcript)
                        if st.session_state.vector_store is None:
                            st.error("Failed to create vector store.")
                            st.stop()

                        # 3. Reset chat history for the new video
                        st.session_state.chat_history = [
                            {"role": "ai", "content": "Video processed! Ask me anything about it."}
                        ]
                        st.success("Video processed successfully!")
                        # Force a rerun to update the main chat interface
                        st.rerun()

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask a question about the video..."):
    
    # Check if a video has been processed
    if st.session_state.vector_store is None:
        st.warning("Please process a YouTube video first using the sidebar.")
    else:
        # Add user's message to history and display it
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                # 1. Create the RAG chain
                rag_chain = get_rag_chain(st.session_state.vector_store)
                
                # 2. Invoke the chain to get an answer
                # The chain automatically handles retrieval, prompting, and LLM call
                response = rag_chain.invoke({"input": user_query})
                answer = response.get("answer", "Sorry, I couldn't generate a response.")
                
                # Add AI's answer to history and display it
                st.session_state.chat_history.append({"role": "ai", "content": answer})
                with st.chat_message("ai"):
                    st.markdown(answer)
                    
            except Exception as e:
                st.error(f"An error occurred while generating the response: {e}")


