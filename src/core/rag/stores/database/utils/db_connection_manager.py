from contextlib import contextmanager
from typing import Generator
from sqlalchemy.engine import Connection, Engine
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DbConnectionManager:
    """Manages database connections and transactions"""
    
    def __init__(self, engine: Engine):
        """
        Initialize connection manager.
        """
        self.engine = engine
        logger.info("✅ ConnectionManager initialized")
    
    @contextmanager
    def read_connection(self) -> Generator[Connection, None, None]:
        """
        Context manager for read-only connections.
        """
        with self.engine.connect() as connection:
            try:
                yield connection
            except Exception as e:
                logger.error(f"❌ Error in read connection: {e}")
                raise
    
    @contextmanager
    def write_transaction(self) -> Generator[Connection, None, None]:
        """
        Context manager for write transactions with auto-commit/rollback.
        """
        with self.engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                logger.error(f"❌ Error in write transaction: {e}")
                raise
