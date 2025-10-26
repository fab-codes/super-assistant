from pydantic import BaseModel

class CalendarEvent(BaseModel):
    summary: str
    description: str
    calendar: str
    start_date: str
    end_date: str