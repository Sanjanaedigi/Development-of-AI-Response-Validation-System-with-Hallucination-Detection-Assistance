import json
import numpy as np
from app.core.config import KB_FILE, KB_INDEX_FILE, RETRIEVAL_TOP_K
from app.knowledge_base.embeddings import generate_embeddings, cosine_similarity, resolve_backend

def load_records():
    return json.loads(KB_FILE.read_text(encoding="utf-8")) if KB_FILE.exists() else []

def build_index(records=None, backend=None):
    records=records if records is not None else load_records()
    backend=resolve_backend(backend)
    vectors=generate_embeddings([r["text"] for r in records],backend)
    payload={"backend":backend,"records":records,"embeddings":vectors.tolist()}
    KB_INDEX_FILE.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
    return len(records)

def _load_index():
    if not KB_INDEX_FILE.exists():
        records=load_records()
        if not records: return [],np.empty((0,0),dtype=np.float32),"hashing"
        build_index(records)
    payload=json.loads(KB_INDEX_FILE.read_text(encoding="utf-8"))
    return payload["records"],np.asarray(payload["embeddings"],dtype=np.float32),payload["backend"]

def semantic_search(query,top_k=None):
    records,matrix,backend=_load_index()
    if not records: return []
    qv=generate_embeddings([query],backend)[0]
    scores=cosine_similarity(qv,matrix)
    order=np.argsort(scores)[::-1][:top_k or RETRIEVAL_TOP_K]
    return [{**records[i],"similarity":round(float(scores[i]),4)} for i in order]
