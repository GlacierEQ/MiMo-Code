# MiMo Code — Unified Integration Manifest

> Generated from `mimo-config-backup` merge into `mimo-code` infrastructure.
> Date: 2026-07-05

## Overview

This manifest documents the complete integration of the `mimo-config-backup` repository into the `mimo-code` CLI infrastructure. All skills, memory systems, and configuration assets have been merged into the open-source codebase.

## Integrated Components

### 1. Skill Registry — 44 Skills

| Category | Source | Count | Status |
|----------|--------|-------|--------|
| **agents/** | `agents_skills/` | 23 | ✅ Merged |
| **gemini/** | `gemini_skills/` | 11 | ✅ Merged |
| **grok/** | `grok_skills/` | 9 | ✅ Merged |
| **mimo/** | `mimocode_skills/` | 1 | ✅ Merged |
| **compose/** | Built-in bundle | ~15 | ✅ Existing |

**Total: 44 integrated + ~15 compose = ~59 available skills**

### 2. Discovery System

- **Built-in registry**: `packages/opencode/skills/` auto-scanned at startup
- **Flag**: `MIMOCODE_DISABLE_BUILTIN_SKILLS=true` to disable
- **Remote discovery**: `index.json` files at each category root
- **Override order**: User skills > Project skills > External skills > Built-in skills > Compose skills

### 3. Configuration

- `skills.paths` — custom skill directories (configurable in `opencode.json`)
- `skills.urls` — remote skill registries (configurable in `opencode.json`)
- Built-in registry auto-discovered — no config needed

### 4. Memory System

- `memory_system/` — session/project/global memory with archive
- `supermemory/` — supermemory integration with ops state
- `mimocode_data/memory/` — runtime memory store
- Integrated via `packages/opencode/src/memory/` service

### 5. MCP Integration

- `mimocode_apex_final/mcp_hub.py` — MCP hub orchestrator
- `mimocode_apex_final/orchestrator/mcp_hub.py` — Orchestrator MCP
- Integrated via `packages/opencode/src/mcp/` service

### 6. JSON Manifests

| Manifest | Purpose | Status |
|----------|---------|--------|
| `CONNECTOR_MESH.json` | Connector/service mesh topology | 📎 Referenced |
| `MEMORY_MESH.json` | Memory system topology | 📎 Referenced |
| `SKILLS_ROUTER.json` | Skill routing rules | 📎 Referenced |
| `WORKFLOW_ROUTER.json` | Workflow orchestration | 📎 Referenced |
| `POINTER_INDEX.json` | File pointer index | 📎 Referenced |
| `PRIVATE_REPO_INDEX.json` | Private repo references | 📎 Referenced |

## Architecture

```
mimo-code/packages/opencode/
├── skills/                    ← Built-in skill registry (NEW)
│   ├── index.json             ← Unified discovery index
│   ├── README.md              ← Registry documentation
│   ├── agents/                ← Vercel ecosystem skills
│   ├── gemini/                ← APEX ecosystem skills
│   ├── grok/                  ← Grok ecosystem skills
│   └── mimo/                  ← MiMo native skills
├── src/
│   ├── skill/
│   │   ├── index.ts           ← Modified: added built-in registry scan
│   │   └── discovery.ts       ← Remote skill discovery
│   ├── flag/
│   │   └── flag.ts            ← Modified: added MIMOCODE_DISABLE_BUILTIN_SKILLS
│   ├── memory/                ← Memory service
│   ├── mcp/                   ← MCP service
│   └── config/
│       └── skills.ts          ← Skills config schema
└── MANIFEST.md                ← This file
```

## Verification

- [x] 60 SKILL.md files with valid frontmatter
- [x] 4 category index.json files for remote discovery
- [x] 1 root index.json for unified discovery
- [x] Built-in registry scan integrated into skill discovery
- [x] MIMOCODE_DISABLE_BUILTIN_SKILLS flag added
- [x] All skills parseable by ConfigMarkdown parser