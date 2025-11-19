from src.core.rag.stores.database.base_database_store import BaseDatabaseStore
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PostgresStoreManager(BaseDatabaseStore):
    """Manages database operations"""