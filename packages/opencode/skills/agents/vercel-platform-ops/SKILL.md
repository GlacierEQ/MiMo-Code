---
name: vercel-platform-ops
description: Vercel platform operations — CLI commands, deployment management, OAuth connect, CI/CD workflows. Use when deploying, managing env vars, configuring CI, or interacting with Vercel from CLI.
merged_from: [vercel-cli, deployments-cicd, vercel-connect]
---

# Vercel Platform Ops (CLI + Deploy + Connect)

Single skill covering: Vercel CLI, deployment promotion/rollback, OAuth token flow, CI/CD configuration.

---

## 1. Vercel CLI

```bash
# Deploy
vercel --prod
vercel --prebuilt

# Environment
vercel env ls
vercel env add
vercel env pull .env.local

# Logs
vercel logs
vercel logs --follow

# Metrics
vercel metrics

# Domains
vercel domains ls
vercel domains add example.com

# Inspection
vercel inspect <deployment-url>
```

### vercel.json Configuration
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "functions": { "api/**/*.ts": { "maxDuration": 30 } }
}
```

---

## 2. Deployment Management

```bash
# Promote to production
vercel promote <deployment-url>

# Rollback
vercel rollback

# Build with --prebuilt
vercel build --prebuilt
vercel deploy --prebuilt

# CI Workflow (GitHub Actions)
- uses: amondnet/vercel-action@v25
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-args: '--prod'
    vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
    vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

# Cron Jobs (vercel.json)
{ "crons": [{ "path": "/api/cron", "schedule": "0 * * * *" }] }
```

---

## 3. OAuth Connect

```typescript
import { createVercelClient } from '@vercel/connect';

const client = createVercelClient({
  clientId: process.env.VERCEL_CLIENT_ID,
  clientSecret: process.env.VERCEL_CLIENT_SECRET,
});

// Get scoped OAuth token
const token = await client.getToken({
  service: 'github', // or 'slack', 'mcp', 'snowflake'
  scope: ['repo', 'read:org'],
});

// Use with Vercel API
const res = await fetch('https://api.vercel.com/v9/projects', {
  headers: { Authorization: `Bearer ${token}` },
});
```

### OIDC Token
```bash
# Get OIDC token for third-party services
curl -H "Authorization: Bearer ${VERCEL_OIDC_TOKEN}" \
  https://api.vercel.com/v1/oidc/token
```

---

## Usage Triggers
- "Vercel deploy", "vercel env", "vercel logs"
- "Deploy to production", "rollback"
- "OAuth token", "Vercel connect"
- "CI/CD", "GitHub Actions"
- "vercel.json", "deployment"
