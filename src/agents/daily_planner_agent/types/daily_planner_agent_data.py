import datetime
from typing import List, TypedDict
from src.agents.priority_manager_agent.types.priority_analysis_result import PriorityAnalysisResult
from src.shared.types.calendar_event import CalendarEvent

class DailyPlannerAgentData(TypedDict):
    current_time: datetime.datetime
    priority_analysis_result: PriorityAnalysisResult
    calendar_events: List[CalendarEvent]