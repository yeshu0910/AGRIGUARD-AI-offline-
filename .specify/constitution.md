# AgriGuard AI Project Constitution

## Purpose

This document defines the non-negotiable principles, architecture rules, and quality standards for the AgriGuard AI project. All specifications, design decisions, and code must align with this constitution.

## Core Principles

### Offline-First
- The application must operate fully offline.
- No cloud APIs, telemetry, or external network calls in any runtime code path.
- All models, data, and logic execute locally on the device.

### CPU-Only
- Inference runs exclusively on CPU.
- No GPU acceleration frameworks (CUDA, ROCm, Vulkan, Metal) may be introduced.
- Quantized models are preferred to maximize CPU throughput.

### Privacy Preserving
- No personal data leaves the device.
- SQLite is the sole persistence layer.
- No third-party analytics or crash reporting.

### Structured Output
- All AI outputs must be JSON.
- JSON must be validated against a strict schema before storage or display.
- Malformed outputs must be caught, logged, and retried.

### Reproducibility
- Pinned dependency versions for builds and tests.
- Deterministic image preprocessing pipelines.
- Model metadata (version, quantization, input resolution) tracked in reports.

## Architecture Constraints

- Backend: FastAPI on Python 3.10+
- Frontend: HTML5 + Tailwind CSS + Vanilla JS (PWA-capable)
- Database: SQLite with FTS5 full-text search
- Inference: TensorFlow Lite (CPU delegate)
- LLM: llama.cpp with Phi-3 Mini GGUF (4-bit)

## Quality Gates

- All code must pass ruff, mypy, and bandit checks.
- Unit test coverage must not decrease.
- Integration tests must pass before merge.
- Pre-commit hooks must be green.
- No secrets in version control.

## Decision Making

- Architecture changes require a proposal in `docs/` and team sign-off.
- Breaking schema or API changes require a migration plan.
- New dependencies require security review and version pinning.
