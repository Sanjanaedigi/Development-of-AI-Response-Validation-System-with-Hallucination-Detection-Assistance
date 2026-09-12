# Milestone 1 Agent Responsibilities

| Component | Responsibility | Input | Output |
|---|---|---|---|
| Evaluation Orchestrator | Coordinates retrieval and all judges | Question, response, evidence | Structured evaluation |
| Relevance Judge Agent | Checks question-response alignment | Question, response, evidence | Score + explanation |
| Accuracy Judge Agent | Checks factual support | Response, evidence/reference | Score + explanation |
| Hallucination Detection Agent | Checks unsupported claims | Response, evidence/reference | Safety score + explanation |
| Completeness Judge Agent | Checks coverage of reference information | Response, reference | Score + explanation |
| Verdict Agent/Module | Combines scores and applies threshold | Four scores | Verdict + reason |
