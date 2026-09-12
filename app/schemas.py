from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator


class EvaluationRequest(BaseModel):

    # Required fields
    question: str = Field(..., min_length=1)
    ai_response: str = Field(..., min_length=1)

    # Optional evidence fields
    reference_evidence: Optional[str] = None
    source_document: Optional[str] = None

    @field_validator("question", "ai_response")
    @classmethod
    def reject_blank(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty or whitespace."
            )

        return value

    @field_validator(
        "reference_evidence",
        "source_document"
    )
    @classmethod
    def normalize_optional(cls, value):

        if value is None:
            return None

        value = value.strip()

        return value or None

    def evidence_text(self):

        # User-provided evidence has priority.
        if self.reference_evidence:
            return self.reference_evidence

        # If reference evidence is not provided,
        # use the optional source document.
        if self.source_document:
            return self.source_document

        # If neither is provided, return None.
        # The orchestrator will use the Knowledge Base.
        return None


class AgentResult(BaseModel):

    score: float
    explanation: str

    details: Dict[str, Any] = Field(
        default_factory=dict
    )


class EvaluationResponse(BaseModel):

    submission_id: str

    relevance: AgentResult
    accuracy: AgentResult
    hallucination: AgentResult
    completeness: AgentResult

    overall_score: float

    verdict: str
    verdict_reason: str

    retrieved_evidence: List[Dict[str, Any]] = Field(
        default_factory=list
    )