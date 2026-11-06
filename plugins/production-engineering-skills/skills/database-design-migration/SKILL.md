---
name: database-design-migration
description: "Use when designing database schemas, writing database migrations, planning index strategies, altering tables on live production systems, or ensuring..."
---

# Database Design & Migration

Standardized protocol for database schema modeling, indexing strategy, and zero-downtime migration execution.

## When to Use
- Creating new tables, altering column types, adding foreign keys, or dropping columns.
- Writing migration scripts (Prisma, TypeORM, Drizzle, Alembic, Django, Laravel, Flyway, Liquibase).
- Designing indexes for slow query optimization.
- Planning data backfills on high-volume production tables.

## Review Protocol & Steps

### 1. Schema Modeling Best Practices
- **Primary Keys**: Use UUIDv7 or ULID for distributed systems; use auto-incrementing BigInt for internal single-database analytics.
- **Normalization vs Denormalization**: Normalize transactional operational data (3NF) to eliminate update anomalies; selectively denormalize high-frequency read views with documented synchronization logic.
- **Timestamps**: Ensure every table has `created_at` and `updated_at` (with timezone: `TIMESTAMPTZ` or UTC ISO-8601).
- **Soft Deletes**: Use `deleted_at` with caution; ensure partial unique indexes (e.g. `WHERE deleted_at IS NULL`) are applied so uniqueness constraints remain valid.

### 2. Zero-Downtime Migration Pattern (Expand-Contract)
Never perform breaking schema changes in a single deployment:
1. **Phase 1 (Expand)**: Add the new column or table as nullable. Deploy application code that writes to both old and new columns, reading from the old.
2. **Phase 2 (Backfill)**: Run an asynchronous background batch script to backfill historical data in chunked batches (avoiding long table locks).
3. **Phase 3 (Switch)**: Deploy code that reads from the new column and writes to both.
4. **Phase 4 (Contract)**: Remove old column references from code, then run a migration to drop the old column or table.

### 3. Index Strategy & Lock Safety
- Create indexes concurrently (`CREATE INDEX CONCURRENTLY` in Postgres) to avoid exclusive table locks.
- Check query selectivity: Avoid indexing low-cardinality boolean or enum fields alone; use compound indexes ordered by: Equality columns -> Sort columns -> Range columns.
- Avoid table-locking operations during peak traffic: Adding a non-null column without a default value or adding a foreign key without `NOT VALID`.

### 4. Migration Verification Checklist
- [ ] Is there an explicit, tested `down()` / rollback migration?
- [ ] Does the migration run safely in a transaction?
- [ ] Has it been benchmarked against a representative data volume?
- [ ] Are all foreign keys indexed to prevent cascading delete locks?
