# Lab Checklist & Scoring Sheet

> DEVDAY EP.3 — 4-hour workshop (08:00-12:30)
> Labs run in **Session 2** (Manual Review) + **Session 4** (Automated Scanning)
> **Session 5** = Dynamic Testing (JWT / File Upload / OS Command Injection) — ไม่มี scoring sheet
> **Appendix B** (CI/CD Integration) = self-study

## Timeline Summary

| Time | Session | Lab Activity |
|------|---------|--------------|
| 08:00-08:30 | Registration | — |
| 08:30-09:15 | Session 1: OWASP + SDLC Intro | — |
| 09:15-10:00 | Session 2: Manual Code Review | Exercise 1 |
| 10:00-10:15 | Break | — |
| 10:15-10:45 | Session 3: Tools Overview + ITSC MIS | — |
| 10:45-11:30 | Session 4: Hands-on Lab | Part A/B/C + Exercise 3 + Part D (bonus) |
| 11:30-12:30 | Session 5: Dynamic Testing | Slides + demo (no checklist) |
| 12:30+ | Lunch | — |

## Pre-Lab Setup

- [ ] Git installed
- [ ] IDE/Text editor ready
- [ ] Semgrep installed (`pip install semgrep` or `brew install semgrep`)
- [ ] Syft installed (`curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s`)
- [ ] Gitleaks installed (`brew install gitleaks` or download from GitHub releases)
- [ ] Repository cloned: `git clone https://github.com/Wsangsrichan/DEVDAY-EP-3.git`

## Exercise 1: Manual Code Review (Session 2)

Review `lab/vulnerable-app/app.py` and find as many vulnerabilities as possible:

| # | Vulnerability | Line(s) | OWASP 2025 | Found? |
|---|--------------|---------|-------------|--------|
| 1 | Hardcoded credentials (DB_PASSWORD, API_KEY) | 17-20 | A02: Misconfiguration | [ ] |
| 2 | Weak Flask secret_key | 23 | A02: Misconfiguration | [ ] |
| 3 | SQL Injection (get_users) | 38-47 | A05: Injection | [ ] |
| 4 | SQL Injection (login) | 50-66 | A05: Injection | [ ] |
| 5 | XSS — user input rendered in HTML | 69-83 | A05: Injection | [ ] |
| 6 | Command Injection (ping) | 87-92 | A05: Injection | [ ] |
| 7 | Path Traversal (file read) | 95-106 | A01: Broken Access Control | [ ] |
| 8 | Weak hashing (MD5, no salt) | 109-119 | A04: Cryptographic Failures | [ ] |
| 9 | Missing authorization (admin endpoints) | 132-151 | A01: Broken Access Control | [ ] |
| 10 | Verbose error messages (debug) | 154-171 | A10: Exceptional Conditions | [ ] |
| 11 | SSRF (fetch arbitrary URL) | 174-185 | A01: Broken Access Control | [ ] |
| 12 | Insecure deserialization (pickle) | 188-198 | A08: Integrity Failures | [ ] |

**Bonus**: Also check `config.js` for hardcoded secrets!

**Score**: ___ / 12 found

## Part A: SAST with Semgrep (Session 4)

```bash
cd lab/vulnerable-app
semgrep scan --config auto --json --output semgrep-results.json .
```

- [ ] Ran Semgrep scan successfully
- [ ] Reviewed results by severity
- [ ] Compared with manual review findings
- [ ] Identified what Semgrep found that manual review missed
- [ ] Identified what manual review found that Semgrep missed

## Part B: SCA with Syft + Dependency-Track (Session 4)

```bash
cd lab/vulnerable-app
syft . -o cyclonedx-json > sbom.json
```

- [ ] Generated SBOM with Syft
- [ ] Reviewed SBOM contents (dependencies list)
- [ ] Uploaded to Dependency-Track (if available)
- [ ] Identified vulnerable dependencies and their CVEs
- [ ] Checked fixed versions for critical vulnerabilities

## Part C: Secret Scanning with Gitleaks (Session 4)

```bash
cd lab/vulnerable-app
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

- [ ] Ran Gitleaks scan
- [ ] Reviewed detected secrets
- [ ] Classified true positives vs false positives
- [ ] Identified secret types (API key, password, token)

## Exercise 3: Fix & Validate (Session 4)

Choose 3-5 critical vulnerabilities and fix them:

- [ ] Fixed SQL Injection (use parameterized queries)
- [ ] Fixed XSS (use HTML escaping)
- [ ] Removed hardcoded secrets (use env variables)
- [ ] Updated vulnerable dependencies
- [ ] Added authorization checks
- [ ] Re-ran scans to verify fixes

**Reference solutions**: `lab/solutions/app_fixed.py`

## Part D: Docker Security Review (Session 4)

```bash
cd lab/vulnerable-app
```

Review `Dockerfile` and `docker-compose.yml`:

| # | Vulnerability | File | Found? |
|---|--------------|------|--------|
| 1 | Unpinned image (`python:latest` / `postgres:latest`) | Dockerfile | [ ] |
| 2 | Running as root (no USER directive) | Dockerfile | [ ] |
| 3 | No .dockerignore — .git/.env could enter image | Dockerfile | [ ] |
| 4 | No HEALTHCHECK | Dockerfile | [ ] |
| 5 | CMD shell form instead of exec form | Dockerfile | [ ] |
| 6 | No multi-stage build — build tools in final image | Dockerfile | [ ] |
| 7 | No resource limits (memory, CPU) | docker-compose.yml | [ ] |
| 8 | Secrets as plaintext environment variables | docker-compose.yml | [ ] |
| 9 | Ports bound to 0.0.0.0 (all interfaces) | docker-compose.yml | [ ] |
| 10 | Database port exposed to host | docker-compose.yml | [ ] |
| 11 | Redis without password authentication | docker-compose.yml | [ ] |
| 12 | No network segmentation | docker-compose.yml | [ ] |
| 13 | Host volume mounts giving container host access | docker-compose.yml | [ ] |
| 14 | No `no-new-privileges` security option | docker-compose.yml | [ ] |

**Score**: ___ / 14 found

- [ ] Identified all Dockerfile vulnerabilities
- [ ] Identified all docker-compose.yml vulnerabilities
- [ ] Reviewed fixed versions in `lab/solutions/`
- [ ] Understood Docker secrets vs environment variables
- [ ] Understood multi-stage build benefits
- [ ] Understood network segmentation in compose

---

## Appendix A: Docker Security Scanning Checklist (Self-study)

Use this checklist to review Docker security for any project:

| # | Check Item | Status |
|---|-----------|--------|
| 1 | ใช้ minimal base image (Alpine/Distroless/slim) | [ ] |
| 2 | ไม่ run เป็น root (มี USER instruction) | [ ] |
| 3 | ใช้ multi-stage builds | [ ] |
| 4 | Pin base image version (SHA256 digest) | [ ] |
| 5 | มี .dockerignore (ไม่ COPY .git, .env, node_modules) | [ ] |
| 6 | ไม่มี secrets hardcode ใน Dockerfile/Compose | [ ] |
| 7 | ใช้ COPY แทน ADD | [ ] |
| 8 | มี HEALTHCHECK | [ ] |
| 9 | read_only: true + tmpfs สำหรับ writable dirs | [ ] |
| 10 | cap_drop: ALL + no-new-privileges | [ ] |
| 11 | Resource limits (CPU, memory, pids) | [ ] |
| 12 | Network segmentation (internal networks) | [ ] |
| 13 | Ports bind เฉพาะ localhost สำหรับ internal services | [ ] |
| 14 | Log size limits + centralized logging | [ ] |
| 15 | Scan image ด้วย Trivy/Syft ก่อน deploy | [ ] |

---

## Session 5: Dynamic Testing — Quick Reference

ไม่มี scoring sheet — Session 5 เน้น slides + demo ผ่าน 3 topic:

### 5.1 JWT Vulnerabilities — Checklist หลัง workshop

- [ ] Server enforce `alg` (ไม่ trust header)
- [ ] Secret ≥ 256-bit (generate ด้วย `openssl rand -base64 32`)
- [ ] Token มี `exp` + short expiry + refresh pattern
- [ ] Defend algorithm confusion (RS256 ≠ HS256)
- [ ] `kid` validation — allowlist เท่านั้น

### 5.2 File Upload Vulnerabilities — Checklist หลัง workshop

- [ ] Extension allowlist (ไม่ใช่ blocklist)
- [ ] Magic-byte validation ไม่ trust Content-Type/extension
- [ ] Store file นอก webroot
- [ ] Randomize filename (UUID / hash)
- [ ] ClamAV/antivirus scan ก่อน save
- [ ] Serve จาก separate domain (user-content.*)

### 5.3 OS Command Injection — Checklist หลัง workshop

- [ ] ไม่มี `shell=True` / string concat เข้า subprocess
- [ ] ใช้ arg array: `subprocess.run(['cmd', arg1, arg2])`
- [ ] Input allowlist (regex validation)
- [ ] `shlex.quote` ถ้าเลี่ยง shell ไม่ได้
- [ ] Container: drop capabilities + non-root + no-new-privileges

## Appendix B: CI/CD Integration (Self-study)

เดิมเป็น Session 5 — ย้ายไป self-study เพราะ overlap กับ ITSC MIS use case ใน Session 3
- [ ] Pre-commit hook (Gitleaks) ติดตั้งแล้ว
- [ ] PR check: Semgrep SAST → block Critical/High
- [ ] Build stage: Syft SBOM generation
- [ ] Post-build: Dependency-Track analyze
- [ ] Scheduled weekly full scan
- [ ] Reference: `docs/tool-comparison.md` + GitHub Actions workflow ใน slides deck
