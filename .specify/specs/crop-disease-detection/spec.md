# Feature Specification: Crop Disease Detection

## Feature Overview

Crop disease detection lets a farmer or agricultural expert upload a crop image,
run offline image analysis, receive a disease prediction with confidence score,
and review AI-generated remedy recommendations in the AgriGuard AI dashboard.
The workflow supports crop health monitoring, sustainable farming decisions,
and field diagnosis when internet access is unreliable or unavailable.

## Problem Statement

Farmers often need rapid disease identification before an infection spreads.
Cloud-based tools can fail in rural areas, expose sensitive farm images or
locations, and provide recommendations without enough explanation. AgriGuard AI
must provide local, explainable, privacy-preserving crop disease support.

## Goals

- Accept crop leaf images from upload or camera capture.
- Run CPU-only local AI inference for disease prediction.
- Return top disease label, confidence score, and safe remedy recommendation.
- Persist diagnosis records for farmer dashboard history and export.
- Provide clear errors for invalid images, missing models, and low confidence.
- Preserve offline support for core image analysis and dashboard review.

## Non Goals

- Cloud AI inference or external diagnosis APIs.
- Replacing certified agricultural experts for severe or unclear cases.
- Automatic purchase or application of pesticides.
- Training new models inside the production diagnosis workflow.

## Functional Requirements

- FR-1: The system shall accept JPEG and PNG crop images through a web upload
  flow and backend API.
- FR-2: The system shall validate file type, file size, and image readability
  before inference.
- FR-3: The system shall preprocess images into the configured model input
  dimensions without modifying the original uploaded image unexpectedly.
- FR-4: The system shall run TensorFlow Lite disease prediction locally on CPU.
- FR-5: The system shall return disease label, confidence score, and optional
  top alternative predictions.
- FR-6: The system shall generate remedy recommendations that include immediate
  actions, sustainable farming practices, prevention, and expert escalation
  guidance.
- FR-7: The farmer dashboard shall display diagnosis history, confidence,
  recommendations, timestamps, and image references.
- FR-8: The system shall store diagnosis results in SQLite using validated
  schemas.
- FR-9: The workflow shall provide useful messages for corrupted images, missing
  model artifacts, low-confidence predictions, and local inference errors.
- FR-10: The core diagnosis and dashboard history workflow shall work without
  network access after required local assets are installed.

## Non Functional Requirements

- NFR-1: No runtime network call is allowed for disease detection.
- NFR-2: Inference must be CPU-only and must not require CUDA, ROCm, or Vulkan.
- NFR-3: Farmer-facing responses should be understandable without technical AI
  language.
- NFR-4: Diagnosis records must avoid storing secrets or unnecessary personal
  data.
- NFR-5: The API, database, and JSON report schema must remain consistent.
- NFR-6: The flow should complete within a practical field-use latency target on
  commodity laptops where model artifacts are available.

## User Stories

- As a farmer, I want to upload a leaf image so I can understand possible crop
  disease symptoms while offline.
- As an agricultural expert, I want confidence scores and alternatives so I can
  judge whether field inspection is needed.
- As a farmer, I want remedy recommendations that include safe immediate action
  and sustainable prevention steps.
- As an extension officer, I want dashboard history so I can track crop health
  across visits and export reports.
- As a user in an emergency, I want low-confidence or severe cases to point me
  toward expert help and emergency SOS workflows.

## Acceptance Criteria

- Given a valid crop image and installed local model, the API returns a disease
  prediction, confidence score, and recommendation payload.
- Given a low-confidence prediction, the UI highlights uncertainty and suggests
  expert review rather than presenting a definitive diagnosis.
- Given an invalid image, the API returns a clear validation error and stores no
  diagnosis record.
- Given no network connection, the installed local workflow still supports image
  analysis and dashboard history.
- Given a completed diagnosis, SQLite contains a record aligned with the API
  response schema.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Misclassification of disease | Wrong treatment may harm crop health | Show confidence, alternatives, and expert escalation |
| Missing local model file | Farmer cannot run diagnosis | Startup checks and clear setup documentation |
| Unsafe remedy text | Farmer safety risk | Use bounded recommendation schema and safety notes |
| Large image upload | Slow or failed diagnosis | Enforce size limits and preprocessing |
| Offline browser cache stale | Dashboard inconsistency | Version cache and expose refresh/retry state |

## Dependencies

- FastAPI backend endpoint for diagnosis.
- Image preprocessing service.
- TensorFlow Lite CPU model artifact in `models/`.
- Local recommendation service or curated remedy mapping.
- SQLite persistence layer.
- Farmer dashboard frontend.

## Security Considerations

- Validate and sanitize all image uploads.
- Do not execute or trust embedded image metadata.
- Keep model files and runtime databases out of Git.
- Avoid logging farmer location, image contents, or emergency SOS details unless
  required for local troubleshooting.
- Run Gitleaks, Bandit, Ruff, Mypy, and Pytest in CI.

## API Changes

Proposed endpoint:

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/v1/diagnose` | Upload image and receive disease prediction |
| `GET` | `/api/v1/history` | List farmer dashboard diagnosis history |
| `GET` | `/api/v1/history/{id}` | Retrieve one diagnosis report |

## Database Changes

Diagnosis persistence should include:

- Diagnosis ID
- Timestamp
- Image path or local image reference
- Crop type when available
- Disease prediction
- Confidence score
- Remedy recommendation JSON
- Model metadata
- Optional location/weather context only when explicitly provided

## Testing Strategy

- Unit test image validation and preprocessing.
- Unit test inference service with mocked TensorFlow Lite output.
- Unit test recommendation schema validation.
- Integration test diagnosis API success and error paths.
- Integration test SQLite persistence and dashboard history retrieval.
- Verify offline behavior by ensuring no runtime network dependency exists.

