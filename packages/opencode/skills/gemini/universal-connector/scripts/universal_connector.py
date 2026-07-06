#!/usr/bin/env python3
"""
UNIVERSAL KEY & API CONNECTOR (DYNAMIC SKILL ENGINE)
Entity Tag: CODE_MASTER:WORLD_CLASS_ENGINEER
Mantra: Write like the repo matters.

This engine dynamically creates, configures, and invokes API connectors and local
skills for various cloud platforms (GitHub, Supabase, Vercel, ClickUp, Qdrant, Sentry, etc.).
It integrates with OperatorKeyVault for secret retrieval and dynamically updates local
MCP server manifests on-the-fly.
"""

import os
import sys
import json
import logging
import requests
from typing import Dict, Any, Optional
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] 🌌 [UNIVERSAL-CONNECTOR]: %(message)s')
logger = logging.getLogger("UniversalConnector")

VAULT_DIR = os.path.expanduser("~/.operator_key_vault")
MCP_SERVERS_JSON = os.path.expanduser("~/.mcp/servers.json")
SKILLS_DIR = os.path.expanduser("~/SKILLS")

class UniversalConnector:
    def __init__(self):
        self.env_vars = self._load_env()
        os.makedirs(SKILLS_DIR, exist_ok=True)

    def _load_env(self) -> Dict[str, str]:
        """Loads local environment variables, falling back to .env file."""
        vars_dict = dict(os.environ)
        env_file = os.path.expanduser("~/.env")
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            k, v = line.split('=', 1)
                            vars_dict[k.strip()] = v.strip().strip('"').strip("'")
            except Exception as e:
                logger.error(f"Failed to parse .env file: {e}")
        return vars_dict

    def get_credential(self, key: str) -> Optional[str]:
        """Retrieves key from active environment or OperatorKeyVault."""
        val = self.env_vars.get(key)
        if not val:
            try:
                sys.path.append(os.path.expanduser("~"))
                from operator_key_vault import OperatorKeyVault
                vault = OperatorKeyVault()
                val = vault.get_secret(key)
            except Exception:
                pass
        return val

    def execute_request(self, platform: str, endpoint: str, method: str = "GET", payload: Any = None) -> Optional[Dict[str, Any]]:
        """Dynamically builds headers and triggers API requests to cloud platforms."""
        platform = platform.lower()
        url = ""
        headers = {"Content-Type": "application/json"}

        # Dynamic authentication mapping based on platform
        if platform == "github":
            token = self.get_credential("GITHUB_TOKEN") or self.get_credential("GITHUB_PAT")
            if not token:
                logger.error("No GITHUB_TOKEN configured.")
                return None
            url = f"https://api.github.com{endpoint}"
            headers["Authorization"] = f"token {token}"
            headers["Accept"] = "application/vnd.github.v3+json"
            
        elif platform == "supabase":
            sb_url = self.get_credential("SUPABASE_URL")
            sb_key = self.get_credential("SUPABASE_SERVICE_ROLE_KEY") or self.get_credential("SUPABASE_ANON_KEY")
            if not sb_url or not sb_key:
                logger.error("No SUPABASE_URL or keys configured.")
                return None
            url = f"{sb_url.rstrip('/')}/rest/v1{endpoint}"
            headers["apikey"] = sb_key
            headers["Authorization"] = f"Bearer {sb_key}"
            
        elif platform == "vercel":
            token = self.get_credential("VERCEL_TOKEN")
            if not token:
                logger.error("No VERCEL_TOKEN configured.")
                return None
            url = f"https://api.vercel.com{endpoint}"
            headers["Authorization"] = f"Bearer {token}"
            
        elif platform == "clickup":
            token = self.get_credential("CLICKUP_API_KEY")
            if not token:
                logger.error("No CLICKUP_API_KEY configured.")
                return None
            url = f"https://api.clickup.com/api/v2{endpoint}"
            headers["Authorization"] = token
            
        elif platform == "qdrant":
            qd_url = self.get_credential("QDRANT_URL")
            qd_key = self.get_credential("QDRANT_API_KEY")
            if not qd_url:
                logger.error("No QDRANT_URL configured.")
                return None
            url = f"{qd_url.rstrip('/')}{endpoint}"
            if qd_key:
                headers["api-key"] = qd_key

        elif platform == "pinecone":
            pc_key = self.get_credential("PINECONE_API_KEY")
            if not pc_key:
                logger.error("No PINECONE_API_KEY configured.")
                return None
            url = endpoint if endpoint.startswith("http") else f"https://api.pinecone.io{endpoint}"
            headers["Api-Key"] = pc_key
        else:
            logger.error(f"Platform '{platform}' not natively mapped. Triggering generic request.")
            url = endpoint

        logger.info(f"Triggering request: {method} -> {url}")
        try:
            r = requests.request(method, url, headers=headers, json=payload, timeout=15)
            if r.status_code in [200, 201, 204]:
                return r.json() if r.text else {"success": True}
            else:
                logger.error(f"API Error ({r.status_code}): {r.text}")
                return {"error": r.status_code, "detail": r.text}
        except Exception as e:
            logger.error(f"HTTP Request failed: {e}")
            return None

    def generate_skill(self, name: str, code_template: str) -> str:
        """Dynamically creates a Python executable skill script under ~/SKILLS/."""
        skill_path = os.path.join(SKILLS_DIR, f"{name.lower()}_skill.py")
        try:
            with open(skill_path, 'w') as f:
                f.write(code_template)
            os.chmod(skill_path, 0o755)
            logger.info(f"Dynamically generated custom skill script: {skill_path}")
            return skill_path
        except Exception as e:
            logger.error(f"Failed to generate skill {name}: {e}")
            raise

    def register_mcp_server(self, name: str, exec_path: str, args: list) -> bool:
        """Registers a dynamically generated skill as a local MCP server in servers.json."""
        if not os.path.exists(MCP_SERVERS_JSON):
            logger.warning(f"MCP servers manifest not found at {MCP_SERVERS_JSON}. Creating a new one...")
            data = {"mcpServers": {}}
        else:
            try:
                with open(MCP_SERVERS_JSON, 'r') as f:
                    data = json.load(f)
            except Exception:
                data = {"mcpServers": {}}

        data["mcpServers"][name] = {
            "command": "python3",
            "args": [exec_path] + args,
            "env": {
                "PATH": os.environ.get("PATH", "")
            }
        }

        try:
            os.makedirs(os.path.dirname(MCP_SERVERS_JSON), exist_ok=True)
            with open(MCP_SERVERS_JSON, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Dynamically registered MCP Server mapping for '{name}' successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to update MCP servers manifest: {e}")
            return False

if __name__ == "__main__":
    connector = UniversalConnector()
    print("🌌 UNIVERSAL CONNECTOR ENGINE ONLINE.")
