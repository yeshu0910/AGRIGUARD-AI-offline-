# Tasks: Crop Disease Detection

## Completed

- [x] Create FastAPI application structure in `AgriGuard/backend/app.py`.
- [x] Implement image preprocessing pipeline in `AgriGuard/backend/preprocess.py`.
- [x] Create TFLite model wrapper in `AgriGuard/backend/detect.py`.
- [x] Implement PlantVillage label parser in `AgriGuard/backend/crop_detector.py`.
- [x] Create SQLite database layer in `AgriGuard/backend/database.py`.
- [x] Implement curated recommendation knowledge base in
  `AgriGuard/backend/recommendation.py`.
- [x] Add local LLM integration via llama.cpp in `AgriGuard/backend/llm.py`.
- [x] Write unit tests for backend components.
- [x] Add integration tests with mocked inference.
- [x] Document API endpoints.

## Planning

- [ ] Confirm supported crops, diseases, and image formats.
- [ ] Define confidence thresholds for safe farmer guidance.
- [ ] Review recommendation language with agricultural experts.

## Backend

- [ ] Verify diagnosis API request validation against the public schema.
- [ ] Verify structured prediction and error response schemas.
- [ ] Verify local report assembly for disease, confidence, and remedies.

## Frontend

- [ ] Add or verify image upload and camera capture flow.
- [ ] Show loading, success, low-confidence, and error states.
- [ ] Display diagnosis history in the farmer dashboard.

## AI

- [ ] Verify local CPU-only model loading from `models/`.
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
