from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback

from app.schemas import EvaluationRequest, EvaluationResponse
from app.evaluation.orchestrator import evaluate_submission
from app.database.storage import save_submission, utc_now
from app.knowledge_base.ingest import build_seed_kb
from app.core.config import KB_FILE, EMBEDDING_BACKEND


app = FastAPI(
    title="AI Response Validation System",
    version="1.0.0",
    description=(
        "Milestone 1 LLM response evaluation "
        "and RAG knowledge-base API."
    )
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup():

    if not KB_FILE.exists():
        build_seed_kb()


@app.get("/")
def root():

    return {
        "message": "AI Response Validation System API is running."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/version")
def version():

    return {
        "version": "1.0.1",
        "embedding_backend": EMBEDDING_BACKEND
    }


@app.post(
    "/api/v1/evaluate",
    response_model=EvaluationResponse,
    status_code=201
)
def evaluate(request: EvaluationRequest):

    try:
        result = evaluate_submission(
            question=request.question,
            ai_response=request.ai_response,
            reference_evidence=request.evidence_text()
        )

        try:
            save_submission(
                {
                    "timestamp": utc_now(),
                    **result
                }
            )
        except Exception as storage_err:
            print("Storage save warning:", storage_err)

        return result

    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {exc}"
        )