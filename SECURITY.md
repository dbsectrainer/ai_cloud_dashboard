# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@your-domain.com**

### What to Include

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next release cycle

## Security Best Practices

### For Production Deployments

1. **Environment Variables**
   - Never commit `.env` files
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)
   - Rotate credentials regularly

2. **Docker Security**
   - Always run containers as non-root user
   - Scan images with Trivy before deployment
   - Keep base images updated
   - Use multi-stage builds to minimize attack surface

3. **Network Security**
   - Enable TLS/SSL for all external connections
   - Use private networks for inter-service communication
   - Configure firewall rules restrictively
   - Implement rate limiting

4. **Database Security**
   - Use strong passwords (32+ characters)
   - Enable SSL/TLS for database connections
   - Restrict database access to application network only
   - Regularly backup and test restore procedures

5. **Monitoring & Logging**
   - Enable audit logging
   - Monitor for suspicious activity
   - Set up alerts for security events
   - Retain logs for compliance requirements (90+ days)

### Known Limitations

- **Beta Status**: This is beta software. Not recommended for production use with sensitive data until v1.0
- **Authentication**: Basic auth only. OAuth2/SAML not yet implemented
- **Encryption**: Database encryption at rest requires manual PostgreSQL configuration
- **API Security**: No API authentication for data ingestion endpoints (use network isolation)

## Security Features

### Current

- ✅ Docker multi-stage builds with non-root user
- ✅ Dependency vulnerability scanning (pip-audit)
- ✅ Container vulnerability scanning (Trivy)
- ✅ SBOM generation (CycloneDX)
- ✅ Pre-commit hooks with secret detection
- ✅ Parameterized queries (SQL injection protection)
- ✅ Environment-based configuration

### Planned (v0.3+)

- 🔲 OAuth2/OIDC authentication
- 🔲 Role-based access control (RBAC)
- 🔲 API key authentication
- 🔲 End-to-end encryption for sensitive data
- 🔲 SOC2 Type II compliance certification
- 🔲 Automated security scanning in CI/CD
- 🔲 Penetration testing reports

## Compliance

See [docs/compliance_map.md](docs/compliance_map.md) for detailed compliance mappings.

## Security Contacts

- Security Team: security@your-domain.com
- General Issues: https://github.com/dbsectrainer/ai_cloud_dashboard/issues
