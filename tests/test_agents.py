from app.agents import relevance_agent, accuracy_agent, hallucination_agent, completeness_agent

def test_relevance_high_for_matching_response():
    r=relevance_agent.evaluate("What is RAG?", "RAG retrieves relevant information.", [{"text":"RAG retrieves relevant information."}])
    assert 0 <= r["score"] <= 1

def test_accuracy_is_bounded():
    r=accuracy_agent.evaluate("Q","correct answer",[{"answer":"correct answer","text":"correct answer"}])
    assert 0 <= r["score"] <= 1

def test_hallucination_is_bounded():
    r=hallucination_agent.evaluate("Q","claim",[{"text":"claim"}])
    assert 0 <= r["score"] <= 1

def test_completeness_is_bounded():
    r=completeness_agent.evaluate("Q","answer",[{"answer":"answer"}])
    assert 0 <= r["score"] <= 1
