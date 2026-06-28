# Feature Specification: Crop Disease Detection

## Overview

AgriGuard AI crop disease detection helps farmers and agricultural experts
analyze crop images offline, predict likely disease, review confidence scores,
and receive practical AI recommendations for crop health and sustainable
farming.

## Problem

Farmers in low-connectivity areas need fast image analysis when leaf symptoms
appear. Cloud tools can fail in the field, expose private farm data, or provide
unclear recommendations. AgriGuard AI must keep diagnosis local, explainable,
and safe.

## Goals

- Accept crop image uploads from the farmer dashboard.
- Run CPU-only disease prediction with local model artifacts.
- Return disease label, confidence score, and remedy recommendation.
- Store diagnosis history for offline dashboard review.
- Provide safe error handling for invalid images, missing models, and uncertain
  predictions.

## Non Goals

- Cloud-based AI inference.
- Replacing agricultural experts for severe or ambiguous symptoms.
- Automatic treatment purchase, pesticide application, or emergency dispatch.

## Functional Requirements

- The system shall accept JPEG and PNG crop images.
- The system shall validate file type, file size, and readable image content.
- The system shall preprocess images into the model input shape.
- The system shall run local CPU-only disease prediction.
- The system shall return confidence scores with predictions.
- The system shall generate remedy guidance with immediate action, prevention,
  safety notes, and sustainable farming practices.
- The dashboard shall show diagnosis history for farmers and extension workers.
- The system shall preserve offline support for image analysis and history.

## Non Functional Requirements

- Runtime disease detection must not require network access.
- AI recommendations must be explainable and confidence-aware.
- Farmer images, weather context, location context, and emergency SOS data must
  remain private unless explicitly exported.
- API, database, and JSON report schemas must stay aligned.
- The interface must be accessible on mobile and desktop field devices.

## Acceptance Criteria

- A valid crop image returns a disease prediction, confidence score, and remedy
  recommendation.
- A low-confidence prediction clearly advises expert review.
- An invalid image returns a validation error and does not create a diagnosis.
- The dashboard can display stored diagnosis history while offline.
- No cloud AI SDK or external API call is required for the core workflow.

## Security Considerations

- Sanitize all image uploads.
- Do not trust image metadata.
- Do not commit model files, runtime databases, secrets, API keys, JWT tokens, or
  cloud credentials.
- Avoid logging sensitive farm, weather, location, or emergency SOS details.

## Testing Strategy

- Unit test image validation and preprocessing.
- Unit test disease prediction service with mocked model output.
- Unit test recommendation schema validation.
- Integration test diagnosis API success and failure paths.
- Integration test SQLite persistence and dashboard history.

