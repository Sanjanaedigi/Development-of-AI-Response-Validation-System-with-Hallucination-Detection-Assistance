from datasets import load_dataset
from app.knowledge_base.vector_store import LocalVectorKnowledgeBase
import uuid

def run_benchmark_ingestion():
    vdb = LocalVectorKnowledgeBase()
    print("Pulling benchmark data records from Hugging Face...")

    ids, documents, metadatas = [], [], []

    # Seeding TruthfulQA
    try:
        truthful_qa = load_dataset("truthful_qa", "generation", split="validation[:10]")
        for row in truthful_qa:
            text_block = f"Question context: {row['question']} Verified Answer profile: {' ; '.join(row['correct_answers'])}"
            ids.append(f"truth_qa_{str(uuid.uuid4())[:8]}")
            documents.append(text_block)
            metadatas.append({"source": "truthful_qa"})
    except Exception as e:
        print(f"TruthfulQA parsing bypass: {e}")

    # Seeding SQuAD
    try:
        squad = load_dataset("squad", split="validation[:10]")
        for row in squad:
            text_block = f"Context Data: {row['context']} Reference Target: {row['question']}"
            ids.append(f"squad_{str(uuid.uuid4())[:8]}")
            documents.append(text_block)
            metadatas.append({"source": "squad"})
    except Exception as e:
        print(f"SQuAD parsing bypass: {e}")

    if documents:
        vdb.add_reference_documents(ids, documents, metadatas)
        print(f"Successfully processed and stored {len(documents)} reference documents into ChromaDB.")

if __name__ == "__main__":
    run_benchmark_ingestion()
