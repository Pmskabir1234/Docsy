import os
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

try:
    from doc_splitting import splitting_doc
except ImportError:
    from backend.doc_splitting import splitting_doc

from langchain_community.vectorstores import Chroma

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_DIR = os.path.join(BASE_DIR, "my_chromadb")

embed_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

def embed_docs(doc, persist_directory=DEFAULT_DB_DIR, collection_name="doc_content"):
    chunks = splitting_doc(doc)
    if isinstance(chunks, dict) and "error" in chunks:
        raise ValueError(chunks["error"])

    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embed_model
    )
    vectorstore.add_documents(chunks)

    return vectorstore

# vs = embed_docs(r"Fine Tuning Learning Plan.pdf") 
# print(vs.get(include=['documents','metadatas']))




