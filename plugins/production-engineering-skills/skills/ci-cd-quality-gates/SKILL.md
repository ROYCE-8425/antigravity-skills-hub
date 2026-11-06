---
name: ci-cd-quality-gates
description: "Use when configuring or reviewing CI/CD pipelines (GitHub Actions, GitLab CI, Bitbucket Pipelines), establishing automated quality gates, blocking..."
---

# CI/CD Quality Gates

Architecture and enforcement standard for automated continuous integration quality gates that prevent buggy, insecure, or substandard code from reaching release branches.

## When to Use
- Setting up or tuning automated pull request validation pipelines.
- Defining mandatory status checks required before merge.
- Configuring fast-feedback matrix builds (lint, typecheck, tests, security scans).
- Optimizing CI build speeds through strategic caching and parallelization.

## The Quality Gate Matrix

A production-grade CI pipeline enforces 5 non-negotiable gates:

| Gate | Stage | Tooling Example | Failure Policy | Max Target Duration |
| :--- | :--- | :--- | :--- | :--- |
| **Gate 1: Fast Static Analysis** | Lint & Formatting | ESLint, Biome, Prettier, Ruff, PHP-CS-Fixer | Hard Block | < 60s |
| **Gate 2: Type Safety** | Type Checking | TypeScript (`tsc --noEmit`), mypy, PHPStan level 8 | Hard Block | < 90s |
| **Gate 3: Security & Secrets** | Vulnerability Scan | TruffleHog, Gitleaks, Snyk, `npm audit`, Dependabot | Hard Block (P0/P1) | < 2m |
| **Gate 4: Automated Testing** | Unit & Integration | Jest, Vitest, Pytest, Pest, PHPUnit | Hard Block | < 3m |
| **Gate 5: Build & Artifact Validation** | Production Build | Next build, Vite build, Docker build, Webpack | Hard Block | < 4m |

## Pipeline Optimization Principles

### 1. Fail Fast
- Order jobs from fastest to slowest. Run static analysis and secret detection before launching expensive multi-container integration tests.
- Enable `fail-fast: true` so the pipeline terminates immediately upon the first fatal error, saving CI runner minutes.

### 2. Aggressive Caching
- Cache package manager dependencies (`npm`, `pnpm`, `pip`, `composer`, `cargo`) keyed by lockfile hash (`hashFiles('**/package-lock.json')`).
- Cache intermediate compiler artifacts (`.next/cache`, `target/`, `.pytest_cache`).

### 3. Hermetic & Deterministic Environment
- Pin all tool versions, Docker base image digests, and GitHub Action commit SHAs (avoid mutable `@latest` or `@v1` tags).
- Require clean dependency installs (`npm ci` instead of `npm install`).
- Reject PRs if lockfiles are dirty or out of sync.

### 4. Review Checklist for CI/CD Configs
- [ ] Are all secrets referenced via secure repository secrets, never plaintext?
- [ ] Are required branch protection rules enabled on `main` / `master`?
- [ ] Is PR branch up to date with target branch before merge?
- [ ] Are test coverage thresholds enforced (e.g. no merge if overall coverage drops > 1%)?
