# Security Scanning Tools — Comparison Matrix

## SAST (Static Application Security Testing)

| Tool | Languages | License | CI/CD Integration | Custom Rules | Notes |
|------|-----------|---------|-------------------|-------------|-------|
| **Semgrep** | 30+ | OSS (LGPL) | GitHub Actions, GitLab CI | Yes (pattern-based) | Recommended for workshop |
| SonarQube | 30+ | Community/Commercial | All major CI | Yes (complex) | Self-hosted, heavy |
| Bandit | Python only | OSS (Apache) | Any | Limited | Python-specific |
| ESLint Security | JS/TS only | OSS (MIT) | Any | Yes (plugins) | JS/TS-specific |
| Brakeman | Ruby/Rails | OSS (MIT) | Any | Limited | Rails-specific |

## SCA (Software Composition Analysis)

| Tool | SBOM Formats | Ecosystems | License | Vuln DB | Notes |
|------|-------------|------------|---------|---------|-------|
| **Syft** | CycloneDX, SPDX | npm, pip, Maven, Go, etc. | OSS (Apache) | - (generator only) | SBOM generator, pairs with Grype/DTrack |
| **Dependency-Track** | CycloneDX, SPDX | All (via SBOM) | OSS (Apache) | NVD, OSV, GitHub | Vuln management platform |
| **DefectDojo** | 150+ importers | All | OSS (BSD) | Aggregator | Findings aggregator |
| Snyk | - | npm, pip, Maven, Go | Commercial | Snyk DB | SaaS, developer-friendly |
| OWASP Dep-Check | - | Java, .NET, npm, etc. | OSS (Apache) | NVD | Standalone scanner |
| Trivy | CycloneDX, SPDX | npm, pip, Maven, Go, containers | OSS (Apache) | Trivy DB | Also scans containers/IaC |

## Secret Scanning

| Tool | Git History | Pre-commit | Custom Rules | License | Notes |
|------|------------|------------|-------------|---------|-------|
| **Gitleaks** | Yes | Yes | .gitleaks.toml | OSS (MIT) | Fast, written in Go |
| TruffleHog | Yes | Yes | Regex/entropy | OSS (AGPL) | High entropy detection |
| detect-secrets | Yes | Yes | Plugin-based | OSS (Apache) | By Yelp |
| GitGuardian | Yes | Yes | Built-in | Commercial | SaaS, dashboard |

## Container Security

| Tool | Scan Type | License | Notes |
|------|-----------|---------|-------|
| **Trivy** | Image, IaC, Secrets, Licenses | OSS (Apache) | Comprehensive, recommended for workshop |
| Docker Bench | Docker host security | OSS (Apache) | CIS Docker Benchmark |
| Hadolint | Dockerfile lint | OSS (GPL) | Best practices linting |
| Docker Scout | Image, SBOM | OSS (Apache) | Built-in Docker CLI |
| Dockle | Image analysis | OSS (Apache) | Policy check, efficiency |

## Recommended Combinations

### Minimal (Free, Quick Start)
- SAST: Semgrep
- SCA: Syft + Grype
- Secrets: Gitleaks

### Standard (Team)
- SAST: Semgrep
- SCA: Syft + Dependency-Track
- Secrets: Gitleaks
- Aggregator: DefectDojo
- CI/CD: GitHub Actions

### Enterprise
- SAST: SonarQube + Semgrep
- SCA: Snyk or Dependency-Track
- Secrets: GitGuardian
- Aggregator: DefectDojo
- Monitoring: Continuous with alerts
