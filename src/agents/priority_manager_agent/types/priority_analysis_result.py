from typing import List
from pydantic import BaseModel
from src.agents.priority_manager_agent.types.prioritized_task import PrioritizedTask

class PriorityAnalysisResult(BaseModel):
    prioritized_tasks: List[PrioritizedTask]
    recommendations: str
    available_slots: List[str]
    overall_strategy: str