import datetime
from src.graph.state import State

def init_state(state: State)-> State:
    state.update({
        "current_time": datetime.datetime.now()
    })

    return state