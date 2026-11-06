---
name: deployment-rollback
description: "Use when planning deployments, executing releases, configuring health check probes, zero-downtime rolling/canary deployments, smoke testing, or executing..."
---

# Deployment & Rollback

Standardized engineering playbook for zero-downtime application deployments, progressive canary rollout verification, and automated rollback execution.

## When to Use
- Preparing release checklists before deploying to staging or production.
- Designing deployment workflows (Blue/Green, Rolling update, Canary).
- Implementing deep application health checks (`/healthz`, `/readyz`).
- Diagnosing post-deployment failures and executing fast rollbacks.

## Deployment Protocol

### 1. Pre-Deployment Readiness (Quality Checklist)
- **Artifact Immutability**: Deploy exact tested artifacts (Docker image digest or compiled build bundle) built in CI, never build on production servers.
- **Environment Verification**: Ensure all required environment variables and secrets are populated in target environment before deploying code.
- **Database Backward Compatibility**: Verify that any schema migrations are backward-compatible with the currently running application version (Expand-Contract pattern).

### 2. Zero-Downtime Deployment Strategy
- **Health & Readiness Probes**:
  - **Liveness Probe**: Is the process running and responding? (If failing: restart container).
  - **Readiness Probe**: Is the application fully warmed up and connected to DB/Redis? (Only route live customer traffic after readiness returns HTTP 200).
- **Graceful Shutdown**:
  - Catch `SIGTERM` / `SIGINT`.
  - Stop accepting new incoming requests.
  - Complete active in-flight requests within a grace period (e.g. 15-30s).
  - Close database pools and background queue workers safely before exit.

### 3. Post-Deployment Verification (Smoke Testing)
Immediately after deployment, run an automated smoke test suite:
- Ping `/healthz` and verify database/cache connectivity.
- Test primary user critical flow (e.g. login, query landing page, submit conversion event).
- Monitor error rate metrics (5xx HTTP status spike, unhandled exception rate) for 15 minutes.

### 4. Emergency Rollback Playbook
If critical alerts fire (error rate > 1%, latency p95 > 2x baseline, or core conversion flow breaks):
1. **Trigger Rollback Immediately**: Do NOT attempt to "hotfix" in production while users are suffering.
2. **Revert Traffic**: Point load balancer / router back to previous known-good release image/revision.
3. **Database Guard**: If a migration ran, verify whether it can remain safely or if a rollback migration is required.
4. **Notify & Freeze**: Inform stakeholders in incident channel and freeze further deployments until Root Cause Analysis is completed.
