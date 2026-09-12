"""Milestone 1 benchmark ingestion and preprocessing.

Sources:
- truthfulqa/truthful_qa (generation/validation)
- rajpurkar/squad (train/validation)

Raw benchmark files are intentionally not committed to GitHub. Running this module
fetches a bounded sample, normalizes fields, chunks contexts, and builds embeddings.
"""
import argparse, json
from app.core.config import KB_FILE, RAW_DIR, PROCESSED_DIR
from app.knowledge_base.chunking import chunk_text
from app.knowledge_base.vector_store import build_index

TRUTHFULQA = "truthfulqa/truthful_qa"
SQUAD = "rajpurkar/squad"

SEED = [
    {"dataset":"Seed Knowledge","question":"What is RAG?","answer":"Retrieval-Augmented Generation retrieves relevant external information and uses it as context for generation.","context":"RAG retrieves relevant information from a knowledge source and supplies it as context to a language model."},
    {"dataset":"Seed Knowledge","question":"What is an AI hallucination?","answer":"An AI hallucination is an unsupported or fabricated claim produced by an AI system.","context":"Hallucination evaluation checks whether generated claims are supported by reliable evidence."},
]


def _write_records(rows):
    records=[]
    for i,row in enumerate(rows):
        base_text=f"Question: {row['question']} Answer: {row['answer']} Context: {row.get('context','')}"
        for j,chunk in enumerate(chunk_text(base_text)):
            records.append({
                "document_id": str(row.get("document_id", f"doc_{i:06d}")),
                "chunk_id": f"{row.get('document_id', f'doc_{i:06d}')}_chunk_{j:03d}",
                "dataset": row["dataset"],
                "question": row["question"],
                "answer": row["answer"],
                "source": row.get("source", row["dataset"]),
                "text": chunk,
            })
    KB_FILE.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    build_index(records)
    return len(records)


def load_hf(dataset_name, config=None, split=None, limit=200):
    from datasets import load_dataset
    kwargs = {"path": dataset_name}
    if config: kwargs["name"] = config
    if split: kwargs["split"] = split
    ds = load_dataset(**kwargs)
    if split is None and hasattr(ds, "keys"):
        split = "train" if "train" in ds else next(iter(ds.keys()))
        ds = ds[split]
    return ds.select(range(min(limit, len(ds))))


def normalize_squad(ds):
    rows=[]
    for i,row in enumerate(ds):
        answers=row.get("answers", {}) or {}
        answer=(answers.get("text") or [""])[0]
        rows.append({"document_id": f"squad_{row.get('id', i)}", "dataset":"SQuAD", "question":str(row.get("question","")), "answer":str(answer), "context":str(row.get("context","")), "source":f"SQuAD:{row.get('title','')}"})
    return rows


def normalize_truthfulqa(ds):
    rows=[]
    for i,row in enumerate(ds):
        best=str(row.get("best_answer", ""))
        correct=row.get("correct_answers", []) or []
        context="; ".join(str(x) for x in correct)
        rows.append({"document_id": f"truthfulqa_{i:05d}", "dataset":"TruthfulQA", "question":str(row.get("question","")), "answer":best, "context":context, "source":str(row.get("source",""))})
    return rows


def build_benchmark_kb(squad_limit=200, truthfulqa_limit=200):
    squad = load_hf(SQUAD, split="train", limit=squad_limit)
    truthful = load_hf(TRUTHFULQA, config="generation", split="validation", limit=truthfulqa_limit)
    rows = normalize_squad(squad) + normalize_truthfulqa(truthful) + SEED
    return _write_records(rows)


def build_seed_kb():
    return _write_records(SEED)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["seed","benchmarks"], default="benchmarks")
    parser.add_argument("--squad-limit", type=int, default=200)
    parser.add_argument("--truthfulqa-limit", type=int, default=200)
    args=parser.parse_args()
    count = build_seed_kb() if args.mode=="seed" else build_benchmark_kb(args.squad_limit,args.truthfulqa_limit)
    print(f"Knowledge base ready: {count} chunks -> {KB_FILE}")
