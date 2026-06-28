# AgriGuard AI Constitution

## Mission

AgriGuard AI helps farmers, agricultural experts, and field volunteers protect crop
health through offline image analysis, disease prediction, AI recommendations,
weather-aware guidance, emergency SOS support, and location-aware services.
Every feature must strengthen sustainable farming while preserving trust,
privacy, and local control.

## Governing Principles

### 1. Farmer-First Development

AgriGuard AI exists for farmers first. Product decisions must prioritize clear
crop health guidance, low-bandwidth and offline workflows, accessible language,
and practical remedies that can be acted on in the field.

### 2. Explainable AI Decisions

Disease prediction must include a confidence score, visible reasoning where
available, and farmer-readable remediation guidance. The system must never
present AI recommendations as a substitute for agricultural experts when the
confidence is low, symptoms are ambiguous, or emergency intervention is needed.

### 3. Privacy by Design

Farmer images, locations, diagnosis history, emergency SOS data, and weather
context must remain local unless a user explicitly chooses to share them. Runtime
code must not add telemetry, cloud inference, third-party analytics, or hidden
network calls.

### 4. Secure Coding

Inputs such as uploaded images, query parameters, file paths, and JSON payloads
must be validated. SQL must be parameterized through ORM or safe database APIs.
Secrets, credentials, model tokens, and API keys must never be committed.

### 5. Open-Source Collaboration

The repository must be readable, auditable, and welcoming to contributors.
Architecture decisions, feature specifications, and work division should be
documented so farmers, students, researchers, and agricultural experts can
evaluate and improve the platform.

### 6. Accessibility

Interfaces must support keyboard navigation, readable contrast, responsive
layouts, and clear messages for low-literacy or multilingual farming contexts.
Image analysis flows must provide useful text alternatives and error recovery.

### 7. Offline-First Support

Core diagnosis workflows should work without internet access wherever possible.
Models, schemas, recommendations, and dashboards should favor local execution,
local storage, CPU-only inference, and predictable behavior in rural settings.

### 8. Test-Driven Development

New behavior must be covered with focused tests for preprocessing, inference
contracts, API responses, database persistence, and error handling. Tests should
mock external binaries such as llama.cpp and must run in CI.

### 9. Spec-Driven Development

Significant features must begin with a specification that describes user value,
functional requirements, data contracts, security considerations, offline
constraints, and acceptance criteria before implementation begins.

### 10. Documentation-First Workflow

Changes that affect farmers, agricultural experts, AI recommendations, crop
health reports, emergency SOS flows, weather insights, image analysis, APIs, or
deployment must update the relevant documentation in `docs/` or `.specify/`.

## Architecture Guardrails

- Runtime AI inference must be CPU-only.
- No cloud AI SDKs or external inference calls may be introduced for core
  diagnosis.
- SQLite schema, API schemas, and JSON report schemas must remain aligned.
- Model artifacts belong in `models/` and must stay out of version control.
- Sensitive user data must not be logged beyond the minimum needed for local
  troubleshooting.

## Quality Gates

- `ruff check .` must pass.
- `mypy backend/` must pass for typed backend code.
- `pytest backend/tests/` and applicable integration tests must pass.
- Secret scanning must pass before merge.
- Documentation must be updated for behavior, schema, deployment, or workflow
  changes.

