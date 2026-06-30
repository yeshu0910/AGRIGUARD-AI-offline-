# Changelog

All notable changes to AgriGuard AI are documented here. This file is compatible
with Git-Cliff and the repository's Conventional Commits workflow.

## [1.0.0] - 2026-06-29

### Added
- Initial release of AgriGuard AI
- Offline crop disease detection using TensorFlow Lite on CPU
- Local LLM recommendation engine using llama.cpp + Phi-3 Mini GGUF
- Knowledge base with 14+ curated crop-disease treatment plans
- FastAPI REST backend with health, detect, history, and export endpoints
- Responsive offline-first web frontend (HTML5 + Tailwind CSS + Vanilla JS)
- SQLite persistence with WAL mode for offline data storage
- Image preprocessing pipeline with OpenCV (resize, normalize, leaf extraction)
- CSV and JSON export functionality
- Docker multi-stage build for production deployment
- Comprehensive test suite with 80%+ coverage target

### Documentation
- Complete README with project overview, features, installation, and API docs
- CONTRIBUTING guide with development workflow and commit conventions
- USER_MANUAL for farmers and extension officers
- AGENTS.md for AI coding agent context
- SECURITY.md with vulnerability reporting and disclosure timeline
- Full documentation suite in `docs/` (architecture, scope, folder structure)
- Spec-Kit specifications in `.specify/` for feature-driven development

### CI/CD
- Production GitLab CI pipeline with 9 stages (format, lint, type_check, security,
  dependency_audit, test, coverage, build, release)
- Complete pre-commit hooks configuration (ruff, mypy, flake8, pylint, bandit,
  vulture, pyupgrade, codespell)
- Automated dependency auditing with pip-audit
- Security scanning with Bandit, Semgrep, and Gitleaks
- Coverage enforcement with minimum 80% threshold
- Automated changelog generation with Git-Cliff
- Docker build and push on default branch

### Quality Tools
- Ruff linting and formatting with comprehensive rule selection
- Mypy strict mode type checking
- Flake8 style enforcement
- Pylint code quality analysis
- Vulture dead code detection
- Bandit security scanning
- Semgrep pattern-based SAST
- Pyupgrade Python modernization
- pip-audit dependency vulnerability scanning
- pytest with pytest-cov for testing and coverage

### Configuration
- Unified pyproject.toml with all tool configurations
- Complete requirements-dev.txt with latest tool versions
- Production Dockerfile with multi-stage build
- Comprehensive .dockerignore and .gitignore
- cliff.toml for Git-Cliff changelog generation
- .editorconfig for consistent editor settings

## [0.1.0] - 2026-06-28

### Added
- Project initialization and documentation suite.
- Planned FastAPI backend architecture with SQLite and SQLAlchemy.
- Planned TensorFlow Lite inference service and OpenCV preprocessing pipeline.
- Planned llama.cpp integration for local AI recommendations.
- Responsive offline-first frontend documentation for farmers and agricultural experts.
- Development tooling configuration for crop health, image analysis, and sustainable farming workflows.
