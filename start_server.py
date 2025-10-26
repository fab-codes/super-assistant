from fastapi import FastAPI, HTTPException
from datetime import datetime

from src.dto.start_network_dto import StartNetworkDto

app = FastAPI(
    title="Super Assistant API",
    description="Multi-agent system for intelligent task prioritization and scheduling",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": app.title,
        "status": "running",
        "version": app.version
    }

@app.post("/start_network")
async def start_network_work(request: StartNetworkDto):
    try:
        tasks_data = request.tasks_to_do
        calendar_data = request.calendar_events

        return {
            "status": "success",
            "message": f"Processed {len(tasks_data)} tasks and {len(calendar_data)} events",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

