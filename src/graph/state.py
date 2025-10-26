import datetime
from typing import List, TypedDict
from src.types.task import Task
from src.types.calendar_event import CalendarEvent
from src.types.priority_analysis_result import PriorityAnalysisResult

class State(TypedDict):
    current_time: datetime

    tasks_to_do: List[Task]
    calendar_events: List[CalendarEvent]
    priority_analysis_result: PriorityAnalysisResult