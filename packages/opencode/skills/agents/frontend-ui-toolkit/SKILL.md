---
name: frontend-ui-toolkit
description: Complete frontend UI — React best practices, shadcn/ui components, SVG animations, Tailwind CSS. Use when building React components, installing shadcn, creating SVG animations, or styling with Tailwind.
merged_from: [react-best-practices, shadcn, svg-animations]
---

# Frontend UI Toolkit (React + shadcn + SVG)

Single skill covering: React patterns, shadcn/ui components, SVG animations, Tailwind CSS.

---

## 1. React Best Practices

### Component Structure
```tsx
// ✅ Server Component by default
export async function UserProfile({ id }: { id: string }) {
  const user = await getUser(id);
  return <UserCard user={user} />;
}

// ✅ Client Component only when needed
'use client';
export function UserCard({ user }: { user: User }) {
  const [editing, setEditing] = useState(false);
  return <div onClick={() => setEditing(true)}>...</div>;
}
```

### Key Rules
| Category | Rule |
|----------|------|
| Waterfalls | Parallelize data fetching with `Promise.all()` |
| Bundle Size | Use dynamic imports for heavy components |
| Server Perf | Prefer Server Components, minimize client JS |
| Re-renders | Memoize expensive computations, avoid inline objects |
| Rendering | Use `Suspense` for streaming, `error.tsx` for boundaries |

### Hooks Rules
```tsx
// ✅ Custom hooks extract logic
function useUserData(id: string) {
  const [user, setUser] = useState(null);
  useEffect(() => { /* fetch */ }, [id]);
  return user;
}

// ✅ Avoid nested hooks
// ❌ Don't call hooks inside loops/conditions
```

---

## 2. shadcn/ui

### Installation
```bash
npx shadcn@latest init
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
```

### Component Usage
```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function Dashboard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Dashboard</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  );
}
```

### Custom Registry
```json
// components.json
{
  "registries": {
    "custom": "https://my-registry.com"
  }
}
```

### Theming
```css
/* globals.css */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  /* ... */
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... */
}
```

---

## 3. SVG Animations

### Path Drawing (SMIL)
```svg
<svg viewBox="0 0 100 100">
  <path d="M10 10 H 90 V 90 H 10 Z" 
        fill="none" 
        stroke="currentColor"
        stroke-dasharray="320"
        stroke-dashoffset="320">
    <animate attributeName="stroke-dashoffset" 
             from="320" to="0" 
             dur="2s" fill="freeze" />
  </path>
</svg>
```

### CSS-Driven Animation
```css
@keyframes draw {
  from { stroke-dashoffset: 1000; }
  to { stroke-dashoffset: 0; }
}

.animate-draw {
  stroke-dasharray: 1000;
  animation: draw 2s ease-in-out forwards;
}
```

### Shape Morphing
```svg
<animate attributeName="d" 
         values="M10,10 H90 V90 H10 Z;M50,10 L90,50 L50,90 L10,50 Z"
         dur="1s" 
         repeatCount="indefinite" />
```

### Motion Paths
```svg
<circle r="5" fill="red">
  <animateMotion dur="5s" repeatCount="indefinite">
    <mpath href="#motion-path" />
  </animateMotion>
</circle>
```

### Performance Tips
- Prefer CSS animations over SMIL for GPU acceleration
- Use `will-change: transform` for complex animations
- Avoid animating `box-shadow` (use `filter` instead)
- Keep SVG paths simple for smooth morphing

---

## Usage Triggers
- "React component", "Server Component", "Client Component"
- "shadcn", "install component", "ui library"
- "SVG animation", "path drawing", "shape morphing"
- "Tailwind", "theming", "CSS variables"
- "React hooks", "re-render", "bundle size"
