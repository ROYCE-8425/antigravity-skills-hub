---
name: security-review
description: "Use when auditing code or infrastructure for security vulnerabilities, authentication/authorization flaws, injection risks, data leakage, OWASP Top 10..."
---

# Security Review

A systematic security assessment protocol designed to catch vulnerabilities before code merges or reaches staging/production.

## When to Use
- Implementing or altering authentication, authorization, session management, or API token validation.
- Adding database queries, dynamic file reads/writes, external HTTP calls, or executing subprocesses.
- Handling sensitive PII, passwords, payment info, tokens, or encryption keys.
- Auditing dependencies for known CVEs or supply-chain risks.

## Review Protocol & Steps

### 1. Authentication & Authorization (AuthN & AuthZ)
- **Broken Object Level Authorization (BOLA / IDOR)**: Verify that every endpoint accessing a resource checks tenant ownership (`user_id` / `account_id`) from the verified session, NOT from request body/params.
- **Role-Based Access Control (RBAC)**: Ensure administrative endpoints have strict middleware/decorator gates.
- **Session & Token Management**: Check token expiry, secure cookie flags (`HttpOnly`, `Secure`, `SameSite=Lax/Strict`), and token invalidation on logout.

### 2. Injection & Input Sanitization
- **SQL / NoSQL Injection**: Zero tolerance for string concatenation in raw queries. Use parameterized queries or ORM binds exclusively.
- **Command Injection**: Avoid passing user input into shell commands (`exec`, `system`, `sh -c`, `PowerShell`). If unavoidable, use strict whitelist regex and array arguments without shell interpretation.
- **XSS (Cross-Site Scripting)**: Ensure output encoding in UI rendering, sanitize raw HTML inputs (e.g. DOMPurify), and enforce Content Security Policy (CSP).
- **SSRF (Server-Side Request Forgery)**: Block server-side fetching of internal/private IP ranges (`10.0.0.0/8`, `192.168.0.0/16`, `127.0.0.1`, cloud metadata IP `169.254.169.254`).

### 3. Secrets & Data Protection
- Audit codebase for hardcoded API keys, JWT secrets, passwords, or private certificates.
- Verify environment variable loading with fail-fast validation on startup.
- Ensure sensitive fields are excluded from log outputs, crash reports, and API error responses.

### 4. Security Findings Report Format
Format all findings as:
- **Severity**: Critical / High / Medium / Low
- **Vulnerability**: Exact CWE / OWASP categorization
- **Location**: Specific file and line number
- **Proof of Risk**: How an attacker could exploit it
- **Remediation**: Exact, drop-in code fix
