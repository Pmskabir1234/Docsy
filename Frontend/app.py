import os
import sys
import tempfile
import time
import streamlit as st

# Add project root directory to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.embed import embed_docs
from backend.main import ask_question, get_rag_chain

# Page Configuration (No emojis)
st.set_page_config(
    page_title="Docsy | RAG powered knowledge assistant",
    page_icon="▫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography & Resets */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        letter-spacing: -0.02em;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* Top Navigation / Brand Banner */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
    }

    .brand-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .brand-logo-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
        color: #ffffff;
    }

    .brand-title {
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }

    .brand-tagline {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 0;
        font-weight: 500;
    }

    .brand-meta {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .status-pill.ready {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.25);
        color: #34D399;
    }

    .status-pill.idle {
        background: rgba(148, 163, 184, 0.1);
        border-color: rgba(148, 163, 184, 0.2);
        color: #94A3B8;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
    }

    .status-dot.ready {
        background: #10B981;
        box-shadow: 0 0 10px #10B981;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    .status-dot.idle {
        background: #64748B;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.15); }
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #0B0F17;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .sidebar-section-header {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin-bottom: 0.75rem;
    }

    .sidebar-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.25rem;
    }

    .doc-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.65rem 0.85rem;
        background: rgba(79, 70, 229, 0.08);
        border: 1px solid rgba(79, 70, 229, 0.25);
        border-radius: 8px;
        color: #A5B4FC;
        font-size: 0.82rem;
        font-weight: 500;
        word-break: break-all;
    }

    /* Welcome / Hero Empty State */
    .hero-card {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }

    .hero-description {
        font-size: 0.95rem;
        color: #94A3B8;
        max-width: 600px;
        margin: 0 auto 1.75rem auto;
        line-height: 1.6;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .feature-item {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: left;
    }

    .feature-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #818CF8;
        margin-bottom: 0.25rem;
    }

    .feature-desc {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 0;
    }

    /* Chat Messages & Cards */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
    }

    /* Intermediate Step Logs */
    .step-timeline {
        border-left: 2px solid rgba(99, 102, 241, 0.3);
        padding-left: 1rem;
        margin: 0.75rem 0;
    }

    .step-item {
        font-size: 0.83rem;
        color: #CBD5E1;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .step-item-tag {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        white-space: nowrap;
    }

    /* Context Source Snippet Cards */
    .source-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-top: 0.75rem;
    }

    .source-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }

    .source-tag {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }

    .source-meta {
        font-size: 0.75rem;
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Buttons & Form Elements */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: -0.01em;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
    }

    /* Prompt Suggestion Chips */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    /* Streamlit Expander Polishing */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        background-color: transparent !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "current_doc_name" not in st.session_state:
    st.session_state.current_doc_name = None

if "current_source_type" not in st.session_state:
    st.session_state.current_source_type = None

# Sidebar Ingestion System
with st.sidebar:
    # Sidebar Header
    st.markdown('<div class="sidebar-section-header">Knowledge Ingestion</div>', unsafe_allow_html=True)

    input_mode = st.radio(
        "Select Source Type",
        options=["Document Upload", "Web URL","YT video URL"],
        index=0,
        label_visibility="collapsed"
    )

    uploaded_file = None
    url_input = ""
    vid_url = ""

    if input_mode == "Document Upload":
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "docx", "pptx", "txt", "csv", "md"],
            help="Supported formats: PDF, DOCX, PPTX, TXT, MD, CSV",
            label_visibility="collapsed"
        )
    elif input_mode == "Web URL":
        url_input = st.text_input(
            "Paste Web Page URL",
            placeholder="https://example.com/docs",
            help="Provide any accessible HTTP or HTTPS URL",
            label_visibility="collapsed"
        )
    else:
        vid_url = st.text_input(
            "Enter YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Provide a public YouTube video link",
            label_visibility="collapsed"
        )

    # Retrieval Configuration Card
    st.markdown('<div class="sidebar-section-header" style="margin-top: 1.5rem;">Retrieval Parameters</div>', unsafe_allow_html=True)
    k_chunks = st.slider(
        "Top-k Context Passages",
        min_value=1,
        max_value=6,
        value=2,
        help="Number of semantically relevant context chunks retrieved from vector storage for each query."
    )

    # Action Controls
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        process_btn = st.button("Index Knowledge", use_container_width=True, type="primary")
    with col2:
        clear_btn = st.button("Reset State", use_container_width=True)

    if clear_btn:
        st.session_state.messages = []
        st.session_state.vector_store = None
        st.session_state.current_doc_name = None
        st.session_state.current_source_type = None
        st.rerun()

    if process_btn:
        if input_mode == "Document Upload" and uploaded_file is not None:
            try:
                with st.status(f"Ingesting '{uploaded_file.name}'...", expanded=True) as status:
                    status.write("Reading binary stream and staging temporary file...")
                    file_suffix = os.path.splitext(uploaded_file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        tmp_path = tmp_file.name

                    status.write("Segmenting document into semantic partitions...")
                    status.write("Computing vector embeddings via BAAI/bge-small-en-v1.5...")
                    vectorstore = embed_docs(tmp_path)
                    st.session_state.vector_store = vectorstore
                    st.session_state.current_doc_name = uploaded_file.name
                    st.session_state.current_source_type = "Document"
                    st.session_state.messages = []

                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass

                    status.update(label=f"Ingestion complete: '{uploaded_file.name}'", state="complete", expanded=False)
                st.rerun()
            except Exception as e:
                st.error(f"Ingestion failed: {str(e)}")

        elif input_mode == "Web URL" and url_input.strip():
            target_url = url_input.strip()
            if not target_url.startswith(("http://", "https://")):
                st.error("Please provide a valid URL beginning with http:// or https://")
            else:
                try:
                    with st.status("Fetching and parsing target URL...", expanded=True) as status:
                        status.write(f"Scraping content from {target_url}...")
                        status.write("Segmenting text chunks and computing embeddings...")
                        vectorstore = embed_docs(target_url)
                        st.session_state.vector_store = vectorstore
                        st.session_state.current_doc_name = target_url
                        st.session_state.current_source_type = "Web URL"
                        st.session_state.messages = []
                        status.update(label="URL parsed and indexed successfully", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    st.error(f"URL parsing failed: {str(e)}")

        elif input_mode == "YT video URL" and vid_url.strip():
            target_vid = vid_url.strip()
            if not ("youtube.com" in target_vid.lower() or "youtu.be" in target_vid.lower()):
                st.error("Please provide a valid YouTube video URL (e.g. https://www.youtube.com/watch?v=...)")
            else:
                try:
                    with st.status("Fetching and parsing YouTube transcript...", expanded=True) as status:
                        status.write(f"Extracting transcript from {target_vid}...")
                        status.write("Segmenting transcript chunks and computing embeddings...")
                        vectorstore = embed_docs(target_vid)
                        st.session_state.vector_store = vectorstore
                        st.session_state.current_doc_name = target_vid
                        st.session_state.current_source_type = "YouTube Video"
                        st.session_state.messages = []
                        status.update(label="YouTube transcript indexed successfully", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    st.error(f"Transcript indexing failed: {str(e)}")
        else:
            st.warning("Please provide a document or valid URL before indexing.")

    # Status Monitor in Sidebar
    st.markdown('<div class="sidebar-section-header" style="margin-top: 2rem;">Knowledge Index Status</div>', unsafe_allow_html=True)
    if st.session_state.vector_store is not None:
        source_label = st.session_state.current_source_type or "Source"
        st.markdown(f"""
            <div class="sidebar-card">
                <div style="font-size: 0.72rem; color: #10B981; font-weight: 700; text-transform: uppercase; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 6px;">
                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981;"></span>
                    ACTIVE {source_label.upper()}
                </div>
                <div style="font-size: 0.85rem; color: #F1F5F9; font-weight: 600; word-break: break-all; margin-bottom: 0.5rem;">
                    {st.session_state.current_doc_name}
                </div>
                <div style="font-size: 0.75rem; color: #64748B;">
                    Context Window: <strong>Top-{k_chunks} Chunks</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="sidebar-card" style="border-style: dashed;">
                <div style="font-size: 0.8rem; color: #64748B; text-align: center;">
                    No knowledge source indexed. Select a file or URL above to begin.
                </div>
            </div>
        """, unsafe_allow_html=True)

# Main Application Banner
is_ready = st.session_state.vector_store is not None
status_pill_class = "ready" if is_ready else "idle"
status_text = "READY FOR QUERIES" if is_ready else "INDEX PENDING"

st.markdown(f"""
    <div class="brand-container">
        <div class="brand-left">
            <div class="brand-logo-badge">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
            </div>
            <div>
                <h1 class="brand-title">DOCSY</h1>
                <p class="brand-tagline">Semantic Document & Knowledge Graph Assistant</p>
            </div>
        </div>
        <div class="brand-meta">
            <div class="status-pill {status_pill_class}">
                <span class="status-dot {status_pill_class}"></span>
                <span>{status_text}</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Empty State / Hero Card when no conversation exists
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Grounded AI Retrieval & Synthesis</div>
            <div class="hero-description">
                Ask targeted questions, synthesize complex reports, and extract precise references with strict factual grounding against your indexed documents.
            </div>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-label">Multi-Format Parsing</div>
                    <div class="feature-desc">Ingests PDF, DOCX, PPTX, CSV, TXT, Web URLs, and YouTube transcripts into semantic vector structures.</div>
                </div>
                <div class="feature-item">
                    <div class="feature-label">Dense Vector Search</div>
                    <div class="feature-desc">High-precision embedding cosine retrieval via BAAI/bge-small-en-v1.5.</div>
                </div>
                <div class="feature-item">
                    <div class="feature-label">Transparent Context</div>
                    <div class="feature-desc">Inspect exact retrieved passages and execution timelines for every generated response.</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Prompt Starters (Clickable)
    if is_ready:
        st.markdown('<div class="sidebar-section-header">Suggested Inquiries</div>', unsafe_allow_html=True)
        col_s1, col_s2, col_s3 = st.columns(3)
        sample_q = None
        with col_s1:
            if st.button("Summarize Key Takeaways", use_container_width=True):
                sample_q = "Provide a structured summary of the main points and key takeaways in this document."
        with col_s2:
            if st.button("Extract Core Methodologies", use_container_width=True):
                sample_q = "What are the core methodologies, architectures, or concepts detailed in this source?"
        with col_s3:
            if st.button("List Important Findings & Facts", use_container_width=True):
                sample_q = "List all critical findings, data points, or conclusions discussed."

        if sample_q:
            st.session_state.selected_sample_query = sample_q

# Render Existing Conversation Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Collapsible Intermediate Steps
        if msg.get("steps"):
            with st.expander("Execution Pipeline & Step Log", expanded=False):
                st.markdown('<div class="step-timeline">', unsafe_allow_html=True)
                for step in msg["steps"]:
                    st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(msg["content"])

        # Collapsible Grounded Source Snippets
        if "sources" in msg and msg["sources"]:
            with st.expander("Retrieved Context Passages", expanded=False):
                for i, doc in enumerate(msg["sources"], 1):
                    content = doc.page_content if hasattr(doc, "page_content") else str(doc)
                    metadata = doc.metadata if hasattr(doc, "metadata") else {}
                    meta_str = f"Source: {metadata.get('source', 'Indexed Knowledge')}" if metadata else "Source: Indexed Knowledge"
                    st.markdown(f"""
                        <div class="source-card">
                            <div class="source-header">
                                <span class="source-tag">Passage {i}</span>
                                <span class="source-meta">{meta_str}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.code(content.strip(), language="markdown")

# Handle input from chat input or sample questions
active_query = None
if "selected_sample_query" in st.session_state and st.session_state.selected_sample_query:
    active_query = st.session_state.selected_sample_query
    st.session_state.selected_sample_query = None

chat_input_val = st.chat_input("Ask a question regarding the indexed source...")
if chat_input_val:
    active_query = chat_input_val

if active_query:
    if st.session_state.vector_store is None:
        st.warning("No knowledge source indexed. Please upload a file or paste a URL in the sidebar and click 'Index Knowledge'.")
    else:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": active_query})
        with st.chat_message("user"):
            st.markdown(active_query)

        # Assistant generation with step-by-step progress
        with st.chat_message("assistant"):
            steps_log = []

            with st.status("Executing retrieval and synthesis pipeline...", expanded=True) as status:
                # Step 1: Query analysis
                status.write("Step 1: Analyzing query semantics and intent...")
                steps_log.append('<span class="step-item-tag">Step 1</span> Semantic query representation formulated.')
                time.sleep(0.12)

                # Step 2: Vector search
                status.write(f"Step 2: Performing vector similarity search for top {k_chunks} passages...")
                context_docs = st.session_state.vector_store.similarity_search(query=active_query, k=k_chunks)
                num_docs = len(context_docs)
                status.write(f"Step 2 Result: Retrieved {num_docs} relevant passage(s) from knowledge base.")
                steps_log.append(f'<span class="step-item-tag">Step 2</span> Retrieved {num_docs} context chunk(s) via vector similarity.')
                time.sleep(0.12)

                # Step 3: Prompt assembly
                status.write("Step 3: Constructing grounded prompt with context constraints...")
                chain = get_rag_chain()
                steps_log.append('<span class="step-item-tag">Step 3</span> Assembled constrained RAG prompt context.')
                time.sleep(0.12)

                # Step 4: Inference
                status.write("Step 4: Streaming grounded response from LLM...")
                steps_log.append('<span class="step-item-tag">Step 4</span> Generated synthesized response.')

                status.update(label="Inference pipeline complete", state="complete", expanded=False)

            try:
                def generate_response_stream():
                    try:
                        for chunk in chain.stream({"query": active_query, "context": context_docs}):
                            yield chunk
                    except Exception:
                        full_res = chain.invoke({"query": active_query, "context": context_docs})
                        for word in full_res.split(" "):
                            yield word + " "
                            time.sleep(0.01)

                response_text = st.write_stream(generate_response_stream)

                if context_docs:
                    with st.expander("Retrieved Context Passages", expanded=False):
                        for i, doc in enumerate(context_docs, 1):
                            content = doc.page_content if hasattr(doc, "page_content") else str(doc)
                            metadata = doc.metadata if hasattr(doc, "metadata") else {}
                            meta_str = f"Source: {metadata.get('source', 'Indexed Knowledge')}" if metadata else "Source: Indexed Knowledge"
                            st.markdown(f"""
                                <div class="source-card">
                                    <div class="source-header">
                                        <span class="source-tag">Passage {i}</span>
                                        <span class="source-meta">{meta_str}</span>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            st.code(content.strip(), language="markdown")

                # Save assistant response to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": context_docs,
                    "steps": steps_log
                })
            except Exception as e:
                error_msg = f"An error occurred during response synthesis: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "steps": steps_log
                })