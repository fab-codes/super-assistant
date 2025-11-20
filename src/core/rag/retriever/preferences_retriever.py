from src.config.settings import VectorDbConfig
from src.core.rag.preferences_rag import PreferencesRag
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PreferencesRetriever:
    """
    Class to handle retriever
    """
    def __init__(self):
        self._preferences_rag = PreferencesRag()

        logger.info("✅ PreferencesRetriever initialized")

    async def retrieve_for_planning(self):
        """
        Retrieve preferences for daily planner
        """
        queries = [
            "preferenze orarie attività",
            "frequenza settimanale obiettivi",
        ]
        
        results = await self._preferences_rag.multiple_search(queries)

        unique_results = []
        seen = set()
        for result_list in results:
            for text in result_list:
                if text not in seen:
                    seen.add(text)
                    unique_results.append(text)
        
        logger.info(f"📋 Retrieved {len(unique_results)} unique preferences")
        return unique_results