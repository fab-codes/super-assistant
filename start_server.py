from src.main import start_network
from src.config.settings import AppConfig
from fastapi import FastAPI, HTTPException, Header

from src.dto.api.requests.start_network_dto import StartNetworkDto

app = FastAPI(
    title="Super Assistant API",
    description="Multi-agent system for intelligent task prioritization and scheduling",
    version="1.0.0"
)

@app.post("/start_network")
async def start_network_work(request: StartNetworkDto, x_api_key: str = Header(None, alias="X-API-Key")):
    if x_api_key != AppConfig.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    
    try:
       return await start_network(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

