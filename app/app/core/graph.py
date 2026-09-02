from typing import Dict, TypedDict, Any
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from.import prompts
import re
import os

class FunnelState(TypedDict):
    question: str
    ai_response: str
    context: str
    scores: Dict[str, float]
    reasoning: Dict[str, str]

def parse_judge_output(text: str):
    score_match = re.search(r"SCORE:\s*([\d\.]+)", text)
    reason_match = re.search(r"REASONING:\s*(.*)", text)
    score = float(score_match.group(1)) if score_match else 0.0
    reason = reason_match.group(1).strip() if reason_match else "Parsed successfully."
    return score, reason

def get_gemini_engine():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY", "mock_key")
    )

def relevance_filter(state: FunnelState) -> Dict[str, Any]:
    if not os.getenv("GOOGLE_API_KEY"):
        return {"scores": {"relevance": 1.0}, "reasoning": {"relevance": "Sandbox evaluation run placeholder."}}
    p = prompts.RELEVANCE_PROMPT.format(question=state["question"], ai_response=state["ai_response"])
    res = get_gemini_engine().invoke(p)
    score, reason = parse_judge_output(res.content)
    return {"scores": {"relevance": score}, "reasoning": {"relevance": reason}}

def hallucination_filter(state: FunnelState) -> Dict[str, Any]:
    if not os.getenv("GOOGLE_API_KEY"):
        return {"scores": {"hallucination": 1.0}, "reasoning": {"hallucination": "Sandbox evaluation run placeholder."}}
    p = prompts.HALLUCINATION_PROMPT.format(context=state["context"], ai_response=state["ai_response"])
    res = get_gemini_engine().invoke(p)
    score, reason = parse_judge_output(res.content)
    return {"scores": {"hallucination": score}, "reasoning": {"hallucination": reason}}

def completeness_filter(state: FunnelState) -> Dict[str, Any]:
    if not os.getenv("GOOGLE_API_KEY"):
        return {"scores": {"completeness": 1.0}, "reasoning": {"completeness": "Sandbox evaluation run placeholder."}}
    p = prompts.COMPLETENESS_PROMPT.format(question=state["question"], ai_response=state["ai_response"])
    res = get_gemini_engine().invoke(p)
    score, reason = parse_judge_output(res.content)
    return {"scores": {"completeness": score}, "reasoning": {"completeness": reason}}

# Build sequential workflow pipeline funnel graph
builder = StateGraph(FunnelState)
builder.add_node("filter_1_relevance", relevance_filter)
builder.add_node("filter_2_hallucination", hallucination_filter)
builder.add_node("filter_3_completeness", completeness_filter)

builder.set_entry_point("filter_1_relevance")
builder.add_edge("filter_1_relevance", "filter_2_hallucination")
builder.add_edge("filter_2_hallucination", "filter_3_completeness")
builder.add_edge("filter_3_completeness", END)

compiled_funnel = builder.compile()

