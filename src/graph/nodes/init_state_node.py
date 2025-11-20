import datetime
import pytz
from src.config.settings import AppConfig
from src.graph.state import State

def init_state_node(state: State) -> State:
    timezone = pytz.timezone(AppConfig.TIMEZONE)
    
    state.update({
        "current_time": datetime.datetime.now(timezone)
    })

    return state