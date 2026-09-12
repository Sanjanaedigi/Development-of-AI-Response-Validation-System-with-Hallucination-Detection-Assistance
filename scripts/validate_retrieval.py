import json
from app.core.config import KB_FILE, RETRIEVAL_REPORT_FILE
from app.knowledge_base.vector_store import semantic_search

def validate(limit=20, top_k=5):
    records=json.loads(KB_FILE.read_text(encoding="utf-8"))
    candidates=[r for r in records if r["dataset"] in {"SQuAD","TruthfulQA"}][:limit]
    hits=0
    rows=[]
    for r in candidates:
        results=semantic_search(r["question"],top_k=top_k)
        ids={x["document_id"] for x in results}
        hit=r["document_id"] in ids
        hits += int(hit)
        rows.append({"question":r["question"],"dataset":r["dataset"],"expected_document_id":r["document_id"],"hit":hit,"top_similarity":results[0]["similarity"] if results else 0})
    report={"sample_size":len(candidates),"top_k":top_k,"hits":hits,"hit_rate":round(hits/max(1,len(candidates)),4),"rows":rows}
    RETRIEVAL_REPORT_FILE.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    return report

if __name__ == "__main__":
    report=validate()
    print(f"Retrieval Hit@{report['top_k']}: {report['hit_rate']*100:.1f}% ({report['hits']}/{report['sample_size']})")
