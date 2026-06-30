# Feature Specification: Crop Disease Detection

## Feature Overview

AgriGuard AI crop disease detection helps farmers and agricultural experts
upload crop or leaf images, run offline diagnosis, review confidence scores, and
receive structured treatment recommendations.

## Problem Statement

Farmers in low-connectivity areas need fast image analysis when leaf symptoms
appear. Cloud tools can fail in the field, expose private farm data, or provide
unclear recommendations. An offline-first AI workflow running on CPU gives
farmers faster guidance without internet dependency.

## Goals

- Accept crop image uploads from the REST API and farmer dashboard.
- Run CPU-only disease prediction with local TFLite model artifacts.
- Map model output to crop and disease labels.
- Return disease label, confidence score, severity, and remedy recommendation.
- Store diagnosis history for offline dashboard review.
- Provide safe error handling for invalid images, missing models, and uncertain
  predictions.

## Non Goals

- Cloud-based AI inference or synchronization.
- Object detection with bounding boxes for the initial single-leaf workflow.
- Replacing agricultural experts for severe or ambiguous symptoms.
- Automatic treatment purchase, pesticide application, or emergency dispatch.

## Functional Requirements

- FR-1: Accept JPEG and PNG image uploads via REST API and web UI.
- FR-2: Validate file type, file size, and readable image content.
- FR-3: Preprocess images into the model input shape.
- FR-4: Run TFLite model inference on CPU.
- FR-5: Map model output to crop and disease labels.
- FR-6: Return structured JSON with disease, confidence, severity, and
  treatments.
- FR-7: Generate remedy guidance with immediate action, prevention, safety
  notes, and sustainable farming practices.
- FR-8: Show diagnosis history for farmers and extension workers.
- FR-9: Preserve offline support for image analysis and history.

## Non Functional Requirements

- NFR-1: Runtime disease detection must not require network access.
- NFR-2: Inference must remain CPU-only with no GPU dependencies.
- NFR-3: Inference should complete under 5 seconds on a modern CPU.
- NFR-4: AI recommendations must be explainable and confidence-aware.
- NFR-5: Farmer images, weather context, location context, and emergency SOS data
  must remain private unless explicitly exported.
- NFR-6: API, database, and JSON report schemas must stay aligned.
- NFR-7: The interface must be accessible on mobile and desktop field devices.

## User Stories

- As a farmer, I want to photograph a diseased leaf and get an immediate
  diagnosis.
- As an extension officer, I want confidence scores to validate the diagnosis.
- As a farmer, I want low-confidence results to clearly advise expert review.
- As a returning user, I want stored diagnosis history available offline.

## Acceptance Criteria

- Given a valid leaf image, when `POST /detect` is called, then the API returns
  200 with diagnosis, confidence, severity, and treatment guidance.
- Given a missing file, when `POST /detect` is called, then the API returns 422.
- Given an invalid image, when `POST /detect` is called, then the API returns a
  validation error and does not create a diagnosis.
- Given a missing model, when `POST /detect` is called, then the API returns 503.
- Given a low-confidence prediction, then the response clearly advises expert
  review.
- Given stored diagnosis records, then the dashboard can display history while
  offline.
- No cloud AI SDK or external API call is required for the core workflow.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Model misprediction | Wrong treatment | Confidence filtering and fallback reports |
| Corrupted image | Failed inference | Input validation and error handling |
| Missing model artifact | Unavailable detection | Startup checks and setup documentation |
| Unsafe recommendation | Farmer harm | Structured schema and safety notes |

## API Changes

| Method | Path | Request | Response | Notes |
|--------|------|---------|----------|-------|
| POST | `/detect` | Multipart image | JSON diagnosis | Main detection endpoint |

## Security Considerations

- Sanitize all image uploads.
- Do not trust image metadata.
- Do not commit model files, runtime databases, secrets, API keys, JWT tokens, or
  cloud credentials.
- Avoid logging sensitive farm, weather, location, or emergency SOS details.

## Testing Strategy

- Unit test image validation and preprocessing.
- Unit test label parsing and recommendation building.
- Unit test disease prediction service with mocked model output.
- Unit test recommendation schema validation.
- Integration test diagnosis API success and failure paths.
- Integration test SQLite persistence and dashboard history.
- End-to-end test with a sample image.
