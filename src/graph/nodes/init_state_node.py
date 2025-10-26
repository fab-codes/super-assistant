import datetime
from src.graph.state import State

def init_state_node(state: State)-> State:
    state.update({
        "current_time": datetime.datetime.now(tz='Europe/Rome')
    })

    return state