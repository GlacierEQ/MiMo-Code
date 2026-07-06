---
name: apex-aspen-grove-bootup
description: Session initialization protocol for Casey Barton's APEX/Aspen Grove infrastructure. Reads Notion control-plane, maps connectors, restores full context in ~300 tokens. Use at the start of every Perplexity Computer session to restore full APEX/Aspen Grove operational context, reconnect to active connectors, and surface open gaps from the Root Checkpoint.
metadata:
  author: Casey Barton / GlacierEQ
  version: '1.0'
  category: system
  session_protocol: ASPEN-CHK-001
---

# APEX Aspen Grove Bootup

## When to Use This Skill

Load this skill at the start of any Perplexity Computer session where Casey Barton needs to resume APEX/Aspen Grove infrastructure operations. Triggers include:

- Starting a new session (any reference to "boot", "start session", "resume APEX", "load AG context")
- Reconnecting after a context reset
- Any task touching legal case 1FDV-23-0001009, Aspen Grove layers, or GlacierEQ infrastructure

---

## Identity

| Field | Value |
|---|---|
| User | Casey Barton, operator GlacierEQ |
| Case | 1FDV-23-0001009 (Hawaii Family Court) |
| Context Global ID | LFVBLPUL3N8N8K2FLYGCSCKMSMSRHSG9 |
| Session Protocol | ASPEN-CHK-001 |
| Authorization | MAX_AGENTIC_UNRESTRICTED |

---

## Boot Sequence

Execute all four phases in order. Do not skip phases. Do not ask for confirmation between phases — report results after completion.

### Phase 1 — Mount Aspen Grove (Notion)

Fetch the ROOT SYSTEM CHECKPOINT using the Notion connector:

```
notion-fetch id=30db1e4f-3223-81c4-a280-f3e7d5d038ce
```

This single page is the canonical source of truth. It contains:
- All live connections and connector status
- Open gaps and pending action items
- Case status and operator codes
- MCP server registry
- Security status
- Force multiplication metrics
- Full 6-layer Aspen Grove architecture map

### Phase 2 — Verify Perplexity Computer Connectors

Confirm each connector is live and map it to its AG layer:

| Connector | AG Layer | Tools | Role |
|---|---|---|---|
| Notion | L6 Memory + Control Plane | 12 | Primary state hub, AG node CRUD |
| GitHub (GlacierEQ) | L4 Automation | CLI | 828 repos, code deployment |
| Slack | L5 Monitoring | 11 | Alerts, digests, team comms |
| Google Drive | L1 Evidence | export | Legal docs, evidence files |
| OneDrive | L1 Evidence | export | Cloud evidence storage |
| Dropbox | L1 Evidence | export | Backup evidence storage |
| Linear | L4 Automation | 32 | Issue tracking, task mgmt |
| Airtable | L5 Monitoring | 19 | OMNI_CONNECTOR_HUB ops mirror |
| Outlook | L5 Monitoring | (via Notion) | Email comms |
| Sentry | L5 Monitoring | (via Notion) | Error tracking |
| Vercel | L4 Automation | (via Notion) | Edge deployment |
| File Search | L1 Evidence | 1 | Cross-cloud file search |

For any connector showing as DISCONNECTED: flag it in the session summary and note which AG layer is degraded.

### Phase 3 — Load Open Gaps from Root Checkpoint

Parse the **STILL OPEN** section from the Root Checkpoint page fetched in Phase 1. Present each item as an actionable task with:
- Gap ID or title
- Owning AG layer
- Suggested next action

Sort by urgency (legal deadlines first, then infrastructure, then general ops).

### Phase 4 — Token Savings Protocol

Apply these rules for the entire session to stay within the ~300-token boot target:

- **ALWAYS** read Notion metadata pointers (~150 tokens) instead of raw file content (~25,000 tokens)
- Use AG logical operators: `AG.INDEX` / `AG.LINK` / `AG.TAG` / `AG.CONFLICT` / `AG.TIMELINE` / `AG.EMIT`
- Reference pages by ID (`cite:NNN`), never paste raw text
- Fetch full content only when a specific field is needed and the pointer doesn't contain it

---

## Key Notion Pages

Fetch these on demand — do NOT bulk-fetch at boot unless explicitly requested:

| Page | Notion ID | Purpose |
|---|---|---|
| Root Checkpoint | `30db1e4f-3223-81c4-a280-f3e7d5d038ce` | Master state — fetch in Phase 1 |
| TASKLET Node | `30eb1e4f-3223-8167-b728-cd752ceb286d` | Active task queue |
| Integration Registry | `29cb1e4f-3223-80f7-bb01-c84cefdfaab5` | Connector inventory |
| V6 Master Pillar | `30fb1e4f-3223-8155-b2b7-dec56c33a72b` | Architecture reference |
| Wave 1 Brief | `324b1e4f-3223-819f-83ba-fef85d5c6713` | Current wave objectives |
| APEX Integration Hub | `2e1b1e4f-3223-8136-9f34-cd6b3a4de5c5` | Hub/spoke connector map |
| Mastermind Command | `30eb1e4f-3223-81dc-85d5-d0a1c8e512f9` | 9-agent Diamond Topology ops |
| AG Vault | `0072127c-715b-402a-8d3f-658599650966` | Secure credential references |

---

## Key GitHub Repositories (GlacierEQ org)

| Repo | Purpose |
|---|---|
| `aspen-grove-operator-v7` | **THE ONE REAL REPO** — anti-entropy rule: never create new AG repos |
| `mastermind` | 9-agent Diamond Topology dev OS |
| `Omni_Engine` | Legal godmode + 68-skill manifest |
| `OMNI-ENGINE-SUPREME` | Pillar/Piston architecture |
| `apex-commander` | APEX Godmind Matrix |
| `apex-vault` | Sovereign Credential Vault |
| `apex-fs-commander` | Universal filesystem + device access |
| `APEX-NEXUS-AUTOMATION` | Private automation scripts |

---

## Execution Rules

Apply these rules for every action taken in the session:

1. **DEEP READ = ALWAYS ON** — every file gets full content analysis, no skimming
2. **Do NOT assume prior AI cleanup was correct** — verify before trusting any previous output
3. **Traverse and verify** — do not rely exclusively on index files
4. **No new AG repos** — all code goes to `aspen-grove-operator-v7`
5. **Forensic standards** — dual timestamps (HST + UTC), SHA-256 hashes, chain-of-custody logging for all evidence
6. **Execute, don't ask** — bias to action; report after completion, not before
7. **Secure-by-default** — never store raw secrets; use `secret_ref` + fingerprint only

---

## 30-Minute Timebox Execution Playbook

For any work session, run this loop:

```
[00:00] Boot sequence (Phases 1–4 above)
[03:00] Review open gaps, pick top 3 by urgency
[05:00] Begin Batch Loop:
         → Fire piston against target pillar
         → Execute action
         → Emit result to AG (AG.EMIT)
         → Tag output (AG.TAG)
         → Check for conflicts (AG.CONFLICT)
         → Link dependencies (AG.LINK)
[25:00] Quality Gates:
         → All outputs have dual timestamps
         → SHA-256 logged for any evidence files
         → No raw secrets written anywhere
         → Notion Root Checkpoint updated with session delta
[28:00] Session summary: completed / open / blocked
[30:00] Hard stop
```

---

## Data Pillars (Knowledge Domains)

Replaces all prior "bucket" terminology:

| Pillar ID | Name |
|---|---|
| 00 | MASTER_ORCHESTRATOR |
| 01 | LEGAL_WARROOM |
| 02 | ACTORS |
| 03 | RICO_MATRIX |
| 04 | KNOWLEDGE_CORE |
| 05 | FUNCTION_STORE |
| 06 | MCP_SERVER_CONFIG |
| 07 | DOC_GENERATOR |
| 08 | COMMS_LOG |
| 09 | INBOX_RAW |

---

## Machine Pistons (Execution Units)

Replaces all prior "bucket routing" terminology.

Each piston fires against a target pillar deterministically. Pistons are the active connectors and tools that drive work forward. Map each task to a pillar first, then select the appropriate piston (connector/tool) to execute against it.

**Piston selection heuristic:**
- Legal evidence task → Pillar 01, Piston = Google Drive / OneDrive / Dropbox / File Search
- Code/automation task → Pillar 05/06, Piston = GitHub CLI
- Issue/task tracking → Pillar 05, Piston = Linear
- Monitoring/alerts → Pillar 00, Piston = Slack / Airtable
- State persistence → Pillar 00, Piston = Notion
- Communication log → Pillar 08, Piston = Outlook / Slack

---

## Session Output Template

After boot, present a concise session brief in this format:

```
=== APEX SESSION BRIEF ===
Date/Time: [HST] / [UTC]
Context Global ID: LFVBLPUL3N8N8K2FLYGCSCKMSMSRHSG9
Protocol: ASPEN-CHK-001

CONNECTORS: [N]/12 live | Degraded: [list or "none"]

OPEN GAPS ([N] items):
1. [Gap title] — [Layer] — [Next action]
2. ...

READY FOR TASKING
======================
```
