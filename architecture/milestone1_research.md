# Milestone 1.1 — Research & Technical Understanding

## 1. LLM evaluation workflow
A response-evaluation workflow accepts a question, generated answer, and optional evidence; retrieves relevant reference material; evaluates the answer on multiple dimensions; aggregates scores; and returns a structured verdict with explanations.

## 2. Evaluation dimensions
- **Relevance:** whether the response directly addresses the question.
- **Accuracy/Factuality:** whether claims agree with the supplied reference evidence.
- **Faithfulness/Hallucination safety:** whether claims are supported by retrieved evidence rather than invented.
- **Completeness:** whether important information in the reference is covered.

Milestone 1 uses deterministic baseline judges so the repository is reproducible without paid APIs. Later milestones can replace the judge internals with LLM-as-a-Judge prompts while keeping the same API contract.

## 3. RAG architecture
Retrieval-Augmented Generation separates evidence retrieval from generation/evaluation. The project follows:

`Question -> embedding -> vector similarity search -> top-k evidence -> evaluation agents -> scores/verdict`

The knowledge base stores normalized question, answer, source, dataset and chunk metadata.

## 4. Embeddings and vector search
The default embedding backend is `sentence-transformers/all-MiniLM-L6-v2`. It produces dense text vectors and cosine similarity is used for retrieval. A HashingVectorizer fallback is included for offline/CI execution. The fallback is explicitly treated as a development fallback, not the preferred semantic embedding path.

Chunking uses normalized whitespace and configurable character chunks (`700` characters with `100` overlap). This provides reproducible context windows while preserving metadata for traceability.

## 5. LLM-as-a-Judge
LLM-as-a-Judge asks a language model to score a response against a rubric and evidence. Benefits include flexible reasoning over paraphrases; risks include judge bias, prompt sensitivity, and correlated errors. Milestone 1 therefore defines prompt contracts in `app/evaluation/prompts.py` but uses deterministic judges for reproducibility.

## 6. RAGAS and TruLens
**RAGAS** is a framework for evaluating RAG systems with metrics such as faithfulness, answer relevance and context relevance. **TruLens** provides evaluation/observability workflows for LLM applications and feedback functions. They are studied as reference frameworks in Milestone 1; the project does not depend on them yet so the baseline remains lightweight and locally runnable.

## 7. Public QA benchmarks
### TruthfulQA
TruthfulQA is designed to test whether models avoid common misconceptions and false answers. The Hugging Face `truthfulqa/truthful_qa` dataset exposes a `generation` configuration with question, best answer, correct answers, incorrect answers and source fields.

### SQuAD
SQuAD is a reading-comprehension benchmark with question, context, answer span and article metadata. The Hugging Face `rajpurkar/squad` dataset provides train and validation splits.

The ingestion module samples bounded amounts of both datasets, cleans them, standardizes them into one schema, chunks the reference text, and indexes embeddings. Raw benchmark downloads are intentionally not committed to GitHub; they are reproducible using the ingestion command.

## 8. Scoring strategy
Four dimensions are equally weighted in Milestone 1:

| Dimension | Weight | Range |
|---|---:|---:|
| Relevance | 25% | 0–1 |
| Accuracy | 25% | 0–1 |
| Hallucination safety | 25% | 0–1 |
| Completeness | 25% | 0–1 |

Overall score is the weighted mean. The baseline pass threshold is `0.70`. These are explicit Milestone 1 baseline decisions and are intended to be calibrated in later milestones.

## 9. Technology choices
- Python — evaluation and RAG implementation
- FastAPI — backend/API
- Pydantic — request validation and data models
- Streamlit — evaluation interface
- Hugging Face Datasets — TruthfulQA/SQuAD ingestion
- Sentence Transformers — dense embeddings
- NumPy/scikit-learn — vector math and offline fallback
- JSONL/JSON — transparent local persistence for Milestone 1
- Pytest — automated tests
- GitHub + Agile artifacts — version control and sprint tracking

## 10. Proposed implementation strategy
Milestone 1 establishes the contract and baseline. Milestone 2 can add production vector databases, LLM judges, calibration, batch evaluation, richer reports, observability and CI/CD without changing the input/output API contract.
