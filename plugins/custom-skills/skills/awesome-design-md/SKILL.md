---
name: awesome-design-md
description: "Library of 84+ real-world brand DESIGN.md files (Linear, Apple, Stripe, Vercel, Claude, Cursor, Airbnb, Figma, Framer, Raycast, Supabase, Notion,..."
---

# Awesome DESIGN.md — Curated Brand Design Systems

> **Local Brand Library:** All 84+ brand `DESIGN.md` files are stored locally in [`references/design-md/<brand>/DESIGN.md`](./references/design-md/).
> **Full Index:** See [`references/README.md`](./references/README.md) for categorized brand descriptions.

## Overview

`VoltAgent/awesome-design-md` provides deeply analyzed `DESIGN.md` specifications extracted from the world's best-designed tech, luxury, developer, fintech, and media brands. Each file defines:
1. Visual theme & atmosphere
2. Exact color palette & surface hierarchy (hex/RGB/HSL roles)
3. Typography rules (font families, weights, fluid scales, tracking)
4. Component stylings (buttons, cards, inputs, navbars, badges)
5. Layout principles, grid systems, whitespace ratios, and elevation shadows
6. Anti-patterns & brand-specific Guardrails

---

## How to Use

1. **Identify the target aesthetic or brand:**
   - **Developer & AI Tools:** `linear.app`, `cursor`, `claude`, `vercel`, `supabase`, `raycast`, `warp`, `zed`, `mintlify`, `resend`, `posthog`, `sentry`, `expo`, `lovable`, `ollama`, `opencode`, `replicate`, `together.ai`, `huggingface`, `mistral.ai`, `cohere`, `elevenlabs`, `runwayml`, `minimax`, `composio`, `clickhouse`, `hashicorp`, `mongodb`, `neon`, `planetscale`, `prisma`, ` railway`, `render`, ` sanity`, `tailwind`
   - **Design & Creative Studios:** `figma`, `framer`, `webflow`, `miro`, `spline`, `lottielab`, `pitch`, `readymag`, `cosmos`, `are.na`
   - **Fintech & Enterprise SaaS:** `stripe`, `mercury`, `wise`, `revolut`, `ramp`, `brex`, `robinhood`, `coinbase`, `binance`, `kraken`, `mastercard`, `airtable`, `notion`, `attio`, `clay`, `cal`, `intercom`, `zendesk`, `ibm`
   - **Consumer, Hardware & Luxury:** `apple`, `airbnb`, `uber`, `spotify`, `pinterest`, `dji`, `teenage-engineering`, `nothing`, `leica`, `ferrari`, `lamborghini`, `porsche`, `bugatti`, `bmw`, `bmw-m`, `tesla`, `rivian`, `nike`, `Aesop`
   - **Editorial & Media:** `nyt`, `the-verge`, `wired`, `monocle`, `aljazeera`, `sub-stack`

2. **Load the Brand's `DESIGN.md`:**
   Read `references/design-md/<brand>/DESIGN.md` (or check `open-design`'s `references/design-systems/<brand>/DESIGN.md` which expands this collection to 150+ systems).

3. **Apply or Copy to Workspace:**
   - If the user wants their project to adopt that design system permanently, copy the selected `DESIGN.md` to their project root (customizing brand name and accent tokens if requested).
   - Map all tokens from the `DESIGN.md` directly into `:root` CSS variables / Tailwind theme tokens before writing component code.
