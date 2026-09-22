try:
    from doc_loading import load_document_content
except ImportError:
    from backend.doc_loading import load_document_content

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_classic.text_splitter import RecursiveCharacterTextSplitter


def splitting_doc(doc):
    """splitting loaded document content into smaller chunks"""
    if isinstance(doc, list):
        content = doc
    else:
        content = load_document_content(doc)

    if isinstance(content, dict):
        return content if "error" in content else {"error": "unsupported file format or empty content"}
    if not content:
        return {"error": "unsupported file format or empty content"}

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=75
    )
    chunks = splitter.split_documents(content)
    return chunks



# a = splitting_doc(r"Fine Tuning Learning Plan.pdf")

# for chunks in a:
#     print(chunks)
#     print("\n")
#     print("-"*100)

# print(type(a))



