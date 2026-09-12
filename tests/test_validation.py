from pydantic import ValidationError
import pytest
from app.schemas import EvaluationRequest

def test_blank_question_rejected():
    with pytest.raises(ValidationError): EvaluationRequest(question=" ", ai_response="valid")

def test_blank_response_rejected():
    with pytest.raises(ValidationError): EvaluationRequest(question="valid", ai_response=" ")

def test_optional_source_document():
    req=EvaluationRequest(question="Q", ai_response="A", source_document="document")
    assert req.evidence_text()=="document"
