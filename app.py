import streamlit as st
from functions.pdf_loader import load_and_split_pdf
from functions.vector_store import create_vector_store
from functions.router import route_query, is_follow_up
from functions.tools import (
    answer_question,
    summarize_notes,
    generate_quiz,
    create_study_plan,
    handle_follow_up,
)

st.set_page_config(page_title="StudyAI", page_icon="📚", layout="wide")

st.markdown("""
<style>

/* ---------- Main App ---------- */

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e1b4b
    );
    color:white;
}

/* Hide Streamlit Branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ---------- Hero ---------- */

.hero{
    background: linear-gradient(
        135deg,
        rgba(99,102,241,0.95),
        rgba(139,92,246,0.95)
    );

    padding:35px;
    border-radius:25px;

    text-align:center;

    margin-bottom:25px;

    box-shadow:0px 10px 30px rgba(0,0,0,0.35);
}

.hero h1{
    color:white;
    font-size:3rem;
    margin-bottom:10px;
}

.hero p{
    color:#e5e7eb;
    font-size:1.1rem;
}

/* ---------- Cards ---------- */

.glass-card{
    background: rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    border:1px solid rgba(255,255,255,0.15);

    border-radius:20px;

    padding:20px;

    margin-bottom:15px;

    box-shadow:0px 6px 20px rgba(0,0,0,0.25);
}

.glass-card h3{
    color:white;
}

.glass-card p{
    color:#d1d5db;
}

/* ---------- Response ---------- */

.response-card{
    background: rgba(255,255,255,0.08);

    border-radius:25px;

    padding:25px;

    margin-top:20px;

    border:1px solid rgba(255,255,255,0.15);

    box-shadow:0px 8px 25px rgba(0,0,0,0.3);
}

/* ---------- Memory ---------- */

.memory-card{
     background: rgba(255,255,255,0.08);

    backdrop-filter: blur(10px);

    border-left: 5px solid #8b5cf6;

    border-radius: 16px;

    padding: 18px;

    margin-bottom: 15px;

    color: #f3f4f6;

    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
}
.memory-card h4{
    color: #c4b5fd;
    margin-bottom: 10px;
}
/* ---------- Buttons ---------- */

.stButton > button{

    width:100%;

    background:linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color:white;

    border:none;

    border-radius:12px;

    height:55px;

    font-weight:600;
}

.stButton > button:hover{
    transform:scale(1.02);
}

/* ---------- Input ---------- */

textarea{
    background:#111827 !important;
    color:white !important;
    border-radius:15px !important;
}

input{
    color:white !important;
}

/* ---------- Upload ---------- */

[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.08);

    padding:20px;

    border-radius:20px;

    border:1px solid rgba(255,255,255,0.15);
}
p, div, span, label {
    color: #f3f4f6 !important;
}
.glass-card{
    min-height:180px;
}
.feature-card{
    min-height:180px;
}
            .glass-card:hover{
    transform: translateY(-4px);
    transition:0.25s;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State Initialization
# -----------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "last_uploaded_file_name" not in st.session_state:
    st.session_state.last_uploaded_file_name = None

if "history" not in st.session_state:
    st.session_state.history = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "last_tool" not in st.session_state:
    st.session_state.last_tool = ""

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "input_box" not in st.session_state:
    st.session_state.input_box = ""

# -----------------------------
# Main Title
# -----------------------------
st.markdown("""
<div class="hero">

<h1>📚 StudyAI</h1>

<p>
Transform your lecture notes into an intelligent learning experience.
Ask questions, generate quizzes, summarize topics,
and create study plans in seconds.
</p>

</div>
""", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📖 Q&A", "Ready")

with col2:
    st.metric("📄 Summaries", "AI Powered")

with col3:
    st.metric("🧪 Quiz Gen", "Active")

with col4:
    st.metric("📅 Planner", "Available")
# -----------------------------
# PDF Processing
# -----------------------------
st.markdown("""
<div class="glass-card">

<h3>📂 Upload Your Notes</h3>

<p>
Upload lecture notes, study material, or academic PDFs
and start interacting with them instantly.
</p>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your PDF here",
    type=["pdf"]
)

if uploaded_file is not None:
    if st.session_state.last_uploaded_file_name != uploaded_file.name:
        st.session_state.vector_store = None
        st.session_state.last_uploaded_file_name = uploaded_file.name

        # Reset memory for new document
        st.session_state.history = []
        st.session_state.last_response = ""
        st.session_state.last_tool = ""
        st.session_state.last_query = ""
        st.session_state.input_box = ""

    if st.session_state.vector_store is None:
        with st.spinner("Processing PDF and building knowledge base..."):
            chunks = load_and_split_pdf(uploaded_file)

            if not chunks:
                st.error(
                    "No readable text could be extracted from this PDF. "
                    "It may be handwritten, scanned, or image-based."
                )
                st.stop()

            st.session_state.vector_store = create_vector_store(chunks)

            if st.session_state.vector_store is None:
                st.error("Could not build vector store because no valid text chunks were created.")
                st.stop()

        st.success("PDF processed successfully!")

if uploaded_file and st.session_state.vector_store:
    st.caption(f"Current document: {uploaded_file.name}")
    st.success("Document is ready for querying.")
else:
    st.warning("Upload a readable PDF to start using the agent.")




st.markdown("## 🚀 What StudyAI Can Do")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="glass-card feature-card">
    <h3>📖 Ask</h3>
    <p>Question answering using RAG.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card feature-card">
    <h3>📄 Summarize</h3>
    <p>Generate concise notes instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card feature-card">
    <h3>🧪 Quiz</h3>
    <p>Create MCQs with explanations.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="glass-card feature-card">
    <h3>📅 Planner</h3>
    <p>Build personalized study schedules.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Quick Actions
# -----------------------------
st.markdown(
    """
    <div class="glass-card">
    <h2>⚡ Quick Actions</h2>
    </div>
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns(3)

button_query = None

with col1:
    if st.button("📄 Summarize Notes", use_container_width=True):
        button_query = "summarize the document"
        st.session_state.input_box = ""

with col2:
    if st.button("🧪 Generate Quiz", use_container_width=True):
        button_query = "generate a quiz"
        st.session_state.input_box = ""

with col3:
    if st.button("📅 Study Plan", use_container_width=True):
        button_query = "create a study plan"
        st.session_state.input_box = ""

# -----------------------------
# Text Input
# -----------------------------
st.markdown("### 💬 Chat With StudyAI")

query_col, button_col = st.columns([5,1])

with query_col:
    text_query = st.text_area(
        "",
        placeholder="Ask anything about your notes...",
        height=120,
        key="input_box"
    )

with button_col:
    send = st.button("🚀 Ask")
# Button gets priority over typed text
if button_query is not None:
    selected_query = button_query
else:
    selected_query = text_query

# -----------------------------
# Agent Execution
# -----------------------------
if selected_query and st.session_state.vector_store:
    if is_follow_up(selected_query) and st.session_state.last_response:
        tool = "follow-up"
        st.markdown(
            f"""
            <div class="glass-card">
            <b>🧠 Active Tool:</b> {tool}
            </div>
            """,
            unsafe_allow_html=True
            )

        with st.spinner("Handling follow-up from memory..."):
            response = handle_follow_up(st.session_state.last_response, selected_query)
            docs = []
    else:
        tool = route_query(selected_query)
        st.markdown(
            f"""
            <div class="glass-card">
            <b>🧠 Active Tool:</b> {tool}
            </div>
            """,
            unsafe_allow_html=True
            )

        with st.spinner(f"Agent selected tool: {tool}"):
            if tool == "summarize":
                response, docs = summarize_notes(st.session_state.vector_store)

            elif tool == "quiz":
                response, docs = generate_quiz(st.session_state.vector_store)

            elif tool == "planner":
                response, docs = create_study_plan(
                    st.session_state.vector_store,
                    selected_query
                )

            else:
                response, docs = answer_question(
                    st.session_state.vector_store,
                    selected_query
                )

    # Save memory
    st.session_state.last_response = response
    st.session_state.last_tool = tool
    st.session_state.last_query = selected_query

    if (
        not st.session_state.history
        or st.session_state.history[-1]["query"] != selected_query
    ):
        st.session_state.history.append({
            "query": selected_query,
            "tool": tool,
            "response": response
        })

    # Show response
    st.markdown("## 🤖 StudyAI Response")

    st.markdown(
        f"""
        <div class="response-card">
        {response}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show retrieved docs when available
    if docs:
        with st.expander("📚 View Retrieved Source Context"):
            for i, doc in enumerate(docs, 1):
                st.markdown(f"**Source {i}**")
                st.caption(doc.page_content[:300])
                st.markdown("---")

elif selected_query and not st.session_state.vector_store:
    st.warning("Please upload a readable PDF first.")

# -----------------------------
# Conversation Memory
# -----------------------------
if st.session_state.history:

    st.markdown("""
    <div class="glass-card">
        <h2>🕘 Session Memory</h2>
        <p>Your previous interactions in this session.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📂 View Conversation History", expanded=False):

        for idx, item in enumerate(reversed(st.session_state.history), 1):

            st.markdown(
                f"""
                <div class="memory-card">

                <h4>💬 Interaction {idx}</h4>

                <b>Query:</b><br>
                {item['query']}

                <br><br>

                <b>Tool Used:</b><br>
                {item['tool']}

                <br><br>

                <b>Response Preview:</b><br>
                {item['response'][:250]}...

                </div>
                """,
                unsafe_allow_html=True
            )