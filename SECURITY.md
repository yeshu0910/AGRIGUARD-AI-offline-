# Security Policy

## Supported Versions

The following versions of AgriGuard AI are currently supported with security updates:

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |
| 0.1.x   | :x:                |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly:

### How to Report

- **Do not** open a public issue on GitLab for security vulnerabilities.
- Send a detailed report to **security@example.com** with the following information:
  - **Subject**: "[AgriGuard AI Security] Brief description"
  - **Description**: A clear and concise description of the vulnerability.
  - **Steps to Reproduce**: Detailed steps to reproduce the issue.
  - **Impact**: What an attacker could achieve by exploiting this vulnerability.
  - **Suggested Fix**: If you have a recommendation for how to address the issue, please include it.
  - **Attachments**: Screenshots, logs, or proof-of-concept code if applicable.

### What to Expect

1. **Acknowledgement**: We will acknowledge receipt of your report within **3 business days**.
2. **Investigation**: Our security team will investigate and validate the report within **10 business days**.
3. **Resolution**: We will develop and release a fix based on severity:
   - **Critical**: Patch released within 7 days of validation.
   - **High**: Patch released within 14 days of validation.
   - **Medium**: Patch released within 30 days of validation.
   - **Low**: Patch released in the next regular release cycle.
4. **Disclosure**: After the fix is released, we will publish a security advisory. We will coordinate with you on the disclosure timeline.

### Disclosure Timeline

| Phase | Duration |
|-------|----------|
| Report received | Day 0 |
| Acknowledgement | Within 3 business days |
| Initial assessment | Within 10 business days |
| Fix development | Based on severity (7–30 days) |
| Coordinated disclosure | After fix is publicly released |

We ask that you refrain from public disclosure until we have released a fix and notified users through our security advisory process.

## Security Best Practices

### Dependencies
- Run `pip-audit` regularly to check for known vulnerabilities.
- Review all dependency updates before merging.
- Use pinned versions in production builds.
- Monitor the Python Advisory Database (PyPA) for vulnerabilities.

### Input Validation
- Validate all uploaded images (size, format, dimensions, content type).
- Sanitize all database queries via SQLAlchemy ORM — no raw SQL with user input.
- Enforce JSON schema validation on all AI model outputs and API responses.
- Limit maximum upload size to 10 MB.

### Secrets Management
- Never commit `.env` files, tokens, passwords, or API keys.
- Use environment variables or a secrets manager for configuration.
- If secrets are accidentally committed, rotate them immediately and purge from Git history.
- All secrets are excluded via `.gitignore` and `.dockerignore`.

### Offline-First Design
- No telemetry, analytics, or crash reporting to third-party services.
- All models, data, and inference remain on the local filesystem.
- Zero outbound network connections in production builds — verified in CI.
- Verify network isolation in CI tests (`tests/test_offline.py`).

### Database Security
- Use WAL mode for SQLite to prevent corruption and allow concurrent reads.
- Back up `agriguard.db` regularly to a secure location.
- Do not expose the database file via the web server's static file serving.
- Database file is excluded from version control via `.gitignore`.

### Model Files
- Keep model artifacts in `.gitignore` (excluded from version control).
- Verify checksums of downloaded model files before use.
- Use quantized models to reduce attack surface and resource usage.
- Model files are binary blobs; do not process them as untrusted input.

### Supply Chain Security
- Review all new dependencies for known vulnerabilities before adding.
- Use `requirements.txt` with compatible version ranges (not unbounded).
- Run `pip-audit` in CI on every pipeline execution.
- Pin base Docker image digests for reproducible builds.

## Security Contacts

- **Security Email**: security@example.com
- **PGP Key**: Available on request for encrypted disclosure.
- **GitLab Issues**: Do NOT file security issues publicly.
