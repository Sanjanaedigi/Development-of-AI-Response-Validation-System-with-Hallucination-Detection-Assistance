import chromadb
from chromadb.utils import embedding_functions

class LocalVectorKnowledgeBase:
    def __init__(self):
        # Store facts locally on-disk
        self.client = chromadb.PersistentClient(path="./chroma_db_storage")
        
        # Embeddings Engine: Explicitly running all-MiniLM-L6-v2 locally
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="rag_evaluation_benchmarks",
            embedding_function=self.embedding_fn
        )

    def add_reference_documents(self, ids: list, documents: list, metadatas: list):
        """Saves target benchmark facts into the vector layout."""
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def semantic_context_lookup(self, query: str, top_k: int = 2):
        """RAG Architecture: Fetches background text matching the query semantic pattern."""
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return results['documents'][0] if results['documents'] else []
