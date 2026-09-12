"""Embedding generation.

Default: Sentence Transformers (all-MiniLM-L6-v2), a real dense text-embedding model.
Fallback: HashingVectorizer for offline/CI execution. The fallback is a vector
representation, not a substitute for the dense semantic model used in the normal path.
"""
from functools import lru_cache
import os
import numpy as np

DEFAULT_MODEL="sentence-transformers/all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def _sentence_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL))

def resolve_backend(requested=None):
    requested=(requested or os.getenv("EMBEDDING_BACKEND", "sentence-transformers")).lower()
    if requested in {"sentence-transformers","sentence_transformers","st"}:
        try:
            _sentence_model()
            return "sentence-transformers"
        except Exception:
            if os.getenv("EMBEDDING_STRICT","0") == "1": raise
            return "hashing"
    if requested in {"hashing","tfidf"}: return requested
    raise ValueError(f"Unsupported embedding backend: {requested}")

def generate_embeddings(texts, backend=None):
    texts=list(texts)
    if not texts: return np.empty((0,0),dtype=np.float32)
    backend=resolve_backend(backend)
    if backend=="sentence-transformers":
        return np.asarray(_sentence_model().encode(texts, normalize_embeddings=True),dtype=np.float32)
    if backend=="hashing":
        from sklearn.feature_extraction.text import HashingVectorizer
        from sklearn.preprocessing import normalize
        matrix=HashingVectorizer(n_features=1024, alternate_sign=False, norm=None, ngram_range=(1,2)).transform(texts)
        return normalize(matrix,norm="l2").toarray().astype(np.float32)
    if backend=="tfidf":
        from sklearn.feature_extraction.text import TfidfVectorizer
        return TfidfVectorizer(lowercase=True,ngram_range=(1,2),min_df=1).fit_transform(texts).toarray().astype(np.float32)
    raise ValueError(backend)

def cosine_similarity(query_vector,matrix):
    q=np.asarray(query_vector,dtype=np.float32); m=np.asarray(matrix,dtype=np.float32)
    if m.size==0 or q.size==0: return np.zeros(len(m),dtype=np.float32)
    qn=np.linalg.norm(q); mn=np.linalg.norm(m,axis=1); denom=mn*qn
    return np.divide(m@q,denom,out=np.zeros_like(mn),where=denom!=0)
