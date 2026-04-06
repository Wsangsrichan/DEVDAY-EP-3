# OWASP Top 10 (2021) — Quick Reference

## A01: Broken Access Control

| Item | Detail |
|------|--------|
| Risk | ผู้ใช้เข้าถึงข้อมูล/function ที่ไม่ได้รับอนุญาต |
| Examples | IDOR, privilege escalation, force browsing |
| Fix | Authorization check ทุก request, RBAC, deny by default |

## A02: Cryptographic Failures

| Item | Detail |
|------|--------|
| Risk | การเข้ารหัสไม่เหมาะสม ไม่มี หรือ algorithm ล้าสมัย |
| Examples | Plain text passwords, MD5/SHA1, HTTP ไม่ใช่ HTTPS, hardcoded keys |
| Fix | bcrypt/argon2 สำหรับ password, TLS, AES-256, ไม่ hardcode |

## A03: Injection

| Item | Detail |
|------|--------|
| Risk | User input ถูก execute โดยตรงโดยไม่ sanitize |
| Examples | SQL Injection, XSS, Command Injection |
| Fix | Parameterized queries, input validation, output encoding |

## A04: Insecure Design

| Item | Detail |
|------|--------|
| Risk | ออกแบบระบบไม่ปลอดภัยตั้งแต่แรก |
| Examples | ไม่มี rate limiting, คำถาม security ที่เดาง่าย |
| Fix | Threat modeling, secure design patterns, abuse case testing |

## A05: Security Misconfiguration

| Item | Detail |
|------|--------|
| Risk | ตั้งค่าไม่ถูกต้อง ปล่อย default settings |
| Examples | DEBUG=True in prod, default credentials, public S3 buckets |
| Fix | Hardening checklist, env-specific configs, automated scanning |

## A06: Vulnerable & Outdated Components

| Item | Detail |
|------|--------|
| Risk | ใช้ library ที่มีช่องโหว่ที่ทราบแล้ว |
| Examples | Log4Shell (CVE-2021-44228), outdated jQuery |
| Fix | Regular updates, SCA tools (Syft, Snyk), monitor CVEs |

## A07: Identification & Authentication Failures

| Item | Detail |
|------|--------|
| Risk | ระบบ authentication อ่อนแอ |
| Examples | Weak passwords, no MFA, session ID in URL |
| Fix | Strong password policy, MFA, secure sessions, rate limiting |

## A08: Software & Data Integrity Failures

| Item | Detail |
|------|--------|
| Risk | ไม่ตรวจสอบ integrity ของ software/data |
| Examples | SolarWinds attack, untrusted libraries, insecure deserialization |
| Fix | Digital signatures, verify checksums, secure CI/CD |

## A09: Security Logging & Monitoring Failures

| Item | Detail |
|------|--------|
| Risk | ไม่มี logging เพียงพอ ตรวจจับ attack ไม่ได้ |
| Examples | ไม่ log failed logins, log sensitive data, ไม่มี alerting |
| Fix | Log security events, centralized logging, alerting, IR plan |

## A10: Server-Side Request Forgery (SSRF)

| Item | Detail |
|------|--------|
| Risk | App ทำ HTTP request ไปยัง URL ที่ attacker กำหนด |
| Examples | URL preview → AWS metadata, webhook ไม่ validate |
| Fix | Allowlist domains, block internal IPs, network segmentation |
