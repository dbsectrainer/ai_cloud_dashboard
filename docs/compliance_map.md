# Compliance Mapping

This document maps Cloud Dashboard features to compliance standards.

## Legend

- ✅ **Automated**: Checked automatically by the dashboard
- ℹ️ **Informational**: Dashboard provides visibility/reports
- 📋 **Manual**: Requires manual configuration/validation
- ❌ **Not Implemented**: Planned for future release

---

## SOC 2 Type II

### CC6 - Logical and Physical Access Controls

| Control | Requirement | Dashboard Capability | Status |
|---------|-------------|---------------------|--------|
| CC6.1 | Restrict logical access | RBAC for dashboard access | 📋 Manual |
| CC6.2 | Authentication mechanisms | MFA enforcement check | ✅ Automated |
| CC6.3 | Authorization | Role-based views (Exec/Manager/Analyst) | ℹ️ Informational |
| CC6.6 | Encryption at rest | Encryption at rest compliance check | ✅ Automated |
| CC6.7 | Encryption in transit | TLS 1.2+ validation | ✅ Automated |

### CC7 - System Operations

| Control | Requirement | Dashboard Capability | Status |
|---------|-------------|---------------------|--------|
| CC7.2 | Monitor system components | Prometheus/Grafana metrics | ✅ Automated |
| CC7.3 | Audit logging | Audit log retention check | ✅ Automated |
| CC7.4 | Incident response | Alert on compliance violations | ℹ️ Informational |

---

## HIPAA (Health Insurance Portability and Accountability Act)

### Security Rule

| Standard | Requirement | Dashboard Capability | Status |
|----------|-------------|---------------------|--------|
| §164.308(a)(1) | Risk analysis | Compliance score & reports | ℹ️ Informational |
| §164.308(a)(3) | Workforce security | Access control checks | ✅ Automated |
| §164.308(a)(5) | Security awareness | Compliance training tracking | ❌ Not Implemented |
| §164.312(a)(1) | Access control | RBAC validation | 📋 Manual |
| §164.312(a)(2)(iv) | Encryption | PHI encryption validation | ✅ Automated |
| §164.312(b) | Audit controls | Audit logging check | ✅ Automated |
| §164.312(c) | Integrity controls | Data integrity monitoring | ❌ Not Implemented |
| §164.312(d) | Transmission security | TLS enforcement check | ✅ Automated |
| §164.312(e) | Encryption at rest | Storage encryption check | ✅ Automated |

---

## ISO 27001:2022

### Annex A Controls

| Control | Requirement | Dashboard Capability | Status |
|---------|-------------|---------------------|--------|
| A.5.1 | Information security policies | Policy doc generation | ℹ️ Informational |
| A.5.10 | Acceptable use of information | Usage metrics tracking | ℹ️ Informational |
| A.5.15 | Access control | Access control validation | ✅ Automated |
| A.5.18 | Access rights | Privileged account MFA check | ✅ Automated |
| A.8.9 | Configuration management | Config drift detection | ❌ Not Implemented |
| A.8.10 | Information deletion | Data retention compliance | ℹ️ Informational |
| A.8.16 | Monitoring | System monitoring (Grafana) | ✅ Automated |
| A.8.24 | Cryptography | Encryption enforcement checks | ✅ Automated |
| A.8.26 | Application security | SAST/DAST in CI/CD | ℹ️ Informational |

---

## GDPR (General Data Protection Regulation)

| Article | Requirement | Dashboard Capability | Status |
|---------|-------------|---------------------|--------|
| Art. 5 | Data minimization | Data inventory & classification | ❌ Not Implemented |
| Art. 25 | Data protection by design | Compliance-by-default configs | 📋 Manual |
| Art. 30 | Record of processing | Processing activity logs | ℹ️ Informational |
| Art. 32 | Security of processing | Encryption & access controls | ✅ Automated |
| Art. 33 | Breach notification | Incident alerting | ℹ️ Informational |
| Art. 35 | Data protection impact assessment | DPIA template generation | ❌ Not Implemented |

---

## PCI-DSS v4.0

| Requirement | Description | Dashboard Capability | Status |
|-------------|-------------|---------------------|--------|
| 1.2 | Firewall configuration | Network config review | ℹ️ Informational |
| 2.2 | Vendor defaults | Default credential check | ❌ Not Implemented |
| 3.5 | Encryption of cardholder data | Encryption validation | ✅ Automated |
| 8.3 | Multi-factor authentication | MFA enforcement check | ✅ Automated |
| 10.2 | Audit logs | Log retention & integrity | ✅ Automated |
| 11.3 | Penetration testing | Test schedule tracking | ℹ️ Informational |

---

## Automated Compliance Checks

The dashboard automatically validates the following:

### ✅ Implemented Checks

1. **Encryption at Rest** (SOC2-EAR-001)
   - Validates storage encryption is enabled
   - Severity: High

2. **Encryption in Transit** (SOC2-EIT-001)
   - Validates TLS 1.2+ for network communication
   - Severity: High

3. **MFA Enforcement** (SOC2-IAM-001)
   - Validates MFA on privileged accounts
   - Severity: Critical

4. **Audit Logging** (SOC2-LOG-001)
   - Validates audit logs enabled with 90+ day retention
   - Severity: High

5. **PHI Encryption** (HIPAA-ENC-001)
   - Validates protected health information encryption
   - Severity: Critical

6. **Access Controls** (HIPAA-ACC-001)
   - Validates role-based access for PHI
   - Severity: High

7. **Data Residency** (GDPR-DAT-001)
   - Validates data stored in compliant regions
   - Severity: Critical

### 🔲 Planned Checks (v0.3)

- Asset inventory validation (ISO27001-AST-001)
- Vulnerability scanning compliance (ISO27001-VUL-001)
- Default credential detection (PCI-DSS 2.2)
- Network segmentation validation (PCI-DSS 1.2)
- Data retention compliance (GDPR Art. 5)

---

## Compliance Scoring

The dashboard calculates a compliance score (0-100%):

- **Pass**: 100 points
- **Warning**: 50 points
- **Fail**: 0 points
- **Unknown**: 0 points

**Score = (Total Points / Maximum Possible Points) × 100**

### Interpretation

- **90-100%**: Excellent - Likely compliant
- **75-89%**: Good - Minor issues to address
- **60-74%**: Fair - Several gaps exist
- **< 60%**: Poor - Significant compliance work needed

---

## Remediation Workflows

For each failed check, the dashboard provides:

1. **Check Details**: What was tested
2. **Status**: Pass/Fail/Warning/Unknown
3. **Severity**: Critical/High/Medium/Low
4. **Remediation Steps**: How to fix the issue
5. **Priority**: Ordered by severity

---

## Limitations

⚠️ **Important Notes**:

1. Automated checks provide **indicators**, not **guarantees** of compliance
2. Manual audits and documentation are still required
3. Legal review is necessary for formal compliance certification
4. Dashboard is a tool to **assist** compliance, not replace it
5. Consult with compliance professionals for your specific requirements

---

## Compliance Roadmap

| Quarter | Target |
|---------|--------|
| Q2 2025 | SOC2 Type I audit readiness |
| Q3 2025 | HIPAA compliance validation |
| Q4 2025 | ISO 27001 certification prep |
| Q1 2026 | SOC2 Type II certification |

---

For questions about compliance features, see [docs/runbook.md](runbook.md) or contact: compliance@your-domain.com
