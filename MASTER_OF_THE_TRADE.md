# MiMo Code CLI — MASTER OF THE TRADE
## Unified Monolith: Skills + Connectors + Excellence

> Single source of truth for all coding agents and CLI agents.
> Combines **62 skills** with distributed memory and MCP scaling.
> **2 monolith skills** reduce activation overhead.

## Core Properties
| Property | Implementation |
|----------|----------------|
| **Free-capable** | `openrouter/free`, `arcee-ai/*:free`, `minimax/*:free`, `qwen/*`, `ollama/*`, `huggingface/*`, `google/gemini-2.0-flash-exp`, `together/meta-llama/Llama-3.3-70B-Instruct-Turbo-Free` |
| **Cache-reliable** | `memoMap` + `ScopedCache` deduplication |
| **Scalable** | MCP hub with shared state via `INSTANCE_STATE` |
| **Token-savings** | Built-in via `token-savings` skill + monoliths |

## Unified Structure

### Skills Registry (`packages/opencode/skills/`)
```
skills/
├── index.json              ← 62 skills unified discovery
├── MANIFEST.md             ← Integration documentation
├── agents/                 ← 29 skills (Vercel ecosystem + monolith)
│   ├── vercel-monolith     ← Functions+Storage+AI+Workflow unified
│   └── index.json
├── gemini/                 ← 20 skills (APEX ecosystem + monolith)
│   ├── apex-monolith       ← hyper-efficiency+memory+connectors unified
│   └── index.json
├── grok/                  ← 9 skills (Office/formatting)
│   └── index.json
└── mimo/                  ← 1 skill (native)
    └── index.json
```

### Memory System (`.apex/`)
```
.apex/
├── MEMORY_MESH.json        ← 6-layer memory topology
├── CONNECTOR_MESH.json       ← MCP/connector routing
├── SKILLS_ROUTER.json        ← Primary skill aliases (308 skills)
├── apex.jsonc              ← Distributed config with free providers
└── skills/apex/skill.json  ← APEX monolith definition
```

## Monolith Skills (Reduced Overhead)

### vercel-monolith
Merges 6 related skills into single activation:
- `vercel-functions` + `vercel-storage` + `vercel-agent` + `workflow` + `runtime-cache` + `ai-sdk`

### apex-monolith
Merges 8 related skills into single activation:
- `hyper-efficiency-flow` + `token-savings` + `memory-connect` + `unified-memory-connect` + `sequential-thinking` + `universal-connector` + `apex-semantic-router` + `operator-is-the-universe`

## Provider Configuration
```json
{
  "model_groups": {
    "free": [
      "openrouter/free", "openrouter/auto",
      "arcee-ai/trinity-large-preview:free",
      "minimax/minimax-m2.5:free",
      "qwen/qwen3-8b",
      "ollama/llama3.2:3b",
      "huggingface/meta-llama/Llama-3.2-3B-Instruct",
      "google/gemini-2.0-flash-exp",
      "together/meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    ]
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
4. Built-in skills (`packages/opencode/skills/`)
5. Compose skills (bundled)