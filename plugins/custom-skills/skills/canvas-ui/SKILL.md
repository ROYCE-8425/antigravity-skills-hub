---
name: canvas-ui
description: "Add interactive WebGL and WebGPU shader effects over live, clickable, selectable HTML elements using Canvas UI (React, Vue, Svelte, Solid, vanilla)."
---

# Canvas UI — WebGL & WebGPU Effects Over Live Interactive HTML

> **Full Component Catalog:** Read [`references/llms.txt`](./references/llms.txt) in this skill directory for the complete component list, documentation URLs, and registry slugs.

## Overview

Canvas UI (`https://canvasui.dev`) lets GPU shader effects run directly over **live, interactive HTML** where buttons remain clickable, inputs remain focusable, and text remains selectable.
- Every effect ships in two renderer builds:
  - **WebGL (GLSL):** Zero external dependencies (default registry slug).
  - **WebGPU (WGSL):** Rendered via `vgpu` (`-webgpu` registry suffix) with identical props and public API.
- Framework support: **React, Solid, Preact, Vue, Svelte, and Vanilla JS**.

---

## Installation via shadcn CLI

`@canvas-ui` is a trusted shadcn registry — no `components.json` registry modification is required:

```bash
# Format: npx shadcn@latest add @canvas-ui/<component>-<framework>[-webgpu]

# React examples (WebGL build):
npx shadcn@latest add @canvas-ui/liquid-react
npx shadcn@latest add @canvas-ui/glass-react
npx shadcn@latest add @canvas-ui/frost-react
npx shadcn@latest add @canvas-ui/ripple-react
npx shadcn@latest add @canvas-ui/particle-scroll-react

# Vue / Svelte / Vanilla examples:
npx shadcn@latest add @canvas-ui/liquid-vue
npx shadcn@latest add @canvas-ui/liquid-svelte
npx shadcn@latest add @canvas-ui/liquid-vanilla

# WebGPU build example:
npx shadcn@latest add @canvas-ui/liquid-react-webgpu
```

---

## Component Selection Guide

| Category | Component (`<slug>`) | Visual Effect Over Live HTML |
|----------|----------------------|------------------------------|
| **Glass & Refraction** | `glass` | Cursor-following glass lens that refracts live HTML and magnifies targets |
| | `glass-object` | Turns any 3D model (GLB/glTF), SVG, or image into floating liquid glass with dispersion |
| | `bubble` | Glassy metaball droplets trailing cursor and refracting the underlying page |
| | `magnify` | Sci-fi scanner lens magnifying live HTML inside a HUD reticle with click ripples |
| **Fluid & Weather** | `liquid` | Pointer-driven GPU fluid simulation over live HTML |
| | `ripple` | Water ripples spreading from clicks and refracting live HTML like a pond |
| | `droplets` | Rain droplets running down the screen and refracting live DOM |
| | `frost` | Frozen pane of ice over HTML that melts under the cursor and refreezes |
| | `clouds` | Theme-aware mist that blurs/refracts live HTML, parted by cursor wind |
| **3D Deformation** | `cloth` | Hangs live HTML on rippling fabric with lit folds and cursor wave physics |
| | `bend` | Folds top/bottom of live HTML over virtual edges like scrolling on a cube face |
| | `peel` | Peels live HTML back from a corner/edge on hover in 3D to reveal a layer beneath |
| | `shatter` | Breaks live HTML into 3D glass shards that lift, float, and refract around cursor |
| | `grid` | 3D tiles that ripple in staggered waves around the cursor over live HTML |
| | `hex-float` | Live HTML on floating hex tiles with perspective tilt and reading window |
| **Particles & Reveal** | `particle-reveal` | Live HTML rendered as fine particles that merge into crisp UI around cursor |
| | `particle-scroll` | Dissolves live HTML below a scroll line into sand particles that reassemble |
| | `particle-object` | Rebuilds any GLB/glTF, SVG, or image as an interactive particle cloud |
| | `laser` | Laser beam near bottom of viewport revealing live HTML on scroll |
| **Stylized & Retro** | `asciify` | Cursor lens that redraws live HTML beneath it as ASCII characters |
| | `retro-dither` | Retro dither lens pixelating live HTML around the cursor |
| | `dithered-object` | 3D GLB/glTF model rendered through a 1-bit Bayer dither (Three.js) |
| | `glitch` | Broadcast glitch bursts with RGB splits and slice shifts over live HTML |
| | `vhs` | Worn tape playback with head-switching noise and chroma bleed over live HTML |
| | `blaze` | Fire sparks, smoke, and heat distortion rising over live HTML |

---

## Usage Rules & Fallbacks

1. **Progressive Enhancement:** Components using the experimental `html-in-canvas` API require Chromium with `chrome://flags/#canvas-draw-element` enabled, while object/standalone canvas components (`glass-object`, `dithered-object`, `particle-object`) work across standard WebGL browsers. Always ensure the underlying HTML remains readable and functional if the WebGL/canvas layer is disabled or unsupported.
2. **Hero & Focal Restraint:** Apply Canvas UI effects to **one hero showcase, interactive callout card, or section transition** per page rather than wrapping the entire document body.
