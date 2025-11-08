from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path
from loguru import logger

class retriving:
    def __init__(
        self,
        persist_root: str = "vectorstores",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        namespace: str = "default"
    ):
        logger.info(f"Initializing retriving with namespace: {namespace}")
        self.persist_root = Path(persist_root)
        self.embedding_model = embedding_model
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        self.namespace = namespace
        self.db = None  # Initialize db as None
        self._load_db_if_exists()

    def _namespace_path(self) -> Path:
        path = self.persist_root / self.namespace
        logger.info(f"Generated namespace path: {path}")
        return path

    def _store_exists(self, ns_path: Path) -> bool:
        # A vectorstore is considered present if both index.faiss and index.pkl exist.
        exists = (ns_path / "index.faiss").exists() and (ns_path / "index.pkl").exists()
        logger.info(f"Checking if store exists at {ns_path}: {exists}")
        return exists

    def _load_db_if_exists(self):
        ns_path = self._namespace_path()
        if self._store_exists(ns_path):
            self.db = self._load_db()

    def reload_db(self):
        logger.info("Reloading vector store.")
        self._load_db_if_exists()

    def _load_db(self):
        # Call this AFTER verifying the vectorstore exists!
        logger.info("Loading vector store.")
        ns_path = self._namespace_path()
        db = FAISS.load_local(
            str(ns_path),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        logger.info("Vector store loaded successfully.")
        return db

    def retrive_relevant_context(self, user_query: str, k: int = 5):
        logger.info(f"Retrieving relevant context for query: {user_query}")
        if not self.db:
            logger.error(f"Vector store not found for namespace: {self.namespace}")
            raise FileNotFoundError(f"Vector store not found for namespace: {self.namespace}")

        results = self.db.similarity_search(user_query, k=k)
        logger.info(f"Found {len(results)} relevant documents.")
        return results

# Explanation:
# The FileNotFoundError occurs if you try to initialize retriving with a namespace that does not have a vectorstore saved under 'vectorstores/<namespace>/index.faiss' and 'index.pkl'.
# This can happen if you haven't yet uploaded and ingested a document that would create the corresponding vectorstore for that namespace.
# The code now initializes retriving even if the store is not present; however, attempting to call retrive_relevant_context will still raise an error if the underlying vectorstore isn't loaded.