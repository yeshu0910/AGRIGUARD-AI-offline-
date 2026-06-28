# Agents — AgriGuard AI

This file provides context for AI coding agents and automated development tools. It defines repository architecture, coding guidelines, and workflow expectations.

## Repository Architecture

AgriGuard AI is an offline-first, CPU-only crop disease diagnosis system.

```
agriguard-ai/
├── backend/          FastAPI + SQLAlchemy + TFLite + llama.cpp
├── frontend/         HTML5 + Tailwind CSS + Vanilla JS
├── models/           .tflite and .gguf model artifacts (gitignored)
├── database/         SQLite schema and runtime DB (gitignored)
├── images/           Sample images for demo
├── assets/           Logos and icons
├── docs/             Phase 1 documentation
├── tests/            Integration and end-to-end tests
└── build/            Deployment bundles (gitignored)
```

## Directory Structure

| Path | Purpose |
|------|---------|
| `backend/main.py` | FastAPI application entrypoint |
| `backend/database/` | SQLAlchemy ORM, schemas, CRUD |
| `backend/routers/` | API route handlers |
| `backend/services/` | Business logic: preprocessor, TFLite, LLM, reports |
| `backend/utils/` | Shared utilities |
| `backend/tests/` | Backend unit and integration tests |
| `frontend/src/js/` | Application JavaScript |
| `frontend/src/css/` | Styles |
| `models/` | Local AI model files |
| `database/schema.sql` | SQLite DDL |
| `docs/` | All project documentation |

## Coding Guidelines

- Python 3.10+ with type hints enforced by `mypy`.
- Use `ruff` for linting and formatting.
- Use `black` for code formatting where `ruff` format is not configured.
- All public functions and classes must have docstrings.
- No network calls allowed in runtime code paths.
- All inference must be CPU-only.
- SQLite writes must be serialized to avoid corruption.
- JSON schemas must be validated with Pydantic.
- Never hardcode secrets or API keys.

## AI Agent Instructions

When working on this repository:

1. **Read before writing**: Inspect existing files to understand patterns and conventions.
2. **Preserve offline-first design**: Do not introduce cloud APIs or SDKs.
3. **Respect CPU-only constraint**: Do not add CUDA, ROCm, or Vulkan dependencies.
4. **Maintain schema consistency**: API, DB, and JSON schemas must stay aligned.
5. **Update docs**: If you change behavior, update the relevant markdown files in `docs/`.
6. **Run tests**: Ensure `pytest backend/tests/` passes before committing.
7. **Check line length**: Keep lines under 100 characters unless justified.
8. **Use conventional commits**: Follow the format in `CONTRIBUTING.md`.

## Development Workflow

1. Create a branch from `main`.
2. Make changes and run tests locally.
3. Run `ruff check .` and `mypy backend/`.
4. Run `pytest` with coverage.
5. Commit with conventional commit messages.
6. Open a merge request.

## Testing Workflow

- Unit tests live in `backend/tests/`.
- Integration tests live in `tests/integration/`.
- Use `pytest` as the test runner.
- Mock external binaries (`llama.cpp`) in unit tests.
- Use test images from `images/` or generate synthetic fixtures.

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
