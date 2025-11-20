from abc import ABC, abstractmethod
from typing import List
from llama_index.core import VectorStoreIndex, Document

class BaseStoreManager(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """Create index from documents"""
        pass
    
    @abstractmethod
    def get_index(self) -> VectorStoreIndex:
        """Get existing index"""
        pass
    
    @abstractmethod
    def should_refresh(self) -> bool:
        """Check if index should be refreshed"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear the vector store"""
        pass