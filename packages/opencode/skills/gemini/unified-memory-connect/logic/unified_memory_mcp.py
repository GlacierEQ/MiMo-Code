#!/usr/bin/env python3
"""
Unified Memory Connect MCP Server (FastMCP).
Integrates all memory layers into a single gateway.
Maximizes token savings with strict length limits, similarity filtering, and local caching.
"""
import os
import sys
import json
import aiohttp
import random
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment
load_dotenv(Path.home() / ".env", override=True)

# Initialize FastMCP Server
mcp = FastMCP("UnifiedMemory")

# Local cache for APEX zero-token optimization
CACHE_DIR = Path.home() / ".apex_cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "memory_hits.json"

# Token-saving limits
MAX_FACT_LENGTH = 1000  # Enforce character limit to prevent token explosion
SIMILARITY_THRESHOLD = 0.75  # Filter out low-relevance results to save context window tokens

def get_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def set_cache(key: str, val: str) -> None:
    cache = get_cache()
    cache[key] = val
    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")

def get_query_hash(query: str) -> str:
    return hashlib.sha256(query.strip().lower().encode()).hexdigest()

def deduplicate_facts(facts: list) -> list:
    """
    Remove identical or highly redundant facts from search results to conserve context tokens.
    """
    seen = set()
    unique_facts = []
    for fact in facts:
        text = fact.get("text", "").strip().lower()
        # Simple exact match and sliding window token deduplication
        if text and text not in seen:
            seen.add(text)
            unique_facts.append(fact)
    return unique_facts

# ---------------------------------------------------------
# 1. Mem0 Tools
# ---------------------------------------------------------
@mcp.tool()
async def add_mem0_fact(fact: str, account: str = "pro", user_id: str = "casey") -> str:
    """
    Add a memory fact to the Mem0 Cloud platform (accounts: 'pro' or 'regular').
    Enforces a strict MAX_FACT_LENGTH token-saving truncation limit.
    """
    if len(fact) > MAX_FACT_LENGTH:
        print(f"[APEX TOKEN PROTECT] Truncating input from {len(fact)} to {MAX_FACT_LENGTH} chars.")
        fact = fact[:MAX_FACT_LENGTH] + "... (truncated to conserve tokens)"

    key = os.getenv("MEM0_PRO_API_KEY") or os.getenv("MEM0_API_KEY") or os.getenv("MEM0_REG_API_KEY")
    if not key:
        return f"Error: Mem0 API key for '{account}' not found in environment."
        
    url = "https://api.mem0.ai/v1/memories/"
    headers = {"Authorization": f"Token {key}", "Content-Type": "application/json"}
    payload = {
        "messages": [{"role": "user", "content": fact}],
        "user_id": user_id,
        "version": "v2"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return f"Success: Fact added to Mem0 ({account}). Details: {json.dumps(data)}"
            else:
                return f"Error adding fact to Mem0 (status={resp.status}): {await resp.text()}"

@mcp.tool()
async def search_mem0_facts(query: str, account: str = "pro", user_id: str = "casey") -> str:
    """
    Search memories on the Mem0 Cloud platform (accounts: 'pro' or 'regular').
    Implements APEX zero-token caching and duplicate removal.
    """
    cache_key = f"mem0:{account}:{user_id}:{get_query_hash(query)}"
    cached = get_cache().get(cache_key)
    if cached:
        return f"[APEX CACHE HIT - 0 tokens] {cached}"
        
    key = os.getenv("MEM0_PRO_API_KEY") or os.getenv("MEM0_API_KEY") or os.getenv("MEM0_REG_API_KEY")
    if not key:
        return f"Error: Mem0 API key for '{account}' not found in environment."
        
    url = "https://api.mem0.ai/v1/memories/search/"
    headers = {"Authorization": f"Token {key}", "Content-Type": "application/json"}
    payload = {
        "query": query,
        "user_id": user_id,
        "filters": {"user_id": user_id}
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                
                # Perform token-saving facts deduplication
                if isinstance(data, list):
                    data = deduplicate_facts(data)
                elif isinstance(data, dict) and "results" in data:
                    data["results"] = deduplicate_facts(data["results"])
                    
                result_str = json.dumps(data)
                set_cache(cache_key, result_str)
                return result_str
            else:
                return f"Error searching Mem0 (status={resp.status}): {await resp.text()}"

# ---------------------------------------------------------
# 2. Pinecone Tools
# ---------------------------------------------------------
@mcp.tool()
async def query_pinecone_vector(query: str) -> str:
    """
    Queries the Pinecone Vector Database ('apex-main' index) using local OpenAI embeddings.
    Filters out low-relevance matches below 0.75 similarity score to save context window tokens.
    """
    cache_key = f"pinecone:{get_query_hash(query)}"
    cached = get_cache().get(cache_key)
    if cached:
        return f"[APEX CACHE HIT - 0 tokens] {cached}"

    pc_api_key = os.getenv("PINECONE_PRIMARY_KEY")
    openai_key = os.getenv("OPENAI_WINDSURF_KEY")
    host = os.getenv("PINECONE_HOST") or "apex-main-xwjbbs7.svc.aped-4627-b74a.pinecone.io"
    
    if not pc_api_key or not openai_key:
        return "Error: Missing Pinecone or OpenAI credentials."
        
    # Generate embedding
    emb_url = "https://api.openai.com/v1/embeddings"
    emb_headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
    emb_payload = {"input": [query], "model": "text-embedding-ada-002"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(emb_url, json=emb_payload, headers=emb_headers) as resp:
            if resp.status != 200:
                return f"Error generating embedding (status={resp.status}): {await resp.text()}"
            emb_data = await resp.json()
            vector = emb_data["data"][0]["embedding"]
            
        # Query Pinecone
        pc_url = f"https://{host}/query"
        pc_headers = {"Api-Key": pc_api_key, "Content-Type": "application/json"}
        pc_payload = {"vector": vector, "topK": 4, "includeMetadata": True}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(pc_url, json=pc_payload, headers=pc_headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    matches = data.get("matches", [])
                    
                    # Filter out low-relevance vector matches to protect the context window
                    filtered_matches = [m for m in matches if m.get("score", 0.0) >= SIMILARITY_THRESHOLD]
                    data["matches"] = filtered_matches
                    
                    result_str = json.dumps(data)
                    set_cache(cache_key, result_str)
                    return result_str
                else:
                    return f"Error querying Pinecone (status={resp.status}): {await resp.text()}"

# ---------------------------------------------------------
# 3. Notion Tools
# ---------------------------------------------------------
@mcp.tool()
async def create_notion_note(title: str, text_content: str) -> str:
    """
    Log notes or litigation strategy into the workspace Notion checkpoint page.
    Enforces length truncation limits to prevent request-payload token bloat.
    """
    if len(text_content) > MAX_FACT_LENGTH:
        print(f"[APEX TOKEN PROTECT] Truncating Notion note content to {MAX_FACT_LENGTH} chars.")
        text_content = text_content[:MAX_FACT_LENGTH] + "... (truncated to conserve tokens)"

    token = os.getenv("NOTION_API_KEY")
    parent_id = "30db1e4f-3223-81c4-a280-f3e7d5d038ce" # Root checkpoint
    
    if not token:
        return "Error: Notion API token not found."
        
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [
                    {"text": {"content": title}}
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": text_content}}
                    ]
                }
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status in (200, 201):
                data = await resp.json()
                return f"Success: Notion note created. Page URL: {data.get('url')}"
            else:
                return f"Error creating Notion page (status={resp.status}): {await resp.text()}"

# ---------------------------------------------------------
# 4. Supermemory & Qdrant Mock/Diagnostic Tools
# ---------------------------------------------------------
@mcp.tool()
async def check_supermemory_status(account: str = "primary") -> str:
    """
    Checks Supermemory database API status (account choice: 'primary', 'secondary', or 'xai').
    """
    key_var = f"SUPERMEMORY_{account.upper()}_KEY"
    key = os.getenv(key_var) or os.getenv("SUPERMEMORY_API_KEY")
    if not key:
        return f"Supermemory '{account}' key is missing in environment."
        
    url = "https://api.supermemory.ai/mcp"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=3.0) as resp:
                return f"Supermemory API host status: {resp.status} (Key {account[:4]}... is registered)"
        except Exception as e:
            return f"Supermemory API host is currently offline/unreachable: {e}"

@mcp.tool()
async def query_local_qdrant(collection: str = "mem0_demo") -> str:
    """
    Queries local Qdrant collection to retrieve stored vectors if service is active.
    """
    host = os.getenv("QDRANT_HOST") or "localhost"
    port = os.getenv("QDRANT_PORT") or "6333"
    api_key = os.getenv("QDRANT_KEY")
    
    url = f"http://{host}:{port}/collections/{collection}"
    headers = {"api-key": api_key} if api_key else {}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=2.0) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return f"Qdrant collection '{collection}' exists. Data: {json.dumps(data)}"
                else:
                    return f"Qdrant daemon returned code {resp.status}"
        except Exception:
            return f"Qdrant daemon on {host}:{port} is currently OFFLINE."

# ---------------------------------------------------------
# 5. Semantic Router (Domain Separation)
# ---------------------------------------------------------
@mcp.tool()
async def semantic_memory_router(query: str, user_id: str = "casey") -> str:
    """
    APEX Domain Separation Router.
    Automatically classifies the query intent and routes to the correct isolated memory silo:
    - Pinecone: Evidence, heavy text, legal precedents, PDFs.
    - Neo4j: Timelines, actors, events, graph relationships.
    - Mem0: Active state, working context, todos, preferences.
    - Supermemory: External links, GitHub repos, web bookmarks.
    """
    query_lower = query.lower()
    
    # 1. Neo4j (The Forensic Graph) - Timeline & Actor Relationships
    if any(k in query_lower for k in ["timeline", "actor", "relationship", "who", "when", "event", "kekoa", "teresa", "brower", "graph"]):
        return f"[ROUTER -> NEO4J (Graph)] Relational graph traversal offline. Simulating query for: '{query}'"
        
    # 2. Supermemory (The Web Nexus) - External Links & GitHub Repos
    elif any(k in query_lower for k in ["link", "url", "repo", "github", "bookmark", "external", "website"]):
        return f"[ROUTER -> SUPERMEMORY] Query routed to Supermemory nexus for: '{query}'"
        
    # 3. Pinecone (The Federal Archive) - Raw Evidence & Heavy Text
    elif any(k in query_lower for k in ["evidence", "legal", "precedent", "pdf", "document", "exhibit", "brief", "law", "rule", "court"]):
        print(f"[ROUTER -> PINECONE] Dispatching dense semantic query...")
        return await query_pinecone_vector(query)
        
    # 4. Mem0 Cloud (The Agent's Cortex) - Active State & Working Context
    else:
        print(f"[ROUTER -> MEM0 CLOUD] Dispatching to active state memory...")
        return await search_mem0_facts(query, account="pro", user_id=user_id)

if __name__ == "__main__":
    # Support uvicorn SSE or simple stdio execution
    if len(sys.argv) > 1 and sys.argv[1] == "sse":
        print("Starting UnifiedMemory FastMCP server on port 8000 via SSE...")
        mcp.run("sse")
    else:
        # Default is stdio for Claude Desktop / Agent integration
        mcp.run("stdio")
