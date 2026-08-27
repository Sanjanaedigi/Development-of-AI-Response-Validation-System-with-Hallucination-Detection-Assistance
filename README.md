# Development-of-AI-Response-Validation-System-with-Hallucination-Detection-Assistance
Milestone 1

This repository contains the foundation architecture, technology stack, and initial module design for the Automated AI Response Evaluation Pipeline. The system leverages a RAG (Retrieval-Augmented Generation) workflow and a multi-agent validation funnel to critique AI-generated outputs for factual safety.

---

## Tech Stack

* **Frontend Interface:** Streamlit (For building the responsive web dashboard entirely in Python).
* **Backend Framework:** FastAPI (To handle high-performance API routing and auto-generate Swagger/OpenAPI documentation).
* **AI Core Engine:** Gemini API (To execute evaluation prompts and serve as the foundational model for the AI judges).
* **Orchestration Framework:** LangChain / LangGraph (To manage state, execution flow, and step-by-step handoffs between judge agents).
* **Architecture Pattern:** RAG (Retrieval-Augmented Generation) (The framework connecting the database to the AI).
* **Vector Database:** ChromaDB (To store and semantically search reference facts locally on-disk).
* **Embeddings Engine:** Sentence Transformers (`all-MiniLM-L6-v2` to convert text chunks into searchable vector representations).
* **Benchmark Datasets:** TruthfulQA & SQuAD from Hugging Face (Used to seed the reference library with baseline facts).
* **Testing Framework:** Pytest (To run automated unit tests on validation pipelines and routing logic).

---

## System Architecture & Data Flow

Our architecture processes submissions through a sequential multi-agent validation funnel to clean, audit, and score AI responses.

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



## 📦 Milestone 1 Breakdown & Status

* **M1.1 Research:** Complete. Finalized tech stack (Gemini + ChromaDB) and mapped out evaluation metrics.
* **M1.2 Architecture:** Complete. Defined orchestration funnel consisting of Relevance, Hallucination, and Completeness filters.
* **M1.3 Input Module:** Initial backend input structures and data schemas created via FastAPI endpoints.
* **M1.4 Knowledge Base:** Initialized scripts to parse Hugging Face datasets (SQuAD/TruthfulQA) into local ChromaDB storage.
