# Agent Responsibilities - AI Response Validation System

## Evaluation Components

| Component | Responsibility | Input | Output |
|---|---|---|---|
| Evaluation Orchestrator | Coordinates evidence retrieval and execution of all evaluation agents | Question, AI response, reference answer/evidence | Structured evaluation results |
| Relevance Judge Agent | Determines whether the AI response is relevant to the user's question | Question, AI response, retrieved evidence | Relevance score + explanation |
| Accuracy Judge Agent | Checks factual correctness against reference answers or retrieved evidence | Question, AI response, evidence/reference | Accuracy score + evidence + explanation |
| Hallucination Detection Agent | Identifies unsupported or contradicted claims | Question, AI response, retrieved evidence | Hallucination safety score + unsupported claims + explanation |
| Completeness Judge Agent | Determines whether the response addresses the relevant aspects of the question | Question, AI response, evidence/reference | Completeness score + addressed/missing aspects + explanation |
| Weighted Scoring Module | Combines the four normalized agent scores using configured weights | Four agent scores | Overall weighted score |
| Verdict Module | Determines the final evaluation category and reason | Agent results + overall score | Pass / Needs Improvement / Fail + reason |
| Submission Storage | Stores structured evaluation results for individual evaluations | Evaluation result | Stored submission with unique ID |
| Batch Evaluation Module | Processes multiple question-response pairs from CSV files | CSV rows | Individual results + batch statistics |
| Streamlit Results UI | Presents evaluation results to the user | Structured evaluation results | Scores, reasoning, evidence and verdict |

## Evaluation Agents

### 1. Relevance Judge Agent

**Purpose:**  
Determine whether the AI-generated response addresses the user's question.

**Responsibilities:**
- Compare the question with the AI response.
- Identify relevant and unrelated content.
- Consider retrieved evidence when available.
- Produce a normalized relevance score.
- Provide reasoning for the score.

**Output includes:**
- Relevance score
- Explanation
- Supporting evaluation details

---

### 2. Accuracy Judge Agent

**Purpose:**  
Determine whether factual claims in the AI response are supported by the available reference information.

**Responsibilities:**
- Compare the AI response with a reference answer when available.
- Compare claims with retrieved evidence when a reference answer is not available.
- Identify correct and unsupported factual statements.
- Provide evidence supporting the evaluation.
- Produce a normalized accuracy score.

**Output includes:**
- Accuracy score
- Explanation
- Evidence
- Claim-level evaluation details

---

### 3. Hallucination Detection Agent

**Purpose:**  
Identify claims that are unsupported or contradicted by the available evidence.

**Responsibilities:**
- Compare response claims against retrieved evidence.
- Identify unsupported claims.
- Detect contradictions with the available reference information.
- Distinguish supported information from unsupported information.
- Produce a hallucination safety score.

**Output includes:**
- Hallucination safety score
- Explanation
- Unsupported claims
- Contradictions
- Supporting evidence

---

### 4. Completeness Judge Agent

**Purpose:**  
Determine whether the AI response sufficiently covers the relevant aspects of the question.

**Responsibilities:**
- Identify expected aspects or requirements.
- Compare the response against those aspects.
- Identify addressed aspects.
- Identify partially addressed aspects.
- Identify missing or omitted aspects.
- Use the reference answer when available.
- Use retrieved evidence when a reference answer is unavailable.

**Output includes:**
- Completeness score
- Addressed aspects
- Partially addressed aspects
- Missing aspects
- Aspect-level evaluation
- Reasoning

---

## Weighted Scoring Module

The Weighted Scoring Module combines the four normalized evaluation dimensions.

| Dimension | Weight |
|---|---:|
| Relevance | 25% |
| Accuracy | 25% |
| Hallucination Safety | 25% |
| Completeness | 25% |

The overall score is calculated from the weighted combination of the four dimension scores.

---

## Verdict Module

The Verdict Module converts the overall evaluation into a final category.

### Verdict Categories

| Overall Score | Verdict |
|---|---|
| 70% or above | Pass |
| 40% to below 70% | Needs Improvement |
| Below 40% | Fail |

A critical contradiction or severe hallucination can also cause a **Fail** verdict even when the weighted score alone would otherwise be higher.

The Verdict Module also generates a consolidated reason explaining the final result.

---

## Evaluation Orchestrator

The Evaluation Orchestrator is responsible for coordinating the complete validation pipeline.

### Processing Flow

1. Receive the question and AI response.
2. Receive optional reference answer/evidence.
3. Retrieve relevant evidence from the knowledge base.
4. Run the Relevance Judge.
5. Run the Accuracy Judge.
6. Run the Hallucination Detection Judge.
7. Run the Completeness Judge.
8. Pass the four results to the Weighted Scoring Module.
9. Generate the final verdict.
10. Store the structured evaluation result.
11. Return the result to the user interface.

---

## Batch Evaluation Module

The Batch Evaluation Module supports evaluation of multiple records from CSV files.

### Required Fields

- `question`
- `ai_response`

### Optional Fields

- `reference_answer`
- `source_document`

### Responsibilities

- Validate CSV structure.
- Validate required columns.
- Process valid rows individually.
- Identify invalid rows without stopping the entire batch.
- Run each valid row through the Evaluation Orchestrator.
- Store individual evaluation results.
- Display row-level scores and verdicts.
- Provide detailed inspection for selected rows.
- Calculate aggregate batch statistics.

---

## Results Presented to the User

The system provides:

- Relevance score and reasoning
- Accuracy score and evidence
- Hallucination safety score
- Unsupported/hallucinated claims
- Contradiction information
- Completeness score
- Addressed and missing aspects
- Overall weighted score
- Final verdict
- Verdict reasoning
- Retrieved evidence
- Validation/submission ID

## Milestone Mapping

### Milestone 1

- Initial system architecture
- Knowledge base
- Semantic retrieval
- Input validation
- Evaluation pipeline foundation

### Milestone 2

- Relevance Judge Agent
- Accuracy Judge Agent
- Hallucination Detection Agent
- Benchmark-based validation

### Milestone 3

- Completeness Judge Agent
- Weighted Scoring Module
- Verdict Module
- Evaluation Results Display
- Batch Evaluation Module