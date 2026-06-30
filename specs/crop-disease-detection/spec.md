# Feature Specification: Crop Disease Detection

## Feature Overview

Allow farmers and agricultural experts to upload leaf images and receive instant,
offline disease diagnosis with structured treatment recommendations.

## Problem Statement

Smallholder farmers lack access to agricultural experts. Sending samples to labs
takes days. An offline-first AI solution running on CPU provides instant diagnosis
without internet dependency.

## Goals

- Enable one-click disease detection from leaf images
- Provide confidence scores for diagnosis
- Generate structured chemical and organic treatment recommendations
- Maintain full offline capability

## Non Goals

- Object detection (bounding boxes) — not needed for single-leaf diagnosis
- Cloud synchronization — all data stays on-device

## Functional Requirements

- FR-1: Accept image upload (JPEG, PNG) via REST API and web UI
- FR-2: Run TFLite model inference on CPU
- FR-3: Map model output to crop and disease labels
- FR-4: Return structured JSON with disease, confidence, severity, treatments

## Non Functional Requirements

- NFR-1: Offline-first — no network calls in inference path
- NFR-2: CPU-only — no GPU dependencies
- NFR-3: Inference under 5 seconds on modern CPU

## User Stories

- As a farmer, I want to photograph a diseased leaf and get an immediate diagnosis
- As an extension officer, I want confidence scores to validate the diagnosis

## Acceptance Criteria

- Given a valid leaf image, when POST /detect is called, then return 200 with diagnosis
- Given a missing file, when POST /detect is called, then return 422
- Given model unavailable, when POST /detect is called, then return 503

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Model misprediction | Wrong treatment | Confidence filtering + fallback reports |
| Corrupted image | Failed inference | Input validation + error handling |

## API Changes

| Method | Path | Request | Response | Notes |
|--------|------|---------|----------|-------|
| POST | /detect | multipart image | JSON diagnosis | Main detection endpoint |

## Testing Strategy

- Unit tests for label parsing, recommendation building
- Integration tests with mocked TFLite interpreter
- End-to-end test with sample image