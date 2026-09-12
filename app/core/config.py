from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
KB_FILE = PROCESSED_DIR / "knowledge_base.json"
KB_INDEX_FILE = PROCESSED_DIR / "embedding_index.json"
SUBMISSIONS_FILE = DATA_DIR / "submissions.jsonl"
RETRIEVAL_REPORT_FILE = PROCESSED_DIR / "retrieval_report.json"

EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "sentence-transformers")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))

for directory in (RAW_DIR, PROCESSED_DIR):
    directory.mkdir(parents=True, exist_ok=True)
