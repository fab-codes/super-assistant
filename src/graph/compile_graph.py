from src.graph.init_state import init_state
from src.core.agent_manager import agent_manager
from src.graph.state import State
from langgraph.graph import StateGraph, START, END
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def priority_manager_node(state: State) -> State:
    agent = agent_manager.get_agent('priority_manager')
    
    agent_data = {
        "tasks_to_do": state["tasks_to_do"],
        "calendar_events": state["calendar_events"]
    }

    result = await agent.process(agent_data)

    state.update(result)

    return state

def compile_graph():
    graph = StateGraph(State)

    graph.add_node('init', init_state)
    graph.add_node('priority_manager_agent', priority_manager_node)
    
    graph.add_edge(START, 'init')
    graph.add_edge('init', 'priority_manager_agent')
    graph.add_edge('priority_manager_agent', END)

    return graph.compile()