# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | Yes                |
| < 0.1   | No                 |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

- **Do not** open a public issue for security vulnerabilities.
- Email the maintainers at `security@example.com` with:
  - A description of the vulnerability.
  - Steps to reproduce.
  - Potential impact.
  - Suggested fixes if available.

We will acknowledge receipt within 3 business days and provide a detailed response within 10 business days.

## Security Best Practices

### Dependencies
- Run `pip-audit` or `safety check` regularly.
- Review dependency updates before merging.
- Use pinned versions in production.

### Input Validation
- Validate all uploaded images (size, format, dimensions).
- Sanitize database queries via ORM.
- Enforce JSON schema validation on all LLM outputs.

### Secrets Management
- Never commit `.env` files or secrets.
- Use environment variables or a secrets manager.
- Rotate credentials if they are accidentally committed.

### Offline-First Design
- No telemetry or crash reporting to third-party services.
- All models and data remain on the local filesystem.
- Verify zero outbound network connections in production builds.

### Database
- Use WAL mode for SQLite to prevent corruption.
- Back up `agriguard.db` regularly.
- Do not expose the database file via the web server.

### Model Files
- Keep model artifacts in `.gitignore`.
- Verify checksums of downloaded model files.
- Use quantized models to reduce attack surface and resource usage.
