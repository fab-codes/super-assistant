import asyncio
from typing import Optional
from src.config.settings import VectorDbConfig
from src.core.rag.preferences_rag import PreferencesRag
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PreferencesRetriever:
    """
    Class to handle retriever
    """
    def __init__(self):
        self._preferences_rag: Optional[PreferencesRag] = None
        self._init_lock = asyncio.Lock()

        logger.info("✅ PreferencesRetriever initialized")

    async def _ensure_rag_initialized(self) -> None:
        """
        Ensure RAG is initialized (async lazy loading).
        """
        if self._preferences_rag is not None:
            return
        
        async with self._init_lock:
            if self._preferences_rag is not None: # Double check pattern
                return
                
            logger.info("🚀 Initializing PreferencesRAG (first use)...")
            loop = asyncio.get_running_loop()
            
            self._preferences_rag = await loop.run_in_executor(
                None,
                PreferencesRag
            )
            logger.info("✅ PreferencesRAG ready")

    async def retrieve_for_planning(self):
        await self._ensure_rag_initialized()

        queries = [
            "preferenze orarie attività",
            "frequenza settimanale obiettivi",
        ]
        
        logger.info(f"🔍 Starting parallel search for {len(queries)} queries")
        
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, self._preferences_rag.search, query)
            for query in queries
        ]
        
        results_list = await asyncio.gather(*tasks)

        unique_results = []
        seen = set()
        for result in results_list:
            for text in result:
                if text not in seen:
                    seen.add(text)
                    unique_results.append(text)

        logger.info(f"📋 Retrieved {len(unique_results)} unique preferences")
        return unique_results