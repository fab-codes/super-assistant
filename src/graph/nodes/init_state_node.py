import datetime
import pytz
from src.graph.state import State

def init_state_node(state: State) -> State:
    timezone = pytz.timezone('Europe/Rome')
    
    state.update({
        "current_time": datetime.datetime.now(timezone)
    })

    return state