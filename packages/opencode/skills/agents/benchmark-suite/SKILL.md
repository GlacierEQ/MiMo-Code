---
name: benchmark-suite
description: Complete testing & evaluation — benchmark agents, e2e pipelines, sandbox eval, plugin audit, hook verification. Use when testing vercel-plugin, measuring skill injection coverage, or running eval scenarios.
merged_from: [benchmark-agents, benchmark-e2e, benchmark-sandbox, benchmark-testing, vercel-plugin-eval, plugin-audit]
---

# Benchmark Suite (Complete Testing & Evaluation)

Single skill covering: agent benchmarks, e2e pipelines, sandbox eval, plugin audit, hook verification, coverage reports.

---

## Architecture

```
BENCHMARK SUITE
├── Agent Benchmark — WezTerm interactive sessions
├── E2E Pipeline — create → build → verify → analyze
├── Sandbox Eval — Firecracker microVM provisioning
├── Plugin Audit — JSONL log parsing, hook matching
├── Hook Verification — Real Claude Code sessions
└── Coverage Reports — Structured scoring
```

---

## 1. Agent Benchmark

```bash
# Launch WezTerm pane with Claude Code
benchmark-agents launch --prompt "Implement auth middleware"

# PostToolUse validation
benchmark-agents validate --session <id> --hook <hook_name>

# Coverage report
benchmark-agents report --session <id>
```

---

## 2. E2E Pipeline

```bash
# 4-stage pipeline
benchmark-e2e run --mode full
# Stages: create → build → verify → analyze

# Quick mode
benchmark-e2e run --mode quick

# Improvement report
benchmark-e2e report --output improvement-report.md
```

---

## 3. Sandbox Eval

```bash
# Firecracker microVM provisioning
benchmark-sandbox provision --model claude-code

# 3-phase eval
benchmark-sandbox run --phase BUILD,VERIFY,DEPLOY

# Haiku scoring
benchmark-sandbox score --format structured
```

---

## 4. Plugin Audit

```bash
# Parse JSONL logs
plugin-audit parse --log conversation.jsonl

# Test hook matching
plugin-audit test --input "actual tool calls"

# Pattern coverage gap analysis
plugin-audit gaps --report coverage.md
```

---

## 5. Hook Verification

```bash
# Real Claude Code session
vercel-plugin-eval launch --verify-hooks

# Dedup correctness
vercel-plugin-eval dedup --test-cases cases.json

# Skill injection verification
vercel-plugin-eval inject --skill <name>
```

---

## 6. Coverage Reports

| Metric | Description |
|--------|-------------|
| Hook Coverage | % of tool calls matched by hooks |
| Skill Injection | % of skills successfully loaded |
| Dedup Correctness | % of dedup rules working |
| Pattern Coverage | % of patterns tested |

---

## Usage Triggers
- "Run benchmark", "test plugin"
- "E2E pipeline", "sandbox eval"
- "Plugin audit", "hook verification"
- "Coverage report", "skill injection"
