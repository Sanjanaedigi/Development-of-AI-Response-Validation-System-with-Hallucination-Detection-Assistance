# Development-of-AI-Response-Validation-System-with-Hallucination-Detection-Assistance
Milestone 1

This repository contains the foundation architecture, technology stack, and initial module design for the Automated AI Response Evaluation Pipeline. The system leverages a RAG (Retrieval-Augmented Generation) workflow and a multi-agent validation funnel to critique AI-generated outputs for factual safety.

## Problem Statement

Generative AI models frequently generate text containing **hallucinations** (untrue facts), **off-topic drift** (unrelated answers), and **incomplete answers** [M1.1]. Relying on a single, expensive LLM prompt to grade these errors introduces prompt distraction and unreliable scoring. Organizations lack a lightweight, local, and structured pipeline to automatically audit AI outputs before exposing them to users.

---

## Objective

To build an automated **LLM-as-a-Judge** auditing pipeline that evaluates AI responses across multiple independent dimensions using specialized micro-agents [M1.1]. By processing answers through a strict sequential filtering sequence, the system ensures that only context-grounded, highly relevant, and complete answers pass through to the end user.

---

## System Architecture & Data Flow

Our architecture processes submissions through a sequential multi-agent validation funnel to clean, audit, and score AI responses [M1.2].

```text
       [ INPUT: Question + AI Response + Optional Reference ]
                                │
                                ▼
                   ┌─────────────────────────┐
                   │  EVALUATION CONTROLLER  │
                   │     (Orchestrator)      │
                   └─────────────────────────┘
                                │
                                ▼
          =============================================
           THE VALIDATION FUNNEL (Cleaning the Answer)
          =============================================
          \                                         /
           \          FILTER 1: RELEVANCE          /  <-- Catches off-topic
            \      "Is this on the right topic?"  /       answers.
             \───────────────────────────────────/
                                │
                                ▼
                       \─────────────────/
                        \   FILTER 2:   /     <-- Catches lies using
                         \HALLUCINATION /         your RAG Knowledge
                          \─────────────/         Base/Reference data.
                                │
                                ▼
                             \─────/
                              \ 3 /           <-- FILTER 3: COMPLETENESS
                               \─/                "Did it miss anything?"
                                │
                                ▼
                   ┌─────────────────────────┐
                   │     VERDICT AGENT       │
                   │ (Combines filter scores)│
                   └────────────┬────────────┘
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
       [ 🟢 ALL FILTERS PASSED ]     [ 🔴 FILTER BLOCK ]
                 │                             │
                 ▼                             ▼
         ┌──────────────┐              ┌──────────────┐
         │   USER UI    │              │  DASHBOARD   │
         │ (Safe Output)│              │  & REPORTS   │
         └──────────────┘              └──────────────┘
```

---

## Agent Responsibilities & Scoring Matrix

The system distributes tasks to specialized micro-agents coordinated by a central manager to ensure high focus and deterministic evaluations [M1.2].

*   **Evaluation Controller (Orchestrator):** Manages the input data stream, initializes the state context, fetches relevant background records from ChromaDB, and coordinates the step-by-step state handoffs between judge agents.
*   **Filter 1: Relevance Judge Agent:** Evaluates if the AI's generated response directly addresses the core intent of the user's initial question without drifting into unrelated topics.
*   **Filter 2: Hallucination Judge Agent:** Performs strict factual grounding checks by matching the assertions made in the AI response line-by-line against retrieved database reference context.
*   **Filter 3: Completeness Judge Agent:** Analyzes the user's question to find all hidden requirements and checks if the AI responded to every single part completely.
*   **Verdict Agent:** Acts as the final supervisor. It aggregates the scores from all three filtering nodes, reviews the evaluation logs, and applies the logic to flag the response as a Pass or a Block.

| Agent Filter Name | Primary Responsibility | Target Metric | Scoring Scale |
| :--- | :--- | :--- | :--- |
| **Evaluation Controller** | Prepares data and manages the state machine workflow transitions [M1.2]. | Context Injection | Internal Graph State |
| **Filter 1: Relevance** | Evaluates if the AI response directly answers the user's question without drifting [M1.1, M1.2]. | Answer Relevance | `0.0 to 1.0` |
| **Filter 2: Hallucination** | Audits whether statements are strictly grounded in, and backed by, the reference data chunks [M1.1, M1.2]. | Faithfulness / Groundedness | `0.0 to 1.0` |
| **Filter 3: Completeness** | Assesses whether the AI response completely addresses all explicit parts of the query [M1.1, M1.2]. | Information Completeness | `0.0 to 1.0` |
| **Verdict Agent** | Consolidates individual filter scores and routes outputs based on custom rules (`🟢 PASS` / `🔴 BLOCK`) [M1.2]. | Final System Verdict | Conditional Threshold |

---

## Tech Stack

*   **Frontend Interface:** **Streamlit** (Building responsive web dashboards entirely in Python).
*   **Backend Framework:** **FastAPI** (Handles high-performance API routing and auto-generates Swagger/OpenAPI documentation) [M1.3].
*   **AI Core Engine:** **Gemini API** (`gemini-1.5-flash`) (Executes evaluation prompts and serves as the model for the judges) [M1.1].
*   **Orchestration Framework:** **LangChain / LangGraph** (Manages state transitions and handoffs between judge agents) [M1.2].
*   **Architecture Pattern:** **RAG (Retrieval-Augmented Generation)** (Connects the local knowledge base to the AI judges) [M1.4].
*   **Vector Database:** **ChromaDB** (Stores and semantically searches reference facts locally on-disk) [M1.4].
*   **Embeddings Engine:** **Sentence Transformers** (`all-MiniLM-L6-v2`) (Converts text chunks into numeric vectors locally) [M1.4].
*   **Benchmark Datasets:** **TruthfulQA & SQuAD** from Hugging Face (Seeds the reference library with baseline facts) [M1.4].
*   **Testing Framework:** **Pytest** (Runs automated unit tests on validation pipelines and data schemas).

---

## Project Structure

```text
app/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI Web API Application Gateway Router
│   ├── schemas.py              # Ingestion Contracts & Input Validation Models
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── prompts.py          # LLM-as-a-Judge Prompt Instructions
│   │   └── graph.py            # LangGraph State Machine Sequential Pipeline
│   │
│   └── knowledge_base/
│       ├── __init__.py
│       ├── vector_store.py     # ChromaDB Database Engine Initialization
│       └── ingest.py           # Hugging Face Dataset Downloader & Text Chunking
|
├── final_ui.py                # Streamlit Web Presentation Dashboard UI
├── requirements.txt            # Software Package Dependencies
└── test_pipeline.py            # Automated Unit Testing Suite (Pytest framework)
```

---

## Installation

1.  **Clone the Repository Workspace:**
    ```bash
    git clone https://github.com
    cd app
    ```
2.  **Install Required Software Packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Configuration

Configure your credentials by exporting your Gemini token to your current environment shell runtime context:

```bash
# On Linux/macOS
export GOOGLE_API_KEY="your-actual-gemini-api-key"

# On Windows (Command Prompt)
set GOOGLE_API_KEY="your-actual-gemini-api-key"

# On Windows (PowerShell)
\$env:GOOGLE_API_KEY="your-actual-gemini-api-key"
```

---

## Running the Application

### Step 1: Preprocess and Seed the Vector Database
Download the benchmark datasets from Hugging Face, apply text splitting, and index the clean chunks locally [M1.4]:
```bash
python -m app.knowledge_base.ingest
```

### Step 2: Spin Up the FastAPI Web API Server Backend
Run the backend web engine cluster gateway using Uvicorn [M1.3]:
```bash
python -m uvicorn app.app.main:app --reload
```
*Note: View interactive API schemas at `http://127.0.0`.*

### Step 3: Launch the Streamlit Frontend Web Dashboard Panel
Open an independent terminal tab window session and start your frontend user interface:
```bash
streamlit run app\final_ui.py
```

---

## Testing

Automated testing is built into the core pipeline using **Pytest** and the **FastAPI TestClient** framework to guarantee that API validation layers, structural input parameters, and agent routing logic remain accurate and reliable.

### Running Tests Locally
To execute the automated diagnostic test suite, open your terminal and run:
```bash
pytest test_pipeline.py -v
```

### Covered Test Dimensions
*   **Empty Payload Interception:** Verifies that the API gateway catches bad submissions (like blank spaces) early and blocks them with a standard `422 Unprocessable Entity` status code before starting downstream LLM processes.

---

## Limitations

*   **Fixed Score Thresholds:** The Verdict Agent uses hardcoded numeric cutoff scores (e.g., `>= 0.7`) to block responses, which might require tuning across different production workflows.
*   **Local Compute Dependencies:** Embedding generation relies on running `sentence-transformers` locally, which consumes CPU resources during bulk ingestion phases.
*   **Simple Parsing Engine:** Extracting judge scores from raw LLM responses relies on strict regular expressions, which can break if the model formats outputs unexpectedly.

---
## Future Improvements

*   **Early-Exit Conditional Routing:** Modify the LangGraph state transitions to stop evaluation immediately if Filter 1 (Relevance) fails, saving unnecessary model tokens.
*   **Dynamic Threshold Adapters:** Allow custom scoring thresholds to be passed directly inside the FastAPI request payload metadata.
*   **Persistent SQLite Analytical Logs:** Replace temporary execution dictionaries with a persistent relational database tracking engine to log audit performance trends over time.
