---
name: google-design-md
description: "Author, lint, diff, and export standards-compliant DESIGN.md files using Google Labs' official DESIGN.md specification (YAML design tokens + prose..."
---

# Google DESIGN.md — Official Format Specification & CLI Tooling

> **Full Specification & Examples:**
> - Official Spec Reference: [`references/spec.md`](./references/spec.md)
> - Reference Examples:
>   - [`references/examples/atmospheric-glass/DESIGN.md`](./references/examples/atmospheric-glass/DESIGN.md)
>   - [`references/examples/paws-and-paths/DESIGN.md`](./references/examples/paws-and-paths/DESIGN.md)
>   - [`references/examples/totality-festival/DESIGN.md`](./references/examples/totality-festival/DESIGN.md)

## Overview

`DESIGN.md` (`https://github.com/google-labs-code/design.md`) is Google Labs' standard specification for describing a visual identity to AI coding agents. It combines two layers in a single `DESIGN.md` file at the project root:
1. **Normative YAML Design Tokens:** Machine-readable tokens (`colors`, `typography`, `rounded`, `spacing`, `elevation`, `components`) defined either in YAML frontmatter (`---`) or interleaved as fenced ````yaml` blocks inside each `##` section.
2. **Human-Readable Markdown Rationale:** Prose organized into standard `##` sections (`## Overview`, `## Colors`, `## Typography`, `## Layout & Spacing`, `## Elevation & Surfaces`, `## Components`, `## Do's and Don'ts`) explaining *why* those values exist and how to apply them.

---

## Standard YAML Token Schema

```yaml
---
version: alpha
name: Heritage
description: Architectural Minimalism meets Journalistic Gravitas
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface-elevated:
    value: "#FFFFFF"
    dark: "#22252A"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
    lineHeight: 1.6
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 0.75rem
    fontWeight: 600
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    borderRadius: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
---
```

---

## CLI Commands (`@google/design.md`)

When Node/npx is available, validate, compare, and export `DESIGN.md` directly:

### 1. Lint & Validate WCAG Contrast + Token References
```bash
npx -y @google/design.md lint DESIGN.md
# Auto-fix structural / ordering issues:
npx -y @google/design.md lint --fix DESIGN.md
```
Checks:
- Broken `{category.token}` references
- Automatic WCAG AA/AAA contrast ratio checks on `components.*` (`textColor` vs `backgroundColor`)
- Required section coverage and token schema conformance

### 2. Diff Two Design System Versions
```bash
npx -y @google/design.md diff DESIGN.md DESIGN-v2.md
```
Detects added/removed/modified tokens and whether contrast or structural regressions occurred.

### 3. Export to CSS Custom Properties or W3C DTCG Tokens
```bash
# Export to CSS variables (:root / dark mode):
npx -y @google/design.md export --format css DESIGN.md > tokens.css

# Export to W3C Design Tokens Community Group (DTCG) JSON:
npx -y @google/design.md export --format dtcg DESIGN.md > tokens.json
```

---

## Agent Workflow

1. **Before coding UI:** Check if `DESIGN.md` (or `design.md`) exists in the project root. If it does, treat its tokens and component rules as the single source of truth.
2. **When creating a new `DESIGN.md`:**
   - Need a real-world brand reference (e.g., Linear, Stripe, Apple, Vercel, Claude, Airbnb, Figma)? Read the `awesome-design-md` or `open-design` skill first to load a brand archetype, then structure or validate the project's `DESIGN.md` using this specification.
   - Always verify that every component's `textColor` against `backgroundColor` passes WCAG AA (≥ 4.5:1 for body text, ≥ 3:1 for large text).
