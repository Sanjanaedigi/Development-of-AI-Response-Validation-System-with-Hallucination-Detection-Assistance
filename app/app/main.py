from fastapi import FastAPI, HTTPException, status
from .schemas import EvaluationSubmission, EvaluationResultResponse
from .knowledge_base.vector_store import LocalVectorKnowledgeBase
from .core.graph import compiled_funnel
import uuid

app = FastAPI(title="LLM Multi-Agent Funnel Auditor Engine", version="1.0.0")
vdb = LocalVectorKnowledgeBase()

@app.post("/api/v1/evaluate", response_model=EvaluationResultResponse, status_code=status.HTTP_201_CREATED)
async def run_audit_evaluation(payload: EvaluationSubmission):
    if not payload.question.strip() or not payload.ai_response.strip():
        raise HTTPException(status_code=422, detail="Inputs cannot be whitespace characters.")

    # RAG Architecture Data Retrieval
    retrieved_facts = vdb.semantic_context_lookup(payload.question, top_k=2)
    context_str = " ".join(retrieved_facts)
    if payload.source_document:
        context_str += f" | Manual Source Document Context: {payload.source_document}"
    if payload.reference_answer:
        context_str += f" | Gold Truth Context: {payload.reference_answer}"

    # Execute LangGraph sequential workflow
    graph_input = {
        "question": payload.question,
        "ai_response": payload.ai_response,
        "context": context_str,
        "scores": {},
        "reasoning": {}
    }
    
    output_state = compiled_funnel.invoke(graph_input)
    
    # Verdict Agent Processing Layer
    
    scores = output_state["scores"]
    
    verdict_flag = output_state.get(
        "verdict",
        "FILTER BLOCKED"
    )
    
    return {
        "submission_id": str(uuid.uuid4()),
        "status": "PROCESSED",
        "scores": scores,
        "verdict": verdict_flag,
        "reasoning": output_state["reasoning"]
    }

