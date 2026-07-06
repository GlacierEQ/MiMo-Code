import os
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

class RawMem0APIClient:
    """
    Lightweight REST API client for Mem0.
    Communicates directly with the raw HTTP endpoints without requiring the 'mem0' library.
    Implements the precise 'Token <key>' Authorization header required by the API specs.
    """

    BASE_URL = "https://api.mem0.ai/v1"

    def __init__(self, api_key: Optional[str] = None, org_id: Optional[str] = None, project_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("MEM0_API_KEY", "your-mem0-api-key")
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Apply enterprise Org & Project IDs to headers if present
        if org_id or os.getenv("MEM0_ORG_ID"):
            self.headers["x-mem0-org-id"] = org_id or os.getenv("MEM0_ORG_ID")
        if project_id or os.getenv("MEM0_PROJECT_ID"):
            self.headers["x-mem0-project-id"] = project_id or os.getenv("MEM0_PROJECT_ID")

    def add_memory(self, messages: List[Dict[str, str]], user_id: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        POST /v1/memories/
        Extracts and stores facts directly via raw HTTP payload parameters.
        """
        url = f"{self.BASE_URL}/memories/"
        payload = {
            "messages": messages,
            "user_id": user_id,
            "metadata": metadata or {},
            "infer": True,
            "output_format": "v1.1",
            "version": "v2",  # Target version lock
            "timestamp": int(datetime.utcnow().timestamp())
        }

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_memories(self, query: str, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        POST /v1/memories/search/
        Queries context using semantic vector similarity search.
        """
        url = f"{self.BASE_URL}/memories/search/"
        payload = {
            "query": query,
            "user_id": user_id,
            "limit": limit
        }

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    casey_pro_id = "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U"
    raw_client = RawMem0APIClient()
    print("Raw REST Client successfully loaded. Authorization: Token header mapping active.")
