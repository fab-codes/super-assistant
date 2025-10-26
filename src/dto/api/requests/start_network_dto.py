from typing import List
from pydantic import BaseModel

from src.shared.types.task import Task
from src.shared.types.calendar_event import CalendarEvent

class StartNetworkDto(BaseModel):
    tasks_to_do: List[Task]
    calendar_events: List[CalendarEvent]