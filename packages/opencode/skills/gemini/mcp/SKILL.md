---
name: mcp
description: Model Context Protocol (MCP) server management and orchestration. Use when interacting with or configuring MCP servers for Postman, GitHub, Google Drive, or the local filesystem.
---

# MCP Orchestration Skill

## Overview
This skill enables the orchestration of Model Context Protocol (MCP) servers, empowering the system to interact with external tools and resources across multiple platforms.

## Core Reference
See `APEX_CORE.md` for foundational principles regarding Topological Surgicality, Surgical File Operations, State Management, and Verification Gates.

## Unified MCP Setup
The system's MCP servers are configured in `~/.gemini/settings.json`.

1.  **Postman**: Connects to `https://mcp.postman.com/mcp` using SSE. Requires `$POSTMAN_API_KEY`.
2.  **GitHub**: Connects to `https://api.githubcopilot.com/mcp/` using HTTP streaming.
3.  **Google Drive**: Uses `npx @isaacphi/mcp-gdrive`. Requires `$GDRIVE_CLIENT_ID` and `$GDRIVE_CLIENT_SECRET`. Credentials are saved in `~/.gemini/mcp_creds/gdrive`.
4.  **Filesystem**: Uses `npx @modelcontextprotocol/server-filesystem` mapped to the workspace root (`/data/data/com.termux/files/home`).

## Executing MCP Operations
-   **Postman**: Use for interacting with Postman collections, sending HTTP requests, and managing API workflows.
-   **GitHub**: Use for repository intelligence, pulling request details, searching codebases, and reading file streams directly from GitHub.
-   **Google Drive**: Use for listing, searching, and reading files.
-   **Filesystem**: Provides secure, local file-system operations within the allowed directory.

## Managing Credentials
Do not expose secrets in plain text. Remind the user to export the required environment variables in their `.bashrc` or `.gemini_env` file.
