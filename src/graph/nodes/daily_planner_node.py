from src.agents.daily_planner_agent.types.daily_planner_agent_data import DailyPlannerAgentData
from src.core.agent_manager import agent_manager
from src.graph.state import State
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def daily_planner_node(state: State) -> State:
    agent = agent_manager.get_agent('daily_planner')

    agent_data: DailyPlannerAgentData = {
        "calendar_events": state["calendar_events"],
        "current_time": state["current_time"],
        "priority_analysis_result": state["priority_analysis_result"]
    }

    result = await agent.process(agent_data)

    logger.info(f"Second agent result content: {result}")

    state.update({
        "daily_plan": result
    })

    return state