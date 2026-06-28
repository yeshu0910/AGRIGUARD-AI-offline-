# Tasks: [Feature Name]

## Planning

- [ ] Confirm farmer and agricultural expert user stories.
- [ ] Review offline-first, CPU-only, privacy, and accessibility constraints.
- [ ] Define acceptance criteria and repository checker requirements.

## Backend

- [ ] Add or update FastAPI routes and Pydantic schemas.
- [ ] Validate image uploads, query parameters, and JSON payloads.
- [ ] Implement structured error responses for farmer-facing workflows.

## Frontend

- [ ] Build responsive UI for mobile and desktop field use.
- [ ] Add accessible controls, loading states, and error recovery.
- [ ] Preserve dashboard functionality for crop health history and reports.

## AI

- [ ] Validate local model loading from `models/`.
- [ ] Run CPU-only image analysis and disease prediction.
- [ ] Return confidence scores and explainable AI recommendations.
- [ ] Handle low-confidence or unavailable-model states safely.

## Database

- [ ] Update SQLite schema or migrations if required.
- [ ] Keep API, ORM, and JSON report schemas aligned.
- [ ] Serialize writes that affect diagnosis, weather, SOS, or report records.

## Testing

- [ ] Add unit tests for validation and service logic.
- [ ] Add integration tests for API and dashboard data flow.
- [ ] Mock llama.cpp and local model binaries where needed.
- [ ] Run `ruff check .`, `mypy backend/`, and `pytest`.

## Documentation

- [ ] Update `.specify/specs/` with decisions and acceptance criteria.
- [ ] Update `docs/` for farmers, agricultural experts, deployment, or APIs.
- [ ] Document model, weather, emergency SOS, and image analysis limitations.

## Deployment

- [ ] Verify `.gitignore` excludes model artifacts and runtime databases.
- [ ] Run security and secret scanning.
- [ ] Generate release notes/changelog.
- [ ] Package offline deployment artifacts.

