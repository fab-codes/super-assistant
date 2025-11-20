from src.core.rag.stores.vector.pgvector.config import VectorStoreConfig
from src.core.rag.stores.database.utils.db_connection_manager import DbConnectionManager
from src.core.rag.stores.database.base_database_store import BaseDatabaseStore
from src.utils.logger import get_logger
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = get_logger(__name__)

class PostgresStoreManager(BaseDatabaseStore):
    """Manages database operations"""

    def __init__(self, connection_string: str):
        # Create dedicated SQLAlchemy engine for direct database operations
        self.engine: Engine = create_engine(
            connection_string,
            pool_pre_ping=True,
            echo=False
        )

        logger.info("✅ PostgresStoreManager initialized")

        self.conn_manager = DbConnectionManager(self.engine)

    def count_documents(self) -> int:
        """
        Count documents
        """
        try:
            with self.conn_manager.read_connection() as conn:
                result = conn.execute(
                    text(f"SELECT COUNT(*) FROM {VectorStoreConfig.EMBEDDINGS_TABLE_FULL_NAME}")
                )
                return result.scalar() or 0
        except Exception as e:
            logger.error(f"❌ Error counting documents: {e}")
            return 0

    def clear_documents(self) -> int:
        """
        Clear all documents from the vector store.
        """
        try:
            with self.conn_manager.write_transaction() as conn:
                result = conn.execute(
                    text(f"DELETE FROM {VectorStoreConfig.EMBEDDINGS_TABLE_FULL_NAME}")
                )
                deleted_count = result.rowcount
                logger.info(
                    f"🗑️  Cleared {deleted_count} documents from "
                    f"table: {VectorStoreConfig.EMBEDDINGS_TABLE_FULL_NAME}"
                )
                return deleted_count
        except Exception as e:
            logger.error(f"❌ Error clearing vector store: {e}")
            raise
    
    def close(self) -> None:
        """Close database connections"""
        try:
            self.engine.dispose()
            logger.info("✅ Database connections closed")
        except Exception as e:
            logger.warning(f"⚠️  Error closing connections: {e}")