# Speaker Notes — DEVDAY EP.3
# Security Code Review & Scanning Tools

> สำหรับ presenter อ่านระหว่าง present แยกออกมาเป็นไฟล์เดียว
> Slide แต่ละอันอ้างถึงหมายเลข slide ใน presentation

---

## Slide 1: Title
**Security Code Review & Scanning Tools**

- ทักทายสั้นๆ แนะนำตัวเอง
- ย้ำว่านี่เป็น workshop แบบ hands-on — ไม่ใช่บรรยาย
- เช็ค prerequisites: laptop + internet + tools ติดตั้งแล้ว
- "วันนี้เราจะทำ scan จริง และแก้ช่องโหว่จริง"

---

## Slide 2: Agenda

- อธิบาย flow คร่าวๆ: เริ่มจากพื้นฐาน (OWASP) → review manual → เรียนรู้ tools → ลงมือ lab → CI/CD
- เน้นว่า Session 4 (Lab) เป็นหัวใจของ workshop
- บอกเวลาพัก: 10:15-10:25
- ให้รู้ว่ามี lab checklist ใน `docs/lab-checklist.md`

---

## Slide 3: Session 1 Title
**Security Fundamentals & OWASP Top 10 (45 min)**

- "เริ่มจากพื้นฐานก่อน จะได้เข้าใจ context ของการ scan"
- ใช้เวลา 45 นาที ดีไหม? — ถ้าเหลือเวลา จะย่อ OWASP บางข้อ

---

## Slide 4: Why Security Code Review?

- พูดจาก experience: "เคยเจอ bug ใน production ที่ scan ตั้งแต่ dev แล้วจะเจอ"
- $4.45M — ย้ำตัวเลข ให้คนจำ "4 ล้านกว่าบาท"
- 287 days — "เกือบ 1 ปี ถึงจะรู้ว่าโดน"
- "เป้าหมายคือทำให้เจอเร็วขึ้น ลดเวลา 287 วันนี้ลง"

---

## Slide 5: Shift-Left Security

- อธิบาย concept: ยิ่งซ้าย (เร็ว) ยิ่งถูก
- เปรียบเทียบต้นทุน: ตอน design แก้ฟรี ตอน production แก่ร้อยเท่า
- ให้มองว่า security scan = automated code reviewer ที่ดูแค่มุม security
- "Shift-left ไม่ใช่แค่เรื่อง tools — เป็น mindset ที่ต้องคิด security ตั้งแต่เขียน code"

---

## Slide 6: OWASP Top 10 (2021) — Overview

- อธิบายสั้นๆ ว่า OWASP คืออะไร: องค์กร nonprofit ที่จัดอันดับ web security risks
- อัปเดตทุก 3-4 ปี (ล่าสุด 2021, 2024 กำลังจะออก)
- เน้นว่านี่คือ "common knowledge" ที่ developer ทุกคนควรรู้
- แยก 3 กลุ่ม: แดง (critical) เหลือง (yellow) ฟ้า (cyan) — ให้เห็นระดับความสำคัญ

---

## Slide 7: A01: Broken Access Control

- เน้นว่าขึ้นจากอันดับ 5 → 1 เพราะพบบ่อยที่สุด
- ให้ตัวอย่าง IDOR: "เปลี่ยน URL เลข 1 = เห็นข้อมูลคนอื่น"
- แสดง code ตัวอย่าง: "ดูบรรทัดนี้ ขาดอะไร?" → authorization check
- ถ้ามีเวลา: ให้ผู้เรียนคิดตัวอย่างเพิ่ม (เช่น API ของบริษัทที่เคยเจอ)

---

## Slide 8: A02: Cryptographic Failures

- MD5 คือตัวอย่าง classic — เคยใช้กัน เดี๋วันใช้ bcrypt
- อธิบายว่า hash ≠ encrypt: hash ทางเดียว, encrypt ถอดกลับได้ด้วย key
- เน้น "อย่า hardcode keys ใน source code" — ให้ใช้ env vars หรือ secret manager
- ตัวอย่างการส่งข้อมูลผ่าน HTTP: อธิบายว่า man-in-the-middle อ่านได้

---

## Slide 9: A03: Injection

- นี่คือ vulnerability ที่คนรู้จักดีที่สุด — ให้เน้น
- SQL Injection: พิมพ์ตัวอย่างลงบน whiteboard หรือให้ผู้เรียนลอง: `' OR 1=1 --`
- XSS: อธิบายผลกระทบ — steal cookies, redirect เว็บ, deface
- Command Injection: "รุนแรงมาก — ลบทั้ง server ได้ด้วยคำสั่งเดียว"
- เน้นว่า parameterized queries แก้ได้ทั้ง 3 ประเภทนี้

---

## Slide 10: A03: Injection (cont.)

- แสดงตัวอย่าง Python code ทั้ง bad และ good
- เน้นว่า `subprocess.run([...])` ใช้ list ไม่ใช่ string — ป้องกัน shell injection
- "ถ้าจะจำอย่างเดียว จำ parameterized queries"

---

## Slide 11: A04: Insecure Design

- เน้นว่านี่ต่างจากอันดับอื่น — แก้ด้วย code ไม่ได้ ต้องออกแบบใหม่
- ตัวอย่าง rate limiting: "ลองนึกว่าถ้าไม่จำกัด login attempt — brute force เล่นเอง"
- "ถ้าออกแบบไม่ดี ตั้งแต่แรก แก้ทีหลังยิ่งยาก"
- แนะนำ threat modeling เป็น practice

---

## Slide 12: A05: Security Misconfiguration

- DEBUG=True คือตัวอย่างที่เจอบ่อยมากใน production
- ให้เล่าเคสจริงที่เคยเจอ: "เคยเจอ stack trace ที่เปิดเผย DB credentials"
- Default credentials: ย้ำว่าต้องเปลี่ยนเสมอ
- "hardening checklist = checklist ที่ต้องทำก่อน deploy ทุกครั้ง"

---

## Slide 13: A06: Vulnerable & Outdated Components

- Log4Shell เป็นตัวอย่างที่ดีที่สุด — impact ทั่วโลก
- "ถ้าไม่ update dependencies ก็เหมือนมีประตูเปิดไว้ให้ attacker"
- แนะนำให้ใช้ Dependabot / Renovate อัตโนมัติ update
- ให้เห็นว่านี่คือเหตุผลที่เรามี Part B: SCA ใน lab

---

## Slide 14: A07: Authentication Failures

- ให้ยกมือถ้าใครในห้องเคยใช้ password '123456'
- MFA: อธิบายว่าแม้แค่ SMS ก็ดีกว่าไม่มี
- Session ID ใน URL: อธิบายว่า URL ถูก log ได้, share ได้, browser history เหลือบ
- Credential stuffing: อธิบายว่า bot ลอง password ที่หลุดจาก website อื่น

---

## Slide 15: A08: Software & Data Integrity Failures

- SolarWinds: "supply chain attack ที่ใหญ่ที่สุด — 18,000+ องค์กร"
- อธิบายว่าไม่ใช่แค่ install library — CI/CD pipeline เองก็โดนเข้าได้
- Insecure deserialization: อธิบายสั้นๆ ว่าเป็นอะไร (pickle exploit)
- "verify ทุกอย่างที่ download มา — checksums, signatures"

---

## Slide 16: A09: Logging & Monitoring Failures

- "ถ้าไม่ log ก็เหมือนถูกขโมยแล้วไม่รู้"
- ให้ตัวอย่าง: ถ้า brute force แต่ไม่ log → ไม่รู้จนกว่าโดน
- เน้น balance: log พอแต่ไม่ log sensitive data (GDPR, privacy)
- แนะนำ centralized logging: ELK, Grafana Loki

---

## Slide 17: A10: SSRF

- อธิบาย concept: "เว็บของเรา fetch URL ที่ user ส่งมา — ถ้าเขาส่ง internal IP ละ?"
- AWS metadata: `169.254.169.254` — ดึง credentials ได้เลย
- "นี่คือเหตุผลที่ต้อง allowlist URL ไม่ใช่ blocklist"
- ให้เห็นว่า SSRF ทำให้เข้าถึง internal network ทั้งหมด

---

## Slide 18: Session 2 Title
**Manual Code Review Techniques**

- "ตอนนี้เราจะลงมือหาช่องโหว่เอง ก่อนใช้ tools"
- อธิบายว่า manual review ยังจำเป็น — tools ไม่เห็น business logic flaws

---

## Slide 19: Security Code Review Checklist

- อ่าน checklist ทั้ง 7 categories ให้ฟัง
- เน้นว่านี่คือ "minimum" — ควรรู้มากกว่านี้
- "ถ้า review PR แล้วดูแค่ function logic ละ — ลืมมอง security แล้ว"

---

## Slide 20: Exercise 1: Manual Code Review

- **จัดกลุ่ม 2-3 คน**
- แจก code จาก `lab/vulnerable-app/app.py`
- "มี 12 ช่องโหว่ ซ่อนอยู่ — ลองหาให้มากที่สุด"
- ให้ 10 นาทีหา + 8 นาทีเฉลย
- **ถ้าหาครบทั้ง 12 = เก่งมาก**

---

## Slide 21: Break

- "พัก 10 นาที ก่อนเข้าสู่ส่วน tools"
- ตอนพัก: ให้ผู้เรียนเปิด laptop ตรวจสอบ tools พร้อม

---

## Slide 22: Session 3 Title
**Security Scanning Tools Overview**

- "ตอนนี้เราจะเรียนรู้ tools ที่จะใช้ใน lab"
- เน้นว่าจะสอนเฉพาะ tools ที่ใช้จริง — tools อื่นๆ อยู่ใน handout
- "เป้าหมายคือให้คุณรู้ว่ามี tools อะไรบ้าง และเลือกใช้ให้ถูก"

---

## Slide 23: 3 Categories of Security Tools

- SAST = static (ไม่ต้อง run code)
- SCA = dependencies (third-party libraries)
- Secret Scanning = credentials ที่หลุด
- "3 categories นี้ครอบคลุม security scanning ในระดับ code"
- บอกว่าเราจะใช้ Semgrep, Syft, Gitleaks ใน lab

---

## Slide 24: SAST: Semgrep

- "Semgrep คือ tool หลักที่เราจะใช้วันนี้"
- เน้นว่า pattern-based ไม่ใช่ regex — เข้าใจโครงสร้าง code
- รองรับ 30+ ภาษา — เหมาะกับทีมที่ใช้หลายภาษา
- แสดง command ให้เห็นว่าง่ายแค่ `semgrep scan --config auto .`

---

## Slide 25: SCA: Syft + Dependency-Track

- Syft: "สร้าง SBOM (Software Bill of Materials) — รายการอะไรอยู่ในเว็บ"
- อธิบาย SBOM แบบง่ายๆ: เหมือน.ingredients list ของอาหาร
- Dependency-Track: "ระบบที่เอา SBOM ไปเทียบกับ database ของ CVEs"
- DefectDojo: "รวมผลจาก tools ทั้งหมดไว้ที่เดียว"
- "SBOM คืออนาคตที่ government และ enterprise ให้ความสำคัญมาก"

---

## Slide 26: Secret Scanning: Gitleaks

- "Gitleaks คือ tool ที่ค้นหา secrets ที่ commit เข้า git โดยไม่ตั้งใจ"
- เน้นว่า scan Git history ทั้งหมด — ไม่ใช่แค่ working directory
- pre-commit hook: "ติดตั้งแล้วจะ block commit ที่มี secrets อัตโนมัติ"
- ให้เห็นว่านี่คือ safety net — ถ้า review พลาด Gitleaks จะจับได้

---

## Slide 27: Session 4 Title
**Hands-on Lab — Security Scanning**

- "นี่คือส่วนที่สำคัญที่สุดของวันนี้"
- ให้เปิด laptop เปิด terminal ไว้
- ย้ำ: "ทำตามผมทีละ step ถ้า stuck ให้ยกมือ"

---

## Slide 28: Lab Setup

- ให้ clone repo ถ้ายังไม่ได้ clone
- verify tools: `semgrep --version`, `syft --version`, `gitleaks version`
- "ถ้า tool ใดขาด ให้บอกเลย — ช่วยติดตั้ง"
- lab checklist อยู่ใน `docs/lab-checklist.md`

---

## Slide 29: Part A: SAST with Semgrep

- ให้รันคำสั่งตาม slide
- อธิบาย step 1-2: "รันแล้วดู output"
- Step 3 สำคัญ: เปรียบเทียบกับ manual review
  - "Tools พบอะไรที่คุณพลาด?"
  - "Manual review พบอะไรที่ tool พลาด?" (logic flaws, business logic)
- "คำตอบที่ 2 คือเหตุผลที่ manual review ยังจำเป็น"

---

## Slide 30: Part B: SCA with Syft + Dependency-Track

- ให้รัน `syft . -o cyclonedx-json > sbom.json`
- "เปิด sbom.json ดู — จะเห็น dependency ทั้งหมดพร้อม version"
- ถ้ามี Dependency-Track: อธิบายวิธี upload
- "ดูว่า library ไหน critical ที่สุด และต้อง update เป็น version อะไร"
- ถ้า Dependency-Track ไม่มี: ให้ใช้ `grype sbom.json` แทน (ใหม่ดีเท่า dependency-track แต่ง่ายกว่า)

---

## Slide 31: Part C: Secret Scanning with Gitleaks

- ให้รัน gitleaks detect
- "ดูว่าเจอ secret อะไรบ้าง — API key, password, token"
- แยก true positive vs false positive:
  - "ถ้าเจออะไรที่ดูเป็น key จริง = true positive"
  - "ถ้าเจอ string ที่บังเอิญตรงกับ pattern = false positive"
- อธิบายแนวทางแก้: env vars, rotate credentials, pre-commit hook

---

## Slide 32: Exercise 3: Fix & Validate

- "เลือก 3-5 critical/high vulnerabilities ที่พบ แล้วแก้ไข"
- ให้เปิด `app.py` แล้วแก้:
  - SQL → parameterized query
  - XSS → HTML escaping
  - Secrets → env vars
- "แก้เสร็จแล้วรัน scan อีกครั้ง — ถ้าหายคือแก้ถูกแล้ว"
- Solutions อยู่ที่ `lab/solutions/app_fixed.py`

---

## Slide 33: Part D: Docker Security Review

- "ตอนนี้เรามอง security ในอีกมุม — infrastructure as code"
- "เช่นเดียวกับ code, Dockerfile และ docker-compose.yml ก็มีช่องโหว่ได้"
- ให้เปิด `lab/vulnerable-app/Dockerfile` อ่าน
- "มี 14 ช่องโหว่ — ทั้ง Dockerfile และ docker-compose.yml"

---

## Slide 34: Dockerfile Vulnerabilities

- อ่านตารางทีละแถว อธิบายสั้นๆ
- เน้น "root container" และ "unpinned image" เป็น critical
- "ให้คิดว่าถ้า attacker exploit ได้ใน container — ถ้าเป็น root = game over"
- "latest tag ไม่ reproducible — วันนี้ build กับพรุ่งนี้อาจต่างกัน"

---

## Slide 35: docker-compose.yml Vulnerabilities

- เน้น "secrets in plaintext env vars" เป็น critical
- "เห็น `DB_PASSWORD=supersecret123` ใน code — ใครก็เห็นได้"
- "Redis ไม่มี password = ใคร connect ได้ทุกคน"
- "DB port 5432 เปิดไว้ — คนภายน่าจะเข้า DB ไม่ได้"
- "Network segmentation = frontend ไม่เห็น backend, backend ไม่เห็น DB"

---

## Slide 36: Secure Dockerfile — Key Fixes

- อธิบายแต่ละ fix:
  - Multi-stage: "แยก build กับ runtime — final image เล็กลง, attack surface ลดลง"
  - Non-root: "เป็น principle พื้นฐาน — container ไม่ควรเป็น root เลย"
  - Healthcheck: "Docker รู้ว่า app ตายหรือยัง แล้ว restart ให้"
  - Exec form: "PID 1 คือ app เอง — signal ทำงานถูกต้อง"
- ให้ดู fixed version ที่ `lab/solutions/Dockerfile`

---

## Slide 37: Secure docker-compose.yml — Key Fixes

- Secrets: "ใช้ Docker secrets แทน env vars — ไม่เห็นใน code และ inspect"
- Port binding: "127.0.0.1 = เข้าได้แค่จากเครื่องตัวเอง ไม่ใช่ทั้ง internet"
- Resource limits: "memory 256M — ถ้า DDoS ก็กินแค่ 256M ไม่ใช่ทั้ง server"
- Network segmentation: "internal: true = container ใน network นี้ไม่ออก internet ได้"
- `no-new-privileges`: "ป้องกัน container ยกระดับ privilege"

---

## Slide 38: Session 5 Title
**CI/CD Integration & Best Practices**

- "ตอนนี้เรารู้จัก tools แล้ว — ถ้าใส่ pipeline จะเป็นยังไง?"
- "เป้าหมายคือ security เป็นส่วนหนึ่งของ development workflow ไม่ใช่ขั้นตอนแยก"

---

## Slide 39: Security in CI/CD Pipeline

- อธิบาย flow: pre-commit → PR → build → post-build → weekly
- "ทุก stage มี security check"
- เน้นว่า PR check เป็น gate สำคัญ: "ถ้า Semgrep เจอ critical → block merge"
- Weekly scan: "ตรวจสอบเต็มรูปแบบทุกสัปดาห์"

---

## Slide 40: GitHub Actions Example

- อ่าน YAML ทีละ job อธิบาย
- Semgrep action: "เพิ่มใน repo แล้วมัน scanทุก PR อัตโนมัติ"
- Gitleaks action: "block secrets ก่อนเข้า code"
- "GitHub Actions config ที่เห็นนี่ใช้ได้เลย — copy ไปใส่ repo ได้"
- GitLab CI / Jenkins versions อยู่ใน handout

---

## Slide 41: Best Practices

- อ่านทีละข้ออธิบายสั้นๆ
- เน้น 3 ข้อแรก:
  1. **Scan Early** — "ยิ่งเร็วยิ่งถูก ยิ่งถูกที่สุด"
  2. **Automate** — "ถ้าต้องจำทุกครั้ง มันจะไม่เกิดขึ้น"
  3. **Fix Critical First** — "อย่าไปแก้ low ก่อนเพราะมันง่าย — critical มีผลกระทบสูงสุด"
- "Security Champions = developer ในทีมที่เป็น security expert คนแรกที่ถาม"

---

## Slide 42: Wrap-up

- สรุปสั้นๆ: เราได้เรียนอะไรบ้างวันนี้
- "ตอนนี้คุณมีทั้ง knowledge และ tools แล้ว ที่จะเริ่ม scan project ของคุณเอง"
- ให้ดู Tools Summary table

---

## Slide 43: Q&A

- เปิดรับคำถาม
- ถ้าไม่มีคำถาม: แนะนำ resources
  - OWASP Top 10 อ่านเพิ่มได้ที่ owasp.org
  - Semgrep playground: semgrep.dev/playground — ลอง online ได้เลย
- บอกว่า materials อยู่ที่ GitHub repo

---

## Slide 44: Thank You

- ขอบคุณทุกคน
- "Happy Secure Coding!"
- "อย่าลืม — scan early, scan often"
- ให้ feedback ได้

---

## Tips สำหรับ Presenter

### จัดการเวลา
- Session 1 (45 min): ถ้าเวลาน้อย ข้าม A06-A08 ให้ผู้เรียนอ่านเอง
- Session 4 (50 min): นี่สำคัญที่สุด อย่าข้าม ให้เวลาเต็ม
- Docker (Part D): ถ้าเวลาไม่พอ ทำเป็น demo แทน hands-on

### จัดการปัญหา
- "ถ้า tool install ไม่ผ่าน — ถามผมเลย อย่านั่งนาน"
- ถ้า Syft/Dependency-Track ไม่มี → ใช้ `grype sbom.json` แทน
- ถ้า Docker ไม่มี → อ่าน Dockerfile/compose เป็น code review แทน

### Engagement
- ถาม question ระหว่าง presentation: "ที่ทำงานใช้ tool อะไรกันบ้าง?"
- ให้ผู้เรียน share experience ของตัวเอง
- ยกมือถามสถานะการณ์: "ใครเคยเจอ breach ใน org ของคุณมั้ย?"
