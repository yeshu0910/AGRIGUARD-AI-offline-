# Contributing to AgriGuard AI

Thank you for your interest in contributing to AgriGuard AI. This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ (for frontend build)
- Git
- Virtual environment tool (`python -m venv`)

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone git@gitlab.com:yeshu_09/agriguard-ai.git
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
pytest backend/tests/
```

## Installation

See the [README.md](README.md) for full installation instructions.

## Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/short-description` | `feature/tflite-model-wrapper` |
| Bugfix | `fix/short-description` | `fix/camera-preview-crash` |
| Hotfix | `hotfix/short-description` | `hotfix/sqlite-concurrent-write` |
| Documentation | `docs/short-description` | `docs/fix-broken-link-in-readme` |
| Refactor | `refactor/short-description` | `refactor/simplify-preprocessor` |
| Chore | `chore/short-description` | `chore/update-requirements` |

## Commit Message Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) with the format:

```
<type>(<scope>): <subject>
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

### Examples
```
feat(backend): add /api/v1/health endpoint
fix(frontend): resolve camera capture crash on mobile Safari
docs(README): update installation instructions
refactor(services): simplify preprocessor pipeline
```

## Pull Request Workflow

1. **Create a branch** from `main` using the naming convention above.
2. **Make your changes** and ensure tests pass locally.
3. **Commit your changes** using the commit message convention.
4. **Push the branch** to your fork.
5. **Open a Merge Request** against `main`.
6. **Fill out the MR template** with:
   - Summary of changes
   - Related issue(s)
   - Screenshots or demo video (if UI changes)
   - Checklist: tests added/updated, docs updated, no secrets committed
7. **Request review** from at least one team member.
8. **Address review feedback** and push additional commits to the same branch.
9. **Merge** once approved and CI is green.

## Code Review Process

- All code must be reviewed before merging.
- Reviewers check for:
  - Correctness and edge-case handling
  - Test coverage (unit/integration)
  - Documentation updates
  - No hardcoded secrets or credentials
  - Compliance with offline-first and CPU-only constraints
  - SQLite and API schema consistency
- Authors should respond to all review comments.
- Approvals required: 1 for docs/chores, 2 for features/bugfixes.

## Coding Standards

### Python
- Follow PEP 8.
- Type hints are required for all public functions and methods (`mypy` enforced).
- Docstrings required for modules, classes, and public functions.
- Maximum line length: 100 characters.
- Use `ruff` and `black` for formatting.

### JavaScript / TypeScript
- Use meaningful variable and function names.
- Prefer `const` and `let` over `var`.
- Handle errors with `.catch()` or `try/catch`.

### General
- Keep functions small and focused.
- Avoid magic numbers; extract named constants.
- Do not commit secrets or credentials.
- Update documentation when changing behavior.

## Testing Instructions

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=backend --cov-report=html
```

### Run specific test file
```bash
pytest backend/tests/test_api.py
```

### Lint and format
```bash
ruff check .
black .
```

### Type check
```bash
mypy backend/
```
