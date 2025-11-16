import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class NotionConfig:
    """Notion API configuration"""

    # Notion Integration Token
    INTEGRATION_TOKEN: str = os.getenv("NOTION_TOKEN", "")

    # Page IDs (with preferences)
    PAGES: List[str] = [
        os.getenv("NOTION_VIDEOGAMES_NOTES_PAGE", ""),
        os.getenv("NOTION_SPORT_PAGE", ""),
    ]

    # Database IDs (for structured data)
    DATABASES: List[str] = [
        os.getenv("NOTION_VIDEOGAMES_LIST_DB", ""),
    ]

    @classmethod
    def validate(cls) -> bool:
        """Validate that all required config is present"""
        if not cls.INTEGRATION_TOKEN:
            raise ValueError("NOTION_TOKEN not set in environment")

        # Filter out empty strings
        cls.PAGES = [p for p in cls.PAGES if p]
        cls.DATABASES = [d for d in cls.DATABASES if d]

        if not cls.PAGES and not cls.DATABASES:
            raise ValueError("No Notion pages or databases configured")

        return True

NotionConfig.validate()