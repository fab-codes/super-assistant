from dataclasses import dataclass
from typing import ClassVar

@dataclass
class VectorStoreConfig:
    """Configuration for PgVectorStore"""

    # Table names
    EMBEDDINGS_TABLE: ClassVar[str] = "preferences_embeddings"
    EMBEDDINGS_TABLE_FULL_NAME: ClassVar[str] = "data_preferences_embeddings"

    METADATA_TABLE: ClassVar[str] = "preferences_metadata"

    # Metadata keys
    REFRESH_KEY: ClassVar[str] = "last_refresh_timestamp"

    # Embedding configuration
    EMBED_DIM: ClassVar[int] = 1024  # Cohere embed-multilingual-v3.0

    # Refresh configuration
    DEFAULT_REFRESH_HOURS: ClassVar[int] = 24