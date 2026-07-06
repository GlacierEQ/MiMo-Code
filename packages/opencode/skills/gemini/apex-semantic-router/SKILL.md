---
name: apex-semantic-router
description: Deploys the APEX Semantic Memory Router MCP server to route queries to domain-isolated memory silos (Mem0, Pinecone, Neo4j, Supermemory) and maximize token savings.
---

# APEX Semantic Memory Router

This skill provides the hardened Unified Memory MCP Server configured with Domain Separation. It routes context queries to their appropriate database engines to prevent token bloat and optimize context window efficiency.

## Bundled Resources

- `scripts/unified_memory_mcp.py`: The core FastMCP server containing the `semantic_memory_router` tool and all individual layer integrations.
- `scripts/launch_remote_mcp.sh`: Bash script to launch the server via SSE and expose it to the internet using localtunnel.

## Usage

To launch the router as a remote SSE MCP server (for use in Claude Desktop, Cursor, or other agents):
```bash
bash scripts/launch_remote_mcp.sh
```

To run it locally as a standard STDIO MCP server:
```bash
python3 scripts/unified_memory_mcp.py
```
