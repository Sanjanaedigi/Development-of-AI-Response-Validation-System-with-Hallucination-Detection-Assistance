# AI Response Validation System - System Architecture

## Overall Architecture

```mermaid
flowchart TD
  UI[Streamlit Evaluation UI] --> API[FastAPI API Layer]
  BATCH[Batch CSV Evaluation] --> ORCH[Evaluation Orchestrator]

  API --> VAL[Pydantic Input Validation]
  VAL --> ORCH[Evaluation Orchestrator]

  KB[TruthfulQA + SQuAD Knowledge Base] --> EMB[Embedding Generation]
  EMB --> VS[Vector Index / Semantic Search]

  ORCH --> VS
  VS --> EVID[Top-K Reference Evidence]

  ORCH --> R[Relevance Judge]
  ORCH --> A[Accuracy Judge]
  ORCH --> H[Hallucination Detection Judge]
  ORCH --> C[Completeness Judge]

  EVID --> R
  EVID --> A
  EVID --> H
  EVID --> C

  R --> SCORE[Weighted Scoring & Verdict]
  A --> SCORE
  H --> SCORE
  C --> SCORE

  SCORE --> RESULTS[Structured Evaluation Results]
  RESULTS --> STORE[Submission Storage]
  RESULTS --> UI
  RESULTS --> BATCHRESULTS[Batch Results & Statistics]