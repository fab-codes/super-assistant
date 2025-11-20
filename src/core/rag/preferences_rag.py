import asyncio
from typing import List
from src.config.settings import VectorDbConfig
from src.core.rag.stores.store_manager import StoreManager
from src.core.rag.embeddings.embeddings_manager import EmbeddingsManager
from src.core.rag.loaders.notion_loader.notion_loader import NotionLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PreferencesRag:
    def __init__(self):
        logger.info("🚀 Initializing PreferencesRAG...")

        self.similarity_top_k = 5

        # Setup embeddings
        EmbeddingsManager.setup_cohere()

        self.notion_loader = NotionLoader()
        self.store_manager = StoreManager(VectorDbConfig.VECTOR_DB_CONNECTION_STRING)

        if self.store_manager.should_refresh():
            logger.info("📥 Refreshing data from Notion...")
            self._refresh()

        # Load index
        self.index = self.store_manager.get_index()

        logger.info("✅ PreferencesRAG ready!")

    def _refresh(self) -> None:
        """Refresh data from Notion (sync helper)"""
        try:
            documents = self.notion_loader.load()

            if not documents:
                logger.warning("⚠️ No documents loaded from Notion")
                return

            self.store_manager.create_index(documents)
            logger.info(f"✅ Refreshed with {len(documents)} documents")

        except Exception as e:
            logger.error(f"❌ Error refreshing from Notion: {e}")
            raise

    async def search(self, query: str) -> List[str]:
        """
        Search for relevant preferences
        """

        # Create retriever
        retriever = self.index.as_retriever(similarity_top_k=self.similarity_top_k)

        # Execute async retrieval
        nodes = await retriever.aretrieve(query)

        results = [node.text for node in nodes]
        logger.info(f"🔍 Query: '{query}' (top_k={self.similarity_top_k}) → {len(results)} results")

        return results

    async def multiple_search(self, queries: List[str]) -> List[List[str]]:
        """
        Execute multiple searches in parallel
        """
        tasks = [self.search(query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        logger.info(f"🔍 Executed {len(queries)} parallel searches")

        return results