---
name: token-savings
description: "APEX V2 — World-class token savings for longest, strongest, smartest ops. Synthesized from aspen-grove-core, apex-bootup-core, activate_memory_savings.py, boot_manager.py, coremaximized.sh. Maximizes operational lifespan and cognitive accuracy."
---

# APEX Token-Savings Protocol V2 — WORLD-CLASS EDITION

## 🎯 Core Reference
See [`APEX_CORE.md`](../APEX_CORE.md) for all 10 foundational principles including:
- Topological Surgicality, Surgical File Ops, Parallel Execution, Cache-Hit Protocol
- Diamond Agent Topology, CoreMaximized Profile Flags, Aspen Grove Boot Sequence

---

## 📊 Token vs. Intelligence Scaling Model

```
Surgical Context Injection → High SNR → Maximum Attention Weighting
→ Accurate Logic Generation → Zero Noise → Fast Execution & Low Latency
```

**Key insight from aspen-grove-core**: Agents receiving "book IDs + memory scope" instead of monolithic prompts achieve 27KB+ skill registrations with near-zero per-call token cost.

---

## 🚀 Activation: CoreMaximized Profile
Before ANY session, set these env flags (from `APEX_BOOTUP/profiles/coremaximized.sh`):
```bash
export APEX_PROFILE=coremaximized
source ~/APEX_BOOTUP/apex-bootup.sh coremaximized
# Or for ultra-lean Termux: source ~/APEX_BOOTUP/apex-bootup.sh troubleshoot
```

---

## 🧠 Token Optimizer Cache (from gemini-unified-ops/scripts/activate_memory_savings.py)
```python
# Before any expensive state read, check cache:
query_hash = "stable_key_v1"
cached = optimizer.get_cached(query_hash)
if not cached:
    result = expensive_op()
    optimizer.set_cache(query_hash, result)
    # → Saves ~42.5% tokens on repeat accesses
```

---

## 🔧 Session Discipline Checklist
- [ ] Resolved all paths via `APEX_POINTER_INDEX.json` or `ASPEN_GROVE_CONSTELLATION.json` first?
- [ ] Set `StartLine`/`EndLine` on every `view_file` call?
- [ ] Used `grep_search` with exact patterns + `Includes` globs?
- [ ] Launched independent tasks in parallel (`&` / `invoke_subagent`)?
- [ ] Maintained single living artifact instead of creating new ones?
- [ ] Applied Cache-Hit check before expensive recomputation?
- [ ] Used Diamond Agent facet routing (9-facet topology) for context injection?
- [ ] Ran `multi_replace_file_content` for all multi-section edits in one call?

---

## ⚡ Token Reduction Quick Reference
| Technique | Reduction |
|---|---|
| Pointer index vs. dir scan | ~85% |
| Exact grep vs. full file read | ~70% |
| Cache-hit on repeated state | ~42.5% |
| Parallel vs. sequential ops | N÷1× |
| StartLine/EndLine constraints | ~60–90% |
| Diamond facet routing | ~89% |
| CoreMaximized profile active | Multiplier × all above |

---

## 🌐 GitHub & Local Optimization Resources

### 1. Environment & Profiles
*   **CoreMaximized V2 Profile:** [coremaximized.sh](file:///data/data/com.termux/files/home/APEX_BOOTUP/profiles/coremaximized.sh) — Multiplier flags active.
*   **LightMax Profile:** [lightmax.sh](file:///data/data/com.termux/files/home/APEX_BOOTUP/profiles/lightmax.sh) — Offloads local models, runs cloud agent execution.

### 2. Caching & Optimization Code
*   **Dynamic Background Sentinel:**
    *   Local: [apex_optimizer.py](file:///data/data/com.termux/files/home/gemini-unified-ops/services/apex_optimizer.py)
    *   Packaged: [apex_optimizer.py](file:///data/data/com.termux/files/home/.gemini/skills/token-savings/apex_optimizer.py)
*   **Token Cache Optimizer:**
    *   Interface: [mcp_ecosystem_integration.py](file:///data/data/com.termux/files/home/intelligence/aspen-grove-operator-v7/mcp_ecosystem_integration.py)
    *   Execution Trigger: [activate_memory_savings.py](file:///data/data/com.termux/files/home/.gemini/skills/token-savings/activate_memory_savings.py)
*   **Stats Registry:** [optimizer_stats.json](file:///data/data/com.termux/files/home/.apex_cache/optimizer_stats.json)

### 3. GlacierEQ Ecosystem Repos
| Repo | Token-Savings Artifact |
|---|---|
| [aspen-grove-core](https://github.com/GlacierEQ/aspen-grove-core) | `BOOTUP_PROTOCOL.md`, `SKILLS_MANIFEST.json` |
| [apex-bootup-core](https://github.com/GlacierEQ/apex-bootup-core) | `profiles/coremaximized.sh`, `profiles/troubleshoot.sh` |
| [apex-boot-core](https://github.com/GlacierEQ/apex-boot-core) | `APEX_MAXIMIZED_WORKFLOW.py`, `helix_orchestrator.py` |
| [Z-BACKUP-aspen-grove-operator-v7](https://github.com/GlacierEQ/Z-BACKUP-aspen-grove-operator-v7) | `core/boot_manager.py`, `mcp_ecosystem_integration.py` |
| [gemini-unified-ops](https://github.com/GlacierEQ/gemini-unified-ops) | `scripts/activate_memory_savings.py` |

