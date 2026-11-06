---
name: production-incident-review
description: "Use when conducting post-incident reviews (post-mortems), analyzing production bugs, determining root cause (5 Whys), establishing timeline of events, or..."
---

# Production Incident Review (Post-Mortem)

Blameless, engineering-driven framework for investigating production outages, diagnosing root causes, and implementing durable preventative safeguards.

## When to Use
- After a production outage, customer-impacting bug, data inconsistency, or security incident.
- Conducting systematic Root Cause Analysis (RCA) and 5 Whys.
- Documenting incident timeline and recovery metrics (MTTD, MTTR).
- Creating prioritized remediation tickets to prevent repeat occurrences.

## Post-Mortem Protocol

### 1. The Blameless Post-Mortem Principle
- Assume everyone made the best decisions possible with the information they had at the time.
- Focus on systemic flaws, missing guardrails, inadequate testing, and architectural vulnerabilities—never individual human error.

### 2. Incident Timeline Construction
Construct an objective, timestamped log of events:
- **T0 (Trigger)**: Time the faulty change merged / deployed / trigger event occurred.
- **T1 (Impact Starts)**: Time end users began experiencing degradation or errors.
- **T2 (Detection / MTTD)**: Time monitoring alert fired or issue was detected.
- **T3 (Diagnosis)**: Time the root cause was identified by the responding team.
- **T4 (Mitigation / MTTR)**: Time rollback completed or service restored.
- **T5 (Full Resolution)**: Time data clean-up / monitoring stabilization concluded.

### 3. Root Cause Analysis (The 5 Whys Technique)
Iteratively probe deeper to uncover structural and organizational root causes:
- *Why did the service crash?* -> Memory exhausted on worker nodes.
- *Why was memory exhausted?* -> A batch job loaded 500,000 records into memory at once.
- *Why did it load 500,000 records?* -> No pagination or chunking was implemented.
- *Why wasn't pagination implemented?* -> The developer assumed the dataset was small based on dev test data.
- *Why didn't testing catch this?* -> Staging environment lacked synthetic volume tests and integration tests didn't simulate production scale.

### 4. Corrective Action Items (SMART)
Categorize remediations into three buckets:
1. **Prevent**: Changes to code, architecture, or validation that make this failure class impossible.
2. **Detect**: New alert rules, health checks, or metrics to reduce MTTD to < 2 minutes.
3. **Mitigate**: Runbooks, automated rollbacks, or circuit breakers to reduce MTTR to < 5 minutes.
