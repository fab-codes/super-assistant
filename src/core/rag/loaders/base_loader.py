from abc import ABC, abstractmethod
from typing import List
from llama_index.core import Document

class BaseLoader(ABC):
    """Abstract base class for document loaders"""
    
    @abstractmethod
    def load(self) -> List[Document]:
        """Load documents from source"""
        pass