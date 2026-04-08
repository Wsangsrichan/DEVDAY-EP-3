# DEVDAY EP.3 — Security Code Review & Scanning Tools

> Hands-on Workshop | 3 Hours | Detailed Course Outline

Learn to find and fix security vulnerabilities through manual code review and automated scanning tools

## Course Overview

เรียนรู้การตรวจสอบความปลอดภัยของ source code ด้วย manual code review และการใช้เครื่องมือ security scanning tools เพื่อค้นหาช่องโหว่และความเสี่ยงด้านความปลอดภัย ก่อนนำ code ไป deploy จริง

## Learning Objectives

เมื่อจบ workshop นี้ ผู้เรียนจะสามารถ:

- เข้าใจหลักการ secure coding และช่องโหว่ที่พบบ่อย (OWASP Top 10)
- ทำ manual code review เพื่อหาจุดอ่อนด้านความปลอดภัย
- ใช้ security scanning tools วิเคราะห์ code อัตโนมัติ
- ตีความและแก้ไขผลลัพธ์จาก security tools
- บูรณาการ security scanning เข้ากับ CI/CD pipeline

## Prerequisites

- มีประสบการณ์พัฒนา software อย่างน้อย 1 ปี
- เข้าใจพื้นฐาน web application security
- รู้จักใช้ Git พื้นฐาน
- มี laptop + internet connection
- ติดตั้ง: Git, IDE/Text editor, Docker (optional)

## Timeline Summary (3 Hours)

| Time | Session |
|------|---------|
| 09:00 - 09:45 | Session 1: Security Fundamentals & OWASP Top 10 (45 min) |
| 09:45 - 10:15 | Session 2: Manual Code Review Techniques + Exercise (30 min) |
| 10:15 - 10:25 | Break (10 min) |
| 10:25 - 10:45 | Session 3: Security Scanning Tools Overview (20 min) |
| 10:45 - 11:35 | Session 4: Hands-on Lab — Security Scanning (50 min) |
| 11:35 - 11:55 | Session 5: CI/CD Integration & Best Practices (20 min) |
| 11:55 - 12:00 | Q&A & Wrap-up (5 min) |
| **Bonus** | **Appendix: Security Dockerfile & Docker Compose (Self-study)** |

---

## Session 1: Security Fundamentals & OWASP Top 10

**Duration**: 45 minutes | 09:00 - 09:45

### 1.1 Course Introduction (5 min)
- แนะนำผู้สอนและผู้เรียนสั้นๆ
- Course objectives: ทำไมต้อง scan code เพื่อความปลอดภัย
- Shift-Left Security: ยิ่งเจอช่องโหว่เร็ว ค่าใช้จ่ายในการแก้ไขยิ่งต่ำ
- สถิติ: ความเสียหายจาก security breaches เฉลี่ย $4.45M ต่อครั้ง (IBM 2023)

### 1.2 OWASP Top 10 (40 min)

OWASP (Open Worldwide Application Security Project) จัดอันดับ 10 ความเสี่ยงด้านความปลอดภัยที่สำคัญที่สุดสำหรับ web applications (ล่าสุด 2025):

<details>
<summary><strong>A01: Broken Access Control</strong></summary>

ผู้ใช้สามารถเข้าถึงข้อมูลหรือ function ที่ไม่ได้รับอนุญาต
- IDOR, privilege escalation, force browsing, **SSRF** (รวมจาก A10)
- Fix: Authorization check ทุก request, RBAC, deny by default, allowlist URLs, block internal IPs

</details>

<details>
<summary><strong>A02: Security Misconfiguration</strong></summary>

ตั้งค่าระบบไม่ถูกต้อง ปล่อย default settings
- DEBUG=True in prod, default credentials, public S3 buckets, directory listing, missing security headers
- Fix: Hardening checklist, env-specific configs, automated scanning, security headers (CSP, HSTS)

</details>

<details>
<summary><strong>A03: Software Supply Chain Failures</strong> 🆕</summary>

ใช้ library CI/CD pipeline หรือ dependency ที่ถูก compromise
- XZ Utils backdoor (CVE-2024-3094), dependency confusion, SolarWinds, compromised npm/PyPI packages
- Fix: SBOM generation (Syft), lock files, private registries, verify checksums, SCA tools (Dependency-Track)

</details>

<details>
<summary><strong>A04: Cryptographic Failures</strong></summary>

การเข้ารหัสที่ไม่เหมาะสม ไม่มีเลย หรือใช้ algorithm ที่ล้าสมัย
- Plain text passwords, MD5/SHA1, TLS 1.0/1.1 ยังใช้อยู่, hardcoded keys, weak IV/salt
- Fix: bcrypt/argon2, TLS 1.3, AES-256-GCM, key rotation, ไม่ hardcode

</details>

<details>
<summary><strong>A05: Injection (SQL, XSS, Command, XXE)</strong></summary>

ข้อมูลที่ผู้ใช้ป้อนถูกนำไป execute โดยตรงโดยไม่ผ่านการ sanitize
- SQL Injection, XSS, Command Injection, **XXE (XML External Entities)**
- Fix: Parameterized queries, input validation, output encoding, disable DTD in XML parsers

</details>

<details>
<summary><strong>A06: Insecure Design</strong></summary>

ปัญหาที่เกิดจากการออกแบบระบบที่ไม่ปลอดภัยตั้งแต่แรก
- ไม่มี rate limiting, คำถาม security ที่เดาง่าย, ไม่มี threat modeling
- Fix: Threat modeling, secure design patterns, abuse case testing, rate limiting

</details>

<details>
<summary><strong>A07: Authentication Failures</strong></summary>

ระบบ authentication อ่อนแอ
- Weak passwords, no MFA, session ID in URL, credential stuffing, weak session management
- Fix: Strong password policy, MFA, secure sessions, rate limiting, account lockout

</details>

<details>
<summary><strong>A08: Software or Data Integrity Failures</strong></summary>

ไม่ตรวจสอบ integrity ของ software หรือ data
- SolarWinds attack, untrusted libraries, insecure deserialization, unsigned updates
- Fix: Digital signatures, verify checksums, secure CI/CD, SLSA framework

</details>

<details>
<summary><strong>A09: Security Logging and Alerting Failures</strong></summary>

ไม่มี logging/alerting เพียงพอ
- ไม่ log failed logins, log sensitive data, ไม่มี alerting, no centralized logging
- Fix: Log security events, centralized logging (ELK, Loki), real-time alerting, IR plan

</details>

<details>
<summary><strong>A10: Mishandling of Exceptional Conditions</strong> 🆕</summary>

การจัดการ errors/exceptions ไม่ดี ทำให้เกิดช่องโหว่
- Fail-open แทน fail-closed, crash DoS จาก unhandled exception, sensitive data ใน error messages
- Fix: Fail-closed by default, global exception handlers, sanitize error messages, log internally

</details>

---

## Session 2: Manual Code Review Techniques + Exercise

**Duration**: 30 minutes | 09:45 - 10:15

### 2.1 Code Review Checklist (12 min)
- **Input Validation**: validate type, length, format, range ทุก user input
- **Authentication & Authorization**: password policy, session timeout, authorization check ทุก endpoint
- **Session Management**: secure, httpOnly, sameSite cookies, session regeneration
- **Cryptography**: ใช้ algorithm ทันสมัย (ไม่ใช่ MD5, SHA1), key management ไม่ hardcode
- **Error Handling & Logging**: ไม่ expose stack trace, log พอแต่ไม่ log sensitive data
- **Sensitive Data Exposure**: ไม่เก็บ credentials/API keys ใน source code

### 2.2 Hands-on Exercise 1: Manual Review (18 min)
- กลุ่มละ 2-3 คน หาช่องโหว่ใน `lab/vulnerable-app/app.py` (12 จุด)
- Review Together: เฉลยและอธิบายช่องโหว่แต่ละจุด

---

## Break

**10 minutes** | 10:15 - 10:25

---

## Session 3: Security Scanning Tools Overview

**Duration**: 20 minutes | 10:25 - 10:45

### 3.1 SAST — Static Application Security Testing (8 min)
- **Semgrep** (main tool): Open source, pattern-based, 30+ languages, custom rules
- Others: SonarQube, Bandit (Python), ESLint Security (JS)

### 3.2 SCA — Software Composition Analysis (6 min)
- **Syft** (SBOM Generator): CycloneDX/SPDX, multiple ecosystems
- **Dependency-Track**: Vulnerability management platform, NVD/OSV/GitHub Advisories
- **DefectDojo**: Findings aggregator, 150+ tool importers

### 3.3 Secret Scanning (6 min)
- **Gitleaks** (main tool): Scan git history, regex + entropy, custom rules, pre-commit hook

---

## Session 4: Hands-on Lab — Security Scanning

**Duration**: 50 minutes | 10:45 - 11:35

### 4.1 Lab Setup (10 min)
- Clone vulnerable app, verify tools, แจก Lab checklist

### 4.2 Part A: SAST Scanning ด้วย Semgrep (15 min)
- Run scan, analyze results, compare with manual review

### 4.3 Part B: SCA ด้วย Syft + Dependency-Track (10 min)
- Generate SBOM, import to Dependency-Track, analyze vulnerabilities

### 4.4 Part C: Secret Scanning ด้วย Gitleaks (10 min)
- Run scan, classify true/false positives, remediation

### 4.5 Part D: Docker Security Review (Bonus)
- Review Dockerfile และ docker-compose.yml vulnerabilities

### 4.6 Exercise 3: Fix & Validate (10 min)
- แก้ไข 3-5 critical vulnerabilities แล้วรัน scan อีกครั้ง

---

## Session 5: CI/CD Integration & Best Practices

**Duration**: 20 minutes | 11:35 - 11:55

### 5.1 CI/CD Integration — GitHub Actions (10 min)
- Pre-commit Hooks, PR/MR Checks, Scheduled Full Scan

### 5.2 Best Practices & Security Culture (10 min)
- Scan Early, Scan Often
- Automate Everything
- Fix Critical First
- Track Security Debt
- Security Champions

---

## Q&A & Wrap-up

**5 minutes** | 11:55 - 12:00

---

## Appendix: Security Dockerfile & Docker Compose

**Bonus Content** | Self-study / Reference

### B1: Secure Dockerfile Best Practices
- B1.1 ใช้ Minimal Base Image (Alpine, Distroless, slim)
- B1.2 ไม่ Run เป็น Root (USER directive)
- B1.3 Multi-stage Builds
- B1.4 Pin Versions & Verify Integrity (SHA256 digest)
- B1.5 ลด Layer และ Clean Up (.dockerignore)
- B1.6 COPY แทน ADD
- B1.7 Health Check
- B1.8 Read-only Filesystem
- B1.9 Scan Image ด้วย Trivy / Syft

### B2: Secure Docker Compose Configuration
- B2.1 Security Options (read_only, no-new-privileges, cap_drop)
- B2.2 Resource Limits (CPU, memory, pids)
- B2.3 Network Security (segmentation, internal networks)
- B2.4 Secrets Management (.env, Docker Secrets, Vault)
- B2.5 Logging & Monitoring
- B2.6 Health Checks in Compose

ดูตัวอย่าง secure Dockerfile และ docker-compose.yml ที่ `lab/solutions/`

---

## Tools Summary

| Category | Tool (Lab) | Others |
|----------|-----------|--------|
| SAST | **Semgrep** | SonarQube, Bandit, ESLint Security |
| SCA / SBOM | **Syft**, **Dependency-Track**, **DefectDojo** | Snyk, Trivy |
| Secret Scanning | **Gitleaks** | TruffleHog, detect-secrets |
| Container Security | **Trivy**, **Syft** (image scan) | Docker Bench, Hadolint |
| CI/CD | **GitHub Actions** | GitLab CI, Jenkins |

## Materials Provided

- Slide presentation (Reveal.js)
- Security scanning checklist
- OWASP Top 10 quick reference
- Tool comparison matrix
- Vulnerable code examples
- Sample CI/CD configurations (GitHub Actions, GitLab CI, Jenkins)
- Secure Dockerfile & docker-compose.yml templates
- Docker security scanning checklist
- Step-by-step lab instructions ([docs/lab-instructions.md](docs/lab-instructions.md))
- Speaker notes

## Target Audience

- Developers ที่ต้องการเพิ่มความรู้ด้าน security
- QA/Test engineers
- DevOps/DevSecOps engineers
- Security champions ในทีม
- Tech leads / Team leads
- Anyone involved in SDLC

## Quick Start

```bash
# Clone
git clone https://github.com/Wsangsrichan/DEVDAY-EP-3.git
cd DEVDAY-EP-3

# Open slides
open slides/index.html    # macOS
xdg-open slides/index.html  # Linux

# Lab setup
cd lab/vulnerable-app
pip install -r requirements.txt
```

> **Lab Step-by-Step Guide**: [docs/lab-instructions.md](docs/lab-instructions.md)
