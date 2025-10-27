from src.agents.priority_manager_agent.types.input_agent_data import InputAgentData
from src.core.agent_manager import agent_manager
from src.graph.state import State
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def priority_manager_node(state: State) -> State:
    agent = agent_manager.get_agent('priority_manager')
    
    agent_data: InputAgentData = {
        "tasks_to_do": state["tasks_to_do"],
        "calendar_events": state["calendar_events"],
        "current_time": state["current_time"]
    }

    result = await agent.process(agent_data)

    logger.info(f"First agent result content: {result}")

    state.update({
        "priority_analysis_result": result
    })

    return state