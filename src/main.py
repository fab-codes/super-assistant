from src.dto.api.requests.start_network_dto import StartNetworkDto
from src.graph.compile_graph import compile_graph
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def start_network(data: StartNetworkDto):
    app = compile_graph()

    result = await app.ainvoke(data)

    logger.info(result)
    # TODO: Gestire ritorno
    return "Worked"