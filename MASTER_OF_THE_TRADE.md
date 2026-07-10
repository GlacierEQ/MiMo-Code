# MiMo Code CLI — MASTER OF THE TRADE
## Unified Monolith: Skills + Connectors + Excellence

> Single source of truth for all coding agents and CLI agents.
> Combines 60 integrated skills with distributed memory and MCP scaling.

## Core Properties
| Property | Implementation |
|----------|----------------|
| **Free-capable** | `openrouter/free`, `arcee-ai/*:free`, `minimax/*:free` |
| **Cache-reliable** | `memoMap` + `ScopedCache` deduplication |
| **Scalable** | MCP hub with shared state via `INSTANCE_STATE` |
| **Token-savings** | Built-in reference chain (`token-savings` skill) |

## Unified Structure

### Skills Registry (`packages/opencode/skills/`)
```
skills/
├── index.json              ← 60 skills unified discovery
├── MANIFEST.md             ← Integration documentation
├── agents/                 ← 28 skills (Vercel ecosystem)
│   ├── ai-gateway/
│   ├── workflow/
│   ├── vercel-*/
│   └── index.json
├── gemini/                 ← 19 skills (APEX ecosystem)  
│   ├── apex-*/
│   ├── digital-law-library-master/
│   ├── hyper-efficiency-flow/
│   └── index.json
├── grok/                  ← 9 skills (Office/formatting)
│   ├── docx/
│   ├── pptx/
│   ├── xlsx/
│   └── index.json
└── mimo/                  ← 1 skill (native)
    ├── test-runner/
    └── index.json
```

### Memory System (`.apex/`)
```
.apex/
├── MEMORY_MESH.json        ← 6-layer memory topology
├── CONNECTOR_MESH.json     ← MCP/connector routing
├── SKILLS_ROUTER.json      ← Primary skill aliases
├── apex.jsonc              ← Distributed config with free providers
└── skills/apex/skill.json  ← APEX monolith skill definition
```

## Provider Configuration
```json
{
  "model_groups": {
    "free": ["openrouter/free", "openrouter/auto", "arcee-ai/trinity-large-preview:free", "minimax/minimax-m2.5:free", "qwen/qwen3-8b"]
  },
  "distributed": {
    "share_auto": true,
    "mcp_scaling": true,
    "shared_state": "apex/sessions",
    "parallel_processing": true
  }
}
```

## Override Hierarchy
1. User skills (`~/.mimocode/skills/`)
2. Project skills (`./.mimocode/skills/`)
3. External skills (`.claude/`, `.opencode/`, `.codex/`)
4. Built-in skills (`packages/opencode/skills/`, **NEW**)
5. Compose skills (bundled)

## Architecture References
- Memory: `MEMORY_MESH.json` → 6 layers (mem0, supermemory, pinecone, qdrant, context7, memory_plugin)
- Connectors: `CONNECTOR_MESH.json` → colossus-gatekeeper, apex-filesystem, unified-memory
- Routing: `SKILLS_ROUTER.json` → 308 skills with primary/false flags