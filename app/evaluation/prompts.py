"""Prompt contracts documented in Milestone 1 for the later LLM-as-a-Judge stage."""
BASE_SYSTEM = "Return a score from 0 to 1 and a concise evidence-based explanation. Do not invent facts."
PROMPTS = {
    "relevance": "Does the AI response directly address the user's question?",
    "accuracy": "Are the factual claims supported by the supplied reference evidence?",
    "hallucination": "Which claims are unsupported, contradicted, or fabricated relative to the evidence?",
    "completeness": "Does the response cover the important information present in the available evidence?",
}
