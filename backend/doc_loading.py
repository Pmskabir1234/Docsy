from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    WebBaseLoader,
    TextLoader,
    CSVLoader
)

try:
    from yt_transcript import YoutubeTranscript
except ImportError:
    from backend.yt_transcript import YoutubeTranscript

load_dotenv()

def load_document_content(name: str):
    """loading user given document content (file path or URL)"""
    if not isinstance(name, str):
        return {}
    
    clean_name = name.strip()
    lower_name = clean_name.lower()
    if "youtube.com" in lower_name or "youtu.be" in lower_name:
        transcript = YoutubeTranscript()
        docs = transcript.get_transcript(clean_name)
        return docs
    elif lower_name.startswith("http://") or lower_name.startswith("https://"):
        loader = WebBaseLoader(clean_name)
        docs = loader.load()
    elif lower_name.endswith(".pdf"):
        loader = PyPDFLoader(clean_name)
        docs = loader.load()
    elif lower_name.endswith(".pptx") or lower_name.endswith(".ppt"):
        loader = UnstructuredPowerPointLoader(clean_name)
        docs = loader.load()
    elif lower_name.endswith(".docx") or lower_name.endswith(".doc"):
        loader = UnstructuredWordDocumentLoader(clean_name)
        docs = loader.load()
    elif lower_name.endswith(".txt") or lower_name.endswith(".md"):
        loader = TextLoader(clean_name, encoding="utf-8")
        docs = loader.load()
    elif lower_name.endswith(".csv"):
        loader = CSVLoader(clean_name)
        docs = loader.load()
    else:
        return {}

    return docs









