# Development of AI Response Validation System with Hallucination Detection Assistance

## Project Overview

The **AI Response Validation System** evaluates AI-generated responses using multiple validation dimensions:

* Relevance
* Accuracy / Factuality
* Hallucination Safety / Faithfulness
* Completeness

The system uses a RAG-style reference knowledge base, semantic retrieval, specialized evaluation agents, a FastAPI backend, a Streamlit user interface, automated testing, benchmark evaluation, weighted verdict scoring, and batch CSV evaluation.

The project is developed using **Agile methodology** across multiple milestones.

---

# System Architecture

```text
                         Evaluation Input
                              |
                              v
                  FastAPI + Pydantic Validation
                              |
                              v
                    Evaluation Orchestrator
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
        RAG Knowledge     Evaluation       Reference /
           Base             Agents          Evidence
              |               |
              |       +-------+-------+-------+
              |       |       |       |       |
              |       v       v       v       v
              |   Relevance Accuracy Hallucination Completeness
              |       |       |       |       |
              +-------+-------+-------+-------+
                              |
                              v
                    Weighted Scoring
                              |
                              v
                          Verdict
                              |
                +-------------+-------------+
                |                           |
                v                           v
        Individual Results          Batch Evaluation
                                        |
                                        v
                                CSV Multiple Records
                                        |
                                        v
                                Results + Statistics
```

Detailed architecture documentation:

* `architecture/system_architecture.md`
* `architecture/agent_responsibilities.md`

---

# Milestone 1 — Foundation & Evaluation Understanding

Milestone 1 established the foundation of the AI response validation system.

## M1 Coverage

| Requirement                | Implementation                                          |
| -------------------------- | ------------------------------------------------------- |
| Evaluation research        | `architecture/milestone1_research.md`                   |
| System architecture        | `architecture/system_architecture.md`                   |
| Agent responsibilities     | `architecture/agent_responsibilities.md`                |
| Evaluation Input Module    | `frontend/final_ui.py`, `app/main.py`, `app/schemas.py` |
| Question input             | `app/schemas.py`                                        |
| AI response input          | `app/schemas.py`                                        |
| Reference / Evidence input | `app/schemas.py`                                        |
| Source document input      | `app/schemas.py`                                        |
| TruthfulQA benchmark       | `app/knowledge_base/ingest.py`                          |
| SQuAD benchmark            | `app/knowledge_base/ingest.py`                          |
| Text chunking              | `app/knowledge_base/chunking.py`                        |
| Embeddings                 | `app/knowledge_base/embeddings.py`                      |
| Vector retrieval           | `app/knowledge_base/vector_store.py`                    |
| Retrieval validation       | `scripts/validate_retrieval.py`                         |
| Automated testing          | `tests/`                                                |
| Agile methodology          | `Agile/`                                                |

---

# Milestone 2 — Evaluation Agents & Validation

Milestone 2 implemented and validated the specialized evaluation agents.

## M2.1 Relevance Judge Agent

The Relevance Judge Agent evaluates whether an AI-generated response addresses the submitted question.

It provides:

* Relevance score
* Relevance category
* Explanation / reasoning
* Semantic similarity
* Question-response overlap
* Evidence support when available

Implementation:

`app/agents/relevance_agent.py`

---

## M2.2 Accuracy Judge Agent

The Accuracy Judge Agent evaluates factual correctness.

It compares the AI response against:

1. A supplied reference answer when available.
2. Retrieved knowledge-base evidence when a reference answer is not available.

It provides:

* Accuracy score
* Accuracy category
* Reasoning
* Supporting evidence
* Semantic similarity
* Overlap score
* Contradiction detection

Implementation:

`app/agents/accuracy_agent.py`

---

## M2.3 Hallucination Detection Agent

The Hallucination Detection Agent evaluates factual claims against available evidence.

It:

* Extracts individual claims
* Checks claims against evidence
* Measures semantic support
* Detects contradictions
* Identifies unsupported claims
* Provides evidence
* Provides reasoning

Implementation:

`app/agents/hallucination_agent.py`

---

## M2.4 Benchmark & Agent Validation

The Milestone 2 evaluation set is stored in:

`data/milestone2_evaluation_set.json`

It covers:

* Correct responses
* Incorrect responses
* Partially correct responses
* Irrelevant responses
* Incomplete responses
* Unsupported claims
* Contradictory responses

Tests:

`tests/test_milestone2_evaluation.py`

---

# Milestone 3 — Completeness, Verdict, Results & Batch Evaluation

Milestone 3 extends the system from individual evaluation agents to complete response evaluation and batch processing.

---

## M3.1 Completeness Judge Agent

The Completeness Judge Agent determines whether an AI response sufficiently covers the expected aspects of a question.

It:

* Identifies expected aspects
* Compares the response against those aspects
* Identifies addressed aspects
* Identifies partially addressed aspects
* Identifies missing aspects
* Uses a reference answer when available
* Uses retrieved evidence when a reference answer is unavailable
* Produces a completeness score
* Provides reasoning

Implementation:

`app/agents/completeness_agent.py`

Tests:

`tests/test_milestone3_completeness.py`

The completeness agent was tested with:

* Fully complete responses
* Partially complete responses
* Substantially incomplete responses
* RAG evidence
* No reference/evidence

---

## M3.2 Weighted Evaluation & Verdict

The system combines the four evaluation dimensions using a weighted scoring model.

### Current Weights

| Dimension            | Weight |
| -------------------- | -----: |
| Relevance            |    25% |
| Accuracy             |    25% |
| Hallucination Safety |    25% |
| Completeness         |    25% |

The weighted overall score is calculated from all four dimensions.

### Verdict Categories

|   Overall Score | Verdict           |
| --------------: | ----------------- |
|       `>= 0.70` | Pass              |
| `0.40 – < 0.70` | Needs Improvement |
|        `< 0.40` | Fail              |

A critical contradiction detected between the AI response and available evidence can also result in a **Fail** verdict.

Implementation:

* `app/core/scoring.py`
* `app/evaluation/verdict.py`
* `app/evaluation/orchestrator.py`

Tests:

`tests/test_milestone3_verdict.py`

---

## M3.3 Evaluation Results Display

The Streamlit interface displays the complete evaluation result.

### Individual Scores

* Relevance
* Accuracy
* Hallucination Safety
* Completeness
* Overall Score

### Evaluation Reasoning

The UI displays reasoning for each evaluation dimension.

### Accuracy Evidence

The system displays supporting evidence used for accuracy evaluation.

### Hallucination Details

The UI displays:

* Unsupported claims
* Hallucinated claims
* Contradictions
* Evidence

### Completeness Details

The UI displays:

* Addressed aspects
* Partially addressed aspects
* Missing aspects

### Final Result

The system displays:

* Overall score
* Verdict
* Verdict reason
* Validation record ID
* Retrieved evidence

Implementation:

`frontend/final_ui.py`

---

# M3.4 Batch CSV Evaluation

Milestone 3.4 adds batch evaluation of multiple question-answer records.

Users can upload a CSV containing:

* `question` — required
* `ai_response` — required
* `reference_answer` — optional
* `source_document` — optional

Example:

```csv
question,ai_response,reference_answer,source_document
"What is the capital of France?","The capital of France is Paris.","Paris is the capital city of France.",""
"What is 2 plus 2?","2 plus 2 equals 4.","2 plus 2 equals 4.",""
```

Implementation:

`app/batch_evaluator.py`

The Streamlit batch interface is implemented in:

`frontend/final_ui.py`

---

## Batch Validation

The batch module validates:

* Required CSV columns
* Missing questions
* Missing AI responses
* Optional reference answers
* Optional source documents
* Malformed CSV files

Invalid records are reported separately and do not stop the evaluation of valid records.

---

## Batch Evaluation Results

The batch results table displays:

* Row number
* Question
* Response ID
* Relevance score
* Accuracy score
* Hallucination Safety score
* Completeness score
* Overall score
* Verdict

---

## Batch Detail Inspection

Users can select an individual batch result and inspect:

* Relevance reasoning
* Accuracy reasoning
* Supporting evidence
* Hallucination reasoning
* Unsupported claims
* Contradictions
* Completeness reasoning
* Addressed aspects
* Partially addressed aspects
* Missing aspects

---

## Batch Aggregated Statistics

The system calculates:

* Average Relevance score
* Average Accuracy score
* Average Hallucination Safety score
* Average Completeness score
* Average Overall score
* Pass count
* Needs Improvement count
* Fail count
* Hallucination-risk record count

---

## Batch Testing

M3.4 was tested using:

* Valid CSV files
* Invalid records
* Missing required columns
* Optional reference/source fields
* Malformed CSV files
* Small batch files
* 10-record batch files

The 10-record batch test successfully processed all 10 records.

---

# Technology Stack

The project uses:

* **Python**
* **FastAPI**
* **Pydantic**
* **Streamlit**
* **Hugging Face Datasets**
* **Sentence Transformers**
* **NumPy**
* **scikit-learn**
* **Pytest**
* **Pandas**
* **CSV**
* **JSON / JSONL**
* **Git / GitHub**
* **Agile methodology**

---

# Knowledge Base & Benchmark Sources

The project uses benchmark datasets from Hugging Face:

* TruthfulQA
* SQuAD

The benchmark manifest is stored in:

`data/benchmark_manifest.json`

The knowledge-base pipeline is:

```text
Benchmark Dataset
       |
       v
Normalization
       |
       v
Chunking
       |
       v
Embedding Generation
       |
       v
Vector Index
       |
       v
Semantic Retrieval
```

The default embedding model is:

`sentence-transformers/all-MiniLM-L6-v2`

A deterministic HashingVectorizer fallback is available for local/CI execution when required.

---

# Setup on Windows PowerShell

Navigate to the project:

```powershell
cd "C:\Users\Sanjana\OneDrive\Desktop\AI_Response_Validation_System"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# Build the Knowledge Base

```powershell
python -m app.knowledge_base.ingest --mode benchmarks --squad-limit 200 --truthfulqa-limit 200
```

---

# Validate Retrieval

```powershell
python scripts/validate_retrieval.py
```

This generates:

`data/processed/retrieval_report.json`

---

# Run the Backend

```powershell
uvicorn app.main:app --reload
```

Backend:

`http://127.0.0.1:8000`

Swagger API documentation:

`http://127.0.0.1:8000/docs`

---

# Run the Streamlit Interface

Open another PowerShell terminal:

```powershell
cd "C:\Users\Sanjana\OneDrive\Desktop\AI_Response_Validation_System"
```

Activate the environment if required:

```powershell
.\venv\Scripts\Activate.ps1
```

Run:

```powershell
streamlit run frontend\final_ui.py
```

The interface normally opens at:

`http://localhost:8501`

---

# Single Response Evaluation

The interface accepts:

* User Question
* AI Generated Response
* Reference / Evidence
* Source Document / Reference Material

The response is processed through:

```text
Question + AI Response
          |
          v
     Retrieval
          |
          v
    Relevance Agent
    Accuracy Agent
    Hallucination Agent
    Completeness Agent
          |
          v
    Weighted Scoring
          |
          v
       Verdict
```

---

# Batch CSV Evaluation

The Streamlit interface provides:

**📦 Batch CSV Evaluation**

Upload a CSV containing multiple question-answer records.

The system:

1. Reads the CSV.
2. Validates required fields.
3. Processes each valid record.
4. Continues when an individual record is invalid.
5. Displays individual evaluation results.
6. Allows detailed inspection.
7. Calculates aggregated statistics.

---

# Testing

Run the complete test suite:

```powershell
pytest -v
```

### Current Test Result

```text
34 passed, 4 warnings
```

All 34 automated tests pass successfully.

The warnings are dependency/framework deprecation warnings and do not represent test failures.

### Test Coverage Includes

* Relevance Agent
* Accuracy Agent
* Hallucination Detection Agent
* Benchmark normalization
* Milestone 2 evaluation
* Completeness Agent
* Weighted scoring
* Verdict categories
* Contradiction handling
* Pipeline routing
* Retrieval
* Input validation
* Batch CSV evaluation
* Invalid batch records
* Missing required columns
* Optional reference/source fields

---

# Milestone 3.4 Batch Tests

Dedicated M3.4 tests are located in:

`tests/test_milestone3_batch.py`

The tests verify:

1. Valid batch evaluation
2. Invalid row does not stop the batch
3. Missing required column handling
4. Optional reference/source fields

The dedicated M3.4 test suite passes:

```text
4 passed
```

---

# Evaluation Scoring

The system uses four evaluation dimensions:

* Relevance — 25%
* Accuracy — 25%
* Hallucination Safety — 25%
* Completeness — 25%

The weighted mean produces the overall evaluation score.

The current development thresholds are:

```text
Overall Score >= 0.70
        |
        v
      Pass

0.40 <= Overall Score < 0.70
        |
        v
Needs Improvement

Overall Score < 0.40
        |
        v
      Fail
```

These are development thresholds and should not be interpreted as calibrated production accuracy.

---

# Agile Working Model

The project follows Agile development practices.

The `Agile/` directory contains:

* Product Backlog
* Sprint Backlog
* Stand-up records
* Retrospection
* Defect Tracker
* Unit Test Plan
* Milestone documentation

The workflow is:

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

A story is considered complete after implementation, acceptance criteria, testing, documentation, and review evidence have been addressed.

---

# Current Project Status

| Milestone     | Requirement                           | Status               |
| ------------- | ------------------------------------- | -------------------- |
| M1            | Foundation & Evaluation Understanding | Completed            |
| M2.1          | Relevance Judge Agent                 | Completed            |
| M2.2          | Accuracy Judge Agent                  | Completed            |
| M2.3          | Hallucination Detection Agent         | Completed            |
| M2.4          | Benchmark & Agent Validation          | Completed            |
| M3.1          | Completeness Judge Agent              | Completed            |
| M3.2          | Weighted Evaluation & Verdict         | Completed            |
| M3.3          | Evaluation Results Display            | Completed            |
| M3.4          | Batch CSV Evaluation                  | Completed            |
| Testing       | Full automated test suite             | 34/34 Passed         |
| Batch Testing | 10-record CSV test                    | Completed            |
| Agile         | Documentation & testing artifacts     | In progress / review |

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
* Larger-scale batch processing
* Improved evaluation visualization

# Milestone 4 — Evaluation Scoring Dashboard, Reporting & End-to-End Validation

Milestone 4 extends the AI Response Validation System from individual and batch evaluation into a complete evaluation analytics and reporting system.

The milestone focuses on:

* Evaluation scoring dashboard
* Verdict distribution
* Average dimension scores
* Score distributions
* Hallucination statistics
* Missing-information statistics
* Structured PDF reporting
* Single evaluation end-to-end validation
* Batch evaluation end-to-end validation
* Batch-to-dashboard integration

---

## M4.1 Evaluation Scoring Dashboard

The Streamlit application provides a dedicated **Dashboard** mode for analyzing stored evaluation results.

The dashboard displays:

* Total evaluations
* Passed evaluations
* Needs Improvement evaluations
* Failed evaluations
* Verdict percentages
* Average Relevance score
* Average Accuracy score
* Average Hallucination Safety score
* Average Completeness score
* Recent evaluation results

The dashboard reads stored evaluation records and calculates statistics dynamically.

Implementation:

```text
frontend/final_ui.py
data/submissions.jsonl
data/batch_evaluation_results.csv
```

---

## M4.2 Verdict Distribution

The dashboard groups evaluation results into three major verdict categories:

| Verdict Category  | Meaning                                                |
| ----------------- | ------------------------------------------------------ |
| Pass              | Evaluation satisfies the configured quality threshold  |
| Needs Improvement | Evaluation requires improvement                        |
| Fail              | Evaluation does not satisfy the required quality level |

The dashboard displays the number and percentage of evaluations belonging to each category.

The system also recognizes equivalent verdict labels such as `VALID`, `WARNING`, `BLOCKED`, `FAIL`, and related evaluation outcomes when calculating dashboard statistics.

---

## M4.3 Average Dimension Scores

The dashboard calculates the average score for each evaluation dimension:

| Dimension            | Weight |
| -------------------- | -----: |
| Relevance            |    25% |
| Accuracy             |    25% |
| Hallucination Safety |    25% |
| Completeness         |    25% |

The dashboard presents these values as percentage-based score cards.

The overall score is calculated using the weighted evaluation dimensions.

---

## M4.4 Score Distribution

The dashboard provides score-distribution visualizations for the four evaluation dimensions.

The distributions allow users to identify:

* High-scoring evaluations
* Low-scoring evaluations
* Variation between evaluation dimensions
* Areas requiring improvement

The dashboard uses the stored evaluation records to generate these statistics dynamically.

---

## M4.5 Hallucination Statistics

The dashboard provides hallucination-related statistics to help identify potentially unsafe AI responses.

The dashboard reports:

* Hallucination-safe evaluation count
* Hallucination-flagged evaluation count
* Hallucination safety score
* Unsupported-claim information
* Contradiction-related information
* Hallucination trends across stored evaluations

These statistics are derived from the Hallucination Detection Agent results.

---

## M4.6 Missing-Information Statistics

The dashboard also analyzes completeness-related missing information.

It reports:

* Evaluations containing missing information
* Total missing aspects
* Partially addressed aspects

This allows users to identify responses that may be factually related to the question but do not provide sufficient coverage.

---

## M4.7 Structured PDF Export

Milestone 4 adds a structured PDF reporting feature.

Users can generate a PDF report from the Dashboard.

The report contains:

* Evaluation summary
* Total evaluation count
* Verdict statistics
* Average dimension scores
* Overall score information
* Flagged evaluation responses
* Evaluation questions
* Dimension-level information
* Recommendations

The generated report can be downloaded directly from the Streamlit interface.

Implementation:

```text
frontend/final_ui.py
ReportLab
```

The generated report uses the filename:

```text
AI_Response_Validation_Milestone4_Report.pdf
```

---

## M4.8 Single Evaluation End-to-End Testing

The complete Single Evaluation workflow was tested from the Streamlit interface through the backend evaluation pipeline and persistent storage.

The workflow was verified as:

```text
User Input
    |
    v
Streamlit Interface
    |
    v
FastAPI Evaluation API
    |
    v
Input Validation
    |
    v
Evaluation Orchestrator
    |
    +--> Relevance
    +--> Accuracy
    +--> Hallucination
    +--> Completeness
    |
    v
Weighted Scoring
    |
    v
Verdict
    |
    v
Stored Evaluation Record
    |
    v
Dashboard
```

A test evaluation was successfully processed and stored with a validation record ID.

---

## M4.9 Batch Evaluation End-to-End Testing

The complete Batch Evaluation workflow was also tested.

The workflow was verified as:

```text
CSV Upload
    |
    v
CSV Validation
    |
    v
Batch Evaluation
    |
    v
Individual AI Response Evaluation
    |
    v
Evaluation Results
    |
    v
CSV Results
    |
    v
Dashboard Statistics
```

A 10-record batch CSV was successfully processed.

The batch results were written to:

```text
data/batch_evaluation_results.csv
```

The processed batch results were also reflected in the Dashboard statistics.

---

## M4.10 Batch-to-Dashboard Integration

The Batch Evaluation module and Dashboard were tested together.

After processing a batch:

1. Multiple records are evaluated.
2. Results are stored.
3. Dashboard statistics are recalculated.
4. Total evaluation count is updated.
5. Verdict counts are updated.
6. Average dimension scores are updated.
7. Hallucination statistics are updated.
8. Missing-information statistics are updated.

This verifies the integration between evaluation, persistent storage, batch processing, and dashboard analytics.

---

## M4.11 Milestone 4 Validation Status

| Requirement                                   | Status      |
| --------------------------------------------- | ----------- |
| Evaluation Scoring Dashboard                  | Completed   |
| Pass / Needs Improvement / Fail visualization | Completed   |
| Average dimension scores                      | Completed   |
| Score distributions                           | Completed   |
| Hallucination statistics                      | Completed   |
| Hallucination trends                          | Completed   |
| Missing-information statistics                | Completed   |
| Structured PDF export                         | Completed   |
| Single Evaluation E2E testing                 | Completed   |
| Batch Evaluation E2E testing                  | Completed   |
| Batch-to-Dashboard integration                | Completed   |
| Final two-AI-system demonstration             | Pending     |
| Final documentation/report                    | In progress |

---

## M4 Implementation Files

Important Milestone 4 functionality is implemented primarily in:

```text
frontend/final_ui.py
data/submissions.jsonl
data/batch_evaluation_results.csv
```

The PDF reporting functionality uses:

```text
ReportLab
```

---

# Updated Project Status

The project currently contains four development milestones:

```text
Milestone 1
Foundation & Evaluation Understanding
        |
        v
Milestone 2
Evaluation Agents & Validation
        |
        v
Milestone 3
Completeness, Verdict & Batch Evaluation
        |
        v
Milestone 4
Dashboard, Reporting & End-to-End Validation
```

Milestones 1, 2, 3 and the core implementation of Milestone 4 have been completed.

The remaining final activities are:

1. Final documentation
2. Demonstration using at least two AI systems
3. Final project review
4. Final Git commit and push

