from src.agents.base_agent import BaseAgent
from src.agents.priority_manager_agent.types.input_agent_data import InputAgentData
from src.agents.priority_manager_agent.types.priority_analysis_result import PriorityAnalysisResult
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PriorityManagerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm, "PriorityManagerAgent")
        self.structured_llm = llm.with_structured_output(PriorityAnalysisResult)

    async def process(self, data: InputAgentData):
        logger.info(f"Processing {len(data["tasks_to_do"])} tasks and {len(data["calendar_events"])} events")

        prompt = f"""
            Analizza questi task e eventi del calendario per fornire una prioritizzazione intelligente:

            TASK DA FARE:
            {[task.dict() for task in data["tasks_to_do"]]}

            EVENTI CALENDARIO:
            {[event.dict() for event in data["calendar_events"]]}

            Prioritizza i task considerando:
            - Deadline e urgenza
            - Importanza del progetto
            - Disponibilità nel calendario
            - Dipendenze tra task

            Assegna un priority_score da 1-10 e fornisci reasoning dettagliato per ogni task.
            Suggerisci slot disponibili e strategia generale di organizzazione.
            Questa è la data di oggi: {data["current_time"]}
        """

        try:
            result = await self.structured_llm.ainvoke(prompt)
            logger.info("Structured priority analysis completed")

            return result.dict()

        except Exception as e:
            logger.error(f"Error in priority analysis: {e}")
            raise