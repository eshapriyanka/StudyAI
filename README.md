# StudyAI — RAG-Based PDF Assistant

StudyAI is an intelligent learning assistant that transforms static lecture notes into an interactive study environment. Built using Retrieval-Augmented Generation (RAG), StudyAI enables students to upload academic PDFs and interact with them through natural language queries, automated summarization, quiz generation, and personalized study planning. The system incorporates intent-based routing and session memory to provide context-aware responses and support follow-up interactions, creating a more engaging and efficient learning experience.
---

## Features

### RAG-Powered Question Answering
- Retrieves relevant content from uploaded lecture notes using semantic similarity search.  
- Generates accurate, context-grounded answers instead of relying solely on model knowledge.

### Intent-Based Task Routing
- Automatically identifies user intent and routes requests to specialized modules. 
- Supports multiple academic tasks through a unified interface.  

### Context-Aware Session Memory
- Maintains interaction history within a session. 
- Enables refinement-based follow-up queries without reprocessing documents.

### Multi-Tool Learning Assistant
- Question Answering 
- Summarization
- Quiz Generation
- Study Plan Creation
- Follow-Up Refinement
  - "make it shorter"
  - "explain better"
  - "make it harder"
- The system utilizes previous responses as context to generate improved outputs.

---

## Architecture Flow

```text
                     +----------------+
                     |   PDF Upload   |
                     +----------------+
                              |
                              v
                     +----------------+
                     | Document Loader |
                     +----------------+
                              |
                              v
                     +----------------+
                     | Text Chunking  |
                     +----------------+
                              |
                              v
                     +---------------------------+
                     | Sentence Transformer      |
                     | Embeddings                |
                     +---------------------------+
                              |
                              v
                     +----------------+
                     | FAISS VectorDB |
                     +----------------+
                              |
                              v
                     +----------------+
                     | User Query     |
                     +----------------+
                              |
                              v
                     +----------------+
                     | Intent Router  |
                     +----------------+
                              |
      -----------------------------------------------------
      |             |              |             |         |
      v             v              v             v         v
+-----------+ +-----------+ +-----------+ +-----------+ +-----------+
| Retrieval | | Summary   | | Quiz Gen  | | Study     | | Follow-Up |
| QA        | | Generator | | Module    | | Planner   | | Handler   |
+-----------+ +-----------+ +-----------+ +-----------+ +-----------+
                              |
                              v
                     +----------------+
                     | Session Memory |
                     +----------------+
                              |
                              v
                     +----------------+
                     | Groq LLaMA LLM |
                     +----------------+
                              |
                              v
                     +----------------+
                     | Final Response |
                     +----------------+
```

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Large Language Model

* LLaMA (via Groq API)

### Retrieval System

* LangChain
* Sentence Transformers
* FAISS Vector Store

### Core Components

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Intent Routing
* Session-Based Memory
* Prompt Engineering

---

## Project Workflow

1. User uploads a PDF document.
2. The document is loaded and split into manageable text chunks.
3. Sentence Transformer embeddings are generated.
4. Embeddings are stored in a FAISS vector database.
5. User submits a query.
6. Intent Router identifies the requested task.
7. Relevant tool/module is selected:

   * Question Answering
   * Summarization
   * Quiz Generation
   * Study Planning
   * Follow-Up Handling
8. Retrieved context is combined with the user query.
9. Groq-hosted LLaMA generates a response.
10. Session memory stores interaction history for future follow-ups.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/StudyAI.git
cd StudyAI
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the Application

```bash
streamlit run app.py
```

---

## Author

**Esha Priyanka Thota**

Computer Science and Engineering Student
---
