"""Compliance checking service for cloud providers and configurations."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ComplianceStandard(Enum):
    """Compliance standards."""

    SOC2 = "SOC2"
    HIPAA = "HIPAA"
    ISO27001 = "ISO27001"
    GDPR = "GDPR"
    PCI_DSS = "PCI-DSS"


class ComplianceStatus(Enum):
    """Compliance check status."""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    UNKNOWN = "unknown"


@dataclass
class ComplianceCheck:
    """Individual compliance check result."""

    check_id: str
    check_name: str
    standard: ComplianceStandard
    status: ComplianceStatus
    details: str
    remediation: str = ""
    severity: str = "medium"  # low, medium, high, critical


@dataclass
class ComplianceReport:
    """Full compliance report."""

    provider: str
    total_checks: int
    passed: int
    failed: int
    warnings: int
    unknown: int
    checks: list[ComplianceCheck]
    compliance_score: float


class ComplianceChecker:
    """
    Check cloud configurations for compliance with various standards.

    This provides automated compliance checks that can be run continuously.
    """

    def __init__(self):
        """Initialize compliance checker with check definitions."""
        self._checks = self._define_checks()

    def _define_checks(self) -> list[dict[str, Any]]:
        """
        Define compliance checks.

        In production, these would be loaded from a database or config file.
        """
        return [
            {
                "id": "SOC2-EAR-001",
                "name": "Encryption at Rest",
                "standard": ComplianceStandard.SOC2,
                "description": "Verify encryption at rest is enabled for all storage",
                "severity": "high",
            },
            {
                "id": "SOC2-EIT-001",
                "name": "Encryption in Transit",
                "standard": ComplianceStandard.SOC2,
                "description": "Verify TLS 1.2+ for all network communications",
                "severity": "high",
            },
            {
                "id": "SOC2-IAM-001",
                "name": "MFA Enforcement",
                "standard": ComplianceStandard.SOC2,
                "description": "Multi-factor authentication required for privileged accounts",
                "severity": "critical",
            },
            {
                "id": "SOC2-LOG-001",
                "name": "Audit Logging",
                "standard": ComplianceStandard.SOC2,
                "description": "Audit logs enabled and retained for 90+ days",
                "severity": "high",
            },
            {
                "id": "HIPAA-ENC-001",
                "name": "PHI Encryption",
                "standard": ComplianceStandard.HIPAA,
                "description": "Protected Health Information encrypted at rest and in transit",
                "severity": "critical",
            },
            {
                "id": "HIPAA-ACC-001",
                "name": "Access Controls",
                "standard": ComplianceStandard.HIPAA,
                "description": "Role-based access controls for PHI access",
                "severity": "high",
            },
            {
                "id": "ISO27001-AST-001",
                "name": "Asset Inventory",
                "standard": ComplianceStandard.ISO27001,
                "description": "Maintain inventory of all information assets",
                "severity": "medium",
            },
            {
                "id": "ISO27001-VUL-001",
                "name": "Vulnerability Management",
                "standard": ComplianceStandard.ISO27001,
                "description": "Regular vulnerability scanning and patching",
                "severity": "high",
            },
            {
                "id": "GDPR-DAT-001",
                "name": "Data Residency",
                "standard": ComplianceStandard.GDPR,
                "description": "Personal data stored in compliant regions",
                "severity": "critical",
            },
            {
                "id": "GDPR-PRT-001",
                "name": "Data Protection",
                "standard": ComplianceStandard.GDPR,
                "description": "Appropriate technical and organizational measures",
                "severity": "high",
            },
        ]

    def check_encryption_at_rest(self, config: dict[str, Any]) -> ComplianceCheck:
        """Check if encryption at rest is enabled."""
        encryption_enabled = config.get("encryption_at_rest", False)

        status = ComplianceStatus.PASS if encryption_enabled else ComplianceStatus.FAIL

        return ComplianceCheck(
            check_id="SOC2-EAR-001",
            check_name="Encryption at Rest",
            standard=ComplianceStandard.SOC2,
            status=status,
            details=f"Encryption at rest: {'enabled' if encryption_enabled else 'disabled'}",
            remediation="Enable encryption at rest for all storage volumes and databases",
            severity="high",
        )

    def check_mfa_enforcement(self, config: dict[str, Any]) -> ComplianceCheck:
        """Check if MFA is enforced for privileged accounts."""
        privileged_accounts = config.get("privileged_accounts", [])

        # Check if all privileged accounts have MFA
        accounts_with_mfa = [acc for acc in privileged_accounts if acc.get("mfa_enabled")]

        if not privileged_accounts:
            status = ComplianceStatus.UNKNOWN
            details = "No privileged accounts found"
        elif len(accounts_with_mfa) == len(privileged_accounts):
            status = ComplianceStatus.PASS
            details = f"MFA enabled for all {len(privileged_accounts)} privileged accounts"
        else:
            status = ComplianceStatus.FAIL
            details = (
                f"MFA enabled for {len(accounts_with_mfa)}/{len(privileged_accounts)} "
                "privileged accounts"
            )

        return ComplianceCheck(
            check_id="SOC2-IAM-001",
            check_name="MFA Enforcement",
            standard=ComplianceStandard.SOC2,
            status=status,
            details=details,
            remediation="Enable MFA for all privileged and administrative accounts",
            severity="critical",
        )

    def check_audit_logging(self, config: dict[str, Any]) -> ComplianceCheck:
        """Check if audit logging is enabled and retained appropriately."""
        logging_enabled = config.get("audit_logging_enabled", False)
        retention_days = config.get("log_retention_days", 0)

        if not logging_enabled:
            status = ComplianceStatus.FAIL
            details = "Audit logging is disabled"
        elif retention_days < 90:
            status = ComplianceStatus.WARNING
            details = f"Audit logs retained for {retention_days} days (minimum 90 recommended)"
        else:
            status = ComplianceStatus.PASS
            details = f"Audit logging enabled with {retention_days} day retention"

        return ComplianceCheck(
            check_id="SOC2-LOG-001",
            check_name="Audit Logging",
            standard=ComplianceStandard.SOC2,
            status=status,
            details=details,
            remediation="Enable audit logging and set retention to at least 90 days",
            severity="high",
        )

    def run_checks(
        self, provider: str, config: dict[str, Any], standards: list[ComplianceStandard] = None
    ) -> ComplianceReport:
        """
        Run compliance checks for a provider configuration.

        Args:
            provider: Cloud provider name
            config: Configuration dictionary
            standards: List of standards to check (None = all)

        Returns:
            Compliance report with results
        """
        # Run automated checks
        check_results = [
            self.check_encryption_at_rest(config),
            self.check_mfa_enforcement(config),
            self.check_audit_logging(config),
        ]

        # Filter by requested standards
        if standards:
            check_results = [c for c in check_results if c.standard in standards]

        # Calculate statistics
        total = len(check_results)
        passed = sum(1 for c in check_results if c.status == ComplianceStatus.PASS)
        failed = sum(1 for c in check_results if c.status == ComplianceStatus.FAIL)
        warnings = sum(1 for c in check_results if c.status == ComplianceStatus.WARNING)
        unknown = sum(1 for c in check_results if c.status == ComplianceStatus.UNKNOWN)

        # Calculate compliance score (0-100)
        # Pass = 100%, Warning = 50%, Fail/Unknown = 0%
        score_sum = (passed * 100) + (warnings * 50)
        compliance_score = (score_sum / (total * 100)) * 100 if total > 0 else 0.0

        return ComplianceReport(
            provider=provider,
            total_checks=total,
            passed=passed,
            failed=failed,
            warnings=warnings,
            unknown=unknown,
            checks=check_results,
            compliance_score=round(compliance_score, 2),
        )

    def get_remediation_plan(self, report: ComplianceReport) -> list[dict[str, Any]]:
        """
        Generate remediation plan for failed/warning checks.

        Args:
            report: Compliance report

        Returns:
            Prioritized list of remediation actions
        """
        failed_checks = [
            c
            for c in report.checks
            if c.status in (ComplianceStatus.FAIL, ComplianceStatus.WARNING)
        ]

        # Sort by severity (critical > high > medium > low)
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        failed_checks.sort(key=lambda c: severity_order.get(c.severity, 99))

        return [
            {
                "priority": idx + 1,
                "check_id": check.check_id,
                "check_name": check.check_name,
                "severity": check.severity,
                "status": check.status.value,
                "remediation": check.remediation,
            }
            for idx, check in enumerate(failed_checks)
        ]
