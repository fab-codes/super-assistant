from datetime import datetime, timezone
from typing import Optional
from src.core.rag.stores.vector.pgvector.config import VectorStoreConfig
from src.core.rag.stores.database.utils.db_connection_manager import DbConnectionManager
from sqlalchemy import text
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MetadataManager:
    """Manages metadata table and operations"""

    def __init__(self, connection_manager: DbConnectionManager):
        self.conn_manager = connection_manager
        self.config = VectorStoreConfig()
        self._create_table_query = text(f"""
            CREATE TABLE IF NOT EXISTS {self.config.METADATA_TABLE} (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        self._upsert_query = text(f"""
            INSERT INTO {self.config.METADATA_TABLE} (key, value, updated_at)
            VALUES (:key, :value, NOW())
            ON CONFLICT (key) 
            DO UPDATE SET value = :value, updated_at = NOW()
        """)
        
        self._select_query = text(f"""
            SELECT value FROM {self.config.METADATA_TABLE} 
            WHERE key = :key
        """)

    def create_table(self) -> None:
        """Create metadata table if it doesn't exist"""
        try:
            with self.conn_manager.write_transaction() as conn:
                conn.execute(self._create_table_query)
                logger.info(f"✅ Metadata table '{self.config.METADATA_TABLE}' ready")
        except Exception as e:
            logger.error(f"❌ Failed to create metadata table: {e}")
            raise

    def save_refresh_time(self) -> None:
        """Save current timestamp as last refresh time (sync)"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()

            with self.conn_manager.write_transaction() as conn:
                conn.execute(
                    self._upsert_query,
                    {"key": self.config.REFRESH_KEY, "value": timestamp}
                )

                logger.info(f"✅ Saved refresh timestamp: {timestamp}")
        except Exception as e:
            logger.error(f"❌ Failed to save refresh time: {e}")
            raise

    def get_refresh_time(self) -> Optional[datetime]:
        """Retrieve last refresh timestamp"""
        try:
            with self.conn_manager.read_connection() as conn:
                result = conn.execute(
                    self._select_query,
                    {"key": self.config.REFRESH_KEY}
                )

                row = result.fetchone()
                if row:
                    timestamp_str = row[0]
                    dt = datetime.fromisoformat(timestamp_str)

                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt

                return None
        except Exception as e:
            logger.warning(f"⚠️ Could not retrieve last refresh time: {e}")
            return None