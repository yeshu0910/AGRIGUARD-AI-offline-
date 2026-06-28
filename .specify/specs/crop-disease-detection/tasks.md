# Tasks: Crop Disease Detection

## Planning

- [ ] Confirm disease labels, crop coverage, and supported image formats.
- [ ] Review farmer-first copy with agricultural experts.
- [ ] Define confidence thresholds for normal, uncertain, and expert-review
  outcomes.

## Backend

- [ ] Add `POST /api/v1/diagnose` request validation.
- [ ] Add structured success and error response schemas.
- [ ] Add local report assembly for prediction, confidence, and remedies.
- [ ] Ensure no network calls exist in diagnosis runtime paths.

## Frontend

- [ ] Add image upload/camera entry point.
- [ ] Show progress, result, confidence, and remedy recommendation states.
- [ ] Add dashboard history for crop health diagnoses.
- [ ] Add accessible error messages for invalid image and missing model states.

## AI

- [ ] Load TensorFlow Lite model from `models/`.
- [ ] Normalize images consistently before inference.
- [ ] Return top prediction and confidence score.
- [ ] Handle low-confidence predictions with expert escalation guidance.

## Database

- [ ] Persist diagnosis ID, timestamp, image reference, disease, confidence, and
  recommendation JSON.
- [ ] Keep SQLite schema aligned with Pydantic/API schemas.
- [ ] Serialize writes to protect local diagnosis history.

## Testing

- [ ] Test valid image diagnosis flow.
- [ ] Test invalid image rejection.
- [ ] Test missing model error handling.
- [ ] Test low-confidence response behavior.
- [ ] Test dashboard history retrieval.
- [ ] Run `pytest backend/tests/` and integration tests where available.

## Documentation

- [ ] Update farmer-facing diagnosis instructions.
- [ ] Document model placement and offline setup.
- [ ] Document AI recommendation limitations and safety guidance.
- [ ] Update API/database docs if schemas change.

## Deployment

- [ ] Verify model artifacts and runtime DB files are gitignored.
- [ ] Run Ruff, Mypy, Bandit, Gitleaks, Pytest, and coverage.
- [ ] Generate Git-Cliff changelog before release.
- [ ] Package offline deployment bundle for field demonstrations.

