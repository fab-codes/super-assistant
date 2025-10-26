from typing import Optional
from pydantic import BaseModel

class Task(BaseModel):
    name: str
    project: str
    priority: str
    expire_date: Optional[str] = None