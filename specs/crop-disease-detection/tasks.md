# Tasks: Crop Disease Detection

## Planning

- [ ] Confirm supported crops, diseases, and image formats.
- [ ] Define confidence thresholds for safe farmer guidance.
- [ ] Review recommendation language with agricultural experts.

## Backend

- [ ] Add diagnosis API request validation.
- [ ] Add structured prediction and error response schemas.
- [ ] Add local report assembly for disease, confidence, and remedies.

## Frontend

- [ ] Add image upload or camera capture flow.
- [ ] Show loading, success, low-confidence, and error states.
- [ ] Display diagnosis history in the farmer dashboard.

## AI

- [ ] Load local CPU-only model from `models/`.
- [ ] Normalize images consistently before inference.
- [ ] Return disease prediction and confidence score.
- [ ] Provide safe fallback messaging for uncertain results.

## Database

- [ ] Persist diagnosis ID, timestamp, image reference, disease, confidence, and
  recommendation JSON.
- [ ] Keep SQLite, API, and report schemas aligned.
- [ ] Serialize diagnosis writes.

## Testing

- [ ] Test valid image diagnosis.
- [ ] Test invalid image rejection.
- [ ] Test missing model behavior.
- [ ] Test low-confidence messaging.
- [ ] Test dashboard history retrieval.

## Documentation

- [ ] Update farmer-facing diagnosis instructions.
- [ ] Document offline model setup.
- [ ] Document AI recommendation limits and expert escalation.

## Deployment

- [ ] Run Ruff lint and format checks.
- [ ] Run Mypy, Pytest, Bandit, and Gitleaks.
- [ ] Generate changelog with Git-Cliff.

