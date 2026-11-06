---
name: triad-dev-workflow
description: "Harmonized engineering workflow combining Superpowers (process & verification), Ponytail (minimal code, reuse-first, caller-aware review/audit), and..."
---

# Triad Dev Workflow (Superpowers + Ponytail + Caveman)

This skill orchestrates **Superpowers**, **Ponytail**, and **Caveman** as complementary layers while resolving their potential conflicts (process overhead on small tasks, TDD vs. trivial changes, and terse output vs. full audit context).

## 1. Division of Responsibilities

| Layer | Source Repo | Core Role | Primary Skills to Reference |
| :--- | :--- | :--- | :--- |
| **Workflow & Proof** | `obra/superpowers` | Decides execution steps and requires concrete runtime verification before claiming completion. | `verification-before-completion`, `systematic-debugging`, `brainstorming`, `writing-plans` |
| **Solution Sizing & Review** | `DietrichGebert/ponytail` | Selects the smallest complete change and traces callers + data flow during reviews/audits. | `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt` |
| **Communication & Surgical Scope** | `JuliusBrussee/caveman` | Keeps status updates and explanations concise while preserving 100% of technical payload. | `caveman`, `surgical-patch`, `investigate-first`, `lean-build` |

---

## 2. Conflict-Resolution Rules (Precedence)

### A. Process Sizing: Feature vs. Small Fix (Superpowers vs. Ponytail/Caveman)
- **Complex / Multi-Decision Features**: Use Superpowers (`brainstorming` → `writing-plans` → `executing-plans` / `subagent-driven-development`). Clarify requirements and design boundaries before writing code.
- **Bounded Bugfixes & Small Tasks**: Skip multi-step design ceremony. Route directly through `investigate-first` / `surgical-patch` + `ponytail`:
  1. Read the target code and grep all callers/callees first.
  2. Fix the root cause once at the narrowest responsible layer.
  3. Verify and report.

### B. Testing Threshold: TDD vs. Trivial Changes (Superpowers vs. Ponytail)
- **Non-Trivial Logic (Superpowers TDD wins)**: Any new branch, loop, parser, state transition, auth/security check, financial/data mutation, or bug fix **MUST** have a failing test or focused regression check (`test-driven-development` / `ponytail` rule 41).
- **Trivial Changes (Ponytail wins)**: Typo fixes, copy/style tweaks, static config adjustments, or dead-code deletions do not require ceremony unit tests—verify via build/typecheck/lint (`verification-before-completion`).

### C. Solution Selection: Reuse Hierarchy (Ponytail Always Wins)
Before writing new code during any Superpowers plan or task, enforce Ponytail's strict priority order:
1. **Does it need to exist?** Drop unrequested options, wrappers, and speculative "for later" abstractions (YAGNI).
2. **Existing codebase helper/component/pattern?** Reuse it the way surrounding code does.
3. **Standard library / platform native feature?** Use it before reaching for packages.
4. **Already-installed dependency?** Use it; never add a dependency for a few lines of code.
5. **Minimal new code**: Write the shortest readable diff that covers all affected callers, tests, and fixtures.
- **Never cut**: Input validation at trust boundaries, error handling that prevents data loss, security checks, and accessibility.
- **Intentional shortcuts**: Document deliberate limits inline as `// shortcut: <ceiling>, <when to upgrade>` so `/ponytail-debt` can track them.

### D. Output Verbosity: Chat vs. Review/Audit Reports (Caveman vs. Ponytail Review)
- **Routine Chat & Progress Updates (Caveman wins)**:
  - Answer first, drop pleasantries/hedging/recaps, keep every code span, file path, command, error message, number, and negation (`not`/`never`/`only`) 100% intact.
- **Code Reviews & Repo Audits (`ponytail-review` / `ponytail-audit` wins over Caveman)**:
  - **Never** compress review or audit findings into cryptic one-liners that hide failure mechanics.
  - Every finding must include a concrete failure scenario (*What this is*, *Problem* with specific input/state that fails, *Smallest Fix*, and *If we skip it*).
- **Safety / Destructive Operations**: Always use clear, complete sentences when warning about security risks or irreversible actions.

---

## 3. Standard Execution Checklist

1. **Scope & Callers**: Read the touched files and grep every caller/consumer before editing.
2. **Reuse Check**: Confirm no existing helper or stdlib function already solves the problem.
3. **Implement**: Apply the smallest complete change across code, callers, and fixtures.
4. **Verify (`verification-before-completion`)**: Run the actual test/build/check command and read the output. Never claim success without fresh command evidence.
5. **Report (`ponytail` + `caveman`)**: State the result concisely, and end with 1–2 lines noting what was verified, any deliberate shortcut taken, or what could not be checked.
