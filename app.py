import os
import re
import streamlit as st
from dotenv import load_dotenv
from youtube_utils import get_youtube_transcript, create_vector_store
from rag_chain import get_rag_chain
from PIL import Image

load_dotenv()

def get_video_id(url: str) -> str:
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

logo = "assets/logo.jpg"
removed_bg = "assets/logo-removebg.png"

try:
    logo_image = Image.open(removed_bg)
    st.set_page_config(
        page_title="YT Transcript AI",
        page_icon=logo_image
    )
except FileNotFoundError:
    st.set_page_config(
        page_title="Chat with YouTube",
        page_icon="▶️"
    )
st.image(removed_bg, width=100)
st.title("Chat with any YouTube Video")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.image(removed_bg, width=200)
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
                        transcript = get_youtube_transcript(video_id)
                        if not transcript:
                            st.error("Could not fetch transcript. The video might not have one.")
                            st.stop()
                        
                        st.session_state.vector_store = create_vector_store(transcript)
                        if st.session_state.vector_store is None:
                            st.error("Failed to create vector store.")
                            st.stop()

                        st.session_state.chat_history = [
                            {"role": "ai", "content": "Video processed! Ask me anything about it."}
                        ]
                        st.success("Video processed successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask a question about the video..."):
    
    if st.session_state.vector_store is None:
        st.warning("Please process a YouTube video first using the sidebar.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.spinner("Thinking..."):
            try:
                rag_chain = get_rag_chain(st.session_state.vector_store)
                
                response = rag_chain.invoke({"input": user_query})
                answer = response.get("answer", "Sorry, I couldn't generate a response.")
                
                st.session_state.chat_history.append({"role": "ai", "content": answer})
                with st.chat_message("ai"):
                    st.markdown(answer)
                    
            except Exception as e:
                st.error(f"An error occurred while generating the response: {e}")


