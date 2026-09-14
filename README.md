# Development of AI Response Validation System with Hallucination Detection Assistance

## Project Overview

The **AI Response Validation System** is designed to evaluate AI-generated responses using multiple validation dimensions: relevance, accuracy/factuality, hallucination safety/faithfulness, and completeness.

The system uses a RAG-style reference knowledge base, semantic retrieval, specialized evaluation agents, a FastAPI backend, a Streamlit user interface, automated tests, benchmark evaluation, and Agile development practices.

---

# Milestone 1 — Foundation & Evaluation Understanding

Milestone 1 established the foundation for evaluating AI-generated responses.

It includes:

* Evaluation research and architecture
* RAG-style reference knowledge base
* TruthfulQA and SQuAD benchmark sources
* Text chunking
* Embedding generation
* Vector similarity retrieval
* Multi-agent evaluation flow
* FastAPI API
* Streamlit UI
* Automated testing
* Agile delivery artifacts

## Milestone 1 Coverage

| Requirement           | Implementation                                                                  |
| --------------------- | ------------------------------------------------------------------------------- |
| M1.1 Research         | `architecture/milestone1_research.md`                                           |
| M1.2 Architecture     | `architecture/system_architecture.md`, `architecture/agent_responsibilities.md` |
| M1.3 Evaluation Input | `frontend/final_ui.py`, `app/main.py`, `app/schemas.py`                         |
| M1.4 Benchmarks       | `app/knowledge_base/ingest.py`, `data/benchmark_manifest.json`                  |
| Chunking              | `app/knowledge_base/chunking.py`                                                |
| Embeddings            | `app/knowledge_base/embeddings.py`                                              |
| Vector Retrieval      | `app/knowledge_base/vector_store.py`                                            |
| Retrieval Validation  | `scripts/validate_retrieval.py`, `tests/test_retrieval.py`                      |
| Automated Testing     | `tests/`                                                                        |
| Agile Methodology     | `Agile/`                                                                        |

---

# Milestone 2 — Evaluation Agents & Validation

Milestone 2 focuses on implementing and validating specialized evaluation agents.

## M2.1 Relevance Judge Agent

The Relevance Judge Agent evaluates whether an AI-generated response directly addresses the submitted question.

It provides:

* Relevance score
* Relevance category
* Explanation/reasoning
* Semantic similarity
* Question-response overlap
* Evidence support when available

Relevance categories include:

* Fully Relevant
* Mostly Relevant
* Partially Relevant
* Mostly Unrelated
* Off-Topic

Implementation:

`app/agents/relevance_agent.py`

---

## M2.2 Accuracy Judge Agent

The Accuracy Judge Agent evaluates the factual correctness of an AI-generated response.

It uses:

1. A provided reference answer when available.
2. Retrieved knowledge-base evidence when a reference answer is not available.

The agent provides:

* Accuracy score
* Accuracy category
* Reasoning/explanation
* Supporting evidence
* Semantic similarity
* Overlap score
* Contradiction detection

Accuracy categories include:

* Correct
* Mostly Correct
* Partially Correct
* Mostly Incorrect
* Incorrect
* Uncertain when sufficient evidence is unavailable

Implementation:

`app/agents/accuracy_agent.py`

---

## M2.3 Hallucination Detection Agent

The Hallucination Detection Agent verifies individual factual claims against retrieved evidence.

The agent:

* Splits responses into individual claims
* Checks each claim against available evidence
* Measures semantic support
* Checks for contradictions
* Identifies unsupported claims
* Provides supporting evidence
* Provides reasoning for unsupported or contradictory claims

This allows the system to identify a specific unsupported statement rather than simply marking the complete response as hallucinated.

Implementation:

`app/agents/hallucination_agent.py`

---

## M2.4 Benchmark & Agent Validation

Milestone 2 includes a dedicated evaluation set:

`data/milestone2_evaluation_set.json`

The evaluation set contains representative cases covering:

* Correct responses
* Incorrect responses
* Partially correct responses
* Irrelevant responses
* Incomplete responses
* Unsupported claims
* Contradictory responses

The Milestone 2 evaluation tests are implemented in:

`tests/test_milestone2_evaluation.py`

The benchmark manifest containing TruthfulQA and SQuAD sources is available at:

`data/benchmark_manifest.json`

---

# Architecture

```text
Evaluation UI
      |
      v
FastAPI + Pydantic Validation
      |
      v
Evaluation Orchestrator <---- RAG Knowledge Base
      |                         |-- TruthfulQA
      |                         |-- SQuAD
      |                         |-- Cleaning + Chunking
      |                         |-- Embeddings
      |                         `-- Vector Similarity Search
      |
      +--> Relevance Judge
      |
      +--> Accuracy Judge
      |
      +--> Hallucination Detection Judge
      |
      `--> Completeness Judge
              |
              v
       Scoring + Verdict
              |
              v
     Structured Results + Evidence
```

The detailed architecture is documented in:

`architecture/system_architecture.md`

Agent responsibilities are documented in:

`architecture/agent_responsibilities.md`

---

# Technology Stack

* Python
* FastAPI
* Pydantic
* Streamlit
* Hugging Face Datasets
* Sentence Transformers
* NumPy
* scikit-learn
* Pytest
* JSON / JSONL
* Git / GitHub
* Agile methodology

---

# Benchmark Sources

The project uses benchmark datasets from Hugging Face:

* TruthfulQA — truthfulness and hallucination-oriented question answering
* SQuAD — reading-comprehension question answering

The benchmark manifest records dataset identifiers, configurations, splits, purposes, and licenses.

Raw benchmark downloads are not committed to the repository. They can be reproduced using the ingestion script.

---

# Setup on Windows PowerShell

```powershell
cd "C:\Users\Sanjana\OneDrive\Desktop\AI_Response_Validation_System"

python -m venv venv

.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

# Build the Benchmark Knowledge Base

For a reproducible bounded development dataset:

```powershell
python -m app.knowledge_base.ingest --mode benchmarks --squad-limit 200 --truthfulqa-limit 200
```

The process is:

```text
Hugging Face Dataset
        |
        v
Normalization
        |
        v
Chunking
        |
        v
Embeddings
        |
        v
Local Vector Index
```

The default embedding backend is:

`sentence-transformers/all-MiniLM-L6-v2`

If the model cannot be downloaded, the project can fall back to a deterministic HashingVectorizer for local/CI execution.

To require the real dense embedding model:

```powershell
$env:EMBEDDING_STRICT="1"
```

---

# Validate Retrieval Quality

After building the benchmark knowledge base:

```powershell
python scripts/validate_retrieval.py
```

The command generates:

`data/processed/retrieval_report.json`

and reports retrieval performance for representative benchmark questions.

---

# Run the Backend

Start the FastAPI backend:

```powershell
uvicorn app.main:app --reload
```

API:

`http://127.0.0.1:8000`

Swagger documentation:

`http://127.0.0.1:8000/docs`

---

# Run the User Interface

Open a second PowerShell terminal.

Navigate to the project:

```powershell
cd "C:\Users\Sanjana\OneDrive\Desktop\AI_Response_Validation_System"
```

Activate the virtual environment if required:

```powershell
.\venv\Scripts\Activate.ps1
```

Then run:

```powershell
streamlit run frontend\final_ui.py
```

The Streamlit interface normally opens at:

`http://localhost:8501`

The interface accepts:

* User Question
* AI Generated Response
* Reference / Evidence
* Source Document / Reference Material

The system then evaluates the response using the evaluation pipeline.

---

# Run Tests

Run the complete test suite:

```powershell
pytest -v
```

The current Milestone 2 regression suite passes:

**19 tests passed**

There are currently 4 deprecation warnings, but they do not cause test failures.

To run only the Milestone 2 evaluation tests:

```powershell
pytest tests\test_milestone2_evaluation.py -v
```

Current result:

**2 tests passed**

---

# Milestone 2 Evaluation Example

The integrated evaluation pipeline has been tested using a factual question and reference evidence.

Example result:

| Evaluation           |  Score |
| -------------------- | -----: |
| Relevance            | 92.74% |
| Accuracy             | 88.19% |
| Hallucination Safety | 98.19% |
| Completeness         | 82.50% |
| Overall Verdict      |  VALID |

These values represent a development test case and should not be interpreted as calibrated production accuracy.

---

# Evaluation Scoring

The system uses four evaluation dimensions:

* Relevance — 25%
* Accuracy — 25%
* Hallucination Safety — 25%
* Completeness — 25%

The overall score is calculated using the weighted mean.

A score of:

* `>= 0.70` → `VALID`
* `< 0.70` → `FILTER BLOCKED`

These are development baseline thresholds and are not claims of calibrated production accuracy.

---

# Agile Working Model

The `Agile/` directory contains project management and testing artifacts, including:

* Product Backlog
* Sprint Backlog
* Stand-up Meeting records
* Retrospection
* Defect Tracker
* Unit Test Plan
* Milestone documentation

The development workflow is:

```text
Backlog
   |
   v
Sprint Planning
   |
   v
Development
   |
   v
Testing
   |
   v
Review
   |
   v
Retrospective
   |
   v
Backlog Update
```

A story is considered complete after its implementation, acceptance criteria, testing, documentation, and review evidence have been addressed.

---

# Current Milestone 2 Status

| Milestone 2 Item              | Status    |
| ----------------------------- | --------- |
| Relevance Judge Agent         | Completed |
| Accuracy Judge Agent          | Completed |
| Hallucination Detection Agent | Completed |
| Benchmark Evaluation Set      | Completed |
| Agent Validation              | Completed |
| Orchestrator Integration      | Completed |
| Regression Testing            | Completed |
| Agile Documentation           | Updated   |

---

# Security

Never commit:

* `.env`
* API keys
* Access tokens
* Passwords
* Other secrets

`.env.example` contains configuration names only.

---

# Future Improvements

Possible future improvements include:

* Larger benchmark evaluation sets
* More advanced contradiction detection
* Improved claim extraction
* LLM-as-a-Judge comparison
* Score calibration
* More comprehensive hallucination evaluation
* Additional retrieval and evaluation metrics
