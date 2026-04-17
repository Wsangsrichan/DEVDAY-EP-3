# DEVDAY EP.3 — Security Code Review & Scanning Tools

> Hands-on Workshop | 4 Hours (08:00-12:30) | Detailed Course Outline

Learn to find and fix security vulnerabilities through manual code review, automated scanning tools, and dynamic testing

## Course Overview

เรียนรู้การตรวจสอบความปลอดภัยของ source code ด้วย manual code review, การใช้เครื่องมือ security scanning tools และ dynamic testing เพื่อค้นหาช่องโหว่และความเสี่ยงด้านความปลอดภัย ก่อนนำ code ไป deploy จริง

## Learning Objectives

เมื่อจบ workshop นี้ ผู้เรียนจะสามารถ:

- เข้าใจบทบาทของ Security Scanning ในวงจร SDLC (DevOps infinity loop)
- เข้าใจหลักการ secure coding และช่องโหว่ที่พบบ่อย (OWASP Top 10)
- ทำ manual code review เพื่อหาจุดอ่อนด้านความปลอดภัย
- ใช้ security scanning tools วิเคราะห์ code อัตโนมัติ
- ตีความและแก้ไขผลลัพธ์จาก security tools
- เข้าใจ dynamic testing: JWT attacks, file upload vulnerabilities, OS command injection
- เชื่อมโยง tools เข้ากับ real-world pipeline (ITSC MIS use case)

## Prerequisites

- มีประสบการณ์พัฒนา software อย่างน้อย 1 ปี
- เข้าใจพื้นฐาน web application security
- รู้จักใช้ Git พื้นฐาน
- มี laptop + internet connection
- ติดตั้ง: Git, IDE/Text editor, Docker (optional)

## Timeline Summary (4 Hours | 08:00 - 12:30)

| Time | Session |
|------|---------|
| 08:00 - 08:30 | Registration (30 min) |
| 08:30 - 09:15 | Session 1: Security Fundamentals & OWASP Top 10 + SDLC Intro (45 min) |
| 09:15 - 10:00 | Session 2: Manual Code Review + Hands-on 1 (45 min) |
| 10:00 - 10:15 | Break (15 min) |
| 10:15 - 10:45 | Session 3: Security Scanning Tools Overview + ITSC MIS Use Case (30 min) |
| 10:45 - 11:30 | Session 4: Hands-on Lab — Security Scanning & Remediation (45 min) |
| 11:30 - 12:30 | Session 5: Dynamic Testing — JWT / File Upload / OS Command Injection (60 min) |
| 12:30+ | Lunch |
| **Bonus** | **Appendix A: Security Dockerfile & Docker Compose (Self-study)** |
| **Bonus** | **Appendix B: CI/CD Integration & Best Practices (Self-study)** |

---

## Session 1: Security Fundamentals & OWASP Top 10

**Duration**: 45 minutes | 08:30 - 09:15

### 1.1 Course Introduction (5 min)
- แนะนำผู้สอนและผู้เรียนสั้นๆ
- Course objectives: ทำไมต้อง scan code เพื่อความปลอดภัย
- Shift-Left Security: ยิ่งเจอช่องโหว่เร็ว ค่าใช้จ่ายในการแก้ไขยิ่งต่ำ
- สถิติ: ความเสียหายจาก security breaches เฉลี่ย $4.45M ต่อครั้ง (IBM 2023)

### 1.2 Introduction: Security Scanning ในวงจร SDLC (5-10 min)

**ทำความเข้าใจความสำคัญของ Security Scanning ในวงจร SDLC**

DevOps infinity loop (Dev ↔ Ops): **Plan → Code → Build → Test → Release → Deploy → Operate → Monitor** — security ต้องไหลผ่านทุก phase ไม่ใช่ขั้นตอนแยก

| Phase | Security Activity |
|-------|-------------------|
| Plan | Threat modeling, abuse cases |
| Code | IDE security plugins, pre-commit (Gitleaks) |
| Build (CI) | SAST (Semgrep), SCA (Syft + Dependency-Track), Secret scan |
| Test | DAST baseline |
| Release | Image scan (Trivy/Grype), policy gate |
| Deploy / Operate | Runtime monitoring, vulnerability management, IR |

> Reference diagram (DevOps infinity loop): `https://media.geeksforgeeks.org/wp-content/uploads/20230410112114/DevOps.png`

Shift-Left Security: ยิ่ง security activity เกิดซ้าย (เร็ว) ต้นทุนยิ่งต่ำ — ซ้ายที่สุดคือ Plan/Code, ขวาที่สุดคือ Operate/Monitor

### 1.3 OWASP Top 10 (30-35 min)

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

## Session 2: Manual Code Review + Hands-on 1

**Duration**: 45 minutes | 09:15 - 10:00

### 2.1 Code Review Checklist (15 min)
- **Input Validation**: validate type, length, format, range ทุก user input
- **Authentication & Authorization**: password policy, session timeout, authorization check ทุก endpoint
- **Session Management**: secure, httpOnly, sameSite cookies, session regeneration
- **Cryptography**: ใช้ algorithm ทันสมัย (ไม่ใช่ MD5, SHA1), key management ไม่ hardcode
- **Error Handling & Logging**: ไม่ expose stack trace, log พอแต่ไม่ log sensitive data
- **Sensitive Data Exposure**: ไม่เก็บ credentials/API keys ใน source code

### 2.2 Hands-on 1: Manual Review (30 min)
- กลุ่มละ 2-3 คน หาช่องโหว่ใน `lab/vulnerable-app/app.py` (12 จุด)
- Review Together: เฉลยและอธิบายช่องโหว่แต่ละจุด

---

## Break

**15 minutes** | 10:00 - 10:15

---

## Session 3: Security Scanning Tools Overview + ITSC MIS Use Case

**Duration**: 30 minutes | 10:15 - 10:45

### 3.1 SAST — Static Application Security Testing (6 min)
- **Semgrep** (main tool): Open source, pattern-based, 30+ languages, custom rules
- Others: SonarQube, Bandit (Python), ESLint Security (JS)

### 3.2 SCA — Software Composition Analysis (6 min)
- **Syft** (SBOM Generator): CycloneDX/SPDX, multiple ecosystems
- **Dependency-Track**: Vulnerability management platform, NVD/OSV/GitHub Advisories
- **DefectDojo**: Findings aggregator, 150+ tool importers

### 3.3 Secret Scanning (4 min)
- **Gitleaks** (main tool): Scan git history, regex + entropy, custom rules, pre-commit hook

### 3.4 ITSC MIS Use Case — Real-world Reference Architecture (~10 min)

**Frame**: "Real-world reference architecture — see how each tool slots into a production pipeline"

```
GitLab Repo
    └── CI (Continuous Integration)
        ├── Unit Testing
        ├── SAST Scan (Trivy + Gitleaks)
        ├── Build Artifact
        ├── Docker Image Build & Push (tag v2.4)
        ├── Grype Security Scan (image v2.4)
        ├── Security Policy Check
        └── Update Kubernetes Manifest
    └── CD (Continuous Deployment)
        └── kubectl apply -f ... → Kubernetes Cluster
    └── DAST
        └── Burp-DAST Baseline
    └── Reports & Tracking
        ├── dependency-track
        └── DefectDojo
    └── Notifications
        ├── notify_ci_pipeline
        ├── notify_failure
        └── notify_security_alert
```

**Key takeaways**:
- Tools ทุกตัวที่เราเรียนวันนี้ (Semgrep/Trivy, Syft, Gitleaks, Grype, Dependency-Track, DefectDojo) มีที่ทางจริงใน pipeline ของ ITSC MIS
- Security gate คือ **Security Policy Check** — ถ้าไม่ผ่าน block ไม่ให้ deploy
- Notifications ทั้ง 3 ช่อง = ไม่มี silent failure

---

## Session 4: Hands-on Lab — Security Scanning & Remediation

**Duration**: 45 minutes | 10:45 - 11:30

### 4.1 Lab Setup (5 min)
- Clone vulnerable app, verify tools, แจก Lab checklist

### 4.2 Part A: SAST Scanning ด้วย Semgrep (12 min)
- Run scan, analyze results, compare with manual review

### 4.3 Part B: SCA ด้วย Syft + Dependency-Track (10 min)
- Generate SBOM, import to Dependency-Track, analyze vulnerabilities

### 4.4 Part C: Secret Scanning ด้วย Gitleaks (8 min)
- Run scan, classify true/false positives, remediation

### 4.5 Exercise 3: Fix & Validate (10 min)
- แก้ไข 3-5 critical vulnerabilities แล้วรัน scan อีกครั้ง

### 4.6 Part D: Docker Security Review (Bonus — if time permits)
- Review Dockerfile และ docker-compose.yml vulnerabilities

---

## Session 5: Dynamic Testing

**Duration**: 60 minutes | 11:30 - 12:30

Dynamic testing = การทดสอบ application ขณะรันจริง เพื่อหาช่องโหว่ที่ SAST ตรวจไม่พบ — สาม topic หลักที่พบบ่อยใน pentest report:

### 5.1 JSON Web Token (JWT) Vulnerabilities (~20 min)

- **`alg=none` attack** — server ยอมรับ token ที่ไม่ sign
- **Weak secret / brute-force HS256** — ใช้ wordlist attack secret
- **No expiry / token replay** — token ไม่มี `exp` → ใช้ได้ตลอดไป
- **Algorithm confusion (RS256 → HS256)** — ใช้ public key เป็น HMAC secret
- **Missing `kid` validation** — path traversal ใน key id
- **Mitigations**: enforce `alg`, strong 256-bit secret, short expiry + refresh tokens, `kid` validation, library hardening

### 5.2 File Upload Vulnerabilities (~20 min)

- **Extension bypass** — `.php.jpg`, double extension, null byte (`shell.php%00.jpg`)
- **MIME type spoofing** — `Content-Type: image/jpeg` ต่ฟัง แต่ file คือ PHP
- **Path traversal in filename** — `../../etc/passwd`, `..\\..\\windows`
- **Polyglot files** — ไฟล์เดียว valid ทั้ง JPG + PHP + HTML
- **Mitigations**: extension allowlist, magic-byte validation, store outside webroot, randomize filenames, ClamAV scan, separate domain for uploads

### 5.3 OS Command Injection (~20 min)

- **Shell metacharacters** — `;`, `|`, `&`, `$()`, backticks
- **Argument injection** — `--` flags ที่ attacker ใส่เข้าไป
- **Blind / time-based detection** — ไม่มี output กลับ → ใช้ `sleep 10` / DNS exfil
- **Mitigations**:
  - ไม่ใช้ `shell=True`
  - `subprocess` ด้วย **arg array** (ไม่ใช่ string concat)
  - Allowlist inputs
  - `shlex.quote` ถ้าต้องสร้าง shell command
  - Principle of least privilege — app ไม่ควรมีสิทธิ์เขียนไฟล์ระบบ

---

## Lunch

**12:30 onwards**

---

## Appendix A: Security Dockerfile & Docker Compose

**Bonus Content** | Self-study / Reference

### A1: Secure Dockerfile Best Practices
- A1.1 ใช้ Minimal Base Image (Alpine, Distroless, slim)
- A1.2 ไม่ Run เป็น Root (USER directive)
- A1.3 Multi-stage Builds
- A1.4 Pin Versions & Verify Integrity (SHA256 digest)
- A1.5 ลด Layer และ Clean Up (.dockerignore)
- A1.6 COPY แทน ADD
- A1.7 Health Check
- A1.8 Read-only Filesystem
- A1.9 Scan Image ด้วย Trivy / Syft

### A2: Secure Docker Compose Configuration
- A2.1 Security Options (read_only, no-new-privileges, cap_drop)
- A2.2 Resource Limits (CPU, memory, pids)
- A2.3 Network Security (segmentation, internal networks)
- A2.4 Secrets Management (.env, Docker Secrets, Vault)
- A2.5 Logging & Monitoring
- A2.6 Health Checks in Compose

ดูตัวอย่าง secure Dockerfile และ docker-compose.yml ที่ `lab/solutions/`

---

## Appendix B: CI/CD Integration & Best Practices

**Bonus Content** | Self-study / Reference — เดิมเป็น Session 5 แต่เนื้อหา overlap กับ ITSC MIS use case ใน Session 3 จึงย้ายมาเป็น self-study

### B1: CI/CD Integration — GitHub Actions

- Pre-commit Hooks (Gitleaks block secrets ก่อน commit)
- PR / MR Checks (Semgrep SAST, block on Critical/High)
- Build stage (Syft SBOM generation)
- Post-build (Dependency-Track analyze vulnerabilities)
- Scheduled Full Scan (weekly)

### B2: Best Practices & Security Culture

- **Scan Early, Scan Often** — ยิ่ง scan เร็ว ค่าแก้ยิ่งต่ำ
- **Automate Everything** — security เป็นส่วนหนึ่งของ pipeline
- **Fix Critical First** — จัดลำดับตาม severity
- **Track Security Debt** — บันทึกและติดตาม issues
- **Regular Updates** — อัปเดต dependencies สม่ำเสมอ
- **Security in Every PR** — ทุก review มีมุมมอง security
- **Security Champions** — มี champion ในแต่ละทีม

ดูตัวอย่าง GitHub Actions workflow พร้อมใช้ได้ใน slides (Session 5 deck เดิม) และใน `docs/tool-comparison.md`

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
git clone https://github.com/watcharap0ng/DEVDAY-EP-3.git
cd DEVDAY-EP-3

# Open slides
open slides/index.html    # macOS
xdg-open slides/index.html  # Linux

# Lab setup
cd lab/vulnerable-app
pip install -r requirements.txt
```

> **Lab Step-by-Step Guide**: [docs/lab-instructions.md](docs/lab-instructions.md)
