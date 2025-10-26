from src.core.agent_manager import agent_manager
from src.graph.state import State

async def priority_manager_node(state: State) -> State:
    agent = agent_manager.get_agent('priority_manager')
    
    agent_data = {
        "tasks_to_do": state["tasks_to_do"],
        "calendar_events": state["calendar_events"]
    }

    result = await agent.process(agent_data)

    state.update(result)

    return state