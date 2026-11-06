# Antigravity UI/UX & Design Engineering Priority Rules

Whenever a task involves **building, redesigning, animating, or auditing web/mobile UI, landing pages, dashboards, or design systems**, orchestrate the 12 installed UI/UX skill suites by phase instead of falling back to generic LLM templates:

## 1. Design System & Direction (Before Writing UI Code)
- **Existing or Brand `DESIGN.md`**: Always check for a `DESIGN.md` at the project root first (`google-design-md`). If the user names a brand aesthetic (Linear, Stripe, Apple, Vercel, Claude, Airbnb, Figma, Cursor, etc.) or needs a starter system, load a curated template from `awesome-design-md` (84+ brands) or `open-design` (152 systems & archetypes).
- **Art Direction & Anti-Slop Framing**:
  - For landing pages, portfolios, and expressive marketing sites: activate `taste-skill` (or `hallmark` when requested) to establish a clear aesthetic direction, macrostructure, and reference palette.
  - For multi-platform product UI, UX rules, font pairings, and industry palettes: query `ui-ux-pro-max` (`scripts/search.py`) and `design-system`.

## 2. Component Craft, Motion & 3D Implementation
- **Micro-Interactions & Polish**: Apply `emil-design-eng`, `animate`, `animation-performance`, and `apple-design` (from `emilkowalski-skills`) for spring physics, custom cubic-bezier curves, tactile press states, and `prefers-reduced-motion` safety.
- **GSAP & Scroll Choreography**: Activate `gsap-core`, `gsap-scrolltrigger`, `gsap-timeline`, and `gsap-react` (`useGSAP`) when building scroll-triggered reveals, pinned timelines, or kinetic typography.
- **Animated React Components**: Check `react-bits` (`references/llms.txt`) for 200+ ready-to-install (`npx shadcn@latest add`) text animations, cursor effects, cards, and backgrounds.
- **WebGL/WebGPU & 3D Scenes**:
  - Use `canvas-ui` (`@canvas-ui/*`) for interactive WebGL/WebGPU effects (liquid glass, frost, cloth, ripple, shatter) over live clickable/selectable HTML.
  - Use `scroll-world` for scrollable 3D world landing pages with canvas frame scrubbing, or `open-design` (`threejs`, `shader-dev`, `mockup-device-3d`) for custom Three.js/GLSL scenes.

## 3. Hard Quality Floor & Pre-Delivery Audit
- **Never ship AI-slop defaults**: No unrequested purple-to-blue gradients, no `transition: all`, no animating `width`/`height`/`top`/`left`, no emoji-as-icons, no invented fake metrics/testimonials, and no raw hex values bypassing `:root` / theme tokens.
- **Critique & Polish Pass**: When reviewing, refining, or finishing UI work, apply `impeccable` (`audit`, `polish`, `critique`, `distill`, `harden`, `craft-floor.md`), `hallmark` (`gates.md`), or `review-animations` to verify WCAG contrast, keyboard `:focus-visible`, responsive overflow (`overflow-x: clip`), and visual rhythm.
