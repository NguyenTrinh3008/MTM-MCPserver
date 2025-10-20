"""
HTTP Client for Memory Layer backend
"""
import httpx
import logging
from typing import Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)


class MemoryClient:
    """HTTP client for Memory Layer backend"""
    
    def __init__(self):
        self.base_url = config.MEMORY_LAYER_URL.rstrip("/")
        self.timeout = config.MEMORY_LAYER_TIMEOUT
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=5)
        )
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    # Ingest methods
    async def ingest_conversation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest conversation context"""
        response = await self.client.post(
            f"{self.base_url}/ingest/conversation",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def ingest_text(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest plain text"""
        response = await self.client.post(
            f"{self.base_url}/ingest/text",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def ingest_code(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest code change"""
        response = await self.client.post(
            f"{self.base_url}/ingest/code",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def ingest_json(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest JSON data"""
        response = await self.client.post(
            f"{self.base_url}/ingest/json",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    # Search methods
    async def search_knowledge(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge graph"""
        response = await self.client.post(
            f"{self.base_url}/search",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def search_code(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Search code changes"""
        response = await self.client.post(
            f"{self.base_url}/search/code",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    # Admin methods
    async def get_stats(self, project_id: str) -> Dict[str, Any]:
        """Get project statistics"""
        response = await self.client.get(
            f"{self.base_url}/stats/{project_id}"
        )
        response.raise_for_status()
        return response.json()
    
    async def clear_cache(self) -> Dict[str, Any]:
        """Clear cache"""
        response = await self.client.post(
            f"{self.base_url}/cache/clear"
        )
        response.raise_for_status()
        return response.json()
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check"""
        response = await self.client.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        response = await self.client.get(
            f"{self.base_url}/cache/stats"
        )
        response.raise_for_status()
        return response.json()


# Singleton instance
_client: Optional[MemoryClient] = None


async def get_client() -> MemoryClient:
    """Get or create memory client instance"""
    global _client
    if _client is None:
        _client = MemoryClient()
    return _client


async def close_client():
    """Close memory client"""
    global _client
    if _client is not None:
        await _client.close()
        _client = None

