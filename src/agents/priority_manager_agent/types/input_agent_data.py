import datetime
from typing import List, TypedDict
from src.shared.types.calendar_event import CalendarEvent
from src.shared.types.task import Task

class InputAgentData(TypedDict):
    current_time: datetime
    tasks_to_do: List[Task]
    calendar_events: List[CalendarEvent]