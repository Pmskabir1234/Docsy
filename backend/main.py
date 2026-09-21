# Docsy - Document Q&A / RAG Assistant
# Copyright (c) 2026 Kabir
# Licensed under the MIT License. See LICENSE file in the project root for full license details.

import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from embed import embed_docs
except ImportError:
    from backend.embed import embed_docs

# Ensure .env is loaded from project root if needed
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))
load_dotenv()

llm = HuggingFaceEndpoint(
    model="Qwen/Qwen3.8-27B",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

RAG_PROMPT = PromptTemplate(
    template="""
    You are a helpful RAG assistant. User question and context from the provided doc is given.
    Answer user's query only with the given context. If you can't find the answer simply reply as
    'Could not find the answer'. The answer should be structured, simple, easy to understand and user-friendly.
    if the topic seems to be difficult you can explain on the basis of context.

    User's query : {query}

    context: {context}""",
    input_variables=['query', 'context']
)

def get_rag_chain():
    """Returns the RAG chain for answering questions based on context."""
    return RAG_PROMPT | model | parser

def ask_question(vector_store, query: str, k: int = 2):
    """Retrieve relevant chunks and generate response using RAG."""
    docs = vector_store.similarity_search(query=query, k=k)
    chain = get_rag_chain()
    response = chain.invoke({"query": query, "context": docs})
    return response, docs

def run_app():
    sample_doc = os.path.join(BASE_DIR, "Fine Tuning Learning Plan.pdf")
    vector_store = embed_docs(sample_doc)
    print("---------Docsy---------\n")
    print(">> Ask anything about document...\n")
    while True: 
        user_ip = input(">> ")
        if user_ip.lower() in {"quit", "exit", "gtfo"}:
            break
        response, _ = ask_question(vector_store, user_ip, k=2)
        print("\n>>Docsy\n", response)
        print("\n")

if __name__ == "__main__":
    run_app()

