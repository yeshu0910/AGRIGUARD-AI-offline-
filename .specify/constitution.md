# AgriGuard AI Project Constitution

## Purpose

This document defines the non-negotiable principles, architecture rules, and quality standards for the AgriGuard AI project. All specifications, design decisions, and code must align with this constitution.

## Core Principles

### Offline-First
- The application must operate fully offline.
- No cloud APIs, telemetry, or external network calls in any runtime code path.
- All models, data, and logic execute locally on the device.
- Zero outbound network connections in production builds.

### CPU-Only
- Inference runs exclusively on CPU.
- No GPU acceleration frameworks (CUDA, ROCm, Vulkan, Metal) may be introduced.
- Quantized models are preferred to maximize CPU throughput.
- Multi-threading limited to CPU threads only.

### Privacy Preserving
- No personal data leaves the device.
- SQLite is the sole persistence layer.
- No third-party analytics or crash reporting.
- All data stays on-device; user owns their data entirely.

### Structured Output
- All AI outputs must be JSON.
- JSON must be validated against a strict schema before storage or display.
- Malformed outputs must be caught, logged, and retried.
- Pydantic v2 enforces schema contracts for every API response.

### Reproducibility
- Pinned dependency versions for builds and tests.
- Deterministic image preprocessing pipelines.
- Model metadata (version, quantization, input resolution) tracked in reports.
- All builds must be reproducible from source.

## Architecture Constraints

- Backend: FastAPI on Python 3.10+
- Frontend: HTML5 + Tailwind CSS + Vanilla JS (PWA-capable)
- Database: SQLite with WAL mode
- Inference: TensorFlow Lite (CPU delegate)
- LLM: llama.cpp with Phi-3 Mini GGUF (4-bit quantized)
- Packaging: Docker multi-stage builds or PyInstaller standalone

## Quality Gates

All checks must pass before any merge:

### Linting & Formatting
- Ruff (all rulesets: E, F, I, N, W, UP, B, C4, SIM, ARG, RUF)
- Ruff Format (must produce no diffs)
- Flake8 (style guide enforcement)
- Pylint (code quality analysis)
- Vulture (dead code detection, min confidence 80%)

### Type Checking
- Mypy (strict mode, disallow untyped defs)

### Security
- Bandit (all Python security issues)
- Semgrep (pattern-based SAST, auto rules)
- Gitleaks (secret scanning)
- pip-audit (dependency vulnerability audit)

### Testing
- pytest with pytest-cov
- Minimum line coverage: 80%
- All unit, integration, and end-to-end tests must pass

### Pre-commit
- All pre-commit hooks must be green
- Includes: trailing whitespace, EOF fixer, YAML/JSON/TOML validation, merge conflict detection

### Modernization
- Pyupgrade (Python 3.10+ idioms enforced)

## Project Structure

```
agriguard-ai/
├── backend/          FastAPI + TFLite + llama.cpp
├── frontend/         HTML5 + Tailwind CSS + Vanilla JS
├── models/           .tflite and .gguf artifacts (gitignored)
├── database/         SQLite schema and runtime DB (gitignored)
├── images/           Sample images for demo
├── assets/           Logos and icons
├── docs/             Documentation
├── tests/            Integration and end-to-end tests
└── build/            Deployment bundles (gitignored)
```

## Decision Making

- Architecture changes require a proposal in `docs/` and team sign-off.
- Breaking schema or API changes require a migration plan.
- New dependencies require security review and version pinning.
- All changes must follow Conventional Commits specification.
- All code must be reviewed before merging (1 approval for docs/chore, 2 for features/bugfixes).

## Licensing

- GNU Affero General Public License v3.0 or later.
- All contributions are made under AGPLv3.
- Third-party dependencies must have compatible licenses.
