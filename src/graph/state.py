import datetime
from typing import List, TypedDict
from src.agents.priority_manager_agent.types.priority_analysis_result import PriorityAnalysisResult
from src.shared.types.calendar_event import CalendarEvent
from src.shared.types.task import Task

class State(TypedDict):
    current_time: datetime.datetime

    tasks_to_do: List[Task]
    calendar_events: List[CalendarEvent]
    priority_analysis_result: PriorityAnalysisResult

    daily_plan: str