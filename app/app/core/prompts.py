RELEVANCE_PROMPT = """You are an expert Relevance Judge Agent.
Task: Evaluate if the AI response directly addresses the user's question.

User Question: {question}
AI Response: {ai_response}

Output exactly in this layout:
SCORE: [Provide score from 0.0 to 1.0]
REASONING: [1 concise sentence explanation]"""

HALLUCINATION_PROMPT = """You are an expert Hallucination Detection Agent.
Task: Verify if the AI response statements are strictly grounded in the provided Context.

Context: {context}
AI Response: {ai_response}

Output exactly in this layout:
SCORE: [Provide score from 0.0 to 1.0]
REASONING: [1 concise sentence explanation]"""

COMPLETENESS_PROMPT = """You are an expert Completeness Judge Agent.
Task: Assess if the AI response misses any core requirements of the question.

User Question: {question}
AI Response: {ai_response}

Output exactly in this layout:
SCORE: [Provide score from 0.0 to 1.0]
REASONING: [1 concise sentence explanation]"""

