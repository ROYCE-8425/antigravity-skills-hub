---
name: integration-testing
description: "Use when designing or writing integration tests connecting multiple components, API routes with real/containerized databases, third-party service..."
---

# Integration Testing

Methodology for creating deterministic, isolated, and reliable integration test suites connecting multiple system layers.

## When to Use
- Testing API endpoints against database transactions and cache layers.
- Verifying message queues (RabbitMQ, Kafka, SQS, BullMQ) and background workers.
- Testing third-party integration adapters using recorded stubs or mock servers (WireMock, MSW, VCR).
- Verifying auth flows, webhook processing, and multi-step state transitions.

## Protocol & Implementation Rules

### 1. Test Isolation & Determinism
- **Ephemeral State**: Every test must run in its own clean transaction that rolls back after test completion, or use distinct tenant/database prefixes.
- **No Shared Mutable State**: Tests must be executable in parallel without race conditions or inter-test dependencies.
- **Time Freezing**: Use clock mocking (e.g. `vi.setSystemTime`, `sinon.useFakeTimers`, `timekeeper`) for any logic dependent on timestamps, TTLs, or cron schedules.

### 2. External Service Boundaries
- **In-Memory / Testcontainers**: Prefer ephemeral Docker testcontainers or embedded databases over shared remote staging databases.
- **Network Boundaries**: Block real outgoing internet calls during test runs. Use MSW (Mock Service Worker), nock, or mock adapters to simulate:
  - 200 OK responses with realistic schemas.
  - 429 Rate Limit responses with `Retry-After` headers.
  - 500 / 503 Server Errors and network timeout disconnects.

### 3. Coverage Strategy (The Golden Paths)
Focus integration tests on high-risk boundaries:
1. **Happy Path**: Complete end-to-end lifecycle (Create -> Retrieve -> Update -> Delete/Archive).
2. **Authorization Boundary**: Unauthenticated requests (401), unauthorized role requests (403), cross-tenant tampering (404/403).
3. **Validation & Edge Conditions**: Malformed payloads, oversized inputs, invalid boundary types.
4. **Failure & Rollback**: Partial failure in a distributed transaction to verify database rollback.

### 4. Verification Check
- Run the full suite with randomized execution order (`--shuffle` or `--randomize`).
- Ensure execution time is tracked; any integration test exceeding 1.5s must be audited for unnecessary sleeps or unindexed lookups.
