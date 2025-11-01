import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()


llm = ChatGoogleGenerativeAI(
        model = os.getenv("GOOGLE_MODEL"),
        temperature = 0.4
    )

def get_rag_chain(vector_store):
 
    template = """You are a helpful AI assistant that helps people find information about YouTube videos based on their transcripts. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. 

    {context}

    Question: {input}
    Helpful Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    stuff_documents_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )
    
    retrieval_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=stuff_documents_chain
    )
    

    return retrieval_chain




    

