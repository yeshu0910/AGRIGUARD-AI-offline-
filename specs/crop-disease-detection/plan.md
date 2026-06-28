# Implementation Plan: Crop Disease Detection

## Architecture

The crop disease detection feature follows AgriGuard AI's offline-first design.
The frontend captures or uploads a crop image, FastAPI validates the request,
local image analysis prepares model input, TensorFlow Lite performs CPU-only
disease prediction, recommendation logic creates farmer-readable guidance, and
SQLite stores the result for dashboard history.

## Technical Design

- Frontend: upload/camera flow, progress state, result view, dashboard history.
- Backend: diagnosis API, validation, error responses, report assembly.
- AI: deterministic preprocessing and local CPU-only inference.
- Database: SQLite diagnosis record with prediction, confidence, recommendations,
  timestamp, image reference, and optional weather/location context.
- Offline: all core image analysis and AI recommendations run locally.

## Data Flow

1. Farmer uploads a crop image.
2. Backend validates the file.
3. Preprocessor prepares the image tensor.
4. Local model returns disease prediction and confidence score.
5. Recommendation service adds remedy and prevention guidance.
6. SQLite persists the diagnosis.
7. Dashboard displays crop health history.
8. Error states guide the farmer toward retry or agricultural expert support.

## Milestones

| Milestone | Deliverable | Exit Criteria |
|-----------|-------------|---------------|
| M1 | API and schema contract | Spec reviewed and accepted |
| M2 | Local inference path | Mocked prediction flow works |
| M3 | Dashboard result view | Farmer sees confidence and remedy |
| M4 | Offline validation | No runtime network dependency |
| M5 | Release readiness | CI, tests, docs, and secret scan pass |

## Risks

| Risk | Mitigation |
|------|------------|
| Missing model artifact | Startup checks and setup documentation |
| Low confidence prediction | Expert review messaging and alternatives |
| Unsafe recommendation | Structured schema and safety notes |
| SQLite contention | Serialized writes |

## Deployment Plan

- Keep `.tflite` and `.gguf` model files in `models/` and out of Git.
- Package backend with CPU-only dependencies.
- Initialize SQLite before first field use.
- Verify Ruff, Mypy, Pytest, Bandit, and Gitleaks in CI.

## Rollback Plan

- Hide or disable the diagnosis route if validation fails.
- Restore previous SQLite schema from backup if a migration was introduced.
- Revert to the previous model artifact if accuracy or latency regresses.

