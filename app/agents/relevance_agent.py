from app.agents.common import overlap

def evaluate(question, response, evidence):
    q_to_r = overlap(question, response)
    ev = " ".join(x["text"] for x in evidence)
    evidence_support = overlap(response, ev) if ev else 0
    score = min(1.0, 0.75*q_to_r + 0.25*evidence_support)
    explanation = (
        "The response addresses important terms from the question."
        if score >= 0.70 else
        "The response has limited overlap with the question and may not directly address it."
    )
    return {"score": round(score, 4), "explanation": explanation,
            "details": {"question_response_overlap": round(q_to_r, 4)}}
