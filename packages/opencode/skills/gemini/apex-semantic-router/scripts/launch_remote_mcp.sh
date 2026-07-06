#!/bin/bash
# Launches the Unified Memory MCP Server with SSE and exposes it remotely using localtunnel
echo "Starting Unified Memory MCP Server on Port 8000..."
python3 /data/data/com.termux/files/home/.gemini/skills/unified-memory-connect/logic/unified_memory_mcp.py sse &
MCP_PID=$!
sleep 2

echo "Exposing port 8000 remotely via localtunnel..."
npx localtunnel --port 8000
