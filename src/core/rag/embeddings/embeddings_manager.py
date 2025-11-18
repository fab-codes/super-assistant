from llama_index.core import Settings
from llama_index.embeddings.cohere import CohereEmbedding

from src.config.settings import CohereConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)

class EmbeddingsManager:
    """Manages embedding model configuration for RAG systems"""

    @staticmethod
    def setup_cohere() -> CohereEmbedding:
        embed_model = CohereEmbedding(
            api_key=CohereConfig.COHERE_API_KEY,
            model_name=CohereConfig.COHERE_MODEL_NAME,
            input_type="search_document"
        )

        # Set globally in LlamaIndex Settings
        Settings.embed_model = embed_model
        Settings.llm = None  # Disable LLM for embedding-only usage

        logger.info(f"🔧 Cohere embeddings configured: {CohereConfig.COHERE_MODEL_NAME}")

        return embed_model

    # @staticmethod
    # def setup_custom(embed_model) -> None:
    #     Settings.embed_model = embed_model
    #     Settings.llm = None

    #     logger.info(f"🔧 Custom embeddings configured: {type(embed_model).__name__}")