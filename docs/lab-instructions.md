# Lab Step-by-Step Instructions

> DEVDAY EP.3 — Security Code Review & Scanning Tools
> ทำตาม step นี้ทีละขั้นตอน จะได้ไม่พลาด

---

## Section 1: Pre-Lab Setup

**เวลา**: 10 min | **Objective**: ติดตั้งเครื่องมือทั้ง 3 ตัว + clone repo

### Step 1.1: ติดตั้ง Semgrep (SAST Scanner)

**macOS**:
```bash
brew install semgrep
```

**Linux**:
```bash
pip install semgrep
```

**Windows**:
```powershell
pip install semgrep
```

**Verify**:
```bash
semgrep --version
```
ผลลัพธ์ที่ควรเห็น: `1.xx.x` (เลขเวอร์ชัน)

### Step 1.2: ติดตั้ง Syft (SBOM Generator)

**macOS**:
```bash
brew install syft
```

**Linux**:
```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

**Windows**:
```powershell
# ดาวน์โหลดจาก https://github.com/anchore/syft/releases
# แตก zip แล้วเพิ่มไปที่ PATH
```

**Verify**:
```bash
syft version
```
ผลลัพธ์ที่ควรเห็น: `syft <version>`

### Step 1.3: ติดตั้ง Gitleaks (Secret Scanner)

**macOS**:
```bash
brew install gitleaks
```

**Linux**:
```bash
# ดาวน์โหลดจาก https://github.com/gitleaks/gitleaks/releases
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.2/gitleaks_8.18.2_linux_x64.tar.gz
tar -xzf gitleaks_8.18.2_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/
```

**Windows**:
```powershell
# ดาวน์โหลดจาก https://github.com/gitleaks/gitleaks/releases
# เพิ่ม gitleaks.exe ไปที่ PATH
```

**Verify**:
```bash
gitleaks version
```
ผลลัพธ์ที่ควรเห็น: `8.x.x`

### Step 1.4: Clone Repository

```bash
git clone https://github.com/Wsangsrichan/DEVDAY-EP-3.git
cd DEVDAY-EP-3
```

### Step 1.5: ติดตั้ง Dependencies ของ Vulnerable App

```bash
cd lab/vulnerable-app
pip install -r requirements.txt
cd ../..
```

**Verify**:
```bash
cd lab/vulnerable-app && python -c "import flask; print(flask.__version__)"
```
ผลลัพธ์ที่ควรเห็น: `2.0.1`

**Setup เสร็จสมบูรณ์! พร้อมเริ่ม lab แล้ว**

---

## Section 2: Exercise 1 — Manual Code Review

**เวลา**: 18 min | **Objective**: หา 12 ช่องโหว่ใน `lab/vulnerable-app/app.py`

### Step 2.1: เปิดไฟล์และทำความเข้าใจโครงสร้าง

```bash
cd lab/vulnerable-app
wc -l app.py
```
ผลลัพธ์: `204 app.py`

เปิดไฟล์ด้วย IDE หรือ:
```bash
cat -n app.py
```

สังเกตโครงสร้าง:
- มี imports ที่อันตราย: `hashlib`, `subprocess`, `os`, `pickle`
- Flask app ตั้งค่า `secret_key = "secret"`
- มี hardcoded credentials ตั้งแต่บรรทัดแรก

### Step 2.2: หาช่องโหว่ทั้ง 12 จุด

ลองหาดูก่อนเอง! เปิด `app.py` แล้วอ่านทีละ endpoint

<details>
<summary>💡 Hint 1: ดูบรรทัดแรกๆ ของไฟล์ (บรรทัด 1-25)</summary>

มีค่าที่ไม่ควรอยู่ใน source code อย่างน้อย 3 อย่าง ที่เกี่ยวกับ credentials/keys
</details>

<details>
<summary>💡 Hint 2: ดู endpoints ที่รับ user input (บรรทัด 38-92)</summary>

มี 4 endpoints ที่รับ input จากผู้ใช้แล้วนำไปใช้โดยตรงโดยไม่ sanitize:
- `/api/users` — query parameter
- `/api/login` — JSON body
- `/search` — query parameter
- `/api/ping` — query parameter
</details>

<details>
<summary>💡 Hint 3: ดู endpoints ที่เกี่ยวกับ files และ data (บรรทัด 95-198)</summary>

มีช่องโหว่เกี่ยวกับ:
- การอ่านไฟล์ (path traversal)
- การเก็บรหัสผ่าน (weak hashing)
- การเข้าถึง admin (missing authorization)
- Error handling ที่เปิดเผยข้อมูล
- การ fetch URL ภายนอก
- การ deserialize data
</details>

<details>
<summary>✅ คำตอบ — 12 ช่องโหว่ทั้งหมด</summary>

| # | Vulnerability | บรรทัด | OWASP 2025 | รายละเอียด |
|---|--------------|--------|-------------|-----------|
| 1 | **Hardcoded Credentials** | 17-20 | A02: Misconfiguration | `DB_PASSWORD`, `API_KEY`, `ADMIN_PASSWORD` อยู่ใน source code ทุกคนเห็น |
| 2 | **Weak Secret Key** | 23 | A02: Misconfiguration | `app.secret_key = "secret"` — เดาได้ง่าย ใช้ encrypt session cookie |
| 3 | **SQL Injection (users)** | 38-47 | A05: Injection | String concatenation: `"'" + username + "'"` — แทรก SQL ได้ เช่น `' OR 1=1 --` |
| 4 | **SQL Injection (login)** | 50-66 | A05: Injection | f-string: `f"... '{username}' AND '{password}'"` — bypass auth ได้ |
| 5 | **XSS** | 69-83 | A05: Injection | `render_template_string` โดยไม่ escape: `f"... {q}"` — inject `<script>` ได้ |
| 6 | **Command Injection** | 87-92 | A05: Injection | `os.popen(f"ping -c 1 {host}")` — execute command ได้ เช่น `; cat /etc/passwd` |
| 7 | **Path Traversal** | 95-106 | A01: Broken Access Control | `os.path.join("/app/uploads", filename)` — `../../etc/passwd` อ่านไฟล์ระบบ |
| 8 | **Weak Password Hashing** | 109-119 | A04: Cryptographic Failures | `hashlib.md5()` — MD5 เร็ว เกรดย่ำ ไม่มี salt |
| 9 | **Missing Authorization** | 132-151 | A01: Broken Access Control | `/api/admin/users` และ `/api/admin/delete/` ไม่มี auth check — ใครก็ได้เข้าถึง |
| 10 | **Verbose Error Messages** | 154-171 | A10: Exceptional Conditions | ส่ง `traceback`, `os.environ`, `db_path` กลับไปให้ user — เปิดเผยข้อมูลภายใน |
| 11 | **SSRF** | 174-185 | A01: Broken Access Control | `requests.get(url)` โดย user ควบคุม URL — fetch internal services ได้ เช่น `http://localhost:5432` |
| 12 | **Insecure Deserialization** | 188-198 | A08: Integrity Failures | `pickle.loads()` — deserializes untrusted data → remote code execution |
</details>

### Step 2.3: Bonus — ตรวจสอบ `config.js`

```bash
cat lab/vulnerable-app/config.js
```

<details>
<summary>✅ คำตอบ</summary>

`config.js` มี hardcoded secrets อีก 7 อย่าง:
- AWS Access Key ID + Secret Access Key
- JWT Secret
- Stripe Live Key
- GitHub Token
- Slack Webhook URL
- DB Password

เหล่านี้ควรอยู่ใน environment variables หรือ secrets manager เท่านั้น
</details>

---

## Section 3: Part A — SAST Scanning ด้วย Semgrep

**เวลา**: 15 min | **Objective**: ใช้ Semgrep scan หาช่องโหว่อัตโนมัติ

### Step 3.1: รัน Semgrep Scan

```bash
cd lab/vulnerable-app
semgrep scan --config auto --json --output semgrep-results.json .
```

หรือถ้าอยากเห็นผลใน terminal เลย:
```bash
semgrep scan --config auto .
```

**ผลลัพธ์ที่ควรเห็น**: Semgrep จะแสดง findings แบ่งตาม severity:
- `ERROR` (critical) — SQL Injection, Command Injection, Insecure Deserialization
- `WARNING` — Hardcoded secrets, weak hashing, XSS
- `INFO` — best practice violations

### Step 3.2: อ่านผลลัพธ์ JSON

```bash
cat semgrep-results.json | python3 -m json.tool | head -50
```

สังเกต structure:
```json
{
  "results": [
    {
      "check_id": "python.lang.security.audit.dangerous-system-call",
      "path": "app.py",
      "start": {"line": 91},
      "extra": {
        "message": "Detected os.popen...",
        "severity": "ERROR",
        "metadata": {"owasp": "A05: Injection"}
      }
    }
  ]
}
```

### Step 3.3: เปรียบเทียบกับ Manual Review

| ช่องโหว่ | Manual Review | Semgrep | หมายเหตุ |
|---------|:---:|:---:|---------|
| Hardcoded Credentials | ✅ | ✅ | ทั้งสองเจอ |
| SQL Injection | ✅ | ✅ | Semgrep เจอ pattern |
| XSS | ✅ | ⚠️ | Semgrep อาจเจอบาง case |
| Command Injection | ✅ | ✅ | เจอ os.popen |
| Path Traversal | ✅ | ⚠️ | อาจไม่เจอทุก pattern |
| Weak Hashing | ✅ | ✅ | เจอ hashlib.md5 |
| Missing Auth | ✅ | ❌ | Semgrep ไม่เจอ — ต้อง manual |
| SSRF | ✅ | ⚠️ | ขึ้นกับ rules |
| Insecure Deserialization | ✅ | ✅ | เจอ pickle.loads |

<details>
<summary>💡 สรุป</summary>

**Semgrep เจอ ~70-80%** ของช่องโหว่ที่ manual review เจอ
แต่ **ไม่เจอ business logic issues** เช่น missing authorization — นี่คือข้อจำกัดของ automated tools

**Best practice**: ใช้ทั้ง manual review + automated scanning ร่วมกัน
</details>

### Step 3.4: เขียน Custom Semgrep Rule (เบื้องต้น)

```bash
cat > custom-rule.yml << 'EOF'
rules:
  - id: detect-hardcoded-password
    patterns:
      - pattern-either:
          - pattern: $VAR = "supersecret123"
          - pattern: $VAR = "admin123"
      - pattern-not: "# ..."
    message: "Hardcoded password detected"
    severity: ERROR
    languages: [python]
EOF

semgrep scan --config custom-rule.yml app.py
```

---

## Section 4: Part B — SCA ด้วย Syft (SBOM)

**เวลา**: 10 min | **Objective**: สร้าง Software Bill of Materials และวิเคราะห์ dependencies

### Step 4.1: Generate SBOM

```bash
cd lab/vulnerable-app
syft . -o cyclonedx-json > sbom.json
```

**ผลลัพธ์ที่ควรเห็น**:
```
 ✔ Indexed file system
 ✔ Loaded catalog
 ✔ Generated SBOM
```

### Step 4.2: อ่าน SBOM Contents

```bash
python3 -c "
import json
with open('sbom.json') as f:
    sbom = json.load(f)
comps = sbom.get('components', [])
print(f'Total dependencies: {len(comps)}')
for c in comps:
    name = c.get('name','?')
    ver = c.get('version','?')
    print(f'  {name} == {ver}')
"
```

**ผลลัพธ์ที่ควรเห็น**:
```
Total dependencies: 8
  flask == 2.0.1
  requests == 2.25.0
  jinja2 == 2.11.3
  werkzeug == 2.0.1
  urllib3 == 1.26.4
  cryptography == 3.3.2
  pyyaml == 5.3.1
```

### Step 4.3: ระบุ Vulnerable Dependencies

<details>
<summary>✅ Dependencies ที่มีช่องโหว่</summary>

| Package | Version | ปัญหา | Fixed Version |
|---------|---------|--------|--------------|
| **Flask** | 2.0.1 | CVE-2023-30861: Open redirect | 2.3.2+ |
| **Jinja2** | 2.11.3 | CVE-2024-22195: XSS in xmlattr filter | 3.1.3+ |
| **Werkzeug** | 2.0.1 | CVE-2023-23934: Multipart form parse | 2.3.7+ |
| **urllib3** | 1.26.4 | CVE-2023-43804: Request body not stripped after redirect | 1.26.18+ |
| **cryptography** | 3.3.2 | Multiple CVEs | 41.0.0+ |
| **PyYAML** | 5.3.1 | CVE-2020-14343: Arbitrary code execution | 5.4+ |

</details>

### Step 4.4: สร้าง SBOM แบบอ่านง่าย (Table)

```bash
syft . -o table
```

ผลลัพธ์จะแสดงเป็นตารางสวยงามพร้อม purl identifiers

---

## Section 5: Part C — Secret Scanning ด้วย Gitleaks

**เวลา**: 10 min | **Objective**: ค้นหา secrets/API keys ที่ซ่อนอยู่ใน code

### Step 5.1: รัน Gitleaks Scan

```bash
cd lab/vulnerable-app
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

หรือดูผลใน terminal:
```bash
gitleaks detect --source . --verbose
```

**ผลลัพธ์ที่ควรเห็น**: Gitleaks จะแสดง findings พร้อม secret type:

```
    12:     API_KEY = "sk-proj-abc123def456..."
Finding:     file:app.py
Secret:      sk-proj-abc123def456ghi789jkl012mno345pqr678
RuleID:      generic-api-key
Entropy:     3.75
...

    19:     DB_PASSWORD = "supersecret123"
Finding:     file:app.py
Secret:      supersecret123
RuleID:      generic-api-key
Entropy:     3.12
...
```

### Step 5.2: อ่าน Report JSON

```bash
python3 -c "
import json
with open('gitleaks-report.json') as f:
    report = json.load(f)
print(f'Total findings: {len(report)}')
print()
for r in report:
    print(f\"File: {r['File']}  Line: {r['StartLine']}\")
    print(f\"  Secret: {r['Secret'][:30]}...\")
    print(f\"  Rule: {r['RuleID']}\")
    print()
"
```

### Step 5.3: Classify True Positives vs False Positives

<details>
<summary>✅ Classification</summary>

| Finding | File | True/False Positive | เหตุผล |
|---------|------|:---:|--------|
| `sk-proj-...` | app.py:19 | **True Positive** | OpenAI API key format |
| `supersecret123` | app.py:18 | **True Positive** | Hardcoded DB password |
| `admin123` | app.py:20 | **True Positive** | Hardcoded admin password |
| `secret` | app.py:23 | **True Positive** | Flask secret key |
| `AKIAIOSFODNN7EXAMPLE` | config.js:8 | **True Positive** | AWS Access Key ID format |
| `wJalrXUtnFEMI...` | config.js:9 | **True Positive** | AWS Secret Key |
| `sk_live_EXAMPLE...` | config.js:11 | **True Positive** | Stripe Live Key |
| `ghp_EXAMPLE...` | config.js:13 | **True Positive** | GitHub Token format |

ทั้งหมดเป็น **True Positive** — เพราะ vulnerable app ออกแบบมาให้มีช่องโหว่จริงๆ

ใน real-world จะมี False Positives ด้วย เช่น test fixtures, example values ใน docs
</details>

### Step 5.4: สร้าง Gitleaks Allowlist (Optional)

ในโปรเจกต์จริง ถ้ามี false positives สามารถสร้าง `.gitleaksignore`:
```bash
cat > .gitleaksignore << 'EOF'
# ตัวอย่าง: ยกเว้น test files
-- allowlist description: "test fixtures"
path: tests/fixtures/
EOF
```

---

## Section 6: Exercise 3 — Fix & Validate

**เวลา**: 10 min | **Objective**: แก้ไข 3-5 ช่องโหว่แล้วรัน scan อีกครั้ม

### Step 6.1: แก้ SQL Injection

**Before** (app.py บรรทัด 43):
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
```

**After**:
```python
query = "SELECT * FROM users WHERE username = ?"
cursor = conn.execute(query, (username,))
```

ทำเช่นเดียวกันกับ `/api/login` (บรรทัด 59):
```python
# Before
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# After
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor = conn.execute(query, (username, password))
```

### Step 6.2: แก้ XSS

**Before** (app.py บรรทัด 74):
```python
html = f"""<h1>Search Results</h1><p>You searched for: {q}</p>"""
```

**After**:
```python
from markupsafe import escape

html = f"""<h1>Search Results</h1><p>You searched for: {escape(q)}</p>"""
```

### Step 6.3: ลบ Hardcoded Secrets

**Before** (app.py บรรทัด 17-23):
```python
DB_PASSWORD = "supersecret123"
API_KEY = "sk-proj-abc123def456..."
ADMIN_PASSWORD = "admin123"
app.secret_key = "secret"
```

**After**:
```python
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY = os.environ.get("API_KEY")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
```

### Step 6.4: Re-run Scan เพื่อ Verify

```bash
semgrep scan --config auto app.py 2>&1 | grep -E "(ERROR|WARNING|found)"
```

ผลลัพธ์ที่ควรเห็น: จำนวน findings ลดลง เช่น:
- SQL Injection findings: **หาย** (fixed)
- Hardcoded secrets: **ลดลง** (แต่ยังมีใน config.js)
- XSS: **ลดลง** หรือหาย

<details>
<summary>💡 ดู Fixed Version เต็ม</summary>

```bash
cat ../solutions/app_fixed.py
```

ไฟล์นี้มีทุกช่องโหว่แก้แล้ว — ใช้เป็น reference
</details>

---

## Section 7: Part D — Docker Security Review (Bonus)

**เวลา**: Self-study | **Objective**: ระบุช่องโหว่ใน Dockerfile + docker-compose.yml

### Step 7.1: Review Dockerfile

```bash
cd lab/vulnerable-app
cat -n Dockerfile
```

<details>
<summary>✅ 12 ช่องโหว่ใน Dockerfile</summary>

| # | Vulnerability | บรรทัด | อธิบาย |
|---|--------------|--------|--------|
| 1 | **Unpinned Image** | 7 | `FROM python:3.9` — ไม่ได้ pin เวอร์ชันที่แน่นอน (ใช้ SHA256 digest) |
| 2 | **Running as Root** | - | ไม่มี `USER` directive — container ทำงานเป็น root |
| 3 | **COPY All Files** | 13 | `COPY . /app` — คัดลอกทุกอย่าง รวม .git, .env, secrets |
| 4 | **No .dockerignore** | - | ไม่มีไฟล์ .dockerignore — build context ใหญ่เกิน |
| 5 | **No Multi-stage Build** | - | final image มี build tools + source code ทั้งหมด |
| 6 | **Shell Form CMD** | 34 | `CMD python app.py` — PID 1 เป็น shell ไม่ใช่ app, signal ไม่ถึง app |
| 7 | **No HEALTHCHECK** | - | ไม่สามารถ monitor สถานะ container |
| 8 | **Debug Port Exposed** | 30 | `EXPOSE 5678` — debug port เปิดอยู่ |
| 9 | **No Resource Limits** | - | ไม่จำกัด CPU/memory — DoS ได้ |
| 10 | **No Read-only FS** | - | container เขียนไฟล์ได้ทุกที่ |
| 11 | **No Security Options** | - | ไม่มี `no-new-privileges`, seccomp |
| 12 | **Unverified Build** | 18 | `pip install` จาก internet โดยไม่ verify checksum |
</details>

### Step 7.2: Review docker-compose.yml

```bash
cat -n docker-compose.yml
```

<details>
<summary>✅ 20 ช่องโหว่ใน docker-compose.yml</summary>

| # | Vulnerability | บรรทัด | อธิบาย |
|---|--------------|--------|--------|
| 1 | **No Resource Limits** | 13-21 | app service ไม่มี `deploy.resources.limits` |
| 2 | **Binding All Interfaces** | 19 | `"5000:5000"` binds 0.0.0.0 — ใครก็ได้เข้าถึง |
| 3 | **Debug Port Exposed** | 22 | `"5678:5678"` — Python debug port เปิดสู่โลกภายนอก |
| 4 | **Secrets in Plaintext** | 27-36 | รหัสผ่าน, API keys, JWT secrets อยู่ใน environment เป็น plain text |
| 5 | **No Security Options** | - | ไม่มี `security_opt: no-new-privileges:true` |
| 6 | **No Healthcheck** | - | Docker ไม่สามารถ detect ว่า app ใช้งานได้ |
| 7 | **No Read-only FS** | - | filesystem เปิดให้เขียนทุกที่ |
| 8 | **No Network Segmentation** | 65 | ทุก service อยู่ network เดียว — ไม่มี isolation |
| 9 | **depends_on ไม่มี Condition** | 53 | app อาจ start ก่อน DB พร้อม — ทำให้ leak connection string ใน logs |
| 10 | **Host Volume Mount** | 59 | `./data:/app/data` — container อาจเข้าถึง host filesystem |
| 11 | **Upload Volume Mount** | 62 | `./uploads:/app/uploads` — อันตรายถ้ามี path traversal |
| 12 | **Unpinned DB Image** | 70 | `postgres:15` — ไม่ pin SHA256 |
| 13 | **No DB Resource Limits** | 71-72 | database ไม่มี resource limits |
| 14 | **Hardcoded DB Credentials** | 77-79 | `POSTGRES_USER=admin`, `POSTGRES_PASSWORD=supersecret123` |
| 15 | **No Volume Encryption** | 83 | database data ไม่ encrypt at rest |
| 16 | **DB Port Exposed** | 87 | `"5432:5432"` — database port เปิดสู่ host |
| 17 | **No DB Healthcheck** | - | ไม่ monitor สถานะ database |
| 18 | **Redis No Auth** | 96-98 | Redis ไม่มี `requirepass` — ใครก็เข้าถึงได้ |
| 19 | **Redis Latest Tag** | 98 | `redis:latest` — ไม่ pin version |
| 20 | **Default Bridge Network** | 111-114 | traffic ไม่มี encryption in transit |
</details>

### Step 7.3: เปรียบเทียบกับ Fixed Version

```bash
cat ../solutions/Dockerfile
```

<details>
<summary>✅ จุดที่แก้ใน Fixed Dockerfile</summary>

- ใช้ `python:3.9-slim` (minimal image)
- เพิ่ม `USER appuser` (ไม่ run เป็น root)
- ใช้ multi-stage build
- เพิ่ม `.dockerignore`
- เพิ่ม `HEALTHCHECK`
- ใช้ exec form `CMD ["python", "app.py"]`
- เพิ่ม `COPY --chown=appuser:appuser`
- เพิ่ม `WORKDIR /app`
- ไม่มี debug port
</details>

```bash
cat ../solutions/docker-compose.yml
```

<details>
<summary>✅ จุดที่แก้ใน Fixed docker-compose.yml</summary>

- เพิ่ม resource limits (`mem_limit`, `cpus`)
- bind `127.0.0.1:5000:5000` (localhost only)
- ลบ debug port
- ใช้ Docker secrets แทน plaintext env vars
- เพิ่ม `security_opt: no-new-privileges:true`
- เพิ่ม `read_only: true` + `tmpfs`
- เพิ่ม `healthcheck`
- ใช้ internal network + dedicated backend network
- ปิด DB port ไม่ expose สู่ host
- เพิ่ม Redis `requirepass`
- Pin image versions
</details>

### Step 7.4: Scan Docker Image (Optional — ถ้ามี Docker)

```bash
# ติดตั้ง Trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Scan image
trivy image python:3.9
```

---

## เสร็จสิ้น Lab!

**สรุปสิ่งที่เรียนรู้:**

| Tool | ที่ค้นพบ | ข้อจำกัด |
|------|---------|---------|
| **Manual Review** | Business logic, auth issues, design flaws | ช้า, ขึ้นกับความเชี่ยวชาญ |
| **Semgrep (SAST)** | Injection, hardcoded secrets, crypto issues | ไม่เจอ logic issues |
| **Syft (SCA)** | Vulnerable dependencies + versions | ต้อง check CVE manually |
| **Gitleaks** | Hardcoded secrets ทุกประเภท | มี false positives |

**Best Practice**: ใช้ทั้ง 4 เครื่องมือร่วมกัน + integrate เข้า CI/CD pipeline
