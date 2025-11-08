"""Tests for compliance checking service."""

import pytest

from src.services.compliance_service import (
    ComplianceChecker,
    ComplianceStandard,
    ComplianceStatus,
)


class TestComplianceChecker:
    """Test cases for compliance checker."""

    @pytest.fixture
    def checker(self):
        """Create checker instance."""
        return ComplianceChecker()

    def test_encryption_at_rest_pass(self, checker):
        """Test encryption at rest check - passing case."""
        config = {"encryption_at_rest": True}

        result = checker.check_encryption_at_rest(config)

        assert result.status == ComplianceStatus.PASS
        assert result.standard == ComplianceStandard.SOC2
        assert "enabled" in result.details.lower()

    def test_encryption_at_rest_fail(self, checker):
        """Test encryption at rest check - failing case."""
        config = {"encryption_at_rest": False}

        result = checker.check_encryption_at_rest(config)

        assert result.status == ComplianceStatus.FAIL
        assert "disabled" in result.details.lower()
        assert len(result.remediation) > 0

    def test_mfa_enforcement_all_enabled(self, checker):
        """Test MFA enforcement - all accounts have MFA."""
        config = {
            "mfa_enforced": True,
            "privileged_accounts": [
                {"username": "admin1", "mfa_enabled": True},
                {"username": "admin2", "mfa_enabled": True},
            ],
        }

        result = checker.check_mfa_enforcement(config)

        assert result.status == ComplianceStatus.PASS
        assert "all" in result.details.lower()

    def test_mfa_enforcement_partial(self, checker):
        """Test MFA enforcement - some accounts missing MFA."""
        config = {
            "mfa_enforced": False,
            "privileged_accounts": [
                {"username": "admin1", "mfa_enabled": True},
                {"username": "admin2", "mfa_enabled": False},
                {"username": "admin3", "mfa_enabled": False},
            ],
        }

        result = checker.check_mfa_enforcement(config)

        assert result.status == ComplianceStatus.FAIL
        assert "1/3" in result.details

    def test_mfa_enforcement_no_accounts(self, checker):
        """Test MFA enforcement - no privileged accounts found."""
        config = {"mfa_enforced": False, "privileged_accounts": []}

        result = checker.check_mfa_enforcement(config)

        assert result.status == ComplianceStatus.UNKNOWN
        assert "no privileged accounts" in result.details.lower()

    def test_audit_logging_pass(self, checker):
        """Test audit logging - passing case."""
        config = {"audit_logging_enabled": True, "log_retention_days": 365}

        result = checker.check_audit_logging(config)

        assert result.status == ComplianceStatus.PASS
        assert "365" in result.details

    def test_audit_logging_warning(self, checker):
        """Test audit logging - retention too short."""
        config = {"audit_logging_enabled": True, "log_retention_days": 30}

        result = checker.check_audit_logging(config)

        assert result.status == ComplianceStatus.WARNING
        assert "30 days" in result.details
        assert "90" in result.details

    def test_audit_logging_fail(self, checker):
        """Test audit logging - disabled."""
        config = {"audit_logging_enabled": False, "log_retention_days": 0}

        result = checker.check_audit_logging(config)

        assert result.status == ComplianceStatus.FAIL
        assert "disabled" in result.details.lower()

    def test_run_checks_all_pass(self, checker):
        """Test running all checks - all passing."""
        config = {
            "encryption_at_rest": True,
            "mfa_enforced": True,
            "privileged_accounts": [{"username": "admin", "mfa_enabled": True}],
            "audit_logging_enabled": True,
            "log_retention_days": 365,
        }

        report = checker.run_checks("AWS", config)

        assert report.provider == "AWS"
        assert report.total_checks > 0
        assert report.passed == report.total_checks
        assert report.failed == 0
        assert report.compliance_score == 100.0

    def test_run_checks_with_failures(self, checker):
        """Test running all checks - some failures."""
        config = {
            "encryption_at_rest": False,  # Fail
            "mfa_enforced": False,
            "privileged_accounts": [],  # Unknown
            "audit_logging_enabled": True,
            "log_retention_days": 30,  # Warning
        }

        report = checker.run_checks("Azure", config)

        assert report.provider == "Azure"
        assert report.failed > 0
        assert report.compliance_score < 100.0

    def test_run_checks_filter_standards(self, checker):
        """Test running checks filtered by standard."""
        config = {
            "encryption_at_rest": True,
            "mfa_enforced": True,
            "privileged_accounts": [{"username": "admin", "mfa_enabled": True}],
            "audit_logging_enabled": True,
            "log_retention_days": 365,
        }

        report = checker.run_checks(
            "GCP", config, standards=[ComplianceStandard.SOC2]
        )

        # All checks in this test are SOC2
        assert all(c.standard == ComplianceStandard.SOC2 for c in report.checks)

    def test_remediation_plan_prioritization(self, checker):
        """Test remediation plan is prioritized by severity."""
        config = {
            "encryption_at_rest": False,  # High severity
            "mfa_enforced": False,
            "privileged_accounts": [
                {"username": "admin", "mfa_enabled": False}
            ],  # Critical
            "audit_logging_enabled": True,
            "log_retention_days": 30,  # Warning
        }

        report = checker.run_checks("Test", config)
        plan = checker.get_remediation_plan(report)

        assert len(plan) > 0

        # First item should be highest priority (critical severity)
        # MFA has critical severity
        assert plan[0]["severity"] == "critical"

        # All items should have remediation steps
        assert all(len(item["remediation"]) > 0 for item in plan)

    def test_compliance_score_calculation(self, checker):
        """Test compliance score calculation logic."""
        # Mix of pass, warning, fail
        config = {
            "encryption_at_rest": True,  # Pass = 100%
            "mfa_enforced": False,
            "privileged_accounts": [
                {"username": "admin", "mfa_enabled": False}
            ],  # Fail = 0%
            "audit_logging_enabled": True,
            "log_retention_days": 30,  # Warning = 50%
        }

        report = checker.run_checks("Test", config)

        # 1 pass (100) + 1 warning (50) + 1 fail (0) = 150 / 300 = 50%
        assert report.compliance_score == 50.0
