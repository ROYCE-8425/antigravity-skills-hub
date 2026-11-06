---
name: react-bits
description: "Integrate 200+ animated, interactive React and Next.js components from React Bits (Text Animations, Animations, UI Components, Backgrounds,..."
---

# React Bits — Animated & Interactive React Component Library

> **Full Component Catalog:** Always read [`references/llms.txt`](./references/llms.txt) in this skill directory to search the complete list of 200+ components, descriptions, URLs, and exact CLI identifiers.

## Overview

React Bits (`https://reactbits.dev`) provides 200+ copy-friendly, customizable React & Next.js components across 5 categories:
1. **Text Animations** (`SplitText`, `BlurText`, `DecryptedText`, `ShinyText`, `ScrollVelocity`, `GradientText`, `ASCIIText`, `TrueFocus`, `RotatingText`, `VariableProximity`, `WarpText`, `SplitFlapText`, etc.)
2. **Animations & Cursor Effects** (`AnimatedContent`, `FadeContent`, `BlobCursor`, `SplashCursor`, `ClickSpark`, `Magnet`, `GlareHover`, `StarBorder`, `ElectricBorder`, `MetaBalls`, `Ribbons`, `ImageTrail`, etc.)
3. **Interactive UI Components** (`TiltedCard`, `SpotlightCard`, `PixelCard`, `Dock`, `BentoGrid`, `Folder`, `Stack`, `CircularGallery`, `InfiniteMenu`, `FlowingMenu`, `DecayCard`, `Lanyard`, `ModelViewer`, etc.)
4. **Backgrounds (WebGL / OGL / Three.js / Canvas)** (`Aurora`, `Beams`, `Silk`, `Iridescence`, `LiquidChrome`, `Hyperspeed`, `Particles`, `Waves`, `Threads`, `Balatro`, `Orb`, `Prism`, `DarkVeil`, `GridDistortion`, `LetterGlitch`, `Lightning`, `Galaxy`, `PixelBlast`, `Dither`, `FaultyTerminal`, etc.)
5. **Micro-Interactions** (switches, magnetic buttons, tactile loaders, stateful toggles)

Every component ships in **4 implementation variants**:
- `JS-CSS` (JavaScript + plain CSS)
- `JS-TW` (JavaScript + Tailwind CSS)
- `TS-CSS` (TypeScript + plain CSS)
- `TS-TW` (TypeScript + Tailwind CSS — **Recommended for modern Next.js/React projects**)

---

## Installation Workflow (CLI)

Prefer installing directly via `shadcn` or `jsrepo` CLI using the PascalCase component identifier from [`references/llms.txt`](./references/llms.txt):

```bash
# Using shadcn CLI (Recommended)
npx shadcn@latest add "https://reactbits.dev/r/<Component>-<LANG>-<STYLE>"

# Examples (TypeScript + Tailwind):
npx shadcn@latest add "https://reactbits.dev/r/SplitText-TS-TW"
npx shadcn@latest add "https://reactbits.dev/r/Aurora-TS-TW"
npx shadcn@latest add "https://reactbits.dev/r/SpotlightCard-TS-TW"
npx shadcn@latest add "https://reactbits.dev/r/AnimatedContent-TS-TW"

# Using jsrepo CLI
npx jsrepo@latest add "https://reactbits.dev/r/<Component>-<LANG>-<STYLE>"
```

- `<LANG>`: `TS` or `JS`
- `<STYLE>`: `TW` (Tailwind) or `CSS`

---

## Best Practices & Anti-Bloat Rules

1. **Restraint Over Overload:**
   - Use **at most 1 WebGL/Canvas background** per viewport (e.g., `Aurora`, `Silk`, `Beams`, or `Particles` in the Hero section). Multiple heavy WebGL canvases on the same page degrade FPS and mobile battery.
   - Use **at most 1 signature text effect** on the primary hero headline (`SplitText`, `BlurText`, or `GradientText`), not on every paragraph.
2. **Verify Peer Dependencies:**
   - Components use `gsap`, `motion` (Framer Motion), `ogl`, or `three` (`@react-three/fiber`, `@react-three/drei`). Check the installed component file imports after running `npx shadcn@latest add` and install any missing peer package.
3. **Next.js App Router Compatibility:**
   - All React Bits components use browser APIs (`window`, `requestAnimationFrame`, `WebGLRenderingContext`). Ensure `"use client"` is present at the top of the component or wrapper, and dynamically import heavy Three.js/OGL backgrounds with `{ ssr: false }` if needed.
4. **Accessibility (`prefers-reduced-motion`):**
   - Wrap high-velocity or glitch/distortion effects (`GlitchText`, `Hyperspeed`, `ScrollVelocity`, `LetterGlitch`) with reduced-motion checks or subtle fallbacks so users with vestibular sensitivity have a comfortable experience.
