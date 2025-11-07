# processing_doc.py
import os
import shutil
import uuid
from pathlib import Path
from typing import Dict, Optional, List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from loguru import logger


class PDFIngestionPipelineFAISS:
    """
    Takes a PDF (bytes), chunks it, and builds/updates a FAISS vector DB on disk (CPU).
    """

    def __init__(
        self,
        persist_root: str = "vectorstores",
        data_root: str = "data",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ):
        logger.info("Initializing PDFIngestionPipelineFAISS.")
        self.persist_root = Path(persist_root)
        self.data_root = Path(data_root)
        self.persist_root.mkdir(parents=True, exist_ok=True)
        self.data_root.mkdir(parents=True, exist_ok=True)

        self.embedding_model = embedding_model
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        )
        logger.info("PDFIngestionPipelineFAISS initialized successfully.")

    def _save_original(self, file_bytes: bytes, filename: str) -> Path:
        logger.info(f"Saving original file: {filename}")
        safe_name = f"{uuid.uuid4()}_{filename}"
        path = self.data_root / safe_name
        with open(path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"File saved to: {path}")
        return path

    def _load_pdf(self, path: Path) -> List[Document]:
        logger.info(f"Loading PDF from: {path}")
        loader = PyPDFLoader(str(path))
        docs = loader.load()
        logger.info(f"PDF loaded successfully. Number of pages: {len(docs)}")
        return docs

    def _namespace_path(self, namespace: str) -> Path:
        path = self.persist_root / namespace
        logger.info(f"Generated namespace path: {path}")
        return path

    def _store_exists(self, ns_path: Path) -> bool:
        exists = (ns_path / "index.faiss").exists() and (ns_path / "index.pkl").exists()
        logger.info(f"Checking if store exists at {ns_path}: {exists}")
        return exists

    def _delete_previous_vector_db(self, ns_path: Path):
        """Deletes all files in the namespace path (vector db directory) if they exist."""
        logger.info(f"Deleting previous vector DB at: {ns_path}")
        if ns_path.exists() and ns_path.is_dir():
            for item in ns_path.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            logger.info(f"Previous vector DB at {ns_path} deleted.")
        else:
            logger.info(f"No previous vector DB found at {ns_path}.")

    def ingest(
        self,
        file_bytes: bytes,
        filename: str,
        namespace: str,
        extra_metadata: Optional[Dict] = None,
    ) -> Dict:
        logger.info(f"Ingesting file: {filename} into namespace: {namespace}")
        if not filename.lower().endswith(".pdf"):
            logger.error("Unsupported file type. Only PDF files are supported.")
            raise ValueError("Only PDF files are supported")

        original_path = self._save_original(file_bytes, filename)
        docs = self._load_pdf(original_path)

        # attach minimal metadata
        for d in docs:
            d.metadata = {
                **d.metadata,
                "source": original_path.name,
                "namespace": namespace,
                **(extra_metadata or {}),
            }

        # chunk
        chunks = self.splitter.split_documents(docs)
        logger.info(f"Split document into {len(chunks)} chunks.")

        ns_path = self._namespace_path(namespace)
        ns_path.mkdir(parents=True, exist_ok=True)

        # NEW BLOCK: Delete any previous vector DB in this namespace before generating a new one
        self._delete_previous_vector_db(ns_path)

        # Always create fresh FAISS index after deleting previous one
        logger.info("Creating new FAISS index.")
        store = FAISS.from_documents(chunks, self.embeddings)
        store.save_local(str(ns_path))
        logger.info("FAISS index created and saved successfully.")

        return {
            "namespace": namespace,
            "chunks_added": len(chunks),
            "index_path": str(ns_path),
            "original_file": original_path.name,
        }
