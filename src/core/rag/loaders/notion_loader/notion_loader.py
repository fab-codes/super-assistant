from typing import List
from llama_index.core import Document
from llama_index.readers.notion import NotionPageReader
from src.core.rag.loaders.base_loader import BaseLoader
from src.config.notion_config import NotionConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)

class NotionLoader(BaseLoader):
    """Load documents from Notion pages and databases"""

    def __init__(self):
        self.page_ids = NotionConfig.PAGES
        self.database_ids = NotionConfig.DATABASES

        self.reader = NotionPageReader(integration_token=NotionConfig.INTEGRATION_TOKEN)
        
        logger.info(
            f"NotionLoader initialized with {len(self.page_ids)} pages "
            f"and {len(self.database_ids)} databases"
        )

    def load(self) -> List[Document]:
        """
        Load all documents from Notion pages and databases.
        """
        all_documents = []
        
        # Load pages
        all_documents.extend(self._load_pages())
        
        # Load databases
        # all_documents.extend(self._load_databases())
        
        logger.info(f"✅ Loaded {len(all_documents)} total documents from Notion")
        
        return all_documents

    def _load_pages(self) -> List[Document]:
        """Load documents from Notion pages"""
        documents = []
        
        for page_id in self.page_ids:
            try:
                docs = self.reader.load_data(page_ids=[page_id])
                
                # Add metadata
                for doc in docs:
                    doc.metadata.update({
                        "source": "notion",
                        "source_type": "page",
                        "page_id": page_id
                    })
                
                documents.extend(docs)
                logger.info(f"📄 Loaded {len(docs)} docs from page {page_id}")
                
            except Exception as e:
                logger.error(f"❌ Error loading page {page_id}: {e}")
        
        return documents
    
    # def _load_databases(self) -> List[Document]:
    #     """Load documents from Notion databases"""
    #     documents = []
        
    #     for db_id in self.database_ids:
    #         try:
    #             docs = self.reader.load_data(database_ids=[db_id])
                
    #             # Add metadata
    #             for doc in docs:
    #                 doc.metadata.update({
    #                     "source": "notion",
    #                     "source_type": "database",
    #                     "database_id": db_id
    #                 })
                
    #             documents.extend(docs)
    #             logger.info(f"🗄️  Loaded {len(docs)} docs from database {db_id}")
                
    #         except Exception as e:
    #             logger.error(f"❌ Error loading database {db_id}: {e}")
        
    #     return documents