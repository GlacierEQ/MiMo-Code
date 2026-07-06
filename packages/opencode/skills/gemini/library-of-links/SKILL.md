---
name: library-of-links
description: Orchestrates and resolves external links, repository anchors, and diagnostic maps.
---

# APEX Library of Links (Navigation & Resolution)

## Overview
This skill anchors the agent's spatial awareness across the distributed APEX framework. It prevents context fragmentation by providing a structured directory of operational domains, triggers, and configuration endpoints.

## Core Reference
See `APEX_CORE.md` for foundational principles regarding Topological Surgicality, Surgical File Operations, State Management, and Verification Gates.

## Core Navigation Map
Invoke this skill to rapidly map local resources to their corresponding GitHub repositories or cloud nodes:

| Module | Purpose | Trigger / Reference | Local Path / Remote |
| :--- | :--- | :--- | :--- |
| **DOCTOR-STRANGE** | Master Orchestration | `gemini --target DOCTOR-STRANGE` | [GlacierEQ/DOCTOR-STRANGE-OMNISCIENT-ORCHESTRATOR](https://github.com/GlacierEQ/DOCTOR-STRANGE-OMNISCIENT-ORCHESTRATOR) |
| **God-Mind** | Cognitive Engine | `gemini --target God-Mind` | [GlacierEQ/God-Mind](https://github.com/GlacierEQ/God-Mind) |
| **aspen-grove-core** | Spiral Engine Core | `apex-pipeline-init legal` | [GlacierEQ/aspen-grove-core](https://github.com/GlacierEQ/aspen-grove-core) |
| **apex-fs-commander** | Legal Intel Node | Set `APEX_MODE="legal"` | [GlacierEQ/apex-fs-commander](https://github.com/GlacierEQ/apex-fs-commander) |
| **Stealth Claw** | Stealth Operations | `activate_stealth.sh` | [GlacierEQ/stealth-claw](https://github.com/GlacierEQ/stealth-claw) |

## Operational Resolution Protocol
1. **Check System Integrity**: Run `bash ~/APEX_BOOTUP/diagnostic.sh`.
2. **Resolve Cross-Repo Paths**: Read `~/APEX_BOOTUP/MISSION_LINK_LIBRARY.md` to map dependencies before launching background pipelines or initializing subagents.
3. **Link to Artifacts**: When creating markdown artifacts, strictly link to local files using absolute file URIs (`file:///...`) for flawless user navigation.
