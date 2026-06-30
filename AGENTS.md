# Agents — AgriGuard AI

This file provides context for AI coding agents and automated development tools. It defines repository architecture, coding guidelines, and workflow expectations.

## Repository Architecture

AgriGuard AI is an offline-first, CPU-only crop disease diagnosis system.

```
agriguard-ai/
├── AgriGuard/backend/   FastAPI + TFLite + llama.cpp backend
├── frontend/            HTML5 + Tailwind CSS + Vanilla JS
├── models/              .tflite and .gguf model artifacts (gitignored)
├── database/            SQLite schema and runtime DB (gitignored)
├── images/              Sample images for demo
├── assets/              Logos and icons
├── docs/                Documentation
├── tests/               Integration and end-to-end tests
├── build/               Deployment bundles (gitignored)
├── .specify/            Spec-Kit specifications
```

## Directory Structure

| Path | Purpose |
|------|---------|
| `AgriGuard/backend/main.py` | FastAPI application entrypoint |
| `AgriGuard/backend/database.py` | SQLite ORM, CRUD operations |
| `AgriGuard/backend/detect.py` | Disease detection pipeline |
| `AgriGuard/backend/preprocess.py` | Image preprocessing with OpenCV |
| `AgriGuard/backend/recommendation.py` | Curated knowledge base for treatments |
| `AgriGuard/backend/llm.py` | Local LLM recommendation generation |
| `AgriGuard/backend/crop_detector.py` | PlantVillage label parser |
| `frontend/src/js/` | Application JavaScript |
| `frontend/src/css/` | Styles |
| `models/` | Local AI model files |
| `database/schema.sql` | SQLite DDL |
| `docs/` | All project documentation |

## Coding Guidelines

- Python 3.10+ with type hints enforced by `mypy` in strict mode.
- Use `ruff` for linting and `ruff format` for formatting.
- Use `black` for code formatting where `ruff format` is not configured.
- All public functions and classes must have Google-style docstrings.
- No network calls allowed in runtime code paths.
- All inference must be CPU-only.
- SQLite writes must be serialized to avoid corruption.
- JSON schemas must be validated with Pydantic.
- Never hardcode secrets or API keys.

## Tool Configuration

All quality tools are configured in `pyproject.toml`:

| Tool | Purpose | Config Section |
|------|---------|---------------|
| Ruff | Linting & formatting | `[tool.ruff]` |
| Mypy | Type checking | `[tool.mypy]` |
| Flake8 | Style guide | `[tool.flake8]` |
| Pylint | Code quality | `[tool.pylint]` |
| Bandit | Security scanning | `[tool.bandit]` |
| Vulture | Dead code detection | `[tool.vulture]` |
| Pyupgrade | Python modernization | `[tool.pyupgrade]` |
| pip-audit | Dependency audit | `[tool.pip-audit]` |
| pytest-cov | Test coverage (80% min) | `[tool.coverage]` |

## AI Agent Instructions

When working on this repository:

1. **Read before writing**: Inspect existing files to understand patterns and conventions.
2. **Preserve offline-first design**: Do not introduce cloud APIs or SDKs.
3. **Respect CPU-only constraint**: Do not add CUDA, ROCm, or Vulkan dependencies.
4. **Maintain schema consistency**: API, DB, and JSON schemas must stay aligned.
5. **Update docs**: If you change behavior, update the relevant markdown files in `docs/`.
6. **Run checks**: Ensure `ruff check .`, `mypy backend/`, and `pytest` pass before committing.
7. **Check line length**: Keep lines under 100 characters unless justified.
8. **Use conventional commits**: Follow the format in `CONTRIBUTING.md`.
9. **Run all pre-commit hooks**: `pre-commit run --all-files`.
10. **Maintain test coverage**: Keep minimum 80% line coverage.

## Development Workflow

1. Create a branch from `main`.
2. Make changes and run tests locally.
3. Run all quality checks:
   ```bash
   ruff check .
   ruff format --check .
   mypy AgriGuard/backend/
   flake8 AgriGuard/backend/
   pylint AgriGuard/backend/
   vulture AgriGuard/backend/ --min-confidence 80
   bandit -qr AgriGuard/backend/
   pytest --cov=AgriGuard.backend --cov-fail-under=80
   ```
4. Commit with conventional commit messages.
5. Open a merge request.

## Testing Workflow

- Unit tests live in `AgriGuard/backend/tests/` and `tests/`.
- Use `pytest` as the test runner.
- Mock external binaries (`llama.cpp`) in unit tests.
- Use test images from `images/` or generate synthetic fixtures.
- Coverage threshold: 80% minimum enforced in CI.

## Security Guidelines

- Do not commit secrets, credentials, or tokens.
- Validate all user inputs (images, query params).
- Sanitize SQL queries via ORM only; no raw SQL with user input.
- Keep model files in `.gitignore`.
- Review dependencies for known vulnerabilities before adding new packages.
- Report security issues to the maintainers privately (see `SECURITY.md`).

## Commit Conventions

See `CONTRIBUTING.md` for the full conventional commits specification.

| Type | Use Case |
|------|----------|
| `feat` | New functionality |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `security` | Security-related changes |
| `ci` | CI/CD changes |
| `perf` | Performance improvements |

## CI/CD Pipeline

The GitLab CI pipeline includes these stages in order:
1. `format` — Ruff format check
2. `lint` — Ruff, Flake8, Pylint, Vulture
3. `type_check` — Mypy
4. `security` — Bandit, Semgrep, Gitleaks
5. `dependency_audit` — pip-audit
6. `test` — pytest with coverage
7. `coverage` — Coverage enforcement (80% min)
8. `build` — Docker build, changelog generation
9. `release` — GitLab release (tagged versions only)
