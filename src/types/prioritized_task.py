from pydantic import BaseModel

class PrioritizedTask(BaseModel):
    name: str
    project: str
    priority_score: int
    reasoning: str
    estimated_duration: str