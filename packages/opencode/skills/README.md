# MiMo Code Extended Skills Registry

This directory contains skills integrated from the mimo-config-backup repository.

## Structure

- **agents/** - Vercel ecosystem skills (ai-gateway, workflow, vercel-*, etc.)
- **gemini/** - APEX ecosystem skills (apex-*, digital-law-library, sovereign-operator, etc.)
- **grok/** - Grok ecosystem skills (docx, pptx, xlsx, etc.)
- **mimo/** - MiMo native skills (test-runner, etc.)

## Skill Sources

Skills are auto-discovered via the Skill service which scans:
1. `.mimocode/skills/**/*.SKILL.md` (project-local)
2. `~/.mimocode/skills/**/*.SKILL.md` (user-global)
3. Config paths in `opencode.json` → `skills.paths`
4. Remote URLs in `opencode.json` → `skills.urls` (requires `index.json`)

## Integration Status

- ✅ agents_skills (32 skills) → /skills/agents/
- ✅ gemini_skills (19 skills) → /skills/gemini/
- ✅ grok_skills (9 skills) → /skills/grok/
- ✅ mimocode_skills (1 skill) → /skills/mimo/

Total: 61 skills integrated