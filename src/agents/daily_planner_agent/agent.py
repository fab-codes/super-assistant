from src.core.rag.retriever.preferences_retriever import PreferencesRetriever
from src.agents.base_agent import BaseAgent
from src.graph.state import State
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DailyPlannerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm, "DailyPlannerAgent")
        self.preferences_retriever = PreferencesRetriever()

    async def process(self, data: State):
        priority_analysis_result = data.get("priority_analysis_result")

        prompt = f"""
            Crea un piano dettagliato per domani basandoti su:

            TASK PRIORITIZZATI:
            {priority_analysis_result["prioritized_tasks"]}
            
            EVENTI GIÀ IN CALENDARIO:
            {data.get("calendar_events", [])}

            CONTESTO:
            - Oggi è {data.get("current_time")}
            - Considera orari realistici (laboratori, uffici, etc.)
            - Inserisci pause tra attività
            - Prevedi eventuale tempi per spostamenti

            Fornisci un piano orario dettagliato che eviti conflitti con gli eventi esistenti.
            Include orari specifici, durata stimata, e istruzioni pratiche.
            Rispondi con SOLO del testo, nient'altro.
        """

        try:
            result = await self.llm.ainvoke(prompt)
            logger.info("Day planning completed")

            return {"daily_plan": getattr(result, 'content', str(result))}

        except Exception as e:
            logger.error(f"Error in priority analysis: {e}")
            raise