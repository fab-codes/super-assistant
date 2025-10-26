from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.utils.logger import get_logger

logger = get_logger(__name__)

class BaseAgent(ABC):
    """
    Base class for all agents
    """
    def __init__(self, llm, agent_name: str):
        self.llm = llm
        self.agent_name = agent_name
        logger.info(f"🤖 Initialized {agent_name}")
    
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing method to be implemented by all agents"""
        pass
    
    def _validate_input(self, data: Dict[str, Any], required_fields: List[str]):
        """Validate input data against required fields"""
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")