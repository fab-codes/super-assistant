from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.daily_planner_agent.agent import DailyPlannerAgent
from src.config.settings import GeminiConfig
from src.utils.logger import get_logger
from src.agents.priority_manager_agent.agent import PriorityManagerAgent

logger = get_logger(__name__)

class AgentManager:
    def __init__(self):
        self.llm = None
        self.agents = {}
        self._initialize_llm()
        self._initialize_agents()
    
    def _initialize_llm(self):
        """Init LLM model"""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=GeminiConfig.MODEL_ID,
                google_api_key=GeminiConfig.API_KEY,
                temperature=0.1
            )
            logger.info(f"✅ LLM initialized: {GeminiConfig.MODEL_ID}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLM: {e}")
            raise
    
    def _initialize_agents(self):
        """Init all agents"""
        try:
            self.agents = {
                "priority_manager": PriorityManagerAgent(self.llm),
                "daily_planner": DailyPlannerAgent(self.llm)
            }
            logger.info(f"✅ Initialized {len(self.agents)} agents")
        except Exception as e:
            logger.error(f"❌ Failed to initialize agents: {e}")
            raise
    
    def get_agent(self, agent_name: str):
        """Get single agent by name"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent type '{agent_name}' not found")
        return self.agents[agent_name]
    
    def get_all_agents(self):
        """Get all agents"""
        return self.agents

# Singleton instance
agent_manager = AgentManager()