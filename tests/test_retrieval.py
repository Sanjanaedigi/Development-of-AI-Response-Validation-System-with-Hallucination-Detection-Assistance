import json
from pathlib import Path

def test_retrieval_fixture_quality(tmp_path, monkeypatch):
    monkeypatch.setenv("EMBEDDING_BACKEND", "hashing")
    from app.knowledge_base.vector_store import build_index, semantic_search
    records=[
      {"document_id":"s1","chunk_id":"s1_1","dataset":"SQuAD","question":"What is the capital of France?","answer":"Paris","source":"fixture","text":"Question: What is the capital of France? Answer: Paris Context: Paris is the capital of France."},
      {"document_id":"t1","chunk_id":"t1_1","dataset":"TruthfulQA","question":"What is RAG?","answer":"Retrieval augmented generation","source":"fixture","text":"Question: What is RAG? Answer: Retrieval augmented generation Context: RAG retrieves external evidence."},
    ]
    import app.knowledge_base.vector_store as vs
    monkeypatch.setattr(vs, "KB_INDEX_FILE", tmp_path/"index.json")
    monkeypatch.setattr(vs, "KB_FILE", tmp_path/"kb.json")
    (tmp_path/"kb.json").write_text(json.dumps(records),encoding="utf-8")
    build_index(records, backend="hashing")
    results=semantic_search("What is the capital of France?", top_k=1)
    assert results and results[0]["document_id"]=="s1"
    assert results[0]["similarity"] > 0
