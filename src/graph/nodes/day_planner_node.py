from src.core.agent_manager import agent_manager
from src.graph.state import State
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def day_planner_node(state: State) -> State:
    agent = agent_manager.get_agent('day_planner')

    result = await agent.process(state)

    logger.info(f"Second agent result content: {result}")

    state.update(result)

    return state