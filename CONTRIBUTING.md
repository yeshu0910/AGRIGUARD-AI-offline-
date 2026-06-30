# Contributing to AgriGuard AI

Thank you for your interest in contributing to AgriGuard AI. This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing. We are committed to providing a welcoming and inclusive environment.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ (for frontend build, optional)
- Git
- Virtual environment tool (`python -m venv`)

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone <repository-url>
cd agriguard-ai

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Install pre-commit hooks
pre-commit install

# 5. Verify setup
pytest
```

## Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/short-description` | `feature/tflite-model-wrapper` |
| Bugfix | `fix/short-description` | `fix/camera-preview-crash` |
| Hotfix | `hotfix/short-description` | `hotfix/sqlite-concurrent-write` |
| Documentation | `docs/short-description` | `docs/fix-broken-link-in-readme` |
| Refactor | `refactor/short-description` | `refactor/simplify-preprocessor` |
| Chore | `chore/short-description` | `chore/update-requirements` |
| Security | `security/short-description` | `security/upgrade-dependencies` |
| Performance | `perf/short-description` | `perf/optimize-preprocessing` |

## Commit Message Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) with the format:

```
<type>(<scope>): <subject>

<body>
<footer>
```

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, semicolons) |
| `refactor` | Code refactoring |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |
| `security` | Security fixes or updates |
| `ai` | AI/ML model or prompt changes |
| `ci` | CI/CD configuration changes |

### Examples
```
feat(backend): add POST /api/v1/diagnose endpoint
fix(frontend): resolve camera capture crash on mobile Safari
docs(README): update installation instructions
refactor(services): simplify preprocessor pipeline
test(backend): add unit tests for recommendation engine
ci: add Semgrep and pip-audit to security stage
```

## Pull Request Workflow

1. **Create a branch** from `main` using the naming convention above.
2. **Make your changes** and ensure all quality checks pass locally.
3. **Commit your changes** using the commit message convention.
4. **Run all quality checks** before pushing:
   ```bash
   ruff check .
   ruff format --check .
   mypy backend/
   flake8 backend/
   pylint backend/
   vulture backend/ --min-confidence 80
   bandit -qr backend/
   pytest --cov=backend --cov-fail-under=80
   ```
5. **Push the branch** to your fork.
6. **Open a Merge Request** against `main`.
7. **Fill out the MR template** with:
   - Summary of changes
   - Related issue(s)
   - Screenshots or demo video (if UI changes)
   - Checklist: tests added/updated, docs updated, no secrets committed, all CI checks pass
8. **Request review** from at least one team member.
9. **Address review feedback** and push additional commits to the same branch.
10. **Merge** once approved and CI is green.

## Code Review Process

- All code must be reviewed before merging.
- Reviewers check for:
  - Correctness and edge-case handling
  - Test coverage (unit/integration, minimum 80%)
  - Documentation updates
  - No hardcoded secrets or credentials
  - Compliance with offline-first and CPU-only constraints
  - SQLite and API schema consistency
  - Type hints and mypy compliance
  - Security considerations
- Authors should respond to all review comments.
- Approvals required: 1 for docs/chores, 2 for features/bugfixes.

## Coding Standards

### Python
- Follow PEP 8 style guide.
- Type hints are required for all functions and methods (`mypy` enforced in strict mode).
- Docstrings required for all modules, classes, and public functions (Google style).
- Maximum line length: 100 characters.
- Use `ruff` for linting and `ruff format` for formatting.
- All public functions must have type-annotated signatures.
- Use Pydantic v2 for all data validation and serialization.

### JavaScript (Frontend)
- Use meaningful variable and function names.
- Prefer `const` and `let` over `var`.
- Handle errors with `.catch()` or `try/catch`.
- Use async/await over raw promises.
- Follow the existing patterns in `frontend/src/js/`.

### Security
- Never commit secrets, credentials, or tokens.
- Validate all user inputs before processing.
- Use ORM for all database queries (no raw SQL with user input).
- Review dependencies for vulnerabilities before adding.
- Follow the guidelines in [SECURITY.md](SECURITY.md).

### General
- Keep functions small and focused (single responsibility).
- Avoid magic numbers; extract named constants.
- Follow the offline-first and CPU-only principles.
- Update documentation when changing behavior.
- Maintain schema consistency across API, DB, and JSON.

## Testing Instructions

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=backend --cov-report=html
```

### Run with coverage and fail under threshold
```bash
pytest --cov=backend --cov-fail-under=80
```

### Run specific test file
```bash
pytest backend/tests/test_api.py
```

### Run all quality checks
Run the following before pushing:
```bash
# Linting and formatting
ruff check .
ruff format --check .

# Type checking
mypy backend/

# Style and quality
flake8 backend/
pylint backend/
vulture backend/ --min-confidence 80

# Security
bandit -qr backend/
pip-audit -r requirements.txt

# Modernization
pyupgrade --py310-plus **/*.py

# Testing
pytest --cov=backend --cov-fail-under=80
```

## CI/CD Pipeline

The GitLab CI pipeline includes the following stages:
1. **format** - Ruff format check
2. **lint** - Ruff, Flake8, Pylint, Vulture
3. **type_check** - Mypy
4. **security** - Bandit, Semgrep, Gitleaks
5. **dependency_audit** - pip-audit
6. **test** - pytest with coverage
7. **coverage** - Coverage report with 80% threshold
8. **build** - Docker build and changelog generation
9. **release** - GitLab release creation

All stages must pass before merge.
