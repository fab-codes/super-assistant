from datetime import datetime, timedelta, timezone
from typing import List
from src.core.rag.stores.base_store_manager import BaseStoreManager
from src.core.rag.stores.database.metadata.metadata_manager import MetadataManager
from src.core.rag.stores.vector.pgvector.config import VectorStoreConfig
from src.core.rag.stores.database.postgres.postgres_store_manager import PostgresStoreManager
from src.core.rag.stores.vector.pgvector.pgvector_store_manager import PgVectorStoreManager
from llama_index.core import VectorStoreIndex, Document
from src.utils.logger import get_logger

logger = get_logger(__name__)

class StoreManager(BaseStoreManager):
    """Class to handle PGVector and DbManager store"""

    def __init__(self, connection_string: str):
        logger.info("🚀 Initializing PgVectorStore...")

        self.refresh_hours = VectorStoreConfig.DEFAULT_REFRESH_HOURS

        # Initialize managers
        self.pg_store_manager = PostgresStoreManager(connection_string)
        self.pgvector_store_manager = PgVectorStoreManager(connection_string)
        self.metadata_manager = MetadataManager(self.pg_store_manager.conn_manager)

        self.metadata_manager.create_table()

        logger.info(
            f"✅ StoreManager initialized "
            f"(refresh_hours: {self.refresh_hours})"
        )

    def should_refresh(self) -> bool:
        """
        Check if index should be refreshed.
        """
        try:
            # Check if empty
            count = self.pg_store_manager.count_documents()
            if count == 0:
                logger.info("📭 Vector store is empty, refresh needed")
                return True
            
            # Check last refresh
            last_refresh = self.metadata_manager.get_refresh_time()
            if last_refresh is None:
                logger.info("⏰ No refresh timestamp found, refresh needed")
                return True
            
            # Check age
            age = datetime.now(timezone.utc) - last_refresh
            age_hours = age.total_seconds() / 3600
            
            if age > timedelta(hours=self.refresh_hours):
                logger.info(
                    f"🔄 Data is {age_hours:.1f}h old "
                    f"(threshold: {self.refresh_hours}h), refresh needed"
                )
                return True
            
            logger.info(
                f"✅ Data is fresh ({age_hours:.1f}h old, {count} documents)"
            )
            return False
            
        except Exception as e:
            logger.warning(f"⚠️  Could not check refresh status: {e}")
            return True

    def create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Create new index from documents.
        """

        # Clear existing data
        self.clear()
        
        # Create index using vector manager
        index = self.pgvector_store_manager.create_index(documents)
        
        # Save metadata
        self.metadata_manager.save_refresh_time()
        
        logger.info("✅ Index created successfully")
        
        return index

    def get_index(self) -> VectorStoreIndex:
        """
        Get existing index from vector store.
        """
        return self.pgvector_store_manager.get_index()

    def clear(self) -> None:
        """Clear all documents from the vector store"""
        try:
            self.pg_store_manager.clear_documents()
            self.pgvector_store_manager.reset_index()
        except Exception as e:
            logger.error(f"❌ Error clearing vector store: {e}")
            raise

    def close(self) -> None:
        """Close all connections"""
        try:
            self.pg_store_manager.close()
            logger.info("✅ PostgresStoreManager closed")
        except Exception as e:
            logger.warning(f"⚠️ Error closing PostgresStoreManager: {e}")

    def __del__(self):
        try:
            if hasattr(self, 'pg_store_manager'):
                self.close()
        except Exception as e:
            pass