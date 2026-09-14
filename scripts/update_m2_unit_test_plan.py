from openpyxl import load_workbook

file_path = "Agile/Unit_Test_Plan_v0.1.xlsx"

workbook = load_workbook(file_path)
sheet = workbook["UT"]

rows = [
    [
        15,
        "M2.4 - Benchmark Evaluation Set",
        "Run the Milestone 2 evaluation dataset through the Relevance, Accuracy, and Hallucination agents.",
        "Representative cases covering correct, incorrect, partially correct, irrelevant, incomplete, unsupported, and contradictory responses.",
        "All three agents should process every benchmark case successfully.",
        "M2.4 evaluation completed successfully using 7 representative cases."
    ],
    [
        16,
        "M2.4 - Agent Consistency",
        "Compare agent scores and categories across the same benchmark evaluation cases.",
        "Multiple QA cases are evaluated consistently by the Relevance, Accuracy, and Hallucination agents.",
        "Scores must remain within the valid 0 to 1 range and expected behaviors should be identified correctly.",
        "M2.4 consistency tests passed for all benchmark cases."
    ],
    [
        17,
        "M2.4 - Unsupported Claim Detection",
        "Evaluate a response containing one supported claim and one unsupported claim.",
        "Response: The capital of France is Paris. France has 20 states. Evidence: Paris is the capital city of France.",
        "The system should identify the specific unsupported claim and provide supporting evidence and reasoning.",
        "Unsupported claim 'France has 20 states.' was identified with evidence and reasoning."
    ],
    [
        18,
        "M2.4 - Full Regression Test",
        "Run the complete pytest test suite after Milestone 2 implementation.",
        "All existing Milestone 1 and Milestone 2 functionality is tested together.",
        "All automated tests should pass without functional failures.",
        "19 tests passed successfully. 4 deprecation warnings were reported."
    ],
]

for row in rows:
    sheet.append(row)

workbook.save(file_path)

print("M2 Unit Test Plan updated successfully.")