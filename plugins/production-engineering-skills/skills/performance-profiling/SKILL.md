---
name: performance-profiling
description: "Use when diagnosing slow response times, database query bottlenecks, N+1 query patterns, excessive memory consumption, client-side bundle bloat, or Core..."
---

# Performance Profiling

Systematic diagnostics protocol for identifying, measuring, and eliminating system performance bottlenecks across backend, database, and frontend.

## When to Use
- API endpoint latency exceeds SLO/SLA targets (e.g. p95 > 250ms).
- High CPU or memory consumption under normal loads.
- Sluggish page loads, high INP (Interaction to Next Paint), or excessive bundle size.
- Investigating database CPU spikes or slow query log alerts.

## Profiling Protocol

### 1. Database & I/O Diagnostics
- **N+1 Query Detection**: Inspect ORM queries generated per request. Look for loops executing queries inside iteration blocks. Resolve using eager loading (`include`, `with`, `select_related`, `prefetch_related`) or dataloaders.
- **Query Execution Plan (`EXPLAIN ANALYZE`)**:
  - Watch for `Seq Scan` on large tables (missing index).
  - Watch for high `Buffers: shared read` vs `shared hit` (cache misses).
  - Identify expensive nested loops or sort operations exceeding `work_mem`.
- **Connection Pool Exhaustion**: Verify connection pool sizing, connection timeout configurations, and ensure client connections are always released in `finally` blocks.

### 2. Backend & Runtime Profiling
- **CPU Bottlenecks**: Profile hot paths using flamegraphs or sampling profilers. Look for synchronous crypto, regex catastrophic backtracking (ReDoS), or repeated JSON serialization of large arrays.
- **Memory Leaks**: Check heap snapshot diffs. Look for unclosed event listeners, unbounded global caches without LRU eviction, and circular references retaining closures.
- **Concurrency & Async Blocking**: Ensure event loops (Node.js, Python asyncio, Go goroutines) are never blocked by synchronous I/O or heavy synchronous computations.

### 3. Frontend & Network Optimization
- **Core Web Vitals**:
  - **LCP (Largest Contentful Paint)**: Preload hero images, remove render-blocking CSS/JS, optimize font loading (`font-display: swap`).
  - **INP (Interaction to Next Paint)**: Break long tasks (> 50ms) using `requestIdleCallback` or web workers; debounce input handlers.
  - **CLS (Cumulative Layout Shift)**: Explicit `width` and `height` on images, videos, and dynamic ad containers.
- **Bundle Auditing**: Analyze webpack/vite/turbopack bundle size. Tree-shake unused icons/libraries, replace heavy date/utility libraries with modern lightweight alternatives.

### 4. Verification & Benchmarking
Always measure before and after under identical conditions:
- **Baseline**: Record p50, p95, p99 latency and throughput (RPS).
- **Stress / Load Test**: Run targeted k6, autocannon, or hey benchmark.
- **Report**: Document concrete delta (% improvement in ms, memory, or payload size).
