# Implementation Plan: Crop Disease Detection

## Architecture

Crop disease detection sits at the center of AgriGuard AI's offline-first
workflow. The frontend collects a crop image from a farmer or agricultural
expert, FastAPI validates and processes the upload, a CPU-only TensorFlow Lite
service predicts disease, a local recommendation layer prepares explainable
remedies, and SQLite stores the report for the dashboard.

## Technical Design

- Frontend: image upload/camera flow, progress state, result panel, dashboard
  history, and accessible error messages.
- API: `POST /api/v1/diagnose` for image analysis and `GET /api/v1/history`
  for farmer dashboard records.
- AI: deterministic preprocessing followed by local TensorFlow Lite inference.
- Recommendations: structured remedy payload covering immediate action,
  sustainable farming, prevention, safety, and expert escalation.
- Database: SQLite diagnosis table aligned with API response schema.
- Offline: no cloud AI SDKs, no network inference, model files loaded locally.

## Data Flow

1. Farmer uploads a crop image from the dashboard.
2. Backend validates content type, size, and image readability.
3. Preprocessor resizes and normalizes the image for the configured model.
4. TensorFlow Lite runs CPU-only disease prediction.
5. Recommendation service builds explainable remedy guidance.
6. SQLite stores the image reference, prediction, confidence, and guidance.
7. Dashboard displays the latest crop health result and history.
8. Errors return safe messages without exposing internals.

## Modules

| Module | Responsibility |
|--------|----------------|
| `backend/main.py` | FastAPI app registration and health routing |
| `backend/routers/` | Diagnosis and history endpoints |
| `backend/services/preprocessor.py` | Image validation and model-ready tensors |
| `backend/services/tflite_inference.py` | CPU-only disease prediction |
| `backend/services/report_builder.py` | Recommendation and report assembly |
| `backend/database/` | SQLite ORM models, schemas, CRUD |
| `frontend/src/js/` | Upload flow, dashboard rendering, offline states |
| `docs/` | Farmer, expert, and deployment guidance |

## Milestones

| Milestone | Deliverable | Exit Criteria |
|-----------|-------------|---------------|
| M1 | Contract approved | Spec, API schema, and DB fields reviewed |
| M2 | Backend diagnosis path | Valid image returns structured prediction |
| M3 | Dashboard integration | Farmer can view result and history |
| M4 | Offline validation | No runtime network calls in diagnosis flow |
| M5 | Release readiness | CI, tests, docs, and security checks pass |

## Risks

| Risk | Mitigation |
|------|------------|
| Model unavailable on deployment device | Preflight checks and setup docs |
| Incorrect or unsafe treatment guidance | Confidence display and expert escalation |
| SQLite write contention | Serialized writes and transaction boundaries |
| Large field images causing latency | Size limits and efficient preprocessing |

## Timeline

| Phase | Duration | Work |
|-------|----------|------|
| Planning | 0.5 day | Finalize schema, UX, and acceptance criteria |
| Backend | 1 day | API, services, validation, persistence |
| Frontend | 1 day | Upload flow, result view, dashboard history |
| AI validation | 0.5 day | Model contract, confidence handling, mocks |
| Testing/docs | 1 day | Unit/integration tests and user docs |

## Deployment Plan

- Keep `.tflite` model artifacts in `models/` and out of Git.
- Package backend with CPU-only dependencies.
- Initialize SQLite schema before first run.
- Build or serve frontend assets for offline-first usage.
- Run `ruff check .`, `mypy backend/`, `pytest`, Bandit, and Gitleaks.
- Publish changelog entries with Git-Cliff.

## Rollback Plan

- Disable the diagnosis route or frontend entry point if validation fails.
- Restore the previous SQLite schema from backup if a migration is introduced.
- Revert to the previous model artifact if confidence or latency regresses.
- Keep existing dashboard history readable even if new recommendation fields are
  hidden during rollback.

