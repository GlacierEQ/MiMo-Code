---
name: nextjs-ecosystem
description: Complete Next.js ecosystem — App Router, Server Components, Cache Components (PPR, use cache), version migration, Turborepo monorepo. Use when building Next.js apps, optimizing caching, upgrading versions, or working with next-forge.
merged_from: [nextjs, next-cache-components, next-upgrade, next-forge]
---

# Next.js Ecosystem (Complete Framework)

Single skill covering: App Router, Server Components, Cache Components, PPR, version migration, Turborepo monorepo.

---

## 1. App Router & Server Components

```tsx
// app/page.tsx — Server Component (default)
export default async function Page() {
  const data = await fetchData();
  return <div>{data.title}</div>;
}

// app/client.tsx — Client Component
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// Server Action
'use server';
export async function submitForm(formData: FormData) {
  await db.insert(formData);
  revalidatePath('/');
}
```

### Data Fetching Patterns
```tsx
// Parallel data fetching
const [user, posts] = await Promise.all([
  getUser(id),
  getPosts(userId),
]);

// Streaming with Suspense
<Suspense fallback={<Skeleton />}>
  <SlowComponent />
</Suspense>
```

---

## 2. Cache Components (PPR)

```tsx
// PPR (Partial Prerendering)
export const experimental_ppr = true;

// use cache directive
async function getProduct(id: string) {
  'use cache';
  return await db.product.findUnique({ where: { id } });
}

// Cache tags
import { cacheTag } from 'next/cache';
async function getPosts() {
  'use cache';
  cacheTag('posts');
  return await db.post.findMany();
}

// Revalidate by tag
import { revalidateTag } from 'next/cache';
revalidateTag('posts');

// cacheLife — configure cache duration
import { cacheLife } from 'next/cache';
cacheLife('hours');
```

---

## 3. Version Migration

```bash
# Run codemods
npx @next/codemod@latest upgrade

# Breaking changes checklist
- next/image → use fill or explicit width/height
- next/link → no more <a> child needed
- Pages Router → App Router migration
```

### Common Codemods
| Codemod | Purpose |
|---------|---------|
| `next-image-to-legacy` | Migrate to new Image component |
| `app-dir-autorender` | Auto-add 'use client' where needed |
| `with-server-action` | Add 'use server' to Server Actions |

---

## 4. next-forge (Turborepo Monorepo)

```bash
# Initialize
npx next-forge init my-project

# Structure
my-project/
├── apps/
│   ├── web/          # Main Next.js app
│   └── app/          # Marketing site
├── packages/
│   ├── ui/           # Shared components (@repo/ui)
│   ├── database/     # Prisma schema (@repo/database)
│   └── types/        # Shared types (@repo/types)
├── turbo.json
└── package.json
```

### Workspace Packages
```json
// apps/web/package.json
{
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/database": "workspace:*"
  }
}
```

---

## Key Patterns

| Pattern | When to Use |
|---------|-------------|
| Server Components | Data fetching, SEO, initial render |
| Client Components | Interactivity, state, browser APIs |
| Server Actions | Form submissions, mutations |
| `use cache` | Expensive computations |
| PPR | Static shell + dynamic islands |
| Streaming | Progressive loading |

---

## Usage Triggers
- "Next.js", "App Router", "Server Component"
- "Cache Components", "PPR", "use cache"
- "next-forge", "Turborepo", "monorepo"
- "Upgrade Next.js", "codemod"
- "cacheLife", "cacheTag", "revalidateTag"
