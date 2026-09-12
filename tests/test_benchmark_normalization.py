from app.knowledge_base.ingest import normalize_squad, normalize_truthfulqa

def test_squad_normalization():
    rows=normalize_squad([{"id":"1","title":"T","question":"Q","context":"C","answers":{"text":["A"]}}])
    assert rows[0]["dataset"]=="SQuAD" and rows[0]["answer"]=="A"

def test_truthfulqa_normalization():
    rows=normalize_truthfulqa([{"question":"Q","best_answer":"A","correct_answers":["A"],"source":"S"}])
    assert rows[0]["dataset"]=="TruthfulQA" and rows[0]["answer"]=="A"
