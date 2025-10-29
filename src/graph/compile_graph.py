from src.graph.nodes.daily_planner_node import daily_planner_node
from src.graph.nodes.init_state_node import init_state_node
from src.graph.nodes.priority_manager_node import priority_manager_node
from src.graph.state import State
from langgraph.graph import StateGraph, START, END
from src.utils.logger import get_logger

logger = get_logger(__name__)

def compile_graph():
    graph = StateGraph(State)

    graph.add_node('init', init_state_node)
    graph.add_node('priority_manager_node', priority_manager_node)
    graph.add_node('daily_planner_node', daily_planner_node)
    
    graph.add_edge(START, 'init')
    graph.add_edge('init', 'priority_manager_node')
    graph.add_edge('priority_manager_node', 'daily_planner_node')
    graph.add_edge('daily_planner_node', END)

    return graph.compile()