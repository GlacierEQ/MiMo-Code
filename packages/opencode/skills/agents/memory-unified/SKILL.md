---
name: memory-unified
description: Unified memory infrastructure — Mem0, Supermemory, Pinecone, Qdrant, Neo4j, Notion. Zero-token caching, dual-memory prime, semantic search, knowledge graphs. Use when building persistent memory, personalization, RAG, or cross-session context retention.
merged_from: [supermemory, supermemory-cli, memory-connect, unified-memory-connect]
---

# Memory Unified (APEX Hybrid Memory Stack)

Single skill covering all memory layers: Mem0 (episodic), Supermemory (knowledge), vector DBs (Pinecone/Qdrant), graph DBs (Neo4j), and Notion workspace.

---

## Architecture

```
Agent Input → Memory Unified Gateway
                ├── Mem0 Cloud (Pro + Regular) — episodic/session memory
                ├── Supermemory (Primary + Secondary) — knowledge/durable memory
                ├── Pinecone (apex-main) — vector search
                ├── Qdrant (local:6333) — vector search
                ├── Neo4j — graph relationships
                └── Notion — workspace database
```

**Zero-token caching:** SHA-256 hash of query → local cache → 0ms/0 tokens on hit.

---

## 1. Supermemory API

### TypeScript
```typescript
import { Supermemory } from 'supermemory';
const client = new Supermemory({ apiKey: process.env.SUPERMEMORY_API_KEY });

// Profile + memories
const context = await client.profile({ containerTag: "user_123", query: "preferences" });

// Add memory
await client.add({ content: text, containerTag: "user_123", metadata: { type: "conversation" } });
```

### Python
```python
from supermemory import Supermemory
client = Supermemory(api_key=os.environ["SUPERMEMORY_API_KEY"])
context = client.profile(container_tag="user_123", query="preferences")
client.add(content=text, container_tag="user_123", metadata={"type": "conversation"})
```

---

## 2. Supermemory CLI (`sm-ops`)

### Setup
```bash
npm install -g supermemory
supermemory login --api-key sm_abc_xxx
sm-ops init --scope project --tag apex-home
```

### Core Commands

| Command | Purpose |
|---------|---------|
| `sm-ops prime "task"` | Inject minimal context (~1200 tokens) before agent call |
| `sm-ops intel "query"` | High-intelligence context (profile + hybrid search) |
| `sm-ops recall "query"` | Semantic search with rerank + rewrite |
| `sm-ops save "outcome" --durable` | Dual-write to Mem0 + Supermemory |
| `sm-ops ingest` | Batch-ingest sitemap (priority-ordered) |
| `sm-ops status` | Dashboard: credits, ingestion, failed URLs |
| `sm-ops tokens` | Track token savings |

### CLI Commands

```bash
# Add content
supermemory add "User prefers TypeScript" --tag user_123
supermemory add ./docs.pdf --tag docs
supermemory add https://example.com --tag links

# Search
supermemory search "auth patterns" --tag api --limit 5 --rerank
supermemory search "user prefs" --mode hybrid

# Remember (direct memory)
supermemory remember "User is senior engineer" --static --tag user_123

# Profile
supermemory profile user_123 --query "programming preferences"

# Documents
supermemory docs list --tag default
supermemory docs status doc_abc123

# Tags
supermemory tags list
supermemory tags merge old-tag --into new-tag

# API Keys
supermemory keys create --name my-agent --permission write

# Connectors
supermemory connectors connect google-drive --tag docs
supermemory connectors sync conn_abc123
```

---

## 3. Mem0 Integration

### REST API
```http
POST https://api.mem0.ai/v1/memories/
Authorization: Token <api_key>
x-mem0-org-id: <org_id>
x-mem0-project-id: <project_id>

{
  "messages": [{"role": "user", "content": "I prefer dark mode"}],
  "user_id": "casey",
  "version": "v2",
  "infer": true
}
```

### Python SDK
```python
from mem0 import MemoryClient

client = MemoryClient(api_key="...", org_id="...", project_id="...")

# Add memory
client.add("I prefer dark mode", user_id="casey", version="v2")

# Search memory
results = client.search("user preferences", filters={"user_id": "casey"})
```

### Key Rules
- Always use `version="v2"` (v1 is deprecated)
- Pass `user_id` at top level for `.add()`, inside `filters` dict for `.search()`
- Set `immutable=true` for critical operational rules
- Filter unsupported kwargs when using local Memory class

---

## 4. Unified Memory Layers

| Layer | Variable | Purpose |
|-------|----------|---------|
| Mem0 Pro | `MEM0_PRO_API_KEY` | Enterprise tenancy |
| Mem0 Regular | `MEM0_REG_API_KEY` | Personal memory |
| Supermemory Primary | `SUPERMEMORY_PRIMARY_KEY` | Knowledge base |
| Pinecone | `PINECONE_PRIMARY_KEY` | Vector search (1536 dim) |
| Qdrant | `QDRANT_KEY` | Local vector DB (:6333) |
| Notion | `NOTION_API_KEY` | Workspace database |

### Zero-Token Cache Protocol
1. Compute SHA-256 of search query
2. Check `~/.apex_cache/memory_hits.json`
3. If match → return cached context (0ms, 0 tokens)
4. If miss → query API, cache result, return

---

## 5. Dual-Memory Prime

| Store | Role | Best For |
|-------|------|----------|
| **Mem0** | Episodic / session | Recent facts, user prefs, task state |
| **Supermemory** | Knowledge / durable | Docs, architecture, long-term patterns |

### Token Budget
- Default: **1200 tokens**/prime vs ~8k full history
- Config: `data/token_config.json`

### Prime Flow
```bash
# Before agent call — minimal context
sm-ops prime "implement auth middleware"

# After session — dual-write
sm-ops save "Fixed apex-gateway auth" --durable
```

---

## 6. Workspace References

| File | Purpose |
|------|---------|
| `scripts/unified_memory_mcp.py` | FastMCP UnifiedMemory server |
| `scripts/verify_mem0_layers.py` | Connectivity diagnostics |
| `scripts/organize_memories.py` | Memory organization |
| `scripts/guard_signal9.sh` | Process monitoring |
| `mem0_master_apex.py` | 5-tier execution testing |
| `~/.apex_cache/memory_hits.json` | Zero-token cache |

---

## Usage Triggers
- "Memory", "recall", "remember", "forget"
- "Semantic search", "knowledge graph"
- "Persistent context", "user profile"
- "Dual-memory", "prime", "sm-ops"
- "Mem0", "Supermemory", "Pinecone", "Qdrant", "Neo4j"
- "Zero-token cache", "token savings"
