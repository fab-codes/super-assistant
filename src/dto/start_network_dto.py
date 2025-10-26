from typing import List
from pydantic import BaseModel

from src.types.calendar_event import CalendarEvent
from src.types.task import Task

class StartNetworkDto(BaseModel):
    tasks_to_do: List[Task]
    calendar_events: List[CalendarEvent]