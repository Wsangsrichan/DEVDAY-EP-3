# DEVDAY EP.3 — Security Code Review & Scanning Tools

> Hands-on Workshop | 3 Hours | Find and fix security vulnerabilities through manual code review and automated scanning tools

## Workshop Overview

เรียนรู้การตรวจสอบความปลอดภัยของ source code ด้วย manual code review และการใช้เครื่องมือ security scanning tools เพื่อค้นหาช่องโหว่และความเสี่ยงด้านความปลอดภัย ก่อนนำ code ไป deploy จริง

## Learning Objectives

- เข้าใจหลักการ secure coding และช่องโหว่ที่พบบ่อย (OWASP Top 10)
- ทำ manual code review เพื่อหาจุดอ่อนด้านความปลอดภัย
- ใช้ security scanning tools วิเคราะห์ code อัตโนมัติ
- ตีความและแก้ไขผลลัพธ์จาก security tools
- บูรณาการ security scanning เข้ากับ CI/CD pipeline

## Timeline (3 Hours)

| Time | Session |
|------|---------|
| 09:00 - 09:45 | Session 1: Security Fundamentals & OWASP Top 10 (45 min) |
| 09:45 - 10:15 | Session 2: Manual Code Review Techniques + Exercise (30 min) |
| 10:15 - 10:25 | Break (10 min) |
| 10:25 - 10:45 | Session 3: Security Scanning Tools Overview (20 min) |
| 10:45 - 11:35 | Session 4: Hands-on Lab — Security Scanning (50 min) |
| 11:35 - 11:55 | Session 5: CI/CD Integration & Best Practices (20 min) |
| 11:55 - 12:00 | Q&A & Wrap-up (5 min) |

## Tools Used

| Category | Tool (Lab) | Others |
|----------|-----------|--------|
| SAST | **Semgrep** | SonarQube, Bandit, ESLint Security |
| SCA / SBOM | **Syft**, **Dependency-Track**, **DefectDojo** | Snyk, Trivy |
| Secret Scanning | **Gitleaks** | TruffleHog, detect-secrets |
| CI/CD | **GitHub Actions** | GitLab CI, Jenkins |

## Prerequisites

- ประสบการณ์พัฒนา software อย่างน้อย 1 ปี
- เข้าใจพื้นฐาน web application security
- รู้จักใช้ Git พื้นฐาน
- Laptop + internet connection
- ติดตั้ง: Git, IDE/Text editor, Docker (optional)

## Repo Structure

```
DEVDAY-EP-3/
├── slides/                  # Reveal.js presentation
│   └── index.html           # Open in browser to present
├── lab/
│   ├── vulnerable-app/      # Intentionally vulnerable code for exercises
│   ├── solutions/           # Fixed versions of vulnerable code
│   └── configs/             # CI/CD configs, tool configs
├── docs/
│   ├── owasp-top10-cheatsheet.md
│   ├── tool-comparison.md
│   └── lab-checklist.md
└── README.md
```

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
npm install   # or pip install -r requirements.txt
```

## Target Audience

- Developers ที่ต้องการเพิ่มความรู้ด้าน security
- QA/Test engineers
- DevOps/DevSecOps engineers
- Security champions ในทีม
- Tech leads / Team leads
