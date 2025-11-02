# Chat with YouTube

A Streamlit web application that allows you to have a conversation with any YouTube video. Simply provide the video URL, and the app will fetch its transcript, process it, and let you ask questions about its content. This project leverages a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers based on the video's transcript.

## Features

*   **YouTube Video Integration:** Accepts any public YouTube video URL.
*   **Automatic Transcript Fetching:** Downloads the English transcript of the video.
*   **In-Memory Vector Store:** Creates a searchable vector database from the transcript for efficient information retrieval.
*   **Conversational AI:** Uses a powerful Large Language Model (LLM) to answer your questions based on the video's content.
*   **Interactive Chat Interface:** A user-friendly chat UI built with Streamlit.

## How It Works

1.  **URL Input:** The user provides a YouTube video URL in the Streamlit sidebar.
2.  **Transcript Fetching:** The application extracts the video ID and uses the `youtube-transcript-api` library to download the video's transcript ([`get_youtube_transcript`](youtube_utils.py)).
3.  **Text Chunking:** The transcript is split into smaller, manageable chunks using LangChain's `RecursiveCharacterTextSplitter` ([`create_vector_store`](youtube_utils.py)).
4.  **Embedding Generation:** Each chunk is converted into a numerical representation (embedding) using a Hugging Face Sentence Transformer model ([`embedding_model`](youtube_utils.py)).# Chat with YouTube

[**Live Demo**](https://yt-transcriptai.streamlit.app/)

A Streamlit web application that allows you to have a conversation with any YouTube video. Simply provide the video URL, and the app will fetch its transcript, process it, and let you ask questions about its content. This project leverages a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers based on the video's transcript.

## Screenshot

![Chat with YouTube Screenshot](website-ss.png)

## Features

*   **YouTube Video Integration:** Accepts any public YouTube video URL.
// ...existing code...
5.  **Vector Store Creation:** The embeddings are stored in a FAISS vector store, which allows for fast similarity searches ([`create_vector_store`](youtube_utils.py)).
6.  **RAG Chain:** When a user asks a question:
    *   The vector store is used as a **Retriever** to find the most relevant transcript chunks related to the query.
    *   A **Prompt Template** formats the user's question and the retrieved chunks.
    *   The formatted prompt is sent to a **Google Generative AI model** (like Gemini) to generate a final, helpful answer ([`get_rag_chain`](rag_chain.py)).
7.  **Display:** The user's question and the AI's answer are displayed in the chat interface ([`app.py`](app.py)).

## Tech Stack

*   **Frontend:** Streamlit
*   **Orchestration:** LangChain
*   **LLM:** Google Generative AI (e.g., Gemini)
*   **Embeddings:** Hugging Face Sentence Transformers
*   **Vector Store:** FAISS (CPU)
*   **Utilities:** `youtube-transcript-api`, `python-dotenv`

## Setup and Installation

1.  **Clone the repository:**
    ````bash
    git clone <your-repository-url>
    cd YoutubeChatbotRAG
    ````

2.  **Create and activate a virtual environment:**
    ````bash
    python -m venv ytchat
    source ytchat/bin/activate  # On Windows use `ytchat\Scripts\activate`
    ````

3.  **Install dependencies:**
    ````bash
    pip install -r requirements.txt
    ````

4.  **Create a `.env` file:**
    Create a file named `.env` in the root directory of the project and add your API keys and model configurations.

    ````env
    # Get your key from https://aistudio.google.com/
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

    # Recommended embedding model
    HF_EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"

    # Recommended Google model
    GOOGLE_MODEL="gemini-1.5-flash"
    ````

## Usage

1.  **Run the Streamlit application:**
    ````bash
    streamlit run app.py
    ````

2.  **Open your browser:**
    Navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

3.  **Process a video:**
    *   Paste a YouTube video URL into the text box in the sidebar.
    *   Click the "Process Video" button.
    *   Wait for the processing to complete.

4.  **Start chatting:**
    Once the video is processed, you can start asking questions about it in the main chat window.

## File Structure

```
.
├── app.py              # Main Streamlit application UI and logic
├── rag_chain.py        # Defines the RAG chain and LLM configuration
├── youtube_utils.py    # Helper functions for YouTube transcript and vector store
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API keys, model names)
└── README.md           # This file
```