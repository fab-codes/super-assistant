from src.config.settings import VectorDbConfig
from src.core.rag.preferences_rag import PreferencesRag
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PreferencesRetriever:
    """
    Class to handle retriever
    """
    def __init__(self, connection_string: str = VectorDbConfig.VECTOR_DB_CONNECTION_STRING, similarity_top_k = 5):
        self._preferences_rag = PreferencesRag(connection_string, similarity_top_k)

        logger.info("✅ PreferencesRetriever initialized")