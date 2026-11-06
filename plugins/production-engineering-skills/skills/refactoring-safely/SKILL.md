---
name: refactoring-safely
description: "Use when restructuring messy, legacy, or tightly-coupled code without changing observable external behavior, paying down technical debt, or breaking..."
---

# Refactoring Safely

Disciplined protocol for restructuring and improving codebase design while guaranteeing behavioral preservation through test pinning and baby steps.

## When to Use
- Cleaning up complex functions, deeply nested conditionals, or bloated classes.
- Extracting shared logic into reusable modules or services.
- Replacing legacy APIs or libraries with modern equivalents.
- Decoupling tightly coupled subsystems.

## The Safe Refactoring Rules

> **Core Principle**: Refactoring means changing the internal structure of code without changing its external observable behavior. Never combine refactoring with feature addition or bug fixing in the same commit.

### 1. Step 1: Pinning the Baseline (Characterization Tests)
- Before touching a single line of production code, verify that the existing behavior is thoroughly pinned by automated tests.
- If tests are missing, write **Characterization Tests** capturing the current behavior—including edge cases and known quirks.
- Run tests and establish 100% green baseline.

### 2. Step 2: Choose the Technique (Martin Fowler Patterns)
- **Extract Method / Function**: Break 50+ line procedures into small, self-documenting functions with clear inputs and outputs.
- **Replace Conditional with Polymorphism / Strategy**: Replace fragile multi-branch switch/case statements with dispatch tables or strategy patterns.
- **Introduce Parameter Object**: Consolidate long parameter lists (> 3 parameters) into strongly typed DTOs or config objects.
- **Split Phase**: Separate data parsing / preparation from core business calculation.

### 3. Step 3: The Micro-Step Loop (Mikado Method)
Execute changes in micro-steps:
1. Make ONE small change (e.g. rename a variable, extract a single helper).
2. Run test suite immediately.
3. If green: Commit or stage.
4. If red: Revert immediately. Never "fix forward" by writing more untested code.

### 4. Step 4: Verification Before Completion
- [ ] Do all pre-existing tests pass without modification?
- [ ] Have public function signatures and API contracts remained backward-compatible?
- [ ] Has code complexity (cyclomatic complexity, cognitive load) measurably decreased?
- [ ] Is the diff clean, readable, and free of accidental cosmetic changes?
