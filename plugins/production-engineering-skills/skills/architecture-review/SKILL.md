---
name: architecture-review
description: "Use when designing a new feature, evaluating existing system structure, reviewing component boundaries, dependency graphs, scalability limits, or..."
---

# Architecture Review

Comprehensive review protocol for software architecture, system boundaries, and structural scalability.

## When to Use
- Proposing or evaluating new modules, services, or significant subsystem changes.
- Assessing dependency boundaries (tight coupling, cyclic dependencies).
- Evaluating data flow and state management strategies across frontend/backend.
- Identifying scalability, reliability, and single points of failure (SPOF).

## Review Protocol & Steps

### 1. Structural Boundaries & Cohesion
- **Single Responsibility Principle**: Does each module or service own exactly one core domain entity or capability?
- **Direction of Dependencies**: Do high-level business policies depend on abstractions rather than low-level details (Dependency Inversion)?
- **Interface Segregation**: Are client-facing interfaces minimal and purpose-built, avoiding bloated god-interfaces?

### 2. Data Flow & State Lifecycle
- Trace the lifecycle of data: source of truth -> transport (REST/gRPC/WebSocket) -> cache -> presentation/state store.
- Check for race conditions, stale cache invalidation mechanisms, and eventual consistency issues.
- Verify idempotency for external mutations, background jobs, and webhook handlers.

### 3. Scalability & Operational Constraints
- Identify potential bottlenecks: Synchronous I/O in high-throughput hot paths, unbounded collection queries in memory, lack of pagination.
- Resilience checks: Circuit breakers, retry policies with exponential backoff and jitter, graceful degradation paths.

### 4. Deliverable Format
Provide an Architecture Evaluation Matrix:
1. **Current vs Proposed Architecture**: Diagram or concise ASCII/Mermaid flow.
2. **Trade-offs**: Latency vs consistency, complexity vs maintainability, cost vs performance.
3. **Actionable Recommendations**: Must-fix (P0), Should-fix (P1), Future considerations (P2).
