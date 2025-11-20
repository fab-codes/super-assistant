from abc import ABC, abstractmethod

class BaseDatabaseStore(ABC):
    """Abstract base class for database stores"""

    @abstractmethod
    def count_documents() -> int:
        """Count saved documents"""
        pass

    @abstractmethod
    def clear_documents() -> int:
        """Remove saved documents"""
        pass

    @abstractmethod
    def close() -> None:
        """Close db connections"""
        pass