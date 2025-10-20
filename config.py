"""
FastMCP Server Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration for FastMCP server"""
    
    # Memory Layer backend
    MEMORY_LAYER_URL = os.getenv("MEMORY_LAYER_URL", "http://localhost:8000")
    MEMORY_LAYER_TIMEOUT = int(os.getenv("MEMORY_LAYER_TIMEOUT", "30"))
    
    # Server settings
    SERVER_NAME = "ZepAI Memory Server"
    SERVER_VERSION = "2.0.0"
    
    # Default project ID
    DEFAULT_PROJECT_ID = os.getenv("DEFAULT_PROJECT_ID", "default_project")
    
    # Limits
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "50"))
    MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "100000"))
    MAX_CONVERSATION_MESSAGES = int(os.getenv("MAX_CONVERSATION_MESSAGES", "100"))


config = Config()

