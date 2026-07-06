---
name: apex-gemma4-omni-node
description: "The Best To Ever Do It: A ground-up Omni Node fusing Apex Gemma 4, Aspen Grove Token Savings, Stealth Claw, FileBoss, and Mega-PDF. Includes an offline native Ollama fallback."
---

# APEX GEMMA 4 OMNI NODE (PRIMORDIAL MESH TITAN)

## 🎯 Core Directive
This skill dictates the invocation of the ultimate bottom-up execution engine located at `~/APEX_GEMMA_4_OMNI_NODE/src/core_engine.py`. 
Use this skill when processing massive file structures, extracting heavy PDF discovery batches, or synthesizing legal/structural logic where **maximum token savings** and **offline resilience** are required.

## 🧬 Architectural Components
This node does not execute linearly. It uses `asyncio.gather` to trigger massive parallel ingestion:
1. **FileBoss**: Dominates filesystem and symlink arrays.
2. **Mega-PDF**: Strips raw text and vectors from discovery dumps.
3. **Stealth Claw**: Ingests ambient environmental/edge data.
4. **Apex Gemma 4**: Fuses all inputs into pure cognitive synthesis.
5. **Aspen Grove**: Hashes the final state (SHA-256) to `.apex_cache/gemma4_omni`. Future identical requests reclaim **95% token overhead** instantly.

## ⚙️ Offline / Fallback Supremacy
If cloud API quotas are exceeded, `ApexGemma4Bridge` automatically drops the cloud requirement and routes the context directly to the local Termux environment via:
```bash
ollama run apex-gemma4 "<prompt>\nContext: <context>"
```
This requires `ollama serve` to be running.

## 🚀 Execution Pattern

When invoking this skill to solve a heavy task, invoke the `core_engine.py` script directly via Python. 
Modify the `execute_prime_directive` arguments as needed to target specific PDFs or directories.

### Base Invocation:
```python
import sys
import asyncio
sys.path.append("/data/data/com.termux/files/home/APEX_GEMMA_4_OMNI_NODE/src")

from core_engine import BestToEverDoItEngine

engine = BestToEverDoItEngine()
result = asyncio.run(engine.execute_prime_directive(
    task_payload="Extract and synthesize all RICO overlaps",
    target_pdf="/path/to/evidence.pdf",
    structure_dir="/path/to/vault"
))
print(result)
```

## 🛠️ Diagnostics & Maintenance
- **Cache Location**: `~/.apex_cache/gemma4_omni/`
- **Model Registration**: The local model is registered via `~/APEX_GEMMA_4_OMNI_NODE/Modelfile`. To rebuild, run `ollama create apex-gemma4 -f Modelfile`.
