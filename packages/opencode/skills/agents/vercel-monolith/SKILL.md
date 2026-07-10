---
name: vercel-monolith
description: Unified Vercel expertise — Functions, Storage, Agent, Workflow, and Runtime Cache in single activation. Reduces chain overhead for full-stack Vercel development.
metadata:
  priority: 10
  docs:
    - "https://vercel.com/docs"
    - "https://vercel.com/docs/functions"
    - "https://vercel.com/docs/storage"
    - "https://vercel.com/docs/workflow"
  pathPatterns:
    - 'api/**/*.*'
    - 'app/**/route.*'
    - 'lib/**'
    - 'vercel.json'
  mergeSources:
    - vercel-functions
    - vercel-storage
    - vercel-agent
    - workflow
    - runtime-cache
    - ai-sdk
retrieval:
  aliases:
    - vercel fullstack
    - vercel unified
    - vercel monolith
  intents:
    - build vercel app
    - deploy full-stack
    - optimize vercel
    - full vercel setup
---

# Vercel Monolith — MASTER OF THE TRADE

> Unified skill combining Functions, Storage, Agent, Workflow, Runtime Cache, and AI SDK.
> **Single activation** provides complete Vercel stack coverage.

## When to Use

- Building full-stack Vercel applications
- Need Functions + Storage + AI in one context
- Deploying applications with background jobs
- Optimizing serverless with caching

## Complete Stack Coverage

| Domain | Skill | Coverage |
|--------|-------|----------|
| **Compute** | vercel-functions | Serverless, Edge, Fluid, Cron |
| **Storage** | vercel-storage | Blob, Edge Config, Neon, Upstash, Supabase |
| **AI** | vercel-agent + ai-sdk | Code review, streaming, tools |
| **Workflow** | workflow | Durable jobs, retries, pause/resume |
| **Cache** | runtime-cache | Region-aware caching |

## Quick Reference

### Function + Storage + AI Stack
```ts
// app/api/chat/route.ts — Full Vercel stack
import { neon } from '@neondatabase/serverless'
import { Redis } from '@upstash/redis'
import { getCache } from '@vercel/functions'
import { streamText } from 'ai'
import { openai } from '@ai-sdk/openai'

export async function POST(req: Request) {
  // Cache layer
  const cache = getCache()
  const cached = await cache.get('model-config')

  // Database layer (Neon)
  const sql = neon(process.env.DATABASE_URL!)
  
  // Cache/store layer (Upstash)
  const redis = Redis.fromEnv()
  const session = await redis.get(`session:${req.headers.get('x-session')}`)

  // AI streaming (OpenAI via AI SDK)
  const result = await streamText({
    model: openai('gpt-4o'),
    messages: req.messages,
  })

  return result.toUIMessageStreamResponse()
}
```

### Workflow Background Jobs
```ts
// app/api/slow-task/route.ts
import { put } from '@vercel/blob'
import { workflow } from '@vercel/workflow'

export const { POST } = workflow({
  async process() {
    // Long-running task in Workflow
    const result = await heavyComputation()
    return put('results/data.json', result)
  }
})
```

## Deprecation Mappings

| Old Package | New Package | Migration |
|------------|-------------|-----------|
| `@vercel/postgres` | `@neondatabase/serverless` | `neon(process.env.DATABASE_URL!)` |
| `@vercel/kv` | `@upstash/redis` | `Redis.fromEnv()` |

## Official Documentation

- [Vercel Functions](https://vercel.com/docs/functions)
- [Vercel Storage](https://vercel.com/docs/storage)
- [Vercel AI SDK](https://sdk.vercel.ai)