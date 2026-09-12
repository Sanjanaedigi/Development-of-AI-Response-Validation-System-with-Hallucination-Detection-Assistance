# Development of AI Response Validation System with Hallucination Detection Assistance

## Milestone 1 — Foundation & Evaluation Understanding

This repository is a reproducible Milestone 1 foundation for evaluating AI-generated responses using four dimensions: relevance, accuracy/factuality, hallucination safety/faithfulness, and completeness. It includes a RAG-style reference knowledge base seeded from public TruthfulQA and SQuAD datasets, dense embedding generation, vector retrieval, a multi-agent evaluation flow, a FastAPI API, Streamlit UI, tests, architecture documentation, and Agile delivery artifacts.

## Milestone 1 coverage

| Requirement | Implementation |
|---|---|
| M1.1 Research | `architecture/milestone1_research.md` |
| M1.2 Architecture | `architecture/system_architecture.md`, `architecture/agent_responsibilities.md` |
| M1.3 Evaluation Input | `frontend/final_ui.py`, `app/main.py`, `app/schemas.py` |
| M1.4 Benchmarks | `app/knowledge_base/ingest.py`, `data/benchmark_manifest.json` |
| Chunking | `app/knowledge_base/chunking.py` |
| Embeddings | `app/knowledge_base/embeddings.py` |
| Vector retrieval | `app/knowledge_base/vector_store.py` |
| Retrieval validation | `scripts/validate_retrieval.py`, `tests/test_retrieval.py` |
| Automated testing | `tests/` |
| Agile methodology | `Agile/` |

## Architecture

```text
Evaluation UI
    |
    v
FastAPI + Pydantic validation
    |
    v
Evaluation Orchestrator <---- RAG Knowledge Base
    |                         |-- TruthfulQA
    |                         |-- SQuAD
    |                         |-- Cleaning + chunking
    |                         |-- Embeddings
    |                         `-- Vector similarity search
    |
    +--> Relevance Judge
    +--> Accuracy Judge
    +--> Hallucination Detection Judge
    `--> Completeness Judge
             |
             v
       Scoring + Verdict
             |
             v
     Structured results + evidence
```

A visual Mermaid version is in `architecture/system_architecture.md`.

## Technology stack

Python, FastAPI, Pydantic, Streamlit, Hugging Face Datasets, Sentence Transformers, NumPy, scikit-learn, Pytest, JSON/JSONL, Git/GitHub, and Agile sprint artifacts.

## Benchmark sources

The ingestion script uses the Hugging Face datasets `truthfulqa/truthful_qa` (generation/validation) and `rajpurkar/squad` (train by default). The benchmark manifest records the dataset identifiers and licenses. Raw downloads are not committed; they can be reproduced with one command.

## Setup on Windows PowerShell

```powershell
cd "C:\path\to\Development-of-AI-Response-Validation-System-with-Hallucination-Detection-Assistance"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Build the Milestone 1 benchmark knowledge base

For a reproducible bounded development dataset:

```powershell
python -m app.knowledge_base.ingest --mode benchmarks --squad-limit 200 --truthfulqa-limit 200
```

This performs:

`Hugging Face dataset -> normalization -> chunking -> embeddings -> local vector index`

The default embedding backend is `sentence-transformers/all-MiniLM-L6-v2`. If the model cannot be downloaded, the project falls back to a deterministic HashingVectorizer for local/CI execution. To require the real dense embedding model, set `EMBEDDING_STRICT=1`.

## Validate retrieval quality

After building the benchmark KB:

```powershell
python scripts/validate_retrieval.py
```

The command writes `data/processed/retrieval_report.json` and reports Hit@5 for a representative sample of benchmark questions.

## Run the backend

```powershell
python -m uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`

## Run the UI

In a second terminal:

```powershell
python -m streamlit run frontend/final_ui.py
```

Open the Streamlit URL shown in the terminal, normally `http://localhost:8501`.

## Run tests

```powershell
python -m pytest -q
```

The test suite covers input validation, all four agents, SQuAD/TruthfulQA normalization, retrieval, and API pipeline routing.

## Evaluation scoring

Milestone 1 uses equal weights:

- Relevance — 25%
- Accuracy — 25%
- Hallucination safety — 25%
- Completeness — 25%

Overall score is the weighted mean. `>= 0.70` returns `VALID`; otherwise `FILTER BLOCKED`.

These are explicit baseline choices, not claims of calibrated production accuracy. Calibration and LLM-as-a-Judge evaluation are planned for later milestones.

## Agile working model

The `Agile/` directory contains:

- Product backlog with user stories and acceptance criteria
- Milestone 1 sprint plan
- Definition of Done
- Defect tracker
- Unit test plan
- Change log
- Milestone review checklist

For every future milestone, work can be managed as:

`Backlog -> Sprint Planning -> Development -> Test -> Review -> Retrospective -> Backlog update`

A story is not Done until acceptance criteria, tests, documentation and review evidence are complete.

## Security

Never commit `.env`, API keys, access tokens, passwords or other secrets. `.env.example` contains configuration names only.
