import asyncio
from typing import List

from src.core.rag.stores.vector.pgvector.pgvector_store_manager import PgVectorStoreManager
from src.core.rag.embeddings.embeddings_manager import EmbeddingsManager
from src.core.rag.loaders.notion_loader.notion_loader import NotionLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PreferencesRag:
    def __init__(self, connection_string: str, similarity_top_k: int):
        logger.info("🚀 Initializing PreferencesRAG...")

        self.similarity_top_k = similarity_top_k

        # Setup embeddings
        EmbeddingsManager.setup_cohere()

        self.vector_store_manager = PgVectorStoreManager(connection_string)
        self.loader = NotionLoader()

        # self.index = self.vector_store_manager.get_index()
        self.index = self.vector_store_manager.create_index(self.loader.load())

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