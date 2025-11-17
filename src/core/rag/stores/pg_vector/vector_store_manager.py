from typing import List, Optional
from core.rag.stores.base_vector_store import BaseVectorStore
from sqlalchemy import make_url
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore

from src.core.rag.stores.pg_vector.config import VectorStoreConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)

class VectorStoreManager(BaseVectorStore):
    """Manages LlamaIndex PGVectorStore operations"""
    
    def __init__(self, connection_string: str):
        """
        Initialize vector store manager
        """
        logger.info("🔧 Initializing VectorStoreManager...")
        
        # Parse connection string
        db_url = make_url(connection_string)
        
        # Initialize LlamaIndex PGVectorStore
        self.vector_store = PGVectorStore.from_params(
            database=db_url.database,
            host=db_url.host,
            password=db_url.password,
            port=db_url.port,
            user=db_url.username,
            table_name=VectorStoreConfig.EMBEDDINGS_TABLE,
            embed_dim=VectorStoreConfig.EMBED_DIM,
            hnsw_kwargs={
                "hnsw_m": 16,
                "hnsw_ef_construction": 64,
                "hnsw_ef_search": 40,
                "hnsw_dist_method": "vector_cosine_ops",
            },
        )
        
        self._index: Optional[VectorStoreIndex] = None
        
        logger.info("✅ VectorStoreManager initialized")
    
    def create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Create new index from documents
        """
        logger.info(f"📊 Creating index from {len(documents)} documents...")
        
        # Create storage context
        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        
        # Create index - PGVectorStore handles embedding insertion
        self._index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        
        logger.info("✅ Index created successfully")
        
        return self._index
    
    def get_index(self) -> VectorStoreIndex:
        """
        Get existing index from vector store
        """
        if self._index is None:
            logger.info("📥 Loading index from pgvector...")

            self._index = VectorStoreIndex.from_vector_store(
                self.vector_store
            )
            logger.info("✅ Index loaded")
        
        return self._index