# Docsy

Docsy is a retrieval-augmented generation (RAG) knowledge assistant for interacting with documents and web content through natural-language queries.

The system combines document ingestion, recursive text chunking, dense embeddings, vector similarity search, and LLM-based response generation into a single Streamlit application.

I built Docsy to understand and implement the complete RAG pipeline, from raw source ingestion to grounded answer generation.

## Overview

Docsy follows a standard RAG workflow:

1. A document or web URL is provided as the knowledge source.
2. The source is loaded and converted into LangChain documents.
3. The extracted content is split into smaller overlapping chunks.
4. Each chunk is converted into a dense vector using `BAAI/bge-small-en-v1.5`.
5. The embeddings are stored in Chroma.
6. A user query is converted into a semantic retrieval request.
7. The most relevant chunks are retrieved using vector similarity search.
8. The retrieved context is passed to a constrained RAG prompt.
9. `Qwen/Qwen3.8-27B` generates the final response through Hugging Face.
10. Retrieved context and execution steps can be inspected directly from the interface.

## Core Features

- Multi-format document ingestion
- Web URL ingestion
- PDF, DOCX, PPTX, TXT, CSV, and Markdown support
- Recursive document chunking
- Dense semantic embeddings
- Persistent Chroma vector storage
- Configurable top-k similarity retrieval
- Context-grounded LLM generation
- Streamlit-based conversational interface
- Retrieved context inspection
- Retrieval pipeline visualization
- Streaming response generation
- Fallback response generation
- Session-based conversation state

## UI Quick View

<img width="1919" height="990" alt="Screenshot 2026-09-20 235851" src="https://github.com/user-attachments/assets/e60054d7-6890-45a6-96f0-f9a3e0414f89" />


## Architecture

The architecture separates the user interface from the document-processing and retrieval pipeline.


<img width="1908" height="846" alt="Screenshot 2026-09-21 001210" src="https://github.com/user-attachments/assets/40f26326-5840-45de-914e-ce02e504a609" />


## Directory Structure

```text
Docsy/
├── Frontend/
│   └── app.py
│
├── backend/
│   ├── main.py
│   ├── doc_loading.py
│   ├── doc_splitting.py
│   ├── embed.py
│  
├── requirements.txt
└── .gitignore
```

### `Frontend/app.py`

The Streamlit application layer responsible for:

- Document upload
- Web URL input
- Knowledge indexing
- Retrieval configuration
- Chat interaction
- Session state
- Retrieval status
- Execution pipeline logs
- Retrieved context display
- Response streaming
- Application styling

### `backend/doc_loading.py`

Handles source ingestion and converts supported inputs into LangChain document objects.

Supported sources include:

- PDF
- DOCX
- PPTX
- TXT
- HTTP/HTTPS web pages

The appropriate loader is selected based on the file extension or URL scheme.

### `backend/doc_splitting.py`

Splits loaded documents into smaller retrieval units using `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk size:     900
Chunk overlap:   75
```

The module also handles unsupported or empty input.

### `backend/embed.py`

Responsible for generating embeddings and populating the Chroma vector store.

Embedding model:

```text
BAAI/bge-small-en-v1.5
```

Default Chroma persistence directory:

```text
backend/my_chromadb/
```

### `backend/main.py`

Contains the core RAG orchestration logic:

- Hugging Face model configuration
- LLM initialization
- RAG prompt definition
- RAG chain construction
- Similarity retrieval
- Question answering
- Command-line testing interface

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | Streamlit | Interactive ingestion and chat interface |
| RAG Framework | LangChain | Document, retrieval, prompt, and model orchestration |
| LLM Integration | LangChain Hugging Face | Hugging Face model integration |
| LLM | Qwen/Qwen3.8-27B | Grounded response generation |
| Embeddings | BAAI/bge-small-en-v1.5 | Dense semantic embeddings |
| Vector Database | Chroma | Vector storage and similarity retrieval |
| PDF Processing | PyMuPDF / PyPDFLoader | PDF document loading |
| Office Documents | Unstructured | DOCX/PPTX ingestion |
| Web Ingestion | WebBaseLoader | Web page loading |
| Data Handling | Pandas / CSVLoader | CSV-oriented ingestion |
| Configuration | python-dotenv | Environment variable management |
| ML Runtime | PyTorch / torchvision | Supporting ML dependencies |

## RAG Pipeline

```text
Source
  |
  v
Document Loader
  |
  v
Loaded Documents
  |
  v
Recursive Character Splitter
  |
  v
Document Chunks
  |
  v
BGE Embeddings
  |
  v
Chroma Vector Store
  |
  v
User Query
  |
  v
Similarity Search
  |
  v
Top-k Relevant Chunks
  |
  v
Grounded Prompt
  |
  v
Qwen3.8-27B
  |
  v
Final Answer
```

## Grounding Strategy

The generation prompt is explicitly constrained to the retrieved context.

The model is instructed to:

- Answer using the supplied context.
- Keep responses structured and user-friendly.
- Explain complex topics using the available context.
- Return `Could not find the answer` when the required information cannot be found in the retrieved context.

This provides a clear separation between **retrieval** and **generation** and reduces reliance on unrestricted model knowledge.

## Retrieval Configuration

The number of retrieved passages can be configured directly from the Streamlit interface.

```text
Minimum k: 1
Maximum k: 6
Default k: 2
```

The selected value determines how many semantically relevant chunks are retrieved from Chroma for each query.

## Environment Setup

Environment variables are loaded using `python-dotenv`.

Create a `.env` file in the project root and provide the credentials required by the Hugging Face integration.

```text
HF_TOKEN=your_huggingface_token
```

Secrets should never be committed to the repository.

## Installation

Clone the repository:

```bash
git clone https://github.com/Pmskabir1234/Docsy.git
cd Docsy
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run Frontend/app.py
```

The Streamlit interface will then be available at the local URL provided by the terminal.

## Using Docsy

The typical workflow is:

1. Start the Streamlit application.
2. Select either **Document Upload** or **Web URL**.
3. Provide the desired knowledge source.
4. Click **Index Knowledge**.
5. The source is loaded and split into chunks.
6. Embeddings are generated and stored in Chroma.
7. Enter a question in the chat interface.
8. Docsy retrieves the most relevant context.
9. The retrieved context is passed to the RAG chain.
10. The LLM generates a grounded response.
11. Retrieved passages can be expanded and inspected from the interface.

## Command-Line Testing

A basic CLI execution path is also available through `backend/main.py`.

The current implementation uses:

```text
backend/Fine Tuning Learning Plan.pdf
```

as the sample document.

Run it with:

```bash
python backend/main.py
```

Questions can then be entered directly through the terminal.

## Design Decisions

### Why RAG?

I use RAG because Docsy needs to answer questions about external and user-provided sources rather than relying exclusively on the knowledge encoded in the LLM.

Retrieval provides the model with explicit source context before generation.

### Why Dense Embeddings?

Dense embeddings allow semantic similarity search, making it possible to retrieve relevant content even when the query and source use different wording.

### Why Chunk Overlap?

A 75-character overlap is used between chunks to reduce the possibility of losing contextual information at chunk boundaries.

### Why Expose Retrieved Context?

Retrieved passages are displayed in the interface to make the retrieval stage inspectable.

This helps identify whether an incorrect answer originates from:

- Poor retrieval
- Insufficient context
- Prompt construction
- LLM generation

## Current Limitations

The current implementation focuses on the core RAG workflow. Several production-oriented capabilities are not yet implemented:

- No authentication or authorization layer
- No multi-user document isolation
- No dedicated document-management service
- No retrieval reranking
- No hybrid keyword + vector retrieval
- No automated retrieval evaluation
- No automated answer-faithfulness evaluation
- No dedicated production API layer
- No background document-processing queue
- No dedicated observability or tracing system
- Vector-store lifecycle is currently handled within the application
- Learning/project artifacts are currently stored alongside application code

## Future Improvements

The planned evolution of Docsy includes:

- Dedicated FastAPI backend
- Authentication and authorization
- Per-user document collections
- Document lifecycle management
- Metadata-aware retrieval
- Hybrid search
- Cross-encoder reranking
- RAG evaluation
- Citation-aware answers
- Background ingestion workers
- Queue-based processing
- Improved vector-store management
- Observability and distributed tracing
- Docker-based deployment
- CI/CD pipeline
- Production-grade configuration management

## Important Implementation Details

- LangChain's document abstraction is used throughout the ingestion pipeline.
- Both local document paths and HTTP/HTTPS URLs are supported at the loader level.
- Chroma is configured with persistent storage.
- The same embedding model is used during indexing and retrieval.
- Context retrieval occurs before the LLM generation step.
- Top-k retrieval is configurable from the frontend.
- Streamlit session state maintains the active vector store and conversation history.
- Response streaming has a fallback path that uses normal chain invocation if streaming fails.
- The RAG prompt explicitly restricts responses to retrieved context.
- Temporary uploaded files are removed after ingestion where possible.

## Project Status

Docsy is currently a functional RAG prototype and learning-oriented implementation.

The core pipeline is implemented:

```text
Document/Web Source
        ↓
Document Loading
        ↓
Chunking
        ↓
Embedding
        ↓
Vector Storage
        ↓
Similarity Retrieval
        ↓
Context-Grounded Generation
        ↓
Answer
```

The next stage is to evolve the prototype toward a production-oriented architecture with stronger retrieval, evaluation, scalability, security, and observability.

## License

MIT License

## Author

I built Docsy as a practical implementation of a document-grounded RAG system, focusing on understanding the complete pipeline from source ingestion to semantic retrieval and LLM-based answer generation.
