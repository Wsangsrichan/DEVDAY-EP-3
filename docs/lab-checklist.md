# Lab Checklist & Scoring Sheet

## Pre-Lab Setup

- [ ] Git installed
- [ ] IDE/Text editor ready
- [ ] Semgrep installed (`pip install semgrep` or `brew install semgrep`)
- [ ] Syft installed (`curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s`)
- [ ] Gitleaks installed (`brew install gitleaks` or download from GitHub releases)
- [ ] Repository cloned: `git clone https://github.com/Wsangsrichan/DEVDAY-EP-3.git`

## Exercise 1: Manual Code Review (Session 2)

Review `lab/vulnerable-app/app.py` and find as many vulnerabilities as possible:

| # | Vulnerability | Line(s) | Found? |
|---|--------------|---------|--------|
| 1 | Hardcoded credentials (DB_PASSWORD, API_KEY) | 14-16 | [ ] |
| 2 | Weak Flask secret_key | 19 | [ ] |
| 3 | SQL Injection (get_users) | 28 | [ ] |
| 4 | SQL Injection (login) | 38 | [ ] |
| 5 | XSS — user input rendered in HTML | 52 | [ ] |
| 6 | Command Injection (ping) | 65 | [ ] |
| 7 | Path Traversal (file read) | 73 | [ ] |
| 8 | Weak hashing (MD5, no salt) | 87 | [ ] |
| 9 | Missing authorization (admin endpoints) | 96-106 | [ ] |
| 10 | Verbose error messages (debug) | 112 | [ ] |
| 11 | SSRF (fetch arbitrary URL) | 126 | [ ] |
| 12 | Insecure deserialization (pickle) | 137 | [ ] |

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
