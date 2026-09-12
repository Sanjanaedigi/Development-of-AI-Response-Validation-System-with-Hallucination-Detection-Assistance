from uuid import uuid4

from app.agents import (
    relevance_agent,
    accuracy_agent,
    hallucination_agent,
    completeness_agent
)

from app.core.scoring import overall_score, verdict
from app.knowledge_base.vector_store import semantic_search


def evaluate_submission(
    question,
    ai_response,
    reference_answer=None,
    reference_evidence=None
):

    # -------------------------------------------------
    # STEP 1: Retrieve evidence from Knowledge Base
    # -------------------------------------------------

    retrieved = semantic_search(
        question,
        top_k=5
    )
    retrieved = [
    item for item in retrieved
    if item.get("similarity", 0) >= 0.30
    ]

    # -------------------------------------------------
    # STEP 2: Add user supplied evidence if available
    # -------------------------------------------------

    if reference_evidence:

        retrieved.insert(
            0,
            {
                "document_id": "user_reference",
                "chunk_id": "user_reference_001",
                "dataset": "User supplied",
                "source": "User supplied",
                "text": reference_evidence,
                "similarity": 1.0,
                "question": question
            }
        )

    # -------------------------------------------------
    # STEP 3: Run evaluation agents
    # -------------------------------------------------

    results = {

        "relevance": relevance_agent.evaluate(
            question,
            ai_response,
            retrieved
        ),

        "accuracy": accuracy_agent.evaluate(
            question,
            ai_response,
            retrieved
        ),

        "hallucination": hallucination_agent.evaluate(
            question,
            ai_response,
            retrieved
        ),

        "completeness": completeness_agent.evaluate(
            question,
            ai_response,
            retrieved
        )
    }

    # -------------------------------------------------
    # STEP 4: Calculate final score
    # -------------------------------------------------

    score = overall_score(results)

    final_verdict, reason = verdict(score)

    # -------------------------------------------------
    # STEP 5: Return final result
    # -------------------------------------------------

    return {

        "submission_id":
            "VAL-" + uuid4().hex[:10].upper(),

        **results,

        "overall_score": score,

        "verdict": final_verdict,

        "verdict_reason": reason,

        "retrieved_evidence": retrieved
    }